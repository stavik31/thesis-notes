#!/usr/bin/env python3
"""
Shared helpers for the cluster-based risk engine experiments (test folder).

This reconstructs the 2026-07-04 night-session recipe that was run ad hoc and
never saved: per-type discrete network clusters + share-of-all-type-total
objective + fully separate per-type models. See
PHASE3/wiki/progress/2026-07-04-clustering-testing.md for the audit trail.

Nothing here touches the production pipeline. It reads the same Stage 2 outputs
(segments.gpkg, crashes_segmented.csv, graph_edges.csv) read-only.

The correctness check for this whole reconstruction is the cross-type Spearman ρ
on a genuine spatial holdout (a whole city excluded): the vanished result was
ρ≈0.201 on a Manchester holdout with the model beating a pure-statistical
baseline. If this code reproduces that, the reconstruction is faithful.
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd
import pyogrio
from scipy.stats import spearmanr

# ── Constants (mirrored from stage3 train.py / stage5 route.py) ────────────────

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']

# Per-type AADF column used as that type's own exposure / clustering feature.
# Identical mapping to stage3 train.py so the two stay consistent.
AADF_COL = {
    'car':        'cars_and_taxis',
    'motorcycle': 'two_wheeled_motor_vehicles',
    'cycle':      'pedal_cycles',
    'lgv':        'lgvs',
    'hgv':        'all_hgvs',
}

HISTORY_YEARS = [2020, 2021]   # cluster construction + input features
TARGET_YEARS  = [2022, 2023]   # target + evaluation (disjoint from history)
HOLDOUT_YEAR  = 2024           # reserved for Stage 6, never touched here

# WGS84 bboxes (lon_min, lat_min, lon_max, lat_max) — copied from train.py.
CITIES = {
    'london':     (-0.51, 51.28,  0.33, 51.72),
    'birmingham': (-2.05, 52.35, -1.75, 52.60),
    'manchester': (-2.40, 53.33, -2.10, 53.55),
    'leeds':      (-1.70, 53.72, -1.45, 53.88),
}

CODE_DIR = Path(__file__).resolve().parents[2]     # .../code
OUTPUTS  = CODE_DIR / 'outputs'

SEG_COLS = ['segment_id', 'road_class', 'length_m', 'all_motor_vehicles',
            'cars_and_taxis', 'lgvs', 'all_hgvs', 'two_wheeled_motor_vehicles',
            'pedal_cycles', 'aadf_fallback', 'centroid_lon', 'centroid_lat']


# ── Loading ────────────────────────────────────────────────────────────────────

def load_segments():
    """Segment attributes only (no geometry) — much lighter than a full read of
    the 3.96M-row gpkg. Returns a DataFrame indexed 0..N-1 with segment_id kept
    as a column."""
    t0 = time.time()
    df = pyogrio.read_dataframe(OUTPUTS / 'segments.gpkg', read_geometry=False,
                                columns=SEG_COLS)
    print(f'  segments: {len(df):,}  ({time.time()-t0:.1f}s)')
    return df.reset_index(drop=True)


def load_crashes():
    df = pd.read_csv(OUTPUTS / 'crashes_segmented.csv', low_memory=False,
                     usecols=['vehicle_type', 'severity_weight',
                              'accident_year', 'segment_id'])
    return df


def load_edges():
    t0 = time.time()
    df = pd.read_csv(OUTPUTS / 'graph_edges.csv')
    print(f'  edges: {len(df):,}  ({time.time()-t0:.1f}s)')
    return df


def in_city(seg_df, city):
    """Boolean mask: which segments fall inside a city bbox (by centroid)."""
    lon_min, lat_min, lon_max, lat_max = CITIES[city]
    return (
        (seg_df['centroid_lon'] >= lon_min) & (seg_df['centroid_lon'] <= lon_max) &
        (seg_df['centroid_lat'] >= lat_min) & (seg_df['centroid_lat'] <= lat_max)
    ).values


# ── Crash aggregation ───────────────────────────────────────────────────────────

def severity_matrix(crashes, seg_index, years):
    """
    Severity-weighted crash sums per (segment, type) over the given years.

    seg_index : dict segment_id -> row position (0..N-1)
    Returns   : float32 array [N, 5] in VEHICLE_TYPES order.
    """
    type_to_idx = {t: i for i, t in enumerate(VEHICLE_TYPES)}
    c = crashes[crashes['accident_year'].isin(years)].copy()
    c['nidx'] = c['segment_id'].map(seg_index)
    c['tidx'] = c['vehicle_type'].map(type_to_idx)
    c = c.dropna(subset=['nidx', 'tidx'])
    out = np.zeros((len(seg_index), len(VEHICLE_TYPES)), dtype=np.float32)
    np.add.at(out,
              (c['nidx'].astype(int).values, c['tidx'].astype(int).values),
              c['severity_weight'].values.astype(np.float32))
    return out


# ── Adjacency ───────────────────────────────────────────────────────────────────

def build_adjacency(edges, seg_index, active_mask=None):
    """
    CSR-style undirected adjacency over segment row-indices.

    active_mask : optional bool array [N]; edges touching an inactive node are
                  dropped (used to spatially exclude a holdout city — a held-out
                  segment must not even be reachable during cluster growth).

    Returns (indptr, neighbors) int arrays for O(1) neighbour iteration.
    """
    a = edges['segment_id_a'].map(seg_index).values
    b = edges['segment_id_b'].map(seg_index).values
    valid = ~(pd.isna(a) | pd.isna(b))
    a = a[valid].astype(np.int64)
    b = b[valid].astype(np.int64)

    if active_mask is not None:
        keep = active_mask[a] & active_mask[b]
        a, b = a[keep], b[keep]

    N = len(seg_index)
    # symmetric: add both directions
    src = np.concatenate([a, b])
    dst = np.concatenate([b, a])
    order = np.argsort(src, kind='stable')
    src, dst = src[order], dst[order]
    indptr = np.zeros(N + 1, dtype=np.int64)
    np.add.at(indptr, src + 1, 1)
    np.cumsum(indptr, out=indptr)
    return indptr, dst.astype(np.int64)


# ── Per-type BFS clustering ─────────────────────────────────────────────────────

def bfs_clusters(indptr, neighbors, hist_count, min_crashes,
                 active_mask=None):
    """
    Grow discrete, connected clusters over the road network for ONE vehicle type.

    Seeded from the highest-history-crash unassigned segment, BFS outward adding
    unassigned neighbours until the cluster's accumulated history crash weight
    reaches `min_crashes` (or the local frontier is exhausted). Sparse regions
    therefore form large coarse clusters; dense regions form small fine ones —
    the adaptive granularity the plan called for, driven by data sufficiency.

    hist_count  : float array [N] — this type's history severity weight per seg.
    active_mask : optional bool [N] — inactive segments are never assigned
                  (holdout city).

    Returns cluster_id int array [N]; inactive/unreached segments get -1.
    """
    N = len(hist_count)
    cluster_id = np.full(N, -1, dtype=np.int64)
    active = np.ones(N, dtype=bool) if active_mask is None else active_mask.copy()

    # Seed order: densest first so crash concentrations anchor tight clusters.
    seed_order = np.argsort(-hist_count, kind='stable')

    cid = 0
    from collections import deque
    for seed in seed_order:
        if not active[seed] or cluster_id[seed] != -1:
            continue
        # BFS from this seed
        q = deque([seed])
        cluster_id[seed] = cid
        acc = hist_count[seed]
        members = [seed]
        while q and acc < min_crashes:
            u = q.popleft()
            for k in range(indptr[u], indptr[u + 1]):
                v = neighbors[k]
                if active[v] and cluster_id[v] == -1:
                    cluster_id[v] = cid
                    acc += hist_count[v]
                    members.append(v)
                    q.append(v)
                    if acc >= min_crashes:
                        break
        cid += 1

    return cluster_id


def cluster_frame(cluster_id, hist_sev, target_sev, seg_df, type_idx):
    """
    Build per-cluster aggregates for one type from history + target windows.

    Returns a DataFrame indexed by cluster_id with:
      c_hist_t, c_hist_all  : history severity (this type / all types) in cluster
      c_share_t             : this type's share of all-type history crashes
      c_size                : segments in cluster
      c_len                 : total length_m in cluster
      c_expo_t              : summed own-type AADF*length (exposure)
      c_rate_t              : c_hist_t / c_expo_t
      c_tgt_t, c_tgt_all    : target-window severity (this type / all)
      c_tgt_share_t         : this type's share of all-type TARGET crashes
    """
    aadf = seg_df[AADF_COL[VEHICLE_TYPES[type_idx]]].fillna(0).values
    length = seg_df['length_m'].values
    df = pd.DataFrame({
        'cluster_id': cluster_id,
        'hist_t':   hist_sev[:, type_idx],
        'hist_all': hist_sev.sum(axis=1),
        'tgt_t':    target_sev[:, type_idx],
        'tgt_all':  target_sev.sum(axis=1),
        'len':      length,
        'expo_t':   aadf * (length / 1000.0),
        'one':      1.0,
    })
    df = df[df['cluster_id'] >= 0]
    g = df.groupby('cluster_id').sum()
    out = pd.DataFrame(index=g.index)
    out['c_hist_t']   = g['hist_t']
    out['c_hist_all'] = g['hist_all']
    out['c_share_t']  = g['hist_t'] / g['hist_all'].replace(0, np.nan)
    out['c_size']     = g['one']
    out['c_len']      = g['len']
    out['c_expo_t']   = g['expo_t']
    out['c_rate_t']   = g['hist_t'] / g['expo_t'].replace(0, np.nan)
    out['c_tgt_t']    = g['tgt_t']
    out['c_tgt_all']  = g['tgt_all']
    out['c_tgt_share_t'] = g['tgt_t'] / g['tgt_all'].replace(0, np.nan)
    return out.fillna(0.0)


# ── Feature builder (shared by XGBoost and GAT variants) ─────────────────────────

def road_class_onehot(seg_df):
    rc = pd.get_dummies(seg_df['road_class'], prefix='rc').astype(np.float32)
    return rc.values, list(rc.columns)


def build_type_features(seg_df, type_idx, cluster_id, cframe, rc_x, rc_cols):
    """Per-segment feature matrix for one type. Cluster stats mapped from the
    segment's cluster; unclustered segments (-1) get 0. Identical inputs for the
    XGBoost and GAT variants so the only difference between them is the learner."""
    tname = VEHICLE_TYPES[type_idx]
    n = len(seg_df)
    own_aadf = seg_df[AADF_COL[tname]].fillna(0).values.astype(np.float32)
    length   = seg_df['length_m'].values.astype(np.float32)
    allmv    = seg_df['all_motor_vehicles'].fillna(0).values.astype(np.float32)

    cols = ['c_share_t', 'c_rate_t', 'c_size', 'c_hist_t', 'c_hist_all']
    cvals = np.zeros((n, len(cols)), dtype=np.float32)
    for ci, c in enumerate(cols):
        d = cframe[c].to_dict()
        cvals[:, ci] = [d.get(cid, 0.0) if cid >= 0 else 0.0 for cid in cluster_id]

    feats = np.column_stack([
        np.log1p(own_aadf), np.log1p(length), np.log1p(allmv), cvals, rc_x
    ]).astype(np.float32)
    names = ['log_own_aadf', 'log_length', 'log_allmv', *cols, *rc_cols]
    return feats, names


def cluster_target_share(cluster_id, cframe):
    """Per-segment target = its cluster's target-window type share (broadcast)."""
    share_map = cframe['c_tgt_share_t'].to_dict()
    return np.array([share_map.get(cid, 0.0) if cid >= 0 else 0.0
                     for cid in cluster_id], dtype=np.float32)


def stat_surface(cluster_id, cframe):
    """Pure-statistical baseline surface = history cluster share."""
    stat_map = cframe['c_share_t'].to_dict()
    return np.array([stat_map.get(cid, 0.0) if cid >= 0 else 0.0
                     for cid in cluster_id], dtype=np.float32)


# ── Evaluation ───────────────────────────────────────────────────────────────────

def cross_type_rho(risk_wide, eval_mask):
    """Mean pairwise cross-type Spearman ρ over evaluation segments.
    risk_wide : array [N, 5] predicted risk per type. Lower ρ = more divergence."""
    sub = risk_wide[eval_mask]
    rhos = []
    for i in range(len(VEHICLE_TYPES)):
        for j in range(i + 1, len(VEHICLE_TYPES)):
            a, b = sub[:, i], sub[:, j]
            if np.std(a) == 0 or np.std(b) == 0:
                continue
            rho, _ = spearmanr(a, b)
            if not np.isnan(rho):
                rhos.append(rho)
    return float(np.mean(rhos)) if rhos else float('nan')


def topn_jaccard(risk_wide, eval_mask, n=1000):
    """Mean pairwise Jaccard of each type-pair's top-N segments (eval subset)."""
    idx = np.where(eval_mask)[0]
    sub = risk_wide[eval_mask]
    n = min(n, len(idx))
    tops = {}
    for i in range(len(VEHICLE_TYPES)):
        order = np.argsort(-sub[:, i])[:n]
        tops[i] = set(idx[order])
    js = []
    for i in range(len(VEHICLE_TYPES)):
        for j in range(i + 1, len(VEHICLE_TYPES)):
            inter = len(tops[i] & tops[j])
            union = len(tops[i] | tops[j])
            if union:
                js.append(inter / union)
    return float(np.mean(js)) if js else float('nan')


def validity(risk_wide, target_sev, eval_mask):
    """Per-type Spearman ρ between predicted risk and REAL target-year crashes.
    Higher = the surface actually predicts where that type crashes."""
    out = {}
    for i, t in enumerate(VEHICLE_TYPES):
        a = risk_wide[eval_mask, i]
        b = target_sev[eval_mask, i]
        if np.std(a) == 0 or np.std(b) == 0:
            out[t] = float('nan')
            continue
        rho, _ = spearmanr(a, b)
        out[t] = float(rho)
    return out
