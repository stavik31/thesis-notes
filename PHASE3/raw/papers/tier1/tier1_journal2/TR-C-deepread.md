# TR-Part-C — Deep-Read Record (Tier 1, Journal 2)

**What this is.** Full-text deep reads of the 3 papers promoted from the keyword-1 (`safe route
planning`) abstract sweep — see [[TR-C-abstract-refs]]. These are the first papers from the routing
*home* read in full this pass. Two layers per paper: **Context grounding** (where it places the
thesis) + **Technical grounding** (machinery; borrow vs. replace).

**Headline:** the routing home now has three solid pillars — a **conceptual ancestor** that hands us
the exact per-type mechanism (Mansoor mean-excess), an **operational sibling** on real crash data
with weather conditioning (Sohrabi & Lord), and a **demand-side niche brick** proving a vehicle class
will trade time for safety (Kavta riders). **None condition on vehicle type** — and the newest of
them (2026) doesn't even list it as future work. Gap confirmed and the mechanism to fill it located.

---

## Mansoor, Li, Chen 2026 — Mean-excess network equilibrium with safety-conscious class-specific route choice sets (HK PolyU) ★★★ STRUCTURAL ANCESTOR OF PER-TYPE ROUTING

### Context grounding
The single most important routing-home find of the pass. It models **class-specific route choice
sets** — each traveler *class* sees a different set of acceptable routes — inside a network-
equilibrium framework. That class-specific-choice-set machinery is **exactly the mechanism the
thesis needs**, just re-keyed: their classes are by **safety preference** (cautious vs. indifferent);
ours would be by **vehicle type** (motorcycle vs. HGV vs. car). Two pointers make the gap vivid:
- It **names heavy vehicles as a risk factor in its own motivation** — *"routes that have a higher
  probability of severe crashes, such as those with more truck volume or high-speed vehicles"* and
  *"avoiding routes with high probabilities of severe outcomes … such as crashes involving heavy
  vehicles"* — yet conditions on preference class, not vehicle type.
- Its **future work** lists more roadway attributes, continuous bicriteria (infinite classes),
  empirical preference studies, CRC-distribution validation — **vehicle type is not even mentioned.**
  So in the most recent (2026) safety-routing-equilibrium paper, the vehicle-type axis is wholly absent.

One scale caveat for honesty: this is **network equilibrium / traffic assignment** (how system flows
distribute when everyone routes), *not* an individual O–D navigation recommender. So it's the
**conceptual / heterogeneity-modelling ancestor**, while Sarraf ([[ESWA-deepread]]) remains the closer
*operational* router. The thesis borrows the *mechanism* (class-specific sets + severity tail) from
here and the *operational route-ranking* from Sarraf.

### Technical grounding
- **Route safety score from roadway characteristics (Dijkstra-2013 method) — borrowable, crash-data-
  free.** Four criteria per route: share of **local roads**, share of **collector roads**, total
  **distance** (VKT = crash exposure), **intersection density** (junctions = serious/fatal hotspots).
  Each min–max normalised to [0,1], **equal-weighted (0.25)** → unsafety score `US = Σ score_c·γ_c`
  → safety score `Θ = (1 − US)·100`. This is a **supply-side route-safety score from road topology
  alone — no crash counts needed.** Worth keeping as a cheap baseline / complement to a Gao-style
  crash-data engine (and as a per-type score if local/collector/junction risk weights are set per
  vehicle class).
- **Class-specific choice set (the mechanism):** route `p` enters class `m`'s set iff `Θ_p ≥ Θ_req^m`
  — a per-class **safety threshold**. Demo: indifferent class (Θ_req=0%) sees all routes; conscious
  class (Θ_req=40%) sees only the safe subset. **Re-key Θ_req on vehicle type → per-type route sets.**
- **Crash risk cost (CRC) distribution per link:** mean μ (flow/speed-dependent via the Elvik 2004
  crash-risk model) + variance σ² (driver/environment/weather uncertainty); route CRC ~ Normal by CLT
  (assumes independent links — correlation left to future work).
- **Mean-excess CRC (MECRC) = the CVaR move for crash severity.** Generalised cost = **METT (mean-
  excess travel time) + MECRC**, joined by converter Λ. MECRC = effective CRC (mean + safety margin at
  confidence α, ensuring frequent safe arrival = *reliability*) **plus the tail beyond it** (extreme
  crash cost = fatal/serious = *unreliability*). This directly handles **the fatal-class tail** that is
  our central imbalance concern (cf. Gao's ZITD, [[AAP-deepread]]) — but on the *routing* side.
- **Solution:** variational inequality, two-stage algorithm (stage 1 = build per-class choice sets;
  stage 2 = solve equilibrium). Numerical tests on small + real networks.

**Borrow:** (1) **class-specific choice sets keyed on a per-class threshold** → the per-vehicle-type
routing mechanism; (2) the **Dijkstra-2013 roadway-characteristic safety score** as a cheap,
transparent, crash-data-free route-safety layer (potentially per-type-weighted); (3) **mean-excess /
CVaR** to make routing averse to the fatal-crash tail. **Tag: `home / method (keystone)`.**

---

## Sohrabi & Lord 2022 — Navigating to Safety: necessity, requirements, barriers to safety in route finding (Texas A&M) ★ OPERATIONAL HOME + MOTIVATION

### Context grounding
The operational sibling of Jiang+Sarraf, on **real crash data at scale**: it asks "are the shortest
routes nav apps give actually safe?" and answers no. **Quantified motivation stat for the thesis
intro:** cutting travel time **8% raised crash risk 23%**; the safest route **changes with weather**;
road curves carry **+30% crash rate in adverse weather**. Proposes an **S-RGS** (safety-based route
guidance system) architecture (static + dynamic) as an add-on to shortest-path routing, and lists the
requirements it needs — *real-time data, accurate crash-prediction models, a time–safety tradeoff
method* — which is essentially the thesis's build spec. Co-authored by **Dominique Lord** (a crash-
statistics heavyweight; also on the Phase-2 Li 2025 multimodal paper). **No vehicle-type conditioning**
— road functional class is a feature, vehicle class is not → gap brick.

### Technical grounding
- **Data/segmentation:** Texas 5-city network, **29,382 homogeneous road segments** (segmented by
  alignment/lanes/median/shoulder/lighting via the **ROCA** curvature GIS tool); TxDOT CRIS crashes
  2015–17 + roadway inventory + Iowa-Mesonet weather.
- **Crash model:** **Negative Binomial** crash-frequency regression (handles over-dispersion) — and
  crucially **two separate models, adverse vs. clear weather.** This validates **condition handling by
  model stratification** (a clean alternative to weather-as-a-feature) for our secondary axes. Adverse-
  weather crash rate was **2.7× clear**; ~53% of crashes intersection-related.
- **Route risk aggregation (borrowable, distinct from Sarraf's WCR sum):** route crash probability =
  complement of the **product of per-segment survival (no-crash) probabilities** along the route — a
  clean probabilistic accumulation of segment risk into a route score. Then safest vs. shortest compared
  per O–D.
- **Evaluation:** NB GOF via AIC; prediction via MAE/RMSE; the headline is the safest-vs-shortest
  divergence and its weather sensitivity.

**Borrow:** weather-**stratified** NB segment models (precedent for separate-model-per-condition on the
secondary axes); the **survival-probability route aggregation**; the homogeneous-segmentation approach;
and the **8%/23% tradeoff stat** for motivation. The S-RGS requirement list doubles as a thesis spec.
**Tag: `home / motivation / engine-precedent (real crash data + weather)`.**

---

## Kavta, Sharif Azadeh, Maknoon, Wang, Correia 2025 — Value of safety against road crashes: SP route choice of food delivery riders (TU Delft + Just Eat Takeaway) ★ DEMAND-SIDE NICHE BRICK

### Context grounding
The niche's **demand-side** justification — distinct from the supply-side "risk differs by type." It
shows a **specific vehicle class** (bike/e-bike/moped **riders**, a rising, vulnerable group: 25–35% of
riders crash-involved; 39% in a Milan study) **will choose safer-but-longer routes** when nudged. So
the thesis's premise isn't only "different types face different risk" — it's also "**a type wants
type-specific safe routing and will act on it.**" Industry co-author (Just Eat Takeaway) signals real
demand. Notably names *"vehicle mix"* among rider crash-risk factors — vehicle type as a risk lens,
again acknowledged but not built into routing.

### Technical grounding
- **Method:** Stated Preference (discrete choice) experiment with riders in **Amsterdam & Copenhagen**;
  hypothetical shorter-route vs. longer-safer-route choices; two intervention arms — **safety
  information** and **monetary incentives**.
- **Route choice model** yields two quantified indicators: **Value of Risk Reduction (VRR)** and
  **Willingness to Accept (WTA)** — how much time/compensation riders trade for crash-risk reduction.
  Working arrangements + socio-demographics significantly shift choices.
- Behavioural/demand study — **not** an algorithm or a risk surface; nothing to borrow for the build
  itself.

**Borrow:** the **VRR/WTA framing** and the finding itself as **niche motivation** — evidence that a
vehicle-class-specific safe-routing product would be valued and adopted (useful for the "why this
matters" chapter and any adoption/evaluation argument). **Tag: `niche-adjacent / demand justification /
motivation`.**

---

---

## Chandra 2014 — Safety-based path finding in urban areas for older drivers and bicyclists (Texas A&M Transportation Institute) ★ CLOSEST USER-CONDITIONED PRECEDENT (but parametric, not data-driven) — *from keyword 2 `risk-based navigation`*

### Context grounding
The closest precedent yet to **routing conditioned on a road-user category** — it builds safe path-
finding explicitly for **two user types** (older drivers in cars; bicyclists). 2014 novelty claim:
*"no single research up till date evaluates safety performance of streets and intersections in a
shortest path finding paradigm."* So it's a historical anchor for safe-routing itself.

**But the deep read reveals the crucial nuance that sharpens — not threatens — the thesis:** the two
user types differ **only parametrically**, via **two knobs**: operating *speed* and *perception-
reaction time* (older driver = high PRT; bicyclist = 1 s PRT + low speed). The safety indicators
themselves are **generic / analytical** — *"actually generic irrespective of the type of road user."*
There is **no per-type risk surface and no crash data**: risk is a **Time-To-Collision proxy derived
analytically from traffic density**, explicitly *"used as proxy to safety … when there is absence of
satisfactory crash data."* So it is user-**motivated** but only **parameter-conditioned**, not
**data-conditioned**.

**Why this strengthens the niche (three ways):**
1. **Gap brick:** even the paper *built for* vulnerable road-user categories does **not** compute a
   data-driven per-type crash-risk surface — it tunes driver PRT/speed. The data-grounded per-vehicle-
   type risk surface remains unoccupied across the whole pass.
2. **Contrast that defines the contribution:** Chandra is the *opposite design philosophy* to the
   thesis — he **avoids** crash data (analytical TTC), we **exploit** it (STATS19 has vehicle type on
   every record). Our novelty crystallises against his: *real per-type crash history*, not a driver-
   parameter knob. It also shows per-type differentiation can be trivially thin (2 parameters) — our
   job is to make it **rich and empirical**.
3. **Method donor for the routing layer** (the math-heavy side flagged in the time-axis discussion).

### Technical grounding (the math-heavy core)
- **Crash-data-free safety indicator via TTC.** Street time-to-collision from vehicle spacing modelled
  as a **Poisson process** (sparse traffic → expected closest distance d_q) and a **Gaussian Unitary
  Ensemble** distribution (dense traffic → d_Q); TTC = distance / relative speed. Intersection TTC
  similar over an n-leg intersection's converging vehicles. Street/intersection **safety indicators**
  (`I_s`, `I_j`) built from these TTCs + speed/density + PRT + tire-road friction; **lower = safer**.
- **Multi-objective shortest path (MSP).** The safest-and-fastest path is a **multi-objective shortest
  path problem (NP-complete)**; he adapts a median-shortest-path formulation. **Yen's algorithm** finds
  the *p*-safest paths (complexity `O(pM(A + M log M))`); the routine then filters to the **non-inferior
  (Pareto) set** trading safety (`Z_p1`) vs travel time (`Z_p2`). College Station, TX example: car/older
  driver → cumulative safety 11.86, time 478 s; bike → 6.5, 1259.8 s (difference driven *only* by speed
  + PRT).

**Borrow:** (1) the **multi-objective / Pareto (non-inferior) shortest-path machinery** (Yen's
p-shortest-paths → Pareto filter) — a concrete, citable routing-layer optimisation for the time+safety
combination, and a "deepen-for-complexity" option; (2) the **crash-data-free analytical TTC safety
indicator** as a possible *secondary/complementary* risk layer where STATS19 per-type counts are too
sparse (graceful-fallback material). **Tag: `niche-adjacent / home / method (multi-objective routing +
crash-data-free risk indicator)`.**

---

## Hu, Zhang, Shelton 2018 — Where are the dangerous intersections for pedestrians and cyclists: a colocation-based approach (USF + Rice) ★ METHOD DONOR: per-category spatial significance gate — *from keyword 3 `crash risk routing`*

### Context grounding (with an honest correction to the keeper note)
Filed at abstract stage as the "spatial-divergence-by-type" brick. The full read **splits that claim
in two** — and the method half is the real prize:

- **Premise (weaker than the title implies):** the analysis **combines pedestrian + cyclist crashes**
  into one "vulnerable-user crash" set and conditions colocation on **crash severity** (fatality /
  injury / no-injury) **× intersection-control type** (traffic-light / stop-sign / non-controlled). It
  does **not** separate ped vs cyclist in the results, and these are vulnerable *non-motorized* users
  contrasted with the motor-vehicle baseline — **not** motor-vehicle *classes*. So as direct
  "motorcycle-hotspots ≠ HGV-hotspots" evidence it is **analogical, not direct.**
- **Why the gap being thin is now better understood:** the authors state this is *"the first effort to
  extend colocation analysis into the transportation safety field."* So nobody has shown spatial
  divergence *by vehicle type* partly because the **spatial tool itself is recent (2018)** and was
  never applied per-vehicle-class for routing. That's a *defensible* niche position, not a dead end:
  **the thesis can generate its own spatial-divergence-by-type evidence by running this method on
  STATS19 per vehicle type** — the paper hands over the tool to produce the missing brick.

### Technical grounding — the Colocation Quotient (CLQ) as a per-category spatial significance gate
This is the strongest **significance-gate / spatial-method** find of the pass, and it ties straight to
the Phase-1 spatial/Cramér's-V assets.

- **What CLQ measures:** unlike spatial *autocorrelation* (same-type clustering), **colocation** tests
  whether **type-A points are spatially attracted to type-B points** — i.e. *"does crash-type A
  significantly colocate with feature-type B vs. random?"* Designed for exactly multi-category questions
  (their cited crime example: residential-burglary vs robbery vs **motorcycle-theft** × land-use types).
- **Global CLQ (GCLQ):** `GCLQ_{A→B} = (N_{A→B}/N_A) / (N_B/(N−1))` — observed share of A's nearest
  neighbours that are type B, over the chance share. **Expected value = 1** under random relabelling;
  **>1 = colocation, <1 = isolation.** Significance via **Monte Carlo** (1000 relabel runs preserving
  category frequencies) → empirical p-value.
- **Local CLQ (LCLQ):** site-specific version with a **Gaussian-kernel distance weighting** (Eq. 7) →
  identifies the *individual* high-risk locations and maps them; Monte-Carlo-tested per point.
- **Two design choices directly relevant to our build:** (1) uses **street-network distance**, not
  Euclidean (crashes geocoded to the network) — correct for road data; (2) operates at the **micro
  level** (individual intersections), explicitly avoiding the **Modifiable Areal Unit Problem (MAUP)**
  that plagues zone/tract aggregation — a direct input to the **segmentation decision** (don't aggregate
  risk to coarse zones).
- **Data/results (for flavour):** 6-yr TxDOT Houston crashes (398,813 total; 98% veh-veh, 1.4% ped, 0.6%
  cyclist), 78,372 cleaned intersections. Crashes colocate **strongly with traffic-light intersections**
  (GCLQ ≈ 8.5; fatality ≈ 9.8), weakly with stop-sign (≈ 1.47), and are **isolated from non-controlled**
  (≈ 0.55). LCLQ surfaces downtown clusters + sites near schools/campuses; common factors = high speed
  limits, wide intersections, mode mix, corner bus stops.

**Borrow (high value):** **CLQ (global + local) as the per-vehicle-type SPATIAL significance gate** —
*"does motorcycle/HGV crash significantly colocate with [junction type / road class / wet-or-dark
segment] vs random?"*, network-distance, Monte-Carlo p-values, micro-level (MAUP-aware). This is a
concrete, citable instrument for both **the significance gate** (alongside Wei's case-crossover and
Wang's χ²-BN, [[AAP-deepread]]) **and the segmentation decision**, and it is the method by which the
thesis can **manufacture its own spatial-divergence-by-type evidence** on STATS19. **Tag: `method
(per-type spatial significance gate / segmentation) / niche-evidence (analogical)`.**

---

## Gap test (Phase 3) — strongest standing
Four safe-routing papers now span **2014–2026**, and **none route by a data-driven vehicle-type risk
surface.** Mansoor (a) names heavy-vehicle risk in motivation, (b) builds the exact class-specific-set
mechanism, (c) omits vehicle type even from future work. Chandra goes *furthest toward* user-conditioned
routing (older drivers / bicyclists) yet differentiates types only by **two parameters (speed + PRT)**
with **generic, crash-data-free** indicators — i.e. even the user-framed paper has **no per-type risk
surface.** So across a 12-year span the field has the routing machinery, the acknowledged vehicle risk
factor, and even user-category framing — but **nobody connects a data-driven per-vehicle-type crash-risk
surface to the router.** That connection (Mansoor's class-specific sets + crash-severity tail, re-keyed
on vehicle type, fed by a STATS19 per-type risk surface, ranked via Sarraf/Chandra-style multi-objective
routing) is the thesis, now precisely located.

## Links
- [[TR-C-abstract-refs]] — the sweep these came from (keyword 1/3); 3 abstract-only keepers
- [[ESWA-deepread]] — Sarraf router (operational route-ranking the thesis pairs with Mansoor's mechanism)
- [[T-ITS-deepread]] · [[AAP-deepread]] — engine + significance-gate ancestors (severity tail ↔ Mansoor's MECRC)
- [[positioning-memo]] — evidence map (routing home now 5 deep-read papers)
