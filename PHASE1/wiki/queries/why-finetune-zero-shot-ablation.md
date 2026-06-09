---
title: "Why fine-tune if the base model already understands crashes? And what baselines should we run?"
type: query
date: "2026-04-28"
tags: [method, thesis-core, experiment, llm-domain-adaptation]
---

# Why fine-tune if the base model already understands crashes?

Related pages: [[concepts/llm-domain-adaptation]], [[progress/crashsage-replication-plan]], [[entities/llama3-8b]]

---

## The question

During data augmentation, LLaMA3-8B rewrites crash narratives into fluent professional prose. This works because the model already understands what crash conditions mean — it was trained on accident reports, road safety literature, and news coverage. If it already understands crashes well enough to rewrite them intelligently, why fine-tune it at all? Has it not already "picked up on context"?

---

## The key distinction: inference vs. learning

**Augmentation is inference only.** Running a narrative through LLaMA3-8B to rewrite it is a forward pass — no weights change, nothing is learned, the model forgets everything immediately after. It never sees the severity label. It is functioning as a text editor, not a student. You could swap it for GPT-4, Claude, or a human copyeditor and get the same result.

**Fine-tuning is supervised learning.** The model sees thousands of (narrative, label) pairs and updates its weights to reliably map crash descriptions to severity classes. This is where task-specific knowledge gets injected.

```
Augmentation:
  Input:  crash narrative            [label never shown]
  Output: more fluent narrative      [label never shown]
  Weights changed: NONE

Fine-tuning:
  Input:  crash narrative + "Serious"
  Output: model adjusts weights to associate this narrative with "Serious"
  Weights changed: YES (LoRA adapters)
```

The user's intuition is partially correct: the base model DOES already have general knowledge about crash severity. Zero-shot, it would probably classify crashes at ~60–65% accuracy. Fine-tuning is needed to push that to ~73–74% — calibrated to STATS19's specific severity definitions, label format, and class distribution.

---

## The paper's gap: no zero-shot baseline

CrashSage never tests whether prompting the base model (without fine-tuning) produces competitive results. They go straight from template narratives to fine-tuning. This is a meaningful omission — if zero-shot performance is close to fine-tuned, the entire fine-tuning pipeline is hard to justify given its compute cost.

---

## The ablation to run

Three conditions, same test set:

| Condition | Description | What it tests |
|---|---|---|
| Zero-shot LLaMA3-8B | Prompt the base model directly, no fine-tuning | Does the base model already know enough? |
| Fine-tuned LLaMA3-8B (QLoRA) | Full pipeline as per CrashSage | Does task-specific training help? |
| CatBoost on raw tabular data | Gradient boosted tree on the original numeric features | Does text representation add anything over numbers? |

Zero-shot inference costs almost nothing extra — the model is already loaded for evaluation anyway.

### Interpreting each outcome

Any result is a valid finding:

- **Fine-tuned >> Zero-shot** → fine-tuning is justified; the pipeline adds real value
- **Zero-shot ≈ Fine-tuned** → the base model's pre-existing knowledge does most of the work; fine-tuning is marginal; augmentation quality matters more than training
- **CatBoost ≈ or beats LLM** → text representation does not add value over raw features for this task and dataset; this would be the most interesting finding and the most honest replication result

The paper found fine-tuned LLaMA barely beats CatBoost (0.7361 vs 0.7284 macro F1). If that gap closes further or reverses on STATS19, that is a substantive thesis contribution — not a failure.

---

## Why this matters for the thesis

The core thesis contribution is not severity prediction — CatBoost already does that well. It is the **gradient attribution analysis**: after fine-tuning, which factors does the model pay attention to when predicting serious crashes, and do those patterns differ between UK (STATS19) and US (WSDOT) data?

The three-way comparison above contextualises that contribution: it establishes whether the fine-tuned model has learned something genuine, or whether the base model's pre-trained knowledge is doing the heavy lifting. Either answer is interesting.

---

## Links

- [[concepts/llm-domain-adaptation]] — fine-tuning strategy and LoRA configuration
- [[concepts/gradient-based-attribution]] — the downstream interpretability step
- [[progress/crashsage-replication-plan]] — full pipeline; zero-shot baseline now tracked in deviation table
- [[entities/llama3-8b]] — the model used for both augmentation and fine-tuning
- [[entities/catboost]] — the tabular baseline
