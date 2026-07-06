---
title: "Phase 3 Positioning Memo — Risk-Aware Routing with a Vehicle-Type Niche (LIVING)"
type: memo
date: "2026-06-17"
last_updated: "2026-07-04"
status: BUILD PHASE — reading closed 2026-06-22; build design locked 2026-06-23; building from 2026-06-24; Stage 3 engine under revision 2026-07-03, redirected to per-type clustering 2026-07-04, ENGINE FINALIZED + VALIDATED LEAKAGE-FREE 2026-07-06 (cluster+share+XGBoost)
tags: [phase3, positioning, thesis-core, route-planning, decision]
---

# Phase 3 Positioning Memo (LIVING)

> **What this is.** The authoritative statement of the thesis direction. Updated as the project
> evolves — reading phase → build design → build → evaluation. Always answers four questions:
> **what field, what niche, what system, what evidence.**
>
> **Status (2026-06-24):** Reading phase CLOSED. 6-stage build design LOCKED. Building from
> today. The niche premise is no longer assumed — it is demonstrated on STATS19 data.

---

## The direction in one paragraph (current)

This thesis contributes to **risk-aware route planning** — the field that ranks routes not only
by time and distance but by crash risk (Jiang 2022; Sarraf 2020). Existing safe-route systems
compute a single aggregate crash-risk score per road segment and route everyone by it. **They
treat all vehicles the same.** But crash risk is not uniform across vehicle types: a motorcycle,
an HGV, and a car face materially different risk on the same wet bend or busy junction, and those
differences are spatial — the segments that are dangerous for motorcycles are not the same
segments that are dangerous for HGVs (Lee et al. 2018; confirmed on STATS19, 2026-06-22). This
thesis builds a routing system whose risk layer is **conditioned on vehicle type**, so that the
recommended route differs by what you are driving. STATS19 supplies the crash data (vehicle type
is on every record); the method is jurisdiction-agnostic. **No natural-language layer** — the
deliverable is the route and its risk breakdown, not a generated explanation (LLM direction cut as
un-solidified and distracting, supervisor 2026-06-17).

---

## Scope & depth — distinctive direction vs. system complexity

**Terminology, pinned.** "Novelty" has two senses and the supervisor split them: (a) **breakthrough
novelty** = inventing a new method — **NOT required** ("I don't always need novelty"); (b) **the
data niche** = applying existing/borrowed methods to a new data direction (vehicle type) — **explicitly
asked for.** This thesis is firmly (b): **nothing is invented — everything is borrowed** (GAT
architecture, MCDM ranking, CLQ spatial test, MPIW/PICP/AccHR@20 metrics). The contribution is the
**direction** that borrowed machinery is pointed at, plus the **complexity** of the pipeline.

The thesis is **two layers of one pipeline, not a choice between them:**

```
STATS19 → [ RISK LAYER: per-vehicle-type crash-risk surface ]  = DISTINCTIVE DIRECTION (the data niche)
        → [ ROUTING LAYER: risk + time + distance → routes   ]  = SYSTEM COMPLEXITY (the home)
        → [ EVALUATION: type-aware vs aggregate routing       ]  = the PAYOFF check
```

- **Risk layer (per-vehicle-type)** — depth buys the distinctive direction. Every step deeper
  (per-type significance gating, sparsity/zero-inflation handling, spatial divergence of hotspots
  by type) directly strengthens the contribution. **This is the spine.**
- **Routing layer** — depth buys complexity only. Go deep enough to build a credible
  multi-objective router and **borrow** the machinery (Mansoor 2026 mean-excess/VI; Sarraf 2020
  MCDM; Yen's k-shortest). Do not try to invent new routing optimisation.

**The premise concern is JUSTIFICATION, not novelty.** The vehicle-type direction must pay off: if
motorcycle hotspots and HGV hotspots are the same places, type-aware routing produces the same
routes as aggregate routing → null result. This has now been confirmed **twice**: the informal
STATS19 probe (2026-06-22, motorcycle 72% urban vs HGV 61% rural) and — much more strongly — the
2026-07-02 model-grade probe: severity-weighted per-type crash surfaces are **near-orthogonal
(cross-type Spearman ρ ≈ −0.047; top-1000 hotspot overlap 4%)** and the divergence **survives
denoising** (pooling 5 years barely moves it). The divergence is real at segment resolution.
The open risks are now (a) **HGV sparsity** (~80–91% zero-HGV cells) and (b) **the current GAT
collapses this real divergence** into ρ=0.855 — a Stage-3 modelling problem, being fixed by
decoupling types. See [[wiki/concepts/vehicle-type-risk-divergence]].

---

## The four questions

### 1. What field? — Risk-aware / safety-aware route planning

The home is routing, not crash-risk modeling as an end. CRM (Gao 2024 etc.) is the *engine*
that produces per-segment risk; the router consumes it.

| Paper | Role |
|---|---|
| Jiang 2022 (T-ITS) | Home paper — SPF/EB/HSM → per-segment risk heat maps; **names the gap in print** ("risks not dependent on vehicle types") |
| Sarraf 2020 (ESWA) | The actual router — Dijkstra + MCDM + eval template (Spearman/AO/DCG); vehicle-blind |
| Sohrabi & Lord 2022 (TR-C) | Operational home — 29k Texas segments; NB weather-stratified; **8% time → +23% crash**; survival-prob route aggregation |
| Mansoor, Li, Chen 2026 (TR-C) | ★★★ Structural ancestor — class-specific route choice sets + mean-excess (CVaR) crash-severity tail; re-key on vehicle type = the per-type routing mechanism |
| Kavta et al. 2025 (TR-C) | Demand-side niche brick — a vehicle class (delivery riders) will trade time for safety |
| Chandra 2014 (TR-C) | Closest user-conditioned routing precedent; parametric/crash-data-free; donates Pareto/Yen multi-objective machinery |
| de Souza 2020 (T-ITS) | Personalisation precedent (crime risk, not crash); abstract only |

**Gap across the whole corpus:** no paper routes by a data-driven per-vehicle-type crash-risk
surface. Mansoor hands the mechanism; nobody has executed it on crash data.

### 2. What niche? — Vehicle-type-conditioned segment crash risk

The novelty the supervisor asked for: a dimension in STATS19 nobody has used for routing.

**Niche premise — DEMONSTRATED (as of 2026-06-22), not assumed:**

- **Lee et al. 2018 (AAP)** — statewide Florida, 8 vehicle types, TAZ level: *"the spatial pattern
  of hot zones is substantially different across vehicle types"* (HGV→rural, bicycle→metro,
  pedestrian→urban, motorcycle→rural). First real-data evidence that vehicle-type hot zones diverge
  *as places*. [[tier1_journal3/AAP-deepread]]
- **STATS19 informal probe (2026-06-22)** — segment level on Great Britain: motorcycle crashes
  72% urban vs HGV 61% rural; per-cell count correlation moto~HGV = 0.24 (vs ~0.41 random) →
  types are actively spatially segregated. **Divergence survives at segment resolution.**
- **HGV sparsity (~80–91% cells zero-HGV)** = the main engineering risk, not an existential
  threat. EB shrinkage toward a coarse unit, CMP/HTCMP family for under-dispersed slices, and the
  graceful fallback in Stage 4 are the response.

**Unoccupied for routing:** no paper in the corpus routes by vehicle type. Sarraf's router even
normalises by AADT but has **no vehicle-type term** — confirmed in deep read.

**Combinable:** vehicle type as the primary axis; weather/time as secondary axes only where a
per-cell crash count is significant (graceful fallback when it isn't = a complexity feature, not a bug).

### 3. What system? — The 6-stage pipeline

The full build design is in `wiki/build/`. Summary:

| Stage | What |
|---|---|
| 1 | Data prep — clean STATS19, join tables, severity-weight (fatal=3/serious=2/slight=1), tag by vehicle type |
| 2 | Segmentation — OS Open Roads network; homogeneous segmentation (cut where road class/lanes/speed/AADF changes); map-match crashes; attach AADF |
| 3 | **Risk model** — per-type discrete network clustering + share-of-all-type-total target + 5 fully separate XGBoost models (GAT retired; validated leakage-free 2026-07-06 — [[wiki/build/stage-3-cluster-share-engine]]) |
| 4 | Risk surface filtering — threshold on GAT output; CLQ post-hoc for spatial divergence maps (not a production gate) |
| 5 | Routing — Yen's k-shortest paths + MCDM ranking (AHP/PROMETHEE) per vehicle type; vehicle-type-conditioned edge weights |
| 6 | Evaluation — precision@X% (Gao) + Sarraf metrics + counterfactual |

**Offline/online split:** Stages 1–4 run once, offline. Stage 5 answers queries live over precomputed risk scores.

### 4. What evidence / evaluation?

- **Risk-model validity:** temporal holdout — profiles on years 1–4, test year 5. Precision@top X%
  high-risk segments per vehicle type; GAT vs naive (raw severity-weighted count) baseline comparison.
  Metrics borrowed from Gao 2024 (MPIW/PICP/AccHR@20).
- **Routing quality:** Spearman rank correlation, Average Overlap, DCG on a test set of O-D pairs.
  Compare type-aware vs aggregate-risk vs shortest-path routes. Metrics borrowed from Sarraf 2020.
- **Headline result — counterfactual:** for each test O-D pair and vehicle type, count year-5
  crashes of that type on the type-aware route vs shortest-path route vs aggregate-risk route. Does
  type-aware routing consistently pass through fewer historical type-specific crash segments?
- **Divergence test (niche headline):** for each O-D pair, does the motorcycle route and the HGV
  route differ? Average Overlap between type routes across all test pairs. Cross-reference with
  CLQ spatial divergence maps.

---

## Build architecture — locked decisions

These were open during the reading phase and are now resolved.

| Decision | Choice | Rationale |
|---|---|---|
| Separate models per type vs unified | ✅ **FINALIZED 2026-07-06: per-type discrete network clustering + share-of-all-type-total target + 5 fully separate XGBoost models. GAT retired.** | The unified GAT with type embeddings caused **type-collapse** (ρ 0.855). Long investigation (07-03/07-04): any signal shared across types collapses divergence, and divergence lives in *location* not volume, so feature-based clustering also fails; the fix pools by network location + predicts each type's *share* + shares nothing across types. **2026-07-06: the ad-hoc 07-04 result (whose code was lost) was rebuilt as durable scripts, reproduced (national eval 158,237 = exact), then validated leakage-free** — 16-fold spatial CV + unseen-2024 temporal holdout give national OOS ρ=−0.097 with **no leakage** (2024 validity ≈ target-year). GAT tested on the *same* recipe: ties divergence, **loses on validity** (negative for some types), simplicity, and explainability → retired to a documented alternative (its only edge = routing into zero-history regions). Honest framing: ρ≈0 is the noise floor; validity (~0.05–0.18, positive everywhere, ≈ statistical baseline) is the real, modest, sufficient measure. **Implementation blueprint: [[wiki/build/stage-3-cluster-share-engine]].** Full detail: [[wiki/progress/2026-07-06]], [[wiki/concepts/vehicle-type-risk-divergence]]. |
| Significance gate (production) | **ML threshold on GAT output** | GAT already does spatial smoothing through message passing; a separate statistical test is redundant overhead |
| CLQ role | **Post-hoc analysis only** | Generates spatial divergence maps for the results section; confirms where hotspots diverge by type |
| Per-type loss function | **Per-type dispersion check in Stage 3** — do not assume | Per-type slices can flip the count regime: motorcycle = under-dispersed (CMP/HTCMP; Pathivada 2025); aggregate = over-dispersed (NB/ZITD; Gao 2024) |
| Segment definition | **Homogeneous segmentation** (Pathivada lineage) — v1 = grid, v2 = homogeneous | Real road geometry; HSM-standard; pooled so less sparse; build v1 grid first |
| Routing mechanism | **Yen's k-shortest + MCDM (AHP/PROMETHEE)** | Sarraf operational template; Mansoor class-specific route sets as reference |
| Tail risk (CVaR/mean-excess) | **Decide in Stage 5 with real risk surface** | May add it if risk surface has a meaningful tail; don't design around it blind |
| LLM explanation layer | **Cut** | Faithfulness unsolvable in time; language distracting to drivers; not solidified enough (supervisor 2026-06-17) |
| Reinforcement learning | **Not used** | Poor fit for offline precomputed graph routing; Dijkstra/Yen's is the correct tool |
| Output form | **Both** — ranked routes + vehicle-type-specific risk-scored map | |

**One remaining open question:** DfT AADF per-type availability at segment level. First check in
Stage 2. If unavailable: use national vehicle-type share fractions as a proxy and document the
approximation.

---

## What changed from Phase 2 (audit trail)

| | Phase 2 (CRM + LLM) | Phase 3 (routing + niche) |
|---|---|---|
| Home field | Crash Risk Modeling (Chai 2024) | Risk-aware route planning (Jiang 2022) |
| Deliverable | NL explanation of risk to a driver | A route (+ risk breakdown), no language |
| Novelty pin | NL-output × condition-conditioned × significance-gated | **Vehicle-type-conditioned crash-risk routing** |
| LLM / LoRA | core | **cut** (faithfulness unsolvable in time; NL distracting + per-person) |
| Keystone baseline | Gao 2024 (risk model) | Jiang 2022 / Sarraf 2020 (routing); Gao = the engine |
| Eval headline | significance-gated faithful explanation | route divergence / per-type counterfactual |

CRM, Gao, and the condition-conditioning evidence **survive** as the engine. The
explanation/faithfulness/LLM half is **future-work**, not core.

---

## Evidence map (complete — reading phase closed 2026-06-22)

### Routing home

| Paper | Role | Status |
|---|---|---|
| Jiang 2022 (T-ITS) | Home = risk engine (NB/EB heat map, not a router; names the gap in print) | deep-read — [[T-ITS-deepread]] |
| Sarraf & McGuire 2020 (ESWA) | The actual router (Dijkstra + MCDM) + eval template; vehicle-blind | deep-read — [[ESWA-deepread]] |
| Mansoor, Li, Chen 2026 (TR-C) | ★★★ Structural ancestor — class-specific route sets + mean-excess CVaR tail | deep-read — [[tier1_journal2/TR-C-deepread]] |
| Sohrabi & Lord 2022 (TR-C) | Operational home — NB weather-stratified; 8%/+23%; survival-prob aggregation | deep-read — [[tier1_journal2/TR-C-deepread]] |
| Kavta et al. 2025 (TR-C) | Demand-side niche brick — riders trade time for safety | deep-read — [[tier1_journal2/TR-C-deepread]] |
| Chandra 2014 (TR-C) | User-conditioned routing precedent; crash-data-free; donates Pareto/Yen machinery | deep-read — [[tier1_journal2/TR-C-deepread]] |
| de Souza 2020 (T-ITS) | Personalisation precedent (crime risk) | abstract only |

### Vehicle-type niche evidence

| Paper | Role | Status |
|---|---|---|
| Lee, Yasmin, Eluru, Abdel-Aty & Cai 2018 (AAP) | ★★★ **THE SPATIAL-DIVERGENCE BRICK** — hot zones "substantially different across vehicle types" (FL, 8 types); donates EPP per-type gate | deep-read — [[tier1_journal3/AAP-deepread]] |
| Barabino et al. 2021 (AAP) | ★★ Structural precedent — R=H·V·E per-bus-route risk → section-sum → quartile ranking; closest per-type→route-risk→ranked-output pipeline | deep-read — [[tier1_journal3/AAP-deepread]] |
| Pathivada et al. 2025 (AAP) | Motorcycle segment SPF — per-type slice flips to under-dispersion → CMP/HTCMP; donates EB ranking + homogeneous segmentation | deep-read — [[tier1_journal3/AAP-deepread]] |
| Hu, Zhang, Shelton 2018 (TR-C) | **Method donor** — Colocation Quotient (GCLQ+LCLQ) = per-type spatial significance test; Monte-Carlo p-values; network-distance; MAUP-aware | deep-read — [[tier1_journal2/TR-C-deepread]] |
| Zhu et al. 2025 (T-ITS) | Vehicle-**group** (not type); method-cousin + Abdel-Aty anchor; **weak premise** | deep-read — [[T-ITS-deepread]] |
| STATS19 informal probe 2026-06-22 | Segment-level confirmation: moto 72% urban / HGV 61% rural; moto~HGV correlation 0.24 (random ~0.41); HGV ~80–91% zero-cell | deliberate non-artifact |

### Risk engine + significance gate (inherited from Phase 2 reading, solid)

| Paper | Role | Status |
|---|---|---|
| Gao 2024 (AAP) | STATS19 segment-risk engine; ZITD for ~96% zero-inflation; MPIW/PICP/AccHR@20 | deep-read — [[AAP-deepread]] |
| Wei 2024 (AAP) | Gate ancestor — case-crossover matched-control (quasi-Poisson DLM/DLNM) | deep-read — [[AAP-deepread]] |
| Wang 2025 (AAP) | Gate ancestor — χ²-CI Bayesian network (Bonferroni; BDs for sparse cells) | deep-read — [[AAP-deepread]] |

---

## Links

- `PLAN.md` — the Phase 3 reading plan (journals, keywords, tiers) — reading complete
- `wiki/build/system-overview.md` — full 6-stage pipeline with data sources + AI architecture
- `wiki/build/stage-3-gat-risk-model.md` — the AI core
- `wiki/build/stage-6-evaluation.md` — full evaluation design
- `../PHASE2/positioning-memo.md` — the superseded CRM/LLM memo (audit trail of the 2026-06-17 pivot)
