#!/usr/bin/env python3
"""
Grouping-robustness / MAUP sensitivity test.

Question this answers (raised 2026-07-07): the clusters are a heuristic GROUPING,
not an optimised clustering — so does the headline result (per-type divergence =
low cross-type rho, plus validity) depend on HOW we group, or is it a property of
the data? If several very different groupings give the same story, the grouping
is not driving the result (the standard defence against the Modifiable Areal Unit
Problem).

Everything downstream of clustering is IDENTICAL to run_xgb.py (same features,
same cluster_share target, same XGBoost config, same eval + stat baseline). The
ONLY thing that changes between runs is how cluster_id is assigned:

  bfs_dense  : the real engine — densest-first BFS growth (== common.bfs_clusters)
  bfs_random : same BFS growth + threshold, but seeds in RANDOM order
               (tests: does the greedy construction ORDER matter?)
  grid       : ignore the road network entirely — bin segments by a lon/lat grid
               (tests: does the NETWORK clustering matter, or any spatial pooling?)
               Note: grid clusters are identical across types, so any divergence
               here comes purely from the per-type SHARE target, not per-type
               grouping — the most stringent test of where divergence comes from.

Default is a NATIONAL run (no holdout) so the scheme comparison isn't confounded
by network propagation into a held-out city (which only BFS can do). Use
--holdout to additionally see generalisation.

Usage:
  python sens_scheme.py                       # national, all three schemes
  python sens_scheme.py --grid-deg 0.03
  python sens_scheme.py --holdout manchester
"""

import argparse
import time
from collections import deque

import numpy as np
import pandas as pd
import xgboost as xgb

import common as C


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--min-crashes', type=float, default=30.0)
    p.add_argument('--grid-deg', type=float, default=0.03,
                   help='grid cell size in degrees for the grid scheme')
    p.add_argument('--holdout', choices=list(C.CITIES.keys()), default=None)
    p.add_argument('--schemes', default='bfs_dense,bfs_random,grid')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--gpu', action='store_true')
    return p.parse_args()


# ── clustering schemes (the only thing that varies) ──────────────────────────────

def bfs_with_order(indptr, neighbors, hist_count, min_crashes, seed_order):
    """common.bfs_clusters, but seeds are consumed in the given order instead of
    densest-first. Identical growth/threshold otherwise."""
    N = len(hist_count)
    cluster_id = np.full(N, -1, dtype=np.int64)
    cid = 0
    for seed in seed_order:
        if cluster_id[seed] != -1:
            continue
        q = deque([seed]); cluster_id[seed] = cid; acc = hist_count[seed]
        while q and acc < min_crashes:
            u = q.popleft()
            for k in range(indptr[u], indptr[u + 1]):
                v = neighbors[k]
                if cluster_id[v] == -1:
                    cluster_id[v] = cid; acc += hist_count[v]; q.append(v)
                    if acc >= min_crashes:
                        break
        cid += 1
    return cluster_id


def grid_clusters(seg_df, deg):
    """Non-network baseline: cluster_id = which lon/lat grid cell the segment's
    centroid falls in. Ignores road topology and data density entirely."""
    lon_bin = np.floor(seg_df['centroid_lon'].values / deg).astype(np.int64)
    lat_bin = np.floor(seg_df['centroid_lat'].values / deg).astype(np.int64)
    key = lon_bin * 1_000_003 + lat_bin          # collision-safe combine
    _, inv = np.unique(key, return_inverse=True)  # -> 0..K-1
    return inv.astype(np.int64)


def clusters_for(scheme, ti, indptr, neighbors, hist_for_build, seg_df,
                 min_crashes, rng):
    if scheme == 'bfs_dense':
        return C.bfs_clusters(indptr, neighbors, hist_for_build[:, ti],
                              min_crashes, active_mask=None)
    if scheme == 'bfs_random':
        order = rng.permutation(len(seg_df))
        return bfs_with_order(indptr, neighbors, hist_for_build[:, ti],
                              min_crashes, order)
    if scheme == 'grid':
        return grid_clusters(seg_df, GRID_DEG)
    raise ValueError(scheme)


# ── downstream (identical to run_xgb.py) ─────────────────────────────────────────

def road_class_onehot(seg_df):
    rc = pd.get_dummies(seg_df['road_class'], prefix='rc').astype(np.float32)
    return rc.values, list(rc.columns)


def build_type_features(seg_df, type_idx, cluster_id, cframe, rc_x, rc_cols):
    tname = C.VEHICLE_TYPES[type_idx]
    n = len(seg_df)
    own_aadf = seg_df[C.AADF_COL[tname]].fillna(0).values.astype(np.float32)
    length   = seg_df['length_m'].values.astype(np.float32)
    allmv    = seg_df['all_motor_vehicles'].fillna(0).values.astype(np.float32)
    cols = ['c_share_t', 'c_rate_t', 'c_size', 'c_hist_t', 'c_hist_all']
    cmap = {c: cframe[c].to_dict() for c in cols}
    cvals = np.zeros((n, len(cols)), dtype=np.float32)
    for ci, c in enumerate(cols):
        d = cmap[c]
        cvals[:, ci] = [d.get(cid, 0.0) if cid >= 0 else 0.0 for cid in cluster_id]
    feats = np.column_stack([
        np.log1p(own_aadf), np.log1p(length), np.log1p(allmv), cvals, rc_x
    ]).astype(np.float32)
    return feats


def run_scheme(scheme, seg_df, indptr, neighbors, hist_for_build, tgt_sev,
               rc_x, rc_cols, active, eval_mask, args, rng):
    N = len(seg_df)
    risk_ml   = np.zeros((N, len(C.VEHICLE_TYPES)), dtype=np.float32)
    risk_stat = np.zeros((N, len(C.VEHICLE_TYPES)), dtype=np.float32)
    ncl = []
    for ti, tname in enumerate(C.VEHICLE_TYPES):
        cluster_id = clusters_for(scheme, ti, indptr, neighbors, hist_for_build,
                                  seg_df, args.min_crashes, rng)
        ncl.append(int(cluster_id.max() + 1))
        cframe = C.cluster_frame(cluster_id, hist_for_build, tgt_sev, seg_df, ti)
        feats  = build_type_features(seg_df, ti, cluster_id, cframe, rc_x, rc_cols)

        share_map = cframe['c_tgt_share_t'].to_dict()
        y = np.array([share_map.get(cid, 0.0) if cid >= 0 else 0.0
                      for cid in cluster_id], dtype=np.float32)
        stat_map = cframe['c_share_t'].to_dict()
        risk_stat[:, ti] = [stat_map.get(cid, 0.0) if cid >= 0 else 0.0
                            for cid in cluster_id]

        train_rows = np.where(active)[0]
        model = xgb.XGBRegressor(
            n_estimators=400, max_depth=6, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
            objective='reg:squarederror', n_jobs=32,
            tree_method='hist', device='cuda' if args.gpu else 'cpu',
            random_state=args.seed,
        )
        model.fit(feats[train_rows], y[train_rows])
        risk_ml[:, ti] = model.predict(feats)

    def line(name, risk):
        rho = C.cross_type_rho(risk, eval_mask)
        val = C.validity(risk, tgt_sev, eval_mask)
        vstr = ' '.join(f'{t}={val[t]:.3f}' for t in C.VEHICLE_TYPES)
        print(f'  {name:<26} cross-type rho={rho:.3f} | validity {vstr}')
        return rho

    print(f'\n[{scheme}]  clusters/type={ncl}')
    line('pure-statistical', risk_stat)
    line('XGBoost cluster+share', risk_ml)


def main():
    args = parse_args()
    global GRID_DEG
    GRID_DEG = args.grid_deg
    rng = np.random.default_rng(args.seed)

    print('Loading data...')
    seg_df  = C.load_segments()
    crashes = C.load_crashes()
    edges   = C.load_edges()
    seg_index = {sid: i for i, sid in enumerate(seg_df['segment_id'])}
    N = len(seg_df)

    hist_sev = C.severity_matrix(crashes, seg_index, C.HISTORY_YEARS)
    tgt_sev  = C.severity_matrix(crashes, seg_index, C.TARGET_YEARS)

    if args.holdout:
        city_mask = C.in_city(seg_df, args.holdout)
        active = ~city_mask
        hist_for_build = hist_sev.copy(); hist_for_build[city_mask] = 0.0
        eval_mask = (tgt_sev.sum(axis=1) > 0) & city_mask
    else:
        active = np.ones(N, dtype=bool)
        hist_for_build = hist_sev
        eval_mask = tgt_sev.sum(axis=1) > 0

    indptr, neighbors = C.build_adjacency(edges, seg_index)
    rc_x, rc_cols = road_class_onehot(seg_df)

    print('=' * 72)
    print(f'GROUPING SENSITIVITY  holdout={args.holdout or "none (national)"}  '
          f'min_crashes={args.min_crashes}  grid_deg={args.grid_deg}')
    print(f'Eval segments: {eval_mask.sum():,}   (lower cross-type rho = more divergence)')
    print('=' * 72)
    for scheme in args.schemes.split(','):
        run_scheme(scheme, seg_df, indptr, neighbors, hist_for_build, tgt_sev,
                   rc_x, rc_cols, active, eval_mask, args, rng)


if __name__ == '__main__':
    main()
