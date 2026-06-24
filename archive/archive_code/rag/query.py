import unsloth
import torch
from unsloth import FastLanguageModel
import json
import csv
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import random

faiss_path = "/home/vik-esoc/Desktop/thesis-code/rag/faiss_index.bin"
metadata_path = "/home/vik-esoc/Desktop/thesis-code/rag/metadata.jsonl"
lora_path = "/home/vik-esoc/Desktop/thesis-code/llm/lora_adapter"
collision_path = "/home/vik-esoc/Desktop/thesis-code/data/collision.csv"

index = faiss.read_index(faiss_path)

coords = {}
with open(collision_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            coords[row["collision_index"]] = (float(row["latitude"]), float(row["longitude"]))
        except (ValueError, KeyError):
            pass

metadata = []
with open(metadata_path, "r") as f:
    for line in f:
        metadata.append(json.loads(line))

encoder = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=lora_path,
    max_seq_length=1024,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

def spatial_filter(query_lat, query_lon, radius_m=1000):
    lats = np.array([m["latitude"] for m in metadata])
    lons = np.array([m["longitude"] for m in metadata])
    distances = haversine(query_lat, query_lon, lats, lons)
    return np.where(distances <= radius_m)[0]

def semantic_search(query_narrative, candidate_indices, k=10):
    query_vec = encoder.encode([query_narrative], convert_to_numpy=True)
    if len(candidate_indices) == 0:
        return []
    candidate_vecs = np.array([index.reconstruct(int(i)) for i in candidate_indices])
    sub_index = faiss.IndexFlatL2(query_vec.shape[1])
    sub_index.add(candidate_vecs)
    k = min(k, len(candidate_indices))
    _, local_indices = sub_index.search(query_vec, k)
    return [candidate_indices[i] for i in local_indices[0]]

def build_prompt(query_narrative, retrieved_indices):
    context = ""
    for i, idx in enumerate(retrieved_indices):
        context += f"Crash {i+1}:\n{metadata[idx]['narrative']}\n\n"

    messages = [
        {"role": "system", "content": "You are a road safety expert. Based only on the crash records provided, generate a brief 2-3 sentence warning for a driver at this location."},
        {"role": "user", "content": f"Historical crashes at this location:\n\n{context}Current conditions:\n{query_narrative}\n\nWhat should the driver watch out for?"}
    ]
    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

def generate_warning(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_length = inputs["input_ids"].shape[1]
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=150, temperature=0.7, do_sample=True)
    new_tokens = outputs[0][input_length:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True)

with open("/home/vik-esoc/Desktop/thesis-code/llm/test.jsonl") as f:
    test_records = [json.loads(line) for line in f]

query = random.choice([r for r in test_records if r["collision_index"] in coords])
lat, lon = coords[query["collision_index"]]

print(f"Query crash: {query['collision_index']} | Label: {query['label']}")
print(f"Location: {lat}, {lon}\n")

candidates = spatial_filter(lat, lon)
print(f"Crashes within 1km: {len(candidates)}")

retrieved = semantic_search(query["narrative"], candidates)
print(f"Retrieved: {len(retrieved)} crashes\n")

prompt = build_prompt(query["narrative"], retrieved)
warning = generate_warning(prompt)

print("Generated warning:")
print(warning)