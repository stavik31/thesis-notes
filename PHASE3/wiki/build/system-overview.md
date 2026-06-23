---
title: "System Build Overview"
type: build-overview
date: "2026-06-23"
tags: [phase3, thesis-core, build, route-planning]
---

# System Build Overview

## What the system does

A route planning system that recommends roads based on crash risk, conditioned on vehicle type. A motorcyclist and an HGV driver get different recommended routes for the same origin and destination, because the roads that are dangerous for motorcycles are not the same roads that are dangerous for HGVs. The system learns those type-specific risk patterns from historical crash data (STATS19), builds a risk map of the road network per vehicle type, and uses that map to score and rank routes.

---

## Two halves

**Offline** — done once, in advance. Take the full crash history, train the GAT on the road network, produce a risk score for every segment per vehicle type. Store the result. This is the expensive computation.

**Online** — when a user queries "route from A to B for a motorcycle," run Yen's k-shortest paths + MCDM ranking over the precomputed risk scores. Fast, because the hard work is already done.

The thesis is almost entirely about the offline half.

---

## Full pipeline

| Stage | Name | What it does |
|---|---|---|
| 1 | Data prep | Clean STATS19, join tables, severity-weight crashes, tag by vehicle type |
| 2 | Segmentation | Divide road network into segments, map-match crashes onto segments |
| 3 | GAT risk model | Train Graph Attention Network with type-conditioned attention to predict per-type crash risk |
| 4 | Risk surface filtering | Threshold GNN output to filter noise; CLQ post-hoc for spatial divergence maps |
| 5 | Routing | Yen's k-shortest paths + MCDM ranking on risk, time, distance per vehicle type |
| 6 | Evaluation | Validate risk model on holdout year; validate routing via counterfactual + Sarraf metrics |

---

## Data sources

| Source | What it provides | Where to get it |
|---|---|---|
| STATS19 | Crash records: location, vehicle type, severity, year | data.gov.uk |
| OS Open Roads | Road network geometry (segments, junctions) | ordnancesurvey.co.uk (free) |
| DfT AADF | Annual traffic volume by vehicle type at count points | roadtraffic.dft.gov.uk |

---

## AI architecture

**Stage 3 — Graph Attention Network (GAT) with vehicle-type embeddings**
- Road network as a graph: segments = nodes, junctions = edges
- Message passing captures spatial autocorrelation (neighbourhood context)
- Each vehicle type has a learned embedding vector
- Type embedding conditions the attention weights — model attends to different neighbourhood patterns per type
- Single unified model across all types (sparse types borrow strength from dense types through shared backbone)
- Training target: severity-weighted crash count per (segment, vehicle type, year)
- Key library: PyTorch Geometric (PyG)

---

## Key design decisions

| Decision | Choice | Rationale |
|---|---|---|
| Separate models per type vs unified | Unified GAT with type embeddings | Preserves cross-type relationships; sparse types borrow strength |
| Statistical significance gate vs ML | ML threshold on GNN output | GAT already does spatial smoothing; separate test is redundant |
| CLQ role | Post-hoc analysis only (not production gate) | Generates spatial divergence maps for results section |
| LLM explanation layer | Cut | Supervisor direction: faithfulness unsolvable in time, distracting to drivers |
| Reinforcement learning for routing | Not used | Poor fit for offline precomputed graph; Dijkstra/Yen's is correct tool |
| Tail risk (CVaR/mean-excess) | Decide during Stage 5 build | Needs real risk surface to evaluate whether it adds value |

---

## Evaluation approach

- **Risk model**: precision at top X% on holdout year (per vehicle type) — Gao 2024 metrics
- **Routing**: Spearman rank correlation, Average Overlap, DCG — Sarraf 2020 metrics
- **Headline**: counterfactual — does type-aware routing pass through fewer historical type-specific crash segments than shortest-path or aggregate routing?

---

## Links

- [[PLAN]] — reading plan and journal tiers
- [[positioning-memo]] — living thesis direction statement
- [[build/stage-3-gat-risk-model]] — the AI core
- [[build/stage-6-evaluation]] — full evaluation design
