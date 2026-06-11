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

## Tier 1 — Journal 4: Knowledge-Based Systems (#5) — 🔄 in progress

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
- **Next:** pull TrafficRiskGPT full text, then continue KBS keywords 2-3
  (`risk assessment framework`, `knowledge extraction traffic`).

---

## Links

- [[PHASE2/PLAN]] — journal order, tiers, search terms
- [[wiki/overview]] — Phase 2 thesis state
- [[wiki/progress/2026-06-09]] — Phase 2 kickoff
