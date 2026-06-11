# ESWA — Tier 1, Journal 2 Reading Record

**Status: COMPLETE.** All 3 keywords triaged (`crash severity prediction`, `road safety
decision support`, `accident risk machine learning`). 2 deep reads — Tab-Text (closest
input-pipeline twin) and Hussien 2025 (strongest explanation-layer prior art) — plus
abstract-only refs below. Gap test unbeaten across all three sweeps. Next journal:
Engineering Applications of AI.

---

## Full-text (deep-read) — the keepers

- **Tab-Text: Bridging Tabular Data and Natural Language for Enhanced Traffic Safety
  Analysis and Modeling** — Zhen, Jidong J. Yang, 2025 (ESWA 290:128450; Univ. of Georgia)
  *Where it lies in the progress: the CLOSEST methodological twin found yet — closer than
  Li 2025 — because the text is **template-generated from tabular crash data**, which is
  exactly Phase 1's tabular-to-text narrative step, now independently published in a top
  applied-AI venue. This both validates our pipeline and converts our narrative-generation
  step into citable PRIOR ART (it is no longer a standalone contribution). The thesis
  novelty survives only in what they don't do.*

  **What they built.** A multi-modal severity classifier. Tabular crash data → predefined
  template → coherent narrative (Fig 2: *"On 2006-02-19, Sunday, at 6:30 AM, an accident
  occurred on a clear day on dry road surface. The environment was dark with streetlights
  on..."*). Then BOTH branches feed a concatenated head: tabular (categorical → factorized
  embedding → MLP; numeric → min-max → MLP) + narrative (→ ELECTRA, 12 layers, 768-dim
  [CLS]) → 1536+768 = 2304-dim → Dense×2 → severity. ELECTRA chosen for efficiency vs BERT.

  **Same problem shape as us.** Victoria CrashStats (VicRoads), 2006–2020, 292,110 crashes,
  3-class severity after dropping non-injury: Minor 67% / Serious 31% / **Fatal 1.63%** —
  essentially identical imbalance to STATS19's ~1.5% fatal. Their narrative-generation
  justification is ours verbatim: categorical codes lose semantic content (their example:
  `ROAD_GEOMETRY = "0: Not at the intersection"` discards the linguistic meaning an LLM
  could use). Crucially they state the template encodes ONLY facts from the tabular data,
  not injected domain knowledge.

  **Results (Table 2 / Table 3).** Tab-Text macro F1 0.4587 (best), micro-acc 0.7152.
  Baselines: MNL 0.3317, CatBoost (tabular-only) 0.4118, T2T-Transformer (text-only)
  0.4179, AT-Transformer (textualized-tabular) 0.4024. The headline: fatal-class accuracy
  9.63% vs 5.25% next-best — the narrative **nearly doubles** rare-class accuracy. Ablation
  (Table 4): removing the narrative drops fatal acc 6.9%, serious 7.48% → the text helps
  most exactly on the rare severe classes (our pain point). Robustness via downsampling
  (Table 6) keeps the ranking. (Absolute fatal recall is still poor — Table 5 shows 88/914
  fatal caught — but directionally the multi-modal lift is real.)

  **Interpretation.** Permutation importance (chosen over SHAP for cost; words shuffled
  within each narrative for the text features). Top factors: DCA (manner of collision),
  SPEED_ZONE, VEHICLE_MOVEMENT, ACCIDENT_TYPE. They then cross-check these against MNL
  significance (Tables 7–8, p<0.05) and find agreement — used as a validity argument.

  **Four takeaways for the thesis:**
  (1) **Our cleanest distinction, now sharp: NL as OUTPUT vs NL as INPUT.** Tab-Text (and
  Li 2025) use the narrative as an intermediate *feature* consumed by the classifier;
  the deliverable is a severity class, never shown to a human. Our deliverable IS the
  prose a human reads. This is the strongest line we can draw against the whole
  tabular-to-text-for-crash family — they encode→predict, we generate→explain.
  (2) **The narrative-generation step is now prior art** (2nd venue after Li). Position
  it as adopted-and-cited method, not contribution. Novelty narrows to the JOIN:
  NL-explanatory-output × condition-conditioned segment patterns × significance-gated
  selection.
  (3) **Borrow:** the ELECTRA-backbone rationale; the with/without-narrative ablation
  design (clean proof the narrative adds value, esp. on rare classes — mirror it); the
  `ROAD_GEOMETRY` semantic-loss argument as a ready citation for *why* tabular-to-text
  helps; Victoria CrashStats as a same-imbalance second dataset; the downsampling
  robustness check.
  (4) **Their MNL cross-check is a primitive cousin of our significance gate** — but it
  only *validates feature importance post-hoc*, it doesn't *gate which patterns get
  explained*. We sharpen: they check alignment after the fact; we gate the explanation on
  a real overrepresentation test BEFORE the LLM speaks. Cite as precedent for
  "ML-checked-against-statistical-significance," then differentiate.

  **Gap-test verdict: still UNBEATEN.** Event-level, NL-as-input, no segment, no
  condition-conditioning, no NL-explanation-output, no significance gate on patterns.
  But the single strongest brick yet that our *input pipeline* is prior art.

  **Watch:** Zhen & J.J. Yang (Univ. Georgia) also have Zhen et al. 2024b (CoT + prompt
  engineering for crash severity, cited here) — an active LLM+crash lab, the closest
  competitor group seen so far. Tag: `related-work` (strong, input-pipeline twin) + `borrow`.

- **RAG-Based Explainable Prediction of Road Users Behaviors for Automated Driving Using
  Knowledge Graphs and Large Language Models** — Hussien, Melo, Ballardini, Salinas
  Maldonado, Izquierdo, Sotelo, 2025 (ESWA 265:125914; Univ. of Alcalá, Madrid; EU HEIDI)
  *Where it lies in the progress: the STRONGEST explanation-layer prior art to date — and
  NOT knockable (unlike Gyawali). A rigorous, well-evaluated neuro-symbolic system from a
  heavyweight group (Sotelo = former President, IEEE ITS Society). It makes the
  explanation-layer architecture firmly prior art across 3 papers now — but leaves the
  same faithfulness hole open, which strengthens our angle.*

  **What they built.** 3-phase system for AD road-user behavior prediction (pedestrian
  crossing / lane change): (1) sensor features → linguistic categories (TTC sec →
  `high/medium/lowRisk`; accel → `left/zero/rightAcceleration`) → Knowledge Graph on a
  hand-built ontology (reified triples); (2) Knowledge Graph Embeddings (TransE/ComplEx via
  AmpliGraph); (3) Bayesian inference P(h|e)=P(h)P(e|h)/P(e) over embeddings → behavior
  label. Explanation via (a) fuzzy association rules (IVTURS-FARC) folded into the KG and
  (b) **RAG**: human-readable state descriptions → Chroma vector DB → GPT-4 generates the
  NL justification. Real datasets (JAAD, PSI, HighD), real baselines.

  **Results.** PedFeatRulesKG F1 0.87 (JAAD) / 0.84 (PSI), beating C3D (0.65), PCPA (0.68),
  their own black-box (0.75), decision trees, fuzzy logic (+22% over C3D). Lane-change F1
  >90% up to 3s pre-maneuver. Rigorous — not a demo.

  **Four points for the thesis:**
  (1) **Explanation-layer prior art is now strong and unknockable** (Zhang + Gyawali +
  Hussien; this is the most complete and credible). We CANNOT claim the LLM-explains-ML
  architecture as novel.
  (2) **But all three leave the same hole: the explanation is never validated.** They
  evaluate the *prediction* rigorously; the RAG explanation appears only as qualitative
  examples (Fig 9, 12) with ZERO faithfulness metric. Zhang at least tried (unreliable
  LLM-judge); Gyawali and Hussien don't. → Our significance-gated, statistically-validated
  explanation answers a hole the whole subfield leaves open. More papers here = our
  contribution stands out MORE, not less.
  (3) **They are the failure mode we design against.** Their prompt (Fig 8) says *"do not
  use conditional words as 'may'"* and the example asserts *"The pedestrian **will** cross
  **because** they are seeking eye contact..."* — confident, causal, intentional NL with no
  faithfulness check. Exactly Zhang's Causal-Plausibility landmine. PERFECT contrast: prior
  work engineers prose to sound *decisive*; we constrain to *association* language
  ("overrepresented under X") gated by a real significance test. Note the inversion — they
  suppress hedging, we require epistemic care.
  (4) **Borrow:** prompt-discipline engineering (word cap, few-shot, "if you don't know,
  say so"); KG-as-retrieval-substrate is a more principled RAG variant than Gyawali's
  canned-blurb lookup. Numeric→linguistic binning of risk (TTC→high/low) is a 3rd instance
  of that move (after Li, Tab-Text).

  **Gap-test verdict: still fully UNBEATEN.** AD real-time kinematic behavior prediction —
  event-level, no segments, no historical crash patterns, no condition-conditioned
  overrepresentation. Tag: `related-work` (strong, explanation-layer) + `borrow`.
  Explanation-layer brick #3, the heaviest.

---

## Abstract-only — triaged, worth citing

- **Integration and Comparison of Multi-Criteria Decision-Making Methods in Safe Route
  Planner** — Sarraf, McGuire, 2020
  *Strong `integration` precedent. Opens with our exact framing — risk maps are
  confusing, drivers must manually interpret them, Google Maps/Waze rank only by time
  and distance. Assumes a per-segment risk score already exists; the contribution is the
  downstream MCDM layer (AHP/Fuzzy AHP/TOPSIS/Fuzzy TOPSIS/PROMETHEE) that combines
  risk+time+distance into a route ranking, evaluated via Spearman's rank correlation,
  Average Overlap, and DCG. Confirms route planning as a real consumer slot for our risk
  profiles — they'd plug in upstream of this MCDM layer. The evaluation metrics echo
  Zhang 2025's overlap-score family.*

- **SSARA: Integrating Safety and Security for Adaptive Risk Assessment of CAVs** —
  Zheng, Deng, Li, 2026
  *Knocked down — term-collision only. "Risk assessment" here means STPA-based
  safety+security hazard analysis for CAV operational monitoring + an autoencoder-
  clustering model over real-time sensor indicators (highD dataset). No crash data, no
  segments, no NL, no condition-conditioning. Confirms "risk assessment" spans very
  different literatures — we sit in the historical-crash-pattern one, not CAV
  operational-systems-safety. Tag `skip`.*

- **Natural Language Processing and Text Mining in Transportation: Current Status,
  Challenges, and Future Roadmap** — Zhang, Gao, Zhang, 2026 (review)
  *Broad land/sea/air NLP survey (sentiment analysis, toolkits, language diversity).
  Largely redundant with Mahmud/Hassan — another generic survey with no crash-risk-
  explanation category. Gap-by-omission citation only; lowest priority of the three
  surveys collected so far.*

- **Combination of Macroscopic and Microscopic Crash Prediction Models with Multiple
  Modeling Approaches: A Highway Case Study** — Rúa, Arias, Martínez-Sánchez, 2024
  *Second independent anchor for the "aggregate crashes → numeric CPM score per
  segment" bucket (AHP+NB+GWPR ensemble, Spain highway 2016-2021), corroborating Jiang
  2022's framing with a different methodological family (CPM/AHP/GWPR vs. SPF/EB).
  Confirmatory, not novel — no condition-conditioning, no NL. Useful for related-work to
  show "aggregate→score" is a family of approaches, not one paper.*

- **Crash Risk Prediction Using Sparse Collision Data: Granger Causal Inference and
  Graph Convolutional Network Approaches (PST-CGCN)** — Hu, Bai, Lee, 2025
  *Spatial-temporal crash-risk forecasting with causal-association analysis between
  regions, interpreted via gradient analysis on the GCN. Different "causal" axis than
  ours — inter-region temporal propagation, not condition-conditioned NL. Tangential
  `related-work`/`borrow` (gradient-based causal interpretability technique), not a
  twin.*

- **Knowledge Graph Construction from British Railway Accident/Incident Reports for
  Hazard Identification and Risk Assessment** (text mining + KG, railway domain)
  *Pre-LLM NER pipeline (HMM/CRF/Bi-LSTM/Bi-LSTM-CRF ensemble + random forest entity
  classification) extracts hazard/fault/accident entities from railway report text,
  builds a multi-dimensional KG, and quantifies risk levels per hazard from its
  topology. Confirms "text → structured representation → risk assessment" as a
  cross-domain pattern, but: railway not road, no LLM, output is a KG visualization +
  numeric risk level per hazard, not condition-conditioned NL. `related-work`/
  `background` — different domain, different era of NLP, different output shape.*

- **RACI: Retrieval-Augmented Generation-Aided Causal Identification of Aviation
  Accidents** (Ren, Zhang, Jia, Zhang, 2025, ESWA 278:127306) — read full text
  2026-06-11, knocked down from deep-read
  *Pulled hoping mAP 0.815/mNDCG 0.761 was a validated faithfulness metric for the
  generated causal explanation — it isn't. Those scores evaluate ONLY the Retriever:
  given a short categorical accident description (phase+occurrence-type codes, e.g.
  "Landing − roll Loss of control − on ground/water"), does it retrieve past NTSB
  accidents with similar type-code profiles? "Relevance" is a rule-based
  inclusion-hierarchy heuristic over NTSB's occurrence/phase coding manual (Eq 12,
  Tables 3-5) — categorical-taxonomy similarity, not human judgment of causal
  correctness. The actual GENERATION step — Qwen2-7b producing "possible causes" from
  the retrieved accidents' cause fields, the part analogous to OUR NL output — is
  evaluated PURELY QUALITATIVELY (Tables 7-10): prompt comparisons and a RACI-vs-GPT-4o
  comparison, with the paper's own conclusion ("difference... negligible") based on
  eyeballing, zero metric.
  **Net effect:** RACI is brick #4 in "generate explanatory text with no faithfulness
  validation" — now spanning 4 papers / 4 domains (traffic-GNN forecasting, V2X
  cybersecurity, AD behavior prediction, aviation cause-by-analogy). Reinforces rather
  than fills the hole. `related-work`/`borrow`: inclusion-hierarchy categorical-
  similarity scoring (Eq 12) as a retrieval-relevance heuristic, and FGM-adversarial-
  training + TF-IDF noise filter as an SBERT-retriever robustness recipe — both
  tangential, not faithfulness-relevant.
  **Gap-test verdict: still UNBEATEN** — the validated-explanation hole just got wider.*

- **Analysis of Traffic Accident Causes Based on Data Augmentation and Ensemble
  Learning with High-Dimensional Small-Sample Data** (China city case study)
  *Road-domain ensemble pipeline (feature crosses + random-variable-augmented feature
  selection as a data-augmentation step + forward-selection ensemble) for identifying
  key accident causes from small-sample data. Finds lane-changes/turns as top causes;
  argues timely driver info reduces risk. No LLM, no NL, no condition-conditioning —
  output is a static global cause ranking. `borrow` — a non-WGAN alternative for
  small-sample/imbalance handling (3rd method on that shelf alongside Man et al.
  2022's WGAN), directly relevant to STATS19's fatal-class sparsity.*

---

## Skipped at title stage (off-layer)

AV control/ethics/RL (DQN ethical decision-making in unavoidable crashes; VSL freeway
control via multi-objective RL; driver-pedestrian inverse RL; vehicle-interaction
prediction in CAV environments); microscopic conflict/trajectory work (manifold-
similarity GNN for mixed-traffic conflicts; two-wheeler trajectory conflicts at
intersections); detection/sensing (audio-visual collision detection; thermal near-miss
"Knowledge PET3D"); pure forecasting (heterogeneous traffic flow; hexagonal-grid
generative accident situations); severity-only ML without explanation/condition framing
(one-vs-rest consensus severity; SOM severity pattern detection; decision-rule severity
analysis; cost-sensitive transfer-learning severity; rear-end explanatory-factor +
sensitivity analysis; cellular-automata + RF/XGBoost Toronto study); completely
off-domain ("crash" = software bugs ×2, ObfSec, stock market crash, crime-app
prioritization).

---

## Tag legend

`home` / `integration` / `related-work` / `borrow` / `background` / `skip`
