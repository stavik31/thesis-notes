---
title: "LLM Fine-tuning Plan"
type: progress
date: "2026-05-14"
tags: [progress, method, thesis-core]
---

# LLM Fine-tuning Plan

**Goal:** Domain-adapt a Gemma IT model to understand crash narratives so it can synthesise location-specific driver warnings at inference time. The fine-tuning task is narrative → severity label (Slight / Serious / Fatal). The model is not deployed as a classifier — fine-tuning is domain adaptation.

**Hardware:** RTX 5080 (16GB VRAM)
**Model:** Gemma IT, non-thinking variant, 7–12B range. Exact model ID TBC — confirm a non-thinking Gemma 4 IT exists on HuggingFace; fall back to `google/gemma-3-12b-it` if not. Do not use Thinking variants — they add inference overhead and are optimised for logical deduction, not narrative generation.
**Input:** `narratives_raw.jsonl` (503,475 records, 3-class labels)

---

## Training Rationale

**Why classification as the training objective?**
The model's eventual job in the RAG system is to read retrieved crash narratives and generate a driver warning — a generation task, not a classification task. Classification is used here as a **proxy task for domain adaptation**: by training on thousands of crash narratives, the model learns which vocabulary, features, and patterns are predictive of outcomes. That domain knowledge transfers to generation at inference time. The instruct capabilities of the base model handle the generation itself.

**Why not summarisation fine-tuning?**
Summarisation fine-tuning (training on retrieved narratives → warning pairs) would be a closer match to the live task, but requires ground truth warnings that do not exist. It is a potential improvement step during the RAG phase only — if the classification-fine-tuned model produces poor warnings when plugged into the RAG system. It is not a required step and should not be planned for until RAG evaluation shows it is needed.

**Why not zero-shot (no fine-tuning)?**
Zero-shot is a baseline, not a training choice. Running the base model with no fine-tuning costs nothing and sets a floor. Fine-tuning is only justified if it beats zero-shot by a meaningful margin.

---

## Step 1 — Install libraries

```bash
pip install unsloth transformers peft trl datasets accelerate bitsandbytes
```

Use **Unsloth** — it's 2x faster than standard HuggingFace LoRA and officially supports LLaMA3.

---

## Step 2 — Get model access

Gemma models are available on HuggingFace under `google/`. Most are not gated (no approval required), but generate a token and login regardless:

```bash
huggingface-cli login
```

Use the **IT (Instruct Tuned)** variant, not the base model — already instruction-tuned, generates cleaner outputs with less training. Do not use Thinking variants.

---

## Step 3 — Split the data

Split `narratives_raw.jsonl` into train / val / test before training. Stratify by label.

| Split | Size | Purpose |
|---|---|---|
| Train | 90% (~453k) | Fine-tuning |
| Validation | 5% (~25k) | Monitor loss during training |
| Test | 5% (~25k) | Final evaluation — do not touch until the very end |

Save as: `train.jsonl`, `val.jsonl`, `test.jsonl`

---

## Step 4 — Format as instruction tuning

Use the LLaMA3 chat template:

```
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a road safety expert. Given a crash incident report, classify the severity as exactly one of: Slight, Serious, Fatal.<|eot_id|><|start_header_id|>user<|end_header_id|>

{narrative}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{label}<|eot_id|>
```

Loss is computed on the completion only, not the prompt.

---

## Step 5 — Load model in 4-bit (QLoRA)

16GB VRAM is not enough for LLaMA3-8B in bf16 (~16GB base model alone). Use 4-bit NF4 quantization — base model drops to ~4GB, leaving ~12GB for LoRA weights, activations, and optimizer state.

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-3-12b-it",  # update once exact model confirmed
    max_seq_length=1024,
    dtype=None,          # auto-detects bf16 on RTX 5080
    load_in_4bit=True,   # NF4 quantization — required for 16GB
)
```

Then apply LoRA on top:

```python
LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
```

Adds ~20M trainable parameters on top of the frozen (quantized) 8B model.

---

## Step 6 — Training configuration

```python
TrainingArguments(
    output_dir="./lora_output",
    num_train_epochs=1,
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,   # effective batch size = 16
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.05,
    bf16=True,                        # RTX 5080 supports bf16
    logging_steps=100,
    evaluation_strategy="steps",
    eval_steps=1000,
    save_steps=2000,
    save_total_limit=2,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss",
)
```

**Class imbalance** (Slight ~77%, Serious ~21%, Fatal ~2%): use weighted random sampling so Fatal and Serious are seen proportionally. Without this the model learns to predict Slight for everything.

---

## Step 7 — Train

```python
SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    peft_config=lora_config,
    args=training_args,
    max_seq_length=1024,
)
```

Watch `eval_loss` — if it starts increasing, stop early. Expected time on RTX 5080 with QLoRA: **4–6 hours for 1 epoch** (more gradient accumulation steps vs. 32GB setup).

---

## Step 8 — Save the adapter

```python
model.save_pretrained("./lora_adapter")
tokenizer.save_pretrained("./lora_adapter")
```

Saves only the LoRA weights (~50–100MB). Base model loaded separately and adapter merged at inference.

---

## Step 9 — Evaluate on test set

Run inference on `test.jsonl` (untouched until now).

| Metric | Why |
|---|---|
| Macro F1 | Main metric — treats all three classes equally |
| Per-class F1 | Shows where the model struggles (expect Fatal to be hardest) |
| Accuracy | Baseline sanity check |

**Three-system comparison:**

| System | Training required | Notes |
|---|---|---|
| XGBoost | Yes (already done) | Tabular features only, strong classical baseline |
| Gemma zero-shot | No | Base IT model, no fine-tuning, costs nothing to run |
| Gemma + LoRA | Yes (this plan) | Domain-adapted on crash narratives |

This comparison is a standalone finding before RAG is built. It answers: does fine-tuning help, and does an LLM on narratives beat classical ML on tabular features? Either outcome is a valid thesis result.

---

## Step 10 — Hyperparameter sweep *(tentative)*

**Goal:** Find the point of diminishing returns across the key LoRA hyperparameters before committing to a full training run. Equivalent to stress-testing model complexity in traditional ML — vary one axis at a time, watch where performance stagnates.

**Priority order** (most informative first given 1–2 hour run cost):

### 1. Learning curve (data efficiency)
Fix all hyperparams. Train on subsets of the training data. If macro F1 plateaus early, future ablations can use the smaller subset to iterate faster.

| Subset | Samples | Purpose |
|---|---|---|
| 10% | ~45k | Floor — does the model learn anything? |
| 25% | ~113k | Likely knee of the curve |
| 50% | ~226k | Check if gains continue |
| 100% | ~453k | Full run |

### 2. LoRA rank sweep
Fix data at whichever subset saturated above. Vary `r`:

| r | Trainable params | Expected behaviour |
|---|---|---|
| 8 | ~10M | Underfit baseline |
| 16 | ~20M | Current plan default |
| 32 | ~40M | Likely stagnation point |
| 64 | ~80M | Diminishing returns expected |

Run cost is near-identical across ranks (frozen model dominates compute). Stop increasing r when macro F1 gain < 0.5%.

### 3. Learning rate sweep
Only run if rank sweep shows sensitivity. Candidates: `5e-5`, `2e-4` (default), `5e-4`.

### 4. Epochs
Not a separate sweep — read from the `eval_loss` curve of any full run. If loss plateaus mid-epoch, that's the effective training budget. Use early stopping (`load_best_model_at_end=True` already set).

---

**Tracking:** Integrate Weights & Biases to overlay runs:

```python
# add to TrainingArguments
report_to="wandb",
run_name="gemma4-e4b-r16-100pct",  # descriptive name per run
```

```bash
pip install wandb
wandb login
```

Each run logs `eval_loss`, `train_loss`, and learning rate curve. Stagnation is visible as a flattening slope across overlaid runs.

**Estimated total sweep cost:** 8–12 runs × 1–2 hours = 1–2 days of GPU time. Run learning curve first — if 25% saturates, subsequent sweeps cost ~30 minutes each.

---

## Phase Context

This fine-tuning plan is **Phase 1 of 2**:

**Phase 1 — Standalone LLM evaluation (this plan)**
Train on classification, evaluate against XGBoost and zero-shot. The fine-tuned adapter is the output. No RAG involved.

**Phase 2 — RAG integration (future)**
Plug the fine-tuned adapter into the RAG pipeline. Retrieved crash narratives go into the prompt; the model generates a structured driver warning. No additional training is required at this stage — the same adapter from Phase 1 is used.

Summarisation fine-tuning is a potential Phase 2 improvement only if RAG evaluation shows warning quality is poor. It requires (retrieved narratives → warning) training pairs which do not currently exist and would need to be synthetically generated.

---

## Watch out for

- **VRAM** — with QLoRA + batch size 2 + seq length 1024, peak VRAM should sit around 12–14GB; if you OOM, drop `per_device_train_batch_size` to 1 first
- **Label leakage** — verify `casualty_severity` is absent from all narratives before training
- **Fatal underrepresentation** — ~2% of records; weighted sampling is not optional
- **Sequence length** — log a warning if any narrative exceeds 1024 tokens
- **Checkpoints** — each adapter checkpoint ~100MB; `save_total_limit=2` keeps disk usage sane
- **HuggingFace token** — request LLaMA3 access the night before; approval is usually instant

---

## Links

- [[concepts/system-architecture]] — where fine-tuning fits in the full pipeline
- [[concepts/llm-domain-adaptation]] — rationale for fine-tuning vs. frozen model
- [[entities/llama3-8b]] — model details
- [[entities/stats19]] — source dataset
