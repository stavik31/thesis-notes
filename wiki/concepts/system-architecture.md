---
title: "System Architecture — Location-Based Crash Risk Advisor"
type: concept
tags: [thesis-core, method, architecture, rag, llm]
sources: ["[[sources/crashsage]]", "[[sources/tab-text]]"]
last_updated: "2026-05-21"
---

# System Architecture — Location-Based Crash Risk Advisor

## The Problem

Drivers have no access to location-specific crash history in a form they can act on. Generic road safety advice ("drive carefully in wet conditions") ignores the fact that risk is highly localised — a specific junction may be disproportionately dangerous at night, or a particular stretch of road may have an unusual rate of side-impact collisions from vehicles failing to give way.

The system answers one question for any road location:

> *"Based on everything that has happened at this spot historically, what should a driver specifically watch out for right now?"*

This is not severity prediction. It is **location-specific factor surfacing with advisory output**.

---

## Why Narratives Over Structured Features

The correlation analysis of STATS19 (Cramér's V, Spearman) showed effect sizes below 0.2 for every individual feature against casualty severity. This is the empirical case for moving beyond structured fields:

- No single feature tells you enough on its own
- Risk emerges from combinations: wet road + night + bend + T-junction is dangerous in a way none of those fields captures individually
- Both Tab-Text and CrashSage demonstrate empirically that converting structured crash records into narrative text allows an LLM to pick up on these factor interactions that structured models miss

**The revised analysis** (to be rerun) will use Mutual Information instead of Cramér's V — MI handles high-cardinality categorical variables correctly and does not deflate on sparse contingency tables. A full pairwise MI matrix across top features will also be computed to identify redundant features before building the retrieval index.

---

## Architecture Overview

The system has two phases: an offline build phase (done once) and an online inference phase (per driver query).

```
OFFLINE
─────────────────────────────────────────────────────────────
STATS19 (collision + vehicle + casualty tables)
    │
    ▼
[1] Tabular-to-text conversion
    Convert each crash record into a natural language narrative
    using STATS19-specific templates (scene, road conditions,
    vehicles involved, casualties). One narrative per crash.
    │
    ▼
[2] LLM fine-tuning (LoRA on LLaMA3-8B, RTX 5090)
    Fine-tune on crash narratives + severity labels.
    Goal: the model learns crash-domain language — what factor
    combinations mean, how conditions interact, what outcomes
    follow from what contexts. This is domain adaptation, not
    a deployed classifier.
    │
    ▼
[3] Spatial retrieval index (FAISS)
    Index all crash narratives by lat/long coordinates.
    Each entry: crash narrative text + metadata (severity,
    date, top contributing factors).


ONLINE (per driver query)
─────────────────────────────────────────────────────────────
Driver GPS coordinates
    │
    ▼
[4] Spatial retrieval
    Query FAISS index for K nearest crashes within radius R.
    Retrieved crashes are already in narrative form.
    │
    ▼
[5] Prompt construction
    System prompt: road safety expert context
    Retrieved context: K crash narratives from this location
    Query: current conditions (time of day, weather if available)
    │
    ▼
[6] Fine-tuned LLM generates warning
    "At this location, most historical crashes involved vehicles
    failing to give way at the junction in low-light conditions.
    Approach slowly and check for traffic from the right."
    │
    ▼
Driver receives location-specific advisory
```

---

## Component Details

### [1] Tabular-to-text conversion
Already designed — see [[concepts/tabular-to-text-transformation]]. Templates cover four narrative blocks: scene (location, time, conditions), road and environment, vehicles involved, casualties. Raw STATS19 codes are decoded to readable descriptions before conversion. Label leakage fields are excluded.

### [2] LLM fine-tuning
LoRA fine-tuning on LLaMA3-8B. Training signal: crash narrative → severity label (same as CrashSage replication). The fine-tuning is not the deployed classifier — it is domain adaptation. The model learns what crash narratives mean so that at inference time it can synthesise retrieved local crash narratives into coherent, grounded advice rather than generic output.

This is the key difference from a frozen base model: a frozen LLaMA3-8B knows English but does not know that "vehicle failing to give way (code 2)" at a "T-junction (code 3)" in "darkness: no lighting (code 7)" is a high-risk pattern. Fine-tuning injects that domain knowledge.

### [3] Retrieval indices (three variants, all built from the same narrative corpus)

**Spatial index** — FAISS index on lat/long coordinates. Retrieves crashes within a radius R of the driver's location. Simple and interpretable: every retrieved crash can be explained ("this happened 200m from here").

**Feature-based index** — FAISS index on the top XGBoost features (speed_limit, light_conditions, road_type, junction_control, urban_or_rural_area, weather_conditions). Retrieves crashes with matching road conditions regardless of location. Useful when a relevant crash happened slightly further away but in identical conditions.

**Dense vector index** — each crash narrative is encoded into a vector using a sentence transformer model (e.g. `all-MiniLM-L6-v2`). FAISS retrieves the K nearest vectors to the encoded query scenario. The model learns what "similar crashes" means from the narratives themselves — capturing subtle combinations of factors that explicit feature matching misses. A crash 2km away in semantically identical conditions may rank higher than one 50m away in unrelated conditions. Computationally heavier (embed 503k narratives once, store vectors) but runs fast at inference.

All three indices are built once offline. At inference, each can be queried independently or combined (e.g. spatial filter → re-rank by dense similarity).

### [4–6] Online inference
Retrieval radius R and number of retrieved cases K are hyperparameters to tune. Too small an R and there are not enough local crashes to synthesise from. Too large and the crashes are no longer local. K affects context window usage and narrative coherence.

The LLM prompt instructs the model to attribute every claim to retrieved cases and not invent statistics. Hallucination risk is managed by keeping the generation grounded: the model is a narrator of what the retrieved records say, not a free generator.

---

## What the System Does Not Do

- It does not predict whether a crash will happen (no probability output)
- It does not classify severity for a hypothetical crash
- It does not generate advice for locations with no crash history in STATS19 (cold-start problem — flag to user)

---

## Evaluation

| What to evaluate | How |
|---|---|
| Retrieval quality | Are retrieved crashes actually from this location? Precision@K on spatial proximity. |
| Factor accuracy | Are the surfaced factors overrepresented at this location vs. national STATS19 baseline? |
| Warning usefulness | Human evaluation rubric: is the advice actionable and location-specific? |
| Temporal holdout | Train on crashes up to date X, evaluate warnings against crashes that occur after X at the same locations. |
| Baseline comparison | CatBoost (tabular severity), zero-shot LLaMA3-8B (no retrieval, no fine-tuning), CrashSage (SFT classifier). |

The temporal holdout is the most important evaluation — it tests whether the system surfaces factors that predict future crash patterns at a location, not just describes the past.

### Ablation Study

The thesis findings come from comparing these system variants:

| System variant | What it tests |
|---|---|
| Spatial only | Does location alone give useful retrieval? |
| Feature only | Do explicit conditions alone work without location? |
| Spatial + feature | Does combining both outperform either? |
| Dense vector only | Does learned semantic similarity outperform explicit feature matching? |
| Spatial + dense vector | Does adding location constraint to semantic retrieval improve results? |
| Zero-shot LLM (no retrieval) | Does retrieval even help at all? |
| Fine-tuned LLM + RAG (best retrieval) | Does domain adaptation improve generation quality? |

Each row is a standalone comparison. The middle block (spatial vs. feature vs. dense vs. hybrid) is the core retrieval research question. The bottom two rows evaluate the generation side.

---

## Build Order

1. ~~**Rerun data analysis**~~ — done (XGBoost SHAP confirmed top features)
2. ~~**Tabular-to-text conversion**~~ — done (503k narratives in `narratives_raw.jsonl`)
3. ~~**Fine-tune LLM**~~ — done (`gemma-3-4b-it`, QLoRA r=16, checkpoint-3500, Macro F1 0.408)
4. ~~**Baselines**~~ — done (zero-shot 0.149, XGBoost 0.350, fine-tuned 0.408)
5. **Build FAISS index** — index narrative corpus by lat/long ← current
6. **Build inference pipeline** — spatial query → prompt construction → generation
7. **Evaluation** — retrieval quality, factor accuracy, warning usefulness, XGBoost comparison

---

## Related

- [[concepts/rag-narrative-generation]] — earlier framing, now superseded by this page
- [[concepts/tabular-to-text-transformation]] — narrative templates (step 1)
- [[concepts/llm-domain-adaptation]] — fine-tuning rationale (step 2)
- [[concepts/crash-severity-inference]] — correlation analysis feeding feature selection
- [[entities/stats19]] — primary dataset
- [[entities/llama3-8b]] — LLM backbone
