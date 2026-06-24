import json
import random 
from sklearn.model_selection import train_test_split

random.seed(42)

with open("../narratives_raw.jsonl") as f:
    records = [json.loads(line) for line in f]
    
labels = [r["label"] for r in records]

train, temp, train_labels, temp_labels = train_test_split(
    records, labels,
    test_size = 0.10,
    stratify=labels,
    random_state=42
)

val, test, _, _ = train_test_split(
    temp, temp_labels,
    test_size=0.50,
    stratify=temp_labels,
    random_state=42
)

def save_jsonl(data, path):
    with open(path, "w") as f:
        for record in data:
            f.write(json.dumps(record) + "\n")

save_jsonl(train, "train.jsonl")
save_jsonl(val, "val.jsonl")
save_jsonl(test, "test.jsonl")
print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")
