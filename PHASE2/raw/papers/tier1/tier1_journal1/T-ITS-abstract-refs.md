# T-ITS — Tier 1, Journal 1 Reading Record

**Progress so far (after these two full reads):** we're on the correct road — the direction
is now confirmed from two different angles — but early in the journey, with a long way to go.
These two papers proved the idea is real and located the home field; they did *not* prove the
idea is novel on its own. ~15% through the planned reading.

---

## Full-text (deep-read) — the two keepers

- **Leveraging Textual Description and Structured Data for Estimating Crash Risks of Traffic Violation: A Multimodal Learning Approach** — Li, Ma, Zhou, Lord, Zhang, 2025
  *Where it lies in the progress: VALIDATION + sharpened gap. Proves text+tabular+LLM crash
  modelling is live, top-venue work (co-authored by crash-stats heavyweight Dominique Lord),
  so our direction is real — but it does the inverse of us (encodes text → predicts crash at
  the event level for enforcement; we generate text → explain a pattern at the segment level
  for drivers). Confirms the road; does not yet differentiate us. Borrow: TabNet baseline,
  text-categorisation pipeline, imbalance handling.*

- **Safe Route Mapping of Roadways Using Multiple Sourced Data** — Jiang, Jafari, Kharbeche, Jalayer, Al-Khalifa, 2022
  *Where it lies in the progress: the bigger step — gives real new CONTEXT, not just
  validation. (1) Roots us in the canonical risk-assessment methodology we were missing —
  SPF (Safety Performance Function) + Empirical Bayes + Highway Safety Manual — i.e. the
  actual "risk assessment" home the supervisor named. (2) Reveals our deliverable already
  exists in primitive form ("safe routes on navigation," risk heat maps for drivers), so the
  raw idea is NOT novel. (3) Therefore pins our real novelty precisely on what it lacks:
  condition-conditioning (no weather/light/time), the natural-language WHY (output is a
  numeric fuzzy score), and significance/overrepresentation. This is what de-artificialises
  the thesis.*

**Combined gap these two define:** the field either encodes crash text → predicts an outcome
(event-level, enforcement — Li 2025) or aggregates crashes → numeric risk score → heat map
(segment-level, routing — Jiang 2022). Neither conditions risk on the live situation, and
neither explains *why* in natural language. That white space is the thesis.

- **Reflective LLM Prompt Optimisation for Interpreting GNN Predictions in Traffic Forecasting** — Zhang, Kim, He, Yildirimoglu, 2025 (ITSC) — found via `LLM transportation` keyword, 2026-06-11
  *Where it lies in the progress: the first real grounding for the EXPLANATION LAYER — not the
  domain (traffic-speed forecasting, not crash) but the problem. It names our exact risk: LLMs
  translating a numeric attribution into NL produce "fluent yet unfaithful" narratives and will
  confidently rationalise invalid inputs. Their fix is a two-phase design: (Phase 1) optimise a
  prompt that VALIDATES whether the importance scores are even trustworthy (supervised on
  real-vs-rank-permuted variants); (Phase 2) freeze that validator, then optimise the explanation
  prompt — validate-then-explain, refuse if invalid. Multi-agent reflection (Analysis→Reflection→
  Synthesis, M iters) does the prompt tuning. Results: Phase 1 acc 0.40→0.75 (peak M=3 then
  DECLINED — unstable); Phase 2 top-3 grounding overlap 0.45→0.72; ablation removing Phase 1
  drops faithfulness 0.68→0.42. Faithfulness eval is mostly qualitative/expert — they admit hard
  metrics are future work.*
  *Four takeaways: (1) Borrow their three faithfulness dimensions — Score Grounding, Contextual
  Coherence, Causal Plausibility — as our explanation-eval rubric, plus the overlap-score proxy
  (does the narrative cite the actual overrepresented conditions). (2) We can do their validity
  gate BETTER: their "validity" is an unreliable LLM-judge (0.75, unstable) on a synthetic proxy;
  OURS is a real statistical test (Empirical Bayes / significance / overrepresentation). Claim:
  significance-gated explanation — the LLM only explains patterns that passed a real test,
  removing their hardest failure mode. (3) Their "Causal Plausibility" is our landmine: discipline
  the NL to say "overrepresented under wet+dark," NOT "caused by" — we report association, not
  causation. (4) Strategic: with Gyawali, this is the 2nd ITS paper doing LLM-explains-ML-for-
  professionals, so the generic "LLM explanation layer" is now PRIOR ART. Our explanation novelty
  must be pinned to: condition-conditioned statistical overrepresentation of crash risk at the
  segment level, significance-gated. Tag: `borrow` + `related-work`. A methodological neighbour,
  not a home.*

---

## Abstract-only — triaged, worth citing

Papers from IEEE T-ITS that were triaged at abstract level. Not deep-read; PDFs not needed —
abstract gave sufficient signal.

---

- **Driving Safety Risk Analysis and Assessment in a Mixed Driving Environment of Connected and Non-Connected Vehicles: A Systematic Survey** — Cheng et al., 2025
  *Field vocabulary and taxonomy for "driving safety risk assessment"; skim for the four-aspect framework (perception, prediction, quantification, early warning) when writing the related-work section.*

- **Automated and Explainable Artificial Intelligence to Enhance Prediction of Pedestrian Injury Severity** — Antariksa, Tamakloe, Liu, Das, 2025
  *Citable parallel to Phase 1 work (crash severity + SHAP/XAI); supports the "extract + explain" framing.*

- **Vehicle-Group-Based Crash Risk Prediction and Interpretation on Highways** — Zhu, Wang, Feng, Ma, Abdel-Aty, 2025
  *Mohamed Abdel-Aty is the most-cited real-time crash-risk researcher — cite as a field anchor regardless of method fit.*

- **An In-Vehicle Warning Information Provision Strategy for V2V-Based Proactive Traffic Safety Management** — Jo, Jang, Ko, Oh, 2022
  *Formalises the when-to-warn / distraction problem (CDR/DFR/IPR metrics); ammunition for justifying the pre-trip delivery model over real-time warnings.*

- **Wasserstein Generative Adversarial Network to Address the Imbalanced Data Problem in Real-Time Crash Risk Prediction** — Man, Quddus, Theofilatos, Yu, Imprialou, 2022
  *WGAN method directly borrowable for Fatal-class imbalance (1.5% of STATS19); UK M1 Motorway data — Quddus is a credible UK crash author.*

- **Safe and Sound: Driver Safety-Aware Vehicle Re-Routing Based on Spatiotemporal Information** — de Souza, Braun, Botega, Villas, Loureiro, 2020
  *Risk-aware re-routing, but "risk" = criminal events, not crash risk. RNN predicts dynamic future risk scores; personalized re-routing lets each vehicle choose which risk types to avoid. Reinforces the Jiang-2022 pattern (aggregate→numeric score→route) with dynamic prediction instead of static SPF/EB — still no condition-conditioning on situational factors, no NL explanation. Another brick in the gap; weak as a cited baseline due to domain mismatch (crime vs. crash).*

- **Integrating LLMs With ITS: Recent Advances, Potentials, Challenges, and Future Directions** — Mahmud, Hajmohamed, Almentheri, Alqaydi, Aldhaheri, Khalil, Saeed, 2025
  *Highest-cited LLM+ITS survey (71). Application taxonomy = traffic flow, detection, AD, sign recognition, pedestrian detection — crash-risk/segment explanation absent. Gap-by-omission citation.*

- **LLeCaT: LLM Enhanced Causality-Aware Traffic Accidents Post-Effects Prediction** — Yang, Tao, Ge, Fan, Akerkar, Koshizuka, 2025
  *LLM extracts semantics from accident records to predict the crash's causal effect on future traffic-state forecasts (post-crash disruption), not pre-crash segment risk. Wrong direction, but validates "LLM on accident text" as workable.*

- **Large Language Models in Transportation: A Comprehensive Bibliometric Analysis of Emerging Trends, Challenges, and Future Research** — Hassan, Kabir, Jusoh, An, Negnevitsky, Li, 2025 (IEEE Access)
  *161-paper bibliometric; +25.74%/yr growth — good "nascent, fast-growing field" stat. Themes = autonomous mobility, traffic optimization, sustainability; no risk-explanation category. Largely redundant with Mahmud — cite one, not both.*

- **Prompt to Path: LLM-Guided Multi-Objective Eco-Routing via Geohash-Compressed Urban Graphs (GB-MOBR)** — Bagosher, Al Jawarneh, Foschini, Bellavista, 2025 (FLLM)
  *LLM parses NL preferences → routing objective weights for eco/environmental bike routing. Opposite direction of NL use from ours (input-parsing vs. output-explaining), off-domain. Weak related-work.*

- **In-Progress: Augmenting Explainable AI with LLMs to Enhance User Trust in ITS** — Gyawali, Jiang, Huang, 2025 (SPW) — read full text 2026-06-11, knocked down from deep-read
  *3-page workshop demo on V2X misbehavior (cybersecurity), but architecturally a near-mirror of our
  Phase 1 stack: black-box XGBoost → SHAP top-3 features → RAG over a vector DB → 7B instruct LLM
  generates NL explanation, no fine-tuning. Independent evidence that SHAP→RAG→LLM→NL is an
  established ITS pattern (so the architecture shape is prior art, not a contribution). BUT weak
  execution — no explanation evaluation at all (they measure only the detector: 98% acc, suspicious
  AUC≈1.0 on simulated data), and the "RAG" is just a lookup table of canned attack blurbs. The low
  bar it cleared is the opening: rigor on the explanation layer (Zhang's faithfulness rubric + our
  significance gate + real STATS19) is where we beat this tier. Pairs with [[Zhang 2025]] as the 2nd
  explanation-layer brick. Tag: `related-work` (architecture-mirror).*
