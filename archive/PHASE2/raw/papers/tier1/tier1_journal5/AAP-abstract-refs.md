# AAP — Tier 1, Journal 5 Reading Record

**Journal:** Accident Analysis & Prevention (AAP) — flagship road-safety venue.

**Progress so far:** ALL 3 keywords complete — AAP done. 5 full-text deep reads —
incl. **Gao et al. 2024 (STZITD-GNN), the direct UK-STATS19 road-level baseline
(★ top find / keystone reference)**. 14 abstract-only refs. Keyword 3 added the
delivery/communication grounding axis (how to deliver risk to a driver) that
completes the pipeline story. Gap test UNBEATEN throughout.

---

## Full-text (deep-read)

---

### 1. Modeling the lagged impacts of hourly weather and speed variation factors on the segment crash risk of rural interstate freeways: Applying a space–time-stratified case-crossover design
**Wei, Das, Wu, Li, Zhang — AAP 195 (2024) 107411 | Texas A&M**

**What they built.** A segment-level, condition-conditioned crash risk analysis
using two interpretable time-series methods — the Distributed Lag Model (DLM)
and the Distributed Lag Nonlinear Model (DLNM) — applied to a
space-time-stratified case-crossover dataset. Data: Texas rural interstate
highways (TxDOT RHiNO road segments + NPMRDS probe-speed + ASOS weather +
CRIS crash records), 2019, aggregated to 1-hour intervals. Case hours (crash
occurred) matched to 3–4 control hours with identical road ID, year, month,
day-of-week, and hour-of-day to control for spatial and temporal confounds.
Final dataset: 27,400 zero-crash + 8,022 one-crash + 175 two-crash + 23
three-crash hourly observations. Quasi-Poisson regression fits both models.
Four time-series exposures: hourly precipitation, hourly visibility, hourly
temperature, hourly speed standard deviation.

**Results by condition.**
- *Precipitation*: Strong lagged impact. Crash risk starts rising at lag 1h,
  peaks at lag 2h (DLM) or lag 3–4h (DLNM) after precipitation. Mechanism:
  after heavy rain stops, drivers resume speed while oil/gasoline residue on
  the dry roadway mixes with rainwater → slippery surface → elevated crash
  risk at lagged hours. At 3 inches/hour intensity, RR peaks ~3.0–3.5 at lag
  2–4h.
- *Visibility*: Immediate impact only (RR ~1.34 for 1-mile visibility at lag 0).
  Dissipates quickly — at lag 1–3h the RR drops below 1.0, because during a
  low-visibility event incoming drivers also come from nearby low-vis areas
  and drive cautiously. No significant lagged effect.
- *Temperature*: DLM finds no effect. DLNM (nonlinear exposure transformation)
  reveals an immediate impact at lag 0 for LOW temperatures (10–20°F, RR ~3.5),
  dropping sharply at lag 1–2h as drivers adapt. Normal-to-high temperatures
  show flat response. DLNM outperforms DLM here because temperature varies
  slowly — the nonlinear polynomial transformation magnifies the small variation
  that exists.
- *Speed standard deviation*: Immediate and large impact at lag 0 (RR ~4–9 for
  high deviation). Dissipates completely by lag 1h. No lagged effect — speed
  variation on one segment doesn't persist to the next hour.

**Conclusions.** AIC: DLNM (35,928) slightly beats DLM (36,241). Key takeaway
(stated explicitly): "warning messages should adapt dynamically based on the
lagged impact patterns on segment crash risk following weather-related exposure,
thereby mitigating potential roadway hazards." Practical applications:
VSL (variable speed limits), in-vehicle driving assistance, road signage adapted
to lagged risk curves.

**Does it beat the gap? NO.** Output = exposure-lag-response curves and relative
risk tables (numeric). The system computes WHAT the lagged risk is, but never
produces a natural-language statement like "this segment is elevated risk for the
next 3 hours due to the precipitation that fell at 4pm." No NL output to any
consumer. No condition-conditioned NL explanation. Gap unbeaten.

**What this hands us (HIGH VALUE — `home`+`borrow` STANDOUT):**

1. *Strongest methodological ancestor to our significance gate found in any
   paper.* The case-crossover design is precisely the conceptual mirror of what
   our significance gate does: it compares crash-hours vs matched non-crash
   control hours on the same road segment, asking "are the conditions during
   crash hours different from what you'd expect by chance?" Our chi-square test
   asks the same question from a different angle. This is citable as the
   methodological precedent for condition-conditioned segment risk analysis.

2. *Validates our exact condition variable set.* Precipitation, visibility,
   temperature, and speed variation are all directly analogous to STATS19
   variables (weather conditions, road surface, light conditions). Published
   in AAP 2024 and confirmed as valid predictors of segment-level crash risk.

3. *Validates the segment × condition × time design.* This is a SEGMENT-LEVEL
   analysis (not intersection, not individual crash, not network aggregate),
   with HOURLY temporal resolution, conditioning on WEATHER+SPEED factors.
   That is our exact design layer.

4. *The lagged-impact narrative is a concrete case for why drivers need
   advance warning.* If risk peaks 2–4 hours after the rain stops, a driver
   who sees dry roads assumes safety but is in an elevated-risk window. Our
   NL output bridges that gap — the model knows the segment is elevated risk
   in post-rain conditions; the system needs to tell the driver that.

Tag: `home`+`borrow` STANDOUT. Gap test: UNBEATEN — but the closest
methodological ancestor in the home journal for our significance gate.

---

### 2. Causal relationship discovery for highway crash analysis using semi-data-driven Bayesian network
**Wang, Wang — AAP 221 (2025) 108181 | Tongji University, Shanghai**

**What they built.** An Expert Knowledge Constraint-based (EKC) Bayesian
Network for crash causation analysis on the HuNing Highway, Suzhou, China.
Data: 10 camera-equipped highway segments, 2022, hourly traffic volume +
crash records + weather conditions (Cloudy/Sunny/Foggy/Rainy/Snowy) + crash
records from the Suzhou Road Traffic Crash Analysis and Warning System. 951
crash cases + 37,352 non-crash cases. 7 variables: Time of week, Daytime,
Season, Weather, Temperature, Volume, Crash.

**The EKC algorithm (the borrowable technique).** Three steps:
1. *Structure learning.* Expert knowledge labels each potential link as True
   (arc exists), False (no arc), or Unknown. For Unknown arcs, chi-square
   conditional independence test determines True/False, with Bonferroni
   correction. Result: 12 links in final BN, including 5 False (set by expert),
   7 True (confirmed by expert or test).
2. *Direction decision.* v-structure detection + acyclicity enforcement →
   directed DAG.
3. *Parameter learning.* Bayesian estimation → Conditional Probability
   Distributions (CPDs) for each node given its parents.
4. *Inference.* Variable elimination across all 3,240 possible scenario
   combinations → crash probability per scenario → rank the 10 most dangerous.

**Key structural findings.** Direct predictors of Crash: Temperature, Volume
only (expert knowledge confirmed; chi-square alone would have excluded them
due to small sample). Time-of-week, Daytime, Season affect crash only
INDIRECTLY (mediated through Temperature, Volume, Weather). This is a strong
interpretability result: the calendar variables matter, but they matter through
their effect on physical conditions.

**Parameter learning (CPD) results:**
- Temperature → crash: Cold AND Hot temperatures = higher crash probability
  vs cool temperatures. Cold: reduced friction, icy conditions. Hot: tire
  pressure issues, heat-related fatigue.
- Volume → crash: MEDIUM volume = highest crash probability (not high — high
  volume produces slow speeds, fewer speed-differential conflicts; low volume
  means few vehicles; medium = highest conflict opportunity).
- Weather → crash: Snowy = highest crash probability.

**Inference (most dangerous scenarios, Table 4):**
Top scenario: Medium volume + Cold temperature + Winter + Cloudy + Weekday
+ Morning, crash probability 4.81×10⁻⁴. All top-10 scenarios share medium
volume + cold + winter + cloudy; daytime and time-of-week vary.

**Model comparison.** EKC achieves best BIC (−243,757 vs Hill Climbing −236,221
vs Chow-Liu Trees −239,643 vs logistic 8,656). Hill Climbing introduces a
counterintuitive Season→Time-of-week dependency; Chow-Liu Trees misses
multivariate dependencies. EKC's expert-first approach eliminates these.

**Does it beat the gap? NO.** Output = conditional probability tables + ranked
dangerous scenarios (numeric probabilities). The most dangerous scenario is a
table row: "medium volume, cold, winter, cloudy, morning, weekday → 4.81×10⁻⁴."
No natural-language statement to a driver. No condition-conditioned NL
explanation. Gap unbeaten.

**What this hands us (`home`+`borrow`):**

1. *Validates our conditioning variable set on a real highway dataset.* Weather,
   temperature, volume, season, time-of-day → crash probability — confirmed
   empirically on 38,303 real cases. These are the conditions our significance
   gate tests.

2. *The EKC algorithm is a direct methodological sibling of our significance
   gate.* Both combine expert knowledge with statistical testing to determine
   which condition–crash associations are real. We use chi-square to test
   overrepresentation; EKC uses chi-square to test conditional independence.
   Same statistical tool, different framing. This is citable as methodological
   validation of our hybrid expert+statistical approach.

3. *The medium-volume danger finding is counter-intuitive and valuable for NL
   output.* "Rush hour is not the most dangerous — moderate traffic, cold, wet
   conditions in winter are" is exactly the kind of non-obvious insight our
   system should be able to surface as NL output.

4. *Interpretability discussion is citable.* The paper explicitly defines a
   framework for model interpretability: causality, trust, heterogeneity,
   transferability, stability. Directly applicable to justifying our own
   interpretability claims.

Tag: `home`+`borrow`. Gap test: UNBEATEN. Second strongest methodological
ancestor to our significance gate.

---

### 3. From crash reports to safer roads: a multimodal framework integrating vision-language models and street view analysis
**Wu, Yan, Zou, Xie — AAP 228 (2026) 108419 | UMass Lowell + Tongji**

**What they built.** A two-stage framework for automated road safety diagnostics
using VLMs on crash reports and street-view imagery. Data: 4,302 crash reports
from Massachusetts DOT (2018–2019, 2021–2022), crashes at/near signal-controlled
ramp terminals across 16 municipalities. Each report contains: crash narrative
(free-text police description) + crash diagram (image of vehicle positions) +
geocoordinates.

**Stage 1: VLM root-cause attribution.** Structured prompt to VLM (Grok 2,
GPT-4o, Gemini 2.0 Flash, DeepSeek V3) → jointly reads narrative + diagram →
produces proportional attribution across 5 factors: Human, Vehicle, Road,
Environment, Traffic Signal, summing to 100%. The prompt specifies role
definitions, factor definitions, causal reasoning rules, and output format.
Validated on 500-expert-annotated reports (2 trained reviewers, Top-1 agreement
0.972, Spearman correlation 0.874 between annotators).

**Stage 2: Spatial clustering + street-view diagnosis.** DBSCAN (ε=50m,
minPts=2) → 440 spatial clusters. Road-related risk score per cluster: average
road attribution proportion (weighted by crash count^γ). Top 20 road-risk
hotspots identified. Google Street View imagery retrieved for each hotspot.
Grok 2 + structured road diagnostics prompt → assessments across 5 dimensions:
roadway alignment, pavement markings, road signs, surface conditions,
shoulders/guardrails. Output: list of observed defects + actionable
infrastructure improvement recommendations.

**Key results.**
- On 100-report test set: Grok 2 multimodal achieves Spearman=0.864,
  Top-1=1.000, WSP=0.968. Significantly beats local regression baselines
  (ResNet18+BERT: Spearman=0.736, BERT-based: 0.737, BLIP-2: 0.746).
- LLMs outperform local models especially for non-human-dominated crashes:
  local models systematically overestimate human factor (trained on imbalanced
  data); LLMs reason from semantic content so they preserve road/environment
  attributions in low-frequency cases.
- On 500-report annotated set: Grok 2 multimodal top performer across all
  crash-level and factor-level metrics.
- BERTScore F1=0.796 (Grok 2) vs F1=0.790 (GPT-4o) for street-view diagnostics.
  Semantically aligned with expert-written reference diagnoses.
- Real-world validation: one hotspot's model-suggested lane-merge signage
  improvement matches actual post-crash infrastructure modification implemented
  by the agency.

**Does it beat the gap? NO — but the closest output-side paper found in AAP.**
Three distinctions that keep the gap unbeaten:
1. *Output addressee*: to road ENGINEERS for infrastructure redesign (defects,
   recommendations for MUTCD compliance), not to DRIVERS for real-time risk
   awareness. The output is a structured report for a safety analyst, not a
   natural-language alert for a person driving on the road right now.
2. *Input*: crashes that already happened (retrospective attribution), not
   condition-conditioned prediction of which scenarios make a segment risky.
3. *No condition-conditioning*: the attribution decomposes by causal factor
   category (human/road/environment), not by condition state (wet road vs dry
   road, morning vs evening). There is no "this location is high-risk in foggy
   conditions" output.

**What this hands us (`related-work`+`borrow`):**

1. *Confirms VLMs can generate valid NL about crash causation, validated against
   human expert judgement.* Spearman=0.864 vs expert annotations is strong. The
   domain knowledge is there; the NL output is high quality. This validates our
   own approach of using an LLM to generate condition-specific explanations.

2. *DBSCAN + road-risk scoring is directly borrowable.* If we want to aggregate
   our segment-level significance-gate findings to hotspot-level reports, this
   spatial aggregation approach is the template.

3. *The two-stage architecture pattern (structured inference → aggregation →
   NL diagnosis) is our architecture.* We do: significance gate (inference) →
   segment risk profile (aggregation) → NL explanation (diagnosis). Same
   logical flow, different domain.

4. *Factor attribution framework (Human/Vehicle/Road/Environment/Signal) is
   related to but distinct from our condition conditioning.* They ask "which
   causal factor type caused this crash?" We ask "under which conditions is this
   segment historically dangerous?" Complementary framings; citable contrast.

Tag: `related-work`+`borrow`. Gap test: UNBEATEN — but the furthest
output-side predecessor. Closest-to-home paper for the "NL output" half
of our novelty pin.

---

### 5. Uncertainty-aware probabilistic graph neural networks for road-level traffic crash prediction (STZITD-GNN)
**Gao, Jiang, Haworth, Zhuang, Wang, Chen, Law — AAP 208 (2024) 107801 | UCL SpaceTimeLab + PKU + MIT + UFlorida**
**★★★ THE DIRECT STATS19 BASELINE — open access, code on GitHub ★★★**

**Why this is the single most important paper of the AAP sweep for us.** It is
the first paper found in the entire Phase 2 reading that does road-level
(segment-level) crash risk prediction **on UK STATS19 data itself**
(Department for Transport, explicitly named), in a real UK urban context
(three London boroughs: Westminster, Lambeth, Tower Hamlets). This is the
baseline-to-replicate-and-improve we flagged as missing — it proves the domain,
the dataset, AND the technical state of the art in one paper, in the flagship
road-safety journal. From a serious UK spatial-analysis group (UCL SpaceTimeLab —
Haworth, Law, Chen).

**What they built.** STZITD-GNN: a Spatiotemporal Zero-Inflated Tweedie Graph
Neural Network for road-level daily crash risk prediction with uncertainty
quantification, forecasting 14 days ahead (multi-step).
- *Graph*: each road segment = a node (not intersection-as-node), edges =
  road connections; adjacency matrix A. Granular, road-specific.
- *Encoder*: GRU (temporal) + GAT (spatial) → spatiotemporal embedding.
- *Decoder*: four parameter decoders output the parameters (π, μ, φ, ρ) of a
  **Zero-Inflated Tweedie distribution** per road per time step → predicts a
  full probabilistic crash-risk distribution, not a point estimate.
- *Crash risk target* (Definition 1): severity-weighted sum of crashes per road
  per time slot — minor=1, serious=2, fatal=3. So "risk" already bakes in
  STATS19 severity classes.
- *Input features* (Table 3): crash counts (DfT/STATS19), Points of Interest
  (Ordnance Survey), road geometry (OS), **meteorological characteristics (Met
  Office — weather)**, date (holiday/working day), socio-demographic (Census
  2011).

**The zero-inflation problem = our exact problem.** They report zero-inflation
rates of **95.72% (Westminster), 96.71% (Lambeth), 96.28% (Tower Hamlets)** —
i.e. ~96% of road-days have zero crashes. This is precisely the STATS19 sparsity
/ rare-event problem we keep hitting (and the fatal-class imbalance is its
extreme tail). Their answer: the ZITD distribution's sparsity parameter π handles
excess zeros end-to-end (cleaner than separate SMOTE/oversampling). This is a
**borrowable, citable solution to our central data problem, validated on STATS19.**

**Results.** vs baselines (HA, STGCN, STGAT, and Gaussian/NB/TD/ZINB GNN
variants): up to 34.60% reduction in point-estimate regression error (MAPE),
≥47% (up to 55.07%) improvement in interval-based uncertainty metrics, 76.59%
precision in identifying actual crashes among top-20% predicted high-risk roads
(Lambeth). Outputs choropleth risk maps per borough (Fig 4) — risk clusters
along major thoroughfares (A11 Whitechapel Rd, A13, A3).

**Does it beat the gap? NO — and the contrast is exactly our thesis.** This is
the cleanest "everything but our contribution" paper we have:
1. *Output = a numeric severity-weighted risk score per road* (plus an
   uncertainty interval). Rendered as a heat map. **No natural language.** No
   explanation of WHY a road is risky. The driver/analyst sees a colored road
   and a number.
2. *Weather is an INPUT FEATURE, not a conditioning axis of the output.* The
   model ingests Met Office weather to improve the aggregate daily prediction,
   but it never outputs "this road is high-risk *in rain*" vs "*at night*."
   There is no condition-stratified, condition-specific risk statement — which
   is the heart of our condition-conditioning.
3. *No significance gate.* Risk is a learned continuous score; there is no test
   of whether a specific condition is statistically overrepresented among a
   road's crashes.
4. *Uncertainty ≠ explanation.* Their "uncertainty-aware" = a prediction
   interval (aleatoric/epistemic), NOT a faithfulness-validated reason. It tells
   you how confident the number is, not why the road is dangerous.

**What this hands us (the highest-value `home`+`borrow` of the sweep):**

1. *THE replication baseline, on our exact dataset.* We can now write: "the
   state of the art for road-level crash risk on STATS19 (Gao et al. 2024, AAP)
   produces a severity-weighted probabilistic risk score per road segment,
   rendered as a heat map; it does not condition the output on situational
   factors, does not test pattern significance, and does not explain risk in
   natural language." That is our contribution stated as a delta against a real,
   recent, top-venue baseline — exactly what you asked for two turns ago.

2. *Proves the domain/context is live and serious.* UK STATS19 + London +
   road-level CRM is published in AAP 2024 by a credible group. The "artificial
   / no research home" critique is fully answered: this IS the home, on our
   data.

3. *Borrowable zero-inflation solution.* Zero-Inflated Tweedie is a principled,
   STATS19-validated alternative/complement to SMOTE for our sparsity problem.
   Add to the statistical-methods shelf.

4. *Borrowable graph construction.* Road-segment-as-node + GAT spatial encoding
   is directly reusable if we want spatial spillover between segments.

5. *Their severity-weighting scheme (minor/serious/fatal = 1/2/3)* is a citable
   precedent for how to collapse STATS19 severity into a single risk target.

6. *Confirms the gap from the predictive side.* Their Table 1 surveys 14
   road/region crash-prediction models — every single one outputs a "Crash Risk
   Score" or "Crash Occurrence." **None outputs an explanation.** This is Chai
   2024's gap-by-omission, now corroborated by a second independent literature
   table, specifically for the road/region-level (CRM) family.

**Their stated future work** (Section 5): improve distributional assumptions,
extend prediction horizon. Nothing about explanation or condition-specific
output — our contribution is not on their roadmap either.

Tag: `home`+`borrow` ★ TOP FIND. Gap test: UNBEATEN — and this is the paper our
thesis should position against most directly. The replication baseline +
the dataset proof + the zero-inflation borrow, all in one open-access paper.

---

### 4. LLM-enhanced causal graph learning for real-time crash risk prediction
**Li, Huang, Zhou, Li, Zhou, Zhong — AAP 233 (2026) 108579 | Central South University, Changsha**

**What they built.** A closed-loop framework combining transfer entropy (TE)
causal discovery, GPT-2+LoRA semantic enhancement, and LSTM+GAT spatiotemporal
prediction for real-time collision risk in car-following scenarios. Data:
HighD dataset (UAV aerial trajectory, German highway, 2017–2018, 55 recordings,
90,748 vehicle trajectories). 240 dangerous car-following events identified
(TTC < 3s threshold), yielding 5,884 training samples (~10% hazardous).

**Three-component framework (LLMG+ST):**
1. *Transfer Entropy (TE) causal graph per event.* For each dangerous event,
   8 traffic variables (v_fol, acc_fol, v_pre, acc_pre, v_diff, acc_diff,
   distance, ttc) → 8×8 TE matrix with variable-delay formulation →
   significance thresholding (θ=0.01, p<0.05) → initial directed causal graph
   G₀. Most influential variables: acc_pre, acc_fol, v_pre. Most common causal
   edges: v_pre→distance (33 occurrences), v_pre→ttc (28 occurrences).
2. *GPT-2 (0.78B) + LoRA (rank=16, scaling=32) Causal Enhancement Agent.*
   Structured prompt encodes: current graph stats, safety rules (TTC<3s =
   high risk, safe headway ≥ 2s), driving knowledge, highway context. LLM
   adjusts edge weights to produce enhanced graph G̃. Key enhancement: strengthens
   acc_pre→ttc, v_pre→ttc, acc_diff→ttc paths; suppresses non-critical edges.
   LoRA applied only to feedforward layer; A initialized N(0,σ²), B=0.
3. *LSTM+GAT spatiotemporal prediction.* LSTM captures temporal dynamics from
   trajectory sequences (window=100, prediction=30 frames); GAT encodes graph
   structure from G̃ edge weights; feature fusion → collision risk prediction.

**Results.** LLMG+ST: Accuracy=0.956, F1=0.872, AUC=0.985, Precision=0.832,
Recall=0.916. vs baselines: LSTM F1=0.474, GRU F1=0.448, CNN-LSTM F1=0.438,
GCN F1=0.467. Ablation: No-LoRA drops F1 to 0.811 (LoRA refinement is
essential); No-LSTM drops F1 to 0.262 (temporal features are critical).
Inference latency: 5–15ms per sliding window (well within 500ms real-time
requirement).

**The stated limitation (directly useful for us).** "Causal graphs were
constructed independently for each event and did not evolve with traffic
dynamics... the current framework relies mainly on basic driving variables
from the ego and leading vehicle, while excluding external factors such as
weather and road geometry." This is exactly our expansion axis: our system
CONDITIONS on weather and road geometry, not on vehicle kinematics.

**Does it beat the gap? NO.** Four reasons:
1. *Event-level, not segment-level.* Each dangerous car-following event gets
   its own causal graph. There is no segment, no historical crash record,
   no overrepresentation test.
2. *No condition-conditioning.* The 8 variables are all vehicle kinematics
   (speed, acceleration, TTC, distance). Weather, road surface, time-of-day,
   season — none appear. Their own limitation statement admits this gap.
3. *No NL output to humans.* The "interpretability" is the enhanced causal
   graph structure — edge weights on an 8-node DAG. No natural-language
   statement is generated or validated. The LLM refines graph topology;
   it does not produce text for a person.
4. *Real-time AV decision support, not human driver advisory.* The output is
   a collision risk score (binary: safe/hazardous) for an automated system.

**What this hands us (`related-work`+`borrow`):**

1. *LoRA precedent now in AAP itself (2026).* After TrafficRiskGPT (KBS 2025),
   this is a second independent paper using LoRA fine-tuning for traffic risk
   in a top venue. The methodological choice is validated twice over.

2. *Transfer entropy as a significance measure for causal structure.* TE
   identifies which variable relationships are directionally significant under
   a permutation-based p-value (their Eq. 3). This is adjacent to our
   chi-square significance gate — both are statistical tests for the question
   "is this association real?" TE captures nonlinear and directional
   information flow; chi-square tests categorical overrepresentation. Citable
   as evidence that significance-gated structure learning is mainstream.

3. *The most common causal paths (acc_pre→ttc, v_pre→ttc) are intuitive and
   validate the general pattern*: upstream conditions (leading vehicle behavior)
   propagate to risk downstream. Our system does the same for environmental
   upstream conditions.

4. *Their limitation = our novelty.* The paper explicitly names "weather and
   road geometry" as the missing variables. Our system adds exactly those.
   This is a citable gap statement from a peer-reviewed paper in our journal.

Tag: `related-work`+`borrow`. Gap test: UNBEATEN. LoRA precedent #2 (after
TrafficRiskGPT); their limitation statement directly frames our contribution.

---

## Abstract-only — triaged, worth citing

- **Crash root-cause identification via trace-rewarded causation chain
  reasoning large language model**
  *DeepSeek-R1-Distill-Qwen-1.5B + MCTS + GRPO on MM-AU video/crash dataset.
  Identifies root-cause CATEGORIES (micro accuracy 0.870, macro recall 0.852)
  from crash reports — not NL prose output to a driver. Per-crash, event-level
  classification. Brick #7 of "LLM applied to crashes, validates the label
  not the reasoning chain." `related-work`.*

- **Network-wide road crash risk screening: A new framework**
  *Risk = probability × vulnerability × exposure per road segment → five-level
  classification → ranked network-wide list. Province of Brescia, Italy; non-urban
  network; 5 years crash data. Proactive (predicts before crashes occur). No
  condition-conditioning, no NL explanation. THIS IS the home-field method
  stated plainly — shows exactly what network screening outputs (a ranked
  numeric score per segment) and what is missing. `home`/`related-work`. Gap
  unbeaten.*

- **Integrating pavement condition records with LLM-based crash narrative
  analysis for pavement safety assessment**
  *LLM parses police narratives → mechanism-specific labels (hydroplaning,
  curve-related loss of control) → quantile regression on pavement condition +
  friction + texture + traffic + geometry → identifies high-risk segments. Third
  venue (after Li 2025, Tab-Text 2025) confirming NL-as-INPUT: narratives go in
  as features, a risk score/distribution comes out, no NL for drivers. Segment-
  level application in AAP itself. `related-work` (NL-as-INPUT in home journal).
  Gap unbeaten.*

- **A spatially adaptive empirical Bayes framework with dynamic dispersion
  parameters for enhanced crash frequency prediction across rural highway networks**
  *SA-EB: EB + Geographically Weighted Poisson Regression + MGWR + CMFs.
  Iran rural divided multilane highways; 1071 km; 2995 crashes 2017–2019.
  Dynamic overdispersion (0.3–0.6) captures spatial variability. Slope and speed
  deviation are key predictors. 20% crash reduction with EB-guided improvements.
  Output: expected crash frequency per segment (numeric). Confirms EB/HSM method
  remains the state-of-practice baseline — still aggregate, not condition-
  specific, not NL. `home`/`related-work` (the baseline our system positions
  above). Gap unbeaten.*

- **Quantifying and comparing the effects of key risk factors on various types
  of roadway segment crashes with LightGBM and SHAP**
  *LightGBM vs XGBoost on Texas crash data 2015–2017; SHAP for factor
  importance by collision type (Rear-End vs Run-Off-Road). Significant factors:
  speed limits, area type, number of lanes, roadway functional class, shoulder
  width/type. Risk factor importance varies across crash types — lane width
  <12ft increases all crash types; speed limit more important for RE than ROR.
  Output: SHAP charts/tables (XAI without NL). `related-work`/`borrow` (SHAP
  for segment-level crash factor importance; specific factors match STATS19
  variables; interaction-effect framing). Gap unbeaten.*

- **Sentence-resampled BERT-CRF model for autonomous vehicle crash causality
  analysis from large-scale accident narrative text data**
  *BERT-CRF + BIO/C-P-R-D annotation + sentence resampling → causal movement
  chain (CMC) extraction from AV crash narratives → 5-category/52-element
  causal attribution framework (DREAM-inspired). 98.03% accuracy (complete),
  96.14% accuracy (10% sample). Rear-end (48.57%) and lane-change (17.04%) are
  highest-risk AV scenarios. NL-as-INPUT: narratives → structured causal labels.
  AV-specific. `related-work`/`borrow` (sentence resampling for imbalanced
  crash narratives; BERT-CRF for crash entity/behavior extraction; DREAM causal
  attribution category framework). Gap unbeaten.*

- **Optimizing crash risk models for freeway segments: heterogeneous effects of road geometric
  design features, traffic operation status, and crash units**
  *Segment-level crash risk prediction on Yongtaiwen Freeway (Zhejiang, China) with widely-spaced
  detectors. Latent Class Analysis (LCA) + Latent Profile Analysis (LPA) classify segments into
  subgroups by geometric features and traffic operation status; binary/conditional logit + grouped
  random parameter logit models fit per subgroup. Finding: combined geometric+operational
  heterogeneity model performs best; grouped random parameters beat conditional logit for
  unobserved heterogeneity. CRM on freeway segments — but "conditioning" = road geometry
  classification, not live weather/time conditions. Output: crash risk prediction paradigm for
  traffic safety management departments (numeric). `home`/`related-work`. Gap unbeaten —
  another CRM baseline paper, no condition-conditioning in our sense, no NL.*

- **Does connected vehicle information reduce beyond-visual-range crash risk in foggy freeway
  conditions? A study based on extreme value theory**
  *Driving simulation experiment: traditional environment (no CVI) vs connected environment (CVI)
  in a foggy freeway beyond-visual-range scenario. EVT (peak-over-threshold → generalized Pareto
  distribution) applied to TTC, MTTC, PET, DRAC conflict indicators. Finding: CVI significantly
  reduces crash risk in foggy beyond-visual-range conditions; DRAC-based EVT models have best
  fit; effectiveness varies across driver groups. Not CRM — no segment-level risk, no historical
  patterns. BUT: strongest empirical evidence found in AAP that providing drivers with
  condition-specific information (here: fog + CV data) produces measurable safety benefits.
  Direct support for the "why does driver-facing condition-specific risk information matter?"
  motivation argument. `background`/`related-work`. Gap unbeaten.*

- **Roadway traffic crash during extreme heat days: insights from hazards-exposure-vulnerability-
  adaptation**
  *Condition-conditioned segment-level crash rate analysis: extreme heat thresholds (90th/95th/97th
  percentile daily max temp 2011–2015) × roadway segments in Miami, Florida. CatBoost + SHAP
  identifies which road features correlate with higher/lower crash rates on extreme-heat days.
  Finding: crash risk shows threshold-dependent pattern — moderate extreme heat has adaptive
  buffers, very extreme heat (97th pct) overwhelms them; roadway investment (construction cost,
  geometric design) is primary protective factor. Condition (weather extreme) × segment-level
  crash rate = the CRM paradigm applied to temperature. CatBoost+SHAP stack mirrors our approach.
  Output: numeric crash rate models + SHAP importance charts. `home`/`related-work`. Gap
  unbeaten — no NL, no significance gate, no driver-facing output.*

### Keyword 3 (`driver risk information`) — delivery/communication + LLM gap-test

The keyword pulled almost entirely the driver-behavior / cognition / human-factors
cluster (~85 off-layer: naturalistic driving, take-over performance, distraction,
fatigue, hazard perception, risk-attitude profiling — driver-level or real-time,
not segment-level CRM). But it surfaced a NEW grounding axis the rest of the sweep
lacked: **how risk should be delivered/communicated to a driver** — the consumer
side of our NL output. 5 abstracts recorded below; none warrant full text.

**Delivery / communication cluster (new grounding for the output-consumer side):**

- **Tailoring in risk communication by linking risk profiles and communication
  preferences: speeding of young car drivers**
  *Survey of 1168 German drivers 17–24. Segments drivers into 4 motivational risk
  groups, links each to distinct communication preferences/media habits → tailoring
  strategy for road-safety campaigns. Validates that TAILORED risk communication to
  drivers is an established, effective practice — grounds WHY delivering risk as
  targeted language (vs a uniform number) has value. Not CRM, not gap-relevant;
  the motivation anchor for the NL-output-to-driver argument. `background`/
  `related-work` (delivery side).*

- **Personalizing In-Vehicle warnings: A causal machine learning approach to
  optimizing workload and risk perception**
  *3×3×5 driving-simulator factorial (52 drivers); Double Machine Learning +
  Causal Forests (DML-CF) on warning modality × lead time → driver workload +
  perceived risk. Finding: moderately early (5.5–6.5s) congruent dual-modality
  warnings reduce workload/perceived-risk; delayed/single-modality increase
  cognitive demand; strong heterogeneity across driver subgroups (CATE). Grounds
  the delivery TIMING/MODALITY design for risk info, and the DML-CF method is a
  borrowable causal-effect tool. `background`/`borrow` (delivery design +
  heterogeneous-effects method).*

- **Investigating the impact of in-vehicle warning information complexity on
  drivers: working memory capacity and cognitive load**
  *4×2×2 simulator study (37 participants), eye-tracker + heart-rate. Visually-rich
  warnings INCREASE braking reaction time — worst for low-working-memory drivers
  under high cognitive load; detailed warnings raise tension (lower RMSSD);
  visually-simple + auditorily-rich is best for fast risk perception. THE direct
  design constraint on our NL output: a driver can only absorb so much detail —
  explanations must be short and low-complexity, not paragraphs. Most useful of
  the delivery cluster. `background`/`related-work` (NL-output complexity
  constraint).*

**LLM-applied-to-driving-risk (gap-test bricks — both confirm the gap holds):**

- **DRPVLM: A generative multimodal large language model for real-time driving
  risk prediction**
  *LoRA-fine-tuned multimodal LLMs (Qwen-2.5-VL 32B/7B/3B, Gemma-3-12B,
  Llama-3.2-11B-Vision) extract road/traffic/driver-state features from Shanghai
  Naturalistic Driving Study video → LSTM → real-time risk prediction. Qwen-32B
  acc 0.89–0.92, F1 0.88–0.91, beats structured-trajectory-only baseline (<0.7
  at long horizons). LoRA PRECEDENT #3 in AAP (#4 overall: Gyawali, TrafficRiskGPT,
  Li et al., now DRPVLM). BUT: real-time, driver-state/behavior level; the LLM
  extracts FEATURES (NL-as-INPUT again); output = a risk number, not NL to a
  driver; no segment, no condition-conditioning. Gap unbeaten. `related-work`+
  `borrow` (LoRA precedent; LLM-as-feature-extractor).*

- **Integrating visual large language model and reasoning chain for driver
  behavior analysis and risk assessment (DDLM)**
  *Visual LLM + whole-body pose estimation + reasoning-chain framework → distracted-
  driving classification with "reasoned explanations" + risk levels. 100-Driver
  dataset; beats standard models zero/few-shot. Generates explanatory text — BUT
  it's distraction CLASSIFICATION (driver-behavior, event-level), and (tellingly)
  reports NO faithfulness validation of the reasoning chain ("better
  interpretability" claimed qualitatively). Another "generate explanation, never
  validate it" brick — now extended to driver-behavior VLMs. Not segment, not
  condition-conditioned. Gap unbeaten. `related-work`.*

**Net:** keyword 3 added the delivery/communication grounding axis (3 refs) that
completes the pipeline story — risk modeling (Gao/Wei/Wang) → NL generation
(Wu/Zhang/Hussien/Smetana) → **delivery to drivers (these 3)** — plus 2 LLM
gap-test bricks (LoRA precedent #3; "explain-never-validate" extended to driver
VLMs). Gap test UNBEATEN. **AAP complete.**

---

## Skipped at title stage (off-layer)

~80 of ~100 results. AAP is on-domain so noise is finer-grained than AI venues
— almost every paper involves crashes, but most fall into:

**CSM-heavy (injury severity focus)** (~25): pedestrian/cyclist/taxi/AV/
e-scooter/novice driver/elderly severity models; mixed logit / random parameters
logit / multinomial logit for severity classification; temporal instability in
severity models; attire-in-nighttime-crashes type niche papers.

**Behavioural / human factors** (~15): distraction (mobile phone, daydreaming),
gap acceptance at roundabouts, aggressive driving, sensation seeking, novice
drivers — modelling individual behaviour, not segment risk.

**Geometry / alignment specific** (~10): curve alignment types on mountainous
freeways, ramp influence area definition, segment length optimization, passing
zone CMFs, run-off-road at curves — relevant to the SPF family but too narrow/
niche for context-grounding; not condition-specific in our sense.

**Real-time COM from trajectory / conflict data** (~6): conflict-based
intersection crash risk, pre-crash vehicle trajectories, near-crash from LiDAR
— microscopic event-level, not segment-level historical pattern.

**Policy / intervention evaluation** (~5): license plate restrictions, L-category
quadricycles future-safety simulation, HAD deployment scenarios — evaluating
external interventions, not modelling segment risk.

**Misc niche** (~10): taxi bibliometric review, tram crashes in Japan, e-scooter
built-environment typology, freight truck satellite imagery, bicycle lane types
— valid road-safety papers but off our positioning scope.

---

## Tag legend

`home` / `integration` / `related-work` / `borrow` / `background` / `skip`
