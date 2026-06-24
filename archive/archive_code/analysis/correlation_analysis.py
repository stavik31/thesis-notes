# Correlation Analysis — STATS19

import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency, spearmanr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import warnings
warnings.filterwarnings('ignore')
from pathlib import Path

DATA_DIR = Path('/home/vik-esoc/Desktop/thesis/data')
OUT_DIR  = Path('/home/vik-esoc/Desktop/thesis/analysis')
OUT_DIR.mkdir(exist_ok=True)

# ── Load ──────────────────────────────────────────────────────────────────────
print("Loading...")
collision = pd.read_csv('data/collision.csv', low_memory=False)
vehicle   = pd.read_csv('data/vehicle.csv',   low_memory=False)
casualty  = pd.read_csv('data/casualty.csv',  low_memory=False)
print(f"  collision {collision.shape}  vehicle {vehicle.shape}  casualty {casualty.shape}")

# ── Merge ─────────────────────────────────────────────────────────────────────
# collision_index is object in casualty/collision but int64 in vehicle — normalise
for tbl in [collision, vehicle, casualty]:
    tbl['collision_index'] = tbl['collision_index'].astype(str)

# Drop duplicate admin columns from vehicle and collision before joining
VEH_COLS = [c for c in vehicle.columns   if c not in ['collision_year', 'collision_ref_no']]
COL_COLS = [c for c in collision.columns if c not in ['collision_year', 'collision_ref_no']]

df = (casualty
      .merge(vehicle[VEH_COLS],  on=['collision_index', 'vehicle_reference'], how='left')
      .merge(collision[COL_COLS], on='collision_index',                        how='left')
      )
print(f"  merged flat table: {df.shape}")

# ── Target ────────────────────────────────────────────────────────────────────
# Original coding: 1=Fatal (worst), 2=Serious, 3=Slight (least severe) — flip
# so severity_score is intuitive: 3=Fatal, 2=Serious, 1=Slight
df['severity_score'] = 4 - df['casualty_severity']

# ── Drop leakage, ID, and deprecated columns ──────────────────────────────────
DROP = [
    # identifiers / admin
    'collision_index', 'collision_year', 'collision_ref_no',
    'vehicle_reference', 'casualty_reference',
    'local_authority_district', 'local_authority_ons_district',
    'local_authority_highway', 'local_authority_highway_current',
    'lsoa_of_accident_location', 'lsoa_of_driver', 'lsoa_of_casualty',
    'location_easting_osgr', 'location_northing_osgr',
    'date', 'time', 'generic_make_model',
    'first_road_number', 'second_road_number',
    'driver_distance_banding', 'casualty_distance_banding',
    # severity leakage — these encode the outcome directly
    'casualty_severity',
    'collision_severity', 'enhanced_severity_collision', 'collision_injury_based',
    'collision_adjusted_severity_serious', 'collision_adjusted_severity_slight',
    'enhanced_casualty_severity', 'casualty_injury_based',
    'casualty_adjusted_severity_serious', 'casualty_adjusted_severity_slight',
    'number_of_casualties',
    # historic / deprecated fields
    'junction_detail_historic', 'vehicle_manoeuvre_historic',
    'vehicle_location_restricted_lane_historic',
    'pedestrian_crossing_human_control_historic',
    'pedestrian_crossing_physical_facilities_historic',
    'journey_purpose_of_driver_historic', 'carriageway_hazards_historic',
]
df.drop(columns=[c for c in DROP if c in df.columns], inplace=True)

# ── Replace STATS19 junk/missing codes with NaN ───────────────────────────────
df.replace([-1, 99, 98], np.nan, inplace=True)

# ── Classify columns into categorical vs numeric ──────────────────────────────
# Numeric: columns where the integer value IS the quantity
NUMERIC = [c for c in [
    'speed_limit', 'number_of_vehicles', 'age_of_driver', 'age_of_vehicle',
    'engine_capacity_cc', 'age_of_casualty', 'driver_imd_decile',
    'casualty_imd_decile', 'latitude', 'longitude',
] if c in df.columns]

# Categorical: all remaining int/float columns (label-encoded, codes not quantities)
CATEGORICAL = [
    c for c in df.select_dtypes(include=['int64', 'float64']).columns
    if c not in NUMERIC and c != 'severity_score'
]

print(f"\n  {len(CATEGORICAL)} categorical columns, {len(NUMERIC)} numeric columns")

# ── Cramér's V (bias-corrected) ───────────────────────────────────────────────
def cramers_v(x, y):
    """Bias-corrected Cramér's V + chi-square p-value."""
    mask = x.notna() & y.notna()
    x, y = x[mask], y[mask]
    if len(x) < 30 or x.nunique() < 2:
        return np.nan, np.nan
    ct = pd.crosstab(x, y)
    chi2, p, _, _ = chi2_contingency(ct)
    n = ct.values.sum()
    phi2 = chi2 / n
    r, k = ct.shape
    phi2c = max(0, phi2 - ((k-1)*(r-1)) / (n-1))
    rc    = r - (r-1)**2 / (n-1)
    kc    = k - (k-1)**2 / (n-1)
    denom = min(rc-1, kc-1)
    return (np.sqrt(phi2c / denom) if denom > 0 else np.nan), p

# ── Run correlation tests ─────────────────────────────────────────────────────
print("\nRunning Cramér's V for categorical columns...")
rows = []
for col in CATEGORICAL:
    v, p = cramers_v(df[col], df['severity_score'])
    if not np.isnan(v):
        rows.append(dict(feature=col, type='categorical', test="Cramér's V",
                         effect_size=v, p_value=p))

print("Running Spearman for numeric columns...")
for col in NUMERIC:
    mask = df[col].notna() & df['severity_score'].notna()
    if mask.sum() < 30:
        continue
    rho, p = spearmanr(df.loc[mask, col], df.loc[mask, 'severity_score'])
    rows.append(dict(feature=col, type='numeric', test='Spearman ρ',
                     effect_size=abs(rho), rho=rho, p_value=p))

results = (pd.DataFrame(rows)
           .sort_values('effect_size', ascending=False)
           .reset_index(drop=True))
results['significant'] = results['p_value'] < 0.05

# ── Print + save ──────────────────────────────────────────────────────────────
print("\n=== TOP 20 FEATURES BY EFFECT SIZE ===")
print(results[['feature', 'type', 'effect_size', 'p_value', 'significant']].head(20).to_string(index=False))
results.to_csv(OUT_DIR / 'correlation_results.csv', index=False)
print(f"\nFull results → {OUT_DIR / 'correlation_results.csv'}")

# ── Multicollinearity among top 15 ───────────────────────────────────────────
print("\nChecking multicollinearity among top 15 features...")
top15    = results.head(15)['feature'].tolist()
top_cat  = [f for f in top15 if f in CATEGORICAL]
top_num  = [f for f in top15 if f in NUMERIC]

if len(top_cat) > 1:
    vcorr = pd.DataFrame(np.nan, index=top_cat, columns=top_cat)
    for a in top_cat:
        for b in top_cat:
            vcorr.loc[a, b] = 1.0 if a == b else cramers_v(df[a], df[b])[0]
    vcorr.to_csv(OUT_DIR / 'multicol_categorical.csv')
    print("\nHigh multicollinearity pairs among categorical features (V > 0.7):")
    flagged = False
    for i, a in enumerate(top_cat):
        for b in top_cat[i+1:]:
            if vcorr.loc[a, b] > 0.7:
                print(f"  {a} ↔ {b}  V={vcorr.loc[a,b]:.3f}")
                flagged = True
    if not flagged:
        print("  None found.")

if len(top_num) > 1:
    df[top_num].dropna().corr(method='spearman').to_csv(OUT_DIR / 'multicol_numeric.csv')

# ── Plots ─────────────────────────────────────────────────────────────────────
print("\nGenerating plots...")
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

top20  = results.head(20)
colors = ['#2196F3' if t == 'numeric' else '#FF5722' for t in top20['type']]
axes[0].barh(top20['feature'][::-1], top20['effect_size'][::-1], color=colors[::-1])
axes[0].axvline(0.1, color='gray', ls='--', alpha=0.6)
axes[0].axvline(0.3, color='gray', ls='-',  alpha=0.6)
axes[0].set_xlabel("Effect size  (Cramér's V  or  |Spearman ρ|)")
axes[0].set_title('Top 20 Features vs Casualty Severity')
axes[0].legend(handles=[
    Patch(facecolor='#FF5722', label="Categorical — Cramér's V"),
    Patch(facecolor='#2196F3', label='Numeric — Spearman ρ'),
])

sev = (df['severity_score']
       .map({3: 'Fatal', 2: 'Serious', 1: 'Slight'})
       .value_counts()
       .reindex(['Fatal', 'Serious', 'Slight']))
axes[1].bar(sev.index, sev.values, color=['#c62828', '#ef6c00', '#2e7d32'])
axes[1].set_title('Casualty Severity Distribution')
axes[1].set_ylabel('Count')
for i, (cat, val) in enumerate(sev.items()):
    axes[1].text(i, val + 500, f'{val:,}\n({val/len(df)*100:.1f}%)', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig(OUT_DIR / 'correlation_analysis.png', dpi=150, bbox_inches='tight')
plt.close()

print(f"\nDone. All outputs in {OUT_DIR}/")
