import pandas as pd
from pathlib import Path

# --- Paths ---
# ROOT points two levels up from this file to the code/ directory.
# All input and output paths are derived from it so the script works regardless
# of where it is called from.
ROOT = Path(__file__).parent.parent  # code/
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

COLLISIONS_FILE = DATA_DIR / "dft-road-casualty-statistics-collision-last-5-years.csv"
VEHICLES_FILE   = DATA_DIR / "dft-road-casualty-statistics-vehicle-last-5-years.csv"
CASUALTIES_FILE = DATA_DIR / "dft-road-casualty-statistics-casualty-last-5-years.csv"

OUTPUT_FILE = OUTPUT_DIR / "crashes_clean.csv"

# --- Constants ---
# We train on 2020–2023 and hold out 2024 for evaluation. Both years are kept
# in this file; the split happens in Stage 3.
YEAR_RANGE = (2020, 2024)

# DfT severity codes: 1=Fatal, 2=Serious, 3=Slight.
# We convert each casualty to a weight so that one fatal crash outweighs several
# slight ones when scoring a segment's risk. These weights are borrowed from Gao 2024.
SEVERITY_WEIGHTS = {1: 3, 2: 2, 3: 1}

# DfT publishes ~100 vehicle_type codes. We collapse them into 5 categories that
# are dense enough in STATS19 to build stable per-type risk surfaces.
# Codes not listed here (buses, agricultural vehicles, etc.) are dropped.
VEHICLE_TYPE_MAP = {
    1:  "cycle",        # pedal cycle
    2:  "motorcycle",   # 50cc and under
    3:  "motorcycle",   # 125cc and under
    4:  "motorcycle",   # 125cc–500cc
    5:  "motorcycle",   # over 500cc
    23: "motorcycle",   # electric motorcycle
    97: "motorcycle",   # unknown cc
    8:  "car",          # taxi/private hire
    9:  "car",          # car
    19: "lgv",          # van / goods up to 3.5t
    20: "hgv",          # goods 3.5t–7.5t
    21: "hgv",          # goods 7.5t and over
    98: "hgv",          # goods unknown weight
}


def load_tables():
    # STATS19 is published as three separate tables that must be joined:
    #   collisions — one row per crash event, with location (lat/lon)
    #   vehicles   — one row per vehicle involved, with vehicle type
    #   casualties — one row per person injured, with injury severity
    # We only load the columns we actually need to keep memory low.
    print("Loading tables...")
    collisions = pd.read_csv(
        COLLISIONS_FILE,
        usecols=["collision_index", "collision_year", "longitude", "latitude"]
    )
    vehicles = pd.read_csv(
        VEHICLES_FILE,
        usecols=["collision_index", "vehicle_type"]
    )
    casualties = pd.read_csv(
        CASUALTIES_FILE,
        usecols=["collision_index", "casualty_severity"]
    )
    print(f"  collisions: {len(collisions):,}  vehicles: {len(vehicles):,}  casualties: {len(casualties):,}")
    return collisions, vehicles, casualties


def compute_crash_severity(casualties):
    # A single crash can injure multiple people with different severities.
    # We convert each casualty to a weight (fatal=3, serious=2, slight=1) and
    # sum them per collision_index to get one severity score per crash event.
    # This means a crash with two serious casualties (score=4) outweighs one
    # with a single serious casualty (score=2) when scoring a segment.
    casualties["severity_weight"] = casualties["casualty_severity"].map(SEVERITY_WEIGHTS)
    return (
        casualties
        .groupby("collision_index", as_index=False)["severity_weight"]
        .sum()
    )


def build_crash_table(collisions, vehicles, crash_severity):
    # Join 1: attach the severity score to each collision.
    # Left join so we keep collisions even if no casualty record exists (rare);
    # those get severity_weight=1 (slight) as a fallback.
    crashes = collisions.merge(crash_severity, on="collision_index", how="left")
    crashes["severity_weight"] = crashes["severity_weight"].fillna(1)

    # Join 2: expand to one row per vehicle involved in each collision.
    # A collision with 3 vehicles becomes 3 rows, each carrying the same
    # collision location and severity score but a different vehicle_type.
    # This is the unit of analysis for per-type risk: each vehicle's involvement
    # in a crash is one observation.
    crashes = crashes.merge(vehicles, on="collision_index", how="inner")
    return crashes


def filter_and_map(crashes):
    # Drop the small fraction of records with missing GPS coordinates.
    crashes = crashes.dropna(subset=["latitude", "longitude"])

    # Keep only the study years (2020–2024).
    crashes = crashes[crashes["collision_year"].between(*YEAR_RANGE)]

    # Map DfT's ~100 vehicle codes to our 5 categories.
    # Rows whose code is not in VEHICLE_TYPE_MAP (buses, agricultural, etc.)
    # become NaN after .map() and are dropped — we don't have enough of them
    # to build stable risk surfaces.
    crashes["vehicle_type"] = crashes["vehicle_type"].map(VEHICLE_TYPE_MAP)
    crashes = crashes.dropna(subset=["vehicle_type"])

    return crashes


def main():
    collisions, vehicles, casualties = load_tables()

    # Severity is computed from casualties, then joined onto the collision table,
    # then vehicles are expanded — the order matters.
    crash_severity = compute_crash_severity(casualties)
    crashes = build_crash_table(collisions, vehicles, crash_severity)
    crashes = filter_and_map(crashes)

    # Keep only the 6 columns Stage 2 needs; rename collision_year → accident_year
    # to match the naming used throughout the rest of the pipeline.
    crashes = (
        crashes[["collision_index", "latitude", "longitude",
                 "vehicle_type", "severity_weight", "collision_year"]]
        .rename(columns={"collision_year": "accident_year"})
        .reset_index(drop=True)
    )

    OUTPUT_DIR.mkdir(exist_ok=True)
    crashes.to_csv(OUTPUT_FILE, index=False)

    print(f"\nOutput: {len(crashes):,} rows → {OUTPUT_FILE}")
    print("\nBy vehicle type:")
    print(crashes["vehicle_type"].value_counts())
    print("\nBy year:")
    print(crashes["accident_year"].value_counts().sort_index())


if __name__ == "__main__":
    main()
