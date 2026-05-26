# Wiki Index

Content catalog — updated after every ingest, progress note, query filed, or lint pass.

---

## Overview

| Page | Description |
|------|-------------|
| [[wiki/overview]] | Evolving thesis argument + project state |

---

## Sources (Papers & Articles)

| Page | Title | Date Ingested | Tags |
|------|-------|---------------|------|
| [[wiki/sources/tab-text]] | Tab-Text: Bridging Tabular Data and Natural Language for Traffic Safety | 2026-04-08 | thesis-core, multimodal, nlp |
| [[wiki/sources/crashsage]] | CrashSage: LLM-Centered Framework for Traffic Crash Analysis | 2026-04-08 | thesis-core, llm, fine-tuning, explainability |

---

## Concepts & Methods

| Page | Description |
|------|-------------|
| [[wiki/concepts/tabular-to-text-transformation]] | Converting structured crash records into natural language narratives for LLM processing |
| [[wiki/concepts/crash-severity-inference]] | The prediction task: classify crash injury outcomes from pre-event features |
| [[wiki/concepts/multimodal-crash-modeling]] | Tab-Text's paradigm: fuse textual narratives with tabular features end-to-end |
| [[wiki/concepts/llm-domain-adaptation]] | Fine-tuning vs. prompting LLMs for specialized traffic safety reasoning (CrashSage) |
| [[wiki/concepts/gradient-based-attribution]] | Word-level explanation via Taylor approximation of token importance (CrashSage) |
| [[wiki/concepts/rag-narrative-generation]] | Earlier RAG framing — superseded by system-architecture |
| [[wiki/concepts/system-architecture]] | Full system design: location-based crash risk advisor, offline/online pipeline, build order, evaluation plan |

---

## Entities (People, Tools, Datasets, Orgs)

| Page | Type | Description |
|------|------|-------------|
| [[wiki/entities/llama3-8b]] | tool | Decoder LLM used for fine-tuning and data augmentation in CrashSage |
| [[wiki/entities/electra]] | tool | Encoder LLM used as text backbone in Tab-Text |
| [[wiki/entities/catboost]] | tool | Primary tabular baseline in both papers; state-of-the-art for structured crash data |
| [[wiki/entities/stats19]] | dataset | UK national crash database; primary thesis dataset; 5 years, ~500k–700k records, 3-class severity |
| [[wiki/entities/stats19-field-reference]] | dataset | Full field-by-field reference for STATS19 CSVs; code mappings, severity distribution, recommended fields for narratives |

---

## Progress Notes

| Page | Date | Summary |
|------|------|---------|
| [[wiki/progress/2026-04-08]] | 2026-04-08 | First session: papers read, STATS19 confirmed as dataset, CrashSage replication set as first implementation target |
| [[wiki/progress/crashsage-replication-plan]] | 2026-04-09 | Step-by-step CrashSage replication plan for STATS19, with paper section references and deviation log |
| [[wiki/progress/2026-04-30]] | 2026-04-30 | Supervisor meeting: RAG + correlation analysis + spatial/location analysis confirmed as primary direction |
| [[wiki/progress/llm-finetune-plan]] | 2026-05-14 | Step-by-step fine-tuning plan for LLaMA3-8B LoRA on STATS19 narratives |
| [[wiki/progress/2026-05-20]] | 2026-05-20 | Fine-tuning complete: gemma-3-4b-it, downsampled training, Macro F1 0.397, zero-shot baseline next |
| [[wiki/progress/2026-05-21]] | 2026-05-21 | Phase 1 complete: three-way comparison (zero-shot 0.149, XGBoost 0.350, fine-tuned 0.408); RAG starts next |
| [[wiki/progress/RAG_PLAN]] | 2026-05-21 | Step-by-step RAG Phase 2 plan: FAISS index, spatial filter, semantic retrieval, prompt construction, evaluation |
| [[wiki/progress/2026-05-25]] | 2026-05-25 | RAG offline phase complete: FAISS index built, embeddings saved, query.py next |
| [[wiki/progress/2026-05-26]] | 2026-05-26 | RAG online phase complete: end-to-end pipeline working; generic output identified; presentation prep begins |

---

## Queries

| Page | Question | Date |
|------|----------|------|
| [[wiki/queries/tabular-to-text-stats19-implementation]] | How to implement tabular-to-text transformation for STATS19? | 2026-04-24 |
| [[wiki/queries/why-finetune-zero-shot-ablation]] | Why fine-tune if the base model already understands crashes? And what baselines to run? | 2026-04-28 |

---

*Last updated: 2026-05-21 | Total pages: 20*
