---
title: "Presentation Plan — 2026-06-02"
type: progress
date: "2026-05-31"
tags: [progress, presentation]
---

# Presentation Plan — 2026-06-02

**Format:** 15 minutes. Audience: 9 classmates + 2 professors.
**Goal:** Communicate the problem, the gap, what was built, results so far, and what's next.

> **Reading this file:** Each slide has two parts — `On the slide:` (what the audience sees) and planning/narration notes (what you say or context for building the slide). Cut from the slide content; leave the notes alone.

---

## Slide 1 — Title

**On the slide:**
- Location-Specific Crash Risk Warnings Using RAG and Fine-Tuned LLMs
- [Your name] | [Course/Module] | June 2026

---

## Slide 2 — Agenda

**On the slide:**
1. Problem Formulation
2. Related Studies
3. Data
4. Proposed Approach
5. Experimental Setup & Results
6. Future Work
7. Summary

---

## Slide 3 — Problem Formulation

**On the slide:**
- ~1,700 fatal road crashes per year in the UK (STATS19, 2020–2024)
- Existing systems classify severity or explain AV decisions — neither output helps a human driver in the moment
- A driver approaching a dangerous junction has no way to know *why* it is dangerous, based on historical evidence
- **Research question:** Can a RAG-based system produce location-specific, historically-grounded crash risk warnings for drivers?

**Narration notes:**
- Open with the real-world stakes — 1,700 deaths is concrete
- "Classify severity" = Tab-Text, CrashSage (set up the related work slide)
- "Explain AV decisions" = RAG-Driver, RAG-SafeAdapt (also set up)
- The research question is the last bullet — let it land, don't rush past it

---

## Slide 4 — Related Studies

**On the slide:**

**Crash Classification**
- Tab-Text (2023) — fuses tabular + narrative text (ELECTRA encoder); Macro F1 0.4587 vs CatBoost 0.4118; output: a severity label
- CrashSage (2024) — fine-tunes LLaMA3-8B with LoRA; Macro F1 0.7361; adds gradient-based token attribution; output: a label + attribution scores, not user-facing
- Both stop at a label — no output a driver can act on

**LLM Explanation for Autonomous Driving**
- RAG-Driver (2024) — RAG + multi-modal LLM (Vicuna 7B + video encoder); retrieves similar driving scenarios as in-context examples; SoTA on BDD-X benchmark
- RAG-SafeAdapt (2025) — RAG + vision-language model for AV safety in complex traffic scenarios
- Both produce explanations — but for autonomous vehicles, using live sensor data, not historical crash records

**The Gap**
- No system uses RAG over historical crash data to warn human drivers
- Spatial location (lat/long) as a retrieval signal is unexplored

**Narration notes:**
- Walk through tier by tier — crash classifiers first, then AV explanation systems, then the gap
- The gap slide is the pivot: everything before it is "what exists"; everything after is "what this thesis does"
- Tab-Text and CrashSage numbers are exact — cite them if asked
- RAG-Driver uses video frames, not crash databases — fundamentally different input modality

---

## Slide 5 — Data

**On the slide:**

**STATS19 — UK National Road Crash Database**
- Maintained by the Department for Transport
- Mandatory police reporting: every injury collision recorded at scene

**Structure**
- 3 relational tables: Collisions · Vehicles · Casualties (linked by collision ID)
- Key fields: date/time, lat/long, road type, speed limit, junction type, light/weather/surface conditions, vehicle type, casualty type and severity

**Thesis subset: 2020–2024**
- 503,475 collisions
- 3-class severity: Slight 386,007 · Serious 109,977 · Fatal 7,491
- Fatal = 1.5% of records → severe class imbalance

**Narration notes:**
- Mandatory reporting = high coverage, low selection bias — this matters for a thesis claim about representativeness
- The three-table structure is worth mentioning: each collision joins to multiple vehicle records and multiple casualty records — joining them is non-trivial
- The imbalance (1.5% Fatal) motivates the downsampling decision in Phase 1 and foreshadows why zero-shot fails on Fatal class

---

## Slide 6 — Proposed Approach: Architecture

**On the slide:** Diagram only — no bullet text. Narrated verbally while pointing at boxes.

**Diagram structure — two columns: Offline (left) | Online (right)**

Offline column (top to bottom):
```
STATS19 Raw Data (503,475 records)
        ↓
Tabular-to-Text Conversion
(scene · road conditions · vehicles · casualties)
        ↓
Sentence Transformer (all-MiniLM-L6-v2)
        ↓
    ┌─────────────────────┐
    │  FAISS Index        │  ←─── saved to disk
    │  (faiss_index.bin)  │
    └─────────────────────┘
    ┌─────────────────────┐
    │  Metadata           │  ←─── saved to disk
    │  (metadata.jsonl)   │
    └─────────────────────┘
```

Online column (top to bottom):
```
Driver GPS (lat, lon) + Current Conditions (text)
        ↓
[1] Spatial Filter
    haversine distance → crashes within 1km → spatial subset
        ↓
[2] Semantic Search
    encode conditions → FAISS search within subset → top 10 crashes
        ↓
[3] Prompt Construction
    retrieved narratives assembled as context
        ↓
Fine-tuned Gemma-3-4b-it
        ↓
Location-Specific Warning
```

Dashed arrows from disk artifacts into the online column labelled "loaded from disk".

**What to say while pointing at Sentence Transformer:**
Narrative text → tokenised → 6 attention layers → mean-pooled → 384-dim vector. Two crashes with similar conditions produce geometrically close vectors. This is what makes semantic retrieval possible.

**What to say while pointing at FAISS:**
478k vectors in a flat matrix. At query time: L2 distance from query vector to every stored vector → returns k nearest. Exact search, no approximation — acceptable at 478k prototype scale.

**What to say while pointing at Spatial Filter:**
Haversine runs first — it constrains the retrieval pool to crashes that physically happened near the driver. Semantic search then re-ranks within that pool, not across all 478k.

**Narration notes:**
- Do not put encoding internals on the slide — too deep for 15 min, save for questions
- Corpus vs. query set: the indexed crashes are the corpus; held-out crashes simulate live driver queries — a crash cannot be in both
- The bridge between offline and online (the dashed arrows) is the key design point: offline runs once, online runs in real time

---

## Slide 7 — Experimental Setup & Results

**On the slide:**

**Dataset:** STATS19 2020–2024 · 503,475 collisions · 3-class severity · test split: 25,174 records

**Phase 1 — Baseline Comparison**

| System | Macro F1 |
|--------|----------|
| Zero-shot Gemma-3-4b-it (no fine-tuning) | 0.149 |
| XGBoost (tabular features only) | 0.350 |
| Fine-tuned Gemma-3-4b-it (QLoRA r=16) | **0.408** |

Per-class breakdown (fine-tuned): Slight 0.693 · Serious 0.364 · Fatal 0.134

**Phase 2 — RAG System (end-to-end working)**

*Query:* [example location + conditions]
*Retrieved:* X crashes within 1km → top 10 by semantic similarity
*Generated warning:* [example output from query.py]

**Known limitation:** Warning is generic — does not reference retrieved crashes or location-specific patterns. Diagnosis: prompt does not force the model to ground its output in retrieved context. Fix is immediate next step.

**Diagrams to show alongside:**
- SHAP bar chart (`xgb_shap_bar.png`) — which features drive severity prediction (speed limit, light conditions, road type)
- Class distribution bar chart — makes 1.5% Fatal imbalance visually obvious
- UK crash map — lat/lon scatter of 503k crashes, shows geographic spread and density

**Narration notes:**
- Zero-shot never predicts Fatal at all — without domain adaptation the model defaults to majority class (Slight). This is why fine-tuning is not optional.
- F1 0.408 is a proxy metric — the thesis claim is not "LLM beats XGBoost at classification." It's "fine-tuning gives the LLM domain knowledge it needs for RAG generation."
- Be direct about the generic output: "the system works end-to-end, but the warnings are currently generic — that's the known limitation and the first thing I fix next." Saying this yourself is more credible than having an audience member point it out.

---

## Slide 8 — Future Work

**On the slide:**

**End goal:** Demonstrate that RAG over historical crash data produces measurably more location-specific and faithful warnings than an ungrounded baseline

**1 · Fix Generic Output (immediate)**
- Problem: model ignores retrieved context, generates generic advice
- Fix: pre-compute statistics from retrieved set → inject into prompt
  - *"7 of 10 retrieved crashes involved wet roads · 6 of 10 occurred in darkness · junction failure-to-give-way in 5 of 10"*
- Fallback: extract factor frequencies directly and template into warning

**2 · Three-Index Ablation (core experiment)**
- Current: spatial filter + dense semantic search
- Add: feature-based index (FAISS on speed limit · light conditions · road type · junction control · weather)
- 6 variants: spatial · feature · dense · spatial+feature · spatial+dense · all three
- Research question: which retrieval combination produces the most faithful, location-specific warnings?

**3 · Evaluation Framework**

*Retrieval quality (no ground truth needed):*
- Feature overlap rate — do top-K retrieved crashes share field values with the query vs. random baseline?
- Severity distribution shift — does retrieval surface local severity skew vs. corpus-wide average?
- Held-out probe — does retrieval improve classification F1 above the 0.408 no-retrieval baseline?

*Generation quality — RAGAS:*
- Faithfulness — does the warning only make claims the retrieved crashes support? (primary metric)
- Answer relevance — is the warning about the actual query location and conditions?
- Context precision — what fraction of retrieved crashes were actually used?
- Context recall — did retrieval cover the key risk factors present in the query?

**4 · Hyperparameter Tuning**
- Radius R: 500m · 1km · 2km
- Retrieved crashes K: 5 · 10 · 20
- Encoder: all-MiniLM-L6-v2 vs. all-mpnet-base-v2

**Longer term / future work**
- Joint embedding — encode location + narrative in a single vector space (requires custom contrastive model training; out of scope for this phase)
- DBSCAN spatial hotspot analysis — cross-reference crash clusters with retrieval signal
- Live API integration — real GPS + OpenWeatherMap → auto-generated query narrative

**Narration notes:**
- Open this slide by stating the end goal — makes everything that follows feel purposeful rather than a list of TODOs
- The three-index ablation is the thesis's core experimental contribution — spend time on it
- RAGAS: explain that it uses an LLM internally as a judge, so no human annotation is needed — this often gets a question
- Joint embedding: frame it precisely — "this would turn retrieval from a two-stage sequential process into a unified learned similarity function; it's a research contribution in itself and is out of scope for this implementation phase." Shows you understand the space without overselling.

---

## Slide 9 — Summary

**On the slide:**
- **Problem** — Drivers have no way to know why a location is dangerous, based on historical evidence
- **Gap** — Prior work stops at severity labels or explains AVs; no RAG system over historical crash data for human drivers
- **Built** — Tabular-to-text pipeline → fine-tuned Gemma (QLoRA) → FAISS spatial + semantic retrieval → location-specific warning
- **Found** — Fine-tuned Gemma (F1 0.408) > XGBoost (0.350) > zero-shot (0.149); RAG end-to-end working; current output is generic (known limitation)
- **Next** — Fix grounding → three-index ablation → RAGAS evaluation → final results (6-week timeline)

---

## References

- Tab-Text: Bridging Tabular Data and Natural Language for Traffic Safety (2023)
- CrashSage: LLM-Centered Framework for Traffic Crash Analysis (2024)
- [RAG-Driver](https://arxiv.org/pdf/2402.10828) — RAG + multi-modal LLM for AV driving explanations (2024)
- [RAG-based explainable road user behaviour prediction](https://www.sciencedirect.com/science/article/pii/S0957417424027817) — RAG + KG + LLM for AV behaviour (2024)
- [RAG-SafeAdapt](https://journals.sagepub.com/doi/10.1177/09544070251368409) — RAG + vision-language for AV safety (2025)
- [SafeTraffic Copilot](https://pmc.ncbi.nlm.nih.gov/articles/PMC12504690/) — LLM for traffic safety with feature attribution

---

## Links

- [[concepts/system-architecture]] — full architecture detail
- [[progress/RAG_PLAN]] — RAG phase 2 plan
- [[progress/presentation-slides-8-10]] — extended draft for slides 7–9
- [[progress/2026-05-26]] — RAG online phase complete
- [[progress/2026-05-21]] — Phase 1 results
- [[sources/tab-text]] — Tab-Text paper
- [[sources/crashsage]] — CrashSage paper
