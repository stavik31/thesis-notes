---
title: "STATS19"
type: entity
entity_type: dataset
tags: [dataset, thesis-core]
sources: []
last_updated: "2026-04-08"
---

## Overview

STATS19 is the UK Department for Transport's national road accident database, compiled from police-reported crashes across Great Britain. It is the primary dataset for this thesis. 5 years of data (~500,000–700,000 crash records) will be used.

## Structure

Three relational tables, joined on `accident_index`:

| Table | Equivalent in CrashSage | Key Contents |
|-------|-------------------------|--------------|
| `accidents` | Crash table | Date, time, location (LSOA, grid ref), road type, speed limit, junction detail, light conditions, weather, road surface |
| `vehicles` | Vehicle/Unit table | Vehicle type, manoeuvre, age/sex of driver, engine capacity, vehicle age |
| `casualties` | Person table | Casualty class (driver/passenger/pedestrian), severity, age, sex |

## Severity Classes

3-class: **Fatal (1) / Serious (2) / Slight (3)**

This differs from CrashSage's binary collapse (no/minor vs. serious/fatal). The decision of whether to mirror CrashSage's binary formulation or tackle 3-class prediction is a key thesis design decision. Extreme class imbalance expected: slight injuries dominate, fatals are rare (~1%).

## Key Differences from Papers' Datasets

| | STATS19 (this thesis) | WSDOT (CrashSage) | VicRoads (Tab-Text) |
|--|----------------------|-------------------|---------------------|
| Country | UK | USA (Washington) | Australia (Victoria) |
| Severity classes | 3 | 2 (binary) | 3 |
| Scale (5yr) | ~500k–700k | ~4,400 (downsampled) | ~292,000 |
| Speed units | mph / zones | mph | km/h |
| Road coding | UK-specific | US-specific | AU-specific |

The tabular-to-text transformation will need to be written from scratch for STATS19's schema — column names, value codes, and UK road/junction terminology all differ from CrashSage's Washington State implementation.

## Related

- [[concepts/tabular-to-text-transformation]] — pipeline to be built for this dataset
- [[concepts/crash-severity-inference]] — the task applied to this data
- [[wiki/progress/2026-04-08]] — session where dataset was confirmed
