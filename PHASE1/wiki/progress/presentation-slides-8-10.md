---
title: "Presentation Slides 8–10 Draft"
type: progress
date: "2026-05-31"
tags: [progress, presentation]
---

# Presentation Slides 8–10 Draft

---

## Slide 8 — Experimental Setup & Results

**Part 1: Fine-Tuning**
- Model: Gemma-3-4b-it, QLoRA (r=16), trained on STATS19 narratives
- Task: 3-class severity classification (Slight / Serious / Fatal)
- Training set downsampled to handle class imbalance
- Evaluation on held-out query set (25,174 records)

| System | Macro F1 | Slight F1 | Serious F1 | Fatal F1 |
|---|---|---|---|---|
| Zero-shot Gemma (no fine-tuning) | 0.149 | — | — | 0.000 |
| XGBoost (tabular baseline) | 0.350 | — | — | — |
| Fine-tuned Gemma-3-4b-it | 0.408 | 0.693 | 0.364 | 0.134 |

Zero-shot never predicts Fatal — without domain adaptation the model defaults to majority class. Fine-tuning is what unlocks minority class prediction.

**Part 2: RAG System Demo**
- Input: test crash narrative + GPS coordinates (simulating a live driver query)
- Spatial filter → X crashes within 1km
- Semantic search → top 10 retrieved
- Fine-tuned Gemma generates a location-specific warning
- Show: example query narrative → example output text (screenshot or text block on slide)

**Known limitation — state this explicitly:**
The current RAG output is generic — warnings like "drive carefully in wet conditions" that do not reference the retrieved crashes or the specific location. Diagnosis: the model is not being forced to ground its output in the retrieved context. This is a prompt engineering problem, not an architectural failure. Fix is the immediate next step.

**Diagrams to include:**
- SHAP feature importance bar chart — `xgb_shap_bar.png`, shows which variables matter most (speed limit, road type, light conditions) — motivates feature-based retrieval in future work
- UK crash location map — lat/lon from collision.csv, shows geographic spread — justifies spatial retrieval as a signal
- Class distribution bar chart — Slight / Serious / Fatal counts — makes imbalance visually obvious, motivates downsampling decision

---

## Slide 9 — Future Work

### End Goal (state this at the top of the slide)
Demonstrate that a RAG system grounded in historical crash data produces measurably more location-specific and faithful warnings than an ungrounded baseline — evaluated on both retrieval quality and generation quality metrics.

---

### Immediate: Fix Generic Output

**Problem:** Model generates warnings not grounded in retrieved context.

**Fix 1 — Prompt restructuring:** Force the model to explicitly reference retrieved statistics. Instead of free generation, compute statistics from the retrieved set before prompting:
- "X of the 10 retrieved crashes involved wet road surfaces"
- "Y of 10 occurred in darkness without street lighting"
- "Junction failure to give way appears in Z of 10 cases"

Inject these pre-computed statistics into the prompt. Model becomes a narrator of evidence, not a free generator.

**Fix 2 — Structured extraction as fallback:** If generation remains generic, switch to extracting factor frequencies from retrieved crashes and templating them directly into the warning. Removes generation unpredictability at the cost of some fluency.

---

### Three-Index Ablation (core retrieval research question)

Current system uses only two retrieval signals: spatial (lat/long) and dense semantic (sentence transformer). The third index — feature-based — is missing.

**Feature-based index:** FAISS index built on XGBoost's top features (speed limit, light conditions, road type, junction control, weather conditions, urban/rural). Retrieves crashes with matching road conditions regardless of location. Useful when local crash history is sparse but nationally similar conditions are abundant.

**Ablation study — 6 system variants:**

| Variant | What it tests |
|---|---|
| Spatial only | Does location alone give useful retrieval? |
| Feature only | Do explicit conditions alone work without location? |
| Dense only | Does learned semantic similarity outperform explicit matching? |
| Spatial + feature | Does combining location and conditions outperform either? |
| Spatial + dense | Current system — does semantic re-rank improve over spatial alone? |
| Spatial + feature + dense | Does the full three-signal combination win? |

Each row produces a retrievl quality score and a generation quality score. This is the thesis's core experimental finding.

---

### Evaluation Framework

**Retrieval quality — three proxy metrics (no ground truth labels needed):**

1. **Feature overlap rate:** For a query crash, check how often the top-K retrieved crashes share values on key STATS19 fields (road type, light conditions, weather) vs. a random sample from the corpus. Higher overlap = better retrieval.

2. **Severity distribution shift:** Does the retrieved set show a different severity distribution than the corpus-wide baseline? If a location has disproportionate Fatal crashes, good retrieval should surface that signal rather than returning the corpus average.

3. **Held-out probe:** Treat each test crash as a live query. Retrieve from the train+val corpus. Feed retrieved crashes as context to the LLM and ask it to predict severity. Compare F1 against the no-retrieval fine-tuned baseline (0.408). If retrieval improves classification, retrieval is adding information — this is the cleanest proxy for retrieval quality.

**Generation quality — RAGAS framework:**

RAGAS evaluates four dimensions using an LLM-as-judge internally (no human labels required):

| Metric | What it measures | Why it matters |
|---|---|---|
| **Faithfulness** | Does the warning only make claims supported by the retrieved crashes? | Directly diagnoses generic output — a warning that ignores retrieved context scores near zero |
| **Answer relevance** | Is the warning relevant to the query location and conditions? | Catches off-topic or boilerplate output |
| **Context precision** | What fraction of the retrieved crashes were actually used? | Identifies whether K=10 is too many — unused context wastes the prompt window |
| **Context recall** | Did the retrieved crashes cover the key risk factors present in the query? | Measures whether retrieval missed important signals |

Faithfulness is the primary metric. A system that produces specific, location-grounded warnings will score high. A system generating generic advice will score low even if the advice is technically true.

---

### Hyperparameter Tuning

| Parameter | Candidates | What changes |
|---|---|---|
| Radius R | 500m, 1km, 2km | How local the retrieval pool is — smaller R means fewer retrieved crashes, higher precision |
| K (retrieved crashes) | 5, 10, 20 | Context richness vs. prompt window usage |
| Sentence transformer | all-MiniLM-L6-v2, all-mpnet-base-v2 | Encoding quality vs. speed |

Tune R and K after fixing generic output — no point tuning retrieval if generation ignores it.

---

### Longer Term (out of scope for this implementation phase)

**Joint embedding** — encode location + narrative into a single vector space so geographic and semantic similarity are captured simultaneously rather than sequentially. Requires custom embedding model training (contrastive learning on crash similarity pairs), custom FAISS index rebuild, and a training data pipeline. This is a research contribution in itself — flagged as future work, not planned for this phase.

**Summarisation fine-tuning** — if RAGAS faithfulness scores remain low after prompt engineering, fine-tune the Gemma adapter further on (retrieved context → grounded summary) pairs. Contingency only.

**DBSCAN spatial hotspot analysis** — cluster crashes by lat/long to identify hotspots. Cross-reference with retrieval signal: do locations with DBSCAN-identified clusters produce higher-quality retrievals?

**Live API integration** — replace simulated query narrative with real GPS (device location) + OpenWeatherMap API for current conditions → auto-generated query narrative.

---

## Slide 10 — Summary

- **Problem:** Drivers lack location-specific, evidence-based crash risk warnings — generic road safety advice ignores that risk is highly localised
- **Gap:** Prior work stops at severity labels (Tab-Text, CrashSage) or explains autonomous vehicles (RAG-Driver, RAG-SafeAdapt) — no system uses RAG over historical crash data for human drivers
- **Built:** End-to-end pipeline — tabular-to-text conversion → fine-tuned Gemma (QLoRA) → FAISS spatial + semantic retrieval → location-specific warning
- **Found:** Fine-tuned Gemma (F1 0.408) outperforms XGBoost (0.350) and zero-shot (0.149); RAG pipeline is end-to-end working; current limitation is generic output (not grounded in retrieved context)
- **Next 6 weeks:** Fix generic output → build feature-based index → run three-index ablation → evaluate with RAGAS faithfulness + retrieval quality proxies → lock final results

---

## Open Questions (to resolve before finalising)

1. For the RAG demo on the experimental slide — show an actual example output from query.py, or keep it generic? Recommended: show the real output and name the generic problem explicitly — more credible than hiding it.
2. Are you generating the crash location map and class distribution chart?

---

## Links

- [[progress/presentation-2026-06-02]] — slides 1–7
