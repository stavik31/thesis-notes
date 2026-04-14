---
title: "Gradient-Based Attribution for LLM Explanation"
type: concept
tags: [method, explainability, xai, thesis-core]
sources: ["[[sources/crashsage]]"]
last_updated: "2026-04-08"
---

## Overview

Gradient-based attribution is the explainability method used in [[sources/crashsage]] to identify which words in a crash narrative most influenced the model's severity prediction. It computes the importance of each input token using the model's gradient with respect to that token's embedding — directly leveraging the model's learned parameters rather than perturbing inputs or using a surrogate model.

## Method (CrashSage Implementation)

**Intuition**: If removing a token would change the output probability, that token is important. Approximate this change using a first-order Taylor expansion around the full-input prediction.

**Formal definition:**

Importance of input token $x_n$ on output token $y_m$:

$$I_{n,m} \approx \langle \frac{\partial f(y_m | Z_m)}{\partial E_i[x_n]}, E_i[x_n] \rangle$$

Where $E_i[x_n]$ is the word embedding of token $x_n$ and $Z_m$ is the full context. This is the dot product of the gradient and the embedding — essentially how much the embedding is "pointing in the direction of change."

**Normalization and thresholding:**

$$(\hat{S})_{n,m} = \lceil \frac{L \times I_{n,m}}{\max_{n'} I_{n',m}} \rceil \text{ if } > b, \text{ else } 0$$

Scaling factor $L = 100$, binary threshold $b = 1$.

**Post-processing**: Sub-word tokens are aggregated to whole-word level. High-attribution words are then categorized into five aspects (environmental, vehicle/occupant, driver behavior, infrastructure, unusual) using a GPT-4o summarization pipeline.

## Advantages Over Alternatives

| Method | Advantage | Disadvantage |
|--------|-----------|--------------|
| Gradient-based (CrashSage) | Faithful to model internals; no out-of-dist inputs; computationally efficient | Approximation; assumes continuity in discrete token space |
| Permutation importance (Tab-Text) | Model-agnostic; simple to interpret | Feature-level only, not word-level; independence assumption |
| SHAP | Theoretically grounded (Shapley axioms) | Exponential complexity for exact; surrogate can misrepresent |
| Attention weights | Intuitive visualization | Not faithful proxies for model reasoning (Jain & Wallace 2019) |

## Key Empirical Findings (CrashSage)

**Minor-injury crash patterns:**
- High attribution to: temporal markers, location, driver demographics, negated risk factors ("not a hit-and-run")
- The *absence* of risk factors is flagged — the model learns what distinguishes low-severity cases

**Serious/fatal crash patterns:**
- High attribution to: vehicle type (motorcycle especially), intoxication (even when negated in text), collision type (rear-end), specific road identifiers
- "Intoxication" receives high attribution score 2.68 even when the text says the driver was NOT intoxicated — the model has learned this factor is diagnostically critical regardless of direction

**Co-occurrence analysis (Sankey diagram):**
- Intoxication/alcohol impairment: central behavioral node linking environmental + infrastructure factors
- Speed + impairment: frequent co-occurrence suggesting synergistic risk amplification
- Restraint usage linked to intoxication status: behavioral coupling

## Limitations

- **Approximation**: Assumes model output is differentiable with respect to input token embeddings; tokenization is discrete, so this is not strictly satisfied
- **Attribution ≠ causation**: High attribution means the model weighted a word heavily — not that the word caused the crash outcome
- **No formal evaluation**: CrashSage only manually validated the summary outputs; no quantitative faithfulness metric reported
- **GPT-4o dependency**: The aspect-categorization step uses GPT-4o, introducing potential hallucination risk and API dependency

## Thesis Relevance

This is potentially the most novel capability in the pipeline — word-level explanations for crash severity that can be directly read by safety practitioners. The contrast with SHAP/permutation importance (which only give feature-level salience) is significant. A thesis could extend this by: (a) formally evaluating attribution faithfulness, (b) applying it to a different jurisdiction, or (c) combining it with the multi-modal architecture of Tab-Text.

## Related Concepts

- [[concepts/llm-domain-adaptation]] — the fine-tuned model being explained
- [[concepts/crash-severity-inference]] — the task being explained
- [[entities/llama3-8b]] — the model whose gradients are computed
