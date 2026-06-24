import pandas as pd
from pathlib import Path

ROOT = Path(__file__).parent.parent  # code/
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

COLLISIONS_FILE = DATA_DIR / "dft-road-casualty-statistics-collision-last-5-years.csv"
VEHICLES_FILE   = DATA_DIR / "dft-road-casualty-statistics-vehicle-last-5-years.csv"
CASUALTIES_FILE = DATA_DIR / "dft-road-casualty-statistics-casualty-last-5-years.csv"

OUTPUT_FILE = OUTPUT_DIR / "crashes_clean.csv"

YEAR_RANGE = (2020, 2024)

# DfT codes: 1=Fatal, 2=Serious, 3=Slight
SEVERITY_WEIGHTS = {1: 3, 2: 2, 3: 1}

# DfT vehicle_type codes mapped to our categories
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
    casualties["severity_weight"] = casualties["casualty_severity"].map(SEVERITY_WEIGHTS)
    return (
        casualties
        .groupby("collision_index", as_index=False)["severity_weight"]
        .sum()
    )


def build_crash_table(collisions, vehicles, crash_severity):
    # attach severity score to each collision
    crashes = collisions.merge(crash_severity, on="collision_index", how="left")
    crashes["severity_weight"] = crashes["severity_weight"].fillna(1)

    # one row per vehicle involved in each collision
    crashes = crashes.merge(vehicles, on="collision_index", how="inner")
    return crashes


def filter_and_map(crashes):
    # drop rows with missing location
    crashes = crashes.dropna(subset=["latitude", "longitude"])

    # keep chosen year range
    crashes = crashes[crashes["collision_year"].between(*YEAR_RANGE)]

    # map raw codes to vehicle categories; drop unmapped types
    crashes["vehicle_type"] = crashes["vehicle_type"].map(VEHICLE_TYPE_MAP)
    crashes = crashes.dropna(subset=["vehicle_type"])

    return crashes


def main():
    collisions, vehicles, casualties = load_tables()

    crash_severity = compute_crash_severity(casualties)
    crashes = build_crash_table(collisions, vehicles, crash_severity)
    crashes = filter_and_map(crashes)

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
