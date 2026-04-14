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

---

## Queries

| Page | Question | Date |
|------|----------|------|
| *(none yet)* | | |

---

*Last updated: 2026-04-09 | Total pages: 13*
