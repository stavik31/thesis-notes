---
title: "Phase 2 Positioning Memo — Securing the Research Home"
type: memo
date: "2026-06-16"
status: SUPERSEDED (2026-06-17) — kept as the audit trail of the pivot. See ../PHASE3
tags: [phase2, positioning, related-work, decision, superseded]
---

> **⚠️ SUPERSEDED 2026-06-17.** At the third supervisor meeting the LLM/NL-explanation
> direction this memo argues was **cut** (faithfulness unsolvable in the time; language
> distracting + per-person). The thesis moved to **risk-aware route planning with a
> vehicle-type data niche** — see `../PHASE3/PLAN.md` and `../PHASE3/positioning-memo.md`.
> The CRM home, the Gao 2024 baseline, and the condition-conditioning evidence survive as
> the *risk engine*; the LLM half is now future-work. This file is retained as the audit
> trail of how the position got here — do not act on its recommendations.

# Phase 2 Positioning Memo — Securing the Research Home

> **What this is.** The single document that converts a week of reading (~40 papers across
> 10 journals) into a defensible position for the thesis. It answers the four questions the
> [[PHASE2/PLAN]] set out — *what field, what cited gap, what framing, what baselines* — and
> closes the supervisor's "artificial / no research home" critique. Read this top-to-bottom
> to understand the whole argument; the last section (Part 10) is how to deliver it to the
> supervisor.
>
> **Honest status of the corpus.** Tier 1 (T-ITS, ESWA, EAAI, KBS, AAP) was read in full.
> Tier 2 (Smart Cities, DSS, IJDRR, IoT/Sensors) was swept — only DSS produced a keeper
> (Ryder 2017). Tier 3 was assessed as diminishing-returns and not run. The gap survived
> every relevant venue. That is the central finding.

---

## Part 0 — The problem this memo solves

The supervisor's repeated critique was not about the build. It was: **the method is a
*floating capability* with no research home, so it reads as "artificial."** In round 1 I
answered with a *self-constructed* gap ("nav says *that* a crash happened; mine says *why*")
argued from first principles. It didn't land — because an invented justification isn't a
research home. He prescribed the fix explicitly: **read good-journal papers, find the
existing research conversation this plugs into, and position against it in that field's
language.**

So the test for this memo is narrow and concrete: *can I now name the field, cite its gap,
name the baseline I improve, and state my contribution in the field's own vocabulary —
without inventing anything?* The answer is **yes**, and the rest of this document is the
evidence.

---

## Part 1 — The answer in one paragraph

This thesis contributes to **Crash Risk Modeling (CRM)** — a named subfield of ML-based road
accident prediction (Chai et al. 2024, EAAI) that estimates crash risk at the level of a
**road segment**. CRM is the *least-explored* of the field's four categories (8% of studies),
and across the entire literature **every CRM system outputs a number** — a risk score, rate,
or probability, usually rendered as a heat map. The flagship-venue state of the art on *our
exact dataset* (Gao et al. 2024, AAP — road-level crash risk on **UK STATS19**, three London
boroughs) is exactly this: a severity-weighted probabilistic risk score per road segment,
with weather as an *input feature*, no test of which conditions are statistically
overrepresented, and **no natural-language explanation of why a segment is risky.** My
contribution is the *join* of three things that no paper in the corpus combines: **(1)
natural language as the explanatory *output* a human reads** (the field uses generated text
only as an internal *input* feature to a classifier), **(2) conditioning the risk on the live
situation** (weather/light/time), gated by **(3) a real statistical significance test** that
decides which patterns are allowed to be spoken at all. STATS19 is the case study; the method
is jurisdiction-agnostic.

---

## Part 2 — The research home: Crash Risk Modeling (CRM)

**Source of the home: Chai, Lau, Tee & McCarthy 2024 (EAAI), a 95-study systematic review.**
This is the most valuable single paper of the sweep because it hands us the field's own map.
ML-based road traffic accident prediction splits into four modeling categories:

| Category | What it does | Share of studies |
|---|---|---|
| **CRM — Crash Risk Modeling** | risk/probability of a crash at a **road segment** over a period | **8% (least explored) ← us** |
| COM — Crash Occurrence Modeling | binary crash / no-crash event classification | 17% |
| CSM — Crash Severity Modeling | severity-level classification (Phase 1's *old* task) | 62% (dominant) |
| CFM — Crash Frequency Modeling | counts per segment → hotspot identification | 13% |

Three things this gives us, all citable:

1. **A name in the field's vocabulary.** We can now open related-work with *"this thesis
   contributes to crash risk modeling (CRM)"* — not an invented framing.
2. **A quantified white space.** CRM is the thinnest category. Every CRM exemplar Chai cites
   (RiskCast, DeepRisk, Li 2020, Zhao 2019) outputs a numeric score; none condition-conditions
   the output, none explains in language.
3. **A gap-by-omission.** Chai's five stated future directions are multitask prediction, data
   quality, hybrid approaches, transferability, and a standardized framework. *Interpretability
   appears only in the narrow SHAP/LIME feature-attribution sense.* Natural-language
   communication of risk to a human is **never mentioned across 95 studies.** The field does
   not even see this as an open problem yet — which is exactly the kind of gap a thesis wants.

**The honesty nuance that makes the position *sharper*, not weaker:** Chai's "key factors"
columns show many studies already *use* weather, time, and road characteristics — but as
*input predictors feeding a number*. So "uses weather/light/time" is not itself novel. Our
distinction is precise: every category outputs a number or a class; **none surfaces a
condition-conditioned pattern as natural language.** Conditions-as-features ≠ condition-
conditioned-explanation-as-output. State it this way and there is no overclaim to attack.

**The methodological home underneath CRM** comes from Jiang et al. 2022 (T-ITS, Safe Route
Mapping): it roots us in the canonical road-safety risk-assessment lineage — **Safety
Performance Functions (SPF) + Empirical Bayes (EB) + the Highway Safety Manual (HSM)** — the
"risk assessment" home the supervisor originally named. This is corroborated by the SA-EB
framework paper (AAP, abstract) confirming EB/HSM is still the state-of-practice baseline.

---

## Part 3 — The gap, in the field's own language

State the gap on **two axes**, because the corpus splits cleanly along them:

**Axis 1 — the risk side (what CRM produces).** The field either:
- *encodes crash text → predicts an outcome* at the **event level** (Li et al. 2025, T-ITS —
  multimodal violation crash risk for enforcement), or
- *aggregates crashes → numeric score → heat map* at the **segment level** (Jiang 2022;
  Gao 2024; Rúa 2024 — the "aggregate→score" family).

Neither **conditions the output on the live situation**. Weather enters as a training feature
that improves the aggregate number; it never produces "this segment is risky *in rain at
night*" as distinct from "*in dry daylight*."

**Axis 2 — the explanation side (how risk is communicated).** A real subfield now generates
NL explanations of ML predictions — but:
- it explains *generic predictions/attributions*, never condition-conditioned segment crash
  patterns, and
- **the faithfulness of the explanation is essentially never validated.** Across five papers
  in five domains (Zhang 2025 traffic-GNN; Gyawali 2025 V2X cyber; Hussien 2025 AD behavior;
  RACI 2025 aviation; TrafficRiskGPT 2025 AD scene-risk) the *prediction* is evaluated
  rigorously and the *generated explanation* is shown only as qualitative examples. The one
  exception (Smetana 2026) validates output faithfulness on a *different axis* and a different
  domain — see Part 7.

**The combined white space (the thesis):** *condition-conditioned, significance-gated,
natural-language explanation of segment-level crash risk, delivered to a human.* Every paper
in the corpus misses at least one of those four properties. None has all four.

---

## Part 4 — The novelty, pinned precisely (the JOIN)

Reading sharpened the novelty by *removing* the parts that turned out to be prior art. This
is good — it means what remains is defensible.

**What is NOT novel (adopt-and-cite, do not claim):**
- **Tabular-to-text crash narratives.** Prior art in two venues: Li et al. 2025 (T-ITS) and
  Tab-Text / Zhen & Yang 2025 (ESWA). Phase 1's narrative step is *adopted method*, not
  contribution.
- **The LLM-explains-ML architecture (SHAP/RAG → LLM → NL).** Prior art across Zhang, Gyawali,
  Hussien. The *shape* of the pipeline is established.
- **LoRA fine-tuning of an ~8B LLM for traffic risk.** Prior art four times over: TrafficRiskGPT
  (KBS 2025), Li et al. 2026 (AAP), DRPVLM (AAP), Gyawali (T-ITS). Our use of LoRA is
  *validated by precedent*, not novel.

**What IS novel — the join of three properties no paper combines:**

> **NL-as-explanatory-OUTPUT × condition-conditioned segment patterns × significance-gated selection.**

1. **NL as OUTPUT, not INPUT.** This is the single cleanest line we hold. The entire
   tabular-to-text crash family (Li 2025, Tab-Text 2025, pavement+LLM, railway KG) uses the
   narrative as an *internal feature* the classifier consumes to predict a class — **it is
   never shown to a human.** Ours *is* the deliverable a person reads. Encode→predict vs
   generate→explain.
2. **Condition-conditioned.** Risk is stratified by live conditions (wet/dark/rush-hour), not
   collapsed into one aggregate score with weather buried as a feature. Multiple AAP papers
   (Wei 2024, Wang 2025) prove condition-conditioning is *valid and meaningful* at the segment
   level — but they output curves/probability tables, not language.
3. **Significance-gated.** A real statistical overrepresentation test decides which patterns
   are allowed to be spoken. This is the methodological core (it was already flagged as such in
   Phase 1's [[../PHASE1/wiki/progress/NEW_FIX_PROF]] Stage 2). It is what separates "crashes
   happen wherever there's traffic" from "this place has a *non-random* pattern," and it is the
   answer to the unsolved faithfulness problem on Axis 2: the LLM only explains patterns that
   passed a real test.

**The discipline that protects the claim:** the NL must say *"overrepresented under wet+dark,"*
**never** *"caused by wet+dark."* We report association, not causation. Two papers give us a
*principled* (not hand-wavy) reason for this: TrafficRiskGPT shows what true causal claims
require (a hand-built DAG + backdoor adjustment + ATE per scene) — tractable for ~5 kinematic
variables in one scene, but it does **not** scale to population-level segment×condition risk.
So association-testing is the honest, tractable choice, not a cop-out.

---

## Part 5 — The keystone baseline: Gao et al. 2024 (STZITD-GNN, AAP)

This is the most important find of the entire sweep and the paper the thesis should position
against most directly. It answers the supervisor's deepest demand — *show me the existing
research this plugs into* — on our exact dataset, in the flagship venue.

**What it is.** Gao, Jiang, Haworth et al. 2024 (AAP 208, UCL SpaceTimeLab). A Spatiotemporal
Zero-Inflated Tweedie Graph Neural Network predicting road-level (segment-level) crash risk on
**UK STATS19** (Department for Transport), in three London boroughs (Westminster, Lambeth,
Tower Hamlets). Road segment = graph node; GRU (temporal) + GAT (spatial) encoder → a 4-param
Zero-Inflated Tweedie decoder → a full probabilistic crash-risk distribution per road, 14 days
ahead, with uncertainty intervals. Target = a severity-weighted crash score (minor/serious/
fatal = 1/2/3). Open access, code on GitHub.

**Why it is the perfect foil — it is "everything but our contribution":**
1. **Output = a numeric severity-weighted risk score + heat map. No natural language.** The
   analyst sees a coloured road and a number, never *why*.
2. **Weather is an INPUT feature, not a conditioning axis of the output.** It improves the
   aggregate daily prediction but never yields "risky *in rain*" vs "risky *at night*."
3. **No significance gate.** Risk is a learned continuous score; nothing tests whether a
   specific condition is statistically overrepresented among a segment's crashes.
4. **"Uncertainty-aware" ≠ explanation.** Their uncertainty is a prediction interval (how
   confident the number is), not a faithfulness-validated reason.

**Our delta, stated against a real, recent, top-venue baseline:**
> *"The state of the art for road-level crash risk on STATS19 (Gao et al. 2024, AAP) produces
> a severity-weighted probabilistic risk score per road segment, rendered as a heat map. It
> does not condition the output on situational factors, does not test pattern significance,
> and does not explain risk in natural language. This thesis adds exactly those three."*

That sentence is the de-artificialization in one move: the home is real, the baseline is real,
the delta is precise.

**Independent corroboration of the gap.** Gao's Table 1 surveys 14 prior road/region crash-
prediction models — **every one outputs a "risk score" or "occurrence," none an explanation.**
This is Chai 2024's gap-by-omission confirmed a *second* time, from a different literature
table, specifically for the CRM family.

**What we borrow from it (it is also our richest method donor):**
- **Zero-Inflated Tweedie** for the ~96% zero-inflation Gao reports (95.72% / 96.71% / 96.28%
  across the three boroughs) — *our exact STATS19 sparsity problem*, with the fatal-class
  imbalance as its extreme tail. A principled, STATS19-validated alternative to SMOTE.
- **Road-segment-as-node + GAT** spatial encoding, if we want spatial spillover between segments.
- **Severity-weighting scheme** (minor/serious/fatal = 1/2/3) as a citable way to collapse
  STATS19 severity into one risk target.

---

## Part 6 — The evidence map (every paper, what it proves)

This is the audit trail. Each paper is logged in its journal's `*-abstract-refs.md`; this table
is the consolidated view of what each *does for the argument*.

### 6A — The gap test: "is anyone doing condition-conditioned, significance-gated, NL segment risk to a driver?"

Every paper below was tested against that question. Every answer was **no.** These are the
"bricks" — each one is a near-neighbour that misses on a specific, nameable axis.

| Paper (venue) | How close it gets | Why it misses (the brick) |
|---|---|---|
| **Gao 2024** (AAP) ★ | road-level CRM on UK STATS19 itself | numeric score + heat map; weather=input; no significance; no NL |
| Jiang 2022 (T-ITS) | segment risk + route heat maps for drivers | SPF/EB numeric fuzzy score; no condition-conditioning; no NL |
| Li 2025 (T-ITS) | text + tabular + LLM crash risk | NL-as-*input*; event-level; for enforcement, not drivers |
| Tab-Text 2025 (ESWA) | tabular→narrative→classifier, same imbalance | NL-as-*input* feature; severity output; never shown to a human |
| TrafficRiskGPT 2025 (KBS) | LLaMA3+LoRA+CI-CoT fluent NL risk reasoning | agent-consumed; scene/kinematic-level; no faithfulness check |
| Hussien 2025 (ESWA) | KG+LLM+RAG, rigorous NL justifications | AD behavior, event-level; explanation never validated |
| Zhang 2025 (T-ITS) | validate-then-explain, names "fluent-yet-unfaithful" | traffic-GNN forecasting; validity gate is an unreliable LLM-judge |
| Wu 2026 (AAP) | VLM → NL road-safety diagnostics, expert-validated | addressee = *engineers* for redesign; retrospective; no conditioning |
| Li 2026 (AAP) | GPT-2+LoRA causal graphs, real-time crash risk | event-level kinematics; *self-states* "excludes weather and road geometry" |
| Ryder 2017 (DSS) | full in-vehicle hotspot-warning DSS, field-tested | warnings are **condition-agnostic**; static label; no significance; no NL |
| Gyawali 2025 (T-ITS) | XGBoost→SHAP→RAG→LLM (mirrors Phase 1) | V2X cyber demo; zero explanation evaluation |
| RACI 2025 (ESWA) | RAG+LLM aviation cause identification | metrics validate the *retriever* only; generation purely qualitative |
| DDLM (AAP) | visual LLM + reasoning chain, generates explanations | driver-distraction classification; no faithfulness validation |
| DeepSeek+MCTS (AAP) | LLM root-cause chain reasoning | identifies cause *categories*, event-level; validates label not reasoning |

**The takeaway:** the gap is not unbeaten by luck. It is unbeaten because each property we
combine is individually present somewhere, but the *combination* — and specifically NL-as-output
gated by real significance on condition-conditioned segment risk — is in none of them.

### 6B — The pipeline is grounded on all three axes (the "artificial" critique, structurally answered)

The supervisor said the system is "a floating capability." It isn't — every stage now has
independent prior art proving it is a real, valid thing to do:

| Pipeline stage | Grounded by | What it proves |
|---|---|---|
| **1. Risk modeling** (segment × condition) | Gao 2024 (STATS19 baseline); Wei 2024 (DLM/DLNM segment×condition lagged risk); Wang 2025 (EKC Bayesian network on weather/temp/volume/time) | segment-level condition-conditioned crash risk is published, valid, and meaningful |
| **2. NL generation** (explain in language) | Wu 2026, Zhang 2025, Hussien 2025, Smetana 2026 | LLMs generate domain-valid crash NL; faithfulness is the open problem |
| **3. Delivery to drivers** (the consumer side) | Ryder 2017 (in-vehicle hotspot DSS *works*); + AAP delivery cluster: tailored risk communication; 5.5–6.5s dual-modality warning timing; working-memory complexity limits | driver-facing risk delivery is established practice with known design constraints |

This is the structural answer to "artificial": there is no floating step. Every component
stands on cited prior work; the contribution is the *combination and the significance gate*.

### 6C — The two application framings (a choice still open)

Two viable homes emerged, and they are compatible — but they imply different primary audiences
and related-work emphasis. **This is the one real decision left.**

- **Framing A — CRM (recommended primary).** Home = Chai 2024's CRM category; baseline = Gao
  2024. Audience = road-safety / applied-AI researchers. Strongest because the gap is quantified
  and the baseline is on our exact dataset. Driver delivery becomes the *use case*.
- **Framing B — In-vehicle driver advisory / DSS.** Home = Ryder 2017 (in-vehicle accident
  hotspot DSS); audience = decision-support / HCI-for-safety. Their warnings are condition-
  agnostic static labels; ours are condition-specific significance-gated NL. The "no immediate
  effect, only a learning effect" finding is a concrete motivation for richer warnings. Weaker
  as a *primary* home (n=1 paper) but excellent as the *applied* framing layered on top of A.

**Recommendation:** lead with **A (CRM)**, use **B** as the application/impact section. That
gives a quantified gap (A) *and* a real-world deployment story with a field-tested predecessor
(B).

---

## Part 7 — What we now inherit (the payoff)

Finding the home hands us the things the plan promised "for free."

**Baselines to compare against / improve:**
- **Gao 2024 (STZITD-GNN)** — the primary replicate-and-improve baseline (UK STATS19, code
  available).
- **SPF + Empirical Bayes / HSM** (Jiang 2022; SA-EB framework) — the state-of-practice
  numeric baseline.
- **CPM / aggregate→score family** (Rúa 2024; network-wide screening framework) — secondary
  anchors showing "aggregate→score" is a *family*, not one paper.

**Related-work skeleton:**
- Chai 2024's four-category taxonomy (CRM/COM/CSM/CFM) *is* the structure of the related-work
  chapter.
- The explanation-layer lineage (Zhang → Gyawali → Hussien → Smetana) is the "LLM explains ML"
  subsection, with the unsolved-faithfulness thread running through it.

**The borrow shelf (methods to reuse, all cited):**

| Need | Borrow from | Note |
|---|---|---|
| Zero-inflation / sparsity (~96% zero, fatal 1.5%) | **Gao 2024** Zero-Inflated Tweedie | STATS19-validated; primary |
| Class imbalance (alternatives) | Man 2022 (WGAN, UK M1); DCGAN; extended accident-triangle weighted oversampling (code); WFFS feature selection (UK data) | a whole shelf of options |
| Significance gate (the core) | **Wei 2024** (case-crossover DLM/DLNM); **Wang 2025** (EKC = expert + chi-square CI tests); Li 2026 (transfer entropy); Liu 2021 (BDeu Bayesian-network structure learning) | methodological ancestors — chi-square/CI testing of condition→crash is mainstream |
| Output faithfulness check | **Smetana 2026** (SelfCheckGPT fact-consistency, 83%) | *stacks* with our gate on a different axis (see below) |
| Explanation-eval rubric | **Zhang 2025** (Score Grounding, Contextual Coherence, Causal Plausibility) + overlap-score proxy | our explanation-quality metrics |
| Spatial aggregation to hotspots | Wu 2026 + Ryder 2017 (both DBSCAN) | two independent DBSCAN precedents |
| Tabular-to-text (adopt) | Li 2025; Tab-Text 2025 (ELECTRA backbone, ablation design) | adopt-and-cite, not contribution |
| LoRA architecture (validate) | TrafficRiskGPT; Li 2026; DRPVLM; Gyawali | precedent ×4 |
| Route-planning consumer | Sarraf 2020; Jiang 2022 | downstream slot for our risk layer |

**The faithfulness story, fully assembled (this is a genuine strength):** the field leaves
explanation-faithfulness unsolved (Axis 2). We close it on **two stacked axes**:
- **Input validity** — *our* significance gate: "is the pattern statistically real /
  overrepresented?" (the thing nobody does).
- **Output faithfulness** — *borrowed* from Smetana 2026: "did the prose stay faithful to the
  validated pattern?" (SelfCheckGPT-style fact-consistency).

Significance-gated **and** fact-consistency-checked closes the hole more completely than any
prior work — and we can say so honestly, because half of it is borrowed and cited.

---

## Part 8 — How this de-artificializes the thesis (answering the original critiques)

Mapping the corpus back onto the supervisor's seven round-1 critiques (from
[[../PHASE1/wiki/progress/prof-feedback]]):

1. **"Artificial / no research home."** → Answered. Home = **CRM** (Chai 2024); the system is
   a CRM method with a significance-gated NL explanation layer. Not invented — named by the field.
2. **"Assumes data exists / sparsity."** → Gao 2024 reports ~96% zero-inflation on STATS19 and
   treats it as *the* modeling problem (Zero-Inflated Tweedie). Sparsity is the field's central
   challenge, not our embarrassment; our "silence where there's no significant pattern" is the
   correct design response.
3. **"Too UK-focused."** → CRM is a global field; STATS19 is the *case study*. Gao 2024 (UK),
   Wei 2024 (Texas), Wang 2025 (China), Tab-Text (Australia) show the method paradigm spans
   jurisdictions.
4. **"Live driver's context is missing → generic output."** → This is now the *named
   contribution* (condition-conditioning), validated as meaningful by Wei 2024 and Wang 2025.
5. **"How does it help, not distract the driver?"** → Grounded by the delivery cluster: Ryder
   2017 (field-tested in-vehicle warnings improve behavior over time); working-memory-complexity
   paper (warnings must be short/low-complexity); warning-timing paper (5.5–6.5s dual-modality).
   The pre-trip/route-briefing model + terse condition-gated delivery is now evidence-backed.
6. **"Real-time radius-vs-speed problem."** → Resolved by the offline-precompute / route-segment
   architecture already in [[../PHASE1/wiki/progress/NEW_FIX_PROF]]; the literature (Ryder's
   precompute-from-historical-data design) supports it.
7. **"Severity isn't the point."** → Correct, and the field agrees: severity (CSM) is a
   *different category* (62% of work, well-trodden). We moved to CRM. Severity is demoted to a
   sanity-check, exactly as the field would expect.

**Net:** all seven are answered with citations, not first-principles argument. That is the
difference between round 1 and now.

---

## Part 9 — Honest weak points to pre-empt (the next round)

A defensible position names its own soft spots before the examiner does.

1. **"Causes" are correlational, not causal.** STATS19 (our dump) has no contributory-factors
   table; risk is inferred from overrepresented conditions. *Mitigation:* the association-not-
   causation discipline (Part 4), with TrafficRiskGPT as the principled reason real causal
   inference doesn't scale to population-level segment×condition risk. Never say "caused by."
2. **Does the LLM earn its place over a template?** If output is "segment X overrepresents
   wet-skidding 3×," a template can say that. *Mitigation:* the LLM's value is *synthesis* —
   merging co-occurring factors into one prioritised, non-redundant, condition-conditioned,
   route-level sentence — and this must be *measured* (Zhang's rubric + overlap score), not
   asserted. This is still the most attackable point; confront it directly.
3. **Significance gate design is not yet built.** The *choice* of test (chi-square
   overrepresentation vs Empirical Bayes vs BDeu Bayesian-network structure learning) and the
   baseline (network-wide vs road-class-specific) and the minimum-crashes threshold (fatal at
   1.5% is data-starved) are open. *Mitigation:* this is acknowledged as the core methodological
   work of the build phase, with a borrow shelf already assembled (Wei/Wang/Liu).
4. **n=1 for the in-vehicle framing.** If Framing B is pushed as primary, Ryder 2017 is the only
   direct predecessor. *Mitigation:* keep CRM (Framing A) as the primary home where the baseline
   is plural and quantified.

---

## Part 10 — How to present this to the supervisor

The whole point of the reading week was this conversation. Here is how to run it.

### The 30-second open (lead with the win he asked for)
> *"You said the method was artificial because it had no research home. I read the literature
> and it does have one — it's called Crash Risk Modeling, and there's a 2024 paper in Accident
> Analysis & Prevention that does exactly road-level crash risk on UK STATS19, the same dataset
> I use. I now position directly against it: it outputs a risk score and a heat map; I add the
> three things it doesn't have — condition-specific risk, a significance test, and a
> natural-language explanation."*

That single paragraph closes the round-1 critique. Say it first.

### The three slides to bring (don't bring more)
1. **The taxonomy slide.** Chai 2024's four categories, CRM highlighted as 8% (least explored),
   with "natural-language communication of risk: absent across 95 studies." → *This is the field
   and the gap, in the field's words.*
2. **The baseline-vs-us slide.** A two-column table: **Gao 2024** (numeric score · weather as
   input · no significance · heat map · no NL) vs **This thesis** (condition-stratified · weather
   as output axis · significance-gated · NL explanation · driver-facing). → *This is the delta,
   against a real top-venue baseline on my data.*
3. **The gap-test slide.** The list of ~13 near-neighbours (Part 6A), each with the one axis it
   misses. → *This is why the contribution is genuinely unoccupied, not just unsearched.*

### Two questions to put to him (turn the meeting into a decision)
1. **"Primary framing — CRM, or in-vehicle DSS?"** Recommend CRM as home with in-vehicle as the
   applied layer (Part 6C). Ask him to confirm. *This is the one genuinely open decision and it
   shapes the introduction and related-work.*
2. **"Is significance-gated NL explanation a strong enough methodological core?"** This was his
   round-1 standard ("is statistical significance of segment patterns strong enough to carry the
   thesis?"). Now you can answer it grounded: the faithfulness problem is *unsolved across five
   papers*, and the significance gate is the answer no one else has tried.

### What NOT to do
- Don't re-defend the round-1 invented gap ("nav says *that*, mine says *why*"). It's superseded;
  lead with CRM instead.
- Don't lead with the build/architecture. He declared evaluation fine and wants the *positioning*.
  The architecture is downstream of the framing decision.
- Don't overclaim causation or LLM novelty. The defensible claims are the *join* and the
  *significance gate*; everything else is adopt-and-cite.

### The one-line thesis statement to land
> *"This thesis contributes to crash risk modeling: it is the first system to surface
> condition-conditioned, statistically-significant segment crash-risk patterns as a faithful
> natural-language explanation for a human driver — where the field today outputs only a numeric
> risk score."*

---

## Links

- [[PHASE2/PLAN]] — the reading plan this memo fulfils
- [[wiki/progress/journal-triage]] — the journal-by-journal triage log (the audit trail)
- [[wiki/overview]] — to be rewritten around this memo (next step)
- Reading records: `raw/papers/tier1/tier1_journal1..5/*-abstract-refs.md`,
  `raw/papers/tier2/tier2_journal2/DSS-abstract-refs.md`
- [[../PHASE1/wiki/progress/prof-feedback]] — the round-1 critique this memo answers
- [[../PHASE1/wiki/progress/NEW_FIX_PROF]] — the round-1 design (significance gate = Stage 2)
