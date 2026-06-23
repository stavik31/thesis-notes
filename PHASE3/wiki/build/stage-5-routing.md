---
title: "Stage 5 — Routing"
type: build-stage
stage: 5
date: "2026-06-23"
tags: [phase3, build, routing]
---

# Stage 5 — Routing

## What this stage does

Given an origin, destination, and vehicle type, generates candidate routes over the risk-weighted road network and ranks them by a combination of risk, time, and distance. The same O-D pair produces a different ranked list for different vehicle types because the edge weights (risk scores) differ per type.

## Input

- `risk_surface_filtered.csv` from Stage 4 — (segment_id, vehicle_type, risk_score)
- `segments.csv` from Stage 2 — segment lengths and speed limits (for time/distance calculation)
- `graph_edges.csv` from Stage 2 — graph structure
- User query: origin, destination, vehicle_type

## Output

- Ranked list of candidate routes, each with: route geometry, total risk score, estimated travel time, total distance

---

## Build steps

**1. Build the routing graph**
- Load the road network graph (segments as nodes, edges from `graph_edges.csv`)
- For a given vehicle type: assign the filtered risk score from `risk_surface_filtered.csv` as an edge weight on each segment
- Add travel time as a second edge attribute: `time = length / speed_limit`
- Use NetworkX to manage the graph

**2. Generate candidate routes (Yen's k-shortest paths)**
- For the queried origin and destination, run Yen's k-shortest paths algorithm
- k = 5 to 10 candidate routes (start with 5)
- "Shortest" here means lowest total risk score — Yen's finds the k best paths by risk weight
- NetworkX has a built-in implementation: `nx.shortest_simple_paths`
- Output: k candidate route sequences (lists of segment_ids)

**3. Score each candidate on three criteria**
- For each candidate route:
  - **Risk**: sum of risk scores across all segments on the route, weighted by segment length (`Σ risk_score_i × length_i`)
  - **Time**: sum of travel times across all segments (`Σ length_i / speed_limit_i`)
  - **Distance**: sum of segment lengths (`Σ length_i`)
- Normalise each criterion to [0, 1] across the k candidates so they're comparable

**4. Rank using MCDM**
- Method: AHP (Analytical Hierarchy Process) to set criterion weights + PROMETHEE to produce the final ranking
- Borrowed from Sarraf 2020
- AHP weights: reflect the relative importance of risk vs time vs distance — start with risk=0.6, time=0.3, distance=0.1 as a default; make these configurable
- PROMETHEE: pairwise comparison of candidates on each criterion, aggregated into a net flow score, ranked highest to lowest
- Output: ranked list of k routes

**5. Build query interface**
- A simple function or command-line call: `route(origin, destination, vehicle_type)` → returns ranked routes
- No front-end required — the thesis deliverable is the system, not an app

---

## Open questions

- **k value**: start with 5 candidate routes; check in Stage 6 whether increasing k changes the top-ranked result meaningfully
- **AHP weights**: risk=0.6, time=0.3, distance=0.1 is a reasonable starting default; consider making these user-configurable so a user can shift the balance (e.g. a delivery driver might weight time higher)
- **Mean-excess / CVaR routing (Mansoor 2026)**: instead of minimising total expected risk, minimise the worst-case tail risk along the route. Revisit this after the basic MCDM routing is working — decide based on whether tail risk is a meaningful distinction on your actual risk surface
- **Zero-risk edges**: segments below the Stage 4 threshold have zero risk score. In routing this means they're treated as equally safe — which is correct (they're not flagged as dangerous). Ensure Dijkstra/Yen's handles zero-weight edges correctly

---

## Tools

- NetworkX (`nx.shortest_simple_paths` for Yen's k-shortest paths)
- pandas, numpy (scoring and normalisation)
- Custom MCDM implementation (AHP + PROMETHEE — implement from Sarraf 2020 description)

## Key papers

- Sarraf & McGuire 2020 (ESWA) — MCDM router: Dijkstra + AHP/PROMETHEE; WCR risk score; Spearman/AO/DCG eval
- Mansoor, Li, Chen 2026 (TR-C) — class-specific route sets + mean-excess CVaR (optional extension)
- Chandra 2014 (TR-C) — Pareto/Yen's multi-objective routing machinery

## Links

- [[build/system-overview]] — full pipeline context
- [[build/stage-4-risk-surface-filtering]] — previous stage
- [[build/stage-6-evaluation]] — next stage
