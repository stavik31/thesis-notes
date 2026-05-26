---
title: "RAG Plan — Phase 2"
type: progress
date: "2026-05-21"
tags: [progress, method, thesis-core, rag]
---

# RAG Plan — Phase 2: Location-Based Crash Risk Advisor

**Goal:** Build a RAG pipeline that takes a driver's GPS coordinates, retrieves historically similar crashes from STATS19, and uses the fine-tuned Gemma adapter to generate a human-readable driver warning grounded in retrieved evidence.

**Backbone:** `google/gemma-3-4b-it` + LoRA adapter (`checkpoint-3500`)
**Corpus:** `narratives_raw.jsonl` — 503,475 crash narratives, each with `collision_index`, `narrative`, `label`
**Hardware:** RTX 5080 (16GB VRAM)

---

## The Vector Space Problem

RAG retrieval needs to find crashes that are similar in two ways simultaneously:
- **Geographically close** — happened near the driver's current location
- **Semantically similar** — same road conditions, junction type, lighting, etc.

Three approaches exist, in order of complexity:

| Approach | How | Difficulty |
|---|---|---|
| Separate indices, combine after | Build spatial + semantic FAISS independently, merge and re-rank | Low |
| Filter then retrieve | Spatial filter first (radius R), semantic retrieval within subset | Low-Medium |
| Joint embedding | Encode location + narrative into single vector | High — likely out of scope |

**Selected approach: Filter then retrieve (Option 2).** Spatial filter constrains the candidate pool to crashes within radius R of the driver. Semantic retrieval then ranks within that subset by narrative similarity. Clean, interpretable, defensible for a thesis.

---

## What to Learn Before Building

1. **FAISS** — how it builds an index, how ANN (approximate nearest neighbour) search works
2. **Sentence transformers** — encode narratives into dense vectors (same idea as BERT encoder, already understood)
3. **Combining retrieval signals** — spatial filter + semantic re-rank

All three are one-session topics. None require new training.

---

## Architecture

```
OFFLINE (build once)
─────────────────────────────────────────────────────
narratives_raw.jsonl
    │
    ▼
[1] Encode narratives → sentence transformer → dense vectors
    Model: all-MiniLM-L6-v2 (fast, 384-dim, good quality)
    Output: matrix of shape (503475, 384)
    │
    ▼
[2] Build FAISS index
    Index type: IndexFlatL2 (exact search, simple start)
    Store: vectors + collision_index + lat/long + label as metadata
    Save index to disk


ONLINE (per driver query)
─────────────────────────────────────────────────────
Driver GPS (lat, long) + optional current conditions
    │
    ▼
[3] Spatial filter
    Compute haversine distance from driver to all crash lat/longs
    Keep only crashes within radius R (e.g. 500m, 1km, 2km — tune this)
    │
    ▼
[4] Semantic retrieval
    Encode query (current conditions as text) → dense vector
    FAISS search within spatially filtered subset
    Return top K crashes (e.g. K=10)
    │
    ▼
[5] Prompt construction
    System: road safety expert context
    Context: K retrieved crash narratives
    Query: current conditions + "what should the driver watch out for?"
    │
    ▼
[6] Fine-tuned Gemma generates warning
    Grounded in retrieved evidence — model narrates what records say
    Output: 2-4 sentence driver warning
```

---

## Step-by-Step Build Order

### Step 1 — Install dependencies
```bash
pip install faiss-cpu sentence-transformers
```
Use `faiss-cpu` unless GPU memory allows `faiss-gpu`. CPU is fine for 503k vectors at 384 dims.

### Step 2 — Encode narratives
Script: `llm/build_index.py`
- Load `narratives_raw.jsonl`
- Encode all narratives with `all-MiniLM-L6-v2`
- Save vectors as `.npy` + metadata as `.jsonl`

### Step 3 — Build FAISS index
- `IndexFlatL2` for exact search (simplest, sufficient for 503k)
- If too slow at query time: upgrade to `IndexIVFFlat` (approximate, faster)
- Save index to `faiss_index.bin`

### Step 4 — Spatial filter
Script: `llm/query.py`
- Load crash metadata (lat/long per collision_index)
- Haversine distance from query point to all crashes
- Return indices within radius R

### Step 5 — Semantic retrieval within spatial subset
- Encode query text → vector
- FAISS search restricted to spatial subset indices
- Return top K

### Step 6 — Prompt construction + generation
- Build prompt with retrieved narratives as context
- Load fine-tuned adapter (`lora_adapter/`)
- Generate warning with `max_new_tokens=150`

---

## Hyperparameters to Tune

| Parameter | Candidates | What it controls |
|---|---|---|
| Radius R | 500m, 1km, 2km | How local the retrieval is |
| K (retrieved crashes) | 5, 10, 20 | Context richness vs. prompt length |
| Sentence transformer | all-MiniLM-L6-v2, all-mpnet-base-v2 | Encoding quality |

Start with R=1km, K=10. Adjust based on retrieval quality.

---

## Evaluation Plan

| What | How |
|---|---|
| Retrieval quality | Are retrieved crashes geographically and semantically relevant? Manual spot-check + severity distribution of retrieved set vs. local STATS19 baseline |
| Factor accuracy | Do surfaced factors match overrepresented STATS19 patterns at that location? |
| Warning usefulness | Human rubric: is the advice actionable, specific, grounded? |
| Baseline comparison | XGBoost → severity label only vs. Gemma + RAG → narrative warning |

---

## Watch Out For

- **Context window** — 10 full crash narratives may exceed 1024 tokens. May need to truncate or summarise retrieved narratives before stuffing into prompt.
- **Cold start** — locations with fewer than K crashes in STATS19 need a fallback (e.g. widen radius, reduce K, flag to user).
- **Hallucination** — prompt must instruct the model to only reference retrieved crashes, not invent statistics.
- **Spatial data quality** — STATS19 lat/long has some noise. Crashes at junctions may be snapped to a fixed point — cluster of records at identical coordinates is expected, not a bug.

---

## Links

- [[concepts/system-architecture]] — full architecture this plan implements
- [[concepts/llm-domain-adaptation]] — fine-tuned adapter rationale
- [[concepts/tabular-to-text-transformation]] — how narratives were built
- [[progress/2026-05-21]] — Phase 1 results that justify this approach
- [[progress/llm-finetune-plan]] — fine-tuning plan; adapter is the output
- [[entities/stats19]] — source dataset
