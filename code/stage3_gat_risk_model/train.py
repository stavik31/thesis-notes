#!/usr/bin/env python3
"""
Stage 3 — GAT Risk Model

Trains a Graph Attention Network with vehicle-type-conditioned attention on
the segmented road network. Produces risk_scores.csv: one row per
(segment_id, vehicle_type) with a severity-weighted crash rate.

Usage:
  python train.py --city london          # quick test (~minutes)
  python train.py                        # full Great Britain run
"""

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import torch
import torch.nn.functional as F
from torch import nn
from torch_geometric.data import Data
from torch_geometric.nn import GATConv
from torch_geometric.loader import NeighborLoader
from tqdm import tqdm

# ── Constants ─────────────────────────────────────────────────────────────────

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']
TYPE_TO_IDX   = {t: i for i, t in enumerate(VEHICLE_TYPES)}

# WHY this mapping: AADF is recorded per vehicle category in DfT counts.
# We pick the closest column for each of our 5 crash types so that when we
# divide predicted count by exposure we are dividing by the right traffic volume.
# motorcycle uses two_wheeled_motor_vehicles (includes mopeds — best available proxy).
AADF_COL = {
    'car':        'cars_and_taxis',
    'motorcycle': 'two_wheeled_motor_vehicles',
    'cycle':      'pedal_cycles',
    'lgv':        'lgvs',
    'hgv':        'all_hgvs',
}

TRAIN_YEARS  = [2020, 2021, 2022, 2023]
HOLDOUT_YEAR = 2024   # never seen during training — reserved for Stage 6 evaluation

# WHY bounding boxes: centroid_lon/lat was stored in segments.gpkg in Stage 2
# so we can filter without touching the geometry column (much faster).
# lon_min, lat_min, lon_max, lat_max — WGS84
CITIES = {
    'london':     (-0.51, 51.28,  0.33, 51.72),
    'birmingham': (-2.05, 52.35, -1.75, 52.60),
    'manchester': (-2.40, 53.33, -2.10, 53.55),
    'leeds':      (-1.70, 53.72, -1.45, 53.88),
}

CODE_DIR = Path(__file__).parent.parent
OUTPUTS  = CODE_DIR / 'outputs'

# ── Args ──────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description='Stage 3: GAT risk model')
    p.add_argument('--city',       choices=list(CITIES.keys()), default=None,
                   help='Restrict to a city bounding box for testing')
    p.add_argument('--epochs',     type=int,   default=200,
                   help='Maximum epochs (early stopping will usually trigger first)')
    p.add_argument('--patience',   type=int,   default=15,
                   help='Stop after this many epochs with no meaningful improvement')
    p.add_argument('--min_delta',  type=float, default=0.0001,
                   help='Minimum val loss improvement to count as progress')
    p.add_argument('--batch_size', type=int,   default=512)
    p.add_argument('--lr',         type=float, default=1e-3)
    p.add_argument('--emb_dim',    type=int,   default=16,
                   help='Vehicle type embedding size')
    p.add_argument('--hidden',     type=int,   default=64,
                   help='GAT hidden channels per head')
    p.add_argument('--heads',      type=int,   default=4,
                   help='Attention heads (intermediate layers only)')
    p.add_argument('--layers',     type=int,   default=2,
                   help='Number of GAT layers (= neighbourhood hop radius)')
    p.add_argument('--seed',       type=int,   default=42)
    return p.parse_args()

# ── Data loading ───────────────────────────────────────────────────────────────

def load_data(city):
    # WHY load all three files: segments give node features, crashes give
    # training targets, edges give graph structure. All three are needed to
    # build the PyG Data object.
    t0 = time.time()
    print('Loading segments.gpkg...', flush=True)
    segments = gpd.read_file(OUTPUTS / 'segments.gpkg')
    print(f'  {len(segments):,} segments  ({time.time()-t0:.1f}s)')

    if city:
        lon_min, lat_min, lon_max, lat_max = CITIES[city]
        mask = (
            (segments['centroid_lon'] >= lon_min) & (segments['centroid_lon'] <= lon_max) &
            (segments['centroid_lat'] >= lat_min) & (segments['centroid_lat'] <= lat_max)
        )
        segments = segments[mask].reset_index(drop=True)
        print(f'  city={city}: {len(segments):,} segments')

    city_ids = set(segments['segment_id']) if city else None

    print('Loading crashes_segmented.csv...', flush=True)
    crashes = pd.read_csv(OUTPUTS / 'crashes_segmented.csv', low_memory=False)
    if city:
        # WHY filter crashes AND edges by the same city_ids: we need a
        # self-contained subgraph where every node, edge, and crash record
        # refers to a segment that actually exists in our filtered node set.
        crashes = crashes[crashes['segment_id'].isin(city_ids)].reset_index(drop=True)
        print(f'  city filter: {len(crashes):,} crashes')

    print('Loading graph_edges.csv...', flush=True)
    edges = pd.read_csv(OUTPUTS / 'graph_edges.csv')
    if city:
        edges = edges[
            edges['segment_id_a'].isin(city_ids) &
            edges['segment_id_b'].isin(city_ids)
        ].reset_index(drop=True)
        print(f'  city filter: {len(edges):,} edges')

    return segments, crashes, edges

# ── Feature engineering ────────────────────────────────────────────────────────

def build_features(segments):
    # WHY these six columns:
    #   road_class         → risk profile differs by class (motorways are fast but regulated;
    #                        unclassified roads are slow but lack safety infrastructure)
    #   length_m           → longer segments accumulate more crashes just by being longer;
    #                        without this, a 5m stub and a 2km A-road look equivalent
    #   all_motor_vehicles → total traffic volume; the GAT uses this to distinguish
    #                        "genuinely dangerous" from "high-crash only because busy"
    #   aadf_fallback      → 41.7% of segments used a road-class mean instead of a real
    #                        count point (Stage 2 limitation); flagging it lets the model
    #                        learn to weight those segments' exposure estimates differently
    #   centroid_lon/lat   → spatial position; lets the GAT learn geography-driven risk
    #                        patterns (e.g. urban density gradients) through message passing
    df = segments[['road_class', 'length_m', 'all_motor_vehicles',
                   'aadf_fallback', 'centroid_lon', 'centroid_lat']].copy()

    # WHY one-hot encode road_class: it is a nominal category with no natural
    # ordering, so we cannot represent it as an integer (that would imply
    # "Motorway" > "A Road" mathematically, which is meaningless).
    rc = pd.get_dummies(df['road_class'], prefix='rc').astype(float)
    df = pd.concat([df.drop(columns='road_class'), rc], axis=1)

    # WHY z-score normalisation: neural networks are sensitive to feature scale.
    # Without it, length_m (range ~1–5000 m) would dominate the gradient signal
    # and effectively drown out the 0/1 fallback flag and the one-hot dummies.
    for col in ['length_m', 'all_motor_vehicles', 'centroid_lon', 'centroid_lat']:
        std = df[col].std()
        df[col] = (df[col] - df[col].mean()) / std if std > 0 else 0.0

    df['aadf_fallback'] = df['aadf_fallback'].astype(float)

    x = torch.tensor(df.values.astype(np.float32))
    print(f'  Node features: {x.shape[1]} dims  '
          f'({rc.shape[1]} road-class dummies + 5 numeric)')
    return x

# ── Targets ───────────────────────────────────────────────────────────────────

def build_targets(crashes, seg_to_idx, num_nodes):
    # WHY severity-weighted counts instead of raw counts: not all crashes are equal.
    # A fatal crash (weight 3) on a segment should flag it as far riskier than a
    # slight-injury crash (weight 1). Weighting before aggregation bakes this
    # into the training signal rather than treating every incident identically.
    #
    # WHY exclude HOLDOUT_YEAR here: the holdout year (2024) is never touched
    # until Stage 6 evaluation. If it leaked into the targets the model trains on,
    # the Stage 6 test would be meaningless — we would be evaluating on data the
    # model has already learned from.
    tc = crashes[crashes['accident_year'].isin(TRAIN_YEARS)].copy()
    tc['nidx'] = tc['segment_id'].map(seg_to_idx)
    tc['tidx'] = tc['vehicle_type'].map(TYPE_TO_IDX)
    tc = tc.dropna(subset=['nidx', 'tidx'])
    tc['nidx'] = tc['nidx'].astype(int)
    tc['tidx'] = tc['tidx'].astype(int)

    # WHY np.add.at instead of a loop: vectorised scatter-add over 885k rows
    # is ~100× faster than iterating row by row.
    y = np.zeros((num_nodes, len(VEHICLE_TYPES)), dtype=np.float32)
    np.add.at(y, (tc['nidx'].values, tc['tidx'].values), tc['severity_weight'].values)

    nonzero_pct = 100 * (y > 0).mean()
    print(f'  Target matrix: {y.shape}  ({nonzero_pct:.1f}% non-zero cells)')
    return torch.tensor(y)

# ── Dispersion check ───────────────────────────────────────────────────────────

def dispersion_check(y):
    # WHY check dispersion before fixing the loss: Poisson regression assumes
    # variance = mean. Crash count data almost never satisfies this:
    #   - Over-dispersed (var >> mean): Poisson underestimates the probability
    #     of high-count segments — use Negative Binomial instead.
    #   - Under-dispersed (var < mean): the opposite problem — Pathivada 2025
    #     found motorcycle segment counts flip to this regime because most segments
    #     have 0 or 1 motorcycle crash, with almost no high outliers.
    # This script uses Poisson NLL throughout (simpler, differentiable in PyTorch).
    # The table below flags where a different loss would improve fit — actionable
    # in a later tuning pass once we have the basic model working.
    print('\nDispersion check (total severity-weight per segment, training years):')
    print(f'  {"Type":<12} {"Mean":>8} {"Variance":>12} {"Var/Mean":>10}  Regime')
    print(f'  ' + '-'*60)
    for i, t in enumerate(VEHICLE_TYPES):
        c   = y[:, i].numpy()
        mu  = c.mean()
        var = c.var()
        r   = var / mu if mu > 0 else float('nan')
        if   r > 2:   regime = 'over-dispersed  → NB preferred'
        elif r < 0.8: regime = 'under-dispersed → CMP preferred'
        else:         regime = 'Poisson OK'
        print(f'  {t:<12} {mu:>8.4f} {var:>12.4f} {r:>10.3f}   {regime}')
    print()

# ── Graph construction ─────────────────────────────────────────────────────────

def build_edge_index(edges, seg_to_idx):
    # WHY convert UUIDs to integers: PyG's edge_index must be a long tensor of
    # integer node indices — it is used as an index into the node feature matrix,
    # which requires integers, not strings.
    #
    # WHY make the graph undirected (add both directions): crash risk propagates
    # both ways across a junction. A dangerous intersection affects every road
    # leading to it regardless of travel direction. Making edges symmetric lets
    # every node aggregate information from all its physical neighbours.
    a = edges['segment_id_a'].map(seg_to_idx)
    b = edges['segment_id_b'].map(seg_to_idx)
    valid = a.notna() & b.notna()
    a = a[valid].astype(int).values
    b = b[valid].astype(int).values

    edge_index = torch.tensor(
        np.stack([np.concatenate([a, b]), np.concatenate([b, a])]),
        dtype=torch.long
    )
    print(f'  Edge index: {edge_index.shape[1]:,} directed edges '
          f'(from {len(a):,} undirected pairs)')
    return edge_index

# ── Model ──────────────────────────────────────────────────────────────────────

class VehicleTypeGAT(nn.Module):
    """
    GAT with vehicle type re-injected at every layer.

    WHY re-inject the type embedding at every layer (not just at input):
    The attention weight α_ij between nodes i and j is computed from their
    feature vectors. If we only add the type embedding at the start, by the
    second layer the node representations are already mixed with neighbour
    information and the type signal has diluted. Re-injecting before each
    GATConv call forces every attention computation to remain type-aware all
    the way through the network — a motorcycle embedding keeps shifting
    attention toward junctions and urban segments at every hop.

    Architecture (default: 2 layers, hidden=64, heads=4):
      Layer 1: GATConv(in_channels+emb_dim, 64, heads=4, concat=True) → 256 ch
      Proj 1:  Linear(256 → 64)       ← bring back to `hidden` before next layer
      Layer 2: GATConv(64+emb_dim, 64, heads=1, concat=False)         →  64 ch
      Output:  Softplus(Linear(64 → 1))                                →   1 ch

    WHY Softplus on output: predicted crash counts must be strictly positive
    (you cannot have −0.3 crashes on a segment). Softplus = log(1 + e^x) is
    always > 0 and differentiable everywhere — unlike ReLU which has a gradient
    of 0 for negative inputs (dead neuron problem).

    WHY proj_layers between GAT layers: after a multi-head GATConv with 4 heads,
    the output is hidden*heads = 256 channels. The next GAT layer expects
    `hidden + emb_dim` as input. The projection Linear(256 → 64) brings it back
    to a consistent size before we concatenate the type embedding again.
    """

    def __init__(self, in_channels, emb_dim, hidden, num_types, heads, num_layers):
        super().__init__()
        self.num_layers = num_layers
        self.type_emb   = nn.Embedding(num_types, emb_dim)

        self.gat_layers  = nn.ModuleList()
        self.proj_layers = nn.ModuleList()

        for i in range(num_layers):
            in_dim  = (in_channels if i == 0 else hidden) + emb_dim
            is_last = (i == num_layers - 1)
            n_heads = 1 if is_last else heads
            self.gat_layers.append(
                GATConv(in_dim, hidden, heads=n_heads, concat=not is_last)
            )
            if not is_last:
                self.proj_layers.append(nn.Linear(hidden * heads, hidden))

        self.output_head = nn.Sequential(nn.Linear(hidden, 1), nn.Softplus())

    def forward(self, x, edge_index, type_idx):
        emb = self.type_emb(torch.tensor(type_idx, device=x.device))
        emb = emb.unsqueeze(0).expand(x.size(0), -1)

        h = x
        for i, gat in enumerate(self.gat_layers):
            h = torch.cat([h, emb], dim=1)        # inject type at this layer
            h = gat(h, edge_index)
            if i < self.num_layers - 1:
                # WHY ELU (not ReLU): ELU has non-zero gradient for negative
                # inputs, which helps with vanishing gradients in deeper networks.
                h = F.elu(h)
                # WHY dropout here (not on output): regularisation between layers
                # prevents the model from memorising individual segment crash
                # histories rather than learning generalised risk patterns.
                h = F.dropout(h, p=0.1, training=self.training)
                h = self.proj_layers[i](h)

        return self.output_head(h).squeeze(-1)     # (num_nodes,)

# ── Training / evaluation ──────────────────────────────────────────────────────

def run_epoch(model, loader, y_full, optimizer, device, train=True, desc=''):
    # WHY iterate over vehicle types in the outer loop: the model produces one
    # risk score per (segment, type) combination. Rather than modifying the
    # graph structure per type, we do one full pass of the dataloader per type,
    # changing only the type_idx fed into the model. This reuses the same sampled
    # mini-batches across types (same neighbourhood context, different attention).
    #
    # WHY Poisson NLL loss: crash counts are non-negative integers — Poisson is
    # the natural distribution for this. The loss is -log P(y | λ) = λ - y·log(λ),
    # which penalises the model when its predicted rate λ diverges from the
    # observed count y. log_input=False because the model outputs λ directly
    # (via Softplus), not log(λ).
    #
    # WHY loss only on seed nodes (not all nodes in the batch): NeighborLoader
    # samples a subgraph of seed_nodes + their neighbours. The neighbour nodes
    # are only there to provide context for the attention computation — computing
    # loss on them too would mean training on nodes we didn't intend to sample
    # in this batch, breaking the mini-batch construction logic.
    model.train(train)
    ctx = torch.enable_grad() if train else torch.no_grad()
    total_loss, n_batches = 0.0, 0

    with ctx:
        for type_idx, type_name in enumerate(VEHICLE_TYPES):
            bar = tqdm(loader, desc=f'  {desc} {type_name:<12}', leave=False)
            for batch in bar:
                batch = batch.to(device)
                pred  = model(batch.x, batch.edge_index, type_idx)

                seed        = slice(0, batch.batch_size)
                pred_seed   = pred[seed]
                target_seed = y_full[batch.n_id[seed].cpu(), type_idx].to(device)

                loss = F.poisson_nll_loss(pred_seed, target_seed,
                                          log_input=False, full=False)
                if train:
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                total_loss += loss.item()
                n_batches  += 1
                bar.set_postfix(loss=f'{loss.item():.4f}')

    return total_loss / n_batches if n_batches else 0.0

# ── Risk score extraction ──────────────────────────────────────────────────────

@torch.no_grad()
def extract_risk_scores(model, data, segments, args, device):
    # WHY divide by exposure to get risk_score:
    # The model predicts a raw severity-weighted crash count per segment.
    # But a segment with 10 crashes and 10,000 vehicles/day is far safer than
    # one with 10 crashes and 50 vehicles/day. Dividing by exposure (AADF ×
    # length_km × num_years) gives a rate: crashes per vehicle-kilometre, which
    # is comparable across segments of different length and traffic volume.
    # This is the standard exposure-normalised risk measure in the road safety
    # literature (Gao 2024, Jiang 2022).
    #
    # WHY batch_size * 4 for inference: no gradients are computed during
    # inference, so PyTorch does not need to store intermediate activations for
    # backprop. This frees up roughly 4× the memory, allowing much larger batches
    # and faster throughput.
    model.eval()

    inf_loader = NeighborLoader(
        data,
        num_neighbors=[10, 5],
        batch_size=args.batch_size * 4,
        input_nodes=torch.arange(data.num_nodes),
        shuffle=False,
    )

    all_preds = torch.zeros(data.num_nodes, len(VEHICLE_TYPES))

    for type_idx, type_name in enumerate(VEHICLE_TYPES):
        print(f'  {type_name}...', end='', flush=True)
        for batch in inf_loader:
            batch = batch.to(device)
            pred  = model(batch.x, batch.edge_index, type_idx)
            all_preds[batch.n_id[:batch.batch_size].cpu(), type_idx] = \
                pred[:batch.batch_size].cpu()
        print(' done')

    records = []
    for type_idx, type_name in enumerate(VEHICLE_TYPES):
        pred_counts = all_preds[:, type_idx].numpy()
        aadf        = segments[AADF_COL[type_name]].fillna(0).values
        exposure    = aadf * (segments['length_m'].values / 1000.0) * len(TRAIN_YEARS)
        risk_score  = np.where(exposure > 0, pred_counts / exposure, 0.0)

        records.append(pd.DataFrame({
            'segment_id':   segments['segment_id'].values,
            'vehicle_type': type_name,
            'pred_count':   pred_counts,
            'exposure_vkm': exposure,
            'risk_score':   risk_score,
        }))

    return pd.concat(records, ignore_index=True)

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    args = parse_args()
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Device: {device}')
    if args.city:
        print(f'City:   {args.city}')
    print()

    # ── Load ──
    segments, crashes, edges = load_data(args.city)
    seg_to_idx = {sid: i for i, sid in enumerate(segments['segment_id'])}
    num_nodes  = len(segments)

    # ── Build graph inputs ──
    print('\nBuilding node features...')
    x = build_features(segments)

    print('Building targets...')
    y = build_targets(crashes, seg_to_idx, num_nodes)

    dispersion_check(y)

    print('Building edge index...')
    edge_index = build_edge_index(edges, seg_to_idx)
    data = Data(x=x, edge_index=edge_index, y=y, num_nodes=num_nodes)

    # ── Train / val split ──
    # WHY 80/20 on nodes rather than on years: a temporal split would mean
    # validation segments are the same as training segments (just a different
    # year). Splitting on nodes instead checks whether the model generalises
    # to unseen road segments — a harder and more honest test. The true
    # temporal holdout (2024) remains untouched until Stage 6.
    g     = torch.Generator().manual_seed(args.seed)
    perm  = torch.randperm(num_nodes, generator=g)
    split = int(0.8 * num_nodes)
    train_idx, val_idx = perm[:split], perm[split:]

    # WHY num_neighbors=[10, 5]: for a 2-layer GAT, each seed node needs its
    # 1-hop neighbours (we sample 10) and their 1-hop neighbours (we sample 5).
    # This gives each seed node a 2-hop receptive field without loading the
    # entire graph into memory. The numbers are a standard starting point;
    # higher values = more accurate aggregation but more memory and slower batches.
    kw = dict(num_neighbors=[10, 5], batch_size=args.batch_size)
    train_loader = NeighborLoader(data, input_nodes=train_idx, shuffle=True,  **kw)
    val_loader   = NeighborLoader(data, input_nodes=val_idx,   shuffle=False, **kw)

    # ── Model ──
    model = VehicleTypeGAT(
        in_channels=x.shape[1],
        emb_dim=args.emb_dim,
        hidden=args.hidden,
        num_types=len(VEHICLE_TYPES),
        heads=args.heads,
        num_layers=args.layers,
    ).to(device)
    print(f'Model: {sum(p.numel() for p in model.parameters()):,} parameters\n')

    # WHY Adam: adaptive learning rates per parameter, which is important here
    # because some node features (sparse crash history) have very different
    # gradient magnitudes than others (dense road class features).
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    # WHY ReduceLROnPlateau: if validation loss stops improving for 5 epochs,
    # the current learning rate is likely too large to find a better minimum —
    # the optimiser is stepping past it. Halving the rate lets it take finer
    # steps and escape the plateau without manually tuning a schedule.
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, patience=5, factor=0.5, min_lr=1e-5
    )

    # ── Training loop with early stopping ──
    # WHY early stopping: a fixed epoch count is arbitrary. Early stopping lets
    # the model train until improvement becomes insignificant — defined as val loss
    # not dropping by at least min_delta for `patience` consecutive epochs.
    # The LR scheduler handles plateaus by halving the rate; early stopping handles
    # the case where even a lower LR can no longer find meaningful improvements.
    print(f'Training up to {args.epochs} epochs  '
          f'(early stop: patience={args.patience}, min_delta={args.min_delta})\n'
          f'  train {len(train_idx):,} | val {len(val_idx):,} nodes\n')

    best_val, best_state = float('inf'), None
    epochs_no_improve = 0

    for epoch in range(1, args.epochs + 1):
        t0  = time.time()
        tr  = run_epoch(model, train_loader, y, optimizer, device,
                        train=True,  desc=f'[{epoch}] train')
        val = run_epoch(model, val_loader,   y, None,      device,
                        train=False, desc=f'[{epoch}] val  ')
        scheduler.step(val)
        elapsed = time.time() - t0

        marker = ''
        if val < best_val - args.min_delta:
            best_val         = val
            best_state       = {k: v.clone() for k, v in model.state_dict().items()}
            epochs_no_improve = 0
            marker           = '  ★'
        else:
            epochs_no_improve += 1

        print(f'  [{epoch:3d}]  train {tr:.4f}  val {val:.4f}  '
              f'{elapsed:.0f}s  (no improve: {epochs_no_improve}/{args.patience}){marker}')

        if epochs_no_improve >= args.patience:
            print(f'\nEarly stopping at epoch {epoch} — '
                  f'no improvement for {args.patience} consecutive epochs.')
            break

    # ── Extract risk scores ──
    # WHY restore best checkpoint: the model at the last epoch is not necessarily
    # the best — validation loss can worsen in later epochs if the model starts
    # overfitting. We saved a copy of the weights every time val loss improved (★)
    # and restore those now before running inference.
    print(f'\nBest val loss {best_val:.4f} — restoring best checkpoint')
    model.load_state_dict(best_state)

    print('Extracting risk scores...')
    risk_df = extract_risk_scores(model, data, segments, args, device)

    out = OUTPUTS / 'risk_scores.csv'
    risk_df.to_csv(out, index=False)
    print(f'\nSaved → {out}')
    print(f'  {len(risk_df):,} rows  ({num_nodes:,} segments × {len(VEHICLE_TYPES)} types)')

    print('\nRisk score summary (non-zero segments):')
    for t in VEHICLE_TYPES:
        s = risk_df[(risk_df['vehicle_type'] == t) & (risk_df['risk_score'] > 0)]['risk_score']
        print(f'  {t:<12}  {len(s):>8,} non-zero  '
              f'mean={s.mean():.6f}  max={s.max():.6f}')


if __name__ == '__main__':
    main()
