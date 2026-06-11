# KBS — Tier 1, Journal 4 Reading Record

**Progress so far:** keyword 1 (`crash prediction`) triaged. 1 full-text deep
read (TrafficRiskGPT — the closest near-miss of the entire sweep). 6
abstract-only refs. 1 term-collision skip.

---

## Full-text (deep-read) — the keepers

- **Large Language Model Based System with Causal Inference and Chain-of-Thoughts
  Reasoning for Traffic Scene Risk Assessment (TrafficRiskGPT)** — Zhong, Huang,
  Wu, Luo, Yu, 2025 (KBS 319:113630; Guangdong University of Technology / South
  China Normal University)
  *Where it lies in the progress: the CLOSEST near-miss in the whole sweep —
  closer in architecture than Gyawali, closer in domain than Smetana. Doesn't
  beat the gap, but hands us our sharpest architecture-validation point AND a
  principled (not hedge-y) justification for our association-not-causation
  discipline.*

  **What they built.** An autonomous-driving decision-support system. Core =
  LLaMA3-8B fine-tuned with **LoRA** on a large traffic-risk dataset
  (HighwayEnv-simulated highway scenes — lane changes, cut-ins, congestion,
  emergencies). Wrapped with: (1) a knowledge base of NL scene descriptions
  (emergency/collision/congestion cases) embedded and HNSW-retrieved; (2) vLLM
  for inference acceleration (3.6x token throughput, 30-59% memory reduction);
  (3) a composite **DriveScore (DS)** risk-evaluation index — weighted sum of
  TTC, DRAC (deceleration rate to avoid crash), DSS (space/stopping-distance
  gap), and DC (driving comfort), Eq 6; (4) **CI-CoT (Causal Inference
  Chain-of-Thought)** — for each scene, build a causal graph (covariates X =
  nearby-vehicle kinematics → driving decision T → collision risk Y, Fig 13),
  apply the backdoor criterion to identify adjustment variables, compute the
  Average Treatment Effect (ATE, Eq 18) of each candidate decision, and fold
  this causal estimate back into the CoT reasoning chain (Algorithm 1) before
  the final decision.

  **Results.** Collision rate (Table 1): -47.73% vs DQN, -64.43% vs ChatGPT-3.5,
  -7.3% vs GPT-4o-mini. DriveScore: +39.40% over DQN, +31.07% over ChatGPT-3.5;
  TTC sub-score +42.69% over ChatGPT-3.5. CI-CoT vs CoT (Figs 15-16) compared
  only qualitatively: CI-CoT's reasoning explicitly traces causal effects of
  each candidate action ("Vehicle 672 ahead... could lead to a potential
  collision if I do not adjust"); CoT's doesn't.

  **Domain — the critical distinction.** Real-time, SCENE-level AV decision
  support (kinematic states of nearby vehicles → next driving action), not
  segment-level historical crash-pattern risk for human drivers. "Causal" here
  = Pearl-style do-calculus/ATE on a HAND-BUILT per-scene DAG over ~3-5
  kinematic variables (speed, acceleration, distance, ATE, action) — a
  completely different object from "is condition X overrepresented among
  historical crashes on segment Y."

  **Does it beat the gap test? NO — but the closest near-miss yet.** CI-CoT
  genuinely produces fluent NL reasoning that READS like an explanation. But:
  (1) it's consumed by the AGENT to select an action, never delivered to a
  human as "why this segment is risky"; (2) conditioning is on instantaneous
  vehicle kinematics, not environmental/temporal/segment conditions; (3) it's
  scene/event-level, not segment-level; (4) ZERO faithfulness validation of the
  CI-CoT text — DriveScore/collision-rate are TASK-outcome metrics, not
  explanation-validity metrics. **Brick #5 of "generate explanatory NL, never
  validate it"** — now 5 papers/5 contexts (traffic-GNN, V2X cyber, AD
  behavior, aviation, AD scene-risk) — and the closest-to-home one yet. Smetana
  2026 remains the sole exception.

  **Two things this paper hands us:**
  (1) **Sharper architecture validation than Gyawali's.** Our exact Phase 1
  fine-tuning method — LoRA on an open ~8B LLM — for traffic-risk reasoning is
  now independently published in a top venue. Not just "LLM-explains-ML is
  prior art" (already established) but "LoRA-fine-tuned-LLM-for-traffic-risk
  specifically is prior art."
  (2) **A principled justification for "association, not causation."** This
  paper shows what TRUE causal claims require: a hand-built DAG + backdoor
  adjustment set + ATE computation — tractable for ~3-5 kinematic variables in
  ONE scene, but does not scale to population-level segment×condition risk
  (you'd need a DAG for every weather×time×road-type×segment combination).
  Citing this gives us a CONCRETE, mechanism-level reason (not just an
  epistemic-humility hedge) for testing statistical ASSOCIATION/
  overrepresentation instead — a weaker but tractable and honestly-labeled
  claim.

  Tag: `related-work` (architecture validation, strongest LoRA precedent) +
  `borrow` (causal-vs-association discipline justification). Gap test: still
  UNBEATEN — but this is the highest-value near-miss of the entire sweep.

---

## Abstract-only — triaged, worth citing

- **A Proactive Decision Support System for Predicting Traffic Crash Events: A
  Critical Analysis of Imbalanced Class Distribution**
  *Real-time crash/no-crash (COM) from vehicle kinematics + driver inputs + road
  geometry + weather (driver-vehicle-environment triptych). RF/SVM/MLP; SMOTE vs
  over/undersampling — SMOTE+MLP best (94.5% precision/F1, ~94% AUC, 95.3%
  recall). Findings note 62% of crashes on downhills/curved-downhills and 44% in
  snow/rain — condition-conditioned FACTS appear in the paper's discussion, but
  are never surfaced as a system output to a user. `borrow` (SMOTE-vs-alternatives
  empirical comparison — imbalance shelf #5) + `related-work` (real-time COM,
  triptych framing). Gap unbeaten — event-level, no NL, no segment.*

- **Towards the Spatial Analysis of Motorway Safety in the Connected Environment
  by Using Explainable Deep Learning**
  *CAV speed/position data → image-alike heatmaps of motorway speed distribution,
  labeled by TTC-derived safety category → CNN classifies safety category → XAI
  (saliency) highlights which spatial/temporal regions of the heatmap drove the
  prediction; studies how CAV+ISA penetration rate changes the spatial
  distribution of "critical regions." A genuine CRM-shaped (segment/spatial
  safety categorization) exemplar WITH explainability — but the explanation is a
  saliency MAP, not NL, and the conditioning variable is CAV-penetration-rate,
  not weather/time/road-surface. Sharpens Chai's claim further: even the rare
  CRM+XAI combination stops at visual saliency, never language. `related-work`/
  `home`-mapping. Gap unbeaten.*

- **WFFS — An Ensemble Feature Selection Algorithm for Heterogeneous Traffic
  Accident Data Analysis**
  *UK traffic accident records → WFFS (Weighted Fusion-based Feature Selection)
  + SMOTE/random-oversampling/percentage-removal balancing → tree-based bagging
  reaches 97.28% severity accuracy with 18 selected features. Pure CSM methods
  paper — no NL, no segment, no condition-conditioning. `borrow` — feature-
  selection step directly applicable to STATS19's heterogeneous categorical
  features, plus another UK-data SMOTE/oversampling data point. Gap unbeaten.*

- **Overcoming Imbalanced Safety Data Using Extended Accident Triangle**
  *Extends Heinrich's accident-triangle theory: minority-class sample importance
  should be weighted by injury severity, accident frequency, AND accident type —
  proposes 3 theoretically-grounded oversampling methods (vs. naive SMOTE).
  Validated across 3 occupational-safety datasets (construction, trucking, US
  truck-driver safety-climate survey), open-source code provided. Occupational,
  not road-crash, but the THEORY (severity/frequency/type-weighted oversampling
  grounded in accident-pyramid theory) is directly transferable to STATS19's
  fatal-class imbalance — gives us a citable safety-science framework beyond "we
  used SMOTE." `borrow` — imbalance shelf #6, with reusable code. Gap unbeaten
  (no NL, no road domain).*

- **Railway Accident Causation Prediction with Improved Transformer Model Based
  on Lexical Information and Contextual Relationships**
  *FRA (US Federal Railroad Administration) accident text → Convolutional Block
  Attention (lexical encoder) + BiGRU (contextual/positional encoder) + cue-word
  tabular-to-text preprocessing → predicts accident CAUSE category
  (classification, not generation). Beats SOTA by ~0.4–3.6 pts P/R/F1; robust on
  rare cause categories with limited training data. Cross-domain (railway)
  confirmation of the "tabular accident data → text representation → ML
  classification" pattern (now seen in road/Tab-Text, aviation/RACI, rail/this
  one). `related-work`/`background`, low priority — confirms the pattern rather
  than adding to it. Gap unbeaten (classification output, not NL, no segment).*

- **Learning Spatial Patterns and Temporal Dependencies for Traffic Accident
  Severity Prediction: A Deep Learning Approach**
  *CNN (spatial feature patterns) + BiLSTM (temporal dependencies) + attention
  (feature-importance weighting) for CSM on real-world data from two cities.
  Another deep-architecture-with-attention severity classifier — attention
  weights are the "interpretability," never NL; "spatial" here means
  feature-space patterns, not geographic segments. `related-work`, low priority
  — confirms CSM saturation with attention-based pseudo-interpretability. Gap
  unbeaten.*

---

## Skipped (term-collision)

- **A Robust Elastic Net via Bootstrap Method Under Sampling Uncertainty for
  Significance Analysis of High-Dimensional Design Problems (RENBOOT)**
  *"Significance analysis" here means bootstrap confidence intervals on
  elastic-net regression coefficients, robust to experimental-design sampling
  variation — answers "is this design variable's effect on the response real
  across resamplings of a Latin hypercube DOE?" Domain: vehicle body-in-white
  structural design optimization. Different statistical question (regression-
  coefficient robustness under DOE resampling) and different domain (mechanical
  design, not crash records) than our significance gate (categorical-pattern
  overrepresentation in crash data). Term-collision, same shape as SSARA (EAAI).
  `skip`.*

---

## Skipped at title stage (off-layer)

~100 of ~110 results. Clusters: finance/trading/forex (~10); cybersecurity/
malware/intrusion-detection incl. in-vehicle IDS (~10); robotics/UAV/swarm
navigation (~8); generic ML methods/optimization with no stated domain —
surrogate optimization, feature transforms, kernel methods, NAS, clustering
(~20); AV/ADAS micro-layer incl. driver drowsiness/gaze, lane-change RL, merging
(~6); pure traffic-flow/speed forecasting (~5); software engineering/NLP/
multimedia off-domain — bug prediction, vulnerability detection, rumor
detection, video indexing (~15); long miscellaneous tail — medical (EEG seizure
detection), sports betting, ontology evolution, energy forecasting, road-surface
maintenance, aviation human-factors/SPI, agent-based simulation, etc. (~25).

---

## Tag legend

`home` / `integration` / `related-work` / `borrow` / `background` / `skip`
