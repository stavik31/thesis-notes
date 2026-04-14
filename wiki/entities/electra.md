---
title: "ELECTRA"
type: entity
entity_type: tool
tags: [llm, model, encoder]
sources: ["[[sources/tab-text]]"]
last_updated: "2026-04-08"
---

## Overview

ELECTRA (Efficiently Learning an Encoder that Classifies Token Replacements Accurately) is an encoder-only transformer model used as the text backbone in [[sources/tab-text]]. It is more computationally efficient than BERT while achieving comparable or better performance on downstream tasks.

## Key Contributions / Features

- **Training objective**: Replaced Token Detection — learns to distinguish real vs. generator-replaced tokens across *all* positions (vs. BERT's masked prediction on ~15% of tokens). This gives a stronger learning signal per compute unit.
- **Encoder-only**: Produces [CLS] token representations for classification. Not generative — cannot produce explanatory text.
- Base version: 12 transformer encoder layers, 768-dimensional embeddings
- Used in Tab-Text's textual head: narrative → ELECTRA tokenizer → [CLS] embedding (768-dim) → fused with tabular features

## Contrast with LLaMA3-8B (CrashSage)

| | ELECTRA | LLaMA3-8B |
|--|---------|-----------|
| Architecture | Encoder-only | Decoder-only |
| Can generate text | No | Yes |
| Parameters | ~110M (base) | 8B |
| Explanation method | Permutation importance only | Word-level gradient attribution |
| Training objective | Token replacement detection | Next token prediction |

The choice of encoder vs. decoder fundamentally shapes the explainability options available: ELECTRA can only report feature-level importance; LLaMA3 can generate natural language explanations and support gradient attribution to specific words.

## Related

- [[entities/llama3-8b]] — generative decoder alternative used in CrashSage
- [[concepts/multimodal-crash-modeling]] — the architecture ELECTRA is embedded in
- [[sources/tab-text]]
