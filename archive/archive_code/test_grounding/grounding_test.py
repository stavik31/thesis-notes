import unsloth
import torch
from unsloth import FastLanguageModel
import json
import csv
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import random

FAISS_PATH     = "/home/vik-esoc/Desktop/thesis-code/rag/faiss_index.bin"
METADATA_PATH  = "/home/vik-esoc/Desktop/thesis-code/rag/metadata.jsonl"
LORA_PATH      = "/home/vik-esoc/Desktop/thesis-code/llm/lora_adapter"
COLLISION_PATH = "/home/vik-esoc/Desktop/thesis-code/data/collision.csv"
TEST_PATH      = "/home/vik-esoc/Desktop/thesis-code/llm/test.jsonl"

N_QUERIES = 5
SEED      = 42
random.seed(SEED)

# ── load index + metadata ──────────────────────────────────────────────────
print("Loading FAISS index...")
index = faiss.read_index(FAISS_PATH)

coords = {}
with open(COLLISION_PATH) as f:
    for row in csv.DictReader(f):
        try:
            coords[row["collision_index"]] = (float(row["latitude"]), float(row["longitude"]))
        except (ValueError, KeyError):
            pass

metadata = []
with open(METADATA_PATH) as f:
    for line in f:
        metadata.append(json.loads(line))

print("Loading sentence encoder...")
encoder = SentenceTransformer("all-MiniLM-L6-v2", local_files_only=True)

print("Loading fine-tuned model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=LORA_PATH,
    max_seq_length=1024,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(model)
print("Ready.\n")

# ── retrieval helpers ──────────────────────────────────────────────────────
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    dphi       = np.radians(lat2 - lat1)
    dlambda    = np.radians(lon2 - lon1)
    a = np.sin(dphi/2)**2 + np.cos(phi1)*np.cos(phi2)*np.sin(dlambda/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))

def spatial_filter(lat, lon, radius_m=1000):
    lats = np.array([m["latitude"] for m in metadata])
    lons = np.array([m["longitude"] for m in metadata])
    return np.where(haversine(lat, lon, lats, lons) <= radius_m)[0]

def semantic_search(narrative, candidates, k=10):
    if len(candidates) == 0:
        return []
    qvec = encoder.encode([narrative], convert_to_numpy=True)
    cvecs = np.array([index.reconstruct(int(i)) for i in candidates])
    sub = faiss.IndexFlatL2(qvec.shape[1])
    sub.add(cvecs)
    _, local_idx = sub.search(qvec, min(k, len(candidates)))
    return [candidates[i] for i in local_idx[0]]

def format_context(retrieved_indices):
    lines = []
    for i, idx in enumerate(retrieved_indices):
        m = metadata[idx]
        lines.append(f"Crash {i+1} [{m['label']}]:\n{m['narrative']}")
    return "\n\n".join(lines)

# ── three prompt variants ──────────────────────────────────────────────────
def prompt_A(query_narrative, retrieved_indices, tok):
    """Control: current bare prompt."""
    ctx = format_context(retrieved_indices)
    msgs = [
        {"role": "system", "content": "You are a road safety expert. Based only on the crash records provided, generate a brief 2-3 sentence warning for a driver at this location."},
        {"role": "user",   "content": f"Historical crashes at this location:\n\n{ctx}\n\nCurrent conditions:\n{query_narrative}\n\nWhat should the driver watch out for?"}
    ]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

def prompt_B(query_narrative, retrieved_indices, tok):
    """Force-cite: must name specific crashes by number."""
    ctx = format_context(retrieved_indices)
    msgs = [
        {"role": "system", "content": (
            "You are a road safety expert analysing historical crash data for a specific location. "
            "Write a 2-3 sentence warning for a driver approaching this location. "
            "You MUST explicitly reference at least 3 of the numbered crashes above by their crash number (e.g. 'Crash 2', 'Crash 5'). "
            "Do not give generic advice — every sentence must be grounded in the specific crashes provided."
        )},
        {"role": "user", "content": (
            f"Historical crashes at this location:\n\n{ctx}\n\n"
            f"Current driver conditions:\n{query_narrative}\n\n"
            "Write a location-specific warning that cites at least 3 of the crashes above by number."
        )}
    ]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

def prompt_C(query_narrative, retrieved_indices, tok):
    """Chain-of-thought: extract patterns first, then warn."""
    ctx = format_context(retrieved_indices)
    msgs = [
        {"role": "system", "content": (
            "You are a road safety expert. Think step by step. "
            "Step 1: List the 2-3 most common crash patterns across the retrieved crashes (road conditions, vehicle types, manoeuvres, timing). "
            "Step 2: Write a 2-3 sentence driver warning that directly references those patterns. "
            "Label each step clearly."
        )},
        {"role": "user", "content": (
            f"Historical crashes at this location:\n\n{ctx}\n\n"
            f"Current driver conditions:\n{query_narrative}\n\n"
            "Step 1 — Patterns:\nStep 2 — Warning:"
        )}
    ]
    return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)

VARIANTS = [
    ("A — Bare (control)",    prompt_A),
    ("B — Force-cite",        prompt_B),
    ("C — Chain-of-thought",  prompt_C),
]

def generate(prompt_text):
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)
    n_in = inputs["input_ids"].shape[1]
    with torch.no_grad():
        out = model.generate(**inputs, max_new_tokens=200, temperature=0.7, do_sample=True)
    return tokenizer.decode(out[0][n_in:], skip_special_tokens=True)

# ── grounding signal detector ──────────────────────────────────────────────
def grounding_score(output_text, n_retrieved):
    """Count how many crash references appear in the output."""
    hits = sum(
        f"crash {i}" in output_text.lower() or f"crash{i}" in output_text.lower()
        for i in range(1, n_retrieved + 1)
    )
    return hits

# ── main loop ─────────────────────────────────────────────────────────────
with open(TEST_PATH) as f:
    test_records = [json.loads(l) for l in f]

eligible = [r for r in test_records if r["collision_index"] in coords]
queries  = random.sample(eligible, N_QUERIES)

results_summary = []

for q_idx, query in enumerate(queries):
    lat, lon = coords[query["collision_index"]]
    print("=" * 70)
    print(f"QUERY {q_idx+1}/5  |  collision_index: {query['collision_index']}  |  label: {query['label']}")
    print(f"Location: {lat:.5f}, {lon:.5f}")
    print(f"Narrative snippet: {query['narrative'][:120]}...")
    print()

    candidates = spatial_filter(lat, lon)
    retrieved  = semantic_search(query["narrative"], candidates)
    print(f"Spatial candidates: {len(candidates)}  |  Retrieved: {len(retrieved)}\n")

    if len(retrieved) == 0:
        print("  No crashes retrieved — skipping.\n")
        continue

    query_results = {"query_id": q_idx+1, "collision_index": query["collision_index"], "variants": {}}

    for vname, vfn in VARIANTS:
        print(f"--- Variant {vname} ---")
        prompt_text = vfn(query["narrative"], retrieved, tokenizer)
        output = generate(prompt_text)
        score  = grounding_score(output, len(retrieved))

        print(f"Output:\n{output}")
        print(f"[Crash references found in output: {score}/{len(retrieved)}]")
        print()

        query_results["variants"][vname] = {"output": output, "crash_refs": score, "n_retrieved": len(retrieved)}

    results_summary.append(query_results)

# ── summary table ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("GROUNDING SUMMARY — crash references cited per variant")
print("=" * 70)
print(f"{'Query':<8} {'A — Bare':<16} {'B — Force-cite':<20} {'C — CoT':<16}")
print("-" * 60)

totals = {v: 0 for v, _ in VARIANTS}
counts = {v: 0 for v, _ in VARIANTS}

for r in results_summary:
    row = f"Q{r['query_id']:<7}"
    for vname, _ in VARIANTS:
        if vname in r["variants"]:
            s = r["variants"][vname]["crash_refs"]
            n = r["variants"][vname]["n_retrieved"]
            row += f"{s}/{n}{'':>10}"
            totals[vname] += s
            counts[vname] += n
        else:
            row += f"{'skip':<16}"
    print(row)

print("-" * 60)
avg_row = "Avg refs "
for vname, _ in VARIANTS:
    if counts[vname] > 0:
        avg_row += f"{totals[vname]}/{counts[vname]}{'':>8}"
    else:
        avg_row += f"{'N/A':<16}"
print(avg_row)

print("\nVerdict key: 0 crash refs = generic output; 1+ refs = some grounding; 3+ refs = strong grounding")

# save raw results
out_path = "/home/vik-esoc/Desktop/thesis-code/test_grounding/results.json"
with open(out_path, "w") as f:
    json.dump(results_summary, f, indent=2)
print(f"\nFull results saved to {out_path}")
