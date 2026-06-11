# EAAI — Tier 1, Journal 3 Reading Record

**Status: COMPLETE.** Keyword 1 (`traffic accident prediction`) → 2 full-text deep
reads (Chai et al. 2024 survey — the field-taxonomy find; Smetana et al. 2026 —
the explanation-output-validation cousin) + 3 abstract-only refs. Keyword 2
(`road risk assessment AI`) → 0 keepers (~67 titles, almost all cross-domain
"risk assessment" noise — geotechnical, occupational safety, fuzzy-MCDM,
maritime/energy; "risk assessment" is too generic a term for a general
engineering-AI journal). Next journal: Knowledge-Based Systems.

---

## Full-text (deep-read) — the keepers

- **Enhancing Road Safety with Machine Learning: Current Advances and Future Directions
  in Accident Prediction Using Non-Visual Data** — Chai, Lau, Tee, McCarthy, 2024
  (EAAI 137:109086; Swinburne U.; 95-study systematic review, 2018–2024)
  *Where it lies in the progress: a POSITIONING GIFT, the most useful single paper for
  the related-work chapter so far. It hands us (1) the field's own vocabulary for what
  we do, (2) a quantified map showing our target sub-field is the least-explored, and
  (3) a clean gap-by-omission (NL/explanation is not even a listed future direction).*

  **The field's taxonomy — and our word.** ML-based RTA prediction splits into 4
  modeling categories:
  - **CRM (Crash Risk Modeling)** — probability of a crash at a specific area/road
    SEGMENT over a period; "a regression task that estimates road safety level at
    different road segments." **← this is us.** We can now write "this thesis
    contributes to crash risk modeling (CRM)" in the field's own terms.
  - COM (Crash Occurrence) — binary crash/non-crash event classification.
  - CSM (Crash Severity) — severity-level classification (Phase 1's original task; the
    dominant category).
  - CFM (Crash Frequency) — counts per segment over a period → hotspot identification.

  **CRM is the LEAST-explored category — 8 studies (8%).** CSM 62%, COM 17%, CFM 13%.
  Our target sub-field is the thinnest of the four. Every CRM exemplar cited (RiskCast,
  DeepRisk, Li 2020, Zhao 2019 — social-sensing / transfer-learning) outputs a NUMERIC
  risk score/rate/probability. None condition-conditioned, none NL.

  **Gap-by-omission.** The 5 future directions (§4.4) are: multitask prediction, data
  quality, hybrid approaches, model transferability, standardized framework.
  Interpretability appears ONLY in the narrow SHAP/LIME feature-attribution sense.
  Natural-language communication of risk to a human is never mentioned — across a
  95-study review. Strong single citation for "the field doesn't see this gap."

  **Honesty nuance (sharpens, not weakens, us).** The "Key Factors Observed" columns
  (A–I) show many studies DO use environmental conditions (C), time (F), road
  characteristics (E) as INPUT FEATURES. So "uses weather/light/time" is not itself
  novel — they're predictors feeding a number. Our distinction gets sharper: all 4
  categories output a number or a class; NONE outputs an explanation. Condition-
  conditioned pattern *overrepresentation surfaced as NL* ≠ conditions-as-features.

  **Borrow shelf:** the class-imbalance synthesis (THE recurring CSM problem; SMOTE /
  undersampling / GBDT minority-weighting, with the note that the right fix is
  dataset-dependent — a citable survey-level backing for our fatal-class handling);
  the data-source breakdown (50% government, 34% open-access → STATS19 is in the
  dominant data pattern); the 4-category taxonomy as the skeleton of our related-work
  section. Tag: `related-work` + `home`-mapping. Gap test: UNBEATEN and now quantified.*

- **Improving Large Language Model Assisted Categorization and Classification of
  Highway Construction Accidents** — Smetana, Salles de Salles, Khazanovich, 2026
  (EAAI 176.2:114798; Univ. of Pittsburgh / RIT; open access)
  *Where it lies in the progress: the EXPLANATION-OUTPUT-VALIDATION cousin — the first
  paper in the whole sweep that actually validates the faithfulness of LLM-generated
  summary text with a computed metric. It does NOT beat our gap, but it hands us the
  exact method we'd been treating as a wished-for idea, and it refines (strengthens)
  our novelty story.*

  **Pipeline.** OSHA highway-construction accident narratives (1,198 cases, NAICS
  237310) → `text-embedding-ada-002` (1536-dim sentence embeddings) → K-means (10
  clusters, elbow + manual t-SNE review) → **MapReduce summarization** (GPT-3.5-turbo):
  Map prompt summarizes N token-limited chunks of incidents per cluster → chunk
  summaries; Reduce prompt distills them → one cluster summary `S_m`. Prompt
  deliberately requests "a list of FACTS, not a narrative" to maximize info density and
  minimize hallucination. Separately: zero/few-shot classification of 8 IMIS
  categorical fields from the narrative.

  **The part that matters — computed output-faithfulness (Eq. 7, adapting SelfCheckGPT
  / Manakul et al. 2023 EMNLP).** After Reduce produces `S_m`, the LLM generates 15
  facts per chunk and is asked per fact: *"Does this fact support the summary?"* → Yes
  (λ=0.0) / No (λ=1.0) / N/A (λ=0.5). Inconsistency `IS_m = 100·(1/J)·Σλ_j`; the final
  summary is rebuilt from ONLY true-assertion facts. **Result: 83% consistency
  (1,551/1,860 true assertions)**; worst = cluster 8 (the over-general "struck-by" one;
  69 false / 71 inconclusive). Per-cluster IS in Table 2. Total cost $2.33.

  **Why it's a gift, not a threat — different axis, and they STACK.**
  - Their fact-consistency check = "did the prose stay faithful to the source text the
    model was given?" — a hallucination filter on the OUTPUT.
  - Our significance gate = "is the pattern statistically real / overrepresented in the
    data?" — a validity test on the INPUT pattern, before the LLM speaks.
  Stacked: **significance-gated (pattern is real) + fact-consistency-checked (prose is
  faithful to it)** closes the faithfulness hole more completely than any prior work.
  This moves our output-validation layer from "wished-for" to a cited, adaptable method.

  **Why it doesn't beat the gap test.** Construction/occupational domain, not road-crash
  CRM. Clusters are SEMANTIC SIMILARITY of narratives, not condition-stratified segment
  risk — no weather/light/time conditioning. The summary is DESCRIPTIVE ("these share
  struck-by + falls"), not a risk explanation; they summarize whatever clustered
  together and NEVER test whether a pattern is non-obvious or overrepresented vs a
  baseline — exactly the significance step they lack and we add. Gap test: UNBEATEN.

  **Refines our novelty story (important).** Old claim "nobody validates the
  explanation" now needs one caveat: in the ROAD-SAFETY explanation-layer papers
  (Zhang, Gyawali, Hussien, RACI) nobody validates — but Smetana, in a neighbouring
  domain, DOES validate internal consistency. Sharper, more defensible position: we
  BORROW Smetana's output-faithfulness check AND add the input-side significance gate
  they lack, on condition-conditioned segment risk, as a human deliverable. Stronger
  than claiming we invented output validation.

  **Borrow shelf:** (1) SelfCheckGPT-style fact-consistency check = our output-
  validation layer (the heaviest borrow of the sweep); (2) "request facts not
  narrative" prompt discipline; (3) MapReduce chunking for context-window limits when
  summarizing many crashes; (4) cluster→curated-human-title move (Cluster 3 →
  "Roadside Risks: Vehicle Strikes Beyond Barriers"); (5) $2.33 cost-transparency
  argument. Tangential: LLM out-corrected the government DB coding in 37.7% of differing
  `event_type` cases (Scenario 2) — a data-quality side-application (could surface
  STATS19 miscoding too). Tag: `related-work` + `borrow`. Pairs with [[Zhang 2025]] as
  the explanation-layer that finally DOES output validation — but on the wrong axis for
  a gap, the right axis for a borrow.*

---

## Abstract-only — triaged, worth citing

- **Driving Risk Prediction of Urban Arterial and Collector Roads Using
  Multi-Dimensional Real-Time Data**
  *Real-time risk-LEVEL classification per road (Entropy-TOPSIS+K-means for
  ground-truth risk labeling, SHAP for feature importance, LightGBM+DCGAN best).
  Segment-type (arterial/collector) + multi-dimensional condition features, but
  output is a risk level/score, not NL — no condition-conditioned pattern explanation,
  no significance gate. `related-work`/`borrow`: Entropy-TOPSIS+K-means as an
  alternative risk-label-construction method; DCGAN as a 4th imbalance-handling
  method (after WGAN, ensemble+small-sample-augmentation, this).*

- **Deep Forest with SHapley Additive Explanations on Detailed Risky Driving Behavior
  Data for Freeway Crash Risk Prediction**
  *Deep Forest (multi-grained scanning + cascade forest) + SHAP for freeway crash
  risk; AUC 0.825; SHAP highlights sharp accel/braking as top risk factors. Same
  shape as Antariksa/Phase 1 (model + SHAP), no NL, no condition-conditioning, no
  significance gate. `related-work`/`borrow` (Deep Forest as an alternative ensemble
  method to XGBoost).*

- **Vehicle Real-Time Collision Risk Prediction: A Multi-Modal Learning Approach for
  Diverse Urban Road Scenarios Based on a Large-Scale Near-Crash Event Dataset
  (PM-Transformer)**
  *Real-time, near-crash (0.5-2s horizon), individual-vehicle collision-avoidance risk
  prediction via multi-module Transformer fusion (time-series + spectral + metadata).
  Redundant with the Zhu/Abdel-Aty real-time-crash-risk sub-literature already noted
  (T-ITS). No explanation framing at all. `related-work` (field-anchor only), low
  priority.*

---

## Skipped at title stage (off-layer)

Pure traffic-flow/speed/volume forecasting (GCN/GNN/Transformer/grey-model variants,
no accident framing — ~28 papers); AV/ADAS micro-control, trajectory, perception,
lane-change, roundabout-conflict prediction (~13); maritime/vessel + air-traffic
prediction (~10); traffic-signal-control/RL (~4); completely off-domain (urban health,
wind speed, pavement friction, infrastructure-failure survival analysis, speech
emotion, occupational-risk ANFIS, parking IoT, holonic-paradigm review, federated
time-series — ~8); incident-duration/real-time-detection sub-literature (RBM duration
fusion, GCN duration classification, feature-optimization for duration, ensemble
incident detection, GAN-based accident detection, dual-stream detection — ~6).

---

## Tag legend

`home` / `integration` / `related-work` / `borrow` / `background` / `skip`
