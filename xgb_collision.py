#!/home/vik-esoc/Desktop/thesis/.venv/bin/python
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xgboost as xgb
import shap
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

DATA = Path('/home/vik-esoc/Desktop/thesis/data')
OUT  = Path('/home/vik-esoc/Desktop/thesis/analysis')

# Load & decode guide
guide = pd.read_excel(DATA / 'dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2024.xlsx', sheet_name='2024_code_list')
lookup = {}
for _, r in guide[(guide['table'] == 'collision') & guide['code/format'].notna() & guide['label'].notna()].iterrows():
    try: lookup.setdefault(r['field name'], {})[int(float(r['code/format']))] = str(r['label']).strip()
    except: pass

# Load collision table
df = pd.read_csv(DATA / 'dft-road-casualty-statistics-collision-last-5-years.csv', low_memory=False)
df = df[df['collision_severity'].isin([1, 2, 3])].copy()
df['target'] = 3 - df['collision_severity']  # 0=Slight 1=Serious 2=Fatal

# Drop leakage, IDs, admin, deprecated
DROP = ['collision_index','collision_year','collision_ref_no','location_easting_osgr',
        'location_northing_osgr','first_road_number','second_road_number','date','time',
        'local_authority_district','local_authority_ons_district','local_authority_highway',
        'local_authority_highway_current','lsoa_of_accident_location','collision_severity',
        'enhanced_severity_collision','collision_injury_based','collision_adjusted_severity_serious',
        'collision_adjusted_severity_slight','number_of_casualties',
        'did_police_officer_attend_scene_of_accident','junction_detail_historic',
        'pedestrian_crossing_human_control_historic','pedestrian_crossing_physical_facilities_historic',
        'carriageway_hazards_historic']
df.drop(columns=[c for c in DROP if c in df.columns], inplace=True)
df.replace([-1, 99, 98], np.nan, inplace=True)

# Decode categoricals using guide labels
NUMERIC = {'speed_limit', 'number_of_vehicles', 'latitude', 'longitude'}
X = df.drop(columns=['target'])
for c in X.columns:
    if c not in NUMERIC and c in lookup:
        X[c] = X[c].map(lookup[c]).astype('category')

y = df['target'].astype(int)

# Train XGBoost
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
counts = y_train.value_counts().sort_index()
sw = y_train.map((len(y_train) / (3 * counts)).to_dict())

model = xgb.XGBClassifier(objective='multi:softmax', num_class=3, n_estimators=300,
                           max_depth=6, learning_rate=0.1, enable_categorical=True,
                           tree_method='hist', random_state=42, n_jobs=-1, eval_metric='mlogloss')
model.fit(X_train, y_train, sample_weight=sw, eval_set=[(X_test, y_test)], verbose=50)

print(classification_report(y_test, model.predict(X_test), target_names=['Slight','Serious','Fatal']))

# SHAP importance
X_sample = X_test.sample(3000, random_state=42)
explanation = shap.TreeExplainer(model)(X_sample)   # shape: (n_samples, n_features, n_classes)
mean_shap = np.abs(explanation.values).mean(axis=(0, 2))
imp = pd.DataFrame({'feature': X_sample.columns, 'shap': mean_shap}).sort_values('shap', ascending=False)
imp.to_csv(OUT / 'xgb_shap_importance.csv', index=False)
print(imp.head(15).to_string(index=False))

# Plot
imp.head(20).plot.barh(x='feature', y='shap', figsize=(10,7), legend=False)
plt.xlabel('Mean |SHAP|'); plt.title('XGBoost Feature Importance — Collision Table')
plt.gca().invert_yaxis(); plt.tight_layout()
plt.savefig(OUT / 'xgb_shap_bar.png', dpi=150); plt.close()
print(f"Done → {OUT}/")
