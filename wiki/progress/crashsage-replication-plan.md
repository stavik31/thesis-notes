---
title: "CrashSage Replication Plan (STATS19)"
type: progress
date: "2026-04-09"
tags: [progress, method, experiment, thesis-core]
---

# CrashSage Replication Plan

Step-by-step plan for replicating the [[sources/crashsage]] framework on the [[entities/stats19]] dataset. Each step references the specific paper section so you can read alongside this guide. Where STATS19 differs from the original Washington State (WSDOT) data, adaptations are noted explicitly.

**Paper:** CrashSage — DOI: [10.1016/j.ait.2025.100030](https://doi.org/10.1016/j.ait.2025.100030)
**Raw file:** `raw/papers/CrashSage A large language model-centered framework...md`

---

## Overview of the Pipeline

```
STATS19 tables
    └─► Relational join + schema mapping     [Section 3.1]
        └─► Tabular-to-text transformation   [Section 3.2]
            └─► Context-aware augmentation   [Section 4.2]
                └─► Supervised fine-tuning   [Section 4.3]
                    └─► Evaluation           [Section 5]
                        └─► Gradient attribution [Section 4.4]
```

---

## Step 1 — Understand and Load STATS19

**Paper reference:** Section 3, Section 3.1

The paper uses WSDOT data with **4 tables**: Crash, Vehicle, Person, Road Segment linked via `CASENO` and spatial keys. STATS19 has **3 tables**:

| STATS19 table | WSDOT equivalent     | Notes                                                                                                         |
| ------------- | -------------------- | ------------------------------------------------------------------------------------------------------------- |
| `Accident`    | Crash + Road Segment | Road attributes are embedded directly in the Accident table in STATS19 — no separate road segment join needed |
| `Vehicle`     | Vehicle/Unit         | Linked via `Accident_Index`                                                                                   |
| `Casualty`    | Person               | Linked via `Accident_Index` + `Vehicle_Reference`                                                             |

**What to do:**
1. Load 5 years of data from the three STATS19 tables. Confirm `Accident_Index` is the primary key linking all three.
2. Inspect the field list for each table. Map numeric codes to categories (the STATS19 data dictionary does this — many fields use integer codes like `1 = Fatal`, `2 = Serious`, `3 = Slight`).
3. Confirm the severity distribution. The paper found a 28:1 imbalance (49,648 minor vs. 1,779 serious/fatal). Expect something similar in STATS19.

**Key decision:** The paper uses **binary** classification (minor vs. serious/fatal). STATS19 has **3 classes** (Slight, Serious, Fatal). Decide upfront whether to:
- Collapse to binary (Slight vs. Serious+Fatal) to match the paper exactly, OR
- Keep 3-class (closer to Tab-Text's setup, and arguably more informative)

For strict replication, collapse to binary first. Run 3-class as a follow-up experiment.

---

## Step 2 — Relational Schema Integration

**Paper reference:** Section 3.1

The paper joins all four tables into a **nested dictionary** (one record per crash), then serializes to JSONL. The hierarchy is:

```
crash_record {
  crash_attributes: {...}          ← Accident table
  road_segment: {...}              ← Road Segment table (in STATS19: already in Accident)
  vehicles: [                      ← Vehicle table (1 crash → many vehicles)
    {
      vehicle_attributes: {...}
      persons: [                   ← Person/Casualty table (1 vehicle → many casualties)
        { person_attributes: {...} }
      ]
    }
  ]
}
```

**What to do:**
1. For each accident, join all matching Vehicle rows (same `Accident_Index`).
2. For each vehicle, join all matching Casualty rows (same `Accident_Index` + `Vehicle_Reference`).
3. Serialize each merged record to a dict/JSON. You'll end up with one JSON object per crash, containing all relational information.
4. Drop records with no vehicle or casualty data (these will produce uninformative narratives).

**STATS19 note:** Because road attributes are already in the Accident table, you skip the spatial join the paper performs. This actually simplifies Step 2 compared to the original.

---

## Step 3 — Tabular-to-Text Transformation

**Paper reference:** Section 3.2

This is the core preprocessing step. The paper uses a **two-phase** process:

### Phase 1: Semantic normalisation
- Map all numeric codes to human-readable strings using the STATS19 data dictionary.
  - E.g., `Light_Conditions: 4` → `"darkness: no street lighting"`
  - E.g., `Road_Surface_Conditions: 2` → `"wet or damp"`
  - E.g., `Junction_Detail: 3` → `"T or staggered junction"`
- Remove null/unknown values ("nan", -1, 99, "Data missing or out of range") — don't include them in the narrative. The paper explicitly removes "uninformative null values."

### Phase 2: Template-based generation
Fill-in-the-blank templates that follow the paper's example structure (Section 3.2):

> *On [date], a [day of week] at [time], an accident involving [number] vehicles occurred [lighting conditions], with [weather conditions]. The road condition at the time was [surface condition]. The accident took place on [road name] ([road type])...*

**Critical design choice (from Section 3.2):** Separate **pre-crash conditions** from **outcome narratives**. The model should learn causation, not just correlation. Structure each narrative as:

1. *Conditions section* — environment, road, time, junction type (inputs to the crash)
2. *Crash mechanics section* — collision type, number of vehicles, manoeuvres
3. *Outcome section* — injury severity, casualties (this is the label region — mask during SFT loss)

**What to do:**
1. Write a Python function that takes a merged crash dict and returns a narrative string.
2. Handle multi-vehicle crashes: loop over vehicles and casualties, concatenating information ("Vehicle 1 was a [type] travelling [direction]...").
3. Check narrative length. The paper uses a **2048-token max sequence length** for fine-tuning. Long multi-vehicle narratives may need truncation or summarisation.

---

## Step 4 — Class Imbalance Handling

**Paper reference:** Section 3.1 (dataset description)

The paper uses **stratified downsampling** of the majority class, ending up with 2,654 minor + 1,779 serious/fatal (roughly 1.5:1 ratio).

**What to do:**
1. After building narratives, check class counts.
2. Downsample the Slight class to achieve a roughly balanced dataset. Keep a fixed random seed for reproducibility.
3. Do a stratified train/val/test split (the paper doesn't state exact split ratios — 70/15/15 or 80/10/10 are reasonable starting points).

**Alternative to consider:** Rather than downsampling, try weighted loss during fine-tuning. This preserves more data but requires tuning the weight hyperparameter. Run downsampling first (matches the paper), then weighted loss as a variant.

---

## Step 5 — Context-Aware Data Augmentation

**Paper reference:** Section 4.2

A **pretrained (not fine-tuned) LLaMA3-8B** acts as a "professional editor" that rewrites each template-generated narrative into more fluent, coherent text while preserving all facts.

**System prompt used in the paper (Section 4.2):**
> *"professional editor specializing in rewriting traffic accident reports"*

**Preservation constraints enforced:**
- Maintain all factual information (times, dates, locations, vehicle details)
- Remove uninformative placeholders (nan, unknown)
- Preserve chronological order
- Employ consistent professional language

**What to do:**
1. Load LLaMA3-8B (pretrained, not fine-tuned) via HuggingFace `transformers`.
2. For each crash narrative, call the model with a system prompt and the template narrative as user input.
3. Collect the rewritten narrative. Store both original and augmented for comparison.
4. Run in batches (the paper mentions batch processing for efficiency).

**Practical notes:**
- This step is compute-intensive. If GPU memory is limited, consider running augmentation on CPU overnight, or use a smaller rewriting model as a proxy.
- You can skip this step in a first pass and go directly to fine-tuning on template narratives — this is a valid ablation to run anyway to quantify augmentation's contribution.
- Augmentation is done once, then cached. Do not re-run it during each training cycle.

---

## Step 6 — Supervised Fine-Tuning (SFT)

**Paper reference:** Section 4.3, Section 5.1

This is the core modelling step. The task is framed as **next-token generation**: given the crash narrative as a prompt, the model generates a severity label as the output token.

### Instruction format
Wrap each training example in a chat template:

```
System: You are a professional road safety engineer.
User: [crash narrative]
Assistant: [severity label]  ← only this is used for loss
```

The paper masks the system prompt and user prompt from the loss calculation — only the assistant's output (the label) is supervised.

### LoRA configuration (Section 5.1)

| Hyperparameter | Paper value |
|---|---|
| LoRA rank (r) | 128 |
| LoRA alpha | 256 |
| LoRA dropout | 0.1 |
| Target modules | all linear layers |
| Optimizer | AdamW |
| Learning rate | 3e-5 |
| LR scheduler | cosine with 5% warmup |
| Weight decay | 1e-4 |
| Max gradient norm | 1.0 |
| Epochs | 30 |
| Batch size per device | 1 |
| Gradient accumulation steps | 16 |
| Max sequence length | 2048 tokens |
| Precision | bfloat16 |
| Framework | DeepSpeed |

**What to do:**
1. Install `transformers`, `peft`, `trl`, `deepspeed`, `bitsandbytes`.
2. Load LLaMA3-8B (or LLaMA3.1-8B if availability differs) from HuggingFace.
3. Apply LoRA config via `peft.LoraConfig`.
4. Use `trl.SFTTrainer` or a custom training loop with the above hyperparameters.
5. Train on augmented narratives. Save checkpoint each epoch or at best val F1.

**GPU note:** The paper used 4× A6000 48GB GPUs. For a single GPU with less memory:
- Reduce batch size to 1 (already done in the paper)
- Increase gradient accumulation to compensate
- Use 4-bit quantisation (QLoRA) via `bitsandbytes` if VRAM is constrained — this is a deviation from the paper but may be necessary

---

## Step 7 — Evaluation

**Paper reference:** Section 5, Table 3

The paper evaluates on **macro F1** and **accuracy**. Macro F1 is the primary metric because the dataset is imbalanced — it weights each class equally.

**What to do:**
1. Run inference on the test set with greedy decoding (paper uses greedy for determinism).
2. Extract the predicted label from the model's generated text. The model should output one of the two class strings exactly — add a parser to catch edge cases.
3. Compute macro F1 and accuracy. Compare against the paper's benchmarks:

| Model | Macro F1 | Accuracy |
|---|---|---|
| SFT LLaMA3-8B (target) | 0.7361 | 0.7395 |
| CatBoost (baseline) | 0.7284 | 0.7383 |

**Run the baselines too:** CatBoost on the same train/test split provides the key comparison. If your replicated SFT model beats CatBoost on STATS19, that validates the approach on a new jurisdiction.

---

## Step 8 — Gradient-Based Explanation

**Paper reference:** Section 4.4, Section 4.4.1

After fine-tuning, compute **word-level attribution scores** for each prediction using a first-order Taylor approximation (equation 3–5 in the paper):

- For each input token, compute the dot product of the gradient of the output probability w.r.t. the token embedding with the token embedding itself.
- Normalise scores to [0, 100] with threshold b=1 (paper's hyperparameters: L=100, b=1).
- High-scoring tokens are those the model relies on most for its severity prediction.

**Implementation:**
1. Retain the embedding layer's gradients during a forward pass (use `torch.no_grad(False)` and register a backward hook on embeddings).
2. Run backward from the predicted class probability.
3. Extract `grad * embedding` per token. Sum over embedding dim, take absolute value.
4. Normalise and threshold.

**Downstream analysis (Section 4.4.2):** The paper then pipes high-attribution tokens into GPT-4o with a structured prompt, categorising them into 5 aspects:
1. Environmental conditions
2. Vehicle/occupant characteristics
3. Driver behaviour
4. Infrastructure
5. Unusual factors

You can replicate this with GPT-4o API calls, or use a cheaper local model for the categorisation step.

**Co-occurrence analysis:** Across the test set, find which high-attribution factors co-occur frequently (Sankey diagram in the paper). This is where the thesis contribution emerges — STATS19 may surface different co-occurrence patterns than Washington State.

---

## Deviations to Track

Document these as you go — each is a potential contribution or limitation:

| Deviation | Reason | Expected effect |
|---|---|---|
| STATS19 vs. WSDOT | Different jurisdiction | Tests generalisability of the framework |
| 3-class vs. binary severity | STATS19 native | More informative but harder task |
| QLoRA instead of full LoRA | GPU memory | Slight performance drop expected |
| Skip augmentation (ablation) | Compute cost | Quantifies augmentation's value |
| No Road Segment table join | STATS19 schema | Road info embedded in Accident table — should be neutral |

---

## Links

- [[sources/crashsage]] — the paper this plan replicates
- [[sources/tab-text]] — the simpler prior approach; useful as an additional baseline
- [[entities/stats19]] — the dataset
- [[entities/llama3-8b]] — the model being fine-tuned
- [[entities/catboost]] — the key tabular baseline to beat
- [[concepts/tabular-to-text-transformation]] — the preprocessing approach
- [[concepts/llm-domain-adaptation]] — the SFT strategy
- [[concepts/gradient-based-attribution]] — the interpretability method
- [[concepts/crash-severity-inference]] — the prediction task
