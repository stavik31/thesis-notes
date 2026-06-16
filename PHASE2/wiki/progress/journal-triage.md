---
title: "Journal Triage Log — Phase 2 Reading"
type: progress
date: "2026-06-09"
tags: [progress, literature-review, phase2]
---

# Journal Triage Log

Running record of the journal-by-journal reading sweep. One section per journal.
Workflow per journal: **search → shortlist titles → read abstracts (decide) → full
text for keepers only → deep-read + ingest.** Tags: `home` / `integration` /
`related-work` / `borrow` / `skip`.

See [[PHASE2/PLAN]] for the journal order and search terms.

---

## Tier 1

### IEEE T-ITS (#20) — ✅ complete (2026-06-09)

Searched on IEEE Xplore; titles triaged 2026-06-09. **Abstracts pulled for the shortlist
below; everything else from the result set skipped at title stage.**

| Status | Paper (year) | Tag | Why kept |
|---|---|---|---|
| ✅ abstract done | Leveraging Textual Description & Structured Data for Crash Risk of Traffic Violation — Multimodal (Li, Ma, Zhou, Lord, Zhang, 2025) | `related-work` | Closest methodological twin: text+tabular+LLM features for crash risk. Different purpose (violation classification vs. segment profiling) — must cite and position against. → **FULL TEXT** |
| ✅ abstract done | Driving Safety Risk Analysis & Assessment in Mixed Driving — Systematic Survey (Cheng et al., 2025) | `background` | AV/CAV-focused — less useful than expected. Skim for risk-assessment vocabulary only. → abstract only |
| ✅ abstract done | Automated & Explainable AI for Pedestrian Injury Severity (Antariksa, Tamakloe, Das, 2025) | `related-work`/`borrow` | Parallel to Phase 1 (XAI + severity); SHAP framing borrowable. → abstract only |
| ✅ abstract done | Vehicle-Group-Based Crash Risk Prediction & Interpretation (Zhu…Abdel-Aty, 2025) | `related-work` | Real-time trajectory data, too microscopic/off-path; cite Abdel-Aty as field anchor. → abstract only |
| ✅ abstract done | Safe Route Mapping of Roadways Using Multiple Sourced Data (Jiang et al., 2022) | `integration`/`home` | Best application anchor: segment-level SPF + heat maps + route/trip planning. Their gap = no condition-specificity, no NL — exactly where my method plugs in. → **FULL TEXT** |
| ✅ abstract done | In-Vehicle Warning Information Provision Strategy, V2V (Jo et al., 2022) | `related-work` | Tackles the when-to-warn / distraction problem directly; formal CDR/DFR/IPR framework useful for delivery argument. → abstract only |
| ✅ abstract done | Wasserstein GAN for Imbalanced Real-Time Crash Risk (Man, Quddus et al., 2022) | `borrow` | UK M1 data, same Fatal-class sparsity problem; WGAN method directly borrowable. Quddus = credible UK crash author. → abstract only |

**Skipped at title stage (off-layer — micro AV control / motion planning / driver-state):**
Driver-Oriented Active Intervention Control (2026); Perceptual Uncertainty-Aware Motion
Planning (2025); Risk-Informed Speed Limits (2024); Pedestrian-Vehicle Conflicts
probabilistic framework (2023); CAMV crash alarm (2023); Traffic-Simulation human-error
modeling (2023); Cooperative Vehicle Merging SAC (2023); Risk Representation in Lane-Change
Decision (2022); Attention-Based Lane Change Risk (2022); Probabilistic Risk Metric for
Highway Driving (2022); Driver Behavior Profiling (2022); Real-Time Cycle-Level Intersection
Risk (2021); Using Crash Databases for AV Maneuvers (2021); Forecasting
Habitual Driving Behaviors (2020); Cost-Sensitive Autoencoders imbalanced (2020).

**Decision after abstracts:** #1 (Multimodal) and #5 (Safe Route Mapping) → full text.
All others → abstract only. 2 keepers on merit — could be more or fewer for other journals.

**Outcome:** both full texts read 2026-06-09 and recorded in
`../../raw/papers/tier1_journal1/T-ITS-abstract-refs.md`. T-ITS sweep complete.
Sharpened gap: field does encode→predict (event-level, Li 2025) OR aggregate→score+map
(segment-level, Jiang 2022); neither condition-conditions nor explains *why* in NL. **Next
journal: Expert Systems with Applications.**

**Additional keyword sweep (2026-06-11) — `hotspot identification`:** 3 results, all
skipped at title stage (airspace clustering — off-domain; intersection trajectory-conflict —
micro/off-layer; maritime IoT data integrity — unrelated). **0 keepers.** Confirms the
plan's expectation: hotspot ID / network screening is an AAP/AMAR-family topic, not a
T-ITS one. T-ITS verdict unchanged.

**Additional keyword sweep (2026-06-11) — `risk-aware routing`:** 3 results; 2 skipped at
title stage (eco-routing — energy not safety; drone delivery — off-domain). 1 abstract
reviewed: *Safe and Sound* (de Souza et al., 2020) — risk-aware re-routing but for
*criminal*, not crash, risk; RNN dynamic score → routing. Abstract-only, tagged
`related-work`/`integration` (recorded in `T-ITS-abstract-refs.md`). Another gap-confirming
brick; no full text. T-ITS verdict unchanged.

**Additional keyword sweep (2026-06-11) — `LLM transportation`:** ~313 results (keyword too
broad — "transportation" pulls drones/maritime/telecom); triaged top ~50 by relevance.
~38 skipped at title stage (AV control/planning, signal control, dispatch/VRP, cybersecurity,
off-domain). 6 abstracts reviewed → 4 abstract-only + **1 full-text deep read** + 1
full-text-then-knocked-down:
- **Zhang et al. 2025 (ITSC), Reflective LLM Prompt Optimisation** → DEEP READ. First real
  grounding for the *explanation layer*: names our "fluent-yet-unfaithful" problem, gives a
  validate-then-explain architecture + 3 faithfulness dimensions we can borrow. We can beat
  their LLM-judge validity gate with a real statistical significance test. Tag `borrow`/`related-work`.
- **Gyawali et al. 2025 (SPW)** → full text read, knocked down. Near-mirror of our Phase 1 stack
  (XGBoost→SHAP→RAG→LLM→NL) but a thin demo with no explanation eval. Architecture-mirror evidence.
- Mahmud 2025 (T-ITS survey, gap-by-omission), LLeCaT 2025 (LLM on accident text, wrong direction),
  Hassan 2025 (bibliometric), Bagosher 2025 (LLM-routing, input-parsing) → all abstract-only.
- **Net effect:** generic "LLM explanation layer" is now established PRIOR ART (Zhang + Gyawali) →
  our explanation novelty narrows to *condition-conditioned, significance-gated* segment crash-risk
  explanation. Gap test still unbeaten: no one does condition-conditioned segment risk. **T-ITS
  sweep now genuinely exhausted across all planned keywords. Next journal: Expert Systems w/ Applications.**

---

## Tier 1 — Journal 2: Expert Systems with Applications (#7) — ✅ complete

Search terms: `crash severity prediction`, `road safety decision support`, `accident risk
machine learning`. Carry the test question: *is anyone doing condition-conditioned,
explanation-generating segment risk?*

**Keyword 1 (`crash severity prediction`), 2026-06-11:** ~29 results, triaged at title
stage → 4 abstracts pulled, recorded in `../../raw/papers/tier1_journal2/ESWA-abstract-refs.md`:
- **Tab-Text (Zhen & J.J. Yang, 2025, ESWA)** → **DEEP READ**. The closest input-pipeline
  twin found yet: template-generated tabular→narrative→ELECTRA multi-modal severity
  classifier on Victoria CrashStats (same ~1.6% fatal imbalance as STATS19). Narrative
  nearly doubles fatal-class accuracy (9.63% vs 5.25%); ablation confirms text helps most
  on rare classes. **Establishes our tabular-to-text step as prior art** (2nd venue after
  Li) → novelty narrows to the join: NL-as-OUTPUT × condition-conditioned segment × 
  significance-gated. Their NL is an input feature, never shown to a human; ours is the
  deliverable — the cleanest distinction we now hold. Tag `related-work`+`borrow`.
- NLP/text-mining transportation survey (Zhang et al., 2026), macro/micro CPM combination
  (Rúa et al., 2024), PST-CGCN causal GCN crash risk (Hu et al., 2025) → all abstract-only.
  Rúa is a useful second domain anchor for the "aggregate→score" CPM family alongside
  Jiang 2022.
- ~21 skipped at title stage (AV control/ethics/RL, microscopic conflict/trajectory,
  detection/sensing, pure forecasting, severity-only ML without condition/explanation
  framing, off-domain "crash" hits).
- **Next:** read Tab-Text full text, then continue with keywords 2-3 (`road safety
  decision support`, `accident risk machine learning`).

**Keyword 2 (`road safety decision support`), 2026-06-11:** ~79 results (broad — pulled
heavy MCDM/DSS noise from mining/construction/freight + ~10 duplicates of keyword 1).
3 abstracts → 1 deep read. Recorded in `../../raw/papers/tier1_journal2/ESWA-abstract-refs.md`:
- **Hussien et al. 2025 (KG+LLM+RAG explainable behavior prediction)** → DEEP READ. The
  strongest, most rigorous explanation-layer system seen (Sotelo group), NOT knockable.
  Makes LLM-explains-ML prior art across 3 papers — but, like the others, never validates
  the explanation (qualitative only). Strengthens our significance-gated angle + perfect
  contrast (they suppress hedging / assert causation; we require association language). AD
  behavior prediction → gap-test unbeaten on every axis. `related-work`+`borrow`.
- Sarraf & McGuire 2020 (MCDM safe route planner) → abstract-only, `integration` (route
  planning is a real consumer slot for our risk score). SSARA 2026 → `skip` (term-collision).

**Keyword 3 (`accident risk machine learning`), 2026-06-11:** ~52 results, ~11 duplicates
of kw1/kw2, heavy off-domain noise (maritime/aviation/insurance/mining/construction —
"accident risk" is a much broader net than "crash"). 3 abstracts, all abstract-only
(no full reads): railway-accident-report KG (`related-work`/`background`, cross-domain
text→KG→risk precedent, pre-LLM), RACI aviation RAG+LLM causal-passage-retrieval
(`related-work`/`borrow`, rare quantitatively-validated RAG), road-domain small-sample
ensemble cause-analysis (`borrow`, alt. to WGAN for fatal-class imbalance). Gap test
unbeaten.

**RACI follow-up (full text), 2026-06-11:** pulled to check whether its mAP/mNDCG=
0.815/0.761 was a validated faithfulness metric for the generated explanation —
it isn't. Those metrics validate only the *Retriever* (categorical-taxonomy
similarity via NTSB's coding hierarchy); the generation step (analogous to our NL
output) is purely qualitative, zero metric. Knocked down from deep-read — now
brick #4 of "generate explanation, never validate it" (4 papers / 4 domains).
Reinforces, doesn't fill, our gap. `related-work`/`borrow` (retrieval-similarity
heuristic, SBERT robustness recipe — tangential).

**ESWA outcome:** all 3 keywords done, 2 deep reads (Tab-Text, Hussien) + 8 abstract-only
refs (1 knocked down from full read), recorded in
`../../raw/papers/tier1_journal2/ESWA-abstract-refs.md`. Next journal:
**Engineering Applications of AI** — search terms `traffic accident prediction`,
`road risk assessment AI`.

---

## Tier 1 — Journal 3: Engineering Applications of AI (#8) — ✅ complete

Search terms: `traffic accident prediction`, `road risk assessment AI`.

**Keyword 1 (`traffic accident prediction`), 2026-06-11:** ~95 results, dominated by
pure traffic-flow/speed forecasting + AV/maritime/aviation noise (the term pulls
"traffic"+"prediction" broadly). 5 abstracts → 1 deep read + 1 abstract-level + 3
abstract-only. Recorded in `../../raw/papers/tier1_journal3/EAAI-abstract-refs.md`:
- **Chai et al. 2024 (95-study systematic review of ML RTA prediction)** → DEEP READ,
  the find of this journal. A POSITIONING GIFT: gives the field's 4-category taxonomy
  (CRM/COM/CSM/CFM) and the term for what we do — **CRM = Crash Risk Modeling**
  (segment-level risk). CRM is the LEAST-explored category (8%), and all its exemplars
  output a numeric score, none NL. NL/explanation communication is not even one of
  their 5 future directions → quantified gap-by-omission. Borrow: imbalance synthesis,
  data-source breakdown, the taxonomy as related-work skeleton. `related-work`/`home`-mapping.
- **Smetana et al. 2026 (LLM categorization of OSHA highway-construction accidents)** →
  DEEP READ (full PDF). The explanation-OUTPUT-validation cousin — first paper in the
  sweep that actually validates LLM summary faithfulness with a computed metric:
  SelfCheckGPT-style fact-consistency check (Eq. 7), 83% consistent (1551/1860 facts).
  It STACKS with, rather than threatens, our gap: their check = "prose faithful to
  source?" (output axis); our significance gate = "pattern statistically real?" (input
  axis). Doesn't beat the gap (construction domain; clusters are semantic-similarity not
  condition-stratified segment risk; descriptive summaries, no overrepresentation test).
  Heaviest BORROW of the sweep: gives us a cited output-validation layer to adopt +
  improve. Refines our story → "we borrow their output check AND add the significance
  gate they lack." `related-work`+`borrow`.
- Abstract-only: driving-risk arterial/collector (Entropy-TOPSIS+K-means labels, DCGAN
  imbalance — `borrow`); Deep Forest+SHAP freeway crash risk (`related-work`/`borrow`);
  PM-Transformer near-crash real-time (`related-work`, redundant w/ Abdel-Aty sub-lit).
- Skipped at title stage: ~63 (pure flow forecasting, AV micro-control, maritime/air,
  signal-control RL, off-domain, incident-duration/detection sub-lit).
- **Next:** EAAI keyword 2 (`road risk assessment AI`).

**Keyword 2 (`road risk assessment AI`), 2026-06-11:** ~67 results, **0 keepers**.
"Risk assessment" is too generic a term for a general engineering-AI journal —
pulled almost entirely cross-domain noise (geotechnical/landslide/embankment,
occupational safety/FMEA, fuzzy-MCDM methodology papers, maritime/pipeline/energy,
AV/ADAS micro-layer, pavement/infrastructure). 1 duplicate (Chai 2024, already
read). 4 marginal titles considered and dropped (counterfactual-KG interpretable
project-risk-management, explainable driving-behavior CPS, ShapG SHAP-variant,
cross-city traffic-network resilience via transfer learning) — none strong enough
to outweigh diminishing returns on an already-saturated explanation layer.

**EAAI outcome:** 2/2 keywords done, 2 deep reads (Chai, Smetana) + 3 abstract-only
refs, recorded in `../../raw/papers/tier1_journal3/EAAI-abstract-refs.md`. Next
journal: **Knowledge-Based Systems** — search terms `crash prediction`, `risk
assessment framework`, `knowledge extraction traffic`.

---

## Tier 1 — Journal 4: Knowledge-Based Systems (#5) — ✅ complete

Search terms: `crash prediction`, `risk assessment framework`, `knowledge
extraction traffic`.

**Keyword 1 (`crash prediction`), 2026-06-11:** ~110 results, ~100 off-domain
(KBS is a general-AI venue — finance, cybersecurity, robotics, generic ML
methods dominate). 8 abstracts reviewed, recorded in
`../../raw/papers/tier1_journal4/KBS-abstract-refs.md`:
- **TrafficRiskGPT** (Zhong et al. 2025, LLaMA3-8B + LoRA + RAG + CI-CoT for AV
  scene risk) → **DEEP READ**. The closest near-miss of the whole sweep — but
  doesn't beat the gap: CI-CoT's NL reasoning is agent-consumed (action
  selection), scene-level (kinematic-conditioned), and unvalidated for
  faithfulness (DriveScore/collision-rate are task metrics, not faithfulness
  metrics). Brick #5 of "explain, never validate." Hands us (1) our sharpest
  LoRA-architecture-validation precedent yet, and (2) a principled,
  mechanism-level justification for "association not causation" — true causal
  inference (DAG+backdoor+ATE) doesn't scale from one scene to
  population-level segment×condition risk.
- 6 abstract-only: imbalance-shelf additions (SMOTE comparison study, Heinrich
  accident-triangle weighted oversampling), CRM+XAI exemplar (CAV motorway
  heatmaps + saliency, still no NL), feature-selection borrow (WFFS), 2 more
  CSM deep-architecture confirmations (railway causation transformer,
  CNN+BiLSTM+attention severity).
- 1 term-collision skip (RENBOOT — "significance analysis" = regression-
  coefficient robustness for mechanical design DOE, unrelated to our gate).
- **Next:** keyword 2 (`risk assessment framework`).

**Keyword 2 (`risk assessment framework`), 2026-06-12:** ~108 results, **0 new
keepers** — 1 dup (the title hit is TrafficRiskGPT's full title, already
deep-read under keyword 1). Rest is off-domain noise (finance/credit/audit,
medical risk, industrial/construction/oil-gas safety, cybersecurity, and a long
tail of generic "X framework" papers with no transport content). 2 marginal
titles considered and dropped (supply-chain-explainability SLR — different
domain, stretch citation; risk-informed road-infrastructure design —
climate/structural, not crash risk). Mirrors EAAI keyword 2's 0/67 — "risk
assessment framework" is too generic for a general-AI venue. Recorded in
`../../raw/papers/tier1_journal4/KBS-abstract-refs.md`. **Next:** keyword 3
(`knowledge extraction traffic`).

**Keyword 3 (`knowledge extraction traffic`), 2026-06-12:** ~100 results. 2 dups
(Alhaek severity CNN+BiLSTM and the proactive-DSS imbalance paper, both from
kw1; the road-infrastructure paper dropped in kw2). 1 abstract reviewed,
recorded in `../../raw/papers/tier1_journal4/KBS-abstract-refs.md`:
- **A Real-Time Explainable Traffic Collision Inference Framework Based on
  Probabilistic Graph Theory** (Liu, Lan, Guan, 2021) — abstract-only. Real-time
  collision-occurrence prediction (event-level COM) from social-media traffic
  features; "explainable" = the causal probabilistic graph itself (BDeu-score
  Bayesian-network structure learning), a THIRD explanation form (alongside
  saliency maps and NL narratives) — never NL, never segment-conditioned.
  P/R/F1≈0.75 validates the prediction, not the graph-as-explanation. `related-
  work` (confirms COM/CRM split) + `borrow` (BDeu/BN structure learning as a
  possible alternative/complement to the significance gate — added to the
  statistical-methods shelf next to Empirical Bayes; full-text deferred to the
  significance-gate design phase).
- Rest of ~100: traffic-FLOW forecasting (GCN/transformer/Mamba spatiotemporal
  variants, ~45); network/cyber "traffic" — malicious-traffic detection, IDS,
  encrypted-traffic classification (~25); AV perception/ATC/signal-control
  off-layer (~15); generic NLP/KG/CV (~15). Gap unbeaten.

**KBS outcome:** all 3 keywords done — 1 full-text deep read (TrafficRiskGPT,
closest near-miss of the entire sweep), 7 abstract-only refs total, 1
term-collision skip. Gap test unbeaten throughout. **Tier 1's core four
journals (T-ITS, ESWA, EAAI, KBS) are now all complete.** AAP/AMAR remains the
optional/deferred parallel track (primary CRM literature — RiskCast/DeepRisk/
Li 2020/Zhao 2019-type papers Chai cites secondhand). Otherwise, next up is
Tier 2 (application-context & framing venues — Smart Cities, Decision Support
Systems, IJDRR, IoT/Sensors, Advanced Engineering Informatics).

---

## AAP — Journal 5: Accident Analysis & Prevention — ✅ complete

Search terms: `road segment crash risk`, `crash risk assessment`, `driver risk
information`. Context-first keywords chosen (not technical SPF/EB terms) to
ground the system before going narrow.

**Keyword 1 (`road segment crash risk`), 2026-06-12:** ~100 results, heavily
on-domain (AAP is the flagship road-safety venue — almost every paper involves
crashes, noise is finer-grained than AI venues). ~80 skipped at title stage
(CSM-heavy injury severity, behavioural/human-factors, geometry-specific niche,
real-time COM from trajectory/conflict, policy/intervention evaluation, misc
niche). 10 abstracts reviewed → 4 full-text + 6 abstract-only. Recorded in
`../../raw/papers/tier1_journal5/AAP-abstract-refs.md`.

**4 full-text reads (deep-read complete, 2026-06-16):**

| Status | Paper | Tag | Why kept |
|---|---|---|---|
| ✅ deep-read done | **Wei et al. 2024** — Modeling lagged impacts of hourly weather + speed on segment crash risk: space-time-stratified case-crossover, DLM+DLNM (AAP 195) | `home`+`borrow` STANDOUT | Segment × condition (precipitation/visibility/temp/speed) + temporal resolution + interpretable lagged-risk curves. Strongest methodological ancestor for our significance gate. Validates our exact condition-variable set. Lagged-impact narrative frames WHY drivers need advance warning. |
| ✅ deep-read done | **Wang & Wang 2025** — Causal relationship discovery: EKC Bayesian network on HuNing Highway (AAP 221) | `home`+`borrow` | EKC = expert knowledge + chi-square CI tests → BN structure + inference. Direct sibling of our significance gate (same statistical tool, different framing). Validates our conditioning variables (weather/temp/volume/time → crash probability) on 38,303 real highway records. |
| ✅ deep-read done | **Wu et al. 2026** — From crash reports to safer roads: VLM + DBSCAN + street-view diagnostics (AAP 228) | `related-work`+`borrow` | Furthest output-side predecessor: Grok 2 VLM produces NL safety diagnostics from crash narratives + diagrams → engineers. Different addressee (engineers, not drivers), different input (retrospective crashes, not condition conditioning) — but validates NL output quality in the crash domain (Spearman=0.864 vs expert annotations). DBSCAN spatial aggregation directly borrowable. |
| ✅ deep-read done | **Li et al. 2026** — LLM-enhanced causal graph learning for real-time crash risk (AAP 233) | `related-work`+`borrow` | GPT-2+LoRA refines TE-based causal graphs for car-following risk prediction. LoRA precedent #2 (after TrafficRiskGPT). Their explicit limitation: "excludes external factors such as weather and road geometry" — our contribution in a peer-reviewed sentence. Transfer entropy as a significance measure for causal links (adjacent to our chi-square gate). |

**Gap test across all 4:** UNBEATEN. No paper produces condition-conditioned,
significance-gated, NL explanation of segment crash risk delivered to a driver.

**6 abstract-only refs:** recorded in `AAP-abstract-refs.md`. Highlights:
- Network-wide crash risk screening paper (the home-field baseline stated plainly —
  what network screening outputs and what it's missing)
- SA-EB framework (EB/HSM remains state-of-practice — another baseline anchor)
- Pavement+LLM narrative paper (NL-as-INPUT confirmation #3 in the home journal)
- LightGBM+SHAP for segment crashes (SHAP-factor-importance borrow, Texas data)
- Crash root-cause via DeepSeek+MCTS (brick #7 of "LLM applied to crashes,
  validates label not explanation")
- BERT-CRF for AV crash causal chain extraction (sentence resampling borrow)

**Keyword 2 (`crash risk assessment`), 2026-06-16:** ~100 results, again heavily
on-domain with the same noise clusters (CSM injury severity, pedestrian/cyclist/
motorcycle-specific, geometry-specific, work-zone, AV micro-control, policy
evaluation). 6 dups of keyword 1 (#11/#13/#27/#56/#72/#92 in the title list).
5 abstracts reviewed → **1 full-text + 3 abstract-only + 1 skip**. Recorded in
`../../raw/papers/tier1_journal5/AAP-abstract-refs.md`.

**★ THE FIND — full-text deep-read complete (2026-06-16):**

| Status | Paper | Tag | Why it matters |
|---|---|---|---|
| ✅ deep-read done ★ | **Gao et al. 2024 — Uncertainty-aware probabilistic GNN for road-level crash prediction (STZITD-GNN), UCL SpaceTimeLab (AAP 208)** | `home`+`borrow` TOP FIND | **The direct STATS19 baseline.** First paper found that does road-level (segment) crash risk on UK STATS19 (DfT) in a real UK context (3 London boroughs). Severity-weighted risk score (minor/serious/fatal=1/2/3) + Zero-Inflated Tweedie to handle ~96% zero-inflation (= our exact sparsity problem). Output = numeric risk score + heat map; weather is an INPUT feature, not an output conditioning axis; no significance gate; no NL. **This is the replicate-and-improve baseline + the dataset/domain proof + a borrowable zero-inflation solution, all in one open-access paper.** Code on GitHub. |

The 3 abstract-only from kw2 (#52 freeway-segment LCA/LPA CRM; #21 CVI-in-fog
EVT driving sim — the strongest empirical "why driver-facing condition info
matters" evidence; #35 extreme-heat-days CatBoost+SHAP condition-conditioned
crash rates) + 1 skip (#96 MCFformer — target is crash-induced *delay*, not
crash risk; traffic-ops not CRM) recorded in the abstract-refs file.

**Why Gao 2024 settles the "baseline + context proof" question** (raised by user
2026-06-16): it simultaneously proves (a) the domain — UK STATS19 road-level CRM
is published in AAP, the flagship venue; (b) the technical baseline — current SOTA
outputs a severity-weighted probabilistic risk score per segment, rendered as a
heat map; and (c) the precise delta our system adds — condition-conditioned,
significance-gated, NL explanation. Their Table 1 (14 road/region crash models)
shows every prior model outputs a "score" or "occurrence," none an explanation —
corroborating Chai 2024's gap-by-omission for the CRM family from a second
independent source.

**Keyword 3 (`driver risk information`), 2026-06-16:** ~95 results, ~85 off-layer
(driver-behavior / cognition / human-factors — naturalistic driving, take-over
performance, distraction, fatigue, hazard perception, risk-attitude profiling;
driver-level or real-time, not segment-level CRM). Several dups of kw1/kw2. 5
abstracts → all abstract-only (no full reads). Recorded in
`../../raw/papers/tier1_journal5/AAP-abstract-refs.md`.

Surfaced a NEW grounding axis the rest of the sweep lacked: **how risk should be
delivered/communicated to a driver** (the consumer side of our NL output):
- *Tailoring risk communication (young drivers)* — tailored risk communication is
  established practice → grounds why NL-to-driver beats a uniform number.
- *Personalizing in-vehicle warnings (DML+Causal Forests)* — 5.5–6.5s dual-modality
  warnings optimal; delivery timing/modality design + borrowable causal method.
- *Warning information complexity (working memory / cognitive load)* — visually-rich
  warnings slow reaction esp. for low-WM drivers → the direct constraint that our NL
  output must be short/low-complexity, not paragraphs.

Plus 2 LLM gap-test bricks: *DRPVLM* (LoRA multimodal LLM real-time risk — LoRA
precedent #3 in AAP; LLM-as-feature-extractor, NL-as-INPUT, output is a number)
and *DDLM* (visual LLM + reasoning chain for distraction — generates explanations
but no faithfulness validation; "explain-never-validate" extended to driver VLMs).
Both gap-unbeaten.

**AAP outcome:** 3/3 keywords done. 5 full-text deep reads (Wei 2024, Wang & Wang
2025, Wu 2026, Li 2026, **★ Gao 2024 STZITD-GNN — keystone reference**) + 14
abstract-only. Gap test UNBEATEN throughout. The journal delivered the single most
important find of Phase 2 (Gao 2024, the UK-STATS19 baseline) plus the
delivery/communication grounding that completes the pipeline story (risk modeling →
NL generation → delivery to drivers). **Next: AMAR (optional) or Tier 2** — but
context-grounding is now effectively settled.

---

---

## Tier 2

### Decision Support Systems (#16) — 🔄 in progress

Search terms: `driver advisory`, `route decision support`, `risk warning system`.

**Keyword 1 (`driver advisory`), 2026-06-16:** ~16 results, almost entirely off-domain
("driver" pulled crowdfunding/business/golf drivers in a general DSS journal). 1 keeper,
recorded in `../../raw/papers/tier2/tier2_journal1/DSS-abstract-refs.md`:

- **Ryder et al. 2017 (ETH Zurich / U St. Gallen / Bosch IoT Lab) — Preventing Traffic
  Accidents with In-Vehicle Decision Support Systems: The Impact of Accident Hotspot
  Warnings on Driver Behaviour, DSS 99 (2017) 64–74** → **DEEP READ** ★.
  THE application-context home paper for the in-vehicle DSS framing. Complete in-vehicle
  DSS: FEDRO 266,000-accident dataset → DBSCAN hotspot ID (1,608 hotspots) → What/Why/
  Where contextual classification → Android warning app. 4-week field study, 57 drivers,
  170,000km, OBD-II braking events as DV. Key findings: (1) **no immediate effect** of
  warnings on driver behaviour — contradicts lab studies; (2) **significant learning
  effect over time** (cumulative exposure to same hotspot warning → safer braking,
  OR=0.892*** per additional exposure); (3) **Agreeableness** moderates effectiveness
  (low-Agreeableness / "reckless" drivers don't benefit). Gap test UNBEATEN: warnings
  are condition-agnostic (same "Dangerous Crossroad" regardless of weather/time/surface).
  No condition-conditioning, no significance gate, no NL statement. Our delta: condition-
  specific + significance-gated + NL sentence. The "no immediate effect" finding is our
  opening — hypothesis that condition-specific NL overcomes it. `integration`/`related-work`.

**Next:** keyword 2 (`route decision support`).

### Smart Cities (#21) — ✅ complete (2026-06-16)

Search terms: `urban road safety`, `risk map`, `smart mobility safety`.

**All 3 keywords, 2026-06-16:** 0 keepers across all 3 keywords (~40 titles reviewed).
The journal does not publish road crash CRM content. Noise profile:
- kw1 (`urban road safety`): pedestrian crossing behaviour, AV simulation, traffic
  anomaly detection, UAV transport, cycling safety alert (marginal, cycling-specific),
  micromobility, congestion prediction, EV driving assistance.
- kw2 (`risk map`): flood hazard map interfaces, smart city resilience review, sewer
  network ML, nighttime traffic light detection, cycling safety (dup), soil liquefaction,
  geotechnical predictive analytics, flood-resilient risk assessment, micromobility safety
  mapping (marginal), crime risk semantic reasoning.
- kw3 (`smart mobility safety`): cybersecurity/regulatory compliance, multimodal ML
  sensing, traffic calming simulator study, scooter-sharing problems, AV/cyclist street
  design, cyber-physical energy/mobility, cycling safety (dup), smart city characterization,
  urban energy planning, rural mobility, AV car-following safety, construction materials.

**Smart Cities verdict:** 0 keepers. Wrong journal for CRM.

---

## Links

- [[PHASE2/PLAN]] — journal order, tiers, search terms
- [[wiki/overview]] — Phase 2 thesis state
- [[wiki/progress/2026-06-09]] — Phase 2 kickoff
