from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained("google/gemma-3-4b-it", max_seq_length=1024, load_in_4bit=True)
for label in [" Slight", " Serious", " Fatal"]:
    ids = tokenizer.tokenizer.encode(label, add_special_tokens=False)
    print(label, ids)