from pathlib import Path
import json
import pandas as pd
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

DATA = Path("../data")
OUT = Path(".")

with open("test.jsonl") as f:
    test_records = [json.loads(line) for line in f]

test_ids = set(r["collision_index"] for r in test_records)
test_labels = {r["collision_index"]: r["label"] for r in test_records}

df = pd.read_csv("../clean_data/collision_clean.csv", low_memory=False)

DROP = ["collision_index", "collision_severity", "number_of_casualties",
        "date", "time", "first_road_number", "longitude", "latitude"]
df.drop(columns=[c for c in DROP if c in df.columns], inplace=True)

LABELS = ["Slight", "Serious", "Fatal"]
label_map = {"Slight": 0, "Serious": 1, "Fatal": 2}

df_full = pd.read_csv("../clean_data/collision_clean.csv", low_memory=False)
df_full = df_full[df_full["collision_severity"].isin(LABELS)].copy()

X = df_full.drop(columns=[c for c in DROP if c in df_full.columns])
y = df_full["collision_severity"].map(label_map)
idx = df_full["collision_index"]

for col in X.select_dtypes(include="object").columns:
    X[col] = X[col].astype("category")

test_mask = idx.isin(test_ids)
X_train, y_train = X[~test_mask], y[~test_mask]
X_test, y_test_encoded = X[test_mask], y[test_mask]
test_idx = idx[test_mask]

counts = y_train.value_counts().sort_index()
sw = y_train.map((len(y_train) / (3 * counts)).to_dict())

model = xgb.XGBClassifier(
    objective="multi:softmax", num_class=3,
    n_estimators=300, max_depth=6, learning_rate=0.1,
    enable_categorical=True, tree_method="hist",
    random_state=42, n_jobs=-1, eval_metric="mlogloss"
)
model.fit(X_train, y_train, sample_weight=sw,
          eval_set=[(X_test, y_test_encoded)], verbose=50)

y_pred_encoded = model.predict(X_test)
inv_label_map = {v: k for k, v in label_map.items()}
y_pred = [inv_label_map[p] for p in y_pred_encoded]
y_true = [inv_label_map[t] for t in y_test_encoded]

macro_f1 = f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)
per_class = f1_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)

print(f"\nMacro F1: {macro_f1:.4f}")
for label, f1 in zip(LABELS, per_class):
    print(f"  {label}: {f1:.4f}")

cm = confusion_matrix(y_true, y_pred, labels=LABELS)
fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay(cm, display_labels=LABELS).plot(ax=ax, colorbar=False)
ax.set_title("XGBoost Confusion Matrix")
plt.tight_layout()
plt.savefig(OUT / "xgb_confusion_matrix.png", dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(LABELS, per_class, color=["steelblue", "orange", "red"])
ax.axhline(macro_f1, linestyle="--", color="black", label=f"Macro F1 = {macro_f1:.3f}")
ax.set_ylabel("F1 Score")
ax.legend()
ax.set_title("XGBoost Per-Class F1 on Test Set")
plt.tight_layout()
plt.savefig(OUT / "xgb_f1.png", dpi=150)
plt.close()

print(f"\nSaved xgb_confusion_matrix.png and xgb_f1.png")
