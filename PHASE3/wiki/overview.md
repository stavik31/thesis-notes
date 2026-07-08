---
title: "Thesis Overview — Phase 3"
type: overview
last_updated: "2026-07-06"
tags: [phase3, thesis-core, overview]
---

# Thesis Overview

> This file is the advisor-facing status memo. Updated after major milestones. If only one thing
> gets read before a meeting, it should be this.

---

## Thesis Argument

**The central claim:** crash risk on a road network is not uniform across vehicle types — the
segments that are dangerous for motorcycles are not the same segments that are dangerous for HGVs.
Current safe-route systems ignore this: they compute a single aggregate risk score per segment and
route all vehicles identically. This thesis builds a route planning system that conditions the
risk layer on vehicle type, so that a motorcyclist and an HGV driver receive different recommended
routes for the same origin–destination pair, each calibrated to the historical crash risk their
vehicle class faces on each road segment.

**Why this is defensible:**

1. **The data exists.** STATS19 records vehicle type on every crash entry, at full national
   coverage for Great Britain.
2. **The spatial divergence is demonstrated.** Lee et al. 2018 (AAP, statewide Florida, 8 types)
   showed directly that *"the spatial pattern of hot zones is substantially different across vehicle
   types."* An informal STATS19 probe (2026-06-22) confirmed this at segment resolution on GB:
   motorcycle crashes 72% urban vs HGV 61% rural; per-cell count correlation 0.24 (vs ~0.41 at
   random) — types are spatially segregated. The divergence is real and worth routing on.
3. **The gap is confirmed.** No paper in the literature routes by a data-driven per-vehicle-type
   crash-risk surface. The gap exists across T-ITS, TR-C, AAP, and ESWA (all of Tier 1).
4. **The complexity is real.** A multi-stage pipeline (STATS19 → segmentation → GAT risk model →
   risk surface → routing → evaluation) satisfies the supervisor's standard: *"I don't always need
   novelty, but I always need complexity of the system."*

**What the thesis does NOT claim:** it does not invent a new method or algorithm. Every component
is borrowed (GAT architecture, MCDM ranking, CLQ spatial analysis, Sarraf metrics). The
contribution is the **direction** borrowed machinery is applied to, plus the complexity of
assembling a full pipeline that exploits it.

---

## State of the Project

**Phase:** Build (started 2026-06-24). Reading phase closed.

**Reading phase result:**
- ~14 deep reads + ~25–30 abstract keepers across T-ITS, TR-C, AAP, ESWA (all of Tier 1).
- Routing home is strong: Jiang 2022 (engine), Sarraf 2020 (router + eval template), Mansoor 2026
  (per-type routing mechanism), Sohrabi & Lord 2022 (operational motivating case).
- Niche premise is demonstrated (not assumed): Lee 2018 + STATS19 probe (see above).
- Build design locked: 6-stage pipeline with GAT + vehicle-type-conditioned attention as the AI core.

**6-stage build (current status — updated 2026-07-02):**

| Stage | What | Status |
|---|---|---|
| 1 | Data prep — clean STATS19, join tables, severity-weight, tag by vehicle type | **done** |
| 2 | Segmentation — OS Open Roads network; homogeneous segmentation; map-match crashes; attach AADF | **done** (3.96M national segments) |
| 3 | Risk model — **per-type discrete network clustering + share-target + 5 separate XGBoost models** | **✅ ENGINE DECIDED + VALIDATED LEAKAGE-FREE (2026-07-06).** Rebuilt as durable code (`code/tests/cluster_risk/`), reproduced 07-04 (national eval 158,237 = exact), then validated with 16-fold spatial CV + unseen-2024 temporal holdout: national OOS ρ=−0.097, **no leakage** (2024 validity ≈ target-year). GAT tested on same recipe → ties divergence, loses validity/simplicity → retired. **✅ IMPLEMENTED + LIVE (2026-07-08):** rewritten (8 sections), objective → `reg:logistic` (bounded [0,1] share; verified metric-identical to squared-error), run nationally → production `risk_scores.csv` (19.8M rows) + 5 training plots. Blueprint: [[wiki/build/stage-3-cluster-share-engine]]. See [[wiki/progress/2026-07-06]], [[wiki/progress/2026-07-08]], [[wiki/concepts/vehicle-type-risk-divergence]] |
| 4 | Risk surface filtering — threshold + CLQ post-hoc divergence maps | **done** on old GAT surface; **re-run on new XGBoost surface pending** (same consumer contract). CLQ stays post-hoc |
| 5 | Routing — Yen's k-shortest + MCDM per type; **+ per-route explainer** | **built; consumer unchanged.** Route on the full-history surface (holdout surface flattens divergence). Config: p99 cap + per-type norm + modest λ (λ is *not* a simple lever — see 07-06 pair-9 result). Per-route explanation added (`explain_route.py`) |
| 6 | Evaluation — spatial CV + temporal-2024 validity + cross-type divergence + Sarraf metrics | **method built (`run_cv.py`)** — port as Stage 6; adds the "predicted-risk vs real-future-crashes" validity axis |

Build files for each stage are in `wiki/build/`. Code lives in a separate repository.

**What's done:**
- STATS19 ingestion pipeline + tabular analysis (MI, Cramér's V, spatial hotspot analysis) from
  Phase 1 — survives the pivot as foundational infrastructure.
- All reading. Corpus is sufficient; further reads happen just-in-time during the build.
- Full system design: architecture decisions locked, build files written.

**What's next (immediate):** fold the validated engine into the main pipeline, guided by the
blueprint [[wiki/build/stage-3-cluster-share-engine]]:
1. **Rewrite `stage3_gat_risk_model/train.py`** — GAT → cluster + share + per-type XGBoost (port
   `common.py` + `run_xgb.py`; keep data-loading + `risk_scores.csv` output contract).
2. Point Stage 4 at the new surface (same columns); re-check thresholds; CLQ stays post-hoc.
3. Route on the **full-history** surface; bake p99 cap + per-type norm + chosen λ into `route.py`;
   add `explain_route.py` (per-route explanation) + `road_association.py` (descriptive layer).
4. Port `run_cv.py` as Stage 6 (spatial CV + temporal-2024 validity + divergence).
5. (Non-blocking) formalise/cite the network-clustering method; robustness sweep of
   `min_crashes`/target; personalized attribute-avoidance routing (deferred future add-on).

**Key result locked 2026-07-06:** the engine decision is **final and validated leakage-free.**
Per-type discrete network clustering + share target + 5 separate XGBoost models: national
out-of-sample cross-type ρ=−0.097 (16-fold spatial CV over all 3.96M segments), and validity on
the **never-seen 2024** year ≈ validity on the target years → **no leakage** (directly answers the
"too good?" worry). Honest read: ρ≈0 is the noise floor; validity (~0.05–0.18, positive everywhere)
is the real, modest, defensible measure. GAT tested on the same recipe → ties divergence, loses on
validity/simplicity → retired. Two explainability layers added (SHAP + descriptive road
associations) and a working per-route explainer. See [[wiki/progress/2026-07-06]] and
[[wiki/build/stage-3-cluster-share-engine]].

**Key results locked 2026-07-03:** the vehicle-type niche is *strongly empirically confirmed* on
STATS19 (per-type crash surfaces near-orthogonal, ρ≈-0.05, 4% hotspot overlap, survives
denoising) — stronger evidence than Lee 2018. But every model tested (GAT variants, XGBoost
variants, even proper Empirical Bayes shrinkage) underperforms a simple statistical smoothing
estimate at preserving that divergence. Best model (GAT: share-target + per-type heads,
**no new input data**) reaches ρ=0.377, real but partial. Mechanism fully diagnosed: any
signal shared equally across types collapses divergence, regardless of method. A second ML
angle (conditional risk by weather/light/time) was premise-tested and killed (Cramér's V
0.03–0.05, negligible). See [[wiki/concepts/vehicle-type-risk-divergence]] and
[[wiki/concepts/routing-risk-normalization]].

---

## Key Open Question

**DfT AADF per-type availability at segment level (check in Stage 2).**

Risk normalised by exposure (crashes / vehicles of that type × distance) is the correct measure.
Without per-type AADF, "motorcycle risk" is confounded with motorcycle *volume* — a road with many
motorcycle crashes might just have many motorcycles. If per-type AADF is unavailable at segment
granularity, the fallback is national vehicle-type share fractions as a proxy, documented as a
limitation. This is an engineering constraint, not a thesis threat.

All other previously-open decisions are resolved (see [[positioning-memo]] → Build architecture).

---

## Literature Landscape

The thesis sits at the intersection of two established fields:

**Risk-aware route planning (the home).** An active field since ~2008 with a clear evaluation
tradition (Sarraf 2020: Spearman/Average Overlap/DCG). The field has mature machinery: NB/EB crash
risk models on segments (Jiang 2022), Dijkstra-based multi-objective routing (Sarraf 2020), and
mean-excess CVaR formulations for the crash-severity tail (Mansoor 2026). The field consistently
shows that the safest route is not the shortest (Sohrabi & Lord 2022: 8% extra travel time → 23%
fewer expected crashes). **What it does not do:** condition the risk layer on vehicle type.

**Vehicle-type crash risk heterogeneity (the niche).** Well-established that types differ in crash
factors and severity (Barabino 2021, Pathivada 2025). The spatial form — that different segments
are risky for different types — was demonstrated for the first time in Lee et al. 2018 at TAZ
(macro) level. At segment resolution on STATS19 (Great Britain), the divergence is confirmed
informally but not yet formally published. **The segment resolution + Great Britain jurisdiction +
routing exploitation combination is the open space.**

**The gap the thesis fills:** no paper routes by a data-driven per-vehicle-type crash-risk surface.
Mansoor 2026 gets close (class-specific route choice sets conditioned on safety preference) but
uses no crash data and has no vehicle-type term — it even names heavy-vehicle risk in its motivation
and omits vehicle type from future work. The thesis connects the gap Mansoor names.

---

## Links

- [[positioning-memo]] — full thesis direction, open decisions, evidence map, build architecture
- [[wiki/build/system-overview]] — 6-stage pipeline, data sources, AI architecture
- [[wiki/queries/2026-06-18-where-we-stand-and-remaining-gaps]] — post-reading gap analysis
- [[../PHASE2/positioning-memo]] — the superseded CRM/LLM direction (audit trail of pivot)
