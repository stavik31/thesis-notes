---
title: "Stage 3 (REWRITE) — Cluster + Share + Per-Type XGBoost Engine"
type: build-stage
stage: 3
date: "2026-07-06"
supersedes: "[[wiki/build/stage-3-gat-risk-model]]"
tags: [phase3, build, risk-model, xgboost, decision, thesis-core, implementation-guide]
---

# Stage 3 (REWRITE) — Cluster + Share + Per-Type XGBoost Engine

> **This page is the implementation blueprint for rewriting the main Stage 3 code.** It replaces
> the GAT design in [[wiki/build/stage-3-gat-risk-model]] (kept for audit trail). The recipe below
> was rebuilt from scratch, validated leakage-free at national scale on 2026-07-06, and is the
> engine we ship. Every mechanism here has a working reference implementation in
> `code/tests/cluster_risk/` — the rewrite is a *port* of those tested scripts into the main
> pipeline, not new research. See [[wiki/progress/2026-07-06]] for how it was validated.

**Decision (final):** the Stage 3 engine is **per-type discrete network clustering + share-of-all-type-total target + 5 fully separate XGBoost models.** GAT is retired from the base pipeline (it ties on divergence but loses on validity, simplicity, and explainability — see comparison below).

---

## 0. Why the GAT is being replaced (one paragraph)

The unified GAT collapsed the per-type divergence (cross-type ρ 0.855 — it smoothed genuinely near-orthogonal per-type crash surfaces into a near-shared one). Root cause, confirmed across many settings: **any signal shared equally across types collapses divergence**, and **divergence lives in *location*, not in volume/features**. The fix satisfies both rules at once: pool by network location (preserves the divergence axis), predict each type's *share* not raw count (removes the "how busy overall" confound), and share nothing across types (5 independent models). Full mechanism: [[wiki/concepts/vehicle-type-risk-divergence]].

---

## 1. The recipe, implement-level

Reference implementation: **`code/tests/cluster_risk/common.py`** (all mechanics) + **`run_xgb.py`** (single train/predict) + **`run_cv.py`** (production cross-val + validity + SHAP). Port these; don't re-derive.

**Time windows** (`common.py`):
- `HISTORY_YEARS = [2020, 2021]` → builds clusters + input features
- `TARGET_YEARS  = [2022, 2023]` → training target + primary evaluation
- `HOLDOUT_YEAR  = 2024` → touched by nothing; temporal leakage check only

**Step 1 — per-type BFS network clusters** (`common.bfs_clusters`), 5 independent clusterings:
- Adjacency = the Stage-2 segment graph (`graph_edges.csv`, undirected), CSR form.
- For each type, take that type's HISTORY severity-weighted count per segment.
- Seed from the highest-count unassigned segment; BFS outward over adjacency, adding unassigned
  neighbours, accumulating that type's history count until it reaches `MIN_CRASHES` (=30) or the
  local frontier is exhausted; close the cluster; repeat until **every** segment is assigned.
- Result: a full partition. Dense areas → many small clusters; sparse areas → few coarse ones
  (adaptive granularity, driven by data sufficiency). Typical counts: car ~64k clusters, hgv ~18k.

**Step 2 — cluster aggregates** (`common.cluster_frame`), per type per cluster:
- from HISTORY: `c_hist_t` (this type), `c_hist_all` (all types), `c_share_t = c_hist_t/c_hist_all`,
  `c_size`, `c_rate_t = c_hist_t / summed own-AADF·length exposure`.
- from TARGET: `c_tgt_share_t = c_tgt_t / c_tgt_all` — **the training target**.

**Step 3 — features + target** (`common.build_type_features`, `cluster_target_share`), per type:
- Features (per segment): `log1p(own_AADF)`, `log1p(length_m)`, `log1p(all_motor_vehicles)`,
  `c_share_t`, `c_rate_t`, `c_size`, `c_hist_t`, `c_hist_all`, `road_class` one-hot.
- Target (per segment): its cluster's `c_tgt_share_t` (broadcast to member segments).

**Step 4 — 5 fully separate XGBoost models** (`run_xgb.py`):
- `XGBRegressor(n_estimators=350–400, max_depth=6, lr=0.05, subsample=0.8, colsample_bytree=0.8,
  min_child_weight=5, objective='reg:squarederror', tree_method='hist')`. GPU optional.
- **Nothing shared across types** — separate model, separate clustering, separate features.
- Train on all segments (or all *active* segments under a holdout); predict every segment.

**Output:** `risk_scores.csv` — `segment_id, vehicle_type, risk_score` — the *same format* Stage 5
already consumes. `risk_score` here = predicted per-type share (∈[0,1]); routing normalises per-type
per-bbox anyway, so absolute scale is irrelevant.

---

## 2. Leakage guards — DO NOT reintroduce these (they cost us hours in the ad-hoc phase)

1. **HISTORY ⟂ TARGET.** Features come from 2020–21, target from 2022–23. If the same years feed
   both, the model copies its input → fake accuracy. (Original GAT's history feature had this risk.)
2. **Clusters built on `hist_for_build`** (a copy where a held-out region's history is zeroed) —
   not on target-year crashes. Growing clusters on the same crashes you then score = circular.
3. **Spatial holdout construction:** zero the held-out city's history, exclude it from XGBoost
   *training rows*, but still let its segments be *assigned* to clusters and *predicted* from
   features. (Making them unassignable gives all-zero predictions — a bug we hit and fixed.)
4. **The temporal 2024 check is the ultimate guard:** 2024 is never in features or target. If
   validity vs 2024 ≈ validity vs 2022–23, there is no leakage (confirmed 2026-07-06).

---

## 3. Validated numbers (the evidence this works — cite these, don't re-argue)

Two-step leakage-free validation, 2026-07-06 (`run_cv.py`, 16-fold spatial CV over all 3.96M
segments + temporal 2024):

| metric | XGBoost cluster+share |
|---|---|
| Cross-type ρ (national OOS, 158,237 crash-bearing) | **−0.097** (vs collapsed GAT 0.855, best old-GAT 0.377) |
| Validity vs 2022–23 (car/mc/cycle/lgv/hgv) | 0.083 / 0.183 / 0.164 / 0.053 / 0.075 |
| **Validity vs 2024 (unseen year)** | 0.116 / 0.150 / 0.167 / 0.039 / 0.079 → **≈ target years = no leakage** |

Single-city holdouts (`run_xgb.py --holdout`): Manchester ρ=−0.039, London ρ=−0.096.

**On "validity ≈ 0.05–0.18 is not weak":** ρ near 0 is the *noise floor* (random surfaces give
ρ≈0.05), so it proves little on its own. Validity is the honest bar, and ~0.1 for predicting sparse
per-type crashes is normal for the field and comparable to the statistical baseline. It is positive
everywhere → the surface is real, not noise. The contribution is *explainable per-type divergence*,
not high accuracy.

**GAT vs XGBoost, same recipe** (`run_gat.py`): divergence tie (Manchester GAT −0.040 vs XGB −0.039;
London −0.087 vs −0.096); XGBoost wins validity (GAT went *negative* for car/cycle/lgv); XGBoost far
simpler/faster with off-the-shelf SHAP. GAT's *only* edge: held-out-city routing divergence 2.10 vs
XGB 1.30 (message passing propagates into a novel area) — relevant only if routing into
zero-history regions becomes a goal. → **XGBoost ships; GAT is a documented investigated alternative.**

---

## 4. Mapping: test scripts → main pipeline files (the actual rewrite)

| Main file | Current state | Change |
|---|---|---|
| `stage3_gat_risk_model/train.py` | Collapsed GAT (Poisson count, shared backbone, type embedding, NeighborLoader) | **Replace wholesale.** Port `common.py` (adjacency, `severity_matrix`, `bfs_clusters`, `cluster_frame`, `build_type_features`) + `run_xgb.py` per-type XGBoost loop. **Keep** the data-loading paths and the `risk_scores.csv` output contract. **Delete** the GAT model, embeddings, Poisson loss, neighbour sampling. |
| `stage4_risk_surface/filter_and_clq.py` | Threshold + CLQ on GAT output | Consume the new `risk_scores.csv` unchanged (same columns). CLQ stays post-hoc. Re-check thresholds on the new surface. |
| `stage5_routing/route.py` | Routing (Yen's + MCDM); consumes `risk_scores.csv` | **No change to the consumer.** But the *deployed surface must be the full-history one* (see §5). Fold in `explain_route.py` as a new output component. Routing config: p99 cap + per-type norm + modest λ (see [[wiki/concepts/routing-risk-normalization]]). |
| `stage6_evaluation/` | Empty | **`run_cv.py` IS Stage 6.** Port it: spatial CV → OOS surface, temporal 2024, cross-type ρ + Jaccard + per-type validity + SHAP. |

New components to add to the main repo (from the test folder):
- **`road_association.py`** → a descriptive analysis script (explainability layer, §6).
- **`explain_route.py`** → a Stage-5 per-route explainer (§6).

---

## 5. Production vs validation surface (critical, easy to get wrong)

- **Validation** (proving no leakage / generalisation): hold regions/years out — `run_cv.py`.
  The CV OOS surface (`cv_oos_risk.csv`) is deliberately pessimistic (every segment predicted
  with its own region's history withheld).
- **Deployment** (the surface routing actually uses): train on **all** history, predict **all**
  segments — the full-context surface (`run_xgb.py --predict-city ... ` with no `--holdout`, or a
  national no-holdout run). This is where the divergence is strongest, because the cluster/location
  context is intact. **Routing divergence needs this surface** — a fully held-out city flattens
  (mean distinct routes 1.3 vs 1.9 full-surface; see [[wiki/progress/2026-07-06]]).

Do not route on the holdout surface. Hold-out is for measuring honesty, not for serving.

---

## 6. Explainability — three layers (the deliverable, kept separate from routing quality)

1. **Model SHAP** (`run_cv.py`, built-in `pred_contribs`): per-type feature importance. Result:
   car→`c_size`/`c_hist_all` (area volume); motorcycle→`c_rate_t`/own-AADF; cycle→`c_rate_t` (0.38);
   hgv→`c_share_t` (0.37). Different types explained by different features.
2. **Descriptive road-attribute association** (`road_association.py`): per-type over-representation
   `P(attr|type)/P(attr|all)` + Cramér's V, over 9 road features. Result: HGV↔motorway 4.8×/trunk
   4.0×/dual-carriageway 2.3×; cycle↔20mph/roundabout 1.4×/local-access; motorcycle↔junctions/20mph.
   **Descriptive, model-free** → not undermined by geometry being a weak *predictor*. Caveat baked
   in: crash-distribution, not exposure-normalised risk.
3. **Per-route explanation** (`explain_route.py`): for a generated route — top risk-contributing
   segments + road composition + why-this-route-vs-fastest (e.g. a London cycle route: −65% risk for
   +0.2 min, naming the avoided A-road segments). Uses only segment-level OS attributes.

Why geometry is only descriptive, never a predictive feature: OS road-geometry features were tested
and are **flat predictors** (07-03) — a model built on them would explain noise. Descriptive
over-representation needs no model to predict well, so it's the honest tool. This *supports* the
thesis ("divergence lives in location, not road-label attributes").

---

## 7. Open items / decisions still to make

- **min_crashes=30 and `cluster_share` target** are the validated defaults; a small sweep could be
  a robustness appendix, not a blocker.
- **Formalise/cite the clustering method** — discrete network-constrained partition; likely relates
  to network-KDE / regionalisation literature; not yet grounded.
- **Routing final config** — bake p99 cap + per-type norm + chosen λ into `route.py` on the final
  surface, then re-measure divergence/detours (the car/λ study showed λ is *not* a simple lever —
  see [[wiki/progress/2026-07-06]], the pair-9 result).
- **Personalized attribute-avoidance routing** — deferred (future add-on, user's call 2026-07-06).

---

## Links
- [[wiki/concepts/vehicle-type-risk-divergence]] — why this recipe, the collapse mechanism
- [[wiki/concepts/routing-risk-normalization]] — Stage-5 edge-weight config
- [[wiki/progress/2026-07-06]] — the session that rebuilt + validated this; test-by-test numbers
- [[wiki/build/stage-3-gat-risk-model]] — the superseded GAT design (audit trail)
- [[wiki/build/system-overview]] · [[PHASE3/positioning-memo]]
