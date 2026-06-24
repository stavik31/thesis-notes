---
title: "Multimodal Crash Modeling"
type: concept
tags: [method, thesis-core, nlp, multimodal]
sources: ["[[sources/tab-text]]"]
last_updated: "2026-04-08"
---

## Overview

Multimodal crash modeling refers to architectures that jointly process multiple data modalities — typically structured tabular features (categorical, numerical) alongside unstructured text (constructed narratives) — in a single end-to-end model. [[sources/tab-text]] introduces this paradigm for traffic safety.

The key insight: neither modality alone is sufficient. Text-only models (T2T-Transformer) outperform tabular-only models (CatBoost) marginally, but combining both (Tab-Text) provides a meaningful boost — especially on rare, high-severity cases.

## Tab-Text Architecture

Three parallel processing branches fused at a final layer:

```
Textual Narrative  →  ELECTRA encoder → [CLS] embedding (768-dim)
Categorical data   →  Factorized embed + MLP             (768-dim)
Numerical data     →  Min-max norm + MLP                 (768-dim)
                        ↓
                   Concatenation (2304-dim)
                        ↓
                   2 Dense Layers → Severity Prediction
```

Each branch is fine-tuned jointly. The textual head fine-tunes the pretrained ELECTRA weights; the tabular heads learn from scratch. Trained using AutoGluon for automated hyperparameter tuning.

## Why Multi-Modal Beats Single-Modal

From Tab-Text's ablation study:
- Tab-Text (full): Macro F1 0.4587, Fatal accuracy 9.63%
- Tab-Text without narrative: Macro F1 0.3946, Fatal accuracy 2.73%

The 6.9-point drop in fatal crash detection when narratives are removed is the key result. Structured features alone don't adequately distinguish fatal from serious crashes — the semantic context in the narrative (vehicle type description, maneuver sequence, road context) is what tips the scale.

UMAP visualization confirms: combined embeddings show the clearest separation between severity classes. The narrative breaks up large dense clusters into fine-grained sub-clusters, revealing context-specific patterns.

## Contrast with CrashSage's Approach

| | Tab-Text | CrashSage |
|--|----------|-----------|
| Keeps original tabular features | Yes | No (narrative only) |
| Text encoder | ELECTRA (encoder-only) | LLaMA3-8B (decoder, fine-tuned) |
| Text generation | Template only | Template + LLM augmentation |
| Interpretation | Permutation importance | Word-level gradient attribution |
| Task | 3-class | Binary |

CrashSage abandons the tabular branch entirely, betting that a well-adapted generative LLM can extract everything useful from the narrative alone. The fact that SFT LLaMA3-8B achieves Macro F1 0.7361 on binary classification (vs. CatBoost's 0.7284) supports this bet — but the tasks are not directly comparable.

## Open Questions / Thesis Relevance

- Is the multi-modal fusion (text + tabular) better than either alone on the same dataset and task? Tab-Text suggests yes, but only tested on Victoria data.
- Does the multi-modal approach offer interpretability advantages? Tab-Text only uses permutation importance, which can't attribute importance to specific words in the narrative. A hybrid that uses Tab-Text's fusion architecture but adds word-level attribution would be novel.
- How does performance scale with narrative quality? The Tab-Text paper didn't test LLM-augmented narratives — that's one direction CrashSage took.

## Related Concepts

- [[concepts/tabular-to-text-transformation]] — how narratives are constructed
- [[concepts/crash-severity-inference]] — the prediction task
- [[concepts/llm-domain-adaptation]] — alternative approach (CrashSage) that drops the tabular branch
- [[entities/electra]] — the text encoder used in Tab-Text
