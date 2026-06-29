#!/usr/bin/env python3
"""
Stage 5 — Risk-Aware Routing

Graph structure (from Stage 2): segment adjacency
  - Nodes = segment_ids (road segments)
  - Edges = (seg_a, seg_b) means the two segments share a junction

Edge weight formula:
  w_t(a → b) = travel_time_b × (1 + λ × norm_risk_b_t)

Route = ordered sequence of segment IDs.
k alternatives found via Yen's algorithm, then MCDM-ranked.
Output: routes.csv + route_map.html (interactive Folium).

Usage:
  python route.py --start "51.5074,-0.1278" --end "51.5200,-0.0900" --type car
  python route.py --start "53.4808,-2.2426" --end "53.4960,-2.2000" --type cycle --k 5
"""

import argparse
import time
from itertools import islice
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
import folium
from folium import LayerControl
from scipy.spatial import KDTree


# ── Constants ─────────────────────────────────────────────────────────────────
# These are shared across every function so they live at module level.

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']

# One fixed colour per type — used consistently in the map and legend.
TYPE_COLOURS = {
    'car':        '#3498db',
    'motorcycle': '#e74c3c',
    'cycle':      '#2ecc71',
    'lgv':        '#f39c12',
    'hgv':        '#8e44ad',
}

# Speed proxies derived from OS MasterMap road_class.
# There is no actual speed data in the dataset, so road class is used as a proxy.
# These are typical free-flow speeds in km/h (not speed limits — they approximate
# average travel speed on each class of road).
SPEED_KMH = {
    'Motorway':               113,   # 70 mph national speed limit
    'A Road':                  97,   # 60 mph
    'B Road':                  80,   # 50 mph
    'Classified Unnumbered':   64,   # 40 mph
    'Unclassified':            48,   # 30 mph (typical urban)
    'Not Classified':          48,
    'Unknown':                 48,
}
DEFAULT_SPEED_KMH = 48  # fallback for any class not in the dict above

# Resolve the outputs directory relative to this script's location.
# __file__ = .../code/stage5_routing/route.py → .parent.parent = .../code/
CODE_DIR = Path(__file__).parent.parent
OUTPUTS  = CODE_DIR / 'outputs'


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    # All five arguments that control a routing run.
    # --start / --end are the only required ones; the rest have sensible defaults.
    p = argparse.ArgumentParser(description='Stage 5: risk-aware routing')
    p.add_argument('--start',       required=True,
                   help='Start coordinate "lat,lon"  e.g. "51.5074,-0.1278"')
    p.add_argument('--end',         required=True,
                   help='End coordinate "lat,lon"')
    p.add_argument('--k',           type=int,   default=3,
                   help='Alternative routes per type (default 3)')
    p.add_argument('--lambda_risk', type=float, default=0.5,
                   help='Risk weight λ in [0,1]: 0 = pure time, 1 = max risk-averse (default 0.5)')
    p.add_argument('--type',        required=True, choices=VEHICLE_TYPES,
                   help='Vehicle type to route: car, motorcycle, cycle, lgv, hgv')
    p.add_argument('--padding',     type=float, default=0.5,
                   help='Bbox padding as fraction of O-D straight-line distance (default 0.5)')
    return p.parse_args()


def parse_coord(s):
    # "51.5074,-0.1278" → (51.5074, -0.1278)
    lat, lon = s.strip().split(',')
    return float(lat), float(lon)


# ── Geometry helpers ──────────────────────────────────────────────────────────

def haversine_km(lat1, lon1, lat2, lon2):
    # Great-circle distance on a sphere of radius 6371 km.
    # Used to compute O-D distance and set the map zoom level.
    R = 6371.0
    d = np.radians
    a = (np.sin((d(lat2) - d(lat1)) / 2) ** 2
         + np.cos(d(lat1)) * np.cos(d(lat2)) * np.sin((d(lon2) - d(lon1)) / 2) ** 2)
    return 2 * R * np.arcsin(np.sqrt(a))


def make_bbox(start, end, padding):
    """
    Returns (lon_min, lat_min, lon_max, lat_max, dist_km).
    Padding adds headroom in every direction so Yen's can find k alternatives —
    if the bbox is too tight there may only be one corridor and the algorithm
    can't diverge to find distinct routes.
    """
    lat1, lon1 = start
    lat2, lon2 = end
    dist_km    = haversine_km(lat1, lon1, lat2, lon2)

    # Convert km padding to degrees: 1 degree latitude ≈ 111 km everywhere,
    # and longitude degrees are similar at UK latitudes (~53°N).
    pad_deg = (dist_km * padding) / 111.0

    return (
        min(lon1, lon2) - pad_deg,   # lon_min
        min(lat1, lat2) - pad_deg,   # lat_min
        max(lon1, lon2) + pad_deg,   # lon_max
        max(lat1, lat2) + pad_deg,   # lat_max
        dist_km,
    )


# ── Data loading ──────────────────────────────────────────────────────────────

def load_segments(bbox):
    """
    Loads segments.gpkg, clips to bbox by centroid, then reprojects geometry
    from EPSG:27700 (British National Grid) to WGS84 so Folium can draw it.
    Returns (GeoDataFrame, set of segment_ids in bbox).
    """
    lon_min, lat_min, lon_max, lat_max = bbox[:4]
    print('  Loading segments.gpkg...', flush=True)
    t0  = time.time()
    gdf = gpd.read_file(OUTPUTS / 'segments.gpkg')

    # Filter by centroid, not geometry bounds — faster and sufficient for routing.
    # Segments whose centroid is inside the bbox are the ones we want to route through.
    gdf = gdf[
        (gdf['centroid_lon'] >= lon_min) & (gdf['centroid_lon'] <= lon_max) &
        (gdf['centroid_lat'] >= lat_min) & (gdf['centroid_lat'] <= lat_max)
    ].copy()

    # The raw geometry is in EPSG:27700 (British National Grid, units = metres).
    # Folium uses WGS84 (EPSG:4326, units = decimal degrees), so we reproject here
    # once, before drawing any polylines on the map.
    gdf = gdf.to_crs('EPSG:4326')
    print(f'  {len(gdf):,} segments in bbox  ({time.time()-t0:.1f}s)')
    return gdf, set(gdf['segment_id'])


def load_adjacency(bbox_ids):
    """
    Loads graph_edges.csv and retains only edges where both endpoints are in
    the bbox. The source file stores each pair once; both directions are added
    when building the networkx DiGraph.
    """
    print('  Loading graph_edges.csv...', flush=True)
    t0  = time.time()
    adj = pd.read_csv(OUTPUTS / 'graph_edges.csv')

    # Both endpoints must be in the bbox — if only one is, the edge crosses the
    # boundary and routing through it would leave the subgraph, causing a dead end.
    adj = adj[
        adj['segment_id_a'].isin(bbox_ids) &
        adj['segment_id_b'].isin(bbox_ids)
    ]
    print(f'  {len(adj):,} adjacency pairs in bbox  ({time.time()-t0:.1f}s)')
    return adj


def load_risk(bbox_ids, types):
    """
    Loads risk_surface_filtered.csv for the bbox segments and requested types.
    Returns dict: {segment_id: {type: risk_score, type+'_hot': bool}}
    """
    print('  Loading risk scores...', flush=True)
    t0 = time.time()
    df = pd.read_csv(OUTPUTS / 'risk_surface_filtered.csv')

    # Only keep rows for segments in the bbox and the vehicle types being routed.
    # The full file has 19.8M rows; this filters it down to at most bbox_size × len(types).
    df = df[df['segment_id'].isin(bbox_ids) & df['vehicle_type'].isin(types)]

    # Reshape from long (one row per segment×type) into a nested dict for O(1) lookup
    # during graph building.  risk[sid]['car'] = risk score; risk[sid]['car_hot'] = bool.
    risk = {}
    for row in df.itertuples(index=False):
        sid = row.segment_id
        if sid not in risk:
            risk[sid] = {}
        risk[sid][row.vehicle_type]          = float(row.risk_score)
        risk[sid][row.vehicle_type + '_hot'] = bool(row.is_hotspot)

    print(f'  Risk loaded for {len(risk):,} segments  ({time.time()-t0:.1f}s)')
    return risk


# ── Graph ─────────────────────────────────────────────────────────────────────

def build_graph(segs_gdf, adj_df, risk, lambda_risk, types):
    """
    Builds a directed segment-adjacency graph.

    Nodes = segment_ids.  Edges = both directions of every adjacency pair.

    Edge weight for type t on edge a → b:
        w_t(a→b) = travel_time_b × (1 + λ × norm_risk_b_t)

    The cost is charged to the DESTINATION segment b because entering a→b
    means you will traverse b — that is where travel time and risk accumulate.
    Segment a's cost was already paid when you entered it from its predecessor.

    Risk scores are normalised per-type over the bbox to [0, 1] so λ has
    a consistent meaning regardless of the absolute risk scale between types.
    """
    # Step 1: build a lookup of segment physical attributes (length, road class, travel time).
    # travel_time_s = (length_km / speed_kmh) × 3600 seconds
    seg_attrs = {}
    for row in segs_gdf.itertuples(index=False):
        speed = SPEED_KMH.get(row.road_class, DEFAULT_SPEED_KMH)
        tt_s  = (row.length_m / 1000.0) / speed * 3600.0
        seg_attrs[row.segment_id] = {
            'length_m':      row.length_m,
            'road_class':    row.road_class,
            'travel_time_s': tt_s,
            'speed_kmh':     speed,
        }

    # Step 2: find the maximum non-zero risk score per type across the bbox.
    # This is used to normalise risk to [0, 1] so λ has consistent meaning
    # regardless of how large the raw risk scores happen to be for each type.
    max_risk = {}
    for t in types:
        vals = [risk[sid][t] for sid in risk if t in risk[sid] and risk[sid][t] > 0]
        max_risk[t] = max(vals) if vals else 1.0

    G = nx.DiGraph()

    # Step 3: add every in-bbox segment as a node, storing its attributes on the node.
    # Storing risk on the node (not just the edge) lets path_metrics read it later
    # without needing to access the raw risk dict again.
    for sid, attrs in seg_attrs.items():
        nd = dict(attrs)
        for t in types:
            nd[f'risk_{t}'] = risk.get(sid, {}).get(t, 0.0)
            nd[f'hot_{t}']  = risk.get(sid, {}).get(t + '_hot', False)
        G.add_node(sid, **nd)

    # Step 4: add directed edges in both directions for every adjacency pair.
    # graph_edges.csv stores each adjacency once (a, b), so we add both a→b and b→a.
    # Edge weight is per-type and stored under key 'w_car', 'w_motorcycle', etc.
    # The weight is applied to the DESTINATION so each direction uses the destination's attributes.
    for row in adj_df.itertuples(index=False):
        a, b = row.segment_id_a, row.segment_id_b
        if a not in seg_attrs or b not in seg_attrs:
            continue  # skip if one endpoint fell outside the bbox after filtering

        tt_a = seg_attrs[a]['travel_time_s']
        tt_b = seg_attrs[b]['travel_time_s']

        w_ab = {}   # weights for the a → b direction (cost = entering b)
        w_ba = {}   # weights for the b → a direction (cost = entering a)
        for t in types:
            nr_b = risk.get(b, {}).get(t, 0.0) / max_risk[t]   # normalised risk of b
            nr_a = risk.get(a, {}).get(t, 0.0) / max_risk[t]   # normalised risk of a
            w_ab[f'w_{t}'] = tt_b * (1 + lambda_risk * nr_b)
            w_ba[f'w_{t}'] = tt_a * (1 + lambda_risk * nr_a)

        G.add_edge(a, b, **w_ab)
        G.add_edge(b, a, **w_ba)

    print(f'  Graph: {G.number_of_nodes():,} nodes, {G.number_of_edges():,} edges')
    return G


# ── Routing ───────────────────────────────────────────────────────────────────

def nearest_segment(segs_gdf, lat, lon):
    """
    Finds the segment whose centroid is closest to (lat, lon) using a KDTree.
    KDTree query is O(log n) — fast even with hundreds of thousands of segments.
    """
    # Build a 2D array of (lat, lon) centroid pairs and query it.
    # The KDTree finds the nearest point in log-time using a spatial index.
    coords = segs_gdf[['centroid_lat', 'centroid_lon']].values
    tree   = KDTree(coords)
    _, idx = tree.query([lat, lon])    # idx = row index of the nearest centroid
    return segs_gdf.iloc[idx]['segment_id']


def run_yens(G, source, target, t, k):
    """
    Yen's k-shortest simple paths for vehicle type t.

    nx.shortest_simple_paths implements Yen's algorithm: it runs Dijkstra for
    the first path, then iteratively builds spur paths from each prefix of the
    previous best path, pruning already-used branches.  This guarantees the k
    paths are distinct (simple = no repeated nodes) and in ascending cost order.

    We stamp the per-type edge weight onto the generic 'weight' attribute
    before each call so networkx uses the right cost surface.
    """
    # networkx uses whatever edge attribute is named 'weight'.
    # Our graph stores per-type weights as 'w_car', 'w_motorcycle', etc.
    # So before each routing call we copy the right column into 'weight'.
    nx.set_edge_attributes(
        G,
        {(u, v): data[f'w_{t}'] for u, v, data in G.edges(data=True)},
        'weight',
    )

    try:
        # islice stops the lazy generator after k paths — we don't need to
        # enumerate all simple paths (that would be exponential).
        paths = list(islice(
            nx.shortest_simple_paths(G, source, target, weight='weight'), k
        ))
    except (nx.NetworkXNoPath, nx.NodeNotFound, nx.exception.NetworkXError):
        paths = []
    return paths


def path_metrics(G, path, t):
    # Walk the sequence of segment IDs and accumulate route statistics.
    # The path is a list of node IDs; each node's attributes are already on the graph.
    total_dist  = 0.0
    total_time  = 0.0
    total_risk  = 0.0   # cumulative sum of raw risk scores (not normalised) along the route
    n_hotspots  = 0
    segments    = []    # per-segment detail list used by build_map to draw the route

    for sid in path:
        if sid not in G.nodes:
            continue
        nd          = G.nodes[sid]
        total_dist  += nd.get('length_m', 0) / 1000.0        # metres → km
        total_time  += nd.get('travel_time_s', 0) / 60.0     # seconds → minutes
        total_risk  += nd.get(f'risk_{t}', 0.0)
        is_hot       = bool(nd.get(f'hot_{t}', False))
        n_hotspots  += int(is_hot)
        segments.append({'segment_id': sid, 'is_hotspot': is_hot})

    return {
        'total_dist_km':  round(total_dist,  3),
        'total_time_min': round(total_time,  3),
        'total_risk':     round(total_risk,  6),
        'n_hotspots':     n_hotspots,
        'segments':       segments,
        'path':           path,
    }


def mcdm_rank(routes, w_time=0.4, w_risk=0.4, w_hotspot=0.2):
    """
    AHP-style multi-criteria ranking over k route candidates.

    Each criterion (time, cumulative risk, hotspot count) is min-max normalised
    to [0, 1] then combined as a weighted sum.  Lower score = better route.

    Why not just pick the shortest path?  A pure shortest-time route might pass
    through many hotspot segments.  A slightly longer route may avoid most of
    them.  AHP makes this trade-off explicit and tunable.

    Rank 1 = best balanced route.  Ranks 2 and 3 shown on the map at lower
    opacity as visible alternatives.
    """
    if len(routes) == 1:
        # Nothing to rank — trivially the best route.
        routes[0].update(rank=1, mcdm_score=0.0)
        return routes

    def norm(vals):
        # Min-max normalisation: maps any list of numbers to [0, 1].
        # If all values are equal the range is 0; return 0 for all (no preference).
        lo, hi = min(vals), max(vals)
        return [(v - lo) / (hi - lo) if hi > lo else 0.0 for v in vals]

    times    = [r['total_time_min'] for r in routes]
    risks    = [r['total_risk']     for r in routes]
    hotspots = [r['n_hotspots']     for r in routes]

    # Compute weighted sum score for each route.
    # zip(norm(times), norm(risks), norm(hotspots)) gives per-route normalised triplets.
    # Lower score = better (all three criteria are costs, not benefits).
    scored = sorted(
        zip(
            (w_time * nt + w_risk * nr + w_hotspot * nh
             for nt, nr, nh in zip(norm(times), norm(risks), norm(hotspots))),
            routes,
        ),
        key=lambda x: x[0],   # sort by score ascending
    )

    # Assign rank and score back onto each route dict in place.
    for rank, (score, route) in enumerate(scored, start=1):
        route['rank']       = rank
        route['mcdm_score'] = round(score, 4)

    return [r for _, r in scored]   # return routes in rank order


# ── Map ───────────────────────────────────────────────────────────────────────

def build_map(all_routes, segs_gdf, start, end):
    """
    Interactive Folium map.

    - OSM tiles give street/landmark context without loading any segment geometry
      as a background layer (that would be ~4M polylines and crash the browser).
    - One FeatureGroup per vehicle type: toggleable via the layer control panel.
    - Within each type, k routes drawn at decreasing opacity (rank 1 = fullest).
    - Hotspot segments overlaid with a dashed red line so risk concentrations
      along the route are immediately visible.
    - Legend panel (bottom-left) shows rank-1 metrics for all types.
    """
    mid_lat = (start[0] + end[0]) / 2
    mid_lon = (start[1] + end[1]) / 2
    dist_km = haversine_km(*start, *end)

    # Pick an initial zoom level based on O-D distance so the full route fits on screen.
    zoom = 14 if dist_km < 2 else 13 if dist_km < 5 else 12 if dist_km < 15 else 11

    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=zoom, tiles='OpenStreetMap')

    # Pre-index segment geometry for fast sid → geometry lookup during drawing.
    seg_geom = segs_gdf.set_index('segment_id')['geometry']

    # Visual hierarchy: rank 1 is bold and opaque, alternatives fade out.
    opacity_by_rank = {1: 0.90, 2: 0.45, 3: 0.25}
    weight_by_rank  = {1: 6,    2: 4,    3: 3   }

    legend_rows = []

    for t, routes in all_routes.items():
        colour = TYPE_COLOURS[t]

        for route in routes:
            rank    = route['rank']
            opacity = opacity_by_rank.get(rank, 0.20)
            lw      = weight_by_rank.get(rank, 2)
            label   = f'{t.capitalize()} – Rank {rank}'

            # Each rank gets its own FeatureGroup so the user can toggle routes individually.
            # Rank 1 starts visible; alternatives start hidden.
            fg = folium.FeatureGroup(name=label, show=(rank == 1))

            for seg in route['segments']:
                sid = seg['segment_id']
                if sid not in seg_geom.index:
                    continue
                geom = seg_geom[sid]

                # Shapely stores geometry coordinates as (lon, lat) in geographic CRS,
                # but Folium expects (lat, lon).  Swap explicitly to avoid silent errors.
                coords = [(lat, lon) for lon, lat in geom.coords]

                tip = f'⚠ {label} · hotspot' if seg['is_hotspot'] else label
                folium.PolyLine(
                    coords, color=colour, weight=lw, opacity=opacity, tooltip=tip,
                ).add_to(fg)

                # Dashed red overlay marks hotspot segments on top of the route line.
                # Drawn as a separate PolyLine so it appears above the route colour.
                if seg['is_hotspot']:
                    folium.PolyLine(
                        coords, color='#ff0000', weight=lw + 2,
                        opacity=opacity, dash_array='6 4',
                    ).add_to(fg)

            fg.add_to(m)

        # Collect rank-1 stats for the legend table.
        best = routes[0]
        legend_rows.append(
            f'<tr>'
            f'<td><b style="color:{colour}">■</b> {t.capitalize()}</td>'
            f'<td style="text-align:right;padding:2px 8px">{best["total_dist_km"]:.1f} km</td>'
            f'<td style="text-align:right;padding:2px 8px">{best["total_time_min"]:.1f} min</td>'
            f'<td style="text-align:right;padding:2px 8px">{best["total_risk"]:.4f}</td>'
            f'<td style="text-align:right;padding:2px 8px">{best["n_hotspots"]}</td>'
            f'</tr>'
        )

    # Start / end markers use FontAwesome icons via prefix='fa'.
    folium.Marker(
        list(start), popup='Start',
        icon=folium.Icon(color='green', icon='play', prefix='fa'),
    ).add_to(m)
    folium.Marker(
        list(end), popup='End',
        icon=folium.Icon(color='red', icon='stop', prefix='fa'),
    ).add_to(m)

    # Legend panel injected as raw HTML into the page root.
    # It is positioned fixed so it stays visible while the user pans the map.
    legend_html = f"""
    <div style="position:fixed;bottom:20px;left:20px;z-index:9999;
                background:white;padding:14px 16px;border-radius:8px;
                box-shadow:0 2px 10px rgba(0,0,0,0.3);font-size:13px;min-width:360px">
      <b>Best route per type</b>
      <span style="float:right;font-size:11px;color:#888">toggle layers ↗</span>
      <table style="width:100%;border-collapse:collapse;margin-top:8px">
        <tr style="background:#f5f5f5;font-size:11px;color:#555">
          <th style="text-align:left;padding:3px 8px">Type</th>
          <th style="padding:3px 8px">Distance</th>
          <th style="padding:3px 8px">Time</th>
          <th style="padding:3px 8px">Risk</th>
          <th style="padding:3px 8px">Hotspots</th>
        </tr>
        {''.join(legend_rows)}
      </table>
      <div style="margin-top:10px;font-size:11px;color:#666">
        <span style="display:inline-block;width:20px;border-bottom:3px dashed red"></span>
        &nbsp;hotspot segment &nbsp;·&nbsp; Rank 2 &amp; 3 at lower opacity
      </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # LayerControl adds the toggle panel (top-right by default).
    # collapsed=False keeps it open so users don't have to click to expand it.
    LayerControl(collapsed=False).add_to(m)
    return m


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    args  = parse_args()
    start = parse_coord(args.start)
    end   = parse_coord(args.end)

    t = args.type   # single vehicle type for this run

    print(f'\nRouting {start} → {end}  [{t}]')
    print(f'k={args.k}  λ={args.lambda_risk}')

    bbox    = make_bbox(start, end, args.padding)
    dist_km = bbox[4]
    print(f'O-D distance: {dist_km:.1f} km  |  padding: {args.padding*100:.0f}%')

    if dist_km > 50:
        print(f'\nWARNING: {dist_km:.0f} km is long — bbox will be large and routing slow.')
        print('Keep start/end within ~30 km for reasonable runtime.\n')

    # Phase 1: load data for the bounding box only.
    # Loading everything nationally would take too long and build a graph too large for Yen's.
    print('\nLoading data...')
    segs_gdf, bbox_ids = load_segments(bbox)
    adj_df              = load_adjacency(bbox_ids)
    risk                = load_risk(bbox_ids, [t])

    if len(adj_df) == 0:
        print('ERROR: No adjacency edges in bounding box. Check coordinates.')
        return

    # Phase 2: build the networkx graph from segments + adjacency + risk.
    print('\nBuilding graph...')
    G = build_graph(segs_gdf, adj_df, risk, args.lambda_risk, [t])

    # Phase 3: find the nearest segment to each coordinate.
    # The user provides geographic coordinates; the graph nodes are segment IDs.
    source = nearest_segment(segs_gdf, *start)
    target = nearest_segment(segs_gdf, *end)
    print(f'\nSource segment: {source}')
    print(f'Target segment: {target}')

    if source == target:
        print('ERROR: Start and end map to the same segment. Use further apart coordinates.')
        return

    # Phase 4: run Yen's to get k candidate routes, then rank by crash risk score.
    print(f'\nRouting [{t}]...', flush=True)
    t0    = time.time()
    paths = run_yens(G, source, target, t, args.k)

    if not paths:
        print('ERROR: No path found. Check coordinates are on/near the road network.')
        return

    metrics = [path_metrics(G, p, t) for p in paths]
    ranked  = mcdm_rank(metrics)

    print(f'  {len(ranked)} routes  ({time.time()-t0:.1f}s)')
    rows = []
    for r in ranked:
        print(f'  Rank {r["rank"]}: '
              f'{r["total_dist_km"]:.1f} km  '
              f'{r["total_time_min"]:.1f} min  '
              f'risk={r["total_risk"]:.4f}  '
              f'hotspots={r["n_hotspots"]}')
        rows.append({
            'vehicle_type': t,
            'rank':         r['rank'],
            'dist_km':      r['total_dist_km'],
            'time_min':     r['total_time_min'],
            'total_risk':   r['total_risk'],
            'n_hotspots':   r['n_hotspots'],
            'mcdm_score':   r['mcdm_score'],
            'n_segments':   len(r['segments']),
        })

    # Phase 5: save outputs.
    # routes.csv = one row per rank — machine-readable for Stage 6 evaluation.
    # route_map.html = interactive Folium map — human-readable for inspection.
    out_csv = OUTPUTS / 'routes.csv'
    pd.DataFrame(rows).to_csv(out_csv, index=False)
    print(f'\nSaved → {out_csv}')

    print('Building map...')
    m       = build_map({t: ranked}, segs_gdf, start, end)
    out_map = OUTPUTS / 'route_map.html'
    m.save(str(out_map))
    print(f'Saved → {out_map}')
    print('\nOpen route_map.html in a browser to explore routes.')


if __name__ == '__main__':
    main()
