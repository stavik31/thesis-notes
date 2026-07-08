#!/usr/bin/env python3
"""
Training-descriptive plots for the Stage 3 cluster+share risk engine.
(Replaces the stale GAT make_plots.py.)

Reads THIS engine's outputs and draws plots that describe the trained model and
its surface — no experiment/comparison plots (those are handled separately):

  outputs/plots/1_risk_distribution.png   per-type predicted-risk histograms
  outputs/plots/2_risk_maps.png           per-type national risk surface (hexbin)
  outputs/plots/3_feature_importance.png  per-type XGBoost feature importance
  outputs/plots/4_summary.png             per-type summary table
  outputs/plots/5_cluster_size_dist.png   per-type cluster-size distribution

Inputs: outputs/{risk_scores.csv, risk_feature_importance.csv, segments.gpkg}.
Cluster sizes aren't saved by train.py, so we recompute them once (reusing the
engine's own clustering) and cache to outputs/cluster_sizes.npz.

Usage:  python make_plots.py
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pyogrio

import train as T   # reuse the engine's constants + loaders + clustering

OUT   = T.OUTPUTS
PLOTS = OUT / 'plots'
TYPES = T.VEHICLE_TYPES
COLOR = {'car': '#1f77b4', 'motorcycle': '#ff7f0e', 'cycle': '#2ca02c',
         'lgv': '#d62728', 'hgv': '#9467bd'}


def _t(msg, t0):
    print(f'  {msg} ({time.time()-t0:.1f}s)', flush=True)


def load_risk_long():
    t0 = time.time()
    df = pd.read_csv(OUT / 'risk_scores.csv',
                     usecols=['segment_id', 'vehicle_type', 'risk_score'])
    _t(f'risk_scores.csv: {len(df):,} rows', t0)
    return df


def get_cluster_sizes():
    """Per-type cluster sizes — recomputed via the engine's own clustering and
    cached, since train.py doesn't persist them."""
    cache = OUT / 'cluster_sizes.npz'
    if cache.exists():
        z = np.load(cache, allow_pickle=True)
        return {t: z[t] for t in TYPES}
    print('  recomputing clusters (one-time, cached after)...', flush=True)
    seg, crashes, edges = T.load_data(None)
    seg_index = {sid: i for i, sid in enumerate(seg['segment_id'])}
    hist = T.severity_matrix(crashes, seg_index, T.HISTORY_YEARS)
    indptr, nbr = T.build_adjacency(edges, seg_index)
    sizes = {}
    for ti, t in enumerate(TYPES):
        cid = T.bfs_clusters(indptr, nbr, hist[:, ti], T.MIN_CRASHES)
        sizes[t] = np.bincount(cid[cid >= 0])
    np.savez(cache, **sizes)
    return sizes


# ── plots ────────────────────────────────────────────────────────────────────

def plot_risk_distribution(risk):
    fig, axes = plt.subplots(1, 5, figsize=(22, 4), sharey=True)
    for ax, t in zip(axes, TYPES):
        v = risk.loc[risk['vehicle_type'] == t, 'risk_score'].values
        ax.hist(v, bins=60, range=(0, 1), color=COLOR[t], alpha=0.85)
        ax.set_yscale('log')
        ax.set_title(f'{t}\nmean={v.mean():.3f}  max={v.max():.3f}')
        ax.set_xlabel('predicted risk (share)')
    axes[0].set_ylabel('segments (log)')
    fig.suptitle('Per-type predicted-risk distribution (national surface)', fontweight='bold')
    fig.tight_layout()
    fig.savefig(PLOTS / '1_risk_distribution.png', dpi=130)
    plt.close(fig)


def plot_risk_maps(risk, cents):
    fig, axes = plt.subplots(1, 5, figsize=(24, 6))
    for ax, t in zip(axes, TYPES):
        d = risk[risk['vehicle_type'] == t].merge(cents, on='segment_id')
        hb = ax.hexbin(d['centroid_lon'], d['centroid_lat'], C=d['risk_score'],
                       reduce_C_function=np.mean, gridsize=280, cmap='inferno',
                       mincnt=1)
        ax.set_title(t); ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
        fig.colorbar(hb, ax=ax, shrink=0.6)
    fig.suptitle('Per-type risk surface over Great Britain (mean predicted risk per cell)',
                 fontweight='bold')
    fig.tight_layout()
    fig.savefig(PLOTS / '2_risk_maps.png', dpi=130)
    plt.close(fig)


def plot_feature_importance():
    imp = pd.read_csv(OUT / 'risk_feature_importance.csv', index_col=0)
    fig, axes = plt.subplots(1, 5, figsize=(24, 5), sharex=False)
    for ax, t in zip(axes, TYPES):
        s = imp[t].sort_values(ascending=True).tail(10)
        ax.barh(s.index, s.values, color=COLOR[t])
        ax.set_title(t); ax.tick_params(axis='y', labelsize=7)
    fig.suptitle('Per-type XGBoost feature importance (top 10, gain)', fontweight='bold')
    fig.tight_layout()
    fig.savefig(PLOTS / '3_feature_importance.png', dpi=130)
    plt.close(fig)


def plot_summary(risk, sizes):
    rows = []
    for t in TYPES:
        v = risk.loc[risk['vehicle_type'] == t, 'risk_score'].values
        s = sizes[t]
        rows.append([t, f'{len(s):,}', f'{np.median(s):.0f}', f'{s.max():,}',
                     f'{v.mean():.3f}', f'{np.percentile(v,90):.3f}',
                     f'{v.max():.3f}', f'{(v>0.5).mean()*100:.1f}%'])
    cols = ['type', 'n_clusters', 'median\ncluster size', 'max\ncluster size',
            'mean\nrisk', 'p90\nrisk', 'max\nrisk', '% risk\n>0.5']
    fig, ax = plt.subplots(figsize=(13, 2.6)); ax.axis('off')
    tab = ax.table(cellText=rows, colLabels=cols, loc='center', cellLoc='center')
    tab.auto_set_font_size(False); tab.set_fontsize(10); tab.scale(1, 2.0)
    for j in range(len(cols)):
        tab[0, j].set_facecolor('#333'); tab[0, j].set_text_props(color='w', fontweight='bold')
    for i, t in enumerate(TYPES, start=1):
        tab[i, 0].set_facecolor(COLOR[t]); tab[i, 0].set_text_props(color='w', fontweight='bold')
    fig.suptitle('Stage 3 per-type training summary', fontweight='bold')
    fig.tight_layout()
    fig.savefig(PLOTS / '4_summary.png', dpi=130)
    plt.close(fig)


def plot_cluster_sizes(sizes):
    fig, axes = plt.subplots(1, 5, figsize=(22, 4), sharey=True)
    for ax, t in zip(axes, TYPES):
        s = sizes[t]
        ax.hist(s, bins=np.logspace(0, np.log10(max(s.max(), 2)), 40), color=COLOR[t])
        ax.set_xscale('log'); ax.set_yscale('log')
        ax.set_title(f'{t}\n{len(s):,} clusters  median={np.median(s):.0f}')
        ax.set_xlabel('segments per cluster (log)')
    axes[0].set_ylabel('clusters (log)')
    fig.suptitle('Per-type cluster-size distribution (adaptive: dense→small, sparse→large)',
                 fontweight='bold')
    fig.tight_layout()
    fig.savefig(PLOTS / '5_cluster_size_dist.png', dpi=130)
    plt.close(fig)


def main():
    PLOTS.mkdir(exist_ok=True)
    risk = load_risk_long()
    t0 = time.time()
    cents = pyogrio.read_dataframe(OUT / 'segments.gpkg', read_geometry=False,
                                   columns=['segment_id', 'centroid_lon', 'centroid_lat'])
    _t('segment centroids', t0)
    sizes = get_cluster_sizes()

    for name, fn in [('1 risk distribution', lambda: plot_risk_distribution(risk)),
                     ('2 risk maps',         lambda: plot_risk_maps(risk, cents)),
                     ('3 feature importance', plot_feature_importance),
                     ('4 summary',           lambda: plot_summary(risk, sizes)),
                     ('5 cluster sizes',     lambda: plot_cluster_sizes(sizes))]:
        t0 = time.time(); fn(); _t(f'plot {name}', t0)

    print(f'\nDone. 5 plots -> {PLOTS}')


if __name__ == '__main__':
    main()
