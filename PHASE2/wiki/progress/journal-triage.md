---
title: "Journal Triage Log — Phase 2 Reading"
type: progress
date: "2026-06-09"
tags: [progress, literature-review, phase2]
---

# Journal Triage Log

Running record of the journal-by-journal reading sweep. One section per journal.
Workflow per journal: **search → shortlist titles → read abstracts (decide) → full
text for keepers only → deep-read + ingest.** Tags: `home` / `integration` /
`related-work` / `borrow` / `skip`.

See [[PHASE2/PLAN]] for the journal order and search terms.

---

## Tier 1

### IEEE T-ITS (#20) — ✅ complete (2026-06-09)

Searched on IEEE Xplore; titles triaged 2026-06-09. **Abstracts pulled for the shortlist
below; everything else from the result set skipped at title stage.**

| Status | Paper (year) | Tag | Why kept |
|---|---|---|---|
| ✅ abstract done | Leveraging Textual Description & Structured Data for Crash Risk of Traffic Violation — Multimodal (Li, Ma, Zhou, Lord, Zhang, 2025) | `related-work` | Closest methodological twin: text+tabular+LLM features for crash risk. Different purpose (violation classification vs. segment profiling) — must cite and position against. → **FULL TEXT** |
| ✅ abstract done | Driving Safety Risk Analysis & Assessment in Mixed Driving — Systematic Survey (Cheng et al., 2025) | `background` | AV/CAV-focused — less useful than expected. Skim for risk-assessment vocabulary only. → abstract only |
| ✅ abstract done | Automated & Explainable AI for Pedestrian Injury Severity (Antariksa, Tamakloe, Das, 2025) | `related-work`/`borrow` | Parallel to Phase 1 (XAI + severity); SHAP framing borrowable. → abstract only |
| ✅ abstract done | Vehicle-Group-Based Crash Risk Prediction & Interpretation (Zhu…Abdel-Aty, 2025) | `related-work` | Real-time trajectory data, too microscopic/off-path; cite Abdel-Aty as field anchor. → abstract only |
| ✅ abstract done | Safe Route Mapping of Roadways Using Multiple Sourced Data (Jiang et al., 2022) | `integration`/`home` | Best application anchor: segment-level SPF + heat maps + route/trip planning. Their gap = no condition-specificity, no NL — exactly where my method plugs in. → **FULL TEXT** |
| ✅ abstract done | In-Vehicle Warning Information Provision Strategy, V2V (Jo et al., 2022) | `related-work` | Tackles the when-to-warn / distraction problem directly; formal CDR/DFR/IPR framework useful for delivery argument. → abstract only |
| ✅ abstract done | Wasserstein GAN for Imbalanced Real-Time Crash Risk (Man, Quddus et al., 2022) | `borrow` | UK M1 data, same Fatal-class sparsity problem; WGAN method directly borrowable. Quddus = credible UK crash author. → abstract only |

**Skipped at title stage (off-layer — micro AV control / motion planning / driver-state):**
Driver-Oriented Active Intervention Control (2026); Perceptual Uncertainty-Aware Motion
Planning (2025); Risk-Informed Speed Limits (2024); Pedestrian-Vehicle Conflicts
probabilistic framework (2023); CAMV crash alarm (2023); Traffic-Simulation human-error
modeling (2023); Cooperative Vehicle Merging SAC (2023); Risk Representation in Lane-Change
Decision (2022); Attention-Based Lane Change Risk (2022); Probabilistic Risk Metric for
Highway Driving (2022); Driver Behavior Profiling (2022); Real-Time Cycle-Level Intersection
Risk (2021); Using Crash Databases for AV Maneuvers (2021); Forecasting
Habitual Driving Behaviors (2020); Cost-Sensitive Autoencoders imbalanced (2020).

**Decision after abstracts:** #1 (Multimodal) and #5 (Safe Route Mapping) → full text.
All others → abstract only. 2 keepers on merit — could be more or fewer for other journals.

**Outcome:** both full texts read 2026-06-09 and recorded in
`../../raw/papers/tier1_journal1/T-ITS-abstract-refs.md`. T-ITS sweep complete.
Sharpened gap: field does encode→predict (event-level, Li 2025) OR aggregate→score+map
(segment-level, Jiang 2022); neither condition-conditions nor explains *why* in NL. **Next
journal: Expert Systems with Applications.**

---

## Tier 1 — Journal 2: Expert Systems with Applications (#7) — ⏳ not started

Search terms: `crash severity prediction`, `road safety decision support`, `accident risk
machine learning`. Carry the test question: *is anyone doing condition-conditioned,
explanation-generating segment risk?*

---

## Links

- [[PHASE2/PLAN]] — journal order, tiers, search terms
- [[wiki/overview]] — Phase 2 thesis state
- [[wiki/progress/2026-06-09]] — Phase 2 kickoff
