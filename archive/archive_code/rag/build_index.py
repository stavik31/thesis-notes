import json
import os
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

train_path = "/home/vik-esoc/Desktop/thesis-code/llm/train.jsonl"
val_path = "/home/vik-esoc/Desktop/thesis-code/llm/val.jsonl"
collision_path = "/home/vik-esoc/Desktop/thesis-code/data/collision.csv"
output_dir = "/home/vik-esoc/Desktop/thesis-code/rag/"

records = []
for path in [train_path, val_path]:
    with open(path, "r") as f:
        for line in f:
            records.append(json.loads(line))

collisions = pd.read_csv(collision_path, usecols=["collision_index", "latitude", "longitude"])
df = pd.DataFrame(records)
df = df.merge(collisions, on="collision_index", how="inner")

model = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)

embeddings_path = output_dir + "embeddings.npy"

if os.path.exists(embeddings_path):
    print("Loading embeddings from disk...")
    embeddings = np.load(embeddings_path)
else:
    print("Encoding narratives...")
    narratives = df["narrative"].tolist()
    embeddings = model.encode(narratives, batch_size=64, show_progress_bar=True, convert_to_numpy=True)
    np.save(embeddings_path, embeddings)
    print("Embeddings saved.")

print(f"Embedding Shape: {embeddings.shape}")

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)
print(f"Index Built: {index.ntotal} vectors")

faiss.write_index(index, output_dir + "faiss_index.bin")

meta = df[["collision_index", "latitude", "longitude", "label", "narrative"]].to_dict(orient="records")
with open(output_dir + "metadata.jsonl", "w") as f:
    for record in meta:
        f.write(json.dumps(record) + "\n")
print("Index and metadata saved")