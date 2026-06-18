# Phase 3 — Carried-Over Papers (from the Phase 2 corpus)

> **What this is.** The papers from the Phase 2 reading week that survive the pivot to
> **risk-aware routing + vehicle-type niche**, copied here verbatim so Phase 3 is
> self-contained. Organized by role: **Routing home · Vehicle-type niche · Risk engine
> (+ borrow shelf)**. Everything tied to the cut LLM/NL-explanation direction (Li 2025,
> Tab-Text, Hussien, Zhang, Gyawali, Smetana, Wu 2026, TrafficRiskGPT, Li 2026, DRPVLM,
> DDLM, DeepSeek+MCTS, RACI, Chai's CRM taxonomy, the CSM/severity papers, the
> in-vehicle delivery/communication cluster) was **left out** — see `../../PHASE2/` for
> those, demoted to future-work.
>
> Source records: `../../PHASE2/raw/papers/tier1/tier1_journal{1,2,5}/` and
> `tier2/tier2_journal2/`. Entries copied as-written; some retain Phase-2 "gap test"
> framing (the old NL gap) — kept for fidelity, read past it.

---

## Full-text PDFs (copied into `carry_over/`)

Four carried-over papers were deep-read in Phase 2 and have full-text PDFs — copied here:

| File | Paper | Role |
|------|-------|------|
| `carry_over/Jiang2022_Safe-Route-Mapping_T-ITS.pdf` | Jiang et al. 2022 | routing **home** |
| `carry_over/Gao2024_STZITD-GNN_uncertainty-aware_AAP208.pdf` | Gao et al. 2024 | STATS19 risk **engine** baseline |
| `carry_over/Wei2024_lagged-weather-segment-risk_AAP195.pdf` | Wei et al. 2024 | significance-gate ancestor |
| `carry_over/Wang2025_EKC-Bayesian-network_AAP221.pdf` | Wang & Wang 2025 | significance-gate ancestor |

**Carried-over papers WITHOUT a PDF (abstract-only in Phase 2 — must be downloaded):**
- **Sarraf & McGuire 2020** (ESWA) — routing layer + eval metrics. *Priority — now core.*
- **Zhu et al. 2025** (T-ITS) — vehicle-group risk, the niche premise. *Priority — now core.*
- **de Souza et al. 2020** (T-ITS) — personalized re-routing precedent.
- The AAP/ESWA/KBS borrow-shelf abstracts (network screening, SA-EB, Rúa, Hu/PST-CGCN,
  Man/WGAN, extreme-heat, freeway LCA/LPA, WFFS, accident-triangle) — pull full text only
  when a method is actually adopted in the build.

> Note: the four PDFs above were *copied* (not moved) — originals remain in the read-only
> Phase 2 archive. Papers tied to the cut LLM direction (Li 2025, Zhang 2025, Tab-Text,
> Hussien, TrafficRiskGPT, Wu 2026, Li 2026, Chai/EAAI, Smetana, RACI, Ryder/DSS) still
> have their PDFs in `../../PHASE2/` but were deliberately **not** copied.

---

## ROUTING HOME

### Jiang et al. 2022 — Safe Route Mapping of Roadways Using Multiple Sourced Data (T-ITS) ★ HOME
*Jiang, Jafari, Kharbeche, Jalayer, Al-Khalifa, 2022.*

Where it lies in the progress: the bigger step — gives real new CONTEXT, not just
validation. (1) Roots us in the canonical risk-assessment methodology we were missing —
SPF (Safety Performance Function) + Empirical Bayes + Highway Safety Manual — i.e. the
actual "risk assessment" home the supervisor named. (2) Reveals our deliverable already
exists in primitive form ("safe routes on navigation," risk heat maps for drivers), so the
raw idea is NOT novel. (3) Therefore pins our real novelty precisely on what it lacks:
condition-conditioning (no weather/light/time), the natural-language WHY (output is a
numeric fuzzy score), and significance/overrepresentation.

**Phase 3 role:** the home paper. Per-segment risk score → safe-route heat maps. Our
routing layer extends this by conditioning the risk on vehicle type. Get full text for
the routing methodology detail.

### Sarraf & McGuire 2020 — Integration and Comparison of MCDM Methods in Safe Route Planner (ESWA) ★ ROUTING LAYER + EVAL
Strong `integration` precedent. Opens with our exact framing — risk maps are
confusing, drivers must manually interpret them, Google Maps/Waze rank only by time
and distance. Assumes a per-segment risk score already exists; the contribution is the
downstream MCDM layer (AHP/Fuzzy AHP/TOPSIS/Fuzzy TOPSIS/PROMETHEE) that combines
risk+time+distance into a route ranking, evaluated via Spearman's rank correlation,
Average Overlap, and DCG. Confirms route planning as a real consumer slot for our risk
profiles — they'd plug in upstream of this MCDM layer.

**Phase 3 role:** the routing-layer method AND the routing-evaluation template
(Spearman / Average Overlap / DCG). Abstract only — **get full text.**

### de Souza et al. 2020 — Safe and Sound: Driver Safety-Aware Vehicle Re-Routing Based on Spatiotemporal Information (T-ITS)
Risk-aware re-routing, but "risk" = criminal events, not crash risk. RNN predicts dynamic
future risk scores; personalized re-routing lets each vehicle choose which risk types to
avoid. Reinforces the Jiang-2022 pattern (aggregate→numeric score→route) with dynamic
prediction instead of static SPF/EB — still no condition-conditioning on situational
factors, no NL explanation. Another brick in the gap; weak as a cited baseline due to
domain mismatch (crime vs. crash).

**Phase 3 role:** precedent for *personalized* (per-vehicle) re-routing — the structural
ancestor of vehicle-type-specific routing. Cite for the personalization pattern, not as a
crash baseline.

---

## VEHICLE-TYPE NICHE EVIDENCE

### Zhu, Wang, Feng, Ma, Abdel-Aty 2025 — Vehicle-Group-Based Crash Risk Prediction and Interpretation on Highways (T-ITS) ★ NICHE PREMISE
Mohamed Abdel-Aty is the most-cited real-time crash-risk researcher — cite as a field
anchor regardless of method fit.

**Phase 3 role:** closest precedent that crash risk varies by *vehicle grouping* —
validates the premise of the vehicle-type niche. But it *predicts* group risk; it does
not *route*. The white space (vehicle-type-conditioned routing) is unoccupied. **Get full
text** — this is now niche-critical, not a peripheral anchor.

### Optimizing crash risk models for freeway segments: heterogeneous effects of road geometric design features, traffic operation status, and crash units (AAP, abstract)
Segment-level crash risk prediction on Yongtaiwen Freeway (Zhejiang, China) with widely-spaced
detectors. Latent Class Analysis (LCA) + Latent Profile Analysis (LPA) classify segments into
subgroups by geometric features and traffic operation status; binary/conditional logit + grouped
random parameter logit models fit per subgroup. Finding: combined geometric+operational
heterogeneity model performs best; grouped random parameters beat conditional logit for
unobserved heterogeneity. CRM on freeway segments — but "conditioning" = road geometry
classification, not live weather/time conditions. Output: crash risk prediction paradigm for
traffic safety management departments (numeric). `home`/`related-work`.

**Phase 3 role:** precedent for *heterogeneous* segment risk modeling (subgroups with
their own risk profiles) — the methodological pattern our vehicle-type stratification
follows, just keyed on vehicle type instead of geometry/operation class.

### Quantifying and comparing the effects of key risk factors on various types of roadway segment crashes with LightGBM and SHAP (AAP, abstract)
LightGBM vs XGBoost on Texas crash data 2015–2017; SHAP for factor importance by collision
type (Rear-End vs Run-Off-Road). Significant factors: speed limits, area type, number of
lanes, roadway functional class, shoulder width/type. Risk factor importance varies across
crash types — lane width <12ft increases all crash types; speed limit more important for RE
than ROR. Output: SHAP charts/tables.

**Phase 3 role:** evidence that risk-factor importance is *not uniform* — it varies by
crash type / segment characteristics. Supports the general "one aggregate risk number is
too coarse" argument behind the niche.

---

## RISK ENGINE (the upstream model that feeds the router)

### Gao, Jiang, Haworth et al. 2024 — Uncertainty-aware probabilistic GNN for road-level traffic crash prediction (STZITD-GNN) (AAP 208) ★★★ STATS19 BASELINE
*Gao, Jiang, Haworth, Zhuang, Wang, Chen, Law — UCL SpaceTimeLab + PKU + MIT + UFlorida. Open access, code on GitHub.*

**Why this is the single most important engine paper.** It is the first paper found that
does road-level (segment-level) crash risk prediction **on UK STATS19 data itself**
(Department for Transport, explicitly named), in a real UK urban context (three London
boroughs: Westminster, Lambeth, Tower Hamlets). Proves the domain, the dataset, AND the
technical state of the art, in the flagship road-safety journal. From a serious UK
spatial-analysis group (UCL SpaceTimeLab — Haworth, Law, Chen).

**What they built.** STZITD-GNN: a Spatiotemporal Zero-Inflated Tweedie Graph Neural
Network for road-level daily crash risk prediction with uncertainty quantification,
forecasting 14 days ahead (multi-step).
- *Graph*: each road segment = a node (not intersection-as-node), edges = road
  connections; adjacency matrix A. Granular, road-specific.
- *Encoder*: GRU (temporal) + GAT (spatial) → spatiotemporal embedding.
- *Decoder*: four parameter decoders output the parameters (π, μ, φ, ρ) of a
  **Zero-Inflated Tweedie distribution** per road per time step → predicts a full
  probabilistic crash-risk distribution, not a point estimate.
- *Crash risk target* (Definition 1): severity-weighted sum of crashes per road per time
  slot — minor=1, serious=2, fatal=3. So "risk" already bakes in STATS19 severity classes.
- *Input features* (Table 3): crash counts (DfT/STATS19), Points of Interest (Ordnance
  Survey), road geometry (OS), meteorological characteristics (Met Office — weather),
  date (holiday/working day), socio-demographic (Census 2011).

**The zero-inflation problem = our exact problem.** Zero-inflation rates of **95.72%
(Westminster), 96.71% (Lambeth), 96.28% (Tower Hamlets)** — ~96% of road-days have zero
crashes. Precisely the STATS19 sparsity / rare-event problem (fatal-class imbalance is its
extreme tail). Their answer: the ZITD distribution's sparsity parameter π handles excess
zeros end-to-end (cleaner than separate SMOTE/oversampling). A borrowable, citable
solution to our central data problem, validated on STATS19.

**Results.** vs baselines (HA, STGCN, STGAT, and Gaussian/NB/TD/ZINB GNN variants): up to
34.60% reduction in point-estimate regression error (MAPE), ≥47% (up to 55.07%)
improvement in interval-based uncertainty metrics, 76.59% precision in identifying actual
crashes among top-20% predicted high-risk roads (Lambeth). Outputs choropleth risk maps per
borough (Fig 4) — risk clusters along major thoroughfares (A11 Whitechapel Rd, A13, A3).

**What it does NOT do (the contrast):** output = a numeric severity-weighted risk score per
road (plus uncertainty interval), rendered as a heat map. Weather is an INPUT feature, not
a conditioning axis of the output. No significance gate. **No vehicle-type stratification —
risk is aggregated across all vehicles.**

**Phase 3 role:** THE engine baseline, on our exact dataset. Borrow: Zero-Inflated Tweedie
for ~96% zero-inflation; road-segment-as-node + GAT spatial encoding; severity-weighting
(minor/serious/fatal = 1/2/3). Our delta on the engine side = per-vehicle-type risk; on the
system side = routing on it. Their Table 1 surveys 14 prior road/region crash-prediction
models — all output a risk score or occurrence.

### Wei, Das, Wu, Li, Zhang 2024 — Modeling the lagged impacts of hourly weather and speed variation on segment crash risk: a space–time-stratified case-crossover design (AAP 195) | Texas A&M
**What they built.** A segment-level, condition-conditioned crash risk analysis using two
interpretable time-series methods — the Distributed Lag Model (DLM) and the Distributed Lag
Nonlinear Model (DLNM) — applied to a space-time-stratified case-crossover dataset. Data:
Texas rural interstate highways (TxDOT RHiNO road segments + NPMRDS probe-speed + ASOS
weather + CRIS crash records), 2019, aggregated to 1-hour intervals. Case hours (crash
occurred) matched to 3–4 control hours with identical road ID, year, month, day-of-week,
and hour-of-day to control for spatial and temporal confounds. Final dataset: 27,400
zero-crash + 8,022 one-crash + 175 two-crash + 23 three-crash hourly observations.
Quasi-Poisson regression fits both models. Four time-series exposures: hourly
precipitation, hourly visibility, hourly temperature, hourly speed standard deviation.

**Results by condition.**
- *Precipitation*: Strong lagged impact. Crash risk starts rising at lag 1h, peaks at lag
  2h (DLM) or lag 3–4h (DLNM) after precipitation. Mechanism: after heavy rain stops,
  drivers resume speed while oil/gasoline residue on the dry roadway mixes with rainwater →
  slippery surface → elevated crash risk at lagged hours. At 3 inches/hour intensity, RR
  peaks ~3.0–3.5 at lag 2–4h.
- *Visibility*: Immediate impact only (RR ~1.34 for 1-mile visibility at lag 0). Dissipates
  quickly. No significant lagged effect.
- *Temperature*: DLM finds no effect. DLNM reveals an immediate impact at lag 0 for LOW
  temperatures (10–20°F, RR ~3.5), dropping at lag 1–2h. DLNM outperforms DLM because
  temperature varies slowly.
- *Speed standard deviation*: Immediate and large impact at lag 0 (RR ~4–9 for high
  deviation). Dissipates completely by lag 1h.

**Conclusions.** AIC: DLNM (35,928) slightly beats DLM (36,241). Key stated takeaway:
"warning messages should adapt dynamically based on the lagged impact patterns on segment
crash risk following weather-related exposure." Applications: VSL (variable speed limits),
in-vehicle driving assistance, road signage adapted to lagged risk curves.

**Phase 3 role:** strongest methodological ancestor for the significance/overrepresentation
gate (case-crossover = compare crash-hours vs matched non-crash control hours on the same
segment). Validates the exact condition variable set (precipitation/visibility/temperature/
speed-deviation ≈ STATS19 weather/road-surface/light). Validates the segment × condition ×
time design — i.e. justifies the *secondary* conditioning axes layered on vehicle type.

### Wang & Wang 2025 — Causal relationship discovery for highway crash analysis using semi-data-driven Bayesian network (AAP 221) | Tongji University
**What they built.** An Expert Knowledge Constraint-based (EKC) Bayesian Network for crash
causation analysis on the HuNing Highway, Suzhou, China. Data: 10 camera-equipped highway
segments, 2022, hourly traffic volume + crash records + weather conditions (Cloudy/Sunny/
Foggy/Rainy/Snowy). 951 crash cases + 37,352 non-crash cases. 7 variables: Time of week,
Daytime, Season, Weather, Temperature, Volume, Crash.

**The EKC algorithm (borrowable).** (1) Structure learning: expert knowledge labels each
potential link True/False/Unknown; for Unknown arcs, chi-square conditional independence
test with Bonferroni correction. (2) Direction decision: v-structure detection + acyclicity
→ DAG. (3) Parameter learning: Bayesian estimation → CPDs. (4) Inference: variable
elimination across all 3,240 scenario combinations → crash probability per scenario → rank
the 10 most dangerous.

**Key findings.** Direct predictors of Crash: Temperature, Volume only (calendar variables
act indirectly through physical conditions). Temperature → crash: cold AND hot = higher.
Volume → crash: MEDIUM volume = highest (high volume → slow speeds, fewer conflicts).
Weather → crash: Snowy = highest. Top dangerous scenario: Medium volume + Cold + Winter +
Cloudy + Weekday + Morning (4.81×10⁻⁴). EKC beats Hill Climbing / Chow-Liu / logistic on BIC.

**Phase 3 role:** second methodological ancestor for the significance gate (chi-square CI
testing of condition→crash). Validates the conditioning variable set on 38,303 real records.
The counter-intuitive findings (medium volume most dangerous; cold matters) are the kind of
non-obvious per-condition pattern stratified risk surfaces. Citable interpretability
framework (causality, trust, heterogeneity, transferability, stability).

---

## BORROW SHELF (methods for the risk engine — sparsity / imbalance / features)

- **Man, Quddus, Theofilatos, Yu, Imprialou 2022 — WGAN for imbalanced real-time crash risk
  prediction (T-ITS).** WGAN directly borrowable for Fatal-class imbalance (1.5% of STATS19);
  **UK M1 Motorway data** — Quddus is a credible UK crash author. Imbalance shelf #1.
- **Rúa, Arias, Martínez-Sánchez 2024 — Combination of Macroscopic and Microscopic Crash
  Prediction Models (ESWA).** Second independent anchor for the "aggregate crashes → numeric
  CPM score per segment" bucket (AHP+NB+GWPR ensemble, Spain highway 2016–2021). Confirms
  "aggregate→score" is a family of approaches — useful related-work context for the engine.
- **Hu, Bai, Lee 2025 — Crash Risk Prediction Using Sparse Collision Data: Granger Causal
  Inference + GCN (PST-CGCN) (ESWA).** Spatial-temporal crash-risk forecasting on sparse
  data; gradient-based causal interpretability. Borrow for the sparse-data / spatial angle.
- **Network-wide road crash risk screening: A new framework (AAP, abstract).** Risk =
  probability × vulnerability × exposure per road segment → five-level classification →
  ranked network-wide list. Province of Brescia, Italy. The home-field screening method
  stated plainly (what network screening outputs: a ranked numeric score per segment).
- **A spatially adaptive empirical Bayes framework with dynamic dispersion (SA-EB) (AAP,
  abstract).** EB + Geographically Weighted Poisson Regression + MGWR + CMFs. Iran rural
  highways. Confirms EB/HSM remains the state-of-practice baseline for segment risk. 20%
  crash reduction with EB-guided improvements. The numeric baseline the routing risk layer
  sits above.
- **Roadway traffic crash during extreme heat days (AAP, abstract).** Condition-conditioned
  segment-level crash-rate analysis (extreme-heat thresholds × segments, Miami) via
  CatBoost + SHAP. The CRM paradigm applied to a weather condition — supports the secondary
  conditioning axes. CatBoost+SHAP stack mirrors Phase 1's approach.
- **WFFS — ensemble feature selection for heterogeneous traffic accident data (KBS,
  abstract).** UK traffic accident records → weighted fusion feature selection + balancing →
  tree-based bagging. Feature-selection step directly applicable to STATS19's heterogeneous
  categorical features; another UK-data point.
- **Overcoming Imbalanced Safety Data Using Extended Accident Triangle (KBS, abstract).**
  Severity/frequency/type-weighted oversampling grounded in Heinrich accident-pyramid theory
  (vs naive SMOTE), open-source code. A citable safety-science framework for fatal-class
  imbalance beyond "we used SMOTE." Imbalance shelf, with reusable code.

---

## Tag legend

`home` / `niche-evidence` / `engine` / `borrow` — Phase 3 routing-direction tags.
(Original Phase 2 records used `home`/`integration`/`related-work`/`borrow`/`background`/`skip`.)
