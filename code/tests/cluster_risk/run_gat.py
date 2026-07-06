#!/usr/bin/env python3
"""
GAT variant of the validated recipe — the 2026-07-04 "next step #1".

Same recipe as run_xgb.py (discrete per-type network clusters + share-of-all-
type-total target + FULLY SEPARATE per-type models, nothing shared across
types), but the per-type learner is a small Graph Attention Network instead of
XGBoost. This is the apples-to-apples GAT-vs-XGBoost comparison the note asked
for — run the SAME way (spatial holdout + routing surface) so the two numbers
are directly comparable.

Difference from the production stage3 train.py: NO shared backbone and NO type
embedding (that shared machinery is exactly what caused type-collapse). Here
each vehicle type gets its own independent GAT trained on its own share target.

Usage:
  python run_gat.py --holdout manchester --gpu
  python run_gat.py --holdout london --predict-city london --out london_gat_risk.csv --gpu
"""

import argparse
import time

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.data import Data
from torch_geometric.nn import GATConv
from torch_geometric.loader import NeighborLoader

import common as C


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--min-crashes', type=float, default=30.0)
    p.add_argument('--holdout', choices=list(C.CITIES.keys()), default=None)
    p.add_argument('--predict-city', choices=list(C.CITIES.keys()), default=None)
    p.add_argument('--out', default=None)
    p.add_argument('--max-train', type=int, default=1_000_000,
                   help='Cap training nodes per type for tractability (all crash-'
                        'bearing kept; zero-crash subsampled). XGBoost uses all; '
                        'the share target is cluster-constant so a representative '
                        'sample suffices — documented approximation.')
    p.add_argument('--epochs', type=int, default=15)
    p.add_argument('--patience', type=int, default=3)
    p.add_argument('--hidden', type=int, default=32)
    p.add_argument('--heads', type=int, default=4)
    p.add_argument('--batch-size', type=int, default=4096)
    p.add_argument('--lr', type=float, default=5e-3)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--gpu', action='store_true')
    return p.parse_args()


class TypeGAT(nn.Module):
    """Independent 2-layer GAT regressor for ONE vehicle type. Sigmoid output
    because the target (crash share) lives in [0, 1]."""
    def __init__(self, in_ch, hidden=32, heads=4):
        super().__init__()
        self.g1 = GATConv(in_ch, hidden, heads=heads, concat=True)
        self.g2 = GATConv(hidden * heads, hidden, heads=1, concat=False)
        self.out = nn.Linear(hidden, 1)

    def forward(self, x, edge_index):
        h = F.elu(self.g1(x, edge_index))
        h = F.dropout(h, p=0.1, training=self.training)
        h = F.elu(self.g2(h, edge_index))
        return torch.sigmoid(self.out(h)).squeeze(-1)


def build_edge_index(edges, seg_index):
    a = edges['segment_id_a'].map(seg_index).values
    b = edges['segment_id_b'].map(seg_index).values
    valid = ~(pd.isna(a) | pd.isna(b))
    a = a[valid].astype(np.int64); b = b[valid].astype(np.int64)
    return torch.tensor(np.stack([np.concatenate([a, b]),
                                  np.concatenate([b, a])]), dtype=torch.long)


def zscore(feats):
    mu = feats.mean(axis=0); sd = feats.std(axis=0); sd[sd == 0] = 1.0
    return ((feats - mu) / sd).astype(np.float32)


def train_one_type(x, edge_index, y, train_rows, args, device):
    data = Data(x=torch.tensor(x), edge_index=edge_index,
                y=torch.tensor(y), num_nodes=x.shape[0])
    # 80/20 split of the (capped) training rows for early stopping
    g = torch.Generator().manual_seed(args.seed)
    perm = train_rows[torch.randperm(len(train_rows), generator=g)]
    split = int(0.8 * len(perm))
    tr_idx, va_idx = perm[:split], perm[split:]

    kw = dict(num_neighbors=[10, 5], batch_size=args.batch_size)
    tr_loader = NeighborLoader(data, input_nodes=tr_idx, shuffle=True, **kw)
    va_loader = NeighborLoader(data, input_nodes=va_idx, shuffle=False, **kw)

    model = TypeGAT(x.shape[1], args.hidden, args.heads).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)

    def run(loader, train):
        model.train(train)
        ctx = torch.enable_grad() if train else torch.no_grad()
        tot, nb = 0.0, 0
        with ctx:
            for batch in loader:
                batch = batch.to(device)
                pred = model(batch.x, batch.edge_index)[:batch.batch_size]
                tgt = batch.y[:batch.batch_size]
                loss = F.mse_loss(pred, tgt)
                if train:
                    opt.zero_grad(); loss.backward(); opt.step()
                tot += loss.item(); nb += 1
        return tot / max(nb, 1)

    best, best_state, bad = float('inf'), None, 0
    for ep in range(args.epochs):
        run(tr_loader, True)
        v = run(va_loader, False)
        if v < best - 1e-6:
            best, best_state, bad = v, {k: t.clone() for k, t in model.state_dict().items()}, 0
        else:
            bad += 1
            if bad >= args.patience:
                break
    model.load_state_dict(best_state)

    # inference over ALL nodes
    model.eval()
    inf = NeighborLoader(data, num_neighbors=[10, 5], batch_size=args.batch_size * 4,
                         input_nodes=torch.arange(x.shape[0]), shuffle=False)
    out = np.zeros(x.shape[0], dtype=np.float32)
    with torch.no_grad():
        for batch in inf:
            batch = batch.to(device)
            pred = model(batch.x, batch.edge_index)[:batch.batch_size]
            out[batch.n_id[:batch.batch_size].cpu().numpy()] = pred.cpu().numpy()
    return out


def main():
    args = parse_args()
    torch.manual_seed(args.seed); np.random.seed(args.seed)
    device = torch.device('cuda' if args.gpu and torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')

    print('Loading data...')
    seg_df = C.load_segments(); crashes = C.load_crashes(); edges = C.load_edges()
    seg_index = {sid: i for i, sid in enumerate(seg_df['segment_id'])}
    N = len(seg_df)

    hist_sev = C.severity_matrix(crashes, seg_index, C.HISTORY_YEARS)
    tgt_sev  = C.severity_matrix(crashes, seg_index, C.TARGET_YEARS)

    if args.holdout:
        city_mask = C.in_city(seg_df, args.holdout); active = ~city_mask
        hist_for_build = hist_sev.copy(); hist_for_build[city_mask] = 0.0
        print(f'Holdout {args.holdout}: {city_mask.sum():,} excluded')
    else:
        city_mask = np.zeros(N, dtype=bool); active = np.ones(N, dtype=bool)
        hist_for_build = hist_sev

    print('Building adjacency + edge_index...')
    indptr, neighbors = C.build_adjacency(edges, seg_index)
    edge_index = build_edge_index(edges, seg_index)
    rc_x, rc_cols = C.road_class_onehot(seg_df)

    crash_bearing = tgt_sev.sum(axis=1) > 0
    eval_mask = (crash_bearing & city_mask) if args.holdout else crash_bearing
    print(f'Eval segments: {eval_mask.sum():,}')

    risk_ml = np.zeros((N, len(C.VEHICLE_TYPES)), dtype=np.float32)
    active_idx = np.where(active)[0]

    for ti, tname in enumerate(C.VEHICLE_TYPES):
        t0 = time.time()
        cluster_id = C.bfs_clusters(indptr, neighbors, hist_for_build[:, ti],
                                    args.min_crashes, active_mask=None)
        cframe = C.cluster_frame(cluster_id, hist_for_build, tgt_sev, seg_df, ti)
        feats, _ = C.build_type_features(seg_df, ti, cluster_id, cframe, rc_x, rc_cols)
        feats = zscore(feats)
        y = C.cluster_target_share(cluster_id, cframe)

        # capped training rows: keep all active crash-bearing, subsample zeros
        act_cb = active & (hist_for_build[:, ti] > 0)
        act_zero = active & ~act_cb
        cb_idx = np.where(act_cb)[0]
        zero_idx = np.where(act_zero)[0]
        budget = max(0, args.max_train - len(cb_idx))
        if len(zero_idx) > budget:
            zero_idx = np.random.choice(zero_idx, budget, replace=False)
        train_rows = torch.tensor(np.concatenate([cb_idx, zero_idx]))

        risk_ml[:, ti] = train_one_type(feats, edge_index, y, train_rows, args, device)
        print(f'  {tname:<11} clusters={cluster_id.max()+1:>7,}  '
              f'train={len(train_rows):,}  ({time.time()-t0:.1f}s)')

    rho = C.cross_type_rho(risk_ml, eval_mask)
    jac = C.topn_jaccard(risk_ml, eval_mask, n=1000)
    val = C.validity(risk_ml, tgt_sev, eval_mask)
    vstr = '  '.join(f'{t}={val[t]:.3f}' for t in C.VEHICLE_TYPES)
    print('\n' + '=' * 68)
    print(f'GAT (cluster+share)  holdout={args.holdout or "none"}')
    print('=' * 68)
    print(f'  cross-type rho = {rho:.3f}   (lower = more divergence)')
    print(f'  top-1000 Jaccard = {jac:.3f}')
    print(f'  validity vs real target crashes: {vstr}')

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
        path = args.out or f'{args.predict_city}_gat_risk.csv'
        out.to_csv(path, index=False)
        print(f'\nWrote routing risk surface -> {path}  ({len(out):,} rows)')


if __name__ == '__main__':
    main()
