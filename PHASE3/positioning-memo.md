---
title: "Phase 3 Positioning Memo — Risk-Aware Routing with a Vehicle-Type Niche (LIVING)"
type: memo
date: "2026-06-17"
status: LIVING DRAFT — update as the reading pass proceeds
tags: [phase3, positioning, thesis-core, route-planning, decision]
---

# Phase 3 Positioning Memo (LIVING)

> **What this is.** A *living* statement of where the thesis stands right now. Unlike the
> Phase 2 memo (a one-shot end-of-week synthesis), this file is updated as papers come in.
> It always answers four questions in the current best form: **what field, what niche,
> what system, what evidence so far.** Edit it; don't append a new one.
>
> **Status of the corpus (2026-06-17):** the pivot just happened. Risk-modeling
> literature is well-covered (inherited from Phase 2); the *routing home* and the
> *vehicle-type niche* are thinly covered and are the target of this reading pass.

---

## The direction in one paragraph (current)

This thesis contributes to **risk-aware route planning** — the field that ranks routes
not only by time and distance but by crash risk (Jiang 2022; Sarraf 2020). Existing
safe-route systems compute a single aggregate crash-risk score per road segment and route
everyone by it. **They treat all vehicles the same.** But crash risk is not uniform across
vehicle types: a motorcycle, an HGV, and a car face materially different risk on the same
wet, unlit bend or the same busy junction. This thesis builds a routing system whose
risk layer is **conditioned on vehicle type** (and, where the data supports it, on weather
and time), so that the recommended route differs by what you are driving. STATS19 supplies
the crash data (vehicle type is on every record); the method is jurisdiction-agnostic.
**No natural-language layer** — the deliverable is the route and its risk breakdown, not a
generated explanation (the LLM direction was cut as un-solidified and distracting).

---

## Scope & depth — distinctive direction vs. system complexity (resolved 2026-06-18)

**Terminology, pinned (important — avoids a recurring confusion).** "Novelty" has two senses and the
supervisor split them: (a) **breakthrough novelty** = inventing a new method/algorithm — **NOT
required** ("I don't always need novelty"); (b) **the data niche** = applying *existing/borrowed*
methods to a *new data direction* (vehicle type) — **explicitly asked for.** This thesis is firmly (b):
**nothing is invented — everything built is borrowed** (CLQ gate, ZITD/NB engine, MCDM/mean-excess
routing). The contribution is the **direction** that borrowed machinery is pointed, plus the
**complexity** of the pipeline. So below, "distinctive direction" = the data-niche application, *not*
breakthrough novelty.

The thesis is **two layers of one pipeline, not a choice between them.** A recurring point of
confusion ("do we go deep into route optimization or into the vehicle-type niche?") is resolved as:

```
STATS19 → [ RISK LAYER: per-vehicle-type crash-risk surface ]  = DISTINCTIVE DIRECTION (the data niche)
        → [ ROUTING LAYER: risk + time + distance → routes   ]  = SYSTEM (the home — complexity)
        → [ EVALUATION: type-aware vs aggregate routing       ]  = the PAYOFF check (does the direction diverge?)
```

**Both layers must be credible — but they earn their depth differently, and effort should be spent
knowing which payoff you're buying:**

- **Risk layer (per-vehicle-type) — depth buys the DISTINCTIVE DIRECTION + rigor.** Every step deeper
  (per-type significance gating, sparsity/zero-inflation handling, per-type exposure normalisation,
  spatial divergence of hotspots by type) *directly strengthens the contribution*. **This is the spine
  of the thesis** — but note it is **borrowed methods on new-directioned data, not a new method.**
- **Routing layer — depth buys COMPLEXITY only.** Go deep enough to build a *credible* multi-objective
  router, and **borrow** the machinery (Mansoor 2026 mean-excess/VI; Sarraf 2020 MCDM; Sohrabi & Lord
  2022; Chandra 2014 Pareto/Yen). Going *deeper* (Pareto multi-objective, time-dependent, reliability)
  adds the *system complexity* the supervisor rewards but **no additional distinctiveness**. Do **not**
  try to invent new routing optimisation — that's not where the contribution lives.

**The premise concern is JUSTIFICATION, not novelty.** The vehicle-type direction must actually *pay
off*: if motorcycle hotspots and HGV hotspots are the *same places*, type-aware routing produces the
*same routes* as aggregate routing → null result, nothing to show. So confirming spatial divergence by
type (via the data probe + CLQ) isn't about being novel — it's about the application **not being a
no-op.** That is the one thing that still must hold.

**Why neither layer alone is a thesis:** pure routing optimisation = no data niche = nothing distinctive
(an examiner asks "Sarraf already does multi-criteria safe routing — what's yours?"); pure vehicle-type
risk = just another crash-risk-modelling paper (Gao already does STATS19 segment risk) with no applied
home. The **combo is the deliverable**: the data niche supplies the distinctiveness, the multi-stage
pipeline supplies the complexity — the 2026-06-17 supervisor framing ("complexity over novelty" + "a
data niche nobody explored, e.g. vehicle type").

**One-line scope:** *go decently deep in both layers; the spine is per-vehicle-type risk (the data-niche
direction — borrowed methods, new data), and the routing optimisation is the borrowed-and-deepened
system that delivers it (complexity). No method is invented; the only thing that must hold is that the
vehicle-type direction actually diverges (justification, not novelty).*

---

## The four questions (kept current)

### 1. What field? — Risk-aware / safety-aware route planning
The home is routing, not crash-risk-modeling-as-an-end. CRM (Gao 2024 etc.) is the
*engine* that produces the per-segment risk the router consumes. Predecessors:
- **Jiang 2022** — Safe Route Mapping (SPF/EB/HSM → per-segment risk → safe-route heat maps). **The home paper.**
- **Sarraf 2020** — MCDM Safe Route Planner (combines risk + time + distance into ranked routes; eval via Spearman/Overlap/DCG). **The routing-layer + eval template.**
- **de Souza 2020** — Safety-aware re-routing with *per-vehicle* risk-type selection (risk = crime; precedent for personalization, not a crash baseline).
- *Gap so far:* none of them condition the risk layer on vehicle type. ← the opening.

### 2. What niche? — Vehicle-type-conditioned segment crash risk
The novelty the supervisor asked for ("find a niche in the data nobody explored"):
- **Premise — WEAKER than carry-over assumed (deep-read correction, 2026-06-18).** Zhu 2025 is
  "vehicle-**group**," not "vehicle-**type**": a VG is a *dynamic cluster of interacting vehicles*
  (trajectory/iTTC, real-time, microscopic), with vehicle type as just 1 of 8 node features. It
  does **not** establish that different vehicle *classes* face different *segment* risk, and it
  doesn't route. So Zhu is a methodological cousin (graph + GNNExplainer XAI) and Abdel-Aty field
  anchor, **not** the niche's core premise. → **The vehicle-type-heterogeneity evidence base is
  still THIN and is the live priority** (need real AAP motorcycle/HGV segment-risk papers). See
  [[T-ITS-deepread]].
- **Unoccupied for routing:** no paper in the corpus routes by vehicle type. Sarraf's router even
  normalises by AADT but has **no vehicle-type term** (deep-read confirmed — [[ESWA-deepread]]).
- **Combinable:** vehicle type as the primary axis; weather/time as secondary axes added
  only where a per-cell crash count is significant (graceful fallback otherwise — this
  multi-dimensional-sparsity handling is itself system complexity).
- *Alternatives considered:* vulnerable-road-user exposure, manoeuvre type, junction type.
  Vehicle type leads on availability + intuition + clean one-line pitch.

### 3. What system? (complexity = the thesis, per the supervisor)
Multi-stage pipeline:
1. STATS19 → segment-level crash records, tagged by vehicle type.
2. Spatial segmentation (road link / grid / DBSCAN — open decision, gates everything).
3. **Per-segment, per-vehicle-type risk profiling** with a significance/overrepresentation
   gate (which type×condition patterns are non-random vs the network baseline).
4. Risk-model handling of sparsity (~96% zero-inflation; fatal ~1.5%) — Zero-Inflated
   Tweedie (Gao) / imbalance shelf.
5. **Routing layer** — given origin + destination + vehicle type, score candidate routes
   on combined risk + time + distance (MCDM, Sarraf lineage).
6. Output: ranked routes + vehicle-type-specific risk-scored map. **No LLM.**

### 4. What evidence / evaluation?
- **Risk-model validity:** temporal holdout, *per vehicle type* (profiles on years 1–4,
  test year 5) + precision@top-X% high-risk segments (Gao metrics).
- **Routing quality:** Spearman rank correlation, Average Overlap, DCG (Sarraf metrics).
- **Headline result:** does vehicle-type-aware routing *diverge* from aggregate routing
  for the same O–D pair, and does the divergence track real per-type crash patterns?
  Counterfactual: would a motorcyclist routed by this system pass through fewer historical
  *motorcycle*-crash segments than under shortest-path / aggregate-risk routing?

---

## What changed from Phase 2 (the pivot, for the audit trail)

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

## Open decisions (to resolve as reading + design proceed)

1. **The niche — vehicle type confirmed, or combine with a 2nd axis from the start?**
   (Leaning: vehicle type primary, weather/time secondary where data allows.)
2. **Segment definition** — road link vs grid vs DBSCAN (gates the whole build).
3. **Significance test** — candidates now: chi-square overrepresentation (Wang lineage) vs Empirical
   Bayes vs Bayesian network vs **Colocation Quotient (Hu 2018 — per-type spatial overrepresentation,
   Monte-Carlo significance, network-distance, MAUP-aware)** vs case-crossover matched control (Wei).
   Baseline = network-wide vs road-class-specific; min-crash threshold per cell. (CLQ is the most
   *spatial* and most directly per-type — strong contender, ties to Phase-1 spatial assets.)
4. **Auxiliary datasets** — OS road network + Met Office weather + DfT AADF (exposure) are
   high-value, low-cost. A second crash dataset only if a chosen niche is data-starved.
5. **Output form** — ranked routes vs risk-map overlay vs both.
6. **⚠ FEASIBILITY (existential, NOT a reading question) — per-type density probe.** Does STATS19
   have enough motorcycle/HGV crashes *per segment* to build a stable per-vehicle-type risk surface?
   Aggregate zero-inflation ~96% (Gao); per-type far worse. **An early data probe must answer this**
   (slice STATS19 by vehicle-type × segment; inspect sparsity) — it gates segment-definition (#2)
   and how many secondary axes (#1) are affordable. Run it in *parallel* with the first niche-premise
   reads, not after. Linked sub-risk: **per-type exposure** — does DfT AADF resolve by vehicle type
   so per-type risk isn't confounded with per-type volume?

---

## Evidence map (running — updated as papers land)

### Routing home
| Paper | Role | Status |
|---|---|---|
| Jiang 2022 (T-ITS) | home = risk **engine** (NB/EB heat map, **not** a router; names the gap in print) | **deep-read full text (2026-06-18)** — [[T-ITS-deepread]] |
| Sarraf & McGuire 2020 (ESWA) | the actual **router** (Dijkstra + MCDM) + eval template (Spearman/AO/DCG); vehicle-blind | **deep-read full text (2026-06-18)** — [[ESWA-deepread]] |
| de Souza 2020 (T-ITS) | personalization precedent | abstract only |
| **Mansoor, Li, Chen 2026 (TR-C)** | ★★★ **structural ancestor**: class-specific route choice sets + mean-excess (CVaR) crash-severity tail — the per-type routing *mechanism*, keyed on safety preference not vehicle type | **deep-read (2026-06-18)** — [[TR-C-deepread]] |
| **Sohrabi & Lord 2022 (TR-C)** | operational home + motivation: safest-vs-shortest on 29k Texas segments; NB models stratified by weather; **8% time → +23% crash**; survival-prob route aggregation | **deep-read (2026-06-18)** — [[TR-C-deepread]] |
| **Kavta et al. 2025 (TR-C)** | **demand-side niche brick**: a vehicle class (delivery riders) *will* trade time for safety (VRR/WTA); SP/behavioural | **deep-read (2026-06-18)** — [[TR-C-deepread]] |
| **Chandra 2014 (TR-C)** | closest **user-conditioned** routing precedent (older drivers/bicyclists) — but parametric (speed+PRT), crash-data-free, **no per-type risk surface**; donates multi-objective (Pareto/Yen) routing machinery | **deep-read (2026-06-18)** — [[TR-C-deepread]] |

> **Structural finding (deep read):** Jiang = engine (risk score → heat map, no routing);
> Sarraf = router (consumes a per-segment score, ranks routes). **engine + router = the
> assembled stack; the thesis conditions both on vehicle type.** TR-C deep reads add the
> *mechanism* to do it: **Mansoor's class-specific route choice sets + mean-excess crash-severity
> tail, re-keyed from safety-preference class → vehicle type.** Mansoor names heavy-vehicle risk in
> its motivation yet omits vehicle type even from future work — the gap is wide open in the newest
> (2026) safety-routing-equilibrium work.

### Vehicle-type niche evidence
| Paper | Role | Status |
|---|---|---|
| Zhu et al. 2025 (T-ITS) | ⚠ vehicle-**group** (not type); method-cousin + Abdel-Aty anchor, **weak premise** | **deep-read full text (2026-06-18)** — [[T-ITS-deepread]] |
| **Hu, Zhang, Shelton 2018 (TR-C)** | **method to GENERATE the spatial-divergence-by-type evidence**: Colocation Quotient (GCLQ+LCLQ) = per-category spatial significance test. (Premise only analogical — combines ped+cyclist, not motor-vehicle classes.) Gap is thin partly because colocation-in-transport-safety is itself new (2018) | **deep-read full text (2026-06-18)** — [[TR-C-deepread]] |
| Freeway-segment LCA/LPA (AAP) | heterogeneity by geometry | abstract only |
| *(to be read — THE priority: motorcycle/HGV segment-risk)* | | this pass |

> **Reframe (2026-06-18):** the spatial-divergence-by-type premise being thin in the literature is
> *not* evidence it's false — the spatial tool (CLQ) is recent and nobody applied it per-vehicle-class.
> **The thesis can manufacture the premise itself** by running Hu's CLQ on STATS19 per vehicle type.
> This makes the per-type density probe (Open Decision #6) even more central — it's both the
> feasibility check *and* the first step of producing the niche evidence.

### Risk engine + significance gate (inherited, solid)
| Paper | Role | Status |
|---|---|---|
| Gao 2024 (AAP) | STATS19 segment-risk engine; ZITD borrow (~96% zero-inflation); MPIW/PICP/AccHR@20 metrics | **deep-read full text (2026-06-18)** — [[AAP-deepread]] |
| Wei 2024 (AAP) | gate ancestor #1: case-crossover matched-control design (quasi-Poisson DLM/DLNM) | **deep-read full text (2026-06-18)** — [[AAP-deepread]] |
| Wang 2025 (AAP) | gate ancestor #2: χ²-CI Bayesian network (Bonferroni; BDs for sparse cells) | **deep-read full text (2026-06-18)** — [[AAP-deepread]] |
| **Hu 2018 (TR-C)** | gate candidate #3: **Colocation Quotient** (per-type spatial overrepresentation, Monte-Carlo significance, network-distance, MAUP-aware) — ties to Phase-1 spatial/Cramér's-V assets | **deep-read (2026-06-18)** — [[TR-C-deepread]] |

---

## Links

- `PLAN.md` — the Phase 3 reading plan (journals, keywords, tiers)
- `../PHASE2/positioning-memo.md` — the superseded CRM/LLM memo (audit trail)
- `../PHASE1/wiki/progress/NEW_FIX_PROF.md` — the segment/significance design that survives
