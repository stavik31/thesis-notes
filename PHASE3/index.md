# Phase 3 — Wiki Index

Content catalog for the **active** phase of the thesis (risk-aware route planning +
vehicle-type data niche). Phase 1 (`../PHASE1/`) and Phase 2 (`../PHASE2/`) are prior
phases — read-only context.

Updated after every reading record, progress note, query filed, or lint pass.

---

## Plan & Direction

| Page | Description |
|------|-------------|
| [[PHASE3/PLAN]] | The Phase 3 plan: why we pivoted (drop LLM, route planning home, data niche), journals, keywords, tiers, reading goals |
| [[PHASE3/positioning-memo]] | **★ LIVING DELIVERABLE.** Current direction — field (risk-aware routing), niche (vehicle-type), system, evidence map. Updated as reading proceeds |

## Overview

| Page | Description |
|------|-------------|
| [[wiki/overview]] | Thesis argument + project state + literature landscape — written 2026-06-24; update after each stage |

---

## Sources (Papers & Articles)

Lightweight per-journal reading records live in `raw/papers/` (NOT full wiki INGEST),
mirroring the Phase 2 working style.

| Record | Journal | Status |
|--------|---------|--------|
| `raw/papers/carry_over.md` | (multi) | Papers from Phase 2 that survive the pivot — routing home, vehicle-type niche, risk engine + borrow shelf |
| `raw/papers/carry_over/T-ITS-deepread.md` | IEEE T-ITS | **Deep read (2026-06-18):** Jiang 2022 (engine, names gap in print) + Zhu 2025 (vehicle-**group** ≠ type — premise reframed weaker) |
| `raw/papers/carry_over/ESWA-deepread.md` | ESWA | **Deep read (2026-06-18):** Sarraf 2020 — the router (Dijkstra+MCDM) + eval template (Spearman/AO/DCG); WCR formula; vehicle-blind |
| `raw/papers/carry_over/AAP-deepread.md` | AAP | **Deep read (2026-06-18):** Gao 2024 (STATS19 ZITD engine) + Wei 2024 & Wang 2025 (significance-gate ancestors: case-crossover; χ²-CI Bayesian net) |
| `raw/papers/tier1/tier1_journal1/T-ITS-abstract-refs.md` | IEEE T-ITS | **Reading pass (2026-06-18):** all 4 keywords swept; 0 full-text keepers, 1 weak abstract keeper (lead-vehicle-type TTC). Gap-test brick: no vehicle-type segment-risk/routing on T-ITS |
| `raw/papers/tier1/tier1_journal2/TR-C-abstract-refs.md` | TR Part C | **Reading pass (2026-06-18), keyword 1/3 (`safe route planning`):** the routing home. 3 promoted to full-text, 3 abstract keepers. Gap brick: 15+ yrs of safe-routing, none by vehicle type |
| `raw/papers/tier1/tier1_journal2/TR-C-deepread.md` | TR Part C | **Deep read (2026-06-18):** Mansoor 2026 (★★★ class-specific route sets + mean-excess CVaR tail = per-type routing mechanism), Sohrabi & Lord 2022 (operational home; NB weather-stratified; 8%/23%; survival-prob route aggregation), Kavta 2025 (demand-side niche: riders trade time for safety), Chandra 2014 (user-conditioned routing precedent — parametric, crash-data-free; donates multi-objective Pareto/Yen routing machinery), Hu 2018 (★ Colocation Quotient = per-type spatial significance gate; the tool to generate spatial-divergence-by-type evidence on STATS19) |
| `raw/papers/tier1/tier1_journal3/AAP-abstract-refs.md` | AAP | **Reading pass complete (2026-06-22), all premise keywords + `motorcycle crash hotspot` swept:** 12 abstract keepers, 3 full-text deep reads. Keywords 3–5 (`truck/HGV`, `vehicle type heterogeneity`, `VRU`) = noise (heterogeneity = statistical, semantic mismatch). Keyword 6 (`motorcycle crash hotspot`, spatial-divergence cluster) → the brick. Gap-test confirmed |
| `raw/papers/tier1/tier1_journal3/AAP-deepread.md` | AAP | **Deep reads (2026-06-19 & 2026-06-22):** Pathivada 2025 (motorcycle segment SPF — per-type slice flips to **under-dispersion** → CMP/HTCMP not NB/ZITD; EB ranking; homogeneous segmentation) + Barabino 2021 (★★ **R=H·V·E** per-bus-route risk → section-sum → quartile ranking) + **Lee 2018 (★★★ THE SPATIAL-DIVERGENCE BRICK — vehicle-type hot zones "substantially different" across types, statewide Florida; donates EPP per-type screening gate)** |
| `raw/papers/tier1/tier1_journal4/ESWA-abstract-refs.md` | ESWA | **Light pass (2026-06-22):** 2 keywords, both return only Sarraf (already deep-read in carry_over). No second routing paper in ESWA. **TIER 1 CLOSED.** Gap holds across all 4 Tier-1 journals |
| *(new reading-pass records continue here)* | | |

---

## Queries (Filed Answers)

| Page | Date | Description |
|------|------|-------------|
| [[wiki/queries/2026-06-18-where-we-stand-and-remaining-gaps]] | 2026-06-18 | Post-deep-read standing + gap analysis; which gaps the reading plan covers vs. the per-type density risk that only a data probe can answer |

## Build Plan

System design and stage-by-stage implementation guides (output of 2026-06-23 system planning session).

| Page | Description |
|------|-------------|
| [[wiki/build/system-overview]] | Full pipeline overview — two halves, 6 stages, data sources, AI architecture, key design decisions |
| [[wiki/build/stage-1-data-prep]] | Clean and join STATS19 tables into a single crash-level table |
| [[wiki/build/stage-2-segmentation]] | Segment OS Open Roads network; map-match crashes; attach AADF traffic counts |
| [[wiki/build/stage-3-cluster-share-engine]] | **★ FINAL Stage 3 engine + rewrite blueprint (2026-07-06).** Per-type discrete network clustering + share target + 5 separate XGBoost; validated leakage-free; test→main-file mapping, leakage guards, explainability layers |
| [[wiki/build/stage-3-gat-risk-model]] | *(superseded)* the GAT design where type-collapse happened — audit trail |
| [[wiki/build/stage-4-risk-surface-filtering]] | Threshold GAT output; CLQ post-hoc divergence maps |
| [[wiki/build/stage-5-routing]] | Yen's k-shortest paths + MCDM ranking (AHP/PROMETHEE) per vehicle type |
| [[wiki/build/stage-6-evaluation]] | Risk model precision@X%; routing counterfactual + Sarraf metrics; divergence test |

---

## Concepts & Methods

| Page | Description |
|------|-------------|
| [[wiki/concepts/vehicle-type-risk-divergence]] | **★ CORE.** Ground-truth per-type crash surfaces are near-orthogonal (ρ≈0, 4% hotspot overlap; survives denoising) — niche confirmed. But the unified GAT collapses it to ρ=0.855 (type-collapse). Ladder diagnostic pins cause to architecture, not message passing/sparsity. Fix = decouple types. #thesis-core #decision |
| [[wiki/concepts/routing-risk-normalization]] | How Stage-3 risk becomes a Stage-5 edge weight (cap × norm-scope × λ). Why the naive version gave identical routes for every type; capping is the lever; per-type vs global norm; λ≈2. #thesis-core #decision |

---

## Entities (People, Tools, Datasets, Orgs)

| Page | Type | Description |
|------|------|-------------|
| *(none yet)* | | |

---

## Progress Notes

| Page | Date | Summary |
|------|------|---------|
| [[wiki/progress/2026-07-07]] | 2026-07-07 | **Direction-justification test battery** (tangent from Stage 3 dev; to be re-run in Stage 6). Grouping-robustness/MAUP: cross-type ρ stable ≈[−0.03,−0.08] across 3 thresholds × 3 schemes (incl. type-blind grid) → divergence comes from the SHARE TARGET, not the partition. **CLQ** (raw 885k points, permutation-tested) certifies the premise but reveals a **3-group structure** (car/two-wheeler/freight): moto↔cycle & lgv↔hgv colocate, all else segregated (cycle↔hgv 0.57) — answers Zhu group-vs-type, softens "near-orthogonal". Field-standard eval metrics identified (Cheng-Washington, crashes@top-X%, HSM, Sarraf) |
| [[wiki/progress/2026-07-06]] | 2026-07-06 | **★ Engine rebuilt (lost 07-04 code), validated LEAKAGE-FREE (16-fold spatial CV + unseen-2024 temporal holdout → national OOS ρ=−0.097, 2024 validity ≈ target-year = no leakage), decision FINALIZED (XGBoost cluster+share; GAT retired), 2 explainability layers + per-route explainer added. Produced the Stage 3 rewrite blueprint. All in `code/tests/cluster_risk/`** |
| [[wiki/progress/2026-07-04-clustering-testing]] | 2026-07-04 | **Clustering direction built and tested end-to-end.** Plan's literal feature-based clustering FAILS (ρ≈0.65-0.9, no better than original GAT) — car/lgv/hgv own-AADF correlate with each other. What works: discrete network/location-based clusters + share-of-all-type-total objective + fully separate per-type XGBoost. Validated on spatial holdout (ρ=0.201, beats best-GAT 0.377) and end-to-end routing test (3.10/5 distinct routes vs. GAT's 2.00/5). Mistakes made and corrected logged in full |
| [[wiki/progress/2026-07-04]] | 2026-07-04 | Supervisor meeting: 2026-07-03 statistical-vs-GAT-stacked fork reframed, not answered directly. New direction — per-type clustering to fix raw sparsity, statistical-vs-model decided at cluster level via same evaluation gate. Plan drafted (`new-direction-plan-2026-07-04.md`), two sub-questions on routing-search grouping still open |
| [[wiki/progress/2026-07-03]] | 2026-07-03 | Full type-collapse investigation: architecture ladder, feature leak caught+fixed, type-specific-vs-agnostic mechanism confirmed 4x, best GAT (share-target+per-head, no new data) reaches ρ=0.377, EB shrinkage tested and beaten by ad hoc statistical smoothing, Task B (conditional risk) killed. Strategic fork logged for supervisor |
| [[wiki/progress/2026-07-02]] | 2026-07-02 | Stage 3 retrained (fixed); routes were identical across types — real cause was uncapped per-type norm over an exposure-artifact max. Phase A factorial: capping is the lever, per-type norm > global, λ≈2. Divergence real but modest |
| [[wiki/progress/2026-06-30]] | 2026-06-30 | Stage 5 bug fixed (risk_scores.csv swap) — **⚠ corrected 2026-07-02: necessary but insufficient**; bbox limitation surfaced and documented |
| [[wiki/progress/2026-06-26]] | 2026-06-26 | GAT teaching session — message passing, weight matrices, type-conditioned attention, oversmoothing; Stage 3 code starts tomorrow |

---

## Carried over from prior phases (read-only context)

| Page | Why it still matters |
|------|----------------------|
| [[../PHASE2/positioning-memo]] | The superseded CRM/LLM positioning — audit trail of the pivot |
| [[../PHASE2/PLAN]] | Phase 2 reading plan + the inherited papers (Jiang, Sarraf, Gao, Zhu, de Souza) |
| [[../PHASE1/wiki/progress/NEW_FIX_PROF]] | The segment/significance design that survives the pivot |
| [[../PHASE1/analysis]] | MI / Cramér's V + spatial/hotspot analysis assets |

---

*Last updated: 2026-07-06 | **Stage 3 engine FINALIZED + validated leakage-free (XGBoost cluster+share); GAT retired; rewrite blueprint written ([[wiki/build/stage-3-cluster-share-engine]]); next = fold into main pipeline.** Earlier note below retained for history. | 2026-07-04 (night testing): **Clustering direction built and tested — its literal mechanism failed, a different one works.** The plan's feature-based clustering (road_class+AADF+length) never beat ρ≈0.65, no better than the original collapsed GAT. What actually works: discrete network/location-based clusters (not feature-based) + share-of-all-type-total objective + fully separate per-type XGBoost models — validated on a genuine spatial holdout (whole city excluded from training: ρ=0.201, beats best-GAT's 0.377) and an actual end-to-end routing test (3.10/5 types take distinct routes, vs. GAT's 2.00/5). Nothing yet committed to the codebase (all tested ad hoc). Two sub-questions from the original plan (routing-search grouping split, "zoom in" semantics) still open, plus new open items (check 2 non-diverging routing pairs; test GAT with the new recipe; validity-check other methods). See [[wiki/concepts/vehicle-type-risk-divergence]] and [[wiki/progress/2026-07-04-clustering-testing]].*
