import time
import pandas as pd
import geopandas as gpd
from pathlib import Path

# --- Paths ---
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"

OS_ROADS_FILE = DATA_DIR / "oproad_gpkg_gb" / "Data" / "oproad_gb.gpkg"
AADF_FILE     = DATA_DIR / "dft_traffic_counts_aadf.csv"

CRASHES_FILE         = OUTPUT_DIR / "crashes_clean.csv"
SEGMENTS_FILE        = OUTPUT_DIR / "segments.gpkg"
CRASHES_SEG_FILE     = OUTPUT_DIR / "crashes_segmented.csv"
GRAPH_EDGES_FILE     = OUTPUT_DIR / "graph_edges.csv"

# --- Coordinate systems ---
# All spatial operations run in British National Grid (metres) so that distance
# thresholds like 25m and 1000m work directly without degree-to-metre conversion.
# Crashes arrive in WGS84 (lat/lon) and are reprojected before any spatial join.
CRS_BNG = "EPSG:27700"
CRS_WGS = "EPSG:4326"

# --- Tuning knobs ---
# MATCH_BUFFER_M: a crash point is only snapped to a road link if the nearest
# link is within this distance. 25m is tight enough to avoid mis-assigning a
# crash to the wrong road in urban areas where roads run close together.
MATCH_BUFFER_M  = 25

# AADF_MAX_DIST_M: DfT count points don't cover every road link. If no count
# point exists within 1km of a segment's centroid, fall back to the mean AADF
# for that road class (the standard approach across the cited routing papers).
AADF_MAX_DIST_M = 1000


def _t():
    return time.perf_counter()

def _done(t0, extra=""):
    print(f"  done ({time.perf_counter() - t0:.1f}s){extra}")


def load_road_network():
    # OS Open Roads publishes the full GB road network as a GeoPackage with
    # three layers. We only need road_link — one row per road segment between
    # two junctions, with a unique TOID identifier, road classification, length,
    # and the node IDs at each end.
    # ~3.96M links cover every classified road in Great Britain.
    print("Loading OS Open Roads road links...", flush=True)
    t = _t()
    links = gpd.read_file(OS_ROADS_FILE, layer="road_link")
    _done(t, f"  {len(links):,} links")
    print(f"  columns: {links.columns.tolist()}")  # diagnostic — check names match below

    # OS Open Roads is natively in BNG so this is a no-op in practice,
    # but explicit reprojection guards against future schema changes.
    print("  Reprojecting to BNG...", end="", flush=True)
    t = _t()
    links = links.to_crs(CRS_BNG)
    _done(t)

    # Rename OS field names to our internal names used throughout the pipeline.
    links = links.rename(columns={
        "id":                 "segment_id",
        "road_classification":"road_class",
        "length":             "length_m",
    })
    links["segment_id"] = links["segment_id"].astype(str)
    links["start_node"] = links["start_node"].astype(str)
    links["end_node"]   = links["end_node"].astype(str)
    return links[["segment_id", "road_class", "length_m", "start_node", "end_node", "geometry"]]


def build_graph_edges(links):
    # The router in Stage 5 needs to know which segments connect to which.
    # Two segments are adjacent if they share a junction node — the end of one
    # is the start of the other, or both meet at the same junction.
    #
    # Method: stack all (segment, start_node) and (segment, end_node) pairs into
    # one long table, then self-join on node ID. Any two segments that appear
    # in the same node group are adjacent. The segment_id_a < segment_id_b filter
    # removes duplicates — without it each pair would appear twice (A→B and B→A).
    #
    # Output is a flat CSV of pairs that Stage 5 loads into NetworkX directly.
    print("Building graph edges...", end="", flush=True)
    t = _t()
    starts = links[["segment_id", "start_node"]].rename(columns={"start_node": "node"})
    ends   = links[["segment_id", "end_node"]].rename(columns={"end_node": "node"})
    long   = pd.concat([starts, ends], ignore_index=True)

    pairs = long.merge(long, on="node", suffixes=("_a", "_b"))
    pairs = pairs[pairs["segment_id_a"] < pairs["segment_id_b"]]
    pairs = pairs[["segment_id_a", "segment_id_b"]].drop_duplicates().reset_index(drop=True)
    _done(t, f"  {len(pairs):,} edges")
    return pairs


def map_match_crashes(links, crashes_df):
    # Each crash in crashes_clean.csv is a GPS point floating in space.
    # We need to assign it to a road segment so Stage 3 can count crashes
    # per (segment, vehicle_type).
    #
    # sjoin_nearest finds the closest road link geometry to each crash point.
    # It uses an R-tree spatial index over the road links to avoid brute-force
    # distance calculations (otherwise: 888k × 3.96M = 3.5 trillion checks).
    # max_distance=25m drops crashes that are too far from any road link —
    # these are typically off-road incidents or GPS errors.
    print(f"Map-matching {len(crashes_df):,} crashes...", end="", flush=True)
    t = _t()
    crashes_gdf = gpd.GeoDataFrame(
        crashes_df,
        geometry=gpd.points_from_xy(crashes_df["longitude"], crashes_df["latitude"]),
        crs=CRS_WGS,
    ).to_crs(CRS_BNG)

    matched = gpd.sjoin_nearest(
        crashes_gdf,
        links[["segment_id", "geometry"]],
        how="left",
        max_distance=MATCH_BUFFER_M,
        distance_col="snap_dist_m",
    )
    _done(t)

    before = len(crashes_df)
    matched = matched.dropna(subset=["segment_id"])
    after  = len(matched)
    print(f"  {after:,} / {before:,} matched  ({before - after:,} unmatched, outside {MATCH_BUFFER_M}m)")

    return matched[["collision_index", "latitude", "longitude", "vehicle_type",
                     "severity_weight", "accident_year", "segment_id", "snap_dist_m"]]


def load_aadf(links):
    # AADF (Annual Average Daily Flow) is the traffic volume on a road — the
    # exposure denominator. Without it, a quiet lane with 2 crashes looks riskier
    # than a motorway with 50. Stage 3 divides crash counts by this to get a rate.
    #
    # DfT publishes counts at ~22k fixed monitoring points, not for every road link.
    # We join each segment's centroid to its nearest count point (within 1km).
    # For segments with no count point in range (~41% of the network, mostly minor
    # roads), we substitute the mean AADF for that road class.
    #
    # The per-type columns (lgvs, all_hgvs, two_wheeled_motor_vehicles, pedal_cycles)
    # are the per-type exposure denominators Stage 3 needs to compute type-specific
    # crash rates.
    print("Loading DfT AADF...", end="", flush=True)
    t = _t()
    aadf = pd.read_csv(AADF_FILE, low_memory=False)
    aadf.columns = aadf.columns.str.lower().str.replace(" ", "_")
    latest_year = aadf["year"].max()
    aadf = aadf[aadf["year"] == latest_year].copy()
    _done(t, f"  {len(aadf):,} count points (year {latest_year})")

    aadf_gdf = gpd.GeoDataFrame(
        aadf,
        geometry=gpd.points_from_xy(aadf["easting"], aadf["northing"]),
        crs=CRS_BNG,
    )
    link_centroids = gpd.GeoDataFrame(
        links[["segment_id", "road_class"]].copy(),
        geometry=links.geometry.centroid,
        crs=CRS_BNG,
    )

    print(f"  Joining {len(link_centroids):,} segments to count points...", end="", flush=True)
    t = _t()
    joined = gpd.sjoin_nearest(
        link_centroids,
        aadf_gdf.drop(columns=["count_point_id"]),
        how="left",
        max_distance=AADF_MAX_DIST_M,
        distance_col="aadf_dist_m",
    )
    # sjoin_nearest can return multiple rows for a segment when its centroid is
    # equidistant from two count points. Keep the first match only.
    joined = joined.drop_duplicates(subset="segment_id", keep="first")
    _done(t)

    # Segments beyond 1km from any count point get NaN for all_motor_vehicles.
    # Replace with the mean for their road class so every segment has a value.
    fallback = joined["all_motor_vehicles"].isna()
    class_means = joined.groupby("road_class")["all_motor_vehicles"].transform("mean")
    joined.loc[fallback, "all_motor_vehicles"] = class_means[fallback]
    joined["aadf_fallback"] = fallback

    n_fallback = fallback.sum()
    print(f"  {n_fallback:,} segments used road-class-mean fallback ({n_fallback / len(joined) * 100:.1f}%)")

    return joined[["segment_id", "all_motor_vehicles", "cars_and_taxis", "lgvs",
                    "all_hgvs", "two_wheeled_motor_vehicles", "pedal_cycles",
                    "aadf_dist_m", "aadf_fallback"]]


def assemble_segment_table(links, aadf_joined):
    # Merge AADF values onto the road links table to produce the final segment table.
    # Also adds centroid lat/lon in WGS84 — used by the data_viewer.ipynb map only;
    # the rest of the pipeline stays in BNG.
    print("Assembling segment table...", end="", flush=True)
    t = _t()
    segments = links.merge(aadf_joined, on="segment_id", how="left")
    wgs_centroids = segments.geometry.centroid.to_crs(CRS_WGS)
    segments["centroid_lon"] = wgs_centroids.x
    segments["centroid_lat"] = wgs_centroids.y
    _done(t, f"  {len(segments):,} segments")
    return segments


def main():
    # Stage 2 produces three outputs that feed the rest of the pipeline:
    #   segments.gpkg        — node feature table for the GAT (geometry + road class + AADF)
    #   crashes_segmented.csv — crash events with segment IDs; aggregated in Stage 3
    #                           into crash counts per (segment, vehicle_type)
    #   graph_edges.csv      — adjacency list; loaded into NetworkX for the GAT message
    #                          passing (Stage 3) and path search (Stage 5)
    t_total = _t()

    links = load_road_network()
    edges = build_graph_edges(links)

    print(f"Reading crashes...", end="", flush=True)
    t = _t()
    crashes_df = pd.read_csv(CRASHES_FILE)
    _done(t, f"  {len(crashes_df):,} rows")

    crashes_seg = map_match_crashes(links, crashes_df)
    aadf_joined = load_aadf(links)
    segments    = assemble_segment_table(links, aadf_joined)

    OUTPUT_DIR.mkdir(exist_ok=True)

    print(f"Writing segments.gpkg...", end="", flush=True)
    t = _t()
    segments.to_file(SEGMENTS_FILE, driver="GPKG")
    _done(t)

    print(f"Writing crashes_segmented.csv...", end="", flush=True)
    t = _t()
    crashes_seg.to_csv(CRASHES_SEG_FILE, index=False)
    _done(t)

    print(f"Writing graph_edges.csv...", end="", flush=True)
    t = _t()
    edges.to_csv(GRAPH_EDGES_FILE, index=False)
    _done(t)

    print(f"\nOutputs:")
    print(f"  segments:          {len(segments):,}  → {SEGMENTS_FILE}")
    print(f"  crashes_segmented: {len(crashes_seg):,}  → {CRASHES_SEG_FILE}")
    print(f"  graph_edges:       {len(edges):,}  → {GRAPH_EDGES_FILE}")
    print(f"\nCrashes per vehicle type after map-matching:")
    print(crashes_seg["vehicle_type"].value_counts())
    print(f"\nTotal time: {time.perf_counter() - t_total:.1f}s")


if __name__ == "__main__":
    main()
