---
title: "CrashSage: A Large Language Model-Centered Framework for Contextual and Interpretable Traffic Crash Analysis"
type: source
source_file: "raw/papers/CrashSage A large language model-centered framework for contextual and interpretable traffic crash analysis.md"
date_ingested: "2026-04-08"
tags: [paper, thesis-core, method, traffic-safety, llm, fine-tuning, explainability]
doi: "10.1016/j.ait.2025.100030"
---

## Summary

CrashSage is the model-centric complement to [[sources/tab-text]]. Where Tab-Text kept the original tabular features alongside narratives, CrashSage converts everything to narrative and fine-tunes a generative LLM (LLaMA3-8B) end-to-end for crash severity inference. The core bet is that a domain-adapted language model can outperform both tabular ML models and general-purpose LLMs at the same task — and produce richer, more actionable explanations in the process.

The paper presents four principal contributions:

1. **Tabular-to-text transformation with relational schema integration** — crash records from Washington State's four-table relational database (Crash, Vehicle, Person, Road Segment) are merged via foreign keys and converted into coherent narrative templates. Numerical codes are mapped to human-readable descriptions. Structural and relational information is preserved in a way structured tabular formats cannot capture.

2. **Context-aware data augmentation** — a pretrained LLaMA3-8B is used as a "professional editor" to rewrite the template-generated narratives into more coherent, standardized text, while preserving all factual content. This is done before fine-tuning, as a preprocessing step.

3. **Supervised fine-tuning (SFT)** — LLaMA3-8B is fine-tuned on the augmented narratives using LoRA (rank 128, alpha 256) with AdamW optimizer, cosine scheduler, trained for 30 epochs on 4× Nvidia A6000 48GB GPUs. Task framed as next-token generation (binary severity label as output token).

4. **Gradient-based word-level explanation** — Taylor approximation is used to compute the importance of each input token to the output prediction. Scores are normalized and thresholded. A downstream GPT-4o pipeline categorizes high-attribution words into five aspects: environmental, vehicle/occupant, driver behavior, infrastructure, and unusual factors.

### Dataset

Washington State (WSDOT), 2020–2022. Four relational tables. Original class imbalance: 49,648 minor/no injury vs. 1,779 serious/fatal. Stratified downsampling used: final dataset 2,654 minor + 1,779 serious/fatal. Binary classification task (unlike Tab-Text's 3-class).

### Results

| Setting | Model | Macro F1 | Accuracy |
|---------|-------|----------|----------|
| SFT | LLaMA3-8B | **0.7361** | **0.7395** |
| Tabular | CatBoost | 0.7284 | 0.7383 |
| Tabular | TabTransformer | 0.7206 | 0.7609 |
| Tabular | FT-Transformer | 0.7132 | 0.7233 |
| ZS | GPT-4o | 0.7067 | 0.7229 |
| ZS | LLaMA3-8B | 0.6726 | 0.6883 |
| ZS_CoT | GPT-4o | 0.3693 | 0.4443 |
| FS | LLaMA3-70B | 0.7051 | 0.7184 |

**Key result:** SFT LLaMA3-8B beats everything. Critically, domain-specific fine-tuning of the 8B model outperforms the 70B model in all zero/few-shot configurations. Chain-of-Thought prompting dramatically *hurts* performance — GPT-4o drops from 0.7067 (ZS) to 0.3693 (ZS_CoT), suggesting that step-by-step reasoning prompts generate speculative text that deviates from domain-consistent interpretation.

### Gradient-Based Explanation Findings

Word-level attribution reveals:
- For minor-injury crashes: temporal markers, location identifiers, driver demographics, and negated risk factors (e.g., "not a hit-and-run") are influential.
- For serious/fatal crashes: vehicle type (especially motorcycle), specific road identifiers, intoxication (even when negated!), and collision type (rear-end) receive high attribution.

Co-occurrence Sankey diagram (across the dataset): intoxication and alcohol-related behaviors emerge as central behavioral nodes, linking to temporal patterns (time of day), infrastructure factors, and restraint usage. Speed + impairment co-occur frequently, suggesting synergistic crash risk.

## Key Takeaways

- Fine-tuning a small domain-specific LLM beats larger general-purpose models — model scale is less important than domain adaptation.
- Chain-of-thought prompting is actively harmful for structured prediction tasks in this domain; avoid it.
- Gradient-based attribution provides word-level insight that SHAP or permutation importance cannot: it tells you *which words* in the narrative drove the prediction.
- The primary value of the LLM approach over tree models is not (just) accuracy — it is richer interpretability and the ability to surface interaction effects.
- LLMs identify intoxication as high-attribution even when negated in the text — the model learns that the *presence or absence* of this factor is diagnostically relevant.
- Limitation: single jurisdiction (Washington State), binary task only, no causal inference, gradient attributions are approximations.

## Links

- [[concepts/tabular-to-text-transformation]]
- [[concepts/crash-severity-inference]]
- [[concepts/llm-domain-adaptation]]
- [[concepts/gradient-based-attribution]]
- [[entities/llama3-8b]]
- [[entities/catboost]]
- [[sources/tab-text]] — predecessor; CrashSage extends its data-centric direction with a model-centric generative approach
