---
title: "Stage 4 — Risk Surface Filtering"
type: build-stage
stage: 4
date: "2026-06-23"
tags: [phase3, build, filtering, significance]
---

# Stage 4 — Risk Surface Filtering

## What this stage does

Applies a threshold to the GAT risk surface to filter out low-signal cells, producing a clean filtered surface for the router. Separately, runs CLQ analysis as a post-hoc analysis tool to generate the spatial divergence maps that demonstrate the niche premise.

## Input

- `risk_scores.csv` from Stage 3 — (segment_id, vehicle_type, risk_score)

## Output

- `risk_surface_filtered.csv` — (segment_id, vehicle_type, risk_score) with low-signal cells zeroed out or set to aggregate fallback
- CLQ divergence maps (for results section, not the production pipeline)

---

## Why the GAT output earns this

The GAT has already done spatial reasoning through message passing. A segment with one random crash in a low-risk neighbourhood will score low because its neighbours don't support elevated risk. A genuine hotspot will score high because the surrounding network reinforces it. The threshold is drawn on an output that's already spatially contextualised — not on raw counts.

---

## Build steps

**Filtering (production pipeline)**

**1. Load risk scores**
- Load `risk_scores.csv`
- Group by vehicle_type

**2. Compute threshold per vehicle type**
- For each vehicle type independently, compute the Xth percentile of risk scores
- Start with top 15% (i.e. 85th percentile as threshold)
- This is a tuning parameter — revisit in Stage 6 evaluation

**3. Apply threshold**
- Cells above threshold: keep risk score as-is
- Cells below threshold: set to 0 (or to the aggregate risk score across all types as a fallback — decide which makes more sense for routing)

**4. Save filtered surface**
- Output: `risk_surface_filtered.csv`

---

**CLQ analysis (post-hoc, for results section)**

**5. Extract high-risk segments per type**
- For each vehicle type, take the flagged (above-threshold) segments from the filtered surface
- These are the candidate hotspots for that type

**6. Run CLQ per vehicle type**
- CLQ asks: do this type's crash hotspots cluster spatially more than chance?
- Method: Hu 2018 (Colocation Quotient) — Monte Carlo simulation, network-distance based
- Implementation: R package `spatstat` has CQ functions; alternatively implement directly in Python
- Run separately for motorcycle, HGV, car — produces a significance value per segment per type

**7. Map the results**
- Plot motorcycle high-risk segments vs HGV high-risk segments on the same map
- Compute overlap: what % of motorcycle hotspots are also HGV hotspots?
- Low overlap = the divergence holds at segment level on STATS19 — this is the headline niche result
- Lee 2018 showed this at TAZ/macro level on Florida; this confirms it at segment level on GB

---

## Open questions

- **Threshold percentile**: start with 15%, tune in Stage 6 based on routing evaluation results
- **Below-threshold fallback**: zero vs aggregate risk score — zero is cleaner for routing; aggregate fallback avoids completely unpenalised segments. Decide based on how Stage 5 handles zero-risk edges
- **CLQ implementation**: R (`spatstat`) is the path of least resistance; Python implementation is possible but more work

---

## Tools

- pandas, numpy (filtering)
- geopandas, matplotlib (mapping divergence results)
- R spatstat or Python custom implementation (CLQ)

## Key papers

- Hu 2018 (TR-C) — CLQ method (Colocation Quotient, Monte Carlo, network-distance)
- Lee 2018 (AAP) — spatial divergence by type at TAZ level; this stage replicates at segment level

## Links

- [[build/system-overview]] — full pipeline context
- [[build/stage-3-gat-risk-model]] — previous stage
- [[build/stage-5-routing]] — next stage (consumes filtered risk surface)
