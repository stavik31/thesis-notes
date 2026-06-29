#!/usr/bin/env python3
"""
Stage 3 — Presentation Plots
Run: .venv/bin/python stage3_gat_risk_model/make_plots.py
Output: outputs/plots/
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

plt.rcParams.update({
    'font.family':       'DejaVu Sans',
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.grid':         True,
    'grid.alpha':        0.3,
    'grid.linewidth':    0.6,
    'figure.facecolor':  'white',
    'axes.facecolor':    'white',
})

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']
COLOURS = {
    'car':        '#3498db',
    'motorcycle': '#e74c3c',
    'cycle':      '#2ecc71',
    'lgv':        '#f39c12',
    'hgv':        '#8e44ad',
}
LABELS = {
    'car': 'Car', 'motorcycle': 'Motorcycle',
    'cycle': 'Cycle', 'lgv': 'LGV', 'hgv': 'HGV',
}

CODE_DIR = Path(__file__).parent.parent
OUTPUTS  = CODE_DIR / 'outputs'
PLOTS    = OUTPUTS / 'plots'
PLOTS.mkdir(exist_ok=True)

# ── Training history (GB full run, 133 epochs) ────────────────────────────────
# Pasted directly from the terminal output — no re-run needed.
_LOSS_RAW = """
1 0.1210 0.1412 1
2 0.1172 0.1337 1
3 0.1163 0.1329 1
4 0.1157 0.1299 1
5 0.1152 0.1300 0
6 0.1149 0.1253 1
7 0.1147 0.1222 1
8 0.1145 0.1232 0
9 0.1143 0.1225 0
10 0.1141 0.1200 1
11 0.1139 0.1214 0
12 0.1139 0.1234 0
13 0.1138 0.1239 0
14 0.1137 0.1197 1
15 0.1137 0.1197 0
16 0.1136 0.1229 0
17 0.1135 0.1205 0
18 0.1134 0.1213 0
19 0.1134 0.1183 1
20 0.1134 0.1189 0
21 0.1133 0.1208 0
22 0.1133 0.1187 0
23 0.1133 0.1184 0
24 0.1132 0.1206 0
25 0.1131 0.1207 0
26 0.1128 0.1162 1
27 0.1127 0.1161 1
28 0.1127 0.1172 0
29 0.1126 0.1159 1
30 0.1126 0.1171 0
31 0.1126 0.1152 1
32 0.1125 0.1162 0
33 0.1125 0.1163 0
34 0.1125 0.1167 0
35 0.1125 0.1156 0
36 0.1125 0.1157 0
37 0.1125 0.1166 0
38 0.1123 0.1158 0
39 0.1122 0.1151 1
40 0.1122 0.1153 0
41 0.1122 0.1147 1
42 0.1122 0.1154 0
43 0.1122 0.1150 0
44 0.1121 0.1147 0
45 0.1121 0.1150 0
46 0.1122 0.1149 0
47 0.1121 0.1149 0
48 0.1122 0.1151 0
49 0.1121 0.1146 1
50 0.1121 0.1147 0
51 0.1121 0.1154 0
52 0.1121 0.1154 0
53 0.1121 0.1147 0
54 0.1121 0.1143 1
55 0.1121 0.1163 0
56 0.1121 0.1144 0
57 0.1120 0.1144 0
58 0.1121 0.1142 0
59 0.1120 0.1149 0
60 0.1121 0.1144 0
61 0.1121 0.1152 0
62 0.1120 0.1145 0
63 0.1121 0.1147 0
64 0.1120 0.1146 0
65 0.1120 0.1143 0
66 0.1119 0.1140 1
67 0.1119 0.1148 0
68 0.1119 0.1147 0
69 0.1119 0.1141 0
70 0.1119 0.1140 0
71 0.1119 0.1142 0
72 0.1119 0.1146 0
73 0.1119 0.1144 0
74 0.1118 0.1142 0
75 0.1118 0.1136 1
76 0.1118 0.1138 0
77 0.1118 0.1134 1
78 0.1118 0.1137 0
79 0.1118 0.1137 0
80 0.1117 0.1139 0
81 0.1118 0.1137 0
82 0.1117 0.1134 0
83 0.1118 0.1136 0
84 0.1118 0.1137 0
85 0.1118 0.1134 0
86 0.1118 0.1134 0
87 0.1118 0.1133 1
88 0.1118 0.1137 0
89 0.1118 0.1136 0
90 0.1117 0.1136 0
91 0.1118 0.1134 0
92 0.1118 0.1135 0
93 0.1117 0.1135 0
94 0.1118 0.1130 1
95 0.1117 0.1132 0
96 0.1118 0.1133 0
97 0.1118 0.1132 0
98 0.1118 0.1131 0
99 0.1117 0.1131 0
100 0.1118 0.1132 0
101 0.1118 0.1130 0
102 0.1118 0.1130 0
103 0.1118 0.1129 1
104 0.1118 0.1129 0
105 0.1117 0.1129 0
106 0.1118 0.1133 0
107 0.1118 0.1130 0
108 0.1118 0.1130 0
109 0.1118 0.1129 0
110 0.1118 0.1129 0
111 0.1117 0.1130 0
112 0.1118 0.1130 0
113 0.1118 0.1128 0
114 0.1118 0.1130 0
115 0.1118 0.1130 0
116 0.1118 0.1128 0
117 0.1117 0.1130 0
118 0.1117 0.1128 1
119 0.1117 0.1128 0
120 0.1117 0.1128 0
121 0.1117 0.1129 0
122 0.1117 0.1130 0
123 0.1118 0.1128 0
124 0.1117 0.1129 0
125 0.1117 0.1128 0
126 0.1117 0.1131 0
127 0.1117 0.1129 0
128 0.1118 0.1127 0
129 0.1118 0.1129 0
130 0.1118 0.1129 0
131 0.1117 0.1130 0
132 0.1118 0.1128 0
133 0.1117 0.1128 1
"""

def _parse_loss_history():
    rows = []
    for line in _LOSS_RAW.strip().splitlines():
        ep, tr, vl, best = line.split()
        rows.append({'epoch': int(ep), 'train': float(tr), 'val': float(vl), 'best': bool(int(best))})
    return pd.DataFrame(rows)


# ── Load ──────────────────────────────────────────────────────────────────────

def load_data():
    print('Loading risk_scores.csv...', flush=True)
    t0 = time.time()
    df = pd.read_csv(OUTPUTS / 'risk_scores.csv')
    print(f'  {len(df):,} rows  ({time.time()-t0:.1f}s)')
    return df


# ── Plot 1: Train / val loss curve ────────────────────────────────────────────

def plot_loss_curve():
    """
    Train and validation Poisson NLL loss across all 133 epochs.
    Val > train throughout = healthy generalisation gap, no overfitting.
    Stars mark epochs where a new best val loss was achieved.
    """
    history = _parse_loss_history()
    best    = history[history['best']]

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(history['epoch'], history['train'], color='#3498db',
            linewidth=2.0, label='Train loss', zorder=3)
    ax.plot(history['epoch'], history['val'],   color='#e74c3c',
            linewidth=2.0, label='Val loss',   zorder=3)

    # Shade the gap between train and val
    ax.fill_between(history['epoch'], history['train'], history['val'],
                    alpha=0.08, color='#e74c3c', label='Generalisation gap')

    # Mark best-val epochs with gold stars
    ax.scatter(best['epoch'], best['val'], marker='*', s=80,
               color='#f1c40f', zorder=5, label='New best val', linewidths=0)

    # Annotate final values
    last = history.iloc[-1]
    ax.annotate(f'train {last["train"]:.4f}',
                xy=(last['epoch'], last['train']),
                xytext=(-55, -14), textcoords='offset points',
                fontsize=9, color='#3498db',
                arrowprops=dict(arrowstyle='->', color='#3498db', lw=1.2))
    ax.annotate(f'val {last["val"]:.4f}',
                xy=(last['epoch'], last['val']),
                xytext=(-55, 10), textcoords='offset points',
                fontsize=9, color='#e74c3c',
                arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.2))

    ax.set_xlabel('Epoch', fontsize=13)
    ax.set_ylabel('Poisson NLL Loss', fontsize=13)
    ax.set_title('GAT Training Curve — Great Britain (133 epochs, early stopping)\n'
                 'Poisson NLL averaged across all 5 vehicle types',
                 fontsize=13, fontweight='bold', pad=14)
    ax.legend(fontsize=11, loc='upper right')
    ax.set_xlim(1, 133)

    fig.tight_layout()
    out = PLOTS / '0_loss_curve.png'
    fig.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  Saved → {out}')


# ── Plot 2: Risk distributions (KDE, log scale, all 5 types) ──────────────────

def plot_distributions(df):
    fig, ax = plt.subplots(figsize=(11, 6))

    for t in VEHICLE_TYPES:
        scores = df[(df['vehicle_type'] == t) & (df['risk_score'] > 0)]['risk_score'].values
        if len(scores) < 100:
            continue
        log_s = np.log10(scores)
        x     = np.linspace(log_s.min(), log_s.max(), 500)
        kde   = gaussian_kde(log_s, bw_method='silverman')
        y     = kde(x)
        ax.plot(x, y, color=COLOURS[t], linewidth=2.5, label=LABELS[t])
        ax.fill_between(x, y, alpha=0.10, color=COLOURS[t])

    ax.set_xlabel('Risk score — log₁₀(crashes per vehicle-km)', fontsize=13)
    ax.set_ylabel('Density', fontsize=13)
    ax.set_title('GAT Risk Score Distributions by Vehicle Type\n(non-zero segments only)',
                 fontsize=14, fontweight='bold', pad=14)
    ax.legend(fontsize=11, loc='upper left')

    ax.tick_params(axis='x', labelsize=10)

    fig.tight_layout()
    out = PLOTS / '1_risk_distributions.png'
    fig.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  Saved → {out}')


# ── Plot 3: Correlation matrix — all 5 types ──────────────────────────────────

def plot_correlation_matrix(df):
    """
    Pearson r between log10(risk_score) for every pair of vehicle types,
    computed on segments where both types have non-zero risk.
    Low r = types are risky in different places = divergence.
    """
    # Pivot to wide: one column per type (only non-zero risk rows)
    wide = (df[df['risk_score'] > 0]
            .pivot_table(index='segment_id', columns='vehicle_type',
                         values='risk_score', aggfunc='mean'))
    log_wide = np.log10(wide)

    # pandas .corr() computes pairwise Pearson r, skipping NaN pairs automatically.
    # np.corrcoef on 4.6M-row arrays would attempt a 4.6M×4.6M covariance matrix.
    types  = VEHICLE_TYPES
    n      = len(types)
    avail  = [t for t in types if t in log_wide.columns]
    corr_df = log_wide[avail].corr(method='pearson')

    rmat = np.full((n, n), np.nan)
    nmat = np.zeros((n, n), dtype=int)
    for i, ta in enumerate(types):
        for j, tb in enumerate(types):
            if ta in avail and tb in avail:
                rmat[i, j] = corr_df.loc[ta, tb]
                nmat[i, j] = log_wide[[ta, tb]].dropna().shape[0]

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(rmat, vmin=-0.2, vmax=1.0, cmap='RdYlGn', aspect='auto')
    plt.colorbar(im, ax=ax, label='Pearson r (log-risk)', shrink=0.85)

    labels = [LABELS[t] for t in types]
    ax.set_xticks(range(n)); ax.set_xticklabels(labels, fontsize=11)
    ax.set_yticks(range(n)); ax.set_yticklabels(labels, fontsize=11)

    # Annotate cells
    for i in range(n):
        for j in range(n):
            val  = rmat[i, j]
            nseg = nmat[i, j]
            if np.isnan(val):
                continue
            colour = 'white' if val < 0.3 else 'black'
            ax.text(j, i, f'{val:.2f}\n({nseg/1000:.0f}k)', ha='center', va='center',
                    fontsize=9, color=colour, fontweight='bold' if i == j else 'normal')

    ax.set_title('Risk Score Correlation Between Vehicle Types\n'
                 'Segment-level Pearson r (log₁₀ scale, non-zero pairs)',
                 fontsize=13, fontweight='bold', pad=14)

    fig.tight_layout()
    out = PLOTS / '2_correlation_matrix.png'
    fig.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  Saved → {out}')


# ── Plot 4: National map — all 5 types ────────────────────────────────────────

def plot_national_map(df):
    """
    Top 0.5% hotspots for each of the 5 vehicle types on a dark GB map.
    Each type gets its own colour. Drawn in order of decreasing size so
    smaller/rarer types (cycle, motorcycle) are always visible on top.
    """
    print('  Loading centroids...', flush=True)
    t0  = time.time()
    gdf = gpd.read_file(OUTPUTS / 'segments.gpkg')
    segs = pd.DataFrame(gdf[['segment_id', 'centroid_lon', 'centroid_lat']])
    del gdf
    print(f'  {len(segs):,} centroids  ({time.time()-t0:.1f}s)')

    N     = len(segs)
    n_top = max(1, int(0.005 * N))   # top 0.5% per type ≈ 19 800 dots each

    top = {}
    for t in VEHICLE_TYPES:
        top[t] = set(df[df['vehicle_type'] == t].nlargest(n_top, 'risk_score')['segment_id'])

    fig, ax = plt.subplots(figsize=(10, 15))
    fig.patch.set_facecolor('#12121f')
    ax.set_facecolor('#12121f')

    # Background road silhouette
    bg = segs.sample(min(500_000, N), random_state=42)
    ax.scatter(bg['centroid_lon'], bg['centroid_lat'],
               s=0.12, c='#2c2c4a', linewidths=0, rasterized=True, zorder=1)

    # Draw larger-count types first (so smaller/rarer types sit on top)
    draw_order = ['car', 'lgv', 'hgv', 'cycle', 'motorcycle']
    for t in draw_order:
        pts = segs[segs['segment_id'].isin(top[t])]
        ax.scatter(pts['centroid_lon'], pts['centroid_lat'],
                   s=1.8, c=COLOURS[t], alpha=0.85,
                   linewidths=0, rasterized=True, zorder=2,
                   label=f'{LABELS[t]}  ({len(pts):,})')

    leg = ax.legend(loc='lower left', fontsize=10, framealpha=0.85,
                    facecolor='#1a1a2e', markerscale=5)
    for text in leg.get_texts():
        text.set_color('white')

    ax.set_title('Top 0.5% Risk Hotspots by Vehicle Type\nGreat Britain',
                 fontsize=14, fontweight='bold', color='white', pad=14)
    ax.set_aspect('equal')
    ax.set_axis_off()

    fig.tight_layout()
    out = PLOTS / '3_national_hotspot_map_all_types.png'
    fig.savefig(out, dpi=180, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'  Saved → {out}')


# ── Plot 5: Zero-exposure rates by type ────────────────────────────────────────

def plot_zero_exposure(df):
    rates = {
        t: 100 * (df[df['vehicle_type'] == t]['exposure_vkm'] == 0).mean()
        for t in VEHICLE_TYPES
    }

    fig, ax = plt.subplots(figsize=(9, 5))
    xs   = [LABELS[t] for t in VEHICLE_TYPES]
    ys   = [rates[t] for t in VEHICLE_TYPES]
    cols = [COLOURS[t] for t in VEHICLE_TYPES]

    bars = ax.bar(xs, ys, color=cols, edgecolor='white', linewidth=1.2, width=0.55)
    for bar, y in zip(bars, ys):
        ax.text(bar.get_x() + bar.get_width() / 2, y + 0.8,
                f'{y:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylim(0, 105)
    ax.set_ylabel('Segments with zero AADF exposure (%)', fontsize=12)
    ax.set_title('Zero-Exposure Rate by Vehicle Type\n'
                 'Segments with no AADF traffic count → risk_score forced to 0',
                 fontsize=13, fontweight='bold', pad=14)
    ax.axhline(50, color='grey', linestyle='--', linewidth=0.8, alpha=0.6)

    fig.tight_layout()
    out = PLOTS / '4_zero_exposure_rates.png'
    fig.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  Saved → {out}')


# ── Plot 6: Risk statistics per type ──────────────────────────────────────────

def plot_risk_stats(df):
    stats = {}
    for t in VEHICLE_TYPES:
        s = df[(df['vehicle_type'] == t) & (df['risk_score'] > 0)]['risk_score']
        stats[t] = {'median': s.median(), 'mean': s.mean(), 'p95': s.quantile(0.95)}

    x   = np.arange(len(VEHICLE_TYPES))
    w   = 0.24
    fig, ax = plt.subplots(figsize=(11, 6))

    ax.bar(x - w, [stats[t]['median'] for t in VEHICLE_TYPES], w,
           color=[COLOURS[t] for t in VEHICLE_TYPES], alpha=0.65, label='Median')
    ax.bar(x,     [stats[t]['mean']   for t in VEHICLE_TYPES], w,
           color=[COLOURS[t] for t in VEHICLE_TYPES], alpha=0.95, label='Mean')
    ax.bar(x + w, [stats[t]['p95']    for t in VEHICLE_TYPES], w,
           color=[COLOURS[t] for t in VEHICLE_TYPES], alpha=0.45,
           hatch='///', edgecolor='white', label='95th percentile')

    ax.set_yscale('log')
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS[t] for t in VEHICLE_TYPES], fontsize=12)
    ax.set_ylabel('Risk score — crashes per vehicle-km (log scale)', fontsize=12)
    ax.set_title('Risk Score Statistics by Vehicle Type\n(non-zero segments only)',
                 fontsize=13, fontweight='bold', pad=14)
    ax.legend(fontsize=11)

    fig.tight_layout()
    out = PLOTS / '5_risk_stats_by_type.png'
    fig.savefig(out, dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  Saved → {out}')


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print('Plot 0 — loss curve (no data load needed)...')
    plot_loss_curve()

    df = load_data()

    print('\nPlot 1 — risk distributions...')
    plot_distributions(df)

    print('Plot 2 — correlation matrix (all 5 types)...')
    plot_correlation_matrix(df)

    print('Plot 3 — national hotspot map (all 5 types)...')
    plot_national_map(df)

    print('Plot 4 — zero-exposure rates...')
    plot_zero_exposure(df)

    print('Plot 5 — risk statistics by type...')
    plot_risk_stats(df)

    print(f'\nDone. All plots → {PLOTS}')


if __name__ == '__main__':
    main()
