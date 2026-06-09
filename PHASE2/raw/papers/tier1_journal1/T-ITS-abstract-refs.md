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
