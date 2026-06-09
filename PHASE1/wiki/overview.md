# Overview

*Evolving thesis argument + project state. Updated after major ingests and milestones.*

---

## Thesis Argument

*(Reframed 2026-06-04 following supervisor feedback — see [[progress/prof-feedback]].)*

Drivers have no access to **localized, actionable knowledge of *why* crashes happen** on the
roads they are about to travel. Generic road-safety advice ("take care in the wet") ignores
the fact that risk is concentrated at specific segments and tied to specific conditions — a
particular bend produces wet-surface skidding crashes in the dark; a particular junction
produces failure-to-give-way collisions. That information exists in historical crash records
but is locked in structured tables no driver can use.

This thesis proposes and evaluates a **method for turning crash records into a conditioned,
pre-trip route briefing of actionable crash *causes*.** Offline, it mines a national crash
dataset to identify high-risk road **segments** and the **condition→mechanism cause profiles**
that are statistically overrepresented at each (e.g. "wet surface + darkness → skidding,
3× the network baseline"). At trip-planning time, the driver supplies origin, destination, and
departure time; the system maps the route to its segments and produces a briefing of the
specific hazards to anticipate, conditioned on the current situation, **delivered before the
drive — not as a real-time in-vehicle interruption.**

**The contribution is the reframing on three axes:**

1. **Cause, not severity.** The deliverable is *what to watch for and why*, not a Slight/
   Serious/Fatal label. Severity classification is demoted to a sanity-check that the model
   understands crash data.
2. **Pre-trip, not real-time.** Computing the whole route up front removes LLM latency,
   removes in-drive driver distraction (itself a leading crash cause), and dissolves the
   fixed-radius problem (a 1 km lookahead means 36 s at 100 km/h but 6 min at 10 km/h).
3. **General method, STATS19 as case study.** The pipeline (mine conditions → segment cause
   profile → verbalize) is jurisdiction-agnostic; STATS19 is the instantiation because it is
   the best open dataset available, not the subject of the thesis.

Both prior papers ([[sources/tab-text]], [[sources/crashsage]]) stop at a severity label or an
attribution score; neither produces output usable by an end user, neither uses spatial
location, and neither communicates cause. This system does all three.

The supporting work: correlation analysis (Mutual Information) to establish which conditions
are overrepresented and where; spatial clustering to define segments and test that location
adds signal; retrieval-grounded LLM generation to verbalize segment profiles into prioritized,
non-redundant, condition-conditioned route briefings.

---

## State of the Project

**Phase:** Phase 1 complete; Phase 2 RAG infrastructure built; **direction under review
2026-06-04.** The offline segment cause-profiling + pre-trip route briefing design is an
**exploratory candidate, not a committed decision** — real-time per-GPS-point delivery is the
part being dropped. See [[progress/prof-feedback]].

**Done:**
- Two foundation papers processed (Tab-Text, CrashSage)
- Dataset: STATS19 (UK), 5 years, ~503k collisions, 3 relational tables
- Tabular-to-text: 503k crash narratives generated
- LLM fine-tuning: `google/gemma-3-4b-it`, QLoRA r=16, 3 epochs — **severity adapter now
  treated as domain adaptation only; severity F1 is a sanity-check, not a result**
- Three-way severity comparison (zero-shot 0.149, XGBoost 0.350, fine-tuned 0.408) —
  **demoted from headline to proxy/sanity-check**
- RAG infrastructure: FAISS index, embeddings, end-to-end pipeline runs — but output is
  generic (not yet grounded in retrieved evidence)
- Grounding test (2026-06-02): force-cite prompting reliably yields 3–4 crash citations per
  query — confirms grounding is achievable via prompting

**Next (post-redirection):**
1. Define the **segment** unit (road link / grid cell / DBSCAN cluster) and the
   significance test for a "real" cause profile vs noise
2. Pre-aggregation as **segment cause-profiling** (the [[progress/future-plan]] Part 1 fix is
   now the core of the system, not polish)
3. Route → segments mapping + pre-trip briefing generation
4. Heat map as the macro analytical artifact (per-cause risk surface)
5. Evaluation: faithfulness (RAGAS), cause/feature overlap, base-rate significance; and a
   defensible theory of change for the briefing

---

## Key Open Questions

*(Reordered 2026-06-04 — the top four are the ones the supervisor will press next.)*

1. **Theory of change:** does a pre-trip cause briefing actually change driver behaviour, and
   how is that argued or evaluated? (The justification the feedback really demands.)
2. **Correlational vs causal:** STATS19 (this dump) has no contributory-factors table — causes
   are *inferred* from overrepresented conditions + mechanics. How is output framed honestly
   as *patterns*, not proven causes?
3. **Segment definition + significance:** what is a segment, and how many crashes (and what
   base-rate test) before a profile is signal not noise? Fatal at 1.5% is data-starved.
4. **Why the LLM:** if a profile is "wet-skidding 3× baseline," a template can say that — what
   does the LLM add that a template cannot? (Synthesis, prioritization, condition-conditioning,
   route-level prose.)
5. Which retrieval strategy surfaces the most condition-relevant crashes — dense semantic,
   feature-based, or keyword? (The [[progress/future-plan]] ablation, reframed.)
6. How to evaluate route-briefing quality beyond severity F1 — RAGAS faithfulness + feature
   overlap + temporal holdout are candidates.

---

## Literature Landscape

The field has two clear approaches as of 2025:

- **Data-centric multimodal** (Tab-Text): keep tabular features, add narrative as a modality,
  encoder LLM. Beats baselines, interpretable via permutation importance, no word-level
  explanation.
- **Model-centric generative** (CrashSage): convert everything to narrative, fine-tune decoder
  LLM (LLaMA3-8B + LoRA), explain via gradient attribution. Word-level insight, but
  single-jurisdiction and binary classification only.

Both cite CatBoost as the tabular baseline to beat, the same XAI lineage (SHAP, LIME,
attention), and the same core problem (semantic information loss in structured crash data).

**The gap this thesis fills:** neither paper produces end-user output, communicates *cause*,
uses *spatial location*, or considers *how and when* safety information should reach a driver.
Both treat crash analysis as classification with optional post-hoc explanation. This thesis
reframes the task as **localized cause communication delivered out of the driving moment** —
a problem neither the crash-classification literature nor the (separate) AV-explanation
literature (RAG-Driver et al.) addresses.

*Last updated: 2026-06-04 | Sources: 2 | Pages: 21*
