---
title: "Presentation Speaker Notes — 2026-06-02"
type: progress
date: "2026-06-02"
tags: [progress, presentation]
---

# Presentation Speaker Notes

Speaker notes for each slide. Slides 8–10, Future Work (Next Phase), and Summary are still to be written — checkpoint as of 2026-06-02.

---

## Slide 1 — Title

No notes needed. State your name, the title, one sentence setting up what you're about to present.

---

## Slide 2 — Agenda

"I'll start with the problem and why existing tools don't solve it, then briefly cover the related work that motivated our approach. I'll describe the dataset we're working with, walk through the system we built, and show the experiments we've run so far. Then I'll finish with the next phase — where the system is going and what we expect to find. This is a progress update, not a final result, so the last section is as important as the experiments."

---

## Slide 3 — Problem Formulation (Part 1)

**Slide change needed:** Replace Google Maps bullet with:
- Google Maps — real-time user reports only, no historical context
- Waze — location-based hazard warnings, but generic ("danger ahead") with no explanation of contributing factors or crash history

**Notes:**

"Every year, fewer than 1700 people die on UK roads, with a much larger number of serious injuries behind that. The data to understand why these crashes happen already exists — STATS19 is one of the most detailed national crash databases in the world, recording every police-reported crash with road conditions, location, vehicle types, and severity. The problem is it's built for analysts, not drivers. Current navigation tools don't solve this either. Google Maps relies on what users report in the moment — no memory of what has historically happened at a location. Waze goes a step further and flags dangerous locations, but all it tells you is 'be careful here.' It doesn't tell you why — what type of crash, under what conditions, what to actually watch for. That explanation is what's missing."

---

## Slide 4 — Problem Formulation (Part 2)

**Slide change needed:** Remove "quickly when needed" from the hypothesis — it implies a latency claim you haven't measured. Replace with: "A RAG system using historical crash records can produce location-specific, evidence-grounded warnings by retrieving and synthesising relevant crash context at inference time."

**Notes:**

"The gap is precisely that: no system connects historical crash evidence to a real-time driver warning that explains the specific risk at that location. Existing research treats this as a classification problem — predict severity as a label, which is useful for analysts but not for a driver. Some explainability work exists but it's built for autonomous vehicles with live sensors, a completely different setting. Our hypothesis is that retrieval-augmented generation can close that gap — given a driver's current location, retrieve the crashes that historically happened nearby under similar conditions, and synthesise that evidence into a warning that doesn't just say 'be careful' but tells you exactly what to be careful about and why."

---

## Slide 5 — Related Work

**Slide change needed:** Add one explicit bullet at the bottom: "Gap: no existing system produces location-specific warnings grounded in historical crash evidence."

**Notes:**

"There are two streams of work relevant to this thesis. The first is crash classification. Tab-Text shows that combining tabular crash data with natural language narratives improves classification — F1 goes from 0.39 to 0.45 when narratives are added. That directly motivates our tabular-to-text preprocessing step. CrashSage goes further — fine-tuning LLaMA3 on crash narratives achieves F1 0.73, very close to CatBoost at 0.72, and adds gradient-based word-level explanations. That validates that LLMs can be domain-adapted for crash reasoning, which is the foundation our fine-tuning step builds on.

The second stream is LLM-based driving explanation. RAG-Driver uses retrieval-augmented generation with a vision model to generate safety recommendations for autonomous vehicles — so the RAG paradigm has been applied to driving. But it uses live camera feeds, not historical data, and has no concept of location-based retrieval. It's designed for AVs in the moment, not for human drivers drawing on crash history.

Neither stream does what our system does. Classification systems output a label. RAG-Driver outputs real-time AV guidance. Nobody has taken historical crash records, retrieved the ones relevant to a specific location, and generated a grounded warning that explains the specific risk at that place. That's the gap."

---

## Slide 6 — Data

**No slide changes needed.**

**Notes:**

"STATS19 is the UK's national road crash database — every crash that's reported to police is recorded using a standardised form, which means the data is consistent across the whole country and across years. It's not user-generated or self-reported — it's official records, which makes it reliable as a foundation for a safety system.

The dataset is actually three relational tables — collisions, vehicles, and casualties — which we join together before processing. Collisions give us the road environment: type, location, weather, lighting. Vehicles tell us what was involved and what manoeuvre was being made. Casualties give us age, gender, and most importantly, injury severity.

That severity label is what drives our classification task — three classes: Slight, Serious, and Fatal. But look at the distribution. 386,000 Slight crashes versus 7,491 Fatal. Fatal is less than 1.5% of the dataset. This imbalance is not a minor detail — it directly shapes our training strategy and it's why a model with no domain adaptation defaults to predicting Slight for everything, which you'll see in the experiments."

---

## Slide 7 — Proposed Approach: Preprocessing (Offline)

**Slide change needed:** Add a box for LLM fine-tuning (offline) alongside the FAISS indexing step — the LoRA adapter is also built offline and needs to appear in this diagram or professors will ask where it came from.

**Notes:**

"This is the offline pipeline — everything that runs once before the live system starts.

The first step is tabular-to-text conversion. Each crash record is three joined tables — collision, vehicle, casualty. We convert each joined record into a structured natural language narrative using fixed templates: four blocks covering the scene, road conditions, vehicles involved, and casualties. The output is a paragraph describing the crash in plain English. This is what makes the data usable by a language model.

The second step is semantic encoding. We pass each narrative through a sentence transformer — specifically all-MiniLM-L6-v2. What this model does is map any piece of text to a fixed-length vector of 384 numbers. The model was pre-trained on millions of sentence pairs to ensure that semantically similar texts produce vectors that are close together in that 384-dimensional space. So two crash narratives describing similar scenarios — same road type, same conditions, similar manoeuvres — will produce vectors that are near each other, even if the exact wording is different. Every crash becomes a point in a 384-dimensional space.

The third step is building the FAISS index. FAISS takes all 500,000 vectors and builds a flat index — essentially a structured store optimised for similarity search. We're using IndexFlatL2, which means when a search is performed it will use exact Euclidean distance with no approximation. The index is saved to disk alongside a metadata file holding the original narrative, coordinates, and severity label for each crash — because FAISS only stores the vectors themselves, not the original data. The actual search happens at query time in the live system."

---

## Slides 8–12 — TO BE WRITTEN

- Slide 8: Proposed Approach — Live System
- Slide 9: Experiments Conducted — Fine-tuning
- Slide 10: Experiments Conducted — RAG Demo
- Slide 11: Next Phase (Future Work)
- Slide 12: Summary

---

## Links

- [[progress/future-plan]]
- [[progress/presentation-2026-06-02]]
- [[progress/presentation-slides-8-10]]
- [[concepts/system-architecture]]
