# AAP — Phase 3 Reading-Pass Record (Tier 1, Journal 3)

**Pass:** 2026-06-19, risk-aware-routing + vehicle-type-niche direction. Lightweight per-journal
record (titles → abstracts → full-text), mirroring the Phase 2 style.

**Keywords swept so far:** `risk aware route planning` (generic, 2026-06-19) ·
`motorcycle crash risk segment` (2026-06-19).

**Keywords swept (7 done):** `risk aware route planning` (2026-06-19) ·
`motorcycle crash risk segment` (2026-06-19) · `truck/HGV crash risk` (2026-06-22) ·
`vehicle type crash heterogeneity` (2026-06-22) · `vulnerable road user crash` (2026-06-22) ·
`motorcycle crash hotspot` (2026-06-22) · *(spatial divergence keywords 7–9 pending)*.

**Pass result (all 5 keywords done): 8 abstract keepers, 2 full-text promotions (deep-read), 0 spatial-divergence papers found.**
Keywords 3–5 returned noise (severity models, behavioral studies, VRU injury papers) with a semantic
mismatch on keyword 4 (`heterogeneity` = statistical unobserved heterogeneity in AAP, not inter-class
differences). The spatial-divergence-by-type evidence base does not exist in AAP under these keywords
— the gap is real, not a search failure. Gap-test brick confirmed.

---

## Keeper (abstract-only)

- **Do motorists select safe routes over efficient routes? An empirical study using travel trajectory
  data** — *(risk aware route planning; abstract read 2026-06-19)*
  *Empirical route choice study using ALPR trajectory data from Changsha, China. Proposes a paired
  scenario comparison (PSC) method contrasting route choices across four scenario pairs
  (daytime/nighttime, work/non-work, livelihood/non-livelihood, short/long distance). Group Random
  Parameters Logit (GRPL) model with safety attributes (fewer intersections, wider roads) and
  efficiency attributes. Finds that motorists prioritise safety-attributed routes significantly
  during **nighttime trips and for non-livelihood purposes**; work/non-work and distance effects
  inconclusive. Provides empirical support for safety-oriented route planning and navigation systems.
  **Tag: `demand-side` / `related-work`.** Demand-side brick: confirms ordinary motorists do trade
  efficiency for safety (complements Kavta 2025 delivery-rider WTA result, extending it to private
  car drivers). Not a routing system; no vehicle-type conditioning; no crash-data risk surface.
  Does NOT supply routing-home or niche-premise evidence directly. Good for one related-work
  sentence on demand-side motivation.*

---

## Keyword 2 — `motorcycle crash risk segment` (2026-06-19)

### Promoted to full-text → **DEEP-READ 2026-06-19** (see [[AAP-deepread]] in this folder)

- **Modeling motorcycle crash frequency on rural multilane segments in Kentucky** (Pathivada et al.
  2025) — ✅ **deep-read.** CMP/HTCMP motorcycle-specific SPFs, pre/post-COVID, homogeneous
  segmentation, EB high-crash ranking. **Key:** motorcycle-only segment crashes were
  **UNDER-dispersed** (variance < mean) → NB/ZITD (over-dispersion) inappropriate; needs CMP family.
  First real-data signal that per-type slicing can **flip the count regime** → load-bearing for
  Open Decision #6. **Tag: `niche-premise` / `method-borrow (CMP/HTCMP, EB, segmentation)`.** Uses
  aggregate AADT exposure (per-type exposure confound). No cross-type contrast, no routing.

- **Bus crash risk evaluation: An adjusted framework and its application in a real network**
  (Barabino et al. 2021) — ✅ **deep-read.** **Rₗ = Hₗ·Vₗ·Eₗ** (NB frequency × binary-logistic
  severity × passenger·km exposure), computed per homogeneous section, **summed → route risk**,
  quartile-cut into a 4-level risk scale, routes ranked. **Tag: `structural-precedent`.** The
  closest existing per-vehicle-type → route-risk → ranked-output pipeline in the corpus (bus-only,
  fixed lines — screening not routing). Donates the **H·V·E decomposition + section-sum +
  quartile ranking** + a binary-severity collapse for rare fatalities. Third-party vehicle type
  shifts severity odds (heavy-veh 1.91×, 2/3-wheeler 2.16× vs car) = extra "type matters" brick.

### Keepers (abstract-only)

- **Identifying environmental factors related to motorcyclist crash rates: variable selection
  using spatial Random Forest with network distance and barriers** — *(motorcycle crash risk
  segment; abstract read 2026-06-19)*
  *spatialRF-NDBAR framework: spatial RF + MGWR for motorcycle crash rates, incorporating
  network-distance and physical road-barrier constraints. Taipei City, 2016–2020, POI data from
  OpenStreetMap. Best model: MGWR with spatialRF-NDBAR variables (R²=0.867). POIs (marketplaces,
  restaurants, bars, hotels, banks, transit stops) associated with higher motorcycle crash risk.
  **Tag: `niche-premise` / `method-adjacent`.** Spatial modeling of per-type (motorcycle) crash
  rates with network-distance awareness. Taipei context limits transferability (motorcycles as
  dominant mode; road barriers prohibiting access). Good for one related-work sentence on spatial
  motorcycle crash rate modeling. Not full-text.*

- **Influence of horizontally curved roadway section characteristics on motorcycle-to-barrier
  crash frequency** — *(motorcycle crash risk segment; abstract read 2026-06-19)*
  *NB regression for motorcycle-to-barrier crash frequency on curved sections, Washington State
  2002–2011. 4,915 horizontal curve sections; 329 crashes. Strongest predictor: curve radius
  (curves ≤820 ft → 10× crash frequency rate). Also significant: curve length, AADT, adjacent
  curve proximity. **Tag: `niche-premise`.** Segment-level motorcycle crash frequency model with
  geometric predictors. Very specific to barrier crashes on curves — not general motorcycle
  segment risk. One related-work sentence on per-segment motorcycle crash frequency variation.
  Not full-text.*

- **Vulnerable road users' crash hotspot identification on multi-lane arterial roads using
  estimated exposure and considering context classification** — *(motorcycle crash risk segment;
  abstract read 2026-06-19)*
  *XGBoost for pedestrian/bike exposure estimation → NB crash prediction models → PSI-based
  hotspot identification at intersections and along segments. Big data: ATSPM, Strava, CCTV,
  crash data, roadway features, land use, socio-demographics. Context classification significantly
  related to crashes. Orlando area; hotspots cluster near city center; coastal segments cold for
  bike crashes. **Tag: `method-adjacent` / `niche-premise`.** Method pipeline (exposure
  estimation + NB prediction + PSI hotspot, by road-user type) is parallel to the thesis build
  for motorcycles/HGVs. Combines pedestrians + bikes, not motor-vehicle classes. Not full-text
  but useful methodology reference for per-type hotspot identification with exposure.*

- **Assessing crash risk considering vehicle interactions with trucks using point detector data**
  — *(motorcycle crash risk segment; abstract read 2026-06-19)*
  *Individual-vehicle-level interaction metrics (headway, headway variance) from ILDs, with GM
  model for truck detection. Case-control conditional logistic regression. Truck–non-truck and
  non-truck–truck following pairs show distinct crash risk profiles under different traffic
  conditions. **Tag: `niche-premise (weak)`.** Shows truck involvement materially changes crash
  risk dynamics vs aggregate traffic. Real-time/interaction-level — not historical segment crash
  data (STATS19 approach). One sentence: trucks demonstrably create distinct crash risk patterns.
  Not full-text.*

- **The importance of flow composition in real-time crash prediction** — *(motorcycle crash risk
  segment; abstract read 2026-06-19)*
  *Logistic regression + SVM for real-time crash prediction on Santiago urban expressway.
  Disaggregated by vehicle type (light, heavy, motorcycle). Disaggregated data improves prediction
  accuracy by up to 30% vs aggregated. **Tag: `niche-premise`.** Direct empirical argument that
  vehicle-type conditioning improves crash prediction accuracy — strong one-sentence niche
  justification. Real-time/flow-based (not historical segment routing), Santiago context. Not
  full-text but a clean citation: "disaggregating crash risk by vehicle type improves prediction
  by up to 30%" (Oviedo-Trespalacios et al.).*

### Skipped at abstract level

- *A spatiotemporal analysis of motorcyclist injury severity — Pennsylvania 20 years* — severity
  focus (not crash frequency/count per segment). Spatial non-stationarity is interesting but the
  thesis builds a crash count risk surface, not a severity model. Skip.

---

---

## Keyword 6 — `motorcycle crash hotspot` (2026-06-22) [SPATIAL DIVERGENCE CLUSTER]

**Result: 3 abstract keepers, 1 full-text → DEEP-READ, ~50 title-level skips.** Mostly AV crashes, severity
models, pedestrian/cyclist studies. Two substantive finds: one CLQ method validation on crash data,
one vehicle-type spatial-divergence paper (the strongest niche-premise find of the entire pass, now deep-read).

### Promoted to full-text → **DEEP-READ 2026-06-22** (see [[AAP-deepread]] in this folder)

- **Analysis of crash proportion by vehicle type at traffic analysis zone level: A mixed fractional
  split multinomial logit modeling approach with spatial effects** (Lee, Yasmin, Eluru, Abdel-Aty &
  Cai 2018, AAP 111:12–22) — ✅ **deep-read.** Models crash *proportion* by vehicle type at TAZ level
  (8,129 zones, statewide Florida, 8 vehicle types) via mixed MNL fractional split. Proposes **EPP
  (Excess Predicted Proportion)** = observed − predicted proportion per type, HSM-analogous screening.
  **Key finding (the brick): "the spatial pattern of hot zones is substantially different across the
  various vehicle type crashes"** — HGV hot zones (rural) ≠ bicycle (metro) ≠ pedestrian (urban) ≠
  motorcycle (rural). **Tag: `niche-premise (STRONG — the spatial-divergence brick)` / `method-borrow
  (EPP gate)`.** Upgrades the niche premise from *analogical* to *demonstrated*: vehicle-type hot zones
  DO diverge spatially with real data. Limits: TAZ macro-level (not segment), proportion not
  exposure-normalised risk, no routing — the segment-resolution + routing combination stays open.*

- **Applying the colocation quotient index to crash severity analyses** — *(motorcycle crash hotspot; abstract read 2026-06-22)*
  *Applies CLQ to crash severity categories (fatal, major injury, minor injury, non-injury) in College
  Station, Texas. Finds crashes cluster by severity level; fatal crashes show strongest spatial
  clustering; CLQ matrix approximately symmetrical for non-injury vs injury grouping. **Tag:
  `method-borrow (CLQ)`.** Validates CLQ on crash categorical data — one step from severity categories
  to vehicle-type categories (our planned application). Establishes CLQ as a legitimate crash analysis
  tool in AAP. Hu 2018 (TR-C) remains the primary CLQ reference; this paper is corroborating method
  precedent. Not full-text.*

- **A review of spatial approaches in road safety** — *(motorcycle crash hotspot; abstract read 2026-06-22)*
  *Systematic review of spatial approaches in road safety: areal unit levels, modelling approaches
  (econometric, Bayesian, ML), MAUP, boundary problems, spatial proximity structures, VRU spatial
  analysis. Summarises study design characteristics in reference tables. **Tag: `method-adjacent
  (spatial methods review)`.** Useful landscape reference for spatial methods — covers MAUP and
  proximity structures relevant to our CLQ/segmentation decisions. Not full-text; covers methods
  already represented by individual papers in the corpus.*

### Skipped (representative)
- AV crash studies, severity models, pedestrian/cyclist papers — all seen in prior keywords.

---

## Keyword 5 — `vulnerable road user crash` (2026-06-22)

**Result: 4 abstract keepers, 0 full-text, ~90 title-level skips.** Dominated by pedestrian/cyclist
severity models, AV crash studies, and behavioral research. VRU in AAP = pedestrians/cyclists; motor
vehicle class spatial risk is absent.

### Keepers (abstract-only)

- **Network-wide road crash risk screening: A new framework** — *(vulnerable road user crash; abstract read 2026-06-22)*
  *Integrates probability × severity × exposure per road segment → ranks segments → 5-level risk
  classification. Applied to non-urban road network of Brescia province, Italy (5 years crash data).
  Framework designed to pinpoint critical segments proactively before crashes occur. No vehicle-type
  conditioning, no routing. **Tag: `method-borrow`.** Structural parallel to Barabino's H·V·E and to
  the thesis risk layer (our version is per vehicle type). One citation as method precedent. Not full-text.*

- **Road crash fatality rates in France: A comparison of road user types, taking account of travel practices** — *(vulnerable road user crash; abstract read 2026-06-22)*
  *Exposure-based fatality rates by road user type using French national police crash data + national
  travel survey (2007–2008). Key finding: motorized two-wheeler (MTW) users face **20–32× the fatality
  rate of car occupants** when exposure is controlled; cyclists ~1.5× higher. Rates differ by age and
  sex. **Tag: `niche-premise (strong)`.** The 20–32× figure is a powerful one-sentence thesis
  introduction citation: crash risk is not uniform across vehicle types even per unit of travel. French
  data; principle transfers universally. Not full-text.*

- **Accident characteristics of professional versus regular two-wheeler riders in France and the UK: insights from national crash databases** — *(vulnerable road user crash; abstract read 2026-06-22)*
  *Compares crash characteristics of professional (delivery) vs regular TW riders in France and UK,
  2019–2023. Professional riders: younger, predominantly male, lighter vehicles, urban/lower-speed
  environments, crash timing peaks around delivery hours, more slight injuries (France: 74.7% vs 54.5%;
  UK: 82.3% vs 69.1%). Logistic regression. Uses UK national crash database (STATS19-adjacent). No
  spatial analysis, no segment-level crash frequency. **Tag: `demand-side` / `niche-premise (weak)`.**
  UK context useful; confirms within-TW rider-type differences in crash profile. Complements Kavta 2025
  on delivery-rider demand side. Not full-text.*

- **Estimate traffic cyclist crashes using Poisson-Tweedie models** — *(vulnerable road user crash; abstract read 2026-06-22)*
  *Cyclist crash frequency in Lisbon (2015–2019) using Poisson-Tweedie models for overdispersed count
  data. 250×250m grid cells; covariates: road length, intersection types, cycling infrastructure.
  Spatial autocorrelation incorporated. Intersection density = strongest predictor. **Tag:
  `method-borrow (count model)`.** Directly relevant to Open Decision #3b: cyclists are *overdispersed*
  (Poisson-Tweedie) while motorcycles are *under-dispersed* (Pathivada → CMP/HTCMP). Two different
  per-type count regimes from two papers = the per-type probe must check dispersion before choosing
  the model family. Not full-text.*

### Skipped (representative)
- Severity models for pedestrians, cyclists, e-scooters, e-bikes — off-domain (severity not frequency, not motor vehicle class).
- AV crash studies — off-domain.
- Behavioral/distraction studies — off-domain.

---

## Keyword 4 — `vehicle type crash heterogeneity` (2026-06-22)

**Result: 0 keepers, ~100 title-level skips. Semantic mismatch.** In AAP, "heterogeneity" = statistical
unobserved heterogeneity (random parameters, latent class, temporal instability in model coefficients).
Not inter-vehicle-class differences in crash patterns. The entire 100-paper list is severity models with
heterogeneous error structures. This keyword hit the wrong semantic field — a better keyword would be
`vehicle type crash frequency` or `vehicle class crash spatial`.

**Marginal method picks (not logged as keepers):**
- *Head-on heavy vehicle crashes in Queensland: random parameters Lindley approach for excessive zeros* — HGV-specific with zero-inflation, but severity not frequency. Skip.
- *Segment length optimization for crash frequency modelling: Evaluating power spectral segment length* — method-adjacent to Open Decision #2 but abstract-level insufficient to assess value. Skip.

**Gap-test note:** No paper in 100 results compared crash *patterns* or *spatial distribution* across vehicle types. Confirms the inter-class spatial divergence evidence does not exist in this venue under any plausible keyword.

---

## Keyword 3 — `truck/HGV crash risk` (2026-06-22)

**Result: 0 keepers, ~40 title-level skips.** Returned severity models, behavioral studies (driver
fatigue, HGV–VRU encounters), and real-time interaction metrics. No segment-level HGV crash frequency
or spatial distribution papers. Confirms HGV *spatial* risk evidence is absent from AAP under this
keyword — the evidence simply does not exist, not a search failure.

**Skipped (near-misses):**
- *Analysis of large truck crash severity using heteroskedastic ordered probit models* — severity, not frequency. Skip.
- *Risk assessment in ramps for heavy vehicles — A French study* — HGV risk at ramp features (specific location); severity focus, no routing. Skip.
- *The importance of flow composition in real-time crash prediction* — already in corpus (keyword 2).

---

## Keyword 1 — `risk aware route planning` (2026-06-19)

### Keeper (abstract-only)

- **Do motorists select safe routes over efficient routes? An empirical study using travel trajectory
  data** — *(risk aware route planning; abstract read 2026-06-19)*
  *Empirical route choice study using ALPR trajectory data from Changsha, China. Proposes a paired
  scenario comparison (PSC) method contrasting route choices across four scenario pairs
  (daytime/nighttime, work/non-work, livelihood/non-livelihood, short/long distance). Group Random
  Parameters Logit (GRPL) model with safety attributes (fewer intersections, wider roads) and
  efficiency attributes. Finds that motorists prioritise safety-attributed routes significantly
  during **nighttime trips and for non-livelihood purposes**; work/non-work and distance effects
  inconclusive. Provides empirical support for safety-oriented route planning and navigation systems.
  **Tag: `demand-side` / `related-work`.** Demand-side brick: confirms ordinary motorists do trade
  efficiency for safety (complements Kavta 2025 delivery-rider WTA result, extending it to private
  car drivers). Not a routing system; no vehicle-type conditioning; no crash-data risk surface.
  Does NOT supply routing-home or niche-premise evidence directly. Good for one related-work
  sentence on demand-side motivation.*

## Skipped at title/abstract level (representative)

- *Safer pathfinding strategies for multilevel interchange guide signs* — "pathfinding" = navigating
  ramp exits, not network routing. Signage design study. Skip.
- *Models of perceived cycling risk and route acceptability* — perceived risk from video clips, not
  crash-data routing system. Behavioural/perception, 1990s-era sample. Skip.
- *Using trip diaries to mitigate route risk...older drivers* — feedback intervention for older
  drivers; "route risk" metric not per-vehicle-type crash data; too narrow. Skip.
- *Seasonal instability in the determinants of vulnerable road user crashes* — VRU injury severity
  with seasonal random parameters; not vehicle-type routing or spatial divergence. Skip.
- *Quantifying heterogeneity in bicycle crash frequency: LCA-RPNB* — bicycle-only crash frequency
  modelling; methodology interesting but not relevant to routing home or vehicle-type niche. Skip.
- ~85 further titles: AV/HMI, maritime safety, pedestrian behaviour, human factors,
  cycling infrastructure, older-driver psychology — all off-domain.

## Gap-test note
- No routing *system* paper appeared. AAP's "risk-aware" keyword skews to human factors and
  perception, not route-planning-on-crash-risk. Confirms vehicle-type evidence must come from
  the dedicated niche keywords (pending).

## Links
- [[PLAN]] — keyword clusters · [[positioning-memo]] — evidence map
- [[2026-06-18-where-we-stand-and-remaining-gaps]] — standing gap analysis
- [[TR-C-abstract-refs]] — TR-C sweep (routing home keywords, done)
- [[T-ITS-abstract-refs]] — T-ITS sweep (done)
