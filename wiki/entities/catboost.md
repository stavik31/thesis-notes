---
title: "CatBoost"
type: entity
entity_type: tool
tags: [ml-model, baseline]
sources: ["[[sources/tab-text]]", "[[sources/crashsage]]"]
last_updated: "2026-04-08"
---

## Overview

CatBoost (Categorical Boosting) is a gradient boosting algorithm optimized for datasets with categorical features. It appears as the primary tabular baseline in both [[sources/tab-text]] and [[sources/crashsage]], representing the state-of-the-art for structured crash data modeling before LLM-based approaches.

## Key Contributions / Features

- Handles categorical data natively via target statistics (no manual encoding required)
- Ordered boosting prevents target leakage during training
- Outperforms or matches Random Forest, XGBoost, LightGBM on typical tabular crash data
- Fast inference, no GPU required

## Performance as Baseline

| Paper | Task | CatBoost Macro F1 | Best Model |
|-------|------|--------------------|------------|
| Tab-Text | 3-class, Victoria | 0.4118 | Tab-Text: 0.4587 |
| CrashSage | Binary, Washington | 0.7284 | SFT LLaMA3-8B: 0.7361 |

CatBoost is a remarkably strong baseline. In CrashSage's binary task, the fine-tuned LLaMA3-8B only edges it by 0.0077 Macro F1 — the performance gap is small. The real advantage of LLM-based approaches is interpretability depth (word-level attribution vs. aggregate SHAP), not raw accuracy.

## Related

- [[concepts/crash-severity-inference]] — the task where CatBoost serves as baseline
- [[entities/llama3-8b]] — the model that narrowly beats it in CrashSage
- [[entities/electra]] — part of Tab-Text which beats it in the multi-class task
