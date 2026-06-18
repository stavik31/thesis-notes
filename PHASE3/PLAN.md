---
title: "Phase 3 — Risk-Aware Routing + Data-Niche Grounding"
type: plan
date: "2026-06-17"
status: ACTIVE — this is the current working folder
tags: [phase3, literature-review, thesis-core, decision, route-planning]
---

# Phase 3 — Route Planning as the Home, a Data Niche as the Novelty

> **Phases 1 and 2 are now history.** Phase 1 (`../PHASE1/`) = the built system
> (narratives, severity LoRA, FAISS RAG, analyses). Phase 2 (`../PHASE2/`) = the
> reading week that searched for a research home for an *LLM-NL-output* thesis.
> **The 2026-06-17 supervisor meeting cut the LLM and relocated the thesis.** Phase 3
> is the new direction: **risk-aware route planning**, with the novelty living in a
> **data niche** (vehicle-type-conditioned crash risk) rather than in an NL layer.
> We work the same way as Phase 2: read good-journal papers, paste them in, discuss
> each against a template, record lightweight per-journal entries.

---

## Why we're here (the supervisor meeting, 2026-06-17)

Third meeting, after presenting the Phase 2 positioning memo (CRM home + LLM-NL
explanation + significance gate). What he said, decoded:

1. **Drop the LLM.** Its hard problems — faithfulness/hallucination, evaluation of
   generated text — are not solvable in the time available. On top of that, **language
   is inherently distracting** to a driver and **varies too much per person** to be a
   solid deliverable. Even though the literature (Ryder, Wu) shows NL *can* work, it is
   not solidified enough to anchor a thesis. → The NL output, faithfulness layer, and
   LoRA fine-tune are **out of the core**.

2. **Route planning is the home — he liked it a lot ("very good").** The Phase 2
   "applied layer" is promoted to *the* thesis. The field is risk-aware / safety-aware
   route planning.

3. **Complexity over novelty.** His exact standard: *"I don't always need novelty, but
   I always need complexity of the system."* A thesis is judged on the depth and
   sophistication of the built pipeline, not on one breakthrough claim. A rich
   multi-stage system (data → risk profiling → segmentation → routing → evaluation) is
   defensible even when individual components have precedent.

4. **Find a niche within the data nobody has explored.** This is what he means by the
   novelty that *does* matter. Example he gave: one paper did UK hotspots of
   heavy-crash areas; **I could condition on vehicle type** and adjust route planning by
   it (a motorcycle and an HGV face different risk on the same segment). The niche is a
   dimension that exists in the data but hasn't been used for routing.

5. **Other datasets are on the table** — to open up additional niches if STATS19 alone
   is too thin for the chosen dimension. Caveat (ours): a second *crash* dataset adds
   cleaning/comparability cost; auxiliary datasets that *enrich* STATS19 (OS road
   network, Met Office weather, DfT AADF traffic counts for exposure) are the cheaper,
   higher-value adds.

**The payoff:** route planning hands us a real, active research field with baselines
(Jiang 2022, Sarraf 2020) and an evaluation tradition; the data niche (vehicle type)
hands us the defensible novelty; the multi-stage pipeline supplies the complexity. No
LLM problem to solve.

---

## The direction, as of 2026-06-17 (see `positioning-memo.md` for the living version)

- **Home field:** risk-aware / safety-aware route planning.
- **Engine (upstream):** STATS19 segment-level crash-risk modeling (Gao-2024 lineage).
- **Niche / novelty:** **vehicle-type-conditioned** segment risk → vehicle-specific
  routing. Possibly layered with weather/time as secondary conditioning axes *where the
  data supports a significant cell* (graceful fallback when it doesn't = a complexity
  feature, not a bug).
- **Output (NO LLM):** ranked alternative routes (risk + time + distance) and/or a
  vehicle-type-specific risk-scored map. The deliverable is the route, not language.
- **Evaluation:** temporal holdout (profiles on years 1–4, test year 5, *per vehicle
  type*) + routing-quality metrics (Spearman rank, Average Overlap, DCG — from Sarraf
  2020) + the headline divergence/counterfactual test (does vehicle-type routing differ
  from aggregate routing, and does the difference track real per-type crash patterns?).

---

## Goal of this reading pass

Phase 2 read deeply into the *old* core (LLM/explanation/faithfulness — now cut) and
only skimmed the edges of the *new* core. This pass fills the two thin areas:

1. **Risk-aware routing** — the new home field. Right now we have **Jiang 2022 (1 deep
   read) + Sarraf 2020 (abstract) + de Souza 2020 (abstract, crime not crash)**. That is
   not enough to write a related-work chapter. This is the priority.
2. **Vehicle-type heterogeneity in crash risk** — the justification that risk genuinely
   differs by vehicle class, so routing-by-type is warranted. We have **Zhu 2025
   (abstract, vehicle-*group* prediction)** and one geometry-heterogeneity freeway paper.
   Thin.
3. **Routing evaluation methodology** — inherited from Sarraf + Jiang; confirm and extend.

Deliverable: a per-journal reading record set (lightweight, like Phase 2) + a kept-current
`positioning-memo.md`. Stop when the routing home and the vehicle-type premise each have
3–5 solid papers and the gap test ("does anyone do vehicle-type-conditioned crash-risk
routing?") has been run across the venues.

> **What reading CANNOT resolve (recorded 2026-06-18 so we don't expect it to).** Two risks are
> *not* literature questions:
> 1. **Feasibility — per-type density.** Whether STATS19 has enough motorcycle/HGV crashes *per
>    segment* to build a stable per-vehicle-type risk surface. Aggregate zero-inflation is ~96%
>    (Gao); per-type it is far worse. **No paper answers this — only a data probe does** (slice
>    STATS19 by vehicle-type × segment, look at the sparsity). This is the thesis's single biggest
>    existential risk and is tracked as an *early* task, run in parallel with the first niche-premise
>    reads — see the query page and positioning-memo Open Decision #6.
> 2. **Per-type exposure availability.** Whether DfT AADF traffic counts resolve by vehicle type at
>    a usable spatial scale (needed so "motorcycle risk" isn't confounded with motorcycle *volume*).
>    A data-availability check, not a reading outcome.

---

## Where to look — journal tiers + keywords (re-pointed at routing + vehicle type)

**Tier 1 — Risk-aware routing + vehicle-type crash risk (START HERE).**
| Journal | What to search in it |
|---|---|
| **IEEE T-ITS** | `risk-aware route planning`, `safest path routing`, `safety-aware navigation`, `vehicle type crash risk` — richest venue, bridges routing + risk |
| **Transportation Research Part C** (emerging tech) | `safe routing`, `risk-based navigation`, `routing crash risk` — the routing/algorithms home |
| **AAP** | `motorcycle crash risk segment`, `truck/HGV crash risk`, `vehicle type crash heterogeneity`, `vulnerable road user crash` — the vehicle-type-risk evidence |
| **Expert Systems w/ Applications** | `safe route planner`, `multi-criteria route`, `routing decision support` — MCDM routing layer (Sarraf lives here) |

**Tier 2 — Spatial, intelligent-vehicle & application venues.**
| Journal | What to search in it |
|---|---|
| **IEEE Trans. Intelligent Vehicles** | `risk map routing`, `vehicle-specific risk` |
| **Transportation Research Record (TRR)** | `network screening vehicle type`, `crash risk by vehicle class` |
| **Computers, Environment & Urban Systems / IJGIS** | `spatial crash risk`, `routing GIS safety` — the spatial-analysis routing angle |
| **Smart Cities / Sensors / IoT** | `connected vehicle routing`, `real-time risk routing` |
| **Journal of Safety Research** | `motorcycle/HGV safety`, `road user crash risk` |

**Tier 3 — Method/breadth sweep (only if Tiers 1–2 leave gaps).**
Megajournals (Applied Sciences, Sustainability, Information, IEEE Access) keyword sweeps:
`risk-aware routing`, `safest path`, `vehicle type crash risk`, `crash risk heat map`.

**Keyword clusters (search by cluster):**
- *Routing (home):* `risk-aware route planning`, `safest path routing`, `safety-aware
  navigation`, `crash-risk routing`, `safe route recommendation`, `risk-based vehicle routing`
- *Vehicle-type niche — PREMISE (do types differ at all):* `motorcycle crash risk`, `heavy
  goods vehicle crash`, `truck crash segment`, `vehicle type crash heterogeneity`,
  `vulnerable road user crash risk`
- *Vehicle-type niche — SPATIAL DIVERGENCE (the sharper, load-bearing claim — added 2026-06-18):*
  `motorcycle crash hotspot`, `vehicle class network screening`, `crash hotspot vehicle type
  spatial`, `vehicle-type crash spatial distribution`. **Why separate:** the PREMISE keywords find
  papers showing types differ in crash *factors/severity/frequency* — a weaker claim. The thesis
  needs evidence that *different segments are risky for different types* (motorcycle hotspots ≠ HGV
  hotspots as *places*). A paper proving "motorcycles crash more at junctions" does NOT supply this.
  Hunt the spatial form explicitly or you can read ten "premise-confirming" papers and still lack
  the brick. **This cluster is the #1 priority of the pass.**
- *Segmentation / spatial-unit decision (added 2026-06-18 — to inform the build choice, not just
  related work):* `crash hotspot DBSCAN`, `road segmentation crash risk`, `spatial unit crash
  analysis`, `network screening segment definition`
- *Risk modeling (mostly have it):* `road segment crash risk`, `network screening`,
  `crash risk prediction segment`, `empirical Bayes crash`
- *Evaluation:* `route ranking evaluation`, `safe route evaluation`, `MCDM route comparison`

---

## How to read (carried over from Phase 2 — it worked)

1. **Triage first** — abstract + figures + conclusion; keep/discard in ~5 min.
2. For each keeper, extract: **problem · method · data · how they represent risk · how
   they route (if they do) · does it use vehicle type or any per-class conditioning ·
   what's missing · is this `home` / `niche-evidence` / `baseline` / `borrow`?**
3. **The gap test for Phase 3:** *does anyone do vehicle-type-conditioned (or any
   per-class) crash-risk routing?* Every "no" is a brick for the niche.
4. Record lightweight per-journal `*-abstract-refs.md` entries (NOT full wiki INGEST) —
   same style as Phase 2's reading records.

### Model usage policy (same as Phase 2)
- **Sonnet 4.6 (default):** triage, recording, index/log bookkeeping, routine Q&A.
- **Opus 4.8 (switch in):** deep reads of `home`/`niche` papers, the niche decision, any
  positioning-memo rewrite, anything going to the supervisor.

---

## What carries over (assets that survive the pivot)

**From Phase 2 (re-tagged for routing):**
- **Jiang 2022** (Safe Route Mapping, T-ITS) — promoted to the *home* paper.
- **Sarraf & McGuire 2020** (MCDM Safe Route Planner, ESWA) — the routing-layer + eval
  methodology. Get full text.
- **Gao 2024** (STZITD-GNN, AAP) — the STATS19 segment-risk baseline; Zero-Inflated
  Tweedie borrow for ~96% zero-inflation.
- **Zhu 2025** (Vehicle-Group crash risk, T-ITS) — validates the vehicle-type premise.
- **de Souza 2020** (Safe & Sound re-routing, T-ITS) — personalized per-type re-routing
  pattern (risk = crime, so precedent not baseline).
- **Wei 2024 / Wang 2025** (AAP) — condition-conditioned segment risk is valid (for the
  secondary weather/time axes).
- *Demoted to future-work:* the entire explanation-layer lineage (Zhang, Gyawali,
  Hussien, Smetana, Wu, TrafficRiskGPT, Tab-Text, Li 2025) — the LLM is out of scope.

**From Phase 1:**
- STATS19 ingestion + the tabular pipeline, MI/Cramér's V + spatial/hotspot analysis
  (`../PHASE1/analysis/`), the segment-significance design (`../PHASE1/wiki/progress/NEW_FIX_PROF.md`).

---

## Links

- `positioning-memo.md` — the living statement of the current direction (update as we read)
- `../PHASE2/positioning-memo.md` — the *superseded* CRM/LLM memo (kept for the audit trail)
- `../PHASE2/PLAN.md` — the Phase 2 reading plan (how this folder is structured)
- `../PHASE1/wiki/progress/NEW_FIX_PROF.md` — the segment/significance design that survives
