  ---
  # CONTEXT.md — Thesis Project Context

  This directory contains data processing and modelling code for a senior undergraduate thesis replicating the **CrashSage** framework on the **STATS19** dataset (UK national crash database).

  ---

  ## What This Project Is

  The thesis replicates and extends [CrashSage](https://doi.org/10.1016/j.ait.2025.100030), a framework that converts structured crash records into natural language narratives, fine-tunes LLaMA3-8B (via LoRA) for severity classification, and explains predictions
  using gradient-based word attribution.

  The original paper used Washington State (WSDOT) data. This thesis applies the same pipeline to STATS19 — a different jurisdiction — to test generalisability and surface UK-specific contributing factors.

  **The interesting thesis angle:** Both CrashSage and its predecessor Tab-Text predict severity *outcomes*. The more valuable problem is identifying *which factors caused the crash and to what degree*. CrashSage's gradient attribution is a step toward this but
  unevaluated for faithfulness. The thesis will investigate whether gradient attribution on UK data surfaces actionable factors in a way that SHAP on CatBoost cannot.

  ---

  ## Dataset

  **STATS19** — UK national crash database, 5 years (2020–2024)

  | Table | Equivalent in paper | Notes |
  |---|---|---|
  | `Accident` | Crash + Road Segment | Road attrs embedded directly — no separate join |
  | `Vehicle` | Vehicle/Unit | Linked via `Accident_Index` |
  | `Casualty` | Person | Linked via `Accident_Index` + `Vehicle_Reference` |

  - ~503,475 collisions total
  - Severity: Fatal = 7,491 / Serious = 109,977 / Slight = 386,007
  - Primary key linking all tables: `Accident_Index`
  - Fields use integer codes — must be mapped to strings via STATS19 data dictionary before narrative generation

  ---

  ## Pipeline Overview

  STATS19 tables
      └─► Step 1: Load + map codes to readable strings
          └─► Step 2: Relational join → one nested dict per crash
              └─► Step 3: Tabular-to-text → natural language narrative
                  └─► Step 4: Class balancing (downsample Slight)
                      └─► Step 5: Data augmentation (LLaMA3-8B as "editor")
                          └─► Step 6: Supervised fine-tuning (LoRA)
                              └─► Step 7: Evaluation (macro F1)
                                  └─► Step 8: Gradient attribution

  ---

  ## Current Step

  **Step 1–2: Data loading and schema integration** (in progress)

  - Load 5 years of Accident, Vehicle, Casualty CSVs
  - Map numeric codes to human-readable labels
  - Join into nested dicts (one record per crash): `crash → [vehicles → [casualties]]`
  - Confirm severity distribution matches expectations
  - Drop records with no vehicle/casualty data

  ---

  ## Step-by-Step Plan

  ### Step 1 — Load STATS19
  - Load Accident, Vehicle, Casualty tables for all 5 years
  - Decode integer codes using the STATS19 data dictionary
  - Target: `Accident_Severity` as the label column (1=Fatal, 2=Serious, 3=Slight)
  - **Key decision:** Collapse to binary (Slight vs. Serious+Fatal) to match CrashSage first, then run 3-class as a follow-up

  ### Step 2 — Relational Join
  - For each Accident, collect all matching Vehicle rows (by `Accident_Index`)
  - For each Vehicle, collect all matching Casualty rows (by `Accident_Index` + `Vehicle_Reference`)
  - Output: list of nested dicts, one per crash, serialisable to JSONL

  ### Step 3 — Tabular-to-Text Transformation
  - Map all codes → strings (remove nulls, -1, 99, "Data missing")
  - Write a template function producing narratives like:
    > *"On [date], a [day] at [time], an accident involving [N] vehicles occurred [lighting]. Weather: [conditions]. Road surface: [surface]. Location: [road name], [road type]..."*
  - Separate: (1) pre-crash conditions, (2) crash mechanics, (3) outcome (mask outcome from loss during SFT)
  - Handle multi-vehicle crashes by looping over vehicles/casualties
  - Check narrative lengths — 2048 token max for fine-tuning

  ### Step 4 — Class Balancing
  - Downsample Slight class to ~1.5:1 ratio (matching paper's 2,654 minor : 1,779 serious/fatal)
  - Fixed random seed for reproducibility
  - Stratified train/val/test split (70/15/15)

  ### Step 5 — Data Augmentation
  - Load pretrained (NOT fine-tuned) LLaMA3-8B
  - Use as "professional editor" to rewrite template narratives into fluent text
  - System prompt: *"professional editor specializing in rewriting traffic accident reports"*
  - Store both original and augmented narratives
  - **Note:** Can skip for a first-pass training run and treat it as an ablation

  ### Step 6 — Supervised Fine-Tuning (LoRA)
  - Task: next-token generation — input = crash narrative, output = severity label
  - Instruction format: System / User (narrative) / Assistant (label, loss here only)
  - LoRA: rank=128, alpha=256, dropout=0.1, all linear layers
  - Optimizer: AdamW, lr=3e-5, cosine scheduler, 5% warmup
  - Batch size 1, grad accum 16, 30 epochs, bfloat16, max 2048 tokens
  - Stack: `transformers`, `peft`, `trl`
  - GPU: RTX 5090 (32GB) — full LoRA feasible; use QLoRA if needed

  ### Step 7 — Evaluation
  - Greedy decoding on test set
  - Parse predicted label from generated text
  - Primary metric: **macro F1** (class-balanced)
  - Baselines to beat:
    - CatBoost tabular: F1=0.7284 (paper, WSDOT)
    - SFT LLaMA3-8B target: F1=0.7361 (paper, WSDOT)

  ### Step 8 — Gradient Attribution
  - Compute per-token importance: `grad(output prob) · embedding` (Taylor approx)
  - Normalise to [0,100], threshold at b=1
  - Aggregate sub-word tokens to whole-word level
  - Pipe high-attribution words into GPT-4o (or local model) to categorise into:
    1. Environmental conditions
    2. Vehicle/occupant characteristics
    3. Driver behaviour
    4. Infrastructure
    5. Unusual factors
  - Co-occurrence analysis across test set → Sankey diagram
  - **This is the thesis contribution:** UK-specific attribution patterns vs. Washington State

  ---

  ## Deviations from the Paper

  | Deviation | Reason | Expected effect |
  |---|---|---|
  | STATS19 vs. WSDOT | Different jurisdiction | Tests generalisability |
  | 3-class vs. binary severity | STATS19 native | Harder task, more informative |
  | QLoRA instead of full LoRA | GPU memory if needed | Slight performance drop |
  | Skip augmentation (ablation) | Compute cost | Quantifies augmentation's value |
  | No Road Segment join | STATS19 embeds road attrs in Accident | Should be neutral |

  ---

  ## Compute

  - **GPU:** RTX 5090 32GB (lab)
  - LLaMA3-8B LoRA fine-tuning confirmed feasible at full precision

  ---