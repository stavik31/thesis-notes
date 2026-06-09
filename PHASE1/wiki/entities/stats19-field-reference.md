---
title: "STATS19 Field Reference"
type: entity
entity_type: dataset
tags: [dataset, thesis-core, method]
sources: []
last_updated: "2026-04-09"
---

# STATS19 Field Reference

Detailed reference for the three DfT CSV files in `data/`. Written to support Step 1 of the [[progress/crashsage-replication-plan]]. The original data guide is `data/dft-road-casualty-statistics-road-safety-open-dataset-data-guide-2024.xlsx`.

---

## Dataset Overview

| File            | Rows    | What it contains                            |
| --------------- | ------- | ------------------------------------------- |
| `collision` CSV | 503,475 | One row per collision — the event itself    |
| `vehicle` CSV   | 920,692 | One row per vehicle involved in a collision |
| `casualty` CSV  | 640,522 | One row per person injured or killed        |

**Years covered:** 2020–2024 (5 years)

**Join keys:**
- `collision_index` links all three tables. It is a unique ID per collision, formed by concatenating `collision_year` + `collision_ref_no`.
- `vehicle_reference` (in vehicle and casualty tables) links a casualty to the specific vehicle they were in.
- So the hierarchy is: **1 collision → many vehicles → many casualties**.

**Encoding conventions:**
- `-1` always means "Data missing or out of range"
- `99` (or `9`) typically means "unknown / self-reported"
- `0` often means "not applicable" (e.g., `pedestrian_location = 0` for non-pedestrians)
- `_historic` suffix = field from the pre-2024 STATS19 specification; the modern equivalent drops the suffix. Use the modern field where available (more granular).

---

## Severity Distribution (the target variable)

This is the most important thing to understand about the data. Severity is recorded at both the collision level and the casualty level.

### Collision-level severity (`collision_severity`)

| Code | Label | Count | % of total |
|------|-------|-------|-----------|
| 1 | Fatal | 7,491 | 1.5% |
| 2 | Serious | 109,977 | 21.8% |
| 3 | Slight | 386,007 | 76.7% |
| **Total** | | **503,475** | |

**Key implication:** A collision is classified by its worst casualty. A collision with one fatal and five slight casualties is coded Fatal.

**For binary classification (CrashSage replication):** Collapse as:
- Class 0 → Slight (386,007)
- Class 1 → Fatal + Serious (117,468)

**Ratio:** ~3.3:1 (Slight vs. Serious+Fatal). Less extreme than the paper's 28:1, but still imbalanced enough to need stratified sampling.

**There is also `enhanced_severity_collision`** — a newer 5-level scale introduced in 2023 (Fatal, Very Serious, Moderately Serious, Less Serious, Slight). Only partially populated (many rows = -1). Not recommended for this thesis unless doing a 2023-only analysis.

---

## Collision Table Fields

These come from the police report and describe the scene *at the time of the collision*.

### Identity & Location
| Field | What it means |
|-------|---------------|
| `collision_index` | Primary key. Join to vehicle and casualty on this. |
| `collision_year` | Year (2020–2024) |
| `collision_ref_no` | Police reference number — not unique across years; use `collision_index` |
| `longitude`, `latitude` | GPS coordinates (null if unknown) |
| `location_easting_osgr`, `location_northing_osgr` | OS grid reference |
| `urban_or_rural_area` | 1=Urban, 2=Rural, 3=Unallocated |

### Time
| Field | What it means |
|-------|---------------|
| `date` | DD/MM/YYYY format |
| `day_of_week` | 1=Sunday, 2=Monday, ..., 7=Saturday |
| `time` | HH:MM (null if unknown) |

### Road & Infrastructure
| Field | What it means |
|-------|---------------|
| `first_road_class` | 1=Motorway, 2=A(M), 3=A, 4=B, 5=C, 6=Unclassified |
| `first_road_number` | Road number (0 if C/Unclassified — these have no number) |
| `road_type` | 1=Roundabout, 2=One-way, 3=Dual carriageway, 6=Single carriageway, 7=Slip road |
| `speed_limit` | 20/30/40/50/60/70 (mph). Valid values only. |
| `junction_detail` | Modern field: 0=Not at junction, 13=T/staggered, 16=Crossroads, 17=4+ arms, 18=Private entrance |
| `junction_detail_historic` | Older equivalent — use `junction_detail` if available |
| `junction_control` | 0=Not at junction, 1=Authorised person, 2=Auto signal, 3=Stop sign, 4=Give way/uncontrolled |
| `second_road_class` | Class of the intersecting road (0 = not at junction) |
| `pedestrian_crossing` | Modern field: 0=None within 50m, 11=School patrol, 13=Zebra, 14=Pelican/puffin, 15=Pedestrian signal |
| `special_conditions_at_site` | 0=None, 1=Signal out, 3=Road sign defective, 4=Roadworks, 5=Road surface defective |
| `carriageway_hazards` | Modern field: 0=None, 13=Roadworks, 16=Dislodged load, 21=Poor road surface, etc. |
| `trunk_road_flag` | 1=Trunk (Highways England), 2=Non-trunk |

### Environment
| Field | What it means |
|-------|---------------|
| `light_conditions` | 1=Daylight, 4=Darkness-lit, 5=Darkness-unlit, 6=Darkness-no lighting, 7=Darkness-lighting unknown |
| `weather_conditions` | 1=Fine, 2=Raining, 3=Snowing, 4=Fine+high winds, 5=Rain+high winds, 7=Fog/mist, 9=Unknown |
| `road_surface_conditions` | 1=Dry, 2=Wet/damp, 3=Snow, 4=Frost/ice, 5=Flood, 6=Oil/diesel, 7=Mud |

### Collision Summary
| Field | What it means |
|-------|---------------|
| `number_of_vehicles` | How many vehicles were involved |
| `number_of_casualties` | How many people were injured or killed |
| `collision_severity` | **Target variable.** 1=Fatal, 2=Serious, 3=Slight |
| `did_police_officer_attend_scene_of_accident` | 1=Yes, 2=No, 3=Self-reported form only |

### Fields to drop (not useful for narratives)
- `local_authority_district`, `local_authority_ons_district`, `local_authority_highway*` — bureaucratic geography codes, hundreds of values, no semantic value in narrative
- `lsoa_of_accident_location` — lower super output area code, not human-readable
- `collision_ref_no` — use `collision_index` instead
- `location_easting_osgr`, `location_northing_osgr` — redundant with lat/lon
- `enhanced_severity_collision` — mostly -1 (missing)
- `collision_injury_based`, `collision_adjusted_severity_*` — methodological bookkeeping fields, not crash characteristics

---

## Vehicle Table Fields

One row per vehicle in a collision. Multiple rows per `collision_index`.

### Identity
| Field | What it means |
|-------|---------------|
| `collision_index` | Join key to collision table |
| `vehicle_reference` | Identifies this specific vehicle within the collision. Used to join to casualty. |

### Vehicle Characteristics
| Field | What it means |
|-------|---------------|
| `vehicle_type` | 1=Pedal cycle, 2=Motorcycle ≤50cc, 3=Motorcycle ≤125cc, 4=Motorcycle 125–500cc, 5=Motorcycle >500cc, 8=Taxi, 9=Car, 10=Minibus, 11=Bus/coach, 17=Agricultural, 19=Van/goods ≤3.5t, 20=Goods 3.5–7.5t, 21=Goods ≥7.5t, 22=Mobility scooter, 23=Electric motorcycle |
| `towing_and_articulation` | 0=None, 1=Articulated, 3=Caravan, 4=Single trailer |
| `generic_make_model` | Vehicle make/model string (e.g. "BMW F 800"). Available from 2020. |
| `engine_capacity_cc` | Engine size in cc |
| `propulsion_code` | 1=Petrol, 2=Diesel, 3=Electric, 8=Hybrid, etc. |
| `age_of_vehicle` | Age in years |
| `vehicle_left_hand_drive` | 1=No, 2=Yes |

### Driver Characteristics
| Field | What it means |
|-------|---------------|
| `sex_of_driver` | 1=Male, 2=Female, 3=Not known |
| `age_of_driver` | Exact age in years |
| `age_band_of_driver` | 1=0–5, 2=6–10, ..., 4=16–20, 5=21–25, 6=26–35, 7=36–45, 8=46–55, 9=56–65, 10=66–75, 11=Over 75 |
| `journey_purpose_of_driver` | 1=Work journey, 2=Commuting, 7=Education, 8=Emergency (blue light), 9=Personal/leisure |
| `driver_imd_decile` | Deprivation decile of driver's home area (1=most deprived, 10=least deprived) |

### Manoeuvre & Movement
| Field | What it means |
|-------|---------------|
| `vehicle_manoeuvre` | Modern field: what the vehicle was doing. 1=Reversing, 2=Parked, 3=Waiting, 4=Slowing, 5=Moving off, 6=U-turn, 7=Turning left, 9=Turning right, 11–12=Lane change, 13–15=Overtaking, 19=Going ahead, 20=Parking |
| `vehicle_direction_from` | Direction vehicle was travelling from (1=N, 3=E, 5=S, 7=W etc.) |
| `vehicle_direction_to` | Direction vehicle was travelling to |
| `junction_location` | Where in relation to junction: 0=Not at junction, 1=Approaching, 3=Leaving roundabout, 4=Entering roundabout, 5=Leaving main road, 7=Slip road entry |
| `vehicle_location_restricted_lane` | Modern: 0=Main carriageway, 2=Bus lane, 4=Cycle lane, 9=Footway |

### Impact & Outcome
| Field | What it means |
|-------|---------------|
| `skidding_and_overturning` | 0=None, 1=Skidded, 2=Skidded+overturned, 3=Jackknifed, 5=Overturned |
| `hit_object_in_carriageway` | 0=None, 4=Parked vehicle, 7=Bollard, 10=Kerb, 11=Other object |
| `vehicle_leaving_carriageway` | 0=No, 1=Nearside, 4=Offside onto central res., 6=Crossed central res., 7=Offside |
| `hit_object_off_carriageway` | 0=None, 1=Road sign, 2=Lamp post, 4=Tree, 6=Crash barrier, 11=Wall/fence |
| `first_point_of_impact` | 0=No impact, 1=Front, 2=Back, 3=Offside, 4=Nearside |

---

## Casualty Table Fields

One row per injured or killed person. Multiple rows per `collision_index`.

### Identity
| Field | What it means |
|-------|---------------|
| `collision_index` | Join key to collision table |
| `vehicle_reference` | Which vehicle this casualty was in (join to vehicle table) |
| `casualty_reference` | Identifies this specific person within the collision |

### Who the Casualty Is
| Field | What it means |
|-------|---------------|
| `casualty_class` | 1=Driver/rider, 2=Passenger, 3=Pedestrian |
| `casualty_type` | Same categories as `vehicle_type` but describes the casualty's mode. 0=Pedestrian, 1=Cyclist, 9=Car occupant, etc. |
| `sex_of_casualty` | 1=Male, 2=Female |
| `age_of_casualty` | Exact age in years |
| `age_band_of_casualty` | Same banding as driver age |
| `casualty_imd_decile` | Deprivation decile of casualty's home area |

### Severity (casualty-level)
| Field | What it means |
|-------|---------------|
| `casualty_severity` | 1=Fatal, 2=Serious, 3=Slight — severity of **this specific person's injuries** |
| `enhanced_casualty_severity` | 5-level scale (2023+, mostly missing in earlier years) |

### Pedestrian-Specific
| Field | What it means |
|-------|---------------|
| `pedestrian_location` | 0=Not pedestrian, 1=On crossing, 5=In carriageway crossing elsewhere, 6=On footway/verge |
| `pedestrian_movement` | 0=Not pedestrian, 1=Crossing from nearside, 3=Crossing from offside, 7=Walking along road facing traffic |
| `pedestrian_road_maintenance_worker` | 0=No, 1=Yes |

### Passenger-Specific
| Field | What it means |
|-------|---------------|
| `car_passenger` | 0=Not car passenger, 1=Front seat, 2=Rear seat |
| `bus_or_coach_passenger` | 0=Not bus passenger, 1=Boarding, 2=Alighting, 3=Standing, 4=Seated |

---

## Recommended Field Selection

**Goal: understand causes of crashes and degree of contribution — not just predict severity.**

This changes the selection logic. Fields are split into three categories:

- **Narrative** — goes into the text narrative fed to the LLM
- **Metadata** — kept in the JSON record for analysis but not in the narrative text
- **Drop** — removed entirely

---

### Collision Table

| Field | Decision | Justification |
|---|---|---|
| `collision_index` | Metadata | Join key — must keep |
| `collision_severity` | Narrative | Target variable |
| `number_of_vehicles` | Narrative | Directly describes crash scale |
| `number_of_casualties` | Narrative | Directly describes crash scale |
| `date` | Narrative | Time context — seasonal patterns matter for causation |
| `day_of_week` | Narrative | Weekend/weekday is a known risk factor |
| `time` | Narrative | Rush hour, night driving — causal |
| `first_road_class` | Narrative | Motorway vs residential — causal |
| `first_road_number` | Metadata | Specific road identity; useful for spatial analysis even if not in narrative |
| `road_type` | Narrative | Roundabout vs dual carriageway — causal |
| `speed_limit` | Narrative | Strong causal factor for severity |
| `junction_detail` | Narrative | Junction type is a leading causal factor |
| `junction_control` | Narrative | Traffic signals vs uncontrolled — causal |
| `pedestrian_crossing` | Narrative | Presence/type of crossing affects pedestrian risk |
| `light_conditions` | Narrative | Darkness is a causal factor |
| `weather_conditions` | Narrative | Rain/fog/ice — causal |
| `road_surface_conditions` | Narrative | Wet/ice — causal |
| `special_conditions_at_site` | Narrative | Roadworks, signal failures — causal |
| `carriageway_hazards` | Narrative | Debris, poor surface — causal |
| `urban_or_rural_area` | Narrative | Speed environment proxy — causal |
| `longitude`, `latitude` | Metadata | Not in narrative but kept for spatial clustering analysis |
| `collision_year` | Drop | Redundant — already in `date` |
| `collision_ref_no` | Drop | Redundant — use `collision_index` |
| `location_easting_osgr`, `location_northing_osgr` | Drop | Redundant with lat/lon |
| `police_force` | Drop | Administrative — not causal |
| `local_authority_district`, `local_authority_ons_district`, `local_authority_highway`, `local_authority_highway_current` | Drop | Bureaucratic region codes — not human-readable, not causal |
| `second_road_class`, `second_road_number` | Drop | `junction_detail` already captures junction type; cross-street class adds marginal value |
| `junction_detail_historic` | Drop | Superseded by `junction_detail` |
| `pedestrian_crossing_human_control_historic`, `pedestrian_crossing_physical_facilities_historic` | Drop | Superseded by `pedestrian_crossing` |
| `carriageway_hazards_historic` | Drop | Superseded by `carriageway_hazards` |
| `trunk_road_flag` | Drop | Bureaucratic road management distinction — not causal |
| `did_police_officer_attend_scene_of_accident` | Drop | Administrative — not causal |
| `lsoa_of_accident_location` | Drop | Area code — not human-readable, not causal |
| `enhanced_severity_collision` | Drop | Mostly missing for pre-2023 records; can't use consistently across 5 years |
| `collision_injury_based`, `collision_adjusted_severity_serious`, `collision_adjusted_severity_slight` | Drop | DfT statistical corrections applied after the fact — not what happened, not causal |

---

### Vehicle Table

| Field | Decision | Justification |
|---|---|---|
| `collision_index` | Metadata | Join key |
| `vehicle_reference` | Metadata | Join key to casualty table |
| `vehicle_type` | Narrative | Motorcycle vs HGV vs car — strong causal factor |
| `towing_and_articulation` | Narrative | Towing affects handling — causal |
| `vehicle_manoeuvre` | Narrative | What the vehicle was doing — core causal factor |
| `vehicle_location_restricted_lane` | Narrative | Cycle lane, bus lane — relevant to cause |
| `junction_location` | Narrative | Where in the junction — causal |
| `skidding_and_overturning` | Narrative | Crash mechanics — causal |
| `hit_object_in_carriageway` | Narrative | What was hit — causal |
| `vehicle_leaving_carriageway` | Narrative | Crash mechanics — causal |
| `hit_object_off_carriageway` | Narrative | What was hit off-road — causal |
| `first_point_of_impact` | Narrative | Front/rear/side impact — causal |
| `sex_of_driver` | Narrative | Known risk factor in literature |
| `age_of_driver` | Narrative | Exact age preferred over band for causation analysis — finer resolution matters (17 vs 24 are different risk profiles) |
| `age_band_of_driver` | Drop | Redundant if keeping `age_of_driver` |
| `journey_purpose_of_driver` | Narrative | Commuting vs leisure vs emergency — causal |
| `propulsion_code` | Narrative | Electric vs petrol vs diesel — vehicle type context |
| `engine_capacity_cc` | Narrative | High-cc vehicles (motorcycles especially) are a distinct risk profile — causal |
| `age_of_vehicle` | Narrative | Older vehicles lack modern safety features — causal |
| `generic_make_model` | Metadata | Keep for analysis but too high-cardinality for narrative |
| `driver_imd_decile` | Metadata | Deprivation is a real contributing factor (older vehicles, higher-risk roads, night driving). Keep as metadata for analysis — conscious decision not to include in narrative to avoid the model learning to weight poverty as a crash cause. |
| `driver_distance_banding` | Metadata | Fatigue proxy — keep if populated, don't force into narrative |
| `collision_year`, `collision_ref_no` | Drop | Redundant |
| `vehicle_manoeuvre_historic` | Drop | Superseded by `vehicle_manoeuvre` |
| `vehicle_location_restricted_lane_historic` | Drop | Superseded by modern field |
| `journey_purpose_of_driver_historic` | Drop | Superseded by modern field |
| `vehicle_direction_from`, `vehicle_direction_to` | Drop | Compass bearing — not causal for severity or cause |
| `vehicle_left_hand_drive` | Drop | Almost always "No" in UK data — effectively a constant |
| `lsoa_of_driver` | Drop | Home area code — not causal |
| `escooter_flag` | Drop | Covered by `vehicle_type` — redundant |

---

### Casualty Table

| Field | Decision | Justification |
|---|---|---|
| `collision_index` | Metadata | Join key |
| `vehicle_reference` | Metadata | Join key |
| `casualty_reference` | Metadata | Identifies individual casualties |
| `casualty_class` | Narrative | Driver / passenger / pedestrian — fundamentally different risk profiles |
| `casualty_type` | Narrative | Cyclist, car occupant, pedestrian — causal |
| `sex_of_casualty` | Narrative | Known risk factor |
| `age_of_casualty` | Narrative | Same reasoning as `age_of_driver` — exact age preferred for causation analysis |
| `age_band_of_casualty` | Drop | Redundant if keeping `age_of_casualty` |
| `casualty_severity` | Narrative | Person-level outcome — mask from SFT loss |
| `pedestrian_location` | Narrative | On crossing vs in carriageway vs on footway — causal for pedestrian crashes |
| `pedestrian_movement` | Narrative | Crossing direction, walking along road — causal |
| `car_passenger` | Narrative | Front vs rear seat — causal for injury severity |
| `bus_or_coach_passenger` | Narrative | Standing vs seated — causal |
| `casualty_imd_decile` | Metadata | Same reasoning as `driver_imd_decile` — keep for analysis, not narrative |
| `casualty_distance_banding` | Drop | Sparsely populated, low causal value |
| `pedestrian_road_maintenance_worker` | Drop | Almost always "No" — effectively a constant |
| `lsoa_of_casualty` | Drop | Home area code — not causal |
| `enhanced_casualty_severity` | Drop | Mostly missing for pre-2023 records |
| `casualty_injury_based`, `casualty_adjusted_severity_serious`, `casualty_adjusted_severity_slight` | Drop | DfT statistical corrections — not what happened |

---

## Links

- [[entities/stats19]] — overview of the STATS19 dataset
- [[progress/crashsage-replication-plan]] — replication plan that uses this data
- [[concepts/tabular-to-text-transformation]] — how these fields become narratives
- [[concepts/crash-severity-inference]] — the prediction task using `collision_severity`
