---
title: "Future Implementation Plan — Grounding, Evaluation, and Retrieval Ablation"
type: progress
date: "2026-06-02"
tags: [progress, plan, rag, evaluation, experiment]
---

# Future Implementation Plan

This document describes the three-part research arc for the remaining 6 weeks of the thesis. Each section explains what needs to be built, why it matters, and what it looks like to someone unfamiliar with the technical details.

---

## The Research Arc

**Hypothesis:** Structured retrieval-grounded prompting produces location-specific safety warnings that are measurably more faithful to retrieved evidence than baseline RAG.

**Experiment:** Build the fix, evaluate it formally, then ablate the retrieval strategy.

**Result:** A quantified improvement backed by a novel finding. No prior crash risk paper has done this.

**Plain English version:** Right now the system works end-to-end but its output is generic — it says things like "drive carefully in wet conditions" without referencing any of the actual crashes it retrieved. The plan is to: (1) fix that, (2) measure how much we fixed it using an established scoring framework, and (3) run an experiment to figure out which method of searching the crash database gives the most useful results. Together, these three things turn "we built something" into "we found something."

---

## Part 1 — Make the Grounding Actually Good

**What:** Improve the prompt so the model produces specific, evidence-citing warnings instead of generic advice.

**Timeline:** Week 1

### The Problem

The current system retrieves 10 historical crash records near the query location and hands them all to the language model as raw text. The model is then expected to read all 10 crashes, count patterns, and synthesise a coherent warning — all in one step.

A 4-billion parameter model is not good at counting or aggregating while also writing. The result is that it ignores the retrieved crashes and writes something generic from its training data instead.

**Plain English:** Imagine you asked someone to read 10 accident reports and immediately write a summary. If they're tired or not paying attention, they'll just write something vague like "accidents happen here — be careful." The problem is we're asking the model to do too many things at once.

### The Fix — Pre-Aggregation

Before passing the crashes to the model, compute the statistics from the retrieved crashes in code (Python, not the model). Then give the model a structured summary alongside the individual crash records.

The model sees something like this instead of 10 raw narratives:

```
Of 10 retrieved crashes at this location:
- 7 occurred on wet or damp road surfaces
- 6 occurred in darkness or low light
- 4 involved pedestrians
- 3 occurred at T or staggered junctions

Individual crashes:
Crash 1 [Serious]: On 14/03/2023, a collision involving...
Crash 2 [Slight]: On 02/11/2022, a collision involving...
...
```

Now the model does not need to count — the counting is already done. Its only job is to write a warning that references the numbers and the crash details. This is a much simpler task.

**Plain English:** Instead of asking someone to "read these 10 reports and figure out what they have in common", you pre-read them yourself, write bullet-point notes ("most crashes happened at night, most involved pedestrians"), and then ask the person to write a warning based on your notes plus the full reports. They will do a much better job.

### What Success Looks Like

**Current output (Variant A — bare prompt):**
> "This location has a high collision rate. Drivers should be aware of pedestrians in urban areas, especially at junctions."

**Target output (pre-aggregation + grounding prompt):**
> "At this location, 7 of 10 historical crashes occurred on wet road surfaces, and 4 involved pedestrians in low light conditions — see Crashes 3, 6, and 8. Reduce speed when visibility is low and watch for pedestrians at the junction ahead."

The target output is specific to this location, references the actual retrieved evidence, and gives actionable advice grounded in what has historically happened there. That is what makes this system novel.

### Implementation

A `summarise_retrieved(indices)` function that reads the metadata for each retrieved crash, tallies key fields (road surface, lighting, junction type, casualty type, severity), and returns a formatted summary block. This runs before `build_prompt()` and its output is injected at the top of the context block.

---

## Part 2 — RAGAS Evaluation

**What:** Formally measure how much the grounding fix improves output quality using an established evaluation framework called RAGAS.

**Timeline:** Week 2

### What RAGAS Is

RAGAS (Retrieval-Augmented Generation Assessment) is a Python library designed specifically to evaluate RAG systems. It produces scores between 0 and 1 for different quality dimensions. No human labelling is required — it uses a language model to check the output automatically.

**Plain English:** RAGAS is like an automated grader for the system's output. Instead of a human reading every warning and deciding if it's good, RAGAS reads the retrieved crashes and the generated warning and scores how well the warning is supported by the evidence. This turns a qualitative observation ("the output seems better") into a quantitative measurement ("faithfulness went from 0.21 to 0.74").

### The Two Metrics We Use

**Faithfulness (0 to 1):** Measures whether every claim in the generated warning is actually supported by the retrieved crash records. A score of 1.0 means every sentence can be traced back to something in the retrieved context. A score near 0 means the model made things up or ignored the context entirely.

**Plain English:** If the warning says "4 crashes involved pedestrians" but the retrieved crashes don't actually show 4 pedestrian crashes, faithfulness catches that. It checks whether the model is telling the truth relative to the evidence it was given.

**Answer Relevance (0 to 1):** Measures whether the output is actually a relevant response to the query. Catches outputs that are technically grounded but off-topic.

### The Experiment

Run RAGAS on three conditions, each on 50 test queries:

| Condition | Description |
|-----------|-------------|
| **A — Bare (current system)** | No grounding instruction |
| **B — Force-cite** | Prompt that forces crash citations by number |
| **B + Pre-aggregation** | Force-cite prompt with pre-computed statistics injected |

The comparison table (faithfulness scores across conditions) is the quantitative result of the thesis. If faithfulness increases from condition A to condition B+agg, that is the empirical finding.

**Why this matters for the thesis:** Without RAGAS, the improvement is just a demonstration — "look, the output mentions specific crashes now." With RAGAS, it is a measured result: "grounded prompting increased faithfulness from X to Y across 50 test queries." That is the difference between a project and a finding.

### Practical Setup

```bash
pip install ragas
```

For each test query, RAGAS needs three things: the query text, the list of retrieved crash narratives, and the generated warning. No ground truth labels needed. Approximately 15 lines of Python per evaluation run.

---

## Part 3 — Three-Index Retrieval Ablation

**What:** Build two additional retrieval strategies and compare all three against each other to find which one surfaces the most relevant historical crashes.

**Timeline:** Weeks 3–4

### Why Retrieval Strategy Matters

The current system retrieves crashes by converting the query narrative into a dense vector (a list of numbers that captures the meaning of the text) and finding the 10 stored crashes whose vectors are closest. This is called **semantic retrieval** — it finds crashes that describe a similar situation in similar language.

But "similar language" is not the same as "similar conditions." A crash described in different words might share the same road type, speed limit, weather, and light conditions as the query crash — making it highly relevant — but score poorly on semantic similarity because the phrasing is different.

**Plain English:** Imagine two accident reports describing the same type of crash — one says "the vehicle skidded on a wet A-road at night" and the other says "the car lost control on a damp dual carriageway in darkness." A semantic search might not rank these as similar because the words are different. But if you compared their structured data fields (road surface: wet, road type: A-road, lighting: dark), they'd be identical. The ablation tests whether searching by structured fields finds better matches than searching by text meaning.

### The Three Retrieval Strategies

**Index 1 — Dense Semantic (current):**
Each crash narrative is converted into a 384-dimensional vector by a sentence encoder model (all-MiniLM-L6-v2). The FAISS index stores these vectors. At query time, the query narrative is encoded the same way and the 10 nearest vectors are retrieved.

**Plain English:** Each crash is turned into a point in a very high-dimensional space. Crashes that describe similar situations end up near each other. The query crash is placed in the same space, and the 10 nearest neighbours are returned.

**Index 2 — Feature-Based FAISS:**
Each crash is represented as a structured feature vector built from its tabular fields: speed limit, road type, light conditions, weather, junction type, urban/rural classification, day of week, hour of day. Categorical fields are one-hot encoded (converted to binary columns). A second FAISS index is built on these feature vectors.

At query time, the query crash's feature vector is used instead of its narrative embedding. Retrieval finds crashes that share the same road conditions, timing, and environment — not just similar text.

**Plain English:** Instead of describing each crash in words and comparing descriptions, we describe each crash as a set of tick-boxes (was it raining? yes/no; was it on a motorway? yes/no; was it at night? yes/no). We then find the 10 crashes with the most matching tick-boxes. This finds crashes that happened in the same conditions, regardless of how they were written up.

**Index 3 — BM25 Keyword:**
BM25 is a classic keyword-based search algorithm (the same family as what search engines used before neural methods). It finds crashes that share specific words with the query narrative — "roundabout", "pedestrian", "fog", "rear-end" — without any neural encoding. Acts as a non-neural baseline to show how much the neural approaches add.

**Plain English:** This is the equivalent of Ctrl+F across all crash reports — find the ones that use the same words as the query. It's the simplest possible retrieval method and serves as the floor to compare against.

### What We Measure

For each retrieval strategy, across 100 test queries, compute **feature overlap** between the query crash and each of the 10 retrieved crashes on 5 key fields:

- Speed limit (exact match)
- Road type (exact match)
- Light conditions (exact match)
- Weather (exact match)
- Severity distribution of retrieved set

This gives a retrieval quality score for each strategy with no human labels needed.

**Plain English:** For each strategy, we check: when the query crash happened on a wet road at night with a 30mph speed limit, did the retrieved crashes also mostly happen on wet roads at night with 30mph limits? The more matches, the better the retrieval.

### The Finding We're After

If feature-based retrieval surfaces more condition-similar crashes than semantic retrieval, that is a concrete, novel finding. It means the current system is retrieving crashes that *sound* similar but do not actually share the same risk conditions — and that a better retrieval strategy exists.

This finding directly motivates future work (joint embedding — training a retrieval model that captures both narrative and feature similarity) without requiring you to implement it now.

**Why this is novel:** No existing crash risk paper has done a controlled comparison of retrieval strategies. Tab-Text and CrashSage do not use retrieval at all. This experiment has not been run before on this type of data.

---

## Full Timeline

| Week | Work |
|------|------|
| 1 | Write `summarise_retrieved()` function; test pre-aggregation prompt; compare Variant A vs B vs B+agg on 10 queries |
| 2 | RAGAS evaluation — 50 queries, faithfulness table across all three conditions |
| 3 | Build feature-based FAISS index from tabular fields |
| 4 | Build BM25 index; run ablation comparison across 100 queries; compute feature overlap table |
| 5 | Write results section — faithfulness table + ablation table |
| 6 | Conclusion, limitations, future work write-up |

---

## What the Thesis Contribution Looks Like at the End

**System contribution:** A RAG pipeline that produces grounded, evidence-citing, location-specific crash warnings — the first of its kind in the crash risk literature.

**Evaluation contribution:** Formal faithfulness measurement (RAGAS) demonstrating that structured grounding prompting increases output faithfulness from X to Y across 50 test queries.

**Research contribution:** The first controlled comparison of retrieval strategies for location-based crash risk RAG — semantic vs. feature-based vs. keyword — with a concrete recommendation on which retrieves more condition-relevant historical evidence.

Tab-Text and CrashSage have none of these three things. That is the thesis gap this system fills.

---

## Architectural Addition — Hybrid Re-Ranker

**What:** A re-ranking step inserted between FAISS retrieval and the LLM, so the model receives the most condition-relevant crashes rather than just the most narratively similar ones.

**Where it sits in the pipeline:**

```
Query narrative + GPS
        ↓
Spatial filter (haversine, 1km)
        ↓
FAISS semantic retrieval → top-20 candidates
        ↓
Hybrid re-ranker (semantic score + feature overlap)
        ↓
Top-10 re-ranked crashes
        ↓
Pre-aggregation (compute statistics across top-10)
        ↓
Grounded prompt → Fine-tuned Gemma → Warning
```

**Plain English:** Right now FAISS retrieves the 10 crashes that are described in the most similar language to the query. But similar language doesn't always mean similar conditions — two crashes can sound very different and still have happened in the same road type, weather, and lighting. The re-ranker looks at both language similarity and condition similarity and combines them into a single score, then picks the best 10 from a larger candidate pool of 20. This ensures the LLM is working with crashes that are relevant in both ways.

### The Method — Hybrid Retrieval with Late Fusion

This is a standard technique in the RAG literature called **hybrid retrieval with late fusion**. It combines two retrieval signals after each has scored the candidates independently:

**Signal 1 — Semantic similarity:** The FAISS distance score, converted to a similarity (closer = higher score). Captures narrative and situational similarity from the text.

**Signal 2 — Feature overlap:** The proportion of key tabular fields that match between the query crash and each candidate (road surface, lighting, road type, speed limit, urban/rural). Captures condition similarity from the structured data.

The combined score:

```
hybrid_score = α × semantic_similarity + (1 − α) × feature_overlap
```

Where α is a tunable weight. α=1 reduces to semantic-only (the current system). α=0 reduces to feature-only. α=0.5 is the hybrid baseline.

**Plain English:** Each candidate crash gets two scores — one for how similar it sounds to the query, one for how similar its conditions are. The re-ranker multiplies each by a weight and adds them together. The top-10 by combined score go to the LLM.

### Why This Is Grounded in the Literature

This is not invented complexity. The two-stage retrieve-then-rerank pipeline is established as the standard pattern (Nogueira & Cho, 2019). Combining dense and sparse/structured signals is used in production RAG systems and documented in the original RAG paper (Lewis et al., 2020). The specific substitution — using structured feature overlap instead of BM25 as the second signal — is the novel contribution here, motivated by the domain: for crash risk, shared conditions are more semantically meaningful than shared keywords.

**Thesis framing:**

> *"We adopt a two-stage retrieval pipeline: an initial candidate set is retrieved via dense semantic search (FAISS), which is then re-ranked using a hybrid score combining semantic similarity with structured feature overlap — a standard approach in the retrieval augmentation literature (Lewis et al., 2020; Nogueira & Cho, 2019). This design is motivated by the observation that narrative similarity and condition similarity are complementary signals in crash risk retrieval."*

### Connection to the Ablation Study

The three-index ablation now becomes a re-ranker ablation. Instead of comparing three separate indexes, you compare three re-ranking configurations:

| Configuration | α | Description |
|--------------|---|-------------|
| Semantic-only | 1.0 | Current system (no re-ranking) |
| Feature-only | 0.0 | Condition similarity only |
| Hybrid | 0.5 | Equal weight to both signals |

RAGAS faithfulness is measured for each. The configuration with the highest faithfulness is the recommended retrieval strategy.

### Implementation

Two additions to the existing pipeline:

1. A `compute_feature_overlap(query_meta, candidate_meta)` function that compares 5 fields and returns a score from 0 to 1.
2. A `rerank(candidates, query_vec, query_meta, alpha)` function that scores each candidate on both signals and returns the top-10 by hybrid score.

The rest of the pipeline (pre-aggregation, prompt, generation) is unchanged.

---

## Links

- [[concepts/system-architecture]]
- [[concepts/rag-narrative-generation]]
- [[progress/2026-05-26]]
- [[progress/presentation-2026-06-02]]
- [[entities/stats19]]
