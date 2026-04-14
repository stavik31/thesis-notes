# Overview

*Evolving thesis argument + project state. Updated after major ingests and milestones.*

---

## Thesis Argument

*(Formal research question TBD — to emerge from CrashSage replication on STATS19. Candidate directions:)*

This thesis replicates and extends CrashSage on STATS19 (UK national crash database), identifying gaps through implementation. The underlying tension the thesis lives in: both Tab-Text and CrashSage predict severity *outcomes* — they classify crashes after the fact. The harder and more valuable problem is identifying which factors caused the crash and to what degree. CrashSage's gradient attribution is a step toward this but is post-hoc and unevaluated for faithfulness. One likely thesis angle: does gradient attribution on UK data surface domain-relevant, actionable factors in a way that SHAP on CatBoost cannot — and can that be formally demonstrated?

---

## State of the Project

**Phase:** Literature review + implementation planning. Foundation papers processed, dataset confirmed, first implementation target set.

**Done:**
- Wiki initialized, two foundation papers fully processed
- Dataset confirmed: STATS19 (UK), 5 years, ~500k–700k records, 3 relational tables
- Implementation strategy decided: build CrashSage on STATS19 first, find gap empirically

**Compute:** RTX 5090 (32GB VRAM, lab). LLaMA3-8B LoRA fine-tuning confirmed feasible.

**Next:**
- Download STATS19, join tables, write tabular-to-text template for UK schema
- Establish baselines (CatBoost + zero-shot LLaMA3-8B)
- Full CrashSage replication → gap identification through implementation

---

## Key Open Questions

1. What dataset will the thesis use? Washington State (WSDOT) as in CrashSage? Victoria (VicRoads) as in Tab-Text? A new one?
2. Is the goal to replicate and extend CrashSage, to compare the two architectures on the same dataset, or to propose a novel hybrid?
3. Can word-level attribution (CrashSage's gradient method) be formally evaluated for faithfulness — not just manually inspected?
4. Does multi-modal fusion (Tab-Text) + generative explanation (CrashSage) combine into a stronger architecture?
5. How does cross-jurisdiction generalization work? Both papers are single-jurisdiction.

---

## Literature Landscape

The field has two clear approaches as of 2025:

- **Data-centric multimodal** (Tab-Text): Keep tabular features, add narrative as an additional modality, use encoder LLM. Strong baseline-beater, interpretable via permutation importance, but no word-level explanation.
- **Model-centric generative** (CrashSage): Convert everything to narrative, fine-tune decoder LLM (LLaMA3-8B with LoRA), explain via gradient attribution. Word-level insight, but single-jurisdiction and binary task only.

Both papers cite the same tabular baselines (CatBoost as the main one to beat), the same XAI lineage (SHAP, LIME, attention), and the same fundamental problem (semantic information loss in structured crash data). They are best read as two answers to the same question.

*Last updated: 2026-04-08 | Sources: 2 | Pages: 11*
