import json
import torch
import matplotlib.pyplot as plt
from tqdm import tqdm
from unsloth import FastLanguageModel
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

LABELS = ["Slight", "Serious", "Fatal"]
BATCH_SIZE = 16

model, tokenizer = FastLanguageModel.from_pretrained(
      model_name="google/gemma-3-4b-it",
      max_seq_length=1024,
      load_in_4bit=True,
)
FastLanguageModel.for_inference(model)
tokenizer.tokenizer.padding_side = "left"
tokenizer.tokenizer.pad_token = tokenizer.tokenizer.eos_token

def load_jsonl(path):
    with open(path) as f:
        return [json.loads(line) for line in f]
    
def make_prompt(record):
    messages = [
        {"role": "system", "content": "You are a road safety expert. Classify the crash severity as exactly one of: Slight, Serious, Fatal. Reply with one word only."},
        {"role": "user", "content": record["narrative"]},
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def predict_batch(records):
    prompts = [make_prompt(r) for r in records]
    inputs = tokenizer.tokenizer(
        prompts, return_tensors="pt", padding=True,
        truncation=True, max_length=1024
    ).to(model.device)
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=5, do_sample=False)
    input_len = inputs["input_ids"].shape[1]
    preds = []
    for generated in out:
        decoded = tokenizer.decode(generated[input_len:], skip_special_tokens=True).strip()
        pred = "Unknown"
        for label in LABELS:
            if label.lower() in decoded.lower():
                pred = label
                break
        preds.append(pred)
    return preds

test_records = load_jsonl("test.jsonl")
y_true = [r["label"] for r in test_records]
y_pred = []

for i in tqdm(range(0, len(test_records), BATCH_SIZE), desc="Evaluating"):
    batch = test_records[i:i + BATCH_SIZE]
    y_pred.extend(predict_batch(batch))

macro_f1 = f1_score(y_true, y_pred, labels=LABELS, average="macro", zero_division=0)
per_class = f1_score(y_true, y_pred, labels=LABELS, average=None, zero_division=0)

print(f"\nMacro F1: {macro_f1:.4f}")
for label, f1 in zip(LABELS, per_class):
    print(f"  {label}: {f1:.4f}")

cm = confusion_matrix(y_true, y_pred, labels=LABELS)
fig, ax = plt.subplots(figsize=(6, 5))
ConfusionMatrixDisplay(cm, display_labels=LABELS).plot(ax=ax, colorbar=False)
ax.set_title("Zero-Shot Confusion Matrix")
plt.tight_layout()
plt.savefig("zero_shot_confusion_matrix.png", dpi=150)
plt.close()

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar(LABELS, per_class, color=["steelblue", "orange", "red"])
ax.axhline(macro_f1, linestyle="--", color="black", label=f"Macro F1 = {macro_f1:.3f}")
ax.set_ylabel("F1 Score")
ax.legend()
ax.set_title("Zero-Shot Per-Class F1 on Test Set")
plt.tight_layout()
plt.savefig("zero_shot_f1.png", dpi=150)
plt.close()

print("\nSaved zero_shot_confusion_matrix.png and zero_shot_f1.png")