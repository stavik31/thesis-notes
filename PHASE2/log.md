# Phase 2 — Wiki Log

Append-only chronological record for the active phase. One entry per operation.
Phase 1's log is archived at `../PHASE1/log.md`.
Parse with: `grep "^## \[" log.md | tail -10`

---

## [2026-06-11] ⏸ RESUME POINT — read this first
- **Where we are:** Phase 2 = *grounding* mode (find the research home so the system stops
  reading as "artificial"). **Tier 1, Journals 1–3 (T-ITS, ESWA, EAAI) fully exhausted.
  Journal 4 (KBS) keyword 1 of 3 done.** Reading records:
  `raw/papers/tier1_journal1/T-ITS-abstract-refs.md` (3 deep reads),
  `raw/papers/tier1_journal2/ESWA-abstract-refs.md` (2 deep reads),
  `raw/papers/tier1_journal3/EAAI-abstract-refs.md` (2 deep reads), and
  `raw/papers/tier1_journal4/KBS-abstract-refs.md` (1 deep read so far).
- **What T-ITS established:** direction *confirmed* (multimodal/LLM crash work is live + segment
  risk-for-drivers is accepted); home field located = **road-safety risk assessment (SPF /
  Empirical Bayes / Highway Safety Manual)** layered with multimodal ML. Sobering: our route-risk-
  map *deliverable already exists* (Jiang 2022) AND the generic *LLM explanation layer* is now
  prior art (Zhang 2025 + Gyawali 2025). So novelty is narrow and precise.
- **The sharpened gap (carry this) — now TWO axes:**
  (1) *Risk side:* field either encodes crash text → *predicts* an outcome (event-level — Li 2025)
  or aggregates crashes → *numeric score* → heat map (segment-level — Jiang 2022). Neither
  conditions on the live situation.
  (2) *Explanation side:* LLM-explains-ML-for-professionals exists (Zhang, Gyawali) but only over
  generic predictions/attributions, never over condition-conditioned crash-risk patterns, and the
  faithfulness problem is unsolved (Zhang's validity gate is an unreliable LLM-judge).
- **Our novelty, pinned (sharpened by Tab-Text):** the JOIN of three things —
  *NL-as-explanatory-OUTPUT × condition-conditioned segment patterns × significance-gated
  selection.* The tabular-to-text narrative step is now PRIOR ART (Li 2025 + Tab-Text 2025),
  so it's adopted-and-cited, not a contribution. **Cleanest surviving distinction: NL as
  OUTPUT vs NL as INPUT** — the field uses narratives as an internal feature to predict a
  class (never shown to a human); ours is the deliverable a human reads. Edge on
  faithfulness: a REAL statistical significance test as the validity gate (beats Zhang's
  LLM-judge; sharper than Tab-Text's post-hoc MNL importance cross-check). Discipline: NL
  must say "overrepresented under X," not "caused by X."
- **Borrow shelf (from Zhang):** 3 faithfulness dimensions (Score Grounding, Contextual Coherence,
  Causal Plausibility) as explanation-eval rubric + overlap-score proxy metric.
- **Test question to carry into every future paper:** *is anyone doing condition-conditioned,
  explanation-generating segment risk?* Every "no" is a brick. Still unbeaten.
- **Field-home found (the Phase 2 goal):** Chai et al. 2024's survey gives the field's
  own term for what we do — **CRM = Crash Risk Modeling** (segment-level crash risk), the
  least-explored of 4 categories (CRM/COM/CSM/CFM), and NL/explanation isn't in its
  future-work list → quantified gap. Output-side validation also now has a method to
  adopt (Smetana 2026's SelfCheckGPT fact-consistency check), which stacks with our
  significance gate on a different axis. We can now write related-work in the field's
  vocabulary instead of an invented gap.
- **Context-grounding status (checkpoint, 2026-06-11):** assessed whether the supervisor's
  "artificial"/no-research-home critique is resolved — **yes**. The CRM taxonomy (Chai 2024)
  gives a field-recognized name/slot, a quantified gap-by-omission, and every method
  component now has independent prior art (tabular-to-text: Li/Tab-Text; LLM-explains-ML:
  Zhang/Gyawali/Hussien; LoRA-for-traffic-risk: TrafficRiskGPT; output-faithfulness:
  Smetana). Diminishing-returns signal: EAAI keyword 2 was a total bust (0/67), KBS keyword
  1 mostly confirmatory aside from TrafficRiskGPT. **Decision:** keep sweeping remaining
  Tier-1 keywords/journals opportunistically — cheap, watch-for-surprises mode, not urgent.
  The one track that would move from "context located" to "context fully grounded" is
  **AAP/AMAR** (primary CRM lit — RiskCast/DeepRisk/Li 2020/Zhao 2019-type papers Chai cites
  secondhand) — optional/deferred, not blocking.
- **NEXT:** KBS keyword 1 done (TrafficRiskGPT deep-read complete) — continue
  KBS keywords 2-3 (`risk assessment framework`, `knowledge extraction traffic`),
  then remaining Tier-1 journals/keywords opportunistically; AAP/AMAR optional.
- **Working style (locked):** record papers as lightweight per-journal md entries, NOT full wiki
  INGEST. Model: Sonnet for triage, Opus for deep reads. Progress ≈ 25% of the reading.
- **The plan in full:** [[PHASE2/PLAN]] · triage state: [[wiki/progress/journal-triage]].

## [2026-06-11] reading | KBS keyword 1 — TrafficRiskGPT, the closest near-miss yet
- Record: `raw/papers/tier1_journal4/KBS-abstract-refs.md` · triage: [[wiki/progress/journal-triage]]
- KBS keyword 1 (`crash prediction`): ~110 results, ~100 off-domain (general-AI
  venue — finance/cyber/robotics/generic-ML noise). 8 abstracts → 1 deep read +
  6 abstract-only + 1 skip.
- **TrafficRiskGPT (Zhong et al. 2025)** → DEEP READ. LLaMA3-8B+LoRA fine-tuned
  for AV traffic-risk reasoning, with CI-CoT (causal graph + backdoor + ATE per
  scene) producing fluent NL reasoning chains. Closest near-miss in the sweep —
  doesn't beat the gap (agent-consumed, scene/kinematic-conditioned, no
  faithfulness check on the NL — DriveScore/collision-rate are task metrics).
  Brick #5 of "explain, never validate" (5 papers/5 contexts). Gives us (1) our
  sharpest LoRA-architecture-validation precedent, and (2) a mechanism-level
  justification for "association not causation" — real causal inference
  (DAG+backdoor+ATE) doesn't scale from one scene to population-level
  segment×condition risk. `related-work`+`borrow`.
- 6 abstract-only: 2 imbalance-shelf adds (SMOTE comparison; Heinrich
  accident-triangle weighted oversampling), CRM+XAI exemplar (CAV heatmaps +
  saliency, no NL), WFFS feature-selection borrow, 2 more CSM confirmations
  (railway causation transformer, CNN+BiLSTM+attention severity).
- 1 skip: RENBOOT (term-collision on "significance analysis").
- Notable: gap test still UNBEATEN. **Next: KBS keywords 2-3** (`risk assessment
  framework`, `knowledge extraction traffic`).

## [2026-06-11] reading | EAAI keyword 2 swept — EAAI complete, 0 keepers
- EAAI keyword 2 (`road risk assessment AI`): ~67 results, 0 keepers. "Risk
  assessment" is too generic for a general engineering-AI journal — pulled
  cross-domain noise (geotechnical, occupational safety, fuzzy-MCDM, maritime/
  energy, AV micro-layer). 1 dup (Chai 2024). 4 marginal titles dropped.
- **EAAI done**: 2/2 keywords, 2 deep reads (Chai, Smetana), gap test unbeaten
  throughout. **Next: Knowledge-Based Systems** (`crash prediction`, `risk
  assessment framework`, `knowledge extraction traffic`).

## [2026-06-11] reading | EAAI keyword 1 — field taxonomy found + output-validation method
- Record: `raw/papers/tier1_journal3/EAAI-abstract-refs.md` · triage: [[wiki/progress/journal-triage]]
- EAAI keyword 1 (`traffic accident prediction`): ~95 results (mostly pure flow
  forecasting + AV/maritime noise). 2 deep reads + 3 abstract-only.
- **Chai et al. 2024 (95-study systematic review)** → DEEP READ, positioning gift.
  Gives the field's 4-category taxonomy and our term: **CRM = Crash Risk Modeling**
  (segment-level risk) — the LEAST-explored category (8%), and all its exemplars output
  a numeric score, none NL. NL/explanation is not one of their 5 future directions →
  quantified gap-by-omission. `related-work`/`home`-mapping.
- **Smetana et al. 2026 (LLM + OSHA construction accidents)** → DEEP READ. First paper
  in the whole sweep that actually validates LLM summary faithfulness with a computed
  metric (SelfCheckGPT fact-consistency, 83%). STACKS with our gap rather than beating
  it: their check = output-faithfulness ("prose faithful to source"), our significance
  gate = input-validity ("pattern real"). Heaviest borrow yet for the explanation-output
  layer; refines our story to "borrow their output check + add the significance gate
  they lack." Gap test UNBEATEN. `related-work`/`borrow`.
- **Net:** the two axes are now both well-grounded AND we have a concrete output-validation
  method to adopt. Domain/context home now has a name (CRM) and a quantified white space.
- Notable: **next = EAAI keyword 2 (`road risk assessment AI`).**

## [2026-06-11] reading | ESWA keyword 3 swept — ESWA complete
- Record: `raw/papers/tier1_journal2/ESWA-abstract-refs.md` · triage: [[wiki/progress/journal-triage]]
- ESWA keyword 3 (`accident risk machine learning`): ~52 results, ~11 dup of kw1/2, heavy
  off-domain noise (maritime/aviation/insurance/mining). 3 abstracts: railway-report KG
  (`background`, cross-domain text→KG→risk, pre-LLM), road small-sample ensemble
  cause-analysis (`borrow`, alt. to WGAN for fatal-class imbalance), and RACI (aviation
  RAG+LLM) — pulled full text, knocked down: its mAP/mNDCG validates only the Retriever
  (categorical-taxonomy similarity), not the generated explanation, which is purely
  qualitative. Brick #4 of "explain, never validate" (4 papers/4 domains). `related-work`/`borrow`.
- **ESWA done**: 3/3 keywords, 2 deep reads (Tab-Text, Hussien), gap test unbeaten
  throughout. **Next: Engineering Applications of AI** (`traffic accident prediction`,
  `road risk assessment AI`).

## [2026-06-11] reading | ESWA keyword 2 — Hussien, the heaviest explanation-layer brick
- Record: `raw/papers/tier1_journal2/ESWA-abstract-refs.md` · triage: [[wiki/progress/journal-triage]]
- ESWA keyword 2 (`road safety decision support`): ~79 results (noisy, ~10 dup of kw1) →
  3 abstracts → 1 deep read.
- **Hussien et al. 2025 (ESWA, KG+LLM+RAG explainable behavior prediction; Sotelo group)** —
  DEEP READ. Strongest, most rigorous explanation-layer system to date, NOT knockable. 3-phase
  neuro-symbolic: features→linguistic KG → KGE → Bayesian inference, with fuzzy rules + RAG/GPT-4
  generating the NL justification. Explanation-layer is now firm prior art across 3 papers.
- **Key leverage:** all 3 (Zhang, Gyawali, Hussien) generate NL explanations but NEVER validate
  them — explanation faithfulness is an open hole the whole subfield leaves → our
  significance-gated, statistically-validated explanation is the answer. Hussien is also the
  failure mode we design against (prompt forbids hedging, asserts "will cross BECAUSE…") →
  perfect contrast for our association-not-causation discipline.
- Abstract-only: Sarraf & McGuire 2020 (MCDM safe route planner, `integration` — route planning
  is a real downstream consumer of our risk score); SSARA 2026 (`skip`, term-collision).
- Notable: gap-test unbeaten on every axis; **next ESWA keyword: `accident risk machine learning`.**

## [2026-06-11] reading | ESWA keyword 1 swept — Tab-Text, the input-pipeline twin
- Record: `raw/papers/tier1_journal2/ESWA-abstract-refs.md` · triage: [[wiki/progress/journal-triage]]
- ESWA keyword 1 (`crash severity prediction`): ~29 titles → 4 abstracts → 1 deep read.
- **Tab-Text (Zhen & J.J. Yang, 2025, ESWA)** — DEEP READ. Template-generated
  tabular→narrative→ELECTRA multi-modal severity classifier (Victoria CrashStats, ~1.6%
  fatal — same as STATS19). This is the closest precedent to Phase 1's tabular-to-text
  step found yet → it converts our narrative-generation from a contribution into citable
  PRIOR ART (2nd venue after Li 2025). Narrative nearly doubles fatal-class accuracy
  (9.63% vs 5.25%); ablation confirms text helps most on rare classes.
- **Net effect on novelty:** our cleanest surviving distinction is NL-as-OUTPUT vs
  NL-as-INPUT — Tab-Text/Li use the narrative as an internal feature, never shown to a
  human; ours is the deliverable. Novelty now pinned to the JOIN: NL-explanatory-output ×
  condition-conditioned segment × significance-gated. Gap test still unbeaten.
- Abstract-only: NLP/text-mining survey (Zhang 2026, redundant), macro/micro CPM ensemble
  (Rúa 2024, a 2nd "aggregate→score" anchor beside Jiang), PST-CGCN causal GCN (Hu 2025).
- Watch: Zhen & J.J. Yang (Univ. Georgia) — active LLM+crash lab, closest competitor.
- Notable: **ESWA keyword 1 done; next keywords `road safety decision support`, `accident
  risk machine learning`.**

## [2026-06-09] structure | Project split into PHASE1 (archive) + PHASE2 (active)
- Moved all Phase 1 work into `../PHASE1/` via `git mv` (history preserved); kept
  CLAUDE/git/Obsidian/env infrastructure at root.
- Created `PHASE2/` with `PLAN.md` + a fresh wiki (index, log, overview, raw/).
- Updated `CLAUDE.md`: directory structure, read-only archive rule, session-start
  protocol now point at PHASE2.
- Notable: fresh-but-linked chosen over continue-in-place — Obsidian resolves
  `[[wikilinks]]` vault-wide so PHASE1 stays reachable while the reframe gets a clean slate.

## [2026-06-11] reading | T-ITS extra keyword sweeps — explanation-layer grounding found
- Record: `raw/papers/tier1_journal1/T-ITS-abstract-refs.md` · triage: [[wiki/progress/journal-triage]]
- Three more T-ITS keywords swept: `hotspot identification` (0 keepers — off-domain), `risk-aware
  routing` (1 abstract: Safe & Sound, crime-not-crash), `LLM transportation` (~313 hits, triaged
  top ~50 → 6 abstracts → 1 deep read).
- **Zhang et al. 2025 (Reflective LLM Prompt Optimisation, ITSC)** — DEEP READ, the find of the day.
  First grounding for the *explanation layer*: names our "fluent-yet-unfaithful" risk, hands us a
  validate-then-explain architecture + 3 faithfulness dimensions to borrow. Edge: our significance
  test beats their unreliable LLM-judge validity gate → claim "significance-gated explanation."
- **Gyawali 2025 (SPW)** — full text, knocked down to a note; a thin demo but architecturally a
  near-mirror of our Phase 1 stack (XGBoost→SHAP→RAG→LLM→NL).
- Notable: generic "LLM explanation layer" is now PRIOR ART (2 papers) → explanation novelty narrows
  to condition-conditioned + significance-gated; the condition-conditioned-segment-risk gap remains
  unbeaten. **T-ITS exhausted across all planned keywords; next journal: Expert Systems w/ Applications.**

## [2026-06-09] reading | T-ITS Tier-1 deep reads — multimodal twin + safe route mapping
- Record: `raw/papers/tier1_journal1/T-ITS-abstract-refs.md` (full reads on top + 5 abstract refs)
- Li et al. 2025 (Multimodal crash risk of violations): closest twin; validates text+tabular+LLM
  direction; clean inversion (they encode→predict event-level for enforcement; we generate→explain
  segment-level for drivers). Borrow: TabNet, text-categorisation pipeline, imbalance handling.
- Jiang et al. 2022 (Safe Route Mapping): the bigger find — roots us in SPF/Empirical Bayes/HSM
  (the risk-assessment home) AND shows our route-risk-map deliverable already exists → novelty
  must live in condition-conditioning + NL why + significance.
- Notable: gap now sharply defined across both papers; our raw idea is NOT novel on its own —
  this is good to learn now. Next journal: Expert Systems with Applications.

## [2026-06-09] progress | Journal triage log started — T-ITS shortlist
- Page: [[wiki/progress/journal-triage]]
- Workflow set: search → shortlist titles → abstracts (decide) → full text for keepers →
  deep-read + ingest, one journal at a time.
- T-ITS: 7 of ~25 results kept for abstract review (multimodal-crash-risk twin, risk-assessment
  survey, XAI severity, vehicle-group prediction, safe-route mapping, in-vehicle warning, GAN
  imbalance); rest skipped at title stage as off-layer micro-AV/control work.

## [2026-06-09] plan | Journal exploration strategy added to PHASE2/PLAN
- Page: [[PHASE2/PLAN]]
- Folded the supervisor's 25-journal list into the plan: triaged to a relevant subset,
  paired with the round-1 road-safety domain venues into two families (domain = risk-
  assessment home; AI list = applied-AI framing/method home; T-ITS bridges both).
- Added a 3-tier exploration order with per-journal search terms: Tier 1 = AI×road-safety
  intersection (T-ITS, ESWA, EAAI, KBS + AAP/AMAR), Tier 2 = application/framing (Smart
  Cities, DSS, IJDRR, IoT, Sensors), Tier 3 = method/breadth sweep (MAKE, BDCC, megajournals).
- Notable: the prof's list being AI-heavy is itself a signal — the thesis is expected to
  read as applied AI, so the framing should foreground the intelligent-systems angle.

## [2026-06-09] progress | Phase 2 kickoff — supervisor pushed for literature grounding
- Page: [[wiki/progress/2026-06-09]]
- Notable: eval declared fine by supervisor (stop polishing); the "artificial" critique
  returned, meaning the contribution needs an external research home, not more internal
  self-justification; week of reading planned around risk assessment / route planning / AVs.
