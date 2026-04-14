---
title: "LLaMA3-8B"
type: entity
entity_type: tool
tags: [llm, model]
sources: ["[[sources/crashsage]]"]
last_updated: "2026-04-08"
---

## Overview

LLaMA3-8B is Meta's 8-billion parameter open-source decoder-only language model. In [[sources/crashsage]], it plays two distinct roles: (1) as the **data augmentation agent** (pretrained, used to rewrite template narratives), and (2) as the **fine-tuned CrashSage agent** (domain-adapted for crash severity inference).

## Key Contributions / Features

- Decoder-only (generative) architecture — produces text autoregressively
- 8B parameters — manageable on 4× A6000 48GB GPUs with LoRA and bfloat16 precision
- Fine-tuned version (CrashSage SFT) achieves Macro F1 0.7361 on binary crash severity — beating LLaMA3-70B in all zero/few-shot configurations
- Used with LoRA for parameter-efficient fine-tuning (only adapters trained, base weights frozen)

## Why This Matters

The result that an 8B fine-tuned model beats a 70B general model has direct implications for deployment cost and feasibility. Domain-specific training data quality is more important than raw model scale. For a thesis building on CrashSage, this suggests that training data curation (and the quality of the tabular-to-text transformation) is likely the highest-leverage intervention.

## Related

- [[entities/electra]] — encoder-only model used in Tab-Text; different architectural approach
- [[concepts/llm-domain-adaptation]] — the fine-tuning methodology
- [[concepts/gradient-based-attribution]] — how this model is explained

## Sources

- [[sources/crashsage]]
