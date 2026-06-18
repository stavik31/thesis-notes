---
title: "Where does Phase 3 stand after the carry-over deep reads, and what gaps remain?"
type: query
date: "2026-06-18"
tags: [phase3, decision, thesis-core, route-planning, gap-analysis]
---

# Where we stand + remaining gaps (post deep-read of the 6 carry-over papers)

Filed after deep-reading all 6 carry-over PDFs (Jiang, Zhu, Sarraf, Gao, Wei, Wang — see
[[T-ITS-deepread]], [[ESWA-deepread]], [[AAP-deepread]]) and stress-testing the reading plan against
the gaps it's supposed to close. This is the "before we read more, where are we" reference.

## What's locked

- **Home field is real with a mature toolchain.** A working **router** ([[ESWA-deepread|Sarraf 2020]]:
  Dijkstra + MCDM + DCG eval) sits downstream of a working **engine** ([[AAP-deepread|Gao 2024]] /
  [[T-ITS-deepread|Jiang 2022]]: STATS19 segment risk). We assemble proven parts.
- **Stack shape is clear:** engine → router, **both vehicle-blind**. The contribution threads vehicle
  type through both. (Key correction from the reads: **Jiang is the engine, not a router** — it makes
  a heat map; Sarraf is the router. Jiang even names the gap in print: *"risks are not dependent on …
  vehicle types or weather conditions."*)
- **Borrowable machinery is identified to the formula:** WCR (severity+exposure scalar per segment),
  ZITD for ~96% zero-inflation, severity weighting (1/2/3), MPIW/PICP/AccHR@20, Spearman/Average-
  Overlap/**DCG**, and two candidate significance gates (case-crossover; χ²-CI Bayesian net).

## The gaps — three kinds, very different

### A. Literature gaps — reading WILL close these
1. **Niche premise is unproven.** No solid evidence yet that segment risk *diverges by vehicle class*
   in a route-changing way. [[T-ITS-deepread|Zhu 2025]] does NOT supply it (it's vehicle-**group**, not
   type). **Priority 1.**
2. **Gap test not run across the routing literature.** TR-Part-C (the routing/algorithms home) is
   completely untouched; a novelty claim needs the gap test run *there*.
3. **Routing-eval depth** is thin (one paper, Sarraf).

### B. Design decisions — reading informs, but we choose
Segment definition (link vs grid vs DBSCAN), which significance gate, engine complexity (full
ZITD-GNN vs lighter per-type rate model). Not search targets; choices the reading informs.

### C. Data-feasibility gaps — papers CANNOT answer these
1. **Per-type density:** is STATS19 dense enough per-type-per-segment? Aggregate zero-inflation ~96%;
   per-type far worse (motorcycle/HGV are a fraction of crashes). **No paper answers this — only a data
   probe does.** This is the single biggest existential risk.
2. **Per-type exposure:** does DfT AADF resolve by vehicle type at a usable scale, so per-type risk
   isn't confounded with per-type *volume*?

## Will the reading plan (PLAN.md keywords) uncover the gaps?

| Gap | Plan coverage | Verdict |
|---|---|---|
| Niche premise (types differ at all) | AAP `motorcycle/truck/vehicle-type heterogeneity`, J-Safety-Research, TRR `crash risk by vehicle class` | **Yes** |
| **Niche premise — SPATIAL form** (different segments risky for different types) | originally **NOT** sharply targeted | **Was a hole → fixed**: added `motorcycle crash hotspot`, `vehicle class network screening`, `crash hotspot vehicle type spatial`, `vehicle-type crash spatial distribution` (PLAN.md, 2026-06-18) |
| TR-Part-C routing gap test | TR-C Tier 1: `safe routing`, `risk-based navigation`, `routing crash risk` | **Yes** |
| Routing-eval depth | ESWA `multi-criteria route`; eval cluster | **Yes** |
| Segment-definition decision | originally only brushed | **Sharpened**: added `crash hotspot DBSCAN`, `road segmentation crash risk`, `spatial unit crash analysis` (PLAN.md, 2026-06-18) |
| **Per-type density (feasibility)** | — | **NO — structurally outside reading.** Needs a data probe. |
| **Per-type exposure (feasibility)** | — | **NO — data-availability check, not a reading outcome.** |

**Why the spatial-divergence sharpening mattered:** the premise keywords find papers showing types
differ in crash *factors/severity/frequency* — a weaker claim than the thesis needs. "Motorcycles
crash more at junctions" ≠ "motorcycle hotspots and HGV hotspots are different *places*." Without the
spatial keywords we could read ten premise-confirming papers and still lack the load-bearing brick.

## Bottom line

The reading plan is **well-aimed at the literature gaps** (premise, routing gap test, eval) — and with
the spatial-divergence + segmentation keywords now added, it's tight. But it is **structurally blind to
the biggest existential risk** (per-type density), which only a data probe can answer. That probe is
therefore **not redundant with reading** — it covers a gap reading cannot — and is tracked as an early,
parallel task ([[positioning-memo]] Open Decision #6).

## Actions taken from this analysis
- PLAN.md: added the **spatial-divergence** keyword cluster (#1 priority) + the **segmentation** cluster;
  recorded the "what reading CANNOT resolve" caveat.
- positioning-memo: added **Open Decision #6** (per-type density probe + exposure-confound sub-risk).

## Next-step sequencing (recommended)
1. **In parallel, now:** kick off the **STATS19 per-type density probe** (data, not reading) +
   start the **spatial-divergence** niche reads (AAP / J. Safety Research).
2. Then the **TR-Part-C routing gap test**.
3. Then routing-eval depth + the design-decision reads (segmentation, gate).

## Links
- [[positioning-memo]] — Open Decision #6 (the probe); evidence map
- [[PLAN]] — keyword clusters (spatial-divergence + segmentation added)
- [[T-ITS-deepread]] · [[ESWA-deepread]] · [[AAP-deepread]] — the deep-read records this builds on
