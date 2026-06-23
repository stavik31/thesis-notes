---
title: "Stage 6 — Evaluation"
type: build-stage
stage: 6
date: "2026-06-23"
tags: [phase3, build, evaluation]
---

# Stage 6 — Evaluation

## What this stage does

Validates two things independently: that the GAT risk model is accurate, and that the routing system actually produces safer type-specific routes than the naive alternatives. The headline result is the counterfactual — does type-aware routing measurably reduce exposure to type-specific crash segments?

## Input

- `risk_scores.csv` from Stage 3 — model predictions on all years including holdout
- Year 5 STATS19 crash records (holdout — never used in training)
- Routing outputs from Stage 5 for a test set of O-D pairs

---

## Part 1 — Risk model evaluation

**What you're checking**: did the GAT correctly identify which segments had elevated crashes in the holdout year (year 5)?

**Step 1 — Precision at top X%**
- Take the model's top X% highest-risk segments per vehicle type (same threshold used in Stage 4)
- Check: what percentage of those flagged segments actually had crashes of that type in year 5?
- This is precision@X% — borrowed from Gao 2024
- Run this per vehicle type independently (motorcycle precision, HGV precision, car precision)

**Step 2 — Temporal stability**
- Take high-risk segments flagged from years 1–4 predictions
- Compute overlap with year 5 actual high-crash segments
- High overlap = the model's risk surface is stable and predictive, not just fitting noise

**Step 3 — Baseline comparison**
- Compare GAT predictions against a naive baseline: raw severity-weighted crash count per segment (no model, no smoothing)
- The GAT should outperform raw counts on precision@X% — especially for sparse vehicle types like HGV where raw counts have almost no signal

---

## Part 2 — Routing evaluation

**What you're checking**: does type-aware routing produce meaningfully different and safer routes than alternatives?

**Step 4 — Set up test O-D pairs**
- Select a set of origin-destination pairs across the network (e.g. 50–100 pairs covering urban/rural/mixed)
- For each pair, generate three routes per vehicle type:
  1. **Type-aware route** — Stage 5 output (risk conditioned on vehicle type)
  2. **Aggregate route** — same router but using a non-type-specific risk surface (all vehicle types combined)
  3. **Shortest path** — Dijkstra on distance only, ignoring risk

**Step 5 — Sarraf metrics**
- For each pair, compare the three route rankings using:
  - **Spearman rank correlation** — do the type-aware and aggregate rankings agree? Low correlation = the type conditioning is changing the route meaningfully
  - **Average Overlap** — what fraction of road segments are shared between routes?
  - **DCG (Discounted Cumulative Gain)** — penalises a dangerous route ranked highly; checks whether type-aware routing correctly deprioritises high-risk segments for that type

**Step 6 — Counterfactual (headline result)**
- For each test O-D pair and vehicle type:
  - Count how many year-5 crashes of that type occurred on the type-aware route
  - Count how many year-5 crashes of that type occurred on the shortest-path route
  - Count how many year-5 crashes of that type occurred on the aggregate route
- Aggregate across all O-D pairs: does type-aware routing consistently pass through fewer type-specific historical crash segments?
- This is the direct test of the thesis claim

---

## Part 3 — Divergence test (niche headline)

**Step 7 — Route divergence by type**
- For each O-D pair: do the motorcycle route and the HGV route for the same pair differ meaningfully?
- Measure: Average Overlap between motorcycle route and HGV route across all test pairs
- Low overlap = the vehicle-type-conditioned risk surface is producing genuinely different routing decisions
- Cross-reference with the CLQ spatial divergence maps from Stage 4: do the route differences align with where the hotspot maps say they should diverge?

---

## Tuning feedback into earlier stages

Stage 6 is also where you tune Stage 4's threshold:
- If precision@X% is low: threshold is too permissive (lower it — top 10% instead of 15%)
- If route divergence is low: threshold is too aggressive (raise it — more segments in play)
- Iterate between Stage 4 and Stage 6 until the balance is right

---

## Key metrics summary

| Metric | What it measures | Borrowed from |
|---|---|---|
| Precision@top X% | Risk model accuracy per type | Gao 2024 |
| Temporal stability | Risk surface predictive stability | Gao 2024 |
| Spearman rank correlation | Route ranking agreement | Sarraf 2020 |
| Average Overlap | Route segment overlap | Sarraf 2020 |
| DCG | Penalty for high-risk routes ranked high | Sarraf 2020 |
| Counterfactual crash exposure | Does type-aware routing avoid type-specific crashes? | Original (thesis) |
| Route divergence by type | Do motorcycle and HGV routes differ? | Original (thesis) |

---

## Tools

- pandas, numpy (metric computation)
- NetworkX (route comparison)
- matplotlib / geopandas (visualisation of divergence maps)

## Links

- [[build/system-overview]] — full pipeline context
- [[build/stage-5-routing]] — previous stage
- [[positioning-memo]] — evaluation design matches the evidence map
