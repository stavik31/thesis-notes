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
| [[wiki/overview]] | Evolving thesis argument + project state (Phase 3) — *to be written* |

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

## Concepts & Methods

| Page | Description |
|------|-------------|
| *(none yet)* | |

---

## Entities (People, Tools, Datasets, Orgs)

| Page | Type | Description |
|------|------|-------------|
| *(none yet)* | | |

---

## Progress Notes

| Page | Date | Summary |
|------|------|---------|
| *(none yet)* | | |

---

## Carried over from prior phases (read-only context)

| Page | Why it still matters |
|------|----------------------|
| [[../PHASE2/positioning-memo]] | The superseded CRM/LLM positioning — audit trail of the pivot |
| [[../PHASE2/PLAN]] | Phase 2 reading plan + the inherited papers (Jiang, Sarraf, Gao, Zhu, de Souza) |
| [[../PHASE1/wiki/progress/NEW_FIX_PROF]] | The segment/significance design that survives the pivot |
| [[../PHASE1/analysis]] | MI / Cramér's V + spatial/hotspot analysis assets |

---

*Last updated: 2026-06-22 | **TIER 1 CLOSED** (T-ITS · TR-C · AAP · ESWA all swept). Reading phase essentially complete (~14 deep reads + ~25–30 abstract keepers). Niche spatial-divergence premise upgraded analogical→demonstrated (Lee 2018) and validated on STATS19 data. **Now: system-build planning underway** (6-stage pipeline; paused mid-Stage-3). Next deliverable: full positioning-memo revamp after the build design is settled.*
