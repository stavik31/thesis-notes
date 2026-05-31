---
title: "Presentation Plan — 2026-06-02"
type: progress
date: "2026-05-31"
tags: [progress, presentation]
---

# Presentation Plan — 2026-06-02

**Format:** 15 minutes. Audience: 9 classmates + 2 professors.
**Goal:** Communicate the problem, the gap, what was built, results so far, and what's next.

---

## Slide 1 — Title

- Project title (TBD — something like "Location-Specific Crash Risk Warnings Using RAG and Fine-Tuned LLMs")
- Name, date, course/module

---

## Slide 2 — Agenda

- Problem Formulation
- Related Studies
- Data
- Proposed Approach (Architecture)
- Experimental Setup & Results
- Future Work
- Summary

---

## Slide 3 — Problem Formulation

**Key points:**
- UK roads: ~1,700 fatal crashes/year. STATS19 captures 500k+ crashes over 5 years with rich structured features.
- Existing systems predict crash severity or produce post-hoc explanations — neither output is usable by a driver in the moment.
- A driver approaching a dangerous location has no way to know *why* it is dangerous, based on historical evidence.
- **Research question:** Can a RAG-based system produce location-specific, historically-grounded crash risk warnings for drivers?

---

## Slide 4 — Related Studies

**Slide format:** bullet points, 3-tier structure

**Crash Classification Systems**
- Tab-Text (2023) — tabular + narrative fusion (ELECTRA encoder), Macro F1: 0.4587 vs CatBoost 0.4118; ablation without narratives drops to 0.3946. Victoria, Australia — 292,110 records, 3-class severity. Output: a severity label.
- CrashSage (2024) — fine-tuned LLaMA3-8B (LoRA r=128, alpha=256), Macro F1: 0.7361 vs CatBoost 0.7284. WSDOT dataset, binary classification. Adds gradient-based (Taylor) attribution for word-level token importance. Output: a label + attribution scores — not user-facing.
- Both stop at a severity label — no output a driver can use

**LLM Explanation for Driving**
- RAG-Driver (2024) — RAG + multi-modal LLM (Vicuna 1.5 7B + video encoder), retrieves similar driving scenarios as in-context examples, SoTA on BDD-X benchmark
- RAG-SafeAdapt (2025) — RAG + vision-language model for AV safety recommendations in complex traffic scenarios
- Both produce explanations — but for autonomous vehicles, using live camera/sensor data, not historical crash records

**The Gap**
- No system uses RAG over historical crash data to warn human drivers
- Spatial location (lat/long) as a retrieval signal is unexplored

---

## Slide 5 — Data

**Slide format:** bullet points — what STATS19 is, how collected, what's in it, scale

**What it is**
- UK national road crash database, maintained by the Department for Transport
- Mandatory reporting: every road traffic collision involving injury must be recorded by police

**How it's collected**
- Police officers fill a standardised form (STATS19 form) at the scene
- Covers: collision circumstances, vehicles involved, casualties — all linked by a collision ID

**What's in it**
- 3 relational tables: Collisions, Vehicles, Casualties
- Collisions: date/time, location (lat/long), road type, speed limit, junction type, light/weather/road surface conditions
- Vehicles: vehicle type, manoeuvre, age of vehicle
- Casualties: age, sex, casualty type (driver/pedestrian/cyclist), severity

**Scale (thesis subset: 2020–2024)**
- 503,475 collisions
- 3-class severity — Slight: 386,007 / Serious: 109,977 / Fatal: 7,491
- Strong class imbalance (Fatal = 1.5% of records)

---

## Slide 6 — Proposed Approach: Architecture

**Slide format:** diagram only — no text on slide, narrated verbally

**Two sections: Offline (left) and Online (right)**

The FAISS Index and Metadata are the bridge between the two phases — offline produces them, online consumes them. Shown as dashed arrows labelled "loaded from disk".

### Offline Phase (built once, saved to disk)

STATS19 Raw Data (503,475 crash records) → Tabular-to-Text Conversion → Sentence Transformer (all-MiniLM-L6-v2) → splits into two disk artifacts:
- FAISS Index (faiss_index.bin) — 478k vectors
- Metadata (metadata.jsonl) — collision ID, lat, lon, severity label, narrative

Terminology: the indexed crashes are the **corpus**. The held-out crashes used to simulate queries are the **query set**. This split is not about ML training — it's evaluation integrity: a crash cannot be both in the retrieval pool and used as a live query.

**What happens inside Sentence Transformer (for verbal narration):**
- Narrative text is tokenised into subword pieces
- Fed through 6 layers of attention — each token's vector is refined by context of surrounding tokens
- All token vectors are mean-pooled into a single 384-dim vector — the semantic fingerprint of that crash
- Two crashes with similar circumstances produce vectors that are geometrically close in 384-dim space

**What happens inside FAISS (for verbal narration):**
- 478k vectors stored in a flat matrix — no compression, no approximation (IndexFlatL2)
- At query time: computes L2 (Euclidean) distance between query vector and every stored vector, returns k nearest neighbours
- Exact search — slower than approximate methods but correct, acceptable for 478k at prototype scale

### Online Phase (runs per query)

Two inputs: Driver GPS (lat, lon) + Current Conditions (narrative)

Step 1 — Spatial Filter: haversine distance between driver GPS and every crash in Metadata → keep crashes within 1km → **spatial subset**

Step 2 — Semantic Search: encode driver conditions with same Sentence Transformer → FAISS searches within spatial subset → **top-10 most similar crashes**

Step 3 — Prompt Construction: 10 retrieved narratives assembled as context around query

Step 4 — Fine-tuned Gemma-3-4b-it → **Location-Specific Warning**

**Narration notes:**
- Spatial filter runs first — ensures everything retrieved is geographically relevant
- Semantic search runs within the spatial subset, not the full 478k corpus
- The diagram shows the flow; spatial/semantic internals explained verbally while pointing at boxes
- Do not go into encoding internals on the slide — too deep for 12–15 min, save for questions

---

## Slide 7 — Experimental Setup & Results (now Slide 8)

**Dataset:** STATS19 (UK), 2020–2024, 503,475 collisions, 3-class severity (Slight / Serious / Fatal)

**Narrative construction:** Tabular-to-text templates converting structured fields into natural language paragraphs (scene, road conditions, vehicles, casualties)

**Phase 1 — Three-way baseline comparison (test split: 25,174 records):**

| System | Macro F1 |
|--------|----------|
| Zero-shot Gemma (no fine-tuning) | 0.149 |
| XGBoost (tabular baseline) | 0.350 |
| Fine-tuned Gemma-3-4b-it (QLoRA r=16) | 0.408 |

- Zero-shot never predicts Fatal without domain adaptation
- Fine-tuned Gemma selected as RAG backbone
- XGBoost retained as tabular comparison baseline

**Phase 2 — RAG system working end-to-end:**
- Show example output: query crash → X crashes within 1km → top 10 retrieved → generated warning
- Current limitation: warnings are somewhat generic — prompt engineering is the next step

---

## Slide 8 — Future Work (now Slide 9)

**Prompt engineering (immediate):**
- Force model to surface overrepresented factors at the location vs. national baseline
- Move from generic advice ("watch for motorcyclists") to location-specific insight ("rear-end collisions at this junction are 3x more frequent after dark")

**Evaluation framework:**
- Ablation: spatial filter vs. no spatial filter — does location improve retrieval quality?
- Retrieval quality: severity distribution of retrieved set vs. local STATS19 baseline
- Warning usefulness: human rubric (specific, actionable, grounded)
- Quantitative: RAG-augmented classification vs. fine-tuned classifier on test set

**Architectural experiments:**
- Radius tuning: R = 500m vs. 1km vs. 2km
- K tuning: 5 vs. 10 vs. 20 retrieved crashes
- Sentence transformer comparison: all-MiniLM-L6-v2 vs. all-mpnet-base-v2
- Live API integration: GPS + OpenWeatherMap → auto-derived query narrative

**Longer term:**
- Summarisation fine-tuning (contingency if generation quality remains poor)
- DBSCAN spatial hotspot analysis — do crash clusters align with retrieval signal?

---

## Slide 9 — Summary (now Slide 10)

- **Problem:** Drivers lack location-specific, evidence-based crash risk warnings
- **Gap:** Existing work stops at severity labels or explains AVs — no RAG system over historical crash data for human drivers
- **Built:** End-to-end RAG pipeline — FAISS spatial + semantic retrieval → fine-tuned Gemma → grounded warning
- **Found:** Fine-tuned Gemma (F1 0.408) outperforms XGBoost (0.350) and zero-shot (0.149); RAG system produces location-specific output, prompt engineering needed for depth
- **Next:** Evaluation, ablation, prompt engineering

---

## References (for related work slide)

- Tab-Text: Bridging Tabular Data and Natural Language for Traffic Safety
- CrashSage: LLM-Centered Framework for Traffic Crash Analysis
- [RAG-Driver](https://arxiv.org/pdf/2402.10828) — RAG + multi-modal LLM for AV driving explanations (2024)
- [RAG-based explainable road user behaviour prediction](https://www.sciencedirect.com/science/article/pii/S0957417424027817) — RAG + KG + LLM for AV behaviour (2024)
- [RAG-SafeAdapt](https://journals.sagepub.com/doi/10.1177/09544070251368409) — RAG + vision-language for AV safety (2025)
- [SafeTraffic Copilot](https://pmc.ncbi.nlm.nih.gov/articles/PMC12504690/) — LLM for traffic safety with feature attribution

---

## Links

- [[concepts/system-architecture]] — full architecture detail
- [[progress/RAG_PLAN]] — RAG phase 2 plan
- [[progress/2026-05-26]] — RAG online phase complete
- [[progress/2026-05-21]] — Phase 1 results
- [[sources/tab-text]] — Tab-Text paper
- [[sources/crashsage]] — CrashSage paper
