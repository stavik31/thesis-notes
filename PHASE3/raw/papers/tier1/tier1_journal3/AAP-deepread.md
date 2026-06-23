# AAP (Tier 1, Journal 3) — Phase-3 Sweep Deep Reads

**Read:** 2026-06-19 (Opus). Two full-text promotions from the `motorcycle crash risk segment`
keyword. These are the *new* Phase-3 AAP reads — distinct from the carry-over AAP deep reads
(Gao 2024 / Wei 2024 / Wang 2025) in [[AAP-deepread]] (`carry_over/`).

Both are **niche / structural** papers: one supplies real-data evidence on what happens to count
statistics when you slice crashes to a *single vehicle type at segment level* (the feasibility
question); the other supplies the closest existing **per-vehicle-type → route-risk → ranked-routes**
pipeline in the corpus.

---

## 1. Pathivada, Banerjee, Haleem, Khan & Justice 2025 — *Modeling motorcycle crash frequency on rural multilane segments in Kentucky* (AAP 218:108085)

**Role: `niche-premise` + `method-borrow (count model)` + feasibility data point.**

### What they did
Built **motorcycle-specific Safety Performance Functions (SPFs)** on rural multilane segments in
Kentucky, KYTC crash data 2015–2022, split **pre-COVID (2015–19)** and **post-COVID (2020–22)** —
trend break justified by monthly-trend plots + LRT. Segmented roads into **homogeneous segments**
(a segment ends where area type / roadway type / # lanes / posted speed / AADT changes) → 277
(pre) and 173 (post) segments. Crashes aggregated to segments. 323 / 177 motorcycle crashes total.
75/25 calibration/validation split. GOF: deviance, AIC, BIC, McFadden pseudo-R², LRT; prediction:
MAD, MSPE.

### The finding that matters most to the thesis — **per-type count statistics flip**
Motorcycle-only segment crashes were **UNDER-dispersed** (variance < mean). This is the *opposite*
of aggregate STATS19 crashes, where Gao found **over-dispersion + ~96% zero-inflation**. NB (the
default crash model, and Gao's lineage) **cannot handle under-dispersion** — it is built for
over-dispersion only. They therefore used:
- **Conway–Maxwell–Poisson (CMP):** generalises Poisson with a dispersion parameter ν; ν>1 =
  under-dispersion, ν<1 = over-dispersion. One flexible family covering both regimes.
- **Heterogeneous CMP (HTCMP):** lets ν vary **per segment** as ln(ν)=γ·ψᵢ (ψ = site features).
  HTCMP beat CMP on every GOF + prediction metric, both periods → the dispersion really does vary
  with road features (right shoulder width, cable median, flat terrain were significant *in the
  dispersion part*).

**Why this is load-bearing for Open Decision #6 (per-type density / feasibility):** it is the first
*real-data* signal of what the per-type slice does to the count distribution. The thesis cannot
assume Gao's ZITD (zero-inflated Tweedie, tuned for over-dispersed aggregate) carries over to a
motorcycle-only or HGV-only surface — the dispersion regime can **flip to under-dispersion**, which
demands a CMP-family model instead. *Caveat:* they **controlled** the zero share — only ~20% of
segments were zero-motorcycle-crash (zeros "randomly collected … to develop valid SPFs"). So this is
not a clean read on STATS19's true per-type zero-inflation; it shows the **non-zero** count regime is
under-dispersed once you condition on motorcycles. The probe still has to measure STATS19's actual
per-type zero rate at our chosen segment definition.

### Borrowable
- **CMP / HTCMP as a per-type count model** — the candidate engine when a vehicle-type slice is
  under-dispersed (complements, doesn't replace, Gao's ZITD for the over-dispersed/zero-heavy case).
  Design rule emerging: *choose the count family per-type after measuring its dispersion*, don't
  assume one family network-wide.
- **Empirical Bayes (EB) high-crash-location ranking** — they rank segments by *higher-than-expected*
  crashes (EB corrects regression-to-the-mean using the SPF dispersion parameter; HSM 2010). EB
  rankings differed materially from raw frequency / crash-rate rankings. → an HSM-standard
  **significance/network-screening gate candidate** alongside Wei (case-crossover), Wang (χ²-BN),
  Hu (CLQ). EB is the most "official"/defensible of the four for a per-segment risk surface.
- **Homogeneous segmentation by feature-change** — a concrete, simple answer to Open Decision #2
  (segment definition): cut where road class / lanes / speed / AADT changes. Cheap and HSM-aligned.
- **AADT as exposure** (entered as offset Eᵝ in the count model) — but it is *aggregate* AADT, not
  motorcycle AADT → exactly the **per-type exposure confound** the thesis flags (Open Decision #6
  sub-risk). They normalise crashes by all-traffic AADT, so "motorcycle risk" here still partly
  tracks motorcycle *volume*. DfT AADF-by-vehicle-type is what would fix this for us.

### Gap-test contribution
A motorcycle-specific segment SPF exists and ranks high-crash segments — but it (a) is
single-type (no cross-type comparison / divergence), (b) does **not route**, (c) uses aggregate
exposure. So it confirms the *risk-layer* half is buildable per-type, and leaves the
**type-divergence + routing** combination wide open. `niche-premise` ✓ (motorcycle segment risk is
real and modellable), not `niche-proof` (no claim that motorcycle hotspots ≠ car hotspots as places).

---

## 2. Barabino, Bonera, Maternini, Olivo & Porcu 2021 — *Bus crash risk evaluation: an adjusted framework and its application in a real network* (AAP 159:106258)

**Role: `structural-precedent` — the closest existing per-vehicle-type → route-risk → ranked-routes pipeline in the corpus.**

### What they did
A framework to score **crash risk per transit route** for one vehicle type (buses), applied to CTM
Cagliari (Italy): 23 routes, 892 crash records 1997–2001. ISO-39001 RTSMS framing. The core is an
adjusted **Fine (1971) risk index**:

> **Rₗ = Hₗ · Vₗ · Eₗ**  (risk = frequency × severity × exposure, per route *l*)

- **Hₗ (frequency):** GLM/**negative-binomial**, crash count as a function of exposure (multiplicative
  offset **Eᵝ**) and intermediate "outcome factors" (context / infrastructure / organisation / vehicle
  / driver / passenger). Deviance-ratio GOF.
- **Vₗ (severity):** **binary logistic** — P(severe) with severity collapsed to {material-damage=0,
  injury/fatality=1} *because fatalities are too rare to model as their own class*. Read via odds ratios.
- **Eₗ (exposure):** passenger·km per route (by season / day-type).
- **Aggregation:** compute R per **homogeneous section** (leg between consecutive stops / constant
  road config), then **sum sections → route risk**. Then rank all routes and cut at quartiles
  (Q1/Q2/Q3) into a **4-level risk scale R1 (max) … R4 (low)**.

### Why it's the structural precedent
This is *exactly the output shape the thesis targets* — a per-vehicle-type risk that fuses
frequency + severity + exposure into **one route-level scalar** and **ranks routes** — already built
and validated for buses. The thesis re-points the same skeleton:
- **single type → contrast across types** (bus-only here; motorcycle vs HGV vs car for us),
- **fixed operator routes → arbitrary O–D candidate routes** (their 23 service routes vs our router's
  alternatives — this is the gap; their "routing" is screening existing lines, not path-finding),
- **section-sum aggregation** = directly reusable: it's the same "route risk = Σ segment risk along
  the path" that Sarraf's WCR and Sohrabi & Lord's survival-product also use, expressed as H·V·E.

### Two extra bricks
- **Severity-by-third-party-vehicle-type heterogeneity (niche-adjacent):** in the severity model,
  vs a car-involved bus crash, **without-collision** crashes raised severity odds **219×**,
  **pedestrian** 44×, **2/3-wheeler 2.16×**, **heavy-vehicle 1.91×**. i.e. *the other vehicle's type
  materially changes crash outcome* — a (third-party-side) vehicle-type-heterogeneity signal. Not the
  focal-vehicle-class spatial claim the niche needs, but one more "vehicle type matters" data point.
- **Rare-fatality handling = binary severity collapse** — a clean, citable precedent for STATS19's
  ~1.5% fatal sparsity: don't model fatal as its own class, fold to severe/not-severe. Cheaper than
  Gao's ZITD tail for the *severity* leg specifically.

### Limitations / where it stops
Their own DB lacks focal vehicle type/driver detail; severity priority lane result is
counter-intuitive (contraflow lanes); crash locations are street-name-only (coarse spatial). And
crucially it is **screening 23 known lines, not routing** — no path generation, no O–D, no shortest-
vs-safest trade-off. So it's the *risk-scoring-and-ranking* spine, not the *router*. Sarraf + Mansoor
remain the routing mechanism; Barabino donates the **H·V·E risk decomposition + section-sum +
quartile risk scale**.

---

## 3. Lee, Yasmin, Eluru, Abdel-Aty & Cai 2018 — *Analysis of crash proportion by vehicle type at traffic analysis zone level: A mixed fractional split multinomial logit modeling approach with spatial effects* (AAP 111:12–22)

**Role: `niche-premise (STRONG — the spatial-divergence brick)` + `method-borrow (EPP screening by vehicle type)`.**
**Read: 2026-06-22 (Opus). Full text. Promoted from the `motorcycle crash hotspot` spatial-divergence keyword.**

### Why this one matters more than the other two
Pathivada and Barabino confirm a per-type *risk surface is buildable* but are both **single-type** — neither
shows that *different vehicle types are risky in different places*. That cross-type spatial-divergence claim is
the **load-bearing premise** of the whole thesis (if motorcycle hotspots = HGV hotspots as places, type-aware
routing produces identical routes → null result). **This is the first paper in the entire Phase-2/Phase-3 corpus
that states that claim with real data.**

### What they did
Modeled the **proportion of crashes by vehicle type** (not frequency) across **8,129 Traffic Analysis Zones**
covering the entire state of **Florida** (FDOT CARS crash data, 2010–2012), across **8 vehicle types**: passenger
car, van, light truck, medium & heavy truck, bus, motorcycle, bicycle, pedestrian. Method = **mixed multinomial
logit fractional split model** (dependent variable = a vector of proportions per TAZ summing to 1; each type has a
propensity equation; compensatory — a variable that raises one type's share lowers others'). The mixing collapsed
(no significant unobserved heterogeneity) → effectively an MNL fractional split. Explanatory vars: socio-demographic,
land-use, roadway/traffic, commuting.

### The finding that is the brick
After fitting, they ran a **statewide screening by vehicle type** and mapped the hot zones for each type (Fig. 2).
The conclusion, in their words:

> *"the spatial pattern of hot zones is **substantially different** across the various vehicle type crashes."*
> *"the spatial pattern of hot zones varies considerably across the various vehicle types."*

And the concrete per-type geography (their Section 5):
- **Light truck** hot zones → rural areas.
- **Medium & heavy truck** → concentrated in central & south **rural** areas.
- **Bus** → **urban/suburban**.
- **Motorcycle** → typically **rural** areas.
- **Bicycle** → large **metropolitan** areas (rural relatively safe).
- **Pedestrian** → **urban/suburban** (residential).

→ HGV-risky zones and bicycle/pedestrian-risky zones are **different places**. That is exactly the
"different segments are risky for different types" divergence the niche needs, demonstrated empirically.

### The method brick — EPP (Excess Predicted Proportion)
Their screening measure, **analogous to the HSM's Excess Predicted Average Crash Frequency** but for proportions:
**EPP = observed proportion − predicted proportion** of a given vehicle type in a zone. Positive EPP = the zone has
*more of that vehicle type's crashes than the model predicts* → a hot zone **for that type**. Rank all zones by EPP
per type, classify into Hot / Not (they used a percentile cut). This is a **per-vehicle-type significance/screening
gate** that is HSM-aligned — joins EB (Pathivada), CLQ (Hu), case-crossover (Wei), χ²-BN (Wang) on the gate
shortlist. Crucially EPP is *inherently per-type and divergence-revealing* — it directly produces the
"which zones are over-represented for type m" map the thesis wants.

### Borrowable
- **The divergence premise itself** — citable as: *vehicle-type crash hot zones are spatially distinct
  (Lee et al. 2018)*. This is the one external citation that supports the niche before we even run our own probe.
- **EPP screening** — adopt/adapt as the per-type over-representation gate (observed − predicted proportion), or as
  a cross-check on CLQ. Note it needs a fitted proportion model; CLQ is model-free, so they're complementary.
- **The 8-type taxonomy + proportion framing** — a precedent for treating vehicle type as a categorical partition
  of crashes at a spatial unit.

### Limitations / where it stops (and why the thesis still has wide-open space)
- **Macro-level (TAZ), not segment/route.** Zones are large planning units, not road segments — it screens *areas*,
  not the *links* a router traverses. The thesis must reproduce the divergence at **segment** resolution (finer →
  sparser → the feasibility risk of Open Decision #6 bites harder). Their own limitation note: proportions can
  mis-identify zones with very few crashes → they suggest **coupling a count model (total crashes) with the
  proportion model**. That coupling is essentially what the thesis does (count engine + per-type screening).
- **Proportion, not risk; no exposure-normalised per-type rate.** A high motorcycle *proportion* in rural Florida
  partly reflects where motorcycles *are*, not just where they're dangerous — the per-type exposure confound again.
- **No routing.** It's screening/planning support, not path-finding. Engine-side, like Jiang/Gao/Pathivada.
- **Compensatory structure** — one type's share up forces others' down; a modelling artifact to keep in mind, and
  a reason CLQ (which doesn't impose closure) is an attractive parallel tool.

### Gap-test contribution — the niche is no longer premise-less
This **upgrades the niche from `analogical premise` to `demonstrated premise`**: there now exists real-data evidence
(statewide, 8 vehicle types) that vehicle-type crash hot zones diverge spatially. The thesis's job shifts from
*"does this divergence exist?"* (Lee says yes at TAZ level) to *"does it hold at **segment** level on **STATS19/GB**,
and can a router **exploit** it?"* — both still open, both ours. Lee gives the premise external support; the
**segment-resolution + routing** combination remains unoccupied.

---

## Net effect on the thesis (all three papers)

1. **Count model is now a per-type decision, not a default.** Gao's ZITD ≠ guaranteed for a type
   slice — Pathivada shows under-dispersion can appear, needing **CMP/HTCMP**. → measure dispersion
   per type in the probe, pick the family accordingly. (Feeds Open Decision #6 + the engine choice.)
2. **A complete per-type route-risk scalar already exists (Barabino H·V·E).** Adopt the decomposition
   and the section-sum + quartile-ranking; the thesis's additions are *cross-type contrast* and
   *arbitrary-O–D routing*, which Barabino lacks → the gap is sharper, not weaker.
3. **EB + EPP join the significance/screening-gate shortlist** (with Wei / Wang / Hu-CLQ). EB
   (Pathivada) is the HSM-standard option for ranking a per-segment risk surface; **EPP (Lee) is
   inherently per-type** — observed − predicted *proportion* per vehicle type — and is the most
   directly divergence-revealing gate after CLQ.
4. **The niche premise is now externally supported, not just analogical (Lee 2018).** Vehicle-type
   crash hot zones are demonstrated to diverge spatially (statewide Florida, 8 types). The thesis's
   open question narrows to *segment-resolution + GB/STATS19 + routing exploitation* — the divergence
   itself no longer has to be assumed.
5. **Exposure confound reconfirmed three times:** all three use *aggregate* exposure (AADT /
   passenger·km) or raw proportion. The thesis's per-type exposure (DfT AADF by vehicle type) is what
   distinguishes per-type *risk* from per-type *volume* — still an open data-availability check.

## Links
- [[AAP-abstract-refs]] — this journal's Phase-3 sweep record (keyword 2)
- [[AAP-deepread]] (`carry_over/`) — Gao/Wei/Wang carry-over deep reads (engine + gate ancestors)
- [[TR-C-deepread]] — Sarraf/Mansoor routing mechanism + Hu CLQ gate
- [[positioning-memo]] — evidence map · [[PLAN]] — keyword clusters
- [[2026-06-18-where-we-stand-and-remaining-gaps]] — Open Decision #6 (per-type density/exposure)
