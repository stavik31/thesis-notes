---
title: "Stage 2 — Segmentation"
type: build-stage
stage: 2
date: "2026-06-23"
tags: [phase3, build, segmentation]
---

# Stage 2 — Segmentation

## What this stage does

Divides the road network into segments (the nodes of the GNN graph) and assigns every crash from Stage 1 to its segment. Also builds the graph structure (which segments connect to which) and attaches traffic volume data from DfT AADF.

## Input

- `crashes_clean.csv` from Stage 1
- OS Open Roads network (geometry)
- DfT AADF traffic counts

## Output

- `segments.csv` — one row per segment: segment_id, road_class, speed_limit, length, AADF, geometry
- `crashes_segmented.csv` — crashes from Stage 1 with segment_id attached
- `graph_edges.csv` — which segment_ids connect at junctions (the graph structure for the GNN)

---

## Build steps

**1. Download OS Open Roads**
- Free from ordnancesurvey.co.uk (OS Open Data)
- Comes as a road network with road links and road nodes (junctions)
- Format: GeoPackage or Shapefile

**2. Define homogeneous segments**
- Adopted approach (Pathivada 2025 / HSM standard): cut road links where any of the following change — road class, speed limit, number of lanes, AADF
- In practice: OS Open Roads already breaks links at junctions; check whether speed limit and road class are consistent within each link. If not, split further
- Assign a unique segment_id to each resulting segment

**3. Build the graph edges**
- Two segments are connected (share an edge in the GNN graph) if they share a junction node in OS Open Roads
- Output: `graph_edges.csv` with columns segment_id_a, segment_id_b

**4. Map-match crashes to segments**
- For each crash (lat/lon), find the nearest segment using a spatial join (within a buffer tolerance — start with 25m)
- Assign the crash's segment_id
- Edge case: crashes that fall near a junction (equidistant from two segments) — assign to the segment whose road class and conditions better match the crash record's road conditions field

**5. Join AADF traffic counts**
- Download DfT AADF from roadtraffic.dft.gov.uk
- Spatially join each segment to the nearest DfT count point
- Assign that count point's AADF values (per vehicle type if available, aggregate otherwise)
- Segments with no count point within a threshold distance (e.g. 1km): use road-class-mean AADF as fallback
- Record which segments used the fallback — flag in the segment table

**6. Assemble segment feature table**
- For each segment: segment_id, road_class, speed_limit, length, AADF (total + per type if available), junction_count (number of connected segments), geometry centroid

**7. Save outputs**

---

## Open questions

- **Buffer tolerance for map-matching**: 25m is a starting point — check how many crashes fall outside and adjust
- **DfT AADF per-type availability**: check whether the downloaded data breaks down AADF by vehicle type at count-point level. If yes, use it directly. If not, use aggregate AADF and apply national type-share fractions as a proxy
- **Road network scope**: all of GB, or a specific region? Starting with a region (e.g. a single city or county) is sensible for the first build iteration before scaling up

---

## Tools

- geopandas (spatial join, geometry operations)
- shapely (buffer, nearest-feature search)
- NetworkX (build and store the graph structure)

## Links

- [[build/system-overview]] — full pipeline context
- [[build/stage-1-data-prep]] — previous stage (provides crash input)
- [[build/stage-3-gat-risk-model]] — next stage (consumes segment table + graph structure)
