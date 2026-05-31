---
title: "Presentation Slides 8–10 Draft"
type: progress
date: "2026-05-31"
tags: [progress, presentation]
---

# Presentation Slides 8–10 Draft

---

## Slide 8 — Experimental Setup & Results

**Part 1: Fine-Tuning**
- Model: Gemma-3-4b-it, QLoRA (r=16), trained on STATS19 narratives
- Task: 3-class severity classification (Slight / Serious / Fatal)
- Training set downsampled to handle class imbalance
- Evaluation on held-out query set (25,174 records)

| System | Macro F1 |
|---|---|
| Zero-shot Gemma (no fine-tuning) | 0.149 |
| XGBoost (tabular baseline) | 0.350 |
| Fine-tuned Gemma-3-4b-it | 0.408 |

**Part 2: RAG System Demo**
- Input: test crash narrative + GPS coordinates (simulating a live driver query)
- Spatial filter → X crashes within 1km
- Semantic search → top 10 retrieved
- Fine-tuned Gemma generates a location-specific warning
- Show: example query narrative → example output text (screenshot or text block on slide)

**Diagrams I'd suggest including:**
- SHAP feature importance bar chart — you already have `xgb_shap_bar.png`, shows which variables matter most (speed limit, road type, light conditions etc.) — strong visual for "what factors drive crash severity"
- UK crash location map — plot lat/lon from collision.csv, shows geographic density and spread of the dataset — gives the audience a feel for what 500k records looks like spatially
- Class distribution bar chart — Slight / Serious / Fatal counts — makes the imbalance visually obvious, motivates the downsampling decision

---

## Slide 9 — Future Work

- **Prompt engineering** — force model to surface factors overrepresented at the location vs. national baseline (e.g. "rear-end collisions at this junction are 3× more frequent after dark")
- **Evaluation framework** — ablation: spatial filter vs. no spatial filter; retrieval quality (severity distribution of retrieved set vs. local baseline); warning usefulness rubric (specific, actionable, grounded)
- **Architectural tuning** — radius R (500m / 1km / 2km), top-K (5 / 10 / 20), sentence transformer variants
- **Live integration** — replace simulated query with real GPS + OpenWeatherMap API → auto-generated narrative
- **Spatial hotspot analysis** — DBSCAN clustering to identify crash hotspots; cross-reference with retrieval signal

---

## Slide 10 — Summary

- **Problem:** Drivers have no way to know why a location is dangerous based on historical evidence
- **Gap:** Existing work stops at severity labels or explains AVs — no RAG system over historical crash data for human drivers
- **Built:** End-to-end pipeline — FAISS spatial + semantic retrieval → fine-tuned Gemma → grounded location-specific warning
- **Found:** Fine-tuned Gemma (F1 0.408) outperforms XGBoost (0.350) and zero-shot (0.149); RAG system produces location-aware output
- **Next:** Prompt engineering, evaluation, ablation

---

## Open Questions (to resolve before finalising)

1. For the RAG demo on the experimental slide — show an actual example output from query.py, or keep it generic?
2. Are you planning to generate the crash location map and class distribution chart, or skip those?

---

## Links

- [[progress/presentation-2026-06-02]] — slides 1–7
