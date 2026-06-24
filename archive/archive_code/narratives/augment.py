import json
import time
import argparse
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

SYSTEM_PROMPT = (
    "You are a professional editor specialising in rewriting traffic accident reports. "
    "Rewrite the following report to be more fluent and professional. "
    "Preserve all factual information exactly — times, dates, vehicle types, manoeuvres, "
    "and road conditions. Do not add any information not present in the original. "
    "Do not include injury severity or outcomes."
)


def load_model():
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
    )
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=quant_config,
        device_map="auto",
    )
    model.eval()
    return tokenizer, model


def rewrite(narrative: str, tokenizer, model) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": narrative},
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)

    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=512,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    new_tokens = output_ids[0][input_ids.shape[-1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  default="narratives_raw.jsonl")
    parser.add_argument("--output", default="narratives_augmented.jsonl")
    parser.add_argument("--limit",  type=int, default=None,
                        help="Stop after this many records (for timing estimates)")
    args = parser.parse_args()

    # resume: collect already-done collision indices
    done = set()
    if Path(args.output).exists():
        with open(args.output) as f:
            for line in f:
                done.add(json.loads(line)["collision_index"])
    print(f"Already done: {len(done)} records")

    tokenizer, model = load_model()
    print("Model loaded. Starting augmentation...\n")

    processed = 0
    times = []

    with open(args.input) as fin, open(args.output, "a") as fout:
        for line in fin:
            if args.limit and processed >= args.limit:
                print(f"\nLimit of {args.limit} reached. Stopping.")
                break

            record = json.loads(line)
            if record["collision_index"] in done:
                continue

            t0 = time.time()
            augmented = rewrite(record["narrative"], tokenizer, model)
            elapsed = time.time() - t0
            times.append(elapsed)

            out = {
                "collision_index":    record["collision_index"],
                "narrative_original": record["narrative"],
                "narrative":          augmented,
                "label":              record["label"],
            }
            fout.write(json.dumps(out) + "\n")
            fout.flush()

            processed += 1

            if processed % 10 == 0:
                avg = sum(times) / len(times)
                total_lines = sum(1 for _ in open(args.input))
                remaining = total_lines - len(done) - processed
                eta_hours = (remaining * avg) / 3600
                print(
                    f"  [{processed}] "
                    f"avg {avg:.1f}s/record | "
                    f"~{remaining:,} remaining | "
                    f"ETA {eta_hours:.1f}h"
                )

    avg = sum(times) / len(times) if times else 0
    print(f"\nDone. Processed {processed} records. Average: {avg:.2f}s/record.")


if __name__ == "__main__":
    main()
