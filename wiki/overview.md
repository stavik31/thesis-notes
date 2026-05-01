# Overview

*Evolving thesis argument + project state. Updated after major ingests and milestones.*

---

## Thesis Argument

*(Formal research question TBD — to be finalised after correlation analysis and RAG prototype. Contribution is now clear:)*

This thesis proposes and evaluates a **RAG-based crash risk narrative generation system**: given a road location or crash scenario described by structured STATS19 features, the system retrieves similar historical crashes and uses a local LLM to generate a human-readable risk narrative for drivers or road safety practitioners.

The contribution is the **generation-first framing**. Tab-Text and CrashSage both stop at a severity label or an attribution score — neither produces output usable by an end user. This system produces explanatory prose grounded in retrieved historical evidence, not predictions encoded into model weights. The LLM is a narrator, not a classifier.

The research question is whether this approach — with retrieval grounded in correlation-selected features and spatial proximity — produces narratives that are (a) factually grounded, (b) competitive with classification baselines on implied severity prediction, and (c) more useful to practitioners than a label alone.

The supporting work: correlation analysis of STATS19 to establish which variables carry signal (feeds feature selection for retrieval); spatial hotspot analysis to determine whether location adds retrieval value beyond structured features; CrashSage fine-tuning replication as the SFT comparison baseline.

---

## State of the Project

**Phase:** Data analysis. Direction confirmed by supervisor (2026-04-30). Moving from planning into hands-on data work before any modelling.

**Done:**
- Wiki initialized, two foundation papers fully processed (Tab-Text, CrashSage)
- Dataset confirmed: STATS19 (UK), 5 years, ~500k–700k records, 3 relational tables
- Tabular-to-text narrative template designed for STATS19 schema
- Zero-shot vs. fine-tuning ablation design documented
- Supervisor meeting: RAG + spatial analysis confirmed as primary direction

**Compute:** RTX 5090 (32GB VRAM, lab). LLaMA3-8B LoRA fine-tuning confirmed feasible.

**Next:**
1. Download STATS19; run correlation analysis at casualty and accident level
2. Spatial clustering (DBSCAN on lat/long) — confirm hotspots before investing in spatial features
3. Draft RAG architecture and retrieval index design
4. Establish baselines: CatBoost + zero-shot LLaMA3-8B

---

## Key Open Questions

1. Which features in STATS19 actually correlate with casualty severity? (Correlation analysis will answer this.)
2. Do crash hotspots cluster spatially in STATS19, and does location improve retrieval relevance in a RAG system?
3. What is the right retrieval strategy for crash RAG — feature-based similarity, spatial proximity, narrative embedding, or a combination?
4. How do you evaluate RAG quality beyond final prediction F1? (Retrieval precision@K on severity-matched cases is a candidate.)
5. Does RAG outperform fine-tuned CrashSage on STATS19, and under what conditions?
6. Can word-level attribution (CrashSage's gradient method) be formally evaluated for faithfulness — not just manually inspected? (Still relevant if CrashSage replication is run as a comparison.)

---

## Literature Landscape

The field has two clear approaches as of 2025:

- **Data-centric multimodal** (Tab-Text): Keep tabular features, add narrative as an additional modality, use encoder LLM. Strong baseline-beater, interpretable via permutation importance, but no word-level explanation.
- **Model-centric generative** (CrashSage): Convert everything to narrative, fine-tune decoder LLM (LLaMA3-8B with LoRA), explain via gradient attribution. Word-level insight, but single-jurisdiction and binary task only.

Both papers cite the same tabular baselines (CatBoost as the main one to beat), the same XAI lineage (SHAP, LIME, attention), and the same fundamental problem (semantic information loss in structured crash data). They are best read as two answers to the same question.

**The gap this thesis fills:** Neither paper generates output for end users. Both treat crash analysis as a classification problem with an optional post-hoc explanation layer. No existing work uses RAG to ground crash risk explanations in retrieved historical evidence, and no existing work produces human-readable narratives as the primary output. The spatial dimension (lat/long as a retrieval signal) is also unexplored in both papers.

*Last updated: 2026-04-30 | Sources: 2 | Pages: 17*
