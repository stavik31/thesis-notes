---
title: "How to implement tabular-to-text transformation for STATS19?"
type: query
date: "2026-04-24"
tags: [method, thesis-core, data-preprocessing]
---

# How to implement tabular-to-text transformation for STATS19?

Context: the STATS19 data has been joined into a nested JSONL (one record per collision, with embedded vehicle and casualty arrays). The semantic codes are already decoded into human-readable strings. The task is to write a Python function that converts each record into a natural language narrative suitable for LLM fine-tuning.

Related pages: [[concepts/tabular-to-text-transformation]], [[progress/crashsage-replication-plan]], [[entities/stats19]]

---

## The Core Task

Phase 1 (semantic normalization) is already done — STATS19 values are already strings like `"Darkness - no lighting"` rather than integer codes. What remains is Phase 2: **template-based generation**. This means writing one Python function:

```
crash_to_narrative(record: dict) -> str
```

The function takes a merged crash record and returns a single narrative string. The severity label lives in a **separate field** in the output JSONL — never embedded in the narrative text. The output record format is:

```
{"narrative": "On 22/05/2021...", "label": "Slight"}
```

This separation is critical. During SFT, the model is given the narrative as the prompt and the label as the completion. If the severity appears inside the narrative, the model learns to copy it rather than reason about it.

---

## Narrative Structure: Four Blocks

The narrative is assembled in four sequential blocks. Each block is one or two sentences. The ordering matters — it follows the logical sequence of a crash event.

```
Block 1: Scene setting      ← when, where, how many involved
Block 2: Road + conditions  ← the physical context
Block 3: Vehicles           ← what each vehicle did (one paragraph per vehicle)
Block 4: Casualties         ← who was in the vehicles (not their injury severity)
```

The outcome (collision_severity) is the label — it does NOT appear in the narrative.

---

## Sentence-Level Templates

### Block 1 — Scene Setting

```
"On {date}, a {day_of_week} at {time}, a collision involving {number_of_vehicles} vehicle(s) occurred in a {urban_or_rural_area} area."
```

Example output:
> On 22/05/2021, a Saturday at 22:44, a collision involving 2 vehicles occurred in a rural area.

Notes:
- Use `number_of_vehicles` from the collision record (not a count of the vehicles array — they match but the field is cleaner).
- Do not include coordinates (longitude/latitude) — they carry no semantic content for the LLM.

---

### Block 2 — Road and Environmental Conditions

This block has two sentences: one for the road, one for conditions.

**Road sentence:**
```
"The accident took place on a {road_type} {first_road_class} road with a {speed_limit}mph speed limit. {junction_sentence}."
```

Junction sentence mapping:
- `"Not at junction or within 20 metres"` → `"The collision was not at or within 20 metres of a junction."`
- Anything else → `"The collision occurred at a {junction_detail}."`

If `junction_control` is informative (not "Data missing or out of range"), append: `"Junction control: {junction_control}."`

**Conditions sentence:**
```
"At the time of the collision, {light_conditions}. Weather conditions were {weather_conditions}. The road surface was {road_surface_conditions}."
```

Only add if non-zero / informative:
- `special_conditions_at_site` → `"Special site conditions: {value}."`
- `carriageway_hazards` → `"Carriageway hazard: {value}."`

Example output:
> The accident took place on an unclassified single carriageway road with a 60mph speed limit. The collision was not at or within 20 metres of a junction.
>
> At the time of the collision, darkness — no lighting. Weather conditions were fine with no high winds. The road surface was dry.

---

### Block 3 — Vehicles

One paragraph per vehicle. Loop over the vehicles array. For each vehicle:

```
"Vehicle {n} was a {vehicle_type}{towing_clause}. The vehicle was {vehicle_manoeuvre}.
{skid_clause} {leave_clause} {object_off_clause} {object_in_clause} {impact_clause}
{driver_clause}"
```

Clause rules — only include clause if condition is met:

| Clause | Include if | Template |
|---|---|---|
| `towing_clause` | `towing_and_articulation` ≠ "No tow/articulation" | `", towing {value}"` |
| `skid_clause` | `skidding_and_overturning` ≠ 0 and ≠ "Did not" | `"The vehicle {skidding_and_overturning}."` |
| `leave_clause` | `vehicle_leaving_carriageway` ≠ "Did not leave carriageway" | `"The vehicle left the carriageway on the {value}."` |
| `object_off_clause` | `hit_object_off_carriageway` ≠ 0 | `"It struck {value} off the carriageway."` |
| `object_in_clause` | `hit_object_in_carriageway` ≠ 0 | `"It struck {value} in the carriageway."` |
| `impact_clause` | `first_point_of_impact` ≠ "Did not impact" | `"The first point of impact was the {value} of the vehicle."` |
| `driver_clause` | `age_of_driver` ≠ "Data missing or out of range" and ≠ -1 | `"The driver was a {age_of_driver}-year-old {sex_of_driver}."` |

If a vehicle has no impact, no leaving of carriageway, and no meaningful crash detail, write:
```
"Vehicle {n} was a {vehicle_type} travelling {vehicle_manoeuvre} and reported no impact."
```

Example output for Vehicle 1 (the involved vehicle):
> Vehicle 1 was a car. The vehicle was going ahead. The vehicle overturned and left the carriageway on the nearside. It struck a tree off the carriageway. The first point of impact was the front of the vehicle. The driver was a 30-year-old female.

Example output for Vehicle 2 (the uninvolved vehicle):
> Vehicle 2 was a car travelling straight ahead and reported no impact.

---

### Block 4 — Casualties

One sentence per casualty. Loop over all casualties across all vehicles (the nested `casualties` array inside each vehicle). Do **not** include `casualty_severity` — that is the label.

```
"A {age_of_casualty}-year-old {sex_of_casualty} {casualty_class} ({casualty_type}{passenger_clause}) was involved in the collision."
```

Passenger clause: only include if `car_passenger` ≠ "Not car passenger":
```
", seated as {car_passenger}"
```

Open the block with a header sentence:
```
"The collision involved {number_of_casualties} casualty/casualties."
```

Example output:
> The collision involved 2 casualties. A 30-year-old female driver or rider (car occupant) was involved in the collision. A 30-year-old male passenger (car occupant, seated as front seat passenger) was involved in the collision.

---

## Complete Example Narrative

For the example record (collision index 2021170H10421):

> On 22/05/2021, a Saturday at 22:44, a collision involving 2 vehicles occurred in a rural area.
>
> The accident took place on an unclassified single carriageway road with a 60mph speed limit. The collision was not at or within 20 metres of a junction.
>
> At the time of the collision, darkness — no lighting. Weather conditions were fine with no high winds. The road surface was dry.
>
> Vehicle 1 was a car. The vehicle was going ahead. The vehicle overturned and left the carriageway on the nearside. It struck a tree off the carriageway. The first point of impact was the front of the vehicle. The driver was a 30-year-old female.
>
> Vehicle 2 was a car travelling straight ahead and reported no impact.
>
> The collision involved 2 casualties. A 30-year-old female driver or rider (car occupant) was involved in the collision. A 30-year-old male passenger (car occupant, seated as front seat passenger) was involved in the collision.

**Label (separate field):** `Slight`

---

## Field Skip List

These fields should never appear in the narrative:

| Field | Reason |
|---|---|
| `collision_index`, `vehicle_reference`, `casualty_reference` | Internal join keys — meaningless to LLM |
| `longitude`, `latitude` | Raw coordinates carry no semantic content |
| `first_road_number` | STATS19 artifact: contains a prose explanation string for unclassified roads, not a road number |
| Any field = `"Data missing or out of range"` | Uninformative null — skip the field entirely, do not write "unknown" |
| Any field = `-1` | Same as above (numeric null encoding in STATS19) |
| Any field = `"Undefined"` | Same (e.g. `propulsion_code`) |
| `vehicle_location_restricted_lane` | Default value ("on main carriageway") applies to virtually all records — uninformative |
| `junction_location` (vehicle-level) | Covered at collision level already |
| `pedestrian_location`, `pedestrian_movement` = "Not a Pedestrian" | Uninformative for non-pedestrian casualties |
| `bus_or_coach_passenger` = "Not a bus or coach passenger" | Uninformative default |
| `journey_purpose_of_driver` = "Not known or not requested" | Uninformative |
| `driver_imd_decile`, `casualty_imd_decile`, `driver_distance_banding` | Deprivation indices — mostly missing, and not in the CrashSage feature set |
| `engine_capacity_cc` | Mostly missing |
| `casualty_severity` | **This is outcome data — label leakage risk. Exclude entirely.** |

Indicator fields set to `0` (only include when non-zero):
- `skidding_and_overturning`
- `hit_object_in_carriageway`
- `hit_object_off_carriageway`
- `special_conditions_at_site`
- `carriageway_hazards`

---

## Output JSONL Format

Each line of your output file should be:

```json
{
  "collision_index": "2021170H10421",
  "narrative": "On 22/05/2021, a Saturday at 22:44...",
  "label": "Slight"
}
```

Keep `collision_index` for traceability — you'll need it later when computing gradient attribution scores per record and when debugging mis-classified crashes.

---

## Label Decision: 3-Class vs Binary

For strict CrashSage replication, **collapse to binary first**:
- `Slight` → `"Minor"`
- `Serious` or `Fatal` → `"Serious"`

Then run 3-class (`Slight` / `Serious` / `Fatal`) as a follow-up experiment. This is documented as a tracked deviation in [[progress/crashsage-replication-plan]].

---

## Implementation Order

1. Write the function with hardcoded block order and clause rules above.
2. Test it on 5–10 records manually. Verify the output reads like natural English — if a sentence sounds broken, find the field causing it and add it to the skip list or rewrite the clause.
3. Run across the full dataset. Check narrative length distribution — any record exceeding ~400 words warrants inspection (the paper's 2048-token max is generous, but very long narratives suggest a data anomaly).
4. Before augmentation (Step 5 of the replication plan): write the raw template narratives to `narratives_raw.jsonl`. You'll want to compare raw vs. augmented later.

---

## Links

- [[concepts/tabular-to-text-transformation]] — the general theory and design choices behind this step
- [[progress/crashsage-replication-plan]] — where this step sits in the overall pipeline (Step 3)
- [[entities/stats19]] — the source dataset
- [[entities/stats19-field-reference]] — field definitions and code mappings for STATS19
- [[concepts/crash-severity-inference]] — the downstream prediction task this narrative feeds
- [[concepts/llm-domain-adaptation]] — the fine-tuning step that consumes these narratives

        import json


def is_missing(val):
    if val is None:
        return True
    if isinstance(val, str) and val in (
        "Data missing or out of range",
        "Undefined",
        "Not known",
        "Not known or not requested",
    ):
        return True
    if val == -1:
        return True
    return False


def junction_sentence(record):
    jd = record.get("junction_detail", "")
    if is_missing(jd) or jd == "Not at junction or within 20 metres":
        return "The collision was not at or within 20 metres of a junction"
    return f"The collision occurred at {jd.lower()}"


def vehicle_sentence(i, v):
    sentences = []

    towing = v.get("towing_and_articulation", "")
    if not is_missing(towing) and towing != "No tow/articulation":
        sentences.append(f"Vehicle {i} was a {v['vehicle_type']}, towing {towing}.")
    else:
        sentences.append(f"Vehicle {i} was a {v['vehicle_type']}.")

    sentences.append(f"The vehicle was {v['vehicle_manoeuvre'].lower()}.")

    skid = v.get("skidding_and_overturning", 0)
    if skid and not is_missing(skid):
        sentences.append(f"The vehicle {str(skid).lower()}.")

    leaving = v.get("vehicle_leaving_carriageway", "")
    if not is_missing(leaving) and leaving != "Did not leave carriageway":
        sentences.append(
            f"The vehicle left the carriageway on the {leaving.lower()}."
        )

    obj_off = v.get("hit_object_off_carriageway", 0)
    if obj_off and not is_missing(obj_off):
        sentences.append(f"It struck {str(obj_off).lower()} off the carriageway.")

    obj_in = v.get("hit_object_in_carriageway", 0)
    if obj_in and not is_missing(obj_in):
        sentences.append(f"It struck {str(obj_in).lower()} in the carriageway.")

    impact = v.get("first_point_of_impact", "")
    if not is_missing(impact) and impact != "Did not impact":
        sentences.append(
            f"The first point of impact was the {impact.lower()} of the vehicle."
        )

    age = v.get("age_of_driver")
    sex = v.get("sex_of_driver", "")
    if not is_missing(age) and not is_missing(sex):
        sentences.append(f"The driver was a {age}-year-old {sex.lower()}.")

    return " ".join(sentences)


def flatten_casualties(vehicles):
    all_casualties = []
    for v in vehicles:
        all_casualties.extend(v.get("casualties", []))
    return all_casualties


def casualty_summary(casualties):
    n = len(casualties)
    header = f"The collision involved {n} {'casualty' if n == 1 else 'casualties'}."
    sentences = [header]

    for c in casualties:
        age = c.get("age_of_casualty", "")
        sex = c.get("sex_of_casualty", "")
        cls = c.get("casualty_class", "")
        ctype = c.get("casualty_type", "")
        passenger = c.get("car_passenger", "")

        passenger_clause = ""
        if not is_missing(passenger) and passenger != "Not car passenger":
            passenger_clause = f", seated as {passenger.lower()}"

        sentences.append(
            f"A {age}-year-old {sex.lower()} {cls.lower()} "
            f"({ctype}{passenger_clause}) was involved in the collision."
        )

    return " ".join(sentences)


def crash_to_narrative(record):
    parts = []

    # Block 1: Scene
    parts.append(
        f"On {record['date']}, a {record['day_of_week']} at {record['time']}, "
        f"a collision involving {record['number_of_vehicles']} vehicle(s) "
        f"occurred in a {record['urban_or_rural_area']} area."
    )

    # Block 2: Road + conditions
    road_sentence = (
        f"The accident took place on a {record['first_road_class'].lower()} "
        f"{record['road_type'].lower()} with a {record['speed_limit']}mph speed limit. "
        f"{junction_sentence(record)}."
    )

    conditions = (
        f"At the time of the collision, {record['light_conditions'].lower()}. "
        f"Weather conditions were {record['weather_conditions'].lower()}. "
        f"The road surface was {record['road_surface_conditions'].lower()}."
    )

    extras = []
    if record.get("special_conditions_at_site") and record["special_conditions_at_site"] != 0:
        extras.append(f"Special conditions: {record['special_conditions_at_site']}.")

    if record.get("carriageway_hazards") and record["carriageway_hazards"] != 0:
        extras.append(f"Carriageway hazard: {record['carriageway_hazards']}.")

    parts.append(" ".join([road_sentence, conditions] + extras))

    # Block 3: Vehicles
    for i, v in enumerate(record["vehicles"], 1):
        parts.append(vehicle_sentence(i, v))

    # Block 4: Casualties
    all_casualties = flatten_casualties(record["vehicles"])
    if all_casualties:
        parts.append(casualty_summary(all_casualties))

    return "\n\n".join(parts)


# --- Output to JSONL ---


def process_records(input_path, output_path, binary=True):
    with open(input_path) as f_in, open(output_path, "w") as f_out:
        for line in f_in:
            record = json.loads(line)
            narrative = crash_to_narrative(record)

            severity = record["collision_severity"]
            label = "Minor" if severity == "Slight" else "Serious" if binary else severity

            out = {
                "collision_index": record["collision_index"],
                "narrative": narrative,
                "label": label,
            }

            json.dump(out, f_out)
            f_out.write("\n")                                                                                                                                                                                                                              
  Three things to pay attention to as you read through it:                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                        
  1. is_missing — called everywhere. If you find a value in your data that should be skipped but isn't caught here, add it to that one function and it fixes it everywhere.                                                                                             
  2. skidding_and_overturning in vehicle_sentence — in your data this is sometimes a string ("Overturned") and sometimes 0. The if skid and not is_missing(skid) handles both: 0 is falsy so it's skipped, the string passes through.
  3. binary=True in process_records — start with this. Flip to False when you run the 3-class experiment later.     