#!/usr/bin/env python3
"""
Stage 3 — Per-Type Cluster + Share Risk Model  (replaces the GAT)

Produces risk_scores.csv: one row per (segment_id, vehicle_type) with a risk
score used by Stage 4 (filtering) and Stage 5 (routing).

Why this replaces the GAT (see wiki/build/stage-3-cluster-share-engine.md):
the unified GAT collapsed the per-type divergence (cross-type ρ 0.855) because
any signal shared across types pulls every type's estimate toward a common
answer, and because the divergence lives in *location*, not volume. This engine
fixes both at once:

  1. pool sparse crash data by NETWORK LOCATION (per-type BFS clusters), so
     there is enough data per unit to estimate from at all;
  2. predict each type's SHARE of its cluster's all-type crash total (not the
     raw count), which removes the "how busy overall" magnitude that all types
     agree on;
  3. train 5 FULLY SEPARATE models — nothing shared across types anywhere.

Validated leakage-free 2026-07-06 (national out-of-sample ρ=-0.097; validity on
the never-seen 2024 year ≈ validity on the target years). This is the DEPLOYMENT
surface: trained on all history, predicting all segments. Generalisation/leakage
testing is Stage 6 (spatial CV + temporal 2024), not here.

Usage:
  python train.py                # full Great Britain
  python train.py --city london  # quick test on one bbox
"""

import argparse
import time
from collections import deque
from pathlib import Path

import numpy as np
import pandas as pd
import pyogrio
import xgboost as xgb

# ── Constants ─────────────────────────────────────────────────────────────────

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']

# Each crash type's own exposure / traffic column (from the DfT AADF join in
# Stage 2). Used as a per-type feature — kept identical to Stage 2's naming.
AADF_COL = {
    'car':        'cars_and_taxis',
    'motorcycle': 'two_wheeled_motor_vehicles',
    'cycle':      'pedal_cycles',
    'lgv':        'lgvs',
    'hgv':        'all_hgvs',
}

# The single most important guardrail in this file: the years that build the
# CLUSTERS + INPUT FEATURES must be disjoint from the years that form the
# TARGET. If they overlap, the model can copy its own input to its output and
# score perfectly while learning nothing that generalises (the temporal leak we
# hit in the ad-hoc phase). HOLDOUT_YEAR is touched by nothing here — it is
# reserved for the Stage 6 temporal-leakage check.
HISTORY_YEARS = [2020, 2021]   # clusters + input features
TARGET_YEARS  = [2022, 2023]   # training target
HOLDOUT_YEAR  = 2024           # reserved for Stage 6 only — never read here

# A cluster keeps growing over the road network until it has accumulated at
# least this much of a type's HISTORY crash weight — enough data to estimate a
# stable share from. Dense areas → many small clusters; sparse areas (e.g. HGV)
# → few coarse ones. 30 is the validated default.
MIN_CRASHES = 30.0

# Bounding boxes (lon_min, lat_min, lon_max, lat_max, WGS84) for --city testing.
CITIES = {
    'london':     (-0.51, 51.28,  0.33, 51.72),
    'birmingham': (-2.05, 52.35, -1.75, 52.60),
    'manchester': (-2.40, 53.33, -2.10, 53.55),
    'leeds':      (-1.70, 53.72, -1.45, 53.88),
}

CODE_DIR = Path(__file__).parent.parent
OUTPUTS  = CODE_DIR / 'outputs'

# Segment attribute columns the engine reads (no geometry — much lighter).
SEG_COLS = ['segment_id', 'road_class', 'length_m', 'all_motor_vehicles',
            'cars_and_taxis', 'lgvs', 'all_hgvs', 'two_wheeled_motor_vehicles',
            'pedal_cycles', 'aadf_fallback', 'centroid_lon', 'centroid_lat']

# ── Data loading ──────────────────────────────────────────────────────────────

def load_data(city=None):
    """Load the three Stage-2 outputs. With --city, clip all three to one bbox
    (by segment centroid) so a self-contained subgraph is loaded for quick tests.

    We read segment ATTRIBUTES only (read_geometry=False) — the engine never
    needs the polylines, only the columns — which is why 3.96M rows load in ~12s.
    """
    t0 = time.time()
    print('Loading segments.gpkg...', flush=True)
    segments = pyogrio.read_dataframe(OUTPUTS / 'segments.gpkg',
                                      read_geometry=False, columns=SEG_COLS)
    print(f'  {len(segments):,} segments  ({time.time()-t0:.1f}s)')

    if city:
        lon_min, lat_min, lon_max, lat_max = CITIES[city]
        m = ((segments['centroid_lon'] >= lon_min) & (segments['centroid_lon'] <= lon_max) &
             (segments['centroid_lat'] >= lat_min) & (segments['centroid_lat'] <= lat_max))
        segments = segments[m].reset_index(drop=True)
        print(f'  city={city}: {len(segments):,} segments')

    # WHY filter crashes AND edges by the same segment set: under --city we want a
    # self-contained subgraph where every crash and every edge refers to a segment
    # that exists in the filtered node set — otherwise clustering/features break.
    city_ids = set(segments['segment_id']) if city else None

    print('Loading crashes_segmented.csv...', flush=True)
    crashes = pd.read_csv(OUTPUTS / 'crashes_segmented.csv', low_memory=False,
                          usecols=['segment_id', 'vehicle_type',
                                   'severity_weight', 'accident_year'])
    if city:
        crashes = crashes[crashes['segment_id'].isin(city_ids)].reset_index(drop=True)

    print('Loading graph_edges.csv...', flush=True)
    edges = pd.read_csv(OUTPUTS / 'graph_edges.csv')
    if city:
        edges = edges[edges['segment_id_a'].isin(city_ids) &
                      edges['segment_id_b'].isin(city_ids)].reset_index(drop=True)

    return segments, crashes, edges

# ── Crash aggregation ─────────────────────────────────────────────────────────

def severity_matrix(crashes, seg_index, years):
    """Severity-weighted crash sums per (segment, type) over `years`.

    Returns a float32 array of shape [N segments, 5 types] in VEHICLE_TYPES order.
    We call it TWICE with different year lists — once for HISTORY_YEARS (to build
    clusters + input features) and once for TARGET_YEARS (the training target).
    Same logic, disjoint years: this is where the leakage guard is enforced.

    `seg_index` maps segment_id -> row position 0..N-1 (built once in main()).
    `severity_weight` was already set in Stage 1 (fatal=3 / serious=2 / slight=1);
    here we SUM it per (segment, type) — a severity-weighted count, not a raw one.
    """
    type_to_idx = {t: i for i, t in enumerate(VEHICLE_TYPES)}
    c = crashes[crashes['accident_year'].isin(years)].copy()
    c['nidx'] = c['segment_id'].map(seg_index)          # segment -> row
    c['tidx'] = c['vehicle_type'].map(type_to_idx)      # type    -> column
    # Any crash on a segment not in our index (unmatched, or outside a --city
    # bbox) maps to NaN and is dropped here — the referential-integrity handling.
    c = c.dropna(subset=['nidx', 'tidx'])

    out = np.zeros((len(seg_index), len(VEHICLE_TYPES)), dtype=np.float32)
    # np.add.at = vectorised scatter-add: for every crash, add its severity weight
    # into cell [its segment row, its type column]. ~100x faster than a Python
    # loop over ~885k rows, and it correctly ACCUMULATES repeats (5 car crashes on
    # one segment sum into the same cell — plain out[idx]=... would not).
    np.add.at(out, (c['nidx'].astype(int).values, c['tidx'].astype(int).values),
              c['severity_weight'].values.astype(np.float32))
    return out

# ── Adjacency + per-type clustering ─────────────────────────────────────────────

def build_adjacency(edges, seg_index):
    """CSR undirected adjacency over segment row-indices — built once, shared by
    all five types' clustering. graph_edges.csv holds one row per adjacent pair
    (a<b); we add both directions so BFS can traverse either way.

    CSR = two flat int arrays: `neighbors` lists every segment's neighbours back to
    back, and the slice `neighbors[indptr[i]:indptr[i+1]]` is segment i's neighbour
    list. O(1) to reach a node's neighbours with no per-node Python objects — which
    is what makes BFS over 3.96M nodes / ~6.9M edges tractable.
    """
    a = edges['segment_id_a'].map(seg_index).values
    b = edges['segment_id_b'].map(seg_index).values
    valid = ~(pd.isna(a) | pd.isna(b))
    a = a[valid].astype(np.int64)
    b = b[valid].astype(np.int64)

    N = len(seg_index)
    src = np.concatenate([a, b])            # both directions: a->b and b->a
    dst = np.concatenate([b, a])
    order = np.argsort(src, kind='stable')  # group neighbours by source node
    src, dst = src[order], dst[order]
    indptr = np.zeros(N + 1, dtype=np.int64)
    np.add.at(indptr, src + 1, 1)           # count neighbours per node...
    np.cumsum(indptr, out=indptr)           # ...then prefix-sum into offsets
    return indptr, dst.astype(np.int64)


def bfs_clusters(indptr, neighbors, hist_count, min_crashes):
    """Grow discrete, connected clusters over the network for ONE vehicle type.

    Seed at the highest-history unassigned segment, BFS outward claiming
    unassigned neighbours until the cluster's accumulated history crash weight
    reaches `min_crashes` (or its local frontier runs out), then seed the next.
    Sparse regions (e.g. HGV) form large coarse clusters; dense regions form small
    fine ones — adaptive granularity driven purely by data sufficiency, which is
    what lets us estimate a stable per-type share in a cluster anywhere.

    Runs once PER TYPE with that type's own history counts, so each type's clusters
    are shaped by where THAT type actually crashes. Returns cluster_id [N]
    (every reachable segment gets exactly one; isolated segments become singletons).
    """
    N = len(hist_count)
    cluster_id = np.full(N, -1, dtype=np.int64)
    seed_order = np.argsort(-hist_count, kind='stable')   # densest crash spots first

    cid = 0
    for seed in seed_order:
        if cluster_id[seed] != -1:              # already claimed by an earlier cluster
            continue
        q = deque([seed])
        cluster_id[seed] = cid
        acc = hist_count[seed]
        while q and acc < min_crashes:
            u = q.popleft()
            for k in range(indptr[u], indptr[u + 1]):
                v = neighbors[k]
                if cluster_id[v] == -1:
                    cluster_id[v] = cid
                    acc += hist_count[v]
                    q.append(v)
                    if acc >= min_crashes:
                        break
        cid += 1
    return cluster_id

# ── Cluster aggregates + share target ───────────────────────────────────────────

def cluster_frame(cluster_id, hist_sev, target_sev, seg_df, type_idx):
    """Aggregate every segment's crashes up to its cluster, for one type.

    Returns a DataFrame indexed by cluster_id. History columns build the FEATURES
    and the statistical baseline; the target column is the LABEL. The two never
    mix (history years vs target years), so this is where the leakage guard pays
    off. The headline column is c_tgt_share_t — each cluster's share of all-type
    crashes in the target window, which is what the model predicts.
    """
    aadf   = seg_df[AADF_COL[VEHICLE_TYPES[type_idx]]].fillna(0).values
    length = seg_df['length_m'].values
    df = pd.DataFrame({
        'cluster_id': cluster_id,
        'hist_t':   hist_sev[:, type_idx],      # this type's history crashes
        'hist_all': hist_sev.sum(axis=1),       # all types' history crashes
        'tgt_t':    target_sev[:, type_idx],    # this type's target crashes
        'tgt_all':  target_sev.sum(axis=1),     # all types' target crashes
        'len':      length,
        'expo_t':   aadf * (length / 1000.0),   # exposure = traffic × road-km
        'one':      1.0,
    })
    df = df[df['cluster_id'] >= 0]              # drop unassigned segments
    g = df.groupby('cluster_id').sum()          # per-cluster sums

    out = pd.DataFrame(index=g.index)
    out['c_hist_t']      = g['hist_t']
    out['c_hist_all']    = g['hist_all']
    out['c_share_t']     = g['hist_t'] / g['hist_all'].replace(0, np.nan)   # HISTORY share (baseline/feature)
    out['c_size']        = g['one']
    out['c_len']         = g['len']
    out['c_expo_t']      = g['expo_t']
    out['c_rate_t']      = g['hist_t'] / g['expo_t'].replace(0, np.nan)     # crashes per exposure
    out['c_tgt_t']       = g['tgt_t']
    out['c_tgt_all']     = g['tgt_all']
    out['c_tgt_share_t'] = g['tgt_t'] / g['tgt_all'].replace(0, np.nan)     # TARGET share ← the label
    return out.fillna(0.0)


def cluster_target_share(cluster_id, cframe):
    """Broadcast each cluster's target share back down to its member segments —
    the per-segment training label y. Segments in no cluster (-1) get 0."""
    share_map = cframe['c_tgt_share_t'].to_dict()
    return np.array([share_map.get(cid, 0.0) if cid >= 0 else 0.0
                     for cid in cluster_id], dtype=np.float32)

# BUILD-MARKER: next section below
