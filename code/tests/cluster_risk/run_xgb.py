#!/usr/bin/env python3
"""
Cluster + share + per-type XGBoost risk engine (reconstruction of 2026-07-04).

Pipeline, per vehicle type (5 fully independent models, nothing shared):
  1. BFS-grow discrete network clusters until each holds >= MIN_CRASHES of this
     type's HISTORY crashes (sparse areas -> coarse clusters, dense -> fine).
  2. Aggregate history + target crash stats per cluster.
  3. Features  = segment own-AADF, road_class, length, all-motor-volume
               + this type's history cluster stats (share, rate, size, counts).
     Target    = this type's SHARE of all-type crashes (removes the "how busy
                 overall" magnitude that collapses divergence). Two variants:
                   cluster_share : the cluster's target-window type share
                   seg_share     : the segment's own smoothed target share
  4. Train XGBoost on TRAIN segments only; predict a risk score for every segment.

Evaluation (lower cross-type rho = more vehicle-type divergence preserved):
  - cross-type Spearman rho + top-1000 Jaccard over crash-bearing segments
  - validity: per-type rho between predicted risk and REAL target-year crashes
  - pure-statistical baseline (history cluster share) for comparison

Spatial holdout (--holdout city): the city is excluded from cluster construction
AND training (its history is never seen); evaluation is on that city only. This
is the genuine generalisation test — the vanished result was rho~0.201 on a
Manchester holdout, ML beating the pure statistic for every type.

Usage:
  python run_xgb.py                              # national, random 80/20, in-sample-ish
  python run_xgb.py --holdout manchester         # genuine spatial holdout
  python run_xgb.py --holdout manchester --target seg_share
  python run_xgb.py --predict-city london --out london_xgb_risk.csv   # for routing
"""

import argparse
import time

import numpy as np
import pandas as pd
import xgboost as xgb

import common as C


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--min-crashes', type=float, default=30.0,
                   help='BFS cluster growth stops at this history severity weight')
    p.add_argument('--target', choices=['cluster_share', 'seg_share'],
                   default='cluster_share')
    p.add_argument('--holdout', choices=list(C.CITIES.keys()), default=None,
                   help='Exclude this city from construction+training; eval on it')
    p.add_argument('--predict-city', choices=list(C.CITIES.keys()), default=None,
                   help='Also write a production risk CSV for this city (routing)')
    p.add_argument('--out', default=None, help='Output CSV path for --predict-city')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--seg-share-k', type=float, default=1.0,
                   help='Smoothing constant for seg_share target')
    p.add_argument('--gpu', action='store_true')
    return p.parse_args()


def road_class_onehot(seg_df):
    rc = pd.get_dummies(seg_df['road_class'], prefix='rc').astype(np.float32)
    return rc.values, list(rc.columns)


def build_type_features(seg_df, type_idx, cluster_id, cframe, rc_x, rc_cols):
    """Per-segment feature matrix for one type. Cluster stats are mapped from the
    segment's cluster; unclustered segments (-1, e.g. holdout city) get 0."""
    tname = C.VEHICLE_TYPES[type_idx]
    n = len(seg_df)

    # segment-level
    own_aadf = seg_df[C.AADF_COL[tname]].fillna(0).values.astype(np.float32)
    length   = seg_df['length_m'].values.astype(np.float32)
    allmv    = seg_df['all_motor_vehicles'].fillna(0).values.astype(np.float32)

    # cluster-level (mapped by cluster_id; -1 -> zeros)
    cols = ['c_share_t', 'c_rate_t', 'c_size', 'c_hist_t', 'c_hist_all']
    cmap = {c: cframe[c].to_dict() for c in cols}
    cvals = np.zeros((n, len(cols)), dtype=np.float32)
    for ci, c in enumerate(cols):
        d = cmap[c]
        cvals[:, ci] = [d.get(cid, 0.0) if cid >= 0 else 0.0 for cid in cluster_id]

    feats = np.column_stack([
        np.log1p(own_aadf), np.log1p(length), np.log1p(allmv), cvals, rc_x
    ]).astype(np.float32)
    names = ['log_own_aadf', 'log_length', 'log_allmv', *cols, *rc_cols]
    return feats, names


def main():
    args = parse_args()
    np.random.seed(args.seed)

    print('Loading data...')
    seg_df  = C.load_segments()
    crashes = C.load_crashes()
    edges   = C.load_edges()

    seg_index = {sid: i for i, sid in enumerate(seg_df['segment_id'])}
    N = len(seg_df)

    print('Aggregating crashes...')
    hist_sev = C.severity_matrix(crashes, seg_index, C.HISTORY_YEARS)
    tgt_sev  = C.severity_matrix(crashes, seg_index, C.TARGET_YEARS)

    # ── holdout / active masks ──
    if args.holdout:
        city_mask = C.in_city(seg_df, args.holdout)
        active    = ~city_mask
        print(f'Holdout {args.holdout}: {city_mask.sum():,} segments excluded '
              f'from construction+training')
        # a held-out segment must not leak its history into cluster stats/features
        hist_for_build = hist_sev.copy(); hist_for_build[city_mask] = 0.0
    else:
        city_mask = np.zeros(N, dtype=bool)
        active    = np.ones(N, dtype=bool)
        hist_for_build = hist_sev

    print('Building adjacency...')
    indptr, neighbors = C.build_adjacency(edges, seg_index)   # full graph for BFS reach
    rc_x, rc_cols = road_class_onehot(seg_df)

    # ── evaluation mask: crash-bearing segments (>=1 any-type target crash) ──
    crash_bearing = tgt_sev.sum(axis=1) > 0
    if args.holdout:
        eval_mask = crash_bearing & city_mask          # generalisation: on the city
    else:
        eval_mask = crash_bearing                        # national in-sample-ish
    print(f'Eval segments: {eval_mask.sum():,}')

    risk_ml   = np.zeros((N, len(C.VEHICLE_TYPES)), dtype=np.float32)
    risk_stat = np.zeros((N, len(C.VEHICLE_TYPES)), dtype=np.float32)

    for ti, tname in enumerate(C.VEHICLE_TYPES):
        t0 = time.time()
        # 1. clusters over ALL segments (a full partition), but grown on
        #    hist_for_build where a holdout city's history is zeroed — so the
        #    city contributes no crash signal to cluster stats yet its segments
        #    are still absorbed into clusters and can be predicted (the genuine
        #    generalisation test). Only XGBoost TRAINING excludes the city.
        cluster_id = C.bfs_clusters(indptr, neighbors, hist_for_build[:, ti],
                                    args.min_crashes, active_mask=None)
        n_clusters = cluster_id.max() + 1
        # 2. cluster aggregates
        cframe = C.cluster_frame(cluster_id, hist_for_build, tgt_sev, seg_df, ti)
        # 3. features + target
        feats, fnames = build_type_features(seg_df, ti, cluster_id, cframe,
                                            rc_x, rc_cols)

        share_map = cframe['c_tgt_share_t'].to_dict()
        c_target  = np.array([share_map.get(cid, 0.0) if cid >= 0 else 0.0
                              for cid in cluster_id], dtype=np.float32)
        if args.target == 'cluster_share':
            y = c_target
        else:  # seg_share: segment's own smoothed target share
            y = tgt_sev[:, ti] / (tgt_sev.sum(axis=1) + args.seg_share_k)

        # pure-statistical baseline surface = history cluster share
        stat_map = cframe['c_share_t'].to_dict()
        risk_stat[:, ti] = [stat_map.get(cid, 0.0) if cid >= 0 else 0.0
                            for cid in cluster_id]

        # 4. train on active segments only; predict everywhere
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

        print(f'  {tname:<11} clusters={n_clusters:>7,}  '
              f'train={len(train_rows):,}  ({time.time()-t0:.1f}s)')

    # ── report ──
    def report(name, risk):
        rho = C.cross_type_rho(risk, eval_mask)
        jac = C.topn_jaccard(risk, eval_mask, n=1000)
        val = C.validity(risk, tgt_sev, eval_mask)
        vstr = '  '.join(f'{t}={val[t]:.3f}' for t in C.VEHICLE_TYPES)
        print(f'\n{name}')
        print(f'  cross-type rho = {rho:.3f}   (lower = more divergence)')
        print(f'  top-1000 Jaccard = {jac:.3f}')
        print(f'  validity vs real target crashes: {vstr}')
        return rho, val

    print('\n' + '=' * 68)
    print(f'RESULT  target={args.target}  '
          f'holdout={args.holdout or "none (national)"}  min_crashes={args.min_crashes}')
    print('=' * 68)
    report('Pure statistical (history cluster share)', risk_stat)
    report('XGBoost (cluster+share)', risk_ml)

    # ── optional production CSV for routing ──
    if args.predict_city:
        pc = C.in_city(seg_df, args.predict_city)
        rows = []
        for ti, tname in enumerate(C.VEHICLE_TYPES):
            rows.append(pd.DataFrame({
                'segment_id':   seg_df['segment_id'].values[pc],
                'vehicle_type': tname,
                'risk_score':   risk_ml[pc, ti],
            }))
        out = pd.concat(rows, ignore_index=True)
        path = args.out or f'{args.predict_city}_xgb_risk.csv'
        out.to_csv(path, index=False)
        print(f'\nWrote routing risk surface -> {path}  ({len(out):,} rows)')


if __name__ == '__main__':
    main()
