import json
import random
from collections import defaultdict
import matplotlib.pyplot as plt
from datasets import Dataset
from unsloth import FastLanguageModel
from trl import SFTTrainer, SFTConfig

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="google/gemma-3-4b-it",
    max_seq_length=1024,
    load_in_4bit=True
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=32,
    target_modules=["q_proj","k_proj","v_proj","o_proj",
                    "gate_proj","up_proj","down_proj"],
    lora_dropout=0.05,
    bias="none"
)

def format_record(record):
    messages = [
        {"role": "system", "content": "You are a road safety expert. Classify the crash severity as exactly one of: Slight, Serious, Fatal."},
        {"role": "user", "content": record["narrative"]},
        {"role": "assistant", "content": record["label"]},
    ]
    return {"text": tokenizer.apply_chat_template(messages, tokenize=False)}

def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f]

def downsample(records, seed=42):
    random.seed(seed)
    by_class = defaultdict(list)
    for r in records:
        by_class[r["label"]].append(r)
    min_count = min(len(v) for v in by_class.values())
    balanced = []
    for label_records in by_class.values():
        balanced.extend(random.sample(label_records, min_count))
    random.shuffle(balanced)
    return balanced

raw_train = load_jsonl("train.jsonl")
train_data = Dataset.from_list([format_record(r) for r in downsample(raw_train)])
val_data   = Dataset.from_list([format_record(r) for r in load_jsonl("val.jsonl")])

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=train_data,
    eval_dataset=val_data,
    args=SFTConfig(
        output_dir="./output",
        num_train_epochs=3,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        bf16=True,
        logging_steps=50,
        eval_strategy="steps",
        eval_steps=500,
        save_steps=500,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        dataset_text_field="text",
        max_seq_length=1024,
    ),
)

trainer.train()

model.save_pretrained("./lora_adapter")
tokenizer.save_pretrained("./lora_adapter")

# --- Training curves ---
history = trainer.state.log_history
train_steps, train_loss = [], []
eval_steps, eval_loss = [], []

for entry in history:
    if "loss" in entry and "eval_loss" not in entry:
        train_steps.append(entry["step"])
        train_loss.append(entry["loss"])
    if "eval_loss" in entry:
        eval_steps.append(entry["step"])
        eval_loss.append(entry["eval_loss"])

plt.plot(train_steps, train_loss, label="train loss")
plt.plot(eval_steps, eval_loss, label="eval loss", marker="o")
plt.xlabel("Step")
plt.ylabel("Loss")
plt.title("Loss Curve")
plt.legend()
plt.tight_layout()
plt.savefig("training_curves.png", dpi=150)
plt.close()
print("Saved training_curves.png")
