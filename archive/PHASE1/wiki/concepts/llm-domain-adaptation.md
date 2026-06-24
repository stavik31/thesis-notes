---
title: "LLM Domain Adaptation for Traffic Safety"
type: concept
tags: [method, thesis-core, llm, fine-tuning]
sources: ["[[sources/crashsage]]"]
last_updated: "2026-04-08"
---

## Overview

LLM domain adaptation refers to the process of specializing a general-purpose pretrained language model for a specific domain — in this case, traffic safety crash analysis. [[sources/crashsage]] is the key paper demonstrating this for crash severity inference.

The central finding: **domain-specific fine-tuning matters more than model scale**. A fine-tuned 8B-parameter model (LLaMA3-8B SFT) outperforms the 70B parameter model in all zero/few-shot configurations. General-purpose LLMs, even very large ones, lack the specialized knowledge needed for structured traffic safety reasoning.

## Approaches on a Spectrum

| Approach | Description | CrashSage Result (Macro F1) |
|----------|-------------|----------------------------|
| Zero-shot | Prompt with task description, no examples | GPT-4o: 0.7067; LLaMA3-8B: 0.6726 |
| Few-shot | Provide 2 labeled examples in context | LLaMA3-70B: 0.7051; GPT-4o: 0.7062 |
| Zero-shot CoT | Prompt to reason step-by-step before answering | GPT-4o: 0.3693 ← **worse than random** |
| SFT | Full supervised fine-tuning on domain data | LLaMA3-8B: **0.7361** |

## The Chain-of-Thought Reversal

The most counterintuitive result: zero-shot chain-of-thought (CoT) dramatically *hurts* performance compared to direct zero-shot prompting. GPT-4o drops from 0.7067 (ZS) to 0.3693 (ZS_CoT). The authors' interpretation: CoT prompting encourages the model to generate speculative or extraneous reasoning that deviates from domain-consistent interpretation of crash narratives.

This is an important negative result for the thesis: **do not assume CoT reasoning improves structured prediction tasks in specialized domains**.

## CrashSage's Fine-Tuning Setup

- Base model: LLaMA3-8B (decoder-only, generative)
- Method: LoRA (Low-Rank Adaptation), rank 128, alpha 256, dropout 0.1, all linear layers
- Optimizer: AdamW, LR 3e-5, cosine scheduler, 5% warmup
- Training: 30 epochs, gradient checkpointing, batch size 1, gradient accumulation 16 steps
- Max sequence length: 2048 tokens
- Hardware: 4× NVIDIA A6000 48GB
- Framework: DeepSpeed

## Why Fine-Tuning Works

1. **Domain vocabulary**: Traffic safety has specialized terminology (DCA codes, maneuver types, infrastructure terms) that general-purpose LLMs haven't encountered in concentrated form during pretraining.
2. **Task framing**: The model is trained to produce severity labels as output tokens, so the generation objective aligns with the prediction task.
3. **Narrative structure**: Fine-tuning teaches the model which parts of the crash narrative are diagnostically relevant (vehicle type, intoxication, collision sequence) vs. incidental (exact timestamps).

## Limitations

- Single jurisdiction training data — generalizability is uncertain
- Static knowledge cutoff — won't know about new vehicle technologies or updated safety standards
- Gradient attributions are approximations, not faithful causal explanations
- Binary task only — not yet validated on 3-class severity (minor/serious/fatal)

## Related Concepts

- [[concepts/tabular-to-text-transformation]] — the input format that makes fine-tuning possible
- [[concepts/crash-severity-inference]] — the task being adapted to
- [[concepts/gradient-based-attribution]] — how the fine-tuned model is explained
- [[concepts/multimodal-crash-modeling]] — alternative approach that retains tabular features
- [[entities/llama3-8b]] — the model fine-tuned in CrashSage
