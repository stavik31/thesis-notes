---
title: "RAG-Based Crash Risk Narrative Generation"
type: concept
tags: [thesis-core, method, llm, rag]
sources: []
last_updated: "2026-04-30"
---

# RAG-Based Crash Risk Narrative Generation

## Overview

The central thesis system. Given a crash scenario or road location described by structured features, the system retrieves similar historical crashes from STATS19 and passes them — along with the current scenario's features — to a local LLM, which generates a human-readable risk narrative for drivers or road safety practitioners.

The output is not a label. It is prose:

> *"This T-junction on the A38 in wet conditions at night has been associated with 7 serious collisions in the past 3 years. Common contributing factors include excessive speed on approach and reduced visibility from the adjacent tree line. Drivers should reduce speed and increase following distance."*

This is a **generation-first** framing. The LLM is a narrator grounded in retrieved evidence, not a classifier trained to predict a label.

---

## How It Differs From Prior Work

| System | LLM role | Output | Evidence source |
|--------|----------|--------|-----------------|
| CrashSage | Fine-tuned classifier | Severity label | Weights (baked in during SFT) |
| Tab-Text | Encoder backbone | Severity label | Tabular + narrative embeddings |
| **This thesis** | **Grounded narrator** | **Risk narrative** | **Retrieved historical crashes (RAG)** |

Neither CrashSage nor Tab-Text produces output usable by a driver or road safety officer. Both stop at a label or an attribution score. This system produces an explanation.

---

## Pipeline

```
Query crash (structured features + lat/long)
    └─► Feature selection (top-correlated variables from correlation analysis)
        └─► Retrieval index (STATS19 historical crashes)
            ├─► Feature-based similarity (Cramér's V top features)
            └─► Spatial proximity (within radius — geo-aware retrieval)
                └─► Top-K retrieved crashes
                    └─► LLM prompt construction
                        [system: road safety expert]
                        [retrieved cases: crash 1, crash 2, ..., crash K]
                        [query: current scenario features]
                        └─► Generated narrative (local LLM)
```

**Retrieval index:** FAISS or similar ANN index over STATS19 records, encoded using top-correlated features (from [[concepts/crash-severity-inference]] correlation analysis) plus spatial coordinates.

**Local LLM:** A frozen or lightly adapted decoder model (LLaMA3-8B is the candidate). Frozen is preferred to keep retrieval as the knowledge source rather than baked weights — this is the key architectural commitment.

---

## Key Design Decisions

**1 — Frozen vs. fine-tuned LLM**
Keeping the LLM frozen means all domain knowledge comes through retrieval. This is more interpretable (you can audit what was retrieved) and cheaper to update (re-index STATS19 without retraining). Fine-tuning the generation model is an ablation to consider, not the baseline design.

**2 — What goes in the retrieval query**
The correlation analysis (see [[concepts/crash-severity-inference]]) determines which features to use. Using low-signal features inflates the index dimensionality without improving retrieval relevance. Spatial proximity is a second retrieval dimension — whether it improves over feature-only retrieval is an empirical question.

**3 — Narrative grounding / hallucination risk**
The LLM must be prompted to cite retrieved cases rather than hallucinate statistics. Prompt design should instruct the model to attribute claims to specific retrieved records and avoid inventing figures not present in the context.

**4 — Narrative template for retrieved cases**
Retrieved cases need to be formatted as readable context, not raw structured data. The [[concepts/tabular-to-text-transformation]] templates already designed for STATS19 serve double duty here — they format both query inputs and retrieved context blocks.

---

## Evaluation

Standard severity prediction metrics (macro F1, accuracy) apply to the final classification implied by the narrative. But narrative quality needs additional measures:

- **Retrieval quality:** Precision@K — what fraction of retrieved cases share the same severity class as the query?
- **Factual grounding:** Does the narrative contain only facts present in the retrieved context? (Manual or LLM-assisted audit)
- **Usefulness:** Does the narrative surface actionable factors? (Human evaluation rubric — could be a small user study with road safety framing)

Comparison baselines: CatBoost (tabular), zero-shot LLaMA3-8B (no retrieval), fine-tuned CrashSage (SFT baseline).

---

## Debates / Open Questions

- Does spatial proximity actually improve retrieval relevance, or does feature-based similarity already capture location implicitly (via road type, junction type, urban/rural)?
- What is K? Too few retrieved cases and the narrative lacks evidence; too many and the context window fills before the LLM can synthesise.
- Should retrieved cases be ranked by similarity score and the narrative instructed to weight them accordingly, or treated as a flat set?
- Is a frozen LLM sufficient for fluent, coherent narrative generation, or does the generation quality require at least light instruction-tuning on crash narrative examples?

---

## Related Concepts

- [[concepts/crash-severity-inference]] — the prediction task; correlation analysis feeds feature selection for retrieval
- [[concepts/tabular-to-text-transformation]] — narrative templates used for both query construction and retrieved case formatting
- [[concepts/llm-domain-adaptation]] — the fine-tuning alternative; CrashSage-style SFT is the comparison baseline
- [[concepts/multimodal-crash-modeling]] — Tab-Text's embedding-fusion approach; another comparison point

## Sources

*(No papers directly address RAG for crash risk narrative generation — this is the gap the thesis fills. Adjacent literature on RAG for QA and LLM grounding to be ingested.)*
