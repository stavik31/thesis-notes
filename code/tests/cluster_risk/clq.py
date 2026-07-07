#!/usr/bin/env python3
"""
Colocation Quotient (CLQ) — model-free certification that vehicle types crash in
spatially divergent places.

Leslie & Kronenfeld (2011), "The colocation quotient: a new measure of spatial
association between categorical subsets of points", Geographical Analysis. Used
for vehicle-type spatial divergence by Lee (2018) and Hu (2018) — the founding
papers of this thesis's niche. This is the industry-standard statistic for the
PREMISE claim ("the divergence is real"), independent of any clustering/model.

Operates on RAW map-matched crash points (crashes_segmented.csv, lat/lon projected
to British National Grid metres). For each ordered type pair (A -> B):

  CLQ_{A->B} = [ (1/N_A) * sum_{i in A} (#B among i's k nearest neighbours)/k ]
               / [ N_B' / (N-1) ]        N_B' = N_B (A!=B) or N_B-1 (A==B)

  CLQ = 1 : colocated at chance     <1 : SEGREGATED (divergence)     >1 : attracted

Significance by label-permutation Monte Carlo: the k-NN structure is fixed; only
the type labels are shuffled, so the null is "same points, types assigned at
random". p_low = P(CLQ_perm <= CLQ_obs) tests significant segregation (CLQ<1).
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from pyproj import Transformer

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']
OUTPUTS = Path(__file__).resolve().parents[2] / 'outputs'
K = 10          # nearest neighbours
N_PERM = 199    # permutations (min p-value = 1/200 = 0.005)
SEED = 42


def clq_matrix(lab, nbr_idx, N, k):
    """5x5 CLQ matrix for label array `lab` given fixed neighbour indices."""
    nbr = lab[nbr_idx]                       # [N, k] neighbour labels
    Ncls = np.bincount(lab, minlength=5).astype(float)
    cntB = np.stack([(nbr == b).sum(1) for b in range(5)], axis=1)  # [N,5]
    M = np.full((5, 5), np.nan)
    for a in range(5):
        mask = lab == a
        if mask.sum() == 0:
            continue
        num = cntB[mask].mean(0) / k         # [5] mean fraction of each B in A's nbrs
        den = (Ncls - np.eye(5)[a]) / (N - 1)  # subtract self only when b==a
        M[a] = num / np.where(den > 0, den, np.nan)
    return M


def main():
    t0 = time.time()
    df = pd.read_csv(OUTPUTS / 'crashes_segmented.csv', low_memory=False,
                     usecols=['latitude', 'longitude', 'vehicle_type'])
    df = df.dropna(subset=['latitude', 'longitude'])
    df = df[df['vehicle_type'].isin(VEHICLE_TYPES)].reset_index(drop=True)

    tr = Transformer.from_crs('EPSG:4326', 'EPSG:27700', always_xy=True)
    x, y = tr.transform(df['longitude'].values, df['latitude'].values)
    xy = np.column_stack([x, y])
    labels = df['vehicle_type'].map({t: i for i, t in enumerate(VEHICLE_TYPES)}
                                    ).values.astype(np.int64)
    N = len(labels)
    counts = np.bincount(labels, minlength=5)
    print(f'{N:,} crash points  ' +
          '  '.join(f'{t}={counts[i]:,}' for i, t in enumerate(VEHICLE_TYPES)) +
          f'  ({time.time()-t0:.1f}s)')

    t1 = time.time()
    tree = cKDTree(xy)
    _, idx = tree.query(xy, k=K + 1, workers=-1)   # +1 because first is self
    idx = idx[:, 1:]                                # drop self column -> [N,K]
    print(f'kNN (k={K}) built  ({time.time()-t1:.1f}s)')

    obs = clq_matrix(labels, idx, N, K)

    t2 = time.time()
    rng = np.random.default_rng(SEED)
    le = np.zeros((5, 5))    # count perm CLQ <= obs  (segregation test)
    ge = np.zeros((5, 5))    # count perm CLQ >= obs  (attraction test)
    for _ in range(N_PERM):
        pm = clq_matrix(rng.permutation(labels), idx, N, K)
        le += (pm <= obs)
        ge += (pm >= obs)
    p_low = (le + 1) / (N_PERM + 1)     # small -> significant segregation (CLQ<1)
    p_high = (ge + 1) / (N_PERM + 1)    # small -> significant attraction  (CLQ>1)
    print(f'permutation test ({N_PERM}x)  ({time.time()-t2:.1f}s)\n')

    hdr = '           ' + ''.join(f'{t:>12}' for t in VEHICLE_TYPES)
    print('CLQ_{A->B}  (row A -> col B; <1 = segregated = divergence)')
    print(hdr)
    for a, t in enumerate(VEHICLE_TYPES):
        cells = ''.join(f'{obs[a,b]:>12.3f}' for b in range(5))
        print(f'{t:>10} {cells}')

    print('\nSignificance (off-diagonal): CLQ<1 with p_low')
    seg_ok = True
    for a in range(5):
        for b in range(5):
            if a == b:
                continue
            tag = 'SEG*' if (obs[a, b] < 1 and p_low[a, b] < 0.01) else \
                  ('seg' if obs[a, b] < 1 else 'attr')
            if not (obs[a, b] < 1 and p_low[a, b] < 0.01):
                seg_ok = False
            print(f'  {VEHICLE_TYPES[a]:>10} -> {VEHICLE_TYPES[b]:<10} '
                  f'CLQ={obs[a,b]:.3f}  p_low={p_low[a,b]:.3f}  {tag}')

    off = obs[~np.eye(5, dtype=bool)]
    diag = np.diag(obs)
    print(f'\nmean off-diagonal (cross-type) CLQ = {off.mean():.3f}  '
          f'(1.0 = chance; <1 = divergence)')
    print(f'mean diagonal (self) CLQ           = {diag.mean():.3f}  '
          f'(>1 = each type self-clusters)')
    print(f'ALL cross-type pairs significantly segregated (CLQ<1, p<0.01): '
          f'{"YES" if seg_ok else "NO"}')


if __name__ == '__main__':
    main()
