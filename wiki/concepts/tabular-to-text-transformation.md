---
title: "Tabular-to-Text Transformation"
type: concept
tags: [method, thesis-core, nlp, data-preprocessing]
sources: ["[[sources/tab-text]]", "[[sources/crashsage]]"]
last_updated: "2026-04-08"
---

## Overview

Tabular-to-text transformation is the technique of converting structured, relational crash records into coherent natural language narratives so that pre-trained LLMs can process them. It is the shared foundational innovation in both [[sources/tab-text]] and [[sources/crashsage]] — and the reason both papers exist.

The core motivation: crash databases store information as numeric codes and categorical flags (e.g., vehicle maneuver = `7`). This encoding is efficient for storage but loses critical semantic content — the distinction between "left turn" and "U-turn" collapsed into the same number, the sequential logic of a crash event, the interaction dynamics between multiple vehicles. LLMs can process and reason about semantic context, but only if the data is presented in a form that activates their pretrained knowledge.

## The Standard Pipeline

1. **Semantic normalization**: Map numeric codes to human-readable descriptions using domain-specific lexicons. E.g., `LIGHT_CONDITION = 3` → "dusk".
2. **Template generation**: Apply fill-in-the-blank templates to assemble fields into a coherent, chronologically-ordered narrative passage.
3. *(Optional in CrashSage)* **LLM augmentation**: Use a pretrained LLM to rewrite the template output into more fluent, consistent prose while preserving all factual content.

### Tab-Text Template Example (Victoria, Australia data)
> "On 25/01/2006, Wednesday, early morning, an accident occurred on a clear day with streetlights on... Prior to the accident, the driver was trying to turn right. The vehicle was turning right. The vehicle, 10 years old, was a car running on gasoline..."

### CrashSage Template Fragment (Washington State data)
> "On [date], a [day of week] at [time], an accident involving [number] vehicles occurred [lighting conditions], with [weather conditions]..."

## Key Design Choices

- **Separate outcome from antecedent**: CrashSage explicitly separates the narrative describing pre-crash conditions from the outcome (injury severity). This enforces the learning objective and prevents data leakage.
- **Relational schema integration** (CrashSage): Multiple database tables (Crash, Vehicle, Person, Road Segment) are joined via foreign keys before narrative construction. One narrative can include details about multiple persons and vehicles, preserving inter-entity relationships that are destroyed when each table row is treated independently.
- **Coherent vs. textualized**: Tab-Text's ablation shows that template-constructed coherent narratives (T2T-Transformer) outperform directly textualized raw field values (AT-Transformer, F1 0.4179 vs 0.4024). Coherence activates more of the LLM's pretrained knowledge.

## Why This Matters for the Thesis

This is the architectural decision that makes the whole approach possible. Without tabular-to-text, crash records are just rows of numbers — no LLM can do anything meaningful with them. The quality and design of the transformation directly affects model performance:
- Better normalization → fewer out-of-vocabulary terms → stronger embedding
- More relational context in the narrative → model can reason about multi-vehicle interactions
- LLM augmentation (CrashSage) → more consistent training signal, but adds a preprocessing inference cost

## Open Questions

- How sensitive is performance to template design? CrashSage notes alternative formats (bulleted, compressed, chronological) haven't been systematically evaluated.
- Does the transformation generalize across jurisdictions? Both papers use jurisdiction-specific lexicons; a cross-jurisdiction system would need a unified normalization layer.

## Related Concepts

- [[concepts/crash-severity-inference]] — the downstream task this transformation enables
- [[concepts/multimodal-crash-modeling]] — Tab-Text keeps tabular features alongside the narrative
- [[concepts/llm-domain-adaptation]] — CrashSage fine-tunes on the transformed narratives
