#!/usr/bin/env python3
"""
Two-step leakage-free validation of the chosen engine (XGBoost cluster+share).

This is the confidence check before committing the recipe to the main pipeline.
It answers "does the method hold up with NO leakage, at full national scale, and
WHAT features explain each type's risk" — not "how high can accuracy go."

STEP 1 — Spatial cross-validation (the leakage-free national surface)
  GB is partitioned into a grid of spatial blocks. Each block is held out in
  turn: its crash history is zeroed, it is excluded from cluster signal and from
  XGBoost training, and it is predicted from the rest. Every segment thus gets a
  prediction from a model that never saw its region -> one fully out-of-sample
  national surface. Cross-type rho + validity are then leakage-free everywhere,
  not just on one city.

STEP 2 — Temporal 2024 holdout
  2024 is the reserved year, used by NOTHING (not features, not target). Validity
  of the OOS surface against real 2024 crashes is the strongest leakage guard and
  is exactly the thesis Stage-6 design (train years 1-4, test year 5).

EXPLAINABILITY — per-type feature importance (gain) + SHAP (mean |contribution|),
aggregated over the held-out predictions. This is the point of choosing XGBoost:
the risk is attributable to interpretable features, unlike a pure spatial smoother.

NOTE on interpretation: every prediction here is deliberately from the pessimistic
"held-out region" regime (no local history). The DEPLOYED surface uses full
history and is stronger; this run is a validation device, not the production
surface.

Usage:
  python run_cv.py --folds-lon 4 --folds-lat 4 --gpu
"""

import argparse
import time

import numpy as np
import pandas as pd
import xgboost as xgb

import common as C


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--min-crashes', type=float, default=30.0)
    p.add_argument('--folds-lon', type=int, default=4)
    p.add_argument('--folds-lat', type=int, default=4)
    p.add_argument('--shap-sample', type=int, default=15000,
                   help='held-out crash-bearing segments per type per fold used for SHAP')
    p.add_argument('--out', default='cv_oos_risk.csv')
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--gpu', action='store_true')
    return p.parse_args()


def spatial_blocks(seg_df, nlon, nlat):
    """Quantile-binned grid on centroids -> ~balanced spatial blocks (each block
    is a contiguous lon x lat cell holding ~equal segment counts)."""
    lon = seg_df['centroid_lon'].values
    lat = seg_df['centroid_lat'].values
    lon_edges = np.quantile(lon, np.linspace(0, 1, nlon + 1))[1:-1]
    lat_edges = np.quantile(lat, np.linspace(0, 1, nlat + 1))[1:-1]
    lb = np.digitize(lon, lon_edges)
    tb = np.digitize(lat, lat_edges)
    return lb * nlat + tb


def main():
    args = parse_args()
    np.random.seed(args.seed)
    T0 = time.time()

    print('Loading data...')
    seg_df  = C.load_segments()
    crashes = C.load_crashes()
    edges   = C.load_edges()
    seg_index = {sid: i for i, sid in enumerate(seg_df['segment_id'])}
    N = len(seg_df)

    hist_sev = C.severity_matrix(crashes, seg_index, C.HISTORY_YEARS)     # 2020-21
    tgt_sev  = C.severity_matrix(crashes, seg_index, C.TARGET_YEARS)      # 2022-23
    fut_sev  = C.severity_matrix(crashes, seg_index, [C.HOLDOUT_YEAR])    # 2024 (unseen)

    print('Building adjacency...')
    indptr, neighbors = C.build_adjacency(edges, seg_index)
    rc_x, rc_cols = C.road_class_onehot(seg_df)

    blocks = spatial_blocks(seg_df, args.folds_lon, args.folds_lat)
    ublocks = np.unique(blocks)
    print(f'Spatial CV: {len(ublocks)} folds  '
          f'(sizes {np.bincount(blocks).min():,}..{np.bincount(blocks).max():,})')

    n_types = len(C.VEHICLE_TYPES)
    oos_risk = np.full((N, n_types), np.nan, dtype=np.float32)
    predicted = np.zeros(N, dtype=bool)

    # feature-importance + SHAP accumulators (feature set is stable across folds).
    # Names mirror C.build_type_features' column order exactly.
    fnames = ['log_own_aadf', 'log_length', 'log_allmv',
              'c_share_t', 'c_rate_t', 'c_size', 'c_hist_t', 'c_hist_all', *rc_cols]
    gain_acc = {t: np.zeros(len(fnames)) for t in C.VEHICLE_TYPES}
    gain_n   = {t: 0 for t in C.VEHICLE_TYPES}
    shap_acc = {t: np.zeros(len(fnames)) for t in C.VEHICLE_TYPES}
    shap_n   = {t: 0 for t in C.VEHICLE_TYPES}

    for fi, b in enumerate(ublocks):
        t0 = time.time()
        blk_mask = blocks == b
        active   = ~blk_mask
        hfb = hist_sev.copy(); hfb[blk_mask] = 0.0
        blk_idx = np.where(blk_mask)[0]

        for ti, tname in enumerate(C.VEHICLE_TYPES):
            cluster_id = C.bfs_clusters(indptr, neighbors, hfb[:, ti],
                                        args.min_crashes, active_mask=None)
            cframe = C.cluster_frame(cluster_id, hfb, tgt_sev, seg_df, ti)
            feats, _ = C.build_type_features(seg_df, ti, cluster_id, cframe, rc_x, rc_cols)
            y = C.cluster_target_share(cluster_id, cframe)

            train_rows = np.where(active)[0]
            model = xgb.XGBRegressor(
                n_estimators=350, max_depth=6, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, min_child_weight=5,
                objective='reg:squarederror', n_jobs=32,
                tree_method='hist', device='cuda' if args.gpu else 'cpu',
                random_state=args.seed,
            )
            model.fit(feats[train_rows], y[train_rows])
            oos_risk[blk_idx, ti] = model.predict(feats[blk_idx])

            # gain importance
            gain_acc[tname] += model.feature_importances_ * len(blk_idx)
            gain_n[tname]   += len(blk_idx)

            # SHAP on a held-out crash-bearing sample (built-in, no external lib)
            cb = blk_idx[tgt_sev[blk_idx, ti] > 0]
            if len(cb) > 0:
                if len(cb) > args.shap_sample:
                    cb = np.random.choice(cb, args.shap_sample, replace=False)
                try:
                    booster = model.get_booster()
                    booster.set_param({'device': 'cpu'})
                    contrib = booster.predict(xgb.DMatrix(feats[cb]), pred_contribs=True)
                    shap_acc[tname] += np.abs(contrib[:, :-1]).sum(axis=0)  # drop bias col
                    shap_n[tname]   += len(cb)
                except Exception as e:
                    if fi == 0:
                        print(f'    (SHAP skipped for {tname}: {e})')

        predicted[blk_idx] = True
        print(f'  fold {fi+1}/{len(ublocks)} (block {b}): {blk_mask.sum():,} segs '
              f'predicted  ({time.time()-t0:.0f}s)')

    # ── evaluation (leakage-free) ──
    eval_tgt = (tgt_sev.sum(axis=1) > 0) & predicted     # crash-bearing 2022-23
    eval_fut = (fut_sev.sum(axis=1) > 0) & predicted     # crash-bearing 2024

    risk = np.nan_to_num(oos_risk)
    rho = C.cross_type_rho(risk, eval_tgt)
    jac = C.topn_jaccard(risk, eval_tgt, n=1000)
    val_tgt = C.validity(risk, tgt_sev, eval_tgt)
    val_fut = C.validity(risk, fut_sev, eval_fut)

    print('\n' + '=' * 72)
    print('STEP 1 — SPATIAL CV (leakage-free national out-of-sample surface)')
    print('=' * 72)
    print(f'  segments predicted OOS: {predicted.sum():,} / {N:,}')
    print(f'  eval (crash-bearing 2022-23): {eval_tgt.sum():,} segments')
    print(f'  cross-type rho   = {rho:.3f}   (lower = more per-type divergence)')
    print(f'  top-1000 Jaccard = {jac:.3f}')
    print(f'  validity vs 2022-23: ' +
          '  '.join(f'{t}={val_tgt[t]:.3f}' for t in C.VEHICLE_TYPES))
    print('\n' + '=' * 72)
    print('STEP 2 — TEMPORAL 2024 HOLDOUT (year unseen by features AND target)')
    print('=' * 72)
    print(f'  eval (crash-bearing 2024): {eval_fut.sum():,} segments')
    print(f'  validity vs 2024:    ' +
          '  '.join(f'{t}={val_fut[t]:.3f}' for t in C.VEHICLE_TYPES))

    # ── explainability ──
    print('\n' + '=' * 72)
    print('EXPLAINABILITY — top features per type (SHAP mean|contribution|, share)')
    print('=' * 72)
    for t in C.VEHICLE_TYPES:
        if shap_n[t] > 0:
            imp = shap_acc[t] / shap_acc[t].sum()
        else:
            imp = gain_acc[t] / max(gain_acc[t].sum(), 1e-9)
        order = np.argsort(-imp)[:6]
        top = '  '.join(f'{fnames[i]}={imp[i]:.2f}' for i in order)
        print(f'  {t:<11} {top}')

    print('\n(gain-based importances, for comparison)')
    for t in C.VEHICLE_TYPES:
        g = gain_acc[t] / max(gain_acc[t].sum(), 1e-9)
        order = np.argsort(-g)[:5]
        print(f'  {t:<11} ' + '  '.join(f'{fnames[i]}={g[i]:.2f}' for i in order))

    # save OOS surface (production-usable, leakage-free)
    rows = []
    for ti, t in enumerate(C.VEHICLE_TYPES):
        rows.append(pd.DataFrame({
            'segment_id': seg_df['segment_id'].values,
            'vehicle_type': t,
            'risk_score': risk[:, ti],
        }))
    pd.concat(rows, ignore_index=True).to_csv(args.out, index=False)
    print(f'\nSaved OOS surface -> {args.out}   (total {time.time()-T0:.0f}s)')


if __name__ == '__main__':
    main()
