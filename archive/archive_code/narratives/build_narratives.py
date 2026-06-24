"""
Regenerates narratives_raw.jsonl from output.jsonl with:
  - 5 grammar fixes (vehicle count, article agreement, weather phrasing)
  - 3-class labels (Slight / Serious / Fatal) instead of binary (Minor / Serious)

Run: python3 build_narratives.py
"""

import json
from pathlib import Path

DIR = Path(__file__).parent


# ── Helpers ───────────────────────────────────────────────────────────────────

MISSING = {
    "Data missing or out of range", "Undefined",
    "Not known", "Not known or not requested",
}

def is_missing(val):
    if val is None: return True
    if isinstance(val, str) and val in MISSING: return True
    if val == -1: return True
    return False

def article(word):
    """'an' before vowel sound, 'a' otherwise."""
    return "an" if str(word)[0].lower() in "aeiou" else "a"

def age_article(age):
    s = str(age)
    if s[0] == "8": return "an"
    if s in ("11", "18"): return "an"
    return "a"

def fix_weather(s):
    """Fix raw STATS19 label missing 'with'."""
    return s.replace("no high winds", "with no high winds")


# ── Block builders ────────────────────────────────────────────────────────────

def block1_scene(r):
    n = r["number_of_vehicles"]
    # FIX 1: proper singular/plural instead of "vehicle(s)"
    vehicle_str = "1 vehicle" if n == 1 else f"{n} vehicles"
    # FIX 2: article agrees with "urban" / "rural" (urban needs "an")
    area = r["urban_or_rural_area"].lower()
    art = article(area)
    return (
        f"On {r['date']}, a {r['day_of_week']} at {r['time']}, "
        f"a collision involving {vehicle_str} occurred in {art} {area} area."
    )


def block2_road(r):
    road_type = r["road_type"].lower()
    road_class = r["first_road_class"]
    road_class_display = road_class.lower() if len(road_class) > 1 else road_class

    # FIX 3: article must agree with road_type (first word after "on"),
    # not road_class — "on a single carriageway unclassified road" not "on an single..."
    art = article(road_type)

    jd = r.get("junction_detail", "")
    if is_missing(jd) or jd == "Not at junction or within 20 metres":
        junction = "The collision was not at or within 20 metres of a junction"
    else:
        junction = f"The collision occurred at a {jd}"

    jc = r.get("junction_control", "")
    junction_control_clause = ""
    if not is_missing(jc):
        junction_control_clause = f" Junction control: {jc}."

    road_sentence = (
        f"The accident took place on {art} {road_type} {road_class_display} road "
        f"with a {r['speed_limit']}mph speed limit. {junction}.{junction_control_clause}"
    )

    # FIX 4: weather — insert missing "with" in "Fine no high winds"
    weather = fix_weather(r["weather_conditions"].lower())

    conditions = (
        f"Lighting conditions at the time of the collision were {r['light_conditions'].lower()}. "
        f"Weather conditions were {weather}. "
        f"The road surface was {r['road_surface_conditions'].lower()}."
    )

    extras = []
    sc = r.get("special_conditions_at_site")
    if sc and sc != 0 and not is_missing(sc):
        extras.append(f"Special conditions at the site included {str(sc).lower()}.")
    ch = r.get("carriageway_hazards")
    if ch and ch != 0 and not is_missing(ch):
        extras.append(f"A carriageway hazard was present ({str(ch).lower()}).")

    return " ".join([road_sentence, conditions] + extras)


def block3_vehicle(i, v):
    sentences = []

    towing = v.get("towing_and_articulation", "")
    if not is_missing(towing) and towing != "No tow/articulation":
        sentences.append(f"Vehicle {i} was a {v['vehicle_type']}, towing {towing}.")
    else:
        sentences.append(f"Vehicle {i} was a {v['vehicle_type']}.")

    manoeuvre = v.get("vehicle_manoeuvre", "")
    if isinstance(manoeuvre, str) and not is_missing(manoeuvre):
        sentences.append(f"The vehicle was {manoeuvre.lower()}.")

    skid = v.get("skidding_and_overturning", 0)
    if skid and not is_missing(skid):
        sentences.append(f"The vehicle {str(skid).lower()}.")

    leaving = v.get("vehicle_leaving_carriageway", "")
    if not is_missing(leaving) and isinstance(leaving, str) and leaving != "Did not leave carriageway":
        sentences.append(f"The vehicle left the carriageway on the {leaving.lower()}.")

    obj_off = v.get("hit_object_off_carriageway", 0)
    if obj_off and not is_missing(obj_off):
        sentences.append(f"It struck {article(obj_off)} {str(obj_off).lower()} off the carriageway.")

    obj_in = v.get("hit_object_in_carriageway", 0)
    if obj_in and not is_missing(obj_in):
        sentences.append(f"It struck {article(obj_in)} {str(obj_in).lower()} in the carriageway.")

    impact = v.get("first_point_of_impact", "")
    if not is_missing(impact) and isinstance(impact, str) and impact != "Did not impact":
        sentences.append(f"The first point of impact was the {impact.lower()} of the vehicle.")

    age = v.get("age_of_driver")
    sex = v.get("sex_of_driver", "")
    if not is_missing(age) and not is_missing(sex) and isinstance(sex, str):
        # FIX 5: use age_article for correct "an 18-year-old" etc.
        sentences.append(f"The driver was {age_article(age)} {age}-year-old {sex.lower()}.")

    return " ".join(sentences)


def block4_casualties(vehicles):
    casualties = [c for v in vehicles for c in v.get("casualties", [])]
    if not casualties:
        return None

    n = len(casualties)
    sentences = [f"The collision involved {n} {'casualty' if n == 1 else 'casualties'}."]

    for c in casualties:
        age   = c.get("age_of_casualty", "")
        sex   = c.get("sex_of_casualty", "")
        cls   = c.get("casualty_class", "")
        ctype = c.get("casualty_type", "")
        passenger = c.get("car_passenger", "")

        passenger_clause = ""
        if not is_missing(passenger) and passenger != "Not car passenger":
            passenger_clause = f", seated as {passenger.lower()}"

        art = age_article(age) if str(age).isdigit() else "a"
        sentences.append(
            f"{art.capitalize()} {age}-year-old {sex.lower()} {cls.lower()} "
            f"({ctype.lower()}{passenger_clause}) was involved in the collision."
        )

    return " ".join(sentences)


def crash_to_narrative(record):
    parts = [
        block1_scene(record),
        block2_road(record),
        *[block3_vehicle(i, v) for i, v in enumerate(record["vehicles"], 1)],
    ]
    casualties = block4_casualties(record["vehicles"])
    if casualties:
        parts.append(casualties)
    return "\n\n".join(parts)


# ── Main ──────────────────────────────────────────────────────────────────────

def build(input_path, output_path):
    total = 0
    with open(input_path) as f_in, open(output_path, "w") as f_out:
        for line in f_in:
            record = json.loads(line)
            narrative = crash_to_narrative(record)
            # 3-class label: Slight / Serious / Fatal (no binary collapse)
            label = record["collision_severity"]
            json.dump({
                "collision_index": record["collision_index"],
                "narrative": narrative,
                "label": label,
            }, f_out)
            f_out.write("\n")
            total += 1
            if total % 50000 == 0:
                print(f"  {total:,} records processed")

    print(f"Done — {total:,} narratives written to {output_path}")


if __name__ == "__main__":
    build(DIR / "output.jsonl", DIR / "narratives_raw.jsonl")
