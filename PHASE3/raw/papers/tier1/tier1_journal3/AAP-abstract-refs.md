# AAP — Phase 3 Reading-Pass Record (Tier 1, Journal 3)

**Pass:** 2026-06-19, risk-aware-routing + vehicle-type-niche direction. Lightweight per-journal
record (titles → abstracts → full-text), mirroring the Phase 2 style.

**Keywords swept so far:** `risk aware route planning` (generic, 2026-06-19) ·
`motorcycle crash risk segment` (2026-06-19).

**Keywords pending:** `truck/HGV crash risk` · `vehicle type crash heterogeneity` ·
`vulnerable road user crash`.

**Pass result (keyword 2/5): 7 abstract keepers, 2 full-text promotions, 1 skip (severity-only), ~90 title-level skips.** AAP's generic routing keyword returns
mostly noise (AV/HMI, human factors, pedestrian/cycling behaviour). Vehicle-type keywords are where
AAP is expected to deliver; this keyword confirms that routing-system work does not home here.

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
