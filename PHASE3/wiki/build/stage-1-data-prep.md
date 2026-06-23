---
title: "Stage 1 — Data Prep"
type: build-stage
stage: 1
date: "2026-06-23"
tags: [phase3, build, data-prep]
---

# Stage 1 — Data Prep

## What this stage does

Cleans and joins the raw STATS19 tables into a single crash-level table, ready for spatial processing in Stage 2. Every row in the output is one crash with its location, vehicle type, severity weight, and year.

## Input

Raw STATS19 tables from data.gov.uk:
- `collisions` — one row per crash: accident_index, location (lat/lon), date, road conditions, lighting, weather
- `vehicles` — one row per vehicle involved: accident_index, vehicle_type
- `casualties` — one row per casualty: accident_index, casualty_severity

## Output

Single clean crash table: `accident_index`, `latitude`, `longitude`, `vehicle_type`, `severity_weight`, `accident_year`

---

## Build steps

**1. Download STATS19**
- Download all three tables for your chosen year range from data.gov.uk
- Recommended range: 2017–2022 (5 years; 1–4 = train, year 5 = holdout)
- Files come as CSVs

**2. Join tables**
- Join `collisions` + `vehicles` + `casualties` on `accident_index`
- One crash can involve multiple vehicles and multiple casualties — decide join logic:
  - Keep one row per vehicle involved (a crash with 2 vehicles = 2 rows, one per vehicle type)
  - This means a crash appears multiple times if multiple vehicle types were involved — that is correct, since each type's risk surface is built independently

**3. Assign severity weights**
- fatal = 3, serious = 2, slight = 1
- These weights are the standard from Gao 2024 and consistent with the literature
- Apply to the casualties table, then aggregate to crash level: sum of (severity_weight × number_of_casualties) per crash

**4. Tag vehicle type**
- STATS19 vehicle_type codes: car, motorcycle, HGV, LGV, bus, pedal cycle, other
- Map raw codes to your target type categories — decide which types to include
- Minimum set: car, motorcycle, HGV (the three with enough data for modelling)

**5. Filter**
- Keep only records with valid lat/lon (drop GPS-missing entries)
- Keep only your chosen year range
- Drop vehicle types you're not modelling (or keep as "other" category)

**6. Save**
- Output: one clean CSV — `crashes_clean.csv`

---

## Open questions

- **Year range**: 2017–2022 is a reasonable default but check data completeness per year before fixing it
- **Vehicle type grouping**: decide how granular — motorcycle vs powered-two-wheeler; rigid HGV vs articulated HGV; lump as HGV or split?
- **Multi-vehicle crashes**: if a crash involves both a motorcycle and an HGV, it appears in both type's training data. This is intentional — each type's risk surface is independent

---

## Tools

- pandas (join, filter, aggregate)
- No spatial tools needed yet — that's Stage 2

## Links

- [[build/system-overview]] — full pipeline context
- [[build/stage-2-segmentation]] — next stage (uses this output)
