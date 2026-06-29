#!/usr/bin/env python3
"""
Stage 4 — Risk Surface Filtering + CLQ Spatial Divergence Analysis

Two independent parts in one script:

  Part 1 (production pipeline)
    Turns the raw GAT risk surface into a clean routing input.
    Extreme outliers are capped, then low-signal segments are zeroed out so
    the router sees a binary hotspot signal rather than a noisy continuum.

  Part 2 (post-hoc thesis results)
    Colocation Quotient (CLQ) analysis: tests whether motorcycle hotspots and
    HGV hotspots (and other pairs) occupy the same road segments or diverge
    spatially.  CLQ < 1 means divergence — the core empirical claim of the
    thesis.  This part produces the divergence maps and statistics that go in
    the results section; it does NOT gate the router.

Usage
-----
  python filter_and_clq.py                    # default: london map, 99 permutations
  python filter_and_clq.py --map_city manchester --n_permutations 999
  python filter_and_clq.py --threshold 0.90   # tighter: top 10% as hotspots
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tqdm import tqdm

# ── Constants ─────────────────────────────────────────────────────────────────

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']

# 99th percentile cap: segments with near-zero AADF exposure produce
# astronomically large risk rates (dividing by a tiny denominator).  These
# are data artifacts, not genuinely the most dangerous roads in Britain.
CAP_PERCENTILE = 0.99

# Default hotspot threshold: top 15% of segments per type.
# This is a Stage 6 tuning parameter — it controls how many segments the
# router treats as "elevated risk".  Start at 0.85, revise after evaluation.
DEFAULT_THRESHOLD = 0.85

# City bounding boxes for the detail maps: (lon_min, lat_min, lon_max, lat_max)
CITIES = {
    'london':     (-0.51, 51.28,  0.33, 51.72),
    'birmingham': (-2.05, 52.35, -1.75, 52.60),
    'manchester': (-2.40, 53.33, -2.10, 53.55),
    'leeds':      (-1.70, 53.72, -1.45, 53.88),
}

CODE_DIR = Path(__file__).parent.parent
OUTPUTS  = CODE_DIR / 'outputs'

# Consistent colours for all 5 vehicle types — shared across map and legend
TYPE_COLOURS = {
    'car':        '#3498db',   # blue
    'motorcycle': '#e74c3c',   # red
    'cycle':      '#2ecc71',   # green
    'lgv':        '#f39c12',   # orange
    'hgv':        '#8e44ad',   # purple
}
OVERLAP_COLOUR  = '#ffffff'   # white — segments where 2+ selected types co-locate
NEITHER_COLOUR  = '#d0d0d0'   # grey  — background road network


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description='Stage 4: filter risk surface + CLQ analysis')
    p.add_argument(
        '--threshold', type=float, default=DEFAULT_THRESHOLD,
        help='Percentile below which risk is zeroed (default: 0.85 = top 15%%)')
    p.add_argument(
        '--map_city', choices=list(CITIES.keys()), default='london',
        help='City for the detailed hotspot map (default: london)')
    p.add_argument(
        '--n_permutations', type=int, default=99,
        help='Monte Carlo permutations for CLQ p-values (default: 99; use 999 for publication-grade)')
    p.add_argument(
        '--map_types', nargs='+', choices=VEHICLE_TYPES, default=VEHICLE_TYPES,
        help='Which vehicle types to show on the map (default: all 5). '
             'Pass 2-5 names e.g. --map_types motorcycle hgv car')
    return p.parse_args()


# ── Part 1: Filtering ─────────────────────────────────────────────────────────

def filter_risk_surface(df: pd.DataFrame, threshold_pct: float) -> pd.DataFrame:
    """
    Applies a two-step cleaning pass to the raw GAT risk surface.

    Step 1 — Percentile cap (per type, on non-zero values only)
      Why non-zero only: segments with zero AADF exposure already have
      risk_score = 0 (set in Stage 3 by the np.where guard).  Including them
      in the percentile would drag the 99th percentile toward zero and cap
      nothing.  We compute the cap on the segments that actually have a
      meaningful denominator.

    Step 2 — Threshold (per type, on the capped scores)
      Everything at or below the Xth percentile is set to 0.  The router
      then only needs to penalise the top (1-X)% of segments.  This keeps
      the routing problem tractable and makes the hotspot signal crisp —
      rather than weighting every segment slightly differently, the router
      sees: is this segment elevated, or not?

      WHY zero and not a fallback aggregate score: the build spec allows
      either.  Zero is cleaner — if a segment is below threshold it is not
      penalised at all, which is conservative.  The aggregate-fallback
      option (weight below-threshold segments by the cross-type mean) adds
      complexity with marginal routing benefit; revisit in Stage 6 if the
      evaluation shows the router is taking bad routes through genuinely
      risky but below-threshold segments.
    """
    print(f'\nFiltering risk surface (cap=p{CAP_PERCENTILE*100:.0f}, '
          f'threshold=p{threshold_pct*100:.0f} → top {(1-threshold_pct)*100:.0f}% are hotspots)')
    print(f'  {"Type":<12} {"Cap value":>12} {"Threshold":>12} {"Hotspots":>10}')
    print(f'  ' + '-'*52)

    parts = []
    for t in VEHICLE_TYPES:
        sub = df[df['vehicle_type'] == t].copy()

        # Step 1: cap at 99th percentile (non-zero scores only)
        nonzero_scores = sub.loc[sub['risk_score'] > 0, 'risk_score']
        cap_val = nonzero_scores.quantile(CAP_PERCENTILE) if len(nonzero_scores) > 0 else 0.0
        sub['risk_score'] = sub['risk_score'].clip(upper=cap_val)

        # Step 2: threshold — zero out everything at or below the threshold percentile
        threshold_val = sub['risk_score'].quantile(threshold_pct)
        sub.loc[sub['risk_score'] <= threshold_val, 'risk_score'] = 0.0

        # Flag hotspots (non-zero after thresholding) as a convenience column
        sub['is_hotspot'] = (sub['risk_score'] > 0).astype(np.int8)

        n_hot = int(sub['is_hotspot'].sum())
        print(f'  {t:<12} {cap_val:>12.6f} {threshold_val:>12.6f} {n_hot:>10,}')
        parts.append(sub)

    return pd.concat(parts, ignore_index=True)


# ── Part 2: CLQ analysis ──────────────────────────────────────────────────────

def _clq_one_pair(
    a_idx: np.ndarray,
    b_idx: np.ndarray,
    N: int,
    n_permutations: int,
) -> dict:
    """
    Colocation Quotient for one ordered type pair (A → B).

    What the CLQ measures
    ---------------------
    "Of all the segments that are hotspots for type A, what fraction are
    also hotspots for type B?  And is that fraction more or less than we
    would expect if type B's hotspots were placed randomly across all N
    segments?"

      observed  = |A ∩ B| / |A|
      expected  = |B| / N          (random-placement baseline)
      CLQ       = observed / expected

    CLQ < 1 → divergence: A and B avoid each other spatially
    CLQ > 1 → co-location: A and B cluster together
    CLQ = 1 → spatially independent

    Monte Carlo permutation test (Hu 2018)
    ---------------------------------------
    Null hypothesis: type B hotspots are placed randomly across all N segments.
    We simulate this by drawing |B| random segments N_PERM times and computing
    the overlap with A each time — this builds the null distribution for the
    overlap fraction.

    p-value = fraction of null overlaps ≤ observed overlap.
    A small p-value (< 0.05) means: the divergence (low overlap) is unlikely
    to arise by chance → the types genuinely occupy different spaces.

    WHY Monte Carlo not a parametric test:
    A hypergeometric test would be faster but assumes the segments are drawn
    independently.  Road segments are spatially autocorrelated (crashes cluster
    in junctions, roundabouts, etc.) so that independence assumption is
    violated.  Monte Carlo makes no distributional assumption — it is the
    standard for network spatial statistics (Hu et al. 2018, TR-C).

    Implementation note:
    Using a boolean mask array rather than Python sets: mask_a[rand_b_idx].sum()
    is a single numpy operation (~0.01s) versus set intersection which is
    O(|rand_b|) in Python-space and ~10× slower.
    """
    n_a = len(a_idx)
    n_b = len(b_idx)
    if n_a == 0 or n_b == 0:
        return {
            'observed': 0.0, 'expected': 0.0,
            'clq': float('nan'), 'p_value': float('nan'),
            'n_overlap': 0, 'n_a': n_a, 'n_b': n_b,
        }

    # Vectorised intersection via a boolean mask over all N segments
    mask_a = np.zeros(N, dtype=bool)
    mask_a[a_idx] = True

    observed_k    = int(mask_a[b_idx].sum())
    observed_frac = observed_k / n_a
    expected_frac = n_b / N           # analytical expected under random placement

    # Monte Carlo null distribution
    null_overlaps = np.empty(n_permutations)
    for i in range(n_permutations):
        rand_b_idx     = np.random.choice(N, size=n_b, replace=False)
        null_overlaps[i] = mask_a[rand_b_idx].sum() / n_a

    # p-value for divergence: fraction of null runs with overlap ≤ observed
    # Interpretation: if p < 0.05, the low overlap is not explainable by chance
    p_value = float((null_overlaps <= observed_frac).mean())

    return {
        'observed':  observed_frac,
        'expected':  expected_frac,
        'clq':       observed_frac / expected_frac if expected_frac > 0 else float('nan'),
        'p_value':   p_value,
        'n_overlap': observed_k,
        'n_a':       n_a,
        'n_b':       n_b,
    }


def run_clq(filtered_df: pd.DataFrame, n_permutations: int):
    """
    Runs CLQ for all thesis-relevant vehicle type pairs.

    Mapping segment UUIDs to integer indices:
    The CLQ computation needs to answer "is segment X also in set Y?" millions
    of times.  Python sets of UUID strings can do this, but numpy boolean masks
    are ~10× faster.  We build a single seg_to_idx dict once here and reuse it
    for all pairs.  The 'car' type is used as the master segment list because
    every segment in the road network appears in the car rows (car has the
    fewest zero-AADF exclusions among the VEHICLE_TYPES).

    Returns:
      clq_df    — DataFrame of CLQ results, one row per pair
      hotspots  — dict {vehicle_type: [segment_id, ...]} for mapping
    """
    # Build integer index (0..N-1) from the car rows (all segments present)
    all_ids    = (filtered_df[filtered_df['vehicle_type'] == 'car']
                  ['segment_id'].reset_index(drop=True))
    seg_to_idx = {sid: i for i, sid in enumerate(all_ids)}
    N          = len(all_ids)

    # Convert hotspot segment_ids to integer indices for each type
    hotspot_idx = {}
    hotspots    = {}   # kept as strings for the mapping step
    for t in VEHICLE_TYPES:
        hot_ids = (filtered_df[(filtered_df['vehicle_type'] == t) &
                               (filtered_df['is_hotspot'] == 1)]['segment_id'].tolist())
        hotspots[t]    = hot_ids
        hotspot_idx[t] = np.array(
            [seg_to_idx[s] for s in hot_ids if s in seg_to_idx], dtype=np.int64)

    # All 10 unique pairs from 5 types (C(5,2) = 10).
    # The thesis claim is that risk diverges across ALL vehicle types — not
    # just motorcycle vs HGV.  Every pair gets equal treatment.
    pairs = [
        ('motorcycle', 'hgv'),
        ('motorcycle', 'car'),
        ('motorcycle', 'cycle'),
        ('motorcycle', 'lgv'),
        ('hgv',        'car'),
        ('hgv',        'cycle'),
        ('hgv',        'lgv'),
        ('car',        'cycle'),
        ('car',        'lgv'),
        ('cycle',      'lgv'),
    ]

    print(f'\nCLQ Analysis ({n_permutations} Monte Carlo permutations per pair)')
    print(f'  CLQ < 1 = diverge  |  CLQ > 1 = co-locate  |  CLQ = 1 = random')
    print()
    print(f'  {"Pair":<22} {"Obs":>8} {"Exp":>8} {"CLQ":>7} {"p-val":>8}  {"Result":<16}  time')
    print(f'  ' + '-'*72)

    rows = []
    for type_a, type_b in pairs:
        t0  = time.time()
        r   = _clq_one_pair(hotspot_idx[type_a], hotspot_idx[type_b], N, n_permutations)
        ela = time.time() - t0

        sig    = ' ★p<0.05' if r['p_value'] < 0.05 else ''
        result = 'DIVERGE' if r['clq'] < 1 else 'co-locate'
        print(f'  {type_a}→{type_b:<17} '
              f'{r["observed"]:>8.4f} {r["expected"]:>8.4f} '
              f'{r["clq"]:>7.3f} {r["p_value"]:>8.4f}  '
              f'{result:<16}{sig}  ({ela:.1f}s)')
        rows.append({'type_a': type_a, 'type_b': type_b, **r})

    return pd.DataFrame(rows), hotspots


# ── Part 3: Maps ──────────────────────────────────────────────────────────────

def make_divergence_map(
    hotspots_selected: dict,
    centroids_df: pd.DataFrame,
    title: str,
    output_path: Path,
) -> None:
    """
    Scatter plot of hotspot centroids for any subset of vehicle types.

    hotspots_selected: {vehicle_type: set_of_segment_ids}
      Pass any 1–5 types.  Controlled by --map_types at the CLI.

    Category logic per segment:
      - In exactly 1 selected type → that type's colour
      - In 2 or more selected types → OVERLAP_COLOUR (white) drawn on top
      - In none → NEITHER_COLOUR (grey background)

    WHY scatter centroids and not road geometry:
      Plotting 590k LineString geometries takes several minutes and produces
      an unreadable blob at national scale.  Centroid dots take ~2 seconds
      and are visually indistinguishable from lines at thesis-figure resolution.

    WHY draw overlap last:
      Overlap is the key visual signal — segments where types share the same
      dangerous road.  Drawing it last keeps it on top of all type dots.
    """
    type_list = list(hotspots_selected.keys())

    df = centroids_df.copy()

    # Flag which segments belong to each selected type (vectorised isin lookup)
    membership = {t: df['segment_id'].isin(hotspots_selected[t]) for t in type_list}

    # Count how many selected types each segment belongs to
    n_types = sum(m.astype(int) for m in membership.values())

    # Assign category: single-type → type name; multi-type → 'overlap'
    df['cat'] = 'neither'
    for t in type_list:
        df.loc[membership[t] & (n_types == 1), 'cat'] = t
    df.loc[n_types >= 2, 'cat'] = 'overlap'

    # Draw order: background first, type dots next, overlap on top
    draw_order = ['neither'] + type_list + ['overlap']

    _, ax = plt.subplots(figsize=(10, 14))

    for cat_name in draw_order:
        sub = df[df['cat'] == cat_name]
        if sub.empty:
            continue
        if cat_name == 'neither':
            colour, size, alpha = NEITHER_COLOUR, 0.2, 0.35
        elif cat_name == 'overlap':
            colour, size, alpha = OVERLAP_COLOUR, 3.0, 1.0
        else:
            colour, size, alpha = TYPE_COLOURS[cat_name], 1.2, 0.85

        ax.scatter(
            sub['centroid_lon'], sub['centroid_lat'],
            c=colour, s=size, alpha=alpha,
            linewidths=0, rasterized=True,
        )

    # Legend — one entry per selected type + overlap row if any co-location exists
    patches = [
        mpatches.Patch(color=TYPE_COLOURS[t],
                       label=f'{t.capitalize()}  ({int((df["cat"] == t).sum()):,})')
        for t in type_list
    ]
    n_overlap = int((df['cat'] == 'overlap').sum())
    if n_overlap > 0:
        patches.append(mpatches.Patch(color=OVERLAP_COLOUR,
                                      label=f'Overlap 2+ types  ({n_overlap:,})'))
    patches.append(mpatches.Patch(color=NEITHER_COLOUR, label='Neither'))

    ax.legend(handles=patches, loc='lower left', fontsize=9, framealpha=0.92)
    ax.set_title(title, fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Longitude', fontsize=9)
    ax.set_ylabel('Latitude',  fontsize=9)
    ax.set_aspect('equal')
    ax.tick_params(labelsize=8)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f'  Saved → {output_path}')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    np.random.seed(42)

    # ── 1. Load risk scores ───────────────────────────────────────────────────
    print('Loading risk_scores.csv...', flush=True)
    t0 = time.time()
    df = pd.read_csv(OUTPUTS / 'risk_scores.csv')
    print(f'  {len(df):,} rows  ({time.time()-t0:.1f}s)')

    # ── 2. Filter → risk_surface_filtered.csv ────────────────────────────────
    filtered_df = filter_risk_surface(df, args.threshold)
    del df   # free ~3 GB before the map step

    out_filtered = OUTPUTS / 'risk_surface_filtered.csv'
    filtered_df[['segment_id', 'vehicle_type', 'risk_score', 'is_hotspot']].to_csv(
        out_filtered, index=False)
    total_hotspots = int(filtered_df['is_hotspot'].sum())
    print(f'\nSaved → {out_filtered}')
    print(f'  {len(filtered_df):,} rows  |  {total_hotspots:,} hotspot cells across all types')

    # ── 3. CLQ analysis → clq_results.csv ───────────────────────────────────
    clq_df, hotspots = run_clq(filtered_df, args.n_permutations)

    out_clq = OUTPUTS / 'clq_results.csv'
    clq_df.to_csv(out_clq, index=False)
    print(f'\nSaved → {out_clq}')

    # ── 4. Maps ───────────────────────────────────────────────────────────────
    print('\nGenerating maps...')
    print('  Loading segment centroids...', flush=True)
    t0 = time.time()

    # Load segments.gpkg for centroid_lon / centroid_lat.
    # We drop the geometry column immediately — we only need the two centroid
    # floats, not the full LineString geometry.  Loading and then dropping is
    # faster than re-processing the CSV because the centroid columns are stored
    # directly in the gpkg attribute table.
    segs_gdf = gpd.read_file(OUTPUTS / 'segments.gpkg')
    segs = pd.DataFrame(segs_gdf[['segment_id', 'centroid_lon', 'centroid_lat']])
    del segs_gdf
    print(f'  {len(segs):,} centroids loaded  ({time.time()-t0:.1f}s)')

    # ── National map: top 1% per selected type ───────────────────────────────
    # At national scale the full 15% hotspot set (~590k dots per type) merges
    # into a solid blob.  Top 1% (~39k dots) shows the urban/motorway/rural
    # split clearly while remaining legible.
    n_top1 = max(1, int(0.01 * len(segs)))
    top1_selected = {
        t: set(filtered_df[filtered_df['vehicle_type'] == t]
               .nlargest(n_top1, 'risk_score')['segment_id'])
        for t in args.map_types
    }
    type_label = ', '.join(t.capitalize() for t in args.map_types)

    background = segs.sample(min(500_000, len(segs)), random_state=42)
    print(f'  Rendering national map (top 1%, types: {type_label})...')
    make_divergence_map(
        top1_selected,
        background,
        title=f'Risk Hotspots — Great Britain, Top 1%\n{type_label}',
        output_path=OUTPUTS / 'map_divergence_national.png',
    )

    # ── City map: full top 15% clipped to bounding box ───────────────────────
    # At city scale the bounding box cuts segment count enough that 15% is legible.
    city      = args.map_city
    lon_min, lat_min, lon_max, lat_max = CITIES[city]
    segs_city = segs[
        (segs['centroid_lon'] >= lon_min) & (segs['centroid_lon'] <= lon_max) &
        (segs['centroid_lat'] >= lat_min) & (segs['centroid_lat'] <= lat_max)
    ].copy()

    city_selected = {t: set(hotspots[t]) for t in args.map_types}
    print(f'  Rendering {city} map ({len(segs_city):,} segments, types: {type_label})...')
    make_divergence_map(
        city_selected,
        segs_city,
        title=f'Risk Hotspots — {city.title()}, Top 15%\n{type_label}',
        output_path=OUTPUTS / f'map_divergence_{city}.png',
    )

    # ── Summary ───────────────────────────────────────────────────────────────
    print('\nStage 4 complete.')
    print(f'  Filtered surface  : {out_filtered}')
    print(f'  CLQ results       : {out_clq}')
    print(f'  National map      : {OUTPUTS}/map_divergence_national.png')
    print(f'  City map          : {OUTPUTS}/map_divergence_{city}.png')

    # Summary: how many pairs show significant divergence?
    n_diverge = (clq_df['clq'] < 1).sum()
    n_sig     = (clq_df['p_value'] < 0.05).sum()
    print(f'\n  {n_diverge}/10 pairs diverge (CLQ < 1)  |  {n_sig}/10 significant at p < 0.05')


if __name__ == '__main__':
    main()
