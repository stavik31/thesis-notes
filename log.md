# Wiki Log

Append-only chronological record. One entry per operation.
Parse with: `grep "^## \[" log.md | tail -10`

---

## [2026-04-09] reference | STATS19 field reference written
- Page: [[wiki/entities/stats19-field-reference]]
- Notable: 503,475 collisions (2020–2024), severity split Fatal=7,491 / Serious=109,977 / Slight=386,007; recommended field inclusion list for narratives; join key structure documented

## [2026-04-09] progress | CrashSage replication plan written
- Page: [[wiki/progress/crashsage-replication-plan]]
- Decisions extracted: none (plan only, no decisions made yet)
- Notable: 8-step pipeline covering schema integration, tabular-to-text, augmentation, SFT (LoRA), evaluation, and gradient attribution; includes a deviation table tracking STATS19-specific adaptations vs. the original WSDOT paper

## [2026-04-08] progress | Session 1 — dataset confirmed, implementation plan set
- Page: [[wiki/progress/2026-04-08]]
- Dataset: STATS19, 5 years, ~500k–700k records, 3 relational tables, 3-class severity
- Decision: build CrashSage on STATS19 first, identify gap empirically
- Notable: thesis angle emerging around contributing factors / causation, not just severity outcome prediction

## [2026-04-08] ingest | CrashSage + Tab-Text (both papers, sequential)
- Source pages: [[wiki/sources/tab-text]], [[wiki/sources/crashsage]]
- Concept pages created: [[wiki/concepts/tabular-to-text-transformation]], [[wiki/concepts/crash-severity-inference]], [[wiki/concepts/multimodal-crash-modeling]], [[wiki/concepts/llm-domain-adaptation]], [[wiki/concepts/gradient-based-attribution]]
- Entity pages created: [[wiki/entities/llama3-8b]], [[wiki/entities/electra]], [[wiki/entities/catboost]]
- Overview updated with thesis landscape
- Notable: These two papers are best read as two competing answers to the same question — Tab-Text keeps tabular + text; CrashSage goes all-in on narrative + generative LLM. Neither tests both approaches on the same dataset.

## [2026-04-08] setup | Wiki initialized
- Schema written: CLAUDE.md
- Index created: index.md
- Log created: log.md (this file)
- Directory structure: raw/papers/, raw/notes/, raw/misc/, raw/assets/, wiki/sources/, wiki/concepts/, wiki/entities/, wiki/progress/, wiki/queries/
- Context: Senior undergraduate thesis, ~1 year scope
- Status: Ready for first ingest
