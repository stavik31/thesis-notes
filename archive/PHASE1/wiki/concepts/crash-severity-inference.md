---
title: "Crash Severity Inference"
type: concept
tags: [thesis-core, traffic-safety, task-definition]
sources: ["[[sources/tab-text]]", "[[sources/crashsage]]"]
last_updated: "2026-04-08"
---

## Overview

Crash severity inference is the prediction task at the center of both [[sources/tab-text]] and [[sources/crashsage]]: given information about a traffic crash (its circumstances, vehicles, people, environment), classify the severity of injury outcomes. This is the benchmark against which all modeling approaches in this domain are evaluated.

## Task Formulations

The task is typically framed as multi-class or binary classification:

| Paper | Classes | Dataset | Scale |
|-------|---------|---------|-------|
| Tab-Text | 3-class: minor injury / serious / fatal | Victoria, Australia (VicRoads) 2006–2020 | ~292,000 samples |
| CrashSage | Binary: no/minor injury vs. serious/fatal | Washington State (WSDOT) 2020–2022 | ~4,433 (downsampled) |

The choice to collapse to binary (CrashSage) trades nuance for tractability — the serious/fatal boundary is the most clinically important but also the most data-scarce.

## Why It's Hard

1. **Class imbalance**: Fatal crashes are rare (1.6% in Victoria data, ~28% serious/fatal in Washington after downsampling). Models trained naively will predict the majority class and miss the cases that matter most.
2. **Information loss in structured data**: Numeric codes collapse semantically distinct events into the same value. The dynamic, sequential, relational nature of a crash is flattened into independent features.
3. **Confounding and unobserved heterogeneity**: Causality is hard to establish from observational data. Statistical approaches use random parameters and latent class models to address this; ML approaches ignore it or address it post-hoc with XAI.
4. **Jurisdictional variation**: Reporting standards, coding schemes, and road environments differ across states/countries. Models trained on one jurisdiction may not transfer.

## Modeling Evolution

The field has moved through four generations:

1. **Statistical/econometric**: Multinomial logit, random parameters models, latent class. Interpretable coefficients, but constrained by functional form assumptions and can only use structured data.
2. **Tree ensemble ML**: CatBoost, Random Forest, XGBoost. Superior predictive accuracy, handles non-linearity, post-hoc XAI via SHAP. Still structured-data-only.
3. **Deep learning**: TabTransformer, FT-Transformer, CNN/LSTM. Learns feature interactions end-to-end. Attention-based interpretability.
4. **LLM-based (current frontier)**: Tab-Text (encoder LLM + tabular fusion), CrashSage (fine-tuned decoder LLM). Processes narrative context, generates linguistic explanations.

## Key Benchmarks

Strong baselines to beat as of 2025:
- CatBoost: Macro F1 ~0.73 (binary, Washington State data per CrashSage)
- Tab-Text: Macro F1 0.4587 (3-class, Victoria data)
- SFT LLaMA3-8B (CrashSage): Macro F1 0.7361 (binary, Washington State)

The metrics are not directly comparable across datasets/task formulations — the 3-class Victoria problem is harder than the binary Washington problem.

## Evaluation Metrics

Both papers use **macro F1** as the primary metric (not accuracy), because:
- Accuracy is dominated by the majority class
- Macro F1 weights each class equally, giving full credit for correctly identifying rare fatal crashes
- Macro precision and recall reported alongside

## Related Concepts

- [[concepts/tabular-to-text-transformation]] — how raw crash data is prepared for LLMs
- [[concepts/multimodal-crash-modeling]] — Tab-Text's approach to this task
- [[concepts/llm-domain-adaptation]] — CrashSage's approach to this task
- [[concepts/gradient-based-attribution]] — how CrashSage explains its predictions on this task
