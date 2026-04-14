---
title: "Tab-Text: Bridging Tabular Data and Natural Language for Enhanced Traffic Safety Analysis and Modeling"
type: source
source_file: "raw/papers/Tab-Text Bridging tabular data and natural language for enhanced traffic safety analysis and modeling.md"
date_ingested: "2026-04-08"
tags: [paper, thesis-core, method, traffic-safety, multimodal, nlp]
doi: "10.1016/j.eswa.2025.128450"
---

## Summary

Tab-Text is one of the earliest papers to apply LLMs to traffic crash severity analysis. Its central argument is that conventional crash data formats — numeric codes and categorical fields — discard crucial semantic context that could improve prediction. The fix is a **data-centric, multi-modal paradigm**: convert structured tabular crash records into coherent textual narratives using a template, then train a model that processes both the original tabular features and the narrative simultaneously.

The paper is explicitly data-centric: the innovation is in how the data is represented, not the model architecture. The text encoder is ELECTRA (an encoder-only transformer), which processes the narrative into a [CLS] embedding. Separate MLP heads process categorical and numerical features. All three branches are concatenated into a unified embedding and passed through two dense layers for severity prediction.

The task is **multi-class crash severity inference** — minor injury, serious injury, or fatal — framed as classification on a per-vehicle record level.

### Dataset

Victoria, Australia (VicRoads CrashStats), 2006–2020. ~292,000 samples after cleaning (4 non-injury cases excluded). Severe class imbalance: 67.6% minor injury, 30.8% serious, 1.6% fatal. Experiments run on both the imbalanced dataset and a downsampled balanced version.

### Architecture

- **Textual head:** ELECTRA-base (12-layer encoder, 768-dim [CLS] output)
- **Categorical head:** factorized embedding + MLP (64 → 768 dim)
- **Numerical head:** min-max normalization + MLP (→ 768 dim)
- **Fusion:** concatenation of all three heads (2304 dim) → 2 dense layers
- Narratives are template-generated from tabular fields (no LLM augmentation)

### Results

| Model | Macro F1 | Micro-Accuracy |
|-------|----------|----------------|
| Tab-Text (ELECTRA) | **0.4587** | **0.7152** |
| T2T-Transformer (text only) | 0.4179 | 0.7008 |
| CatBoost | 0.4118 | 0.6962 |
| AT-Transformer (textualized) | 0.4024 | 0.6965 |
| MNL | 0.3317 | 0.7054 |

Ablation: removing the textual narrative drops Macro F1 from 0.4587 → 0.3946. Fatal crash accuracy drops 6.9 percentage points and serious crash accuracy drops 7.5 points — confirming that narratives drive the gain specifically on rare, high-severity cases.

Balanced dataset (downsampled): ranking holds, Tab-Text Macro F1 0.5629 vs T2T 0.5597.

### Interpretability

Permutation importance (not SHAP — chosen for computational efficiency). Top features: DCA code (manner of accident), speed zone, vehicle movement, accident type, collision point, age group, region. Rankings are consistent with significant factors identified by the MNL model, validating the model's domain relevance.

UMAP visualization shows that adding textual embeddings breaks up dense class-overlapping clusters into more separable sub-clusters, with clear separation for fatal (red) and serious (green) from minor (blue) accidents.

## Key Takeaways

- Textual narratives built from tabular data consistently improve crash severity prediction, especially for fatal/serious cases — the rarest and most critical outcomes.
- The multi-modal fusion (text + tabular together) outperforms text-only or tabular-only models.
- Template-constructed coherent narratives outperform direct textualization of raw field values (T2T > AT).
- The gain comes from the narratives activating pre-trained semantic knowledge in ELECTRA; coherence in the narrative is key to triggering this knowledge.
- Identified risk factors align with classical econometric models, suggesting the model is learning legitimate patterns, not artifacts.
- Key limitation: ELECTRA is encoder-only — no generative explanation capability. Permutation importance gives variable salience, not word-level reasoning traces.

## Links

- [[concepts/tabular-to-text-transformation]]
- [[concepts/crash-severity-inference]]
- [[concepts/multimodal-crash-modeling]]
- [[entities/electra]]
- [[entities/catboost]]
- [[sources/crashsage]] — directly builds on this work, extends to generative LLM + word-level explanations
