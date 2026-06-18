# TR-Part-C — Phase 3 Reading-Pass Record (Tier 1, Journal 2)

**Journal:** Transportation Research Part C: Emerging Technologies (Elsevier) — the routing /
algorithms **home**, untouched in Phase 2. First time the safe-route-planning literature actually
shows up by title.

**Pass:** 2026-06-18, risk-aware-routing + vehicle-type-niche direction.
**Keywords:** `safe route planning` (1/3, done) · `risk-based navigation` (2/3, done) ·
`crash risk routing` (3/3, **done**). (`safe route planning` re-phrased from the ambiguous
`safe routing`, which on a networking-indexed search returns VANET secure-packet-routing.)
**TR-C sweep complete (all 3 keywords).**

**Keyword-1 result:** large list, mostly VRP / drone-UAV / rail / maritime / air-mobility / eco-EV
routing noise (skipped). **8 safe-routing abstracts pulled → 3 promoted to full-text, 3 abstract-only
keepers, 2 skip-logged.**

**Keyword-2 result (`risk-based navigation`):** ~90% maritime / aviation-ATC / UAV-airspace /
AV-motion-planning / detection noise. 2 strong abstracts pulled → **1 full-text keeper, 1 downgraded.**
- ✅ **Safety-based path finding in urban areas for older drivers and bicyclists** (Chandra 2014) —
  **deep-read 2026-06-18 → [[TR-C-deepread]].** Multi-objective shortest path on **cost = safety + travel time**,
  conditioned on **road-user category** (older drivers, bicyclists); safety indicators from traffic
  (speed/density) + **driver attributes (perception-reaction time)** + street attributes (length,
  tire-road friction) — **no historical crash data required** (crash-data-free risk layer, cf.
  Mansoor's Dijkstra-2013 score). College Station, TX. **Gap-strengthening nuance:** abstract states
  the indicators are *"generic irrespective of the type of road user"* → it is user-**motivated** but
  not user-**conditioned** in the risk layer (personalisation = tuning driver PRT, not a per-type risk
  surface). So even the paper built for vulnerable road users does NOT compute per-type crash risk →
  the data-driven per-vehicle-type risk surface remains unoccupied. Tag: `niche-adjacent / home / method`.
- ✗ **Adaptive vehicle routing for risk-averse travelers** — DOWNGRADED. "Risk" = **travel-time
  reliability** (prospect theory, on-time arrival), not crash. Off-core; at most a one-line method cite
  for risk-averse / prospect-theory routing. (Relevant instead to the *time*-optimization axis — see
  note below.) Tag: `skip (travel-time reliability, not crash)`.

**Keyword-3 result (`crash risk routing`):** mostly returns crash-risk **prediction** (the Abdel-Aty /
Quddus real-time-crash-modelling lineage — engine-side, already covered by Gao) + AV-control / driver-
behaviour noise. Most routing-on-crash-risk hits were **already deep-read** (Mansoor, Sohrabi & Lord,
Kavta, Chandra) or already kept (Dijkstra, kw1). **2 new keepers → 1 full-text, 1 abstract.**
- ✅ **Where are the dangerous intersections for pedestrians and cyclists: A colocation-based approach**
  (Hu, Zhang, Shelton 2018) — **deep-read 2026-06-18 → [[TR-C-deepread]].** **Correction on full read:** the
  results **combine** ped+cyclist and condition on **severity × intersection-type** (not ped-vs-cyclist
  separation, not motor-vehicle classes) → premise is **analogical, not direct.** The prize is the
  **method: Colocation Quotient (global GCLQ + local LCLQ)** = a per-category **spatial significance gate**
  ("does crash-type A significantly colocate with feature-type B vs random?", expected value 1, Monte-Carlo
  p-values, network-distance, micro-level/MAUP-aware). Directly a candidate **significance gate** + input to
  the **segmentation** decision, and **the tool by which the thesis can generate its own spatial-divergence-
  by-type evidence on STATS19.** Tag: `method (per-type spatial significance gate / segmentation) / niche-
  evidence (analogical)`.
- ✓ **Speed limits, speed selection and network equilibrium** (Yang, Ye, Zhao 2015) — abstract-only keeper.
  **Class-specific crash risk in route + speed choice at equilibrium** — a *predecessor to Mansoor 2026* in
  the heterogeneous-user crash-risk-equilibrium lineage, adding the **speed→crash** mechanism (Nash
  equilibrium of speed choice). Classes by risk perception, not vehicle type. Cite as lineage ancestor;
  Mansoor is the fuller recent version → no full text needed. Tag: `home / method (equilibrium lineage)`.
- *Skip-noted:* #42 LIFT (truck driving risk via fine-tuned LLMs) — has "truck" (vehicle type) but is
  *driver*-level + the cut LLM direction → wrong level; confirms truck-specific risk is an active thread.

> **Gap-test brick (kw3):** `crash risk routing` returns crash-*prediction*, not *routing* — the routing-
> side literature is genuinely thin and largely already found. Still **no motor-vehicle-class routing**;
> the only per-type spatial signal is Hu 2018 (ped/cyclist). The crash-risk-equilibrium + spatial-crash
> lineage runs 2010–2015 with Mansoor 2026 as the capstone → an *established* field with vehicle type as
> the unfilled slot.

> **Note (time-optimization axis, flagged 2026-06-18):** the corpus's math-heavy *time + safety joint*
> optimization is anchored by **Mansoor 2026** (METT+MECRC, variational inequality) + **Sarraf 2020**
> (MCDM time+safety+distance) + the hazmat CVaR/bicriterion borrow. The standalone routing-optimization
> literature (multi-objective / Pareto / time-dependent / stochastic shortest path) is **not yet swept
> as its own pillar**; two reliability cousins surfaced unpulled ("Path finding under uncertainty…",
> "Adaptive vehicle routing for risk-averse travelers"). Decision pending: is routing optimization a
> *contribution* (→ add a routing-optimization keyword cluster) or a *borrowed component* (→ Mansoor +
> Sarraf suffice)?

---

## Promoted to FULL-TEXT — ✅ DOWNLOADED & DEEP-READ (2026-06-18 → [[TR-C-deepread]])
*(all 3 now read in full; technical grounding in the deep-read record)*

1. **Modeling safety reliability and unreliability in a mean-excess network equilibrium framework:
   Heterogeneous users with safety-conscious route choice sets** — ★ **structural ancestor of
   per-type routing.** Network equilibrium / variational inequality with **class-specific route
   choice sets**, routes scored by roadway characteristics, **crash-risk-cost distribution** + the
   severe-crash tail via α-reliable **mean-excess** (CVaR family). Classes are by *safety
   preference*, not vehicle type — but the machinery transplants directly onto vehicle type. Tag:
   `home / method`. **This is the keystone find of the pass.**
2. **Navigating to safety: Necessity, requirements, and barriers to considering safety in route
   finding** — ★ home + quantified motivation. Texas, 29,000+ segments: shortest ≠ safest, cutting
   travel time **8% → +23% crash risk**; safest route **varies by weather** (secondary axis). Names
   our exact requirements (real-time data, better crash prediction, time–safety tradeoff method).
   No vehicle type → gap brick. Tag: `home / motivation`.
3. **Estimating the value of safety against road crashes: A stated preference experiment on route
   choice of food delivery riders** — ★ **demand-side niche brick.** Amsterdam/Copenhagen SP study:
   a specific vehicle class (bike/e-bike **riders**) will choose safer-but-longer routes; quantified
   Value of Risk Reduction / WTA. Justifies that *a vehicle class wants type-specific safe routing*
   (distinct from "risk differs by type"). Behavioural/SP, not an algorithm. Tag: `niche-adjacent /
   demand justification`.

## Abstract-only keepers (cite; no full text needed)

- **Tradeoffs between safety and time: A routing view** — minimal bi-attribute (travel-time vs
  collision-count) routing on NYC collision data; the lightweight version of Sarraf's MCDM tradeoff.
  Tag: `home / method (lightweight)`.
- **Assessing the safety of routes in a regional network** — NL "Sustainable Safety" vision: the
  *quickest route should equal the safest route*; conflict-surrogate, micro-sim, older. Tag:
  `home (historical) / related-work`.
- **Routing hazardous materials on time-dependent networks using conditional value-at-risk** —
  representative of the **risk-averse routing** borrow (CVaR over time-dependent accident
  probability × consequence; optimal departure + route, Buffalo NY). Same severity-tail family as
  the mean-excess paper above. Tag: `borrow (method)`.

## Skip-logged (abstract read, not cited unless a method is adopted)
- **A decision support system for integrated hazardous materials routing and emergency response** —
  older multi-criteria hazmat DSS (Greece); #CVaR paper already represents the cluster.
- **Solving the bicriterion routing and scheduling problem for hazardous materials distribution** —
  older bicriterion (cost+risk) time-dependent hazmat routing; supporting only.

## Gap-test synthesis (the strongest brick of the pass so far)
Across **8 safe-routing papers spanning ~2008–2024, none route by vehicle type.** The food-delivery
paper is about riders but is behavioural SP, not a per-type routing algorithm; the mean-excess paper
has heterogeneous classes but by *preference*, not *vehicle*. → The safe-routing home is a **15+-year-
old field that still has no vehicle-type conditioning**, and the **mean-excess paper hands over the
exact mechanism** (class-specific route sets + crash-risk-cost tail) to fill it, re-keyed on vehicle
type. Confirms the white space and supplies the method to occupy it.

## Links
- [[T-ITS-abstract-refs]] — Tier 1, Journal 1 sweep (0 keepers; gap brick)
- [[ESWA-deepread]] — Sarraf router (the MCDM cousin of these tradeoff papers)
- [[PLAN]] · [[positioning-memo]] · [[2026-06-18-where-we-stand-and-remaining-gaps]]
