#!/usr/bin/env python3
"""
Batch routing-divergence test — reconstruction of the 2026-07-04 London test.

Given a per-(segment,type) risk surface CSV, for N random O-D pairs in a city:
  * build a bbox subgraph (same padding logic as route.py),
  * route each of the 5 vehicle types with route.py's EXACT edge-weight formula
    w_t(a->b) = travel_time_b * (1 + lambda * norm_risk_b_t),
  * count how many of the 5 types take a genuinely distinct path.

Headline metric = mean distinct paths / 5 per O-D pair (the vanished result:
3.10 for cluster+share XGBoost, 2.00 for best-GAT, 1.00 for no-risk).

Per-pair detail is saved to a JSON so the car/pair-9 diagnosis can reuse it
without re-running.

Usage:
  python routing_test.py --risk london_xgb_risk.csv --city london --lambda 1.0
"""

import argparse
import json
import sys
import time
from itertools import islice
from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

import common as C

# Reuse the production routing constants + geometry helpers verbatim so the test
# can never drift from route.py's real formula.
sys.path.insert(0, str(C.CODE_DIR / 'stage5_routing'))
from route import SPEED_KMH, DEFAULT_SPEED_KMH, haversine_km, make_bbox  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--risk', required=True, help='risk CSV: segment_id,vehicle_type,risk_score')
    p.add_argument('--city', default='london', choices=list(C.CITIES.keys()))
    p.add_argument('--n-pairs', type=int, default=10)
    p.add_argument('--lambda', dest='lam', type=float, default=1.0)
    p.add_argument('--min-km', type=float, default=3.0)
    p.add_argument('--max-km', type=float, default=12.0)
    p.add_argument('--padding', type=float, default=0.5)
    p.add_argument('--seed', type=int, default=42)
    p.add_argument('--out', default=None, help='JSON of per-pair detail')
    return p.parse_args()


def load_city(city):
    seg = C.load_segments()
    mask = C.in_city(seg, city)
    seg = seg[mask].reset_index(drop=True)
    ids = set(seg['segment_id'])
    edges = C.load_edges()
    edges = edges[edges['segment_id_a'].isin(ids) & edges['segment_id_b'].isin(ids)]
    return seg, edges


def nearest_seg(seg, lat, lon):
    d = (seg['centroid_lat'].values - lat) ** 2 + (seg['centroid_lon'].values - lon) ** 2
    return seg['segment_id'].values[int(np.argmin(d))]


def build_bbox_graph(seg, edges, risk, bbox, lam, types):
    """Directed subgraph for one bbox with per-type edge weights, exactly as
    route.py builds it (risk normalised per-type over the bbox; cost on dest)."""
    lon_min, lat_min, lon_max, lat_max = bbox[:4]
    m = ((seg['centroid_lon'] >= lon_min) & (seg['centroid_lon'] <= lon_max) &
         (seg['centroid_lat'] >= lat_min) & (seg['centroid_lat'] <= lat_max)).values
    sub = seg[m]
    sub_ids = set(sub['segment_id'])

    attrs = {}
    for row in sub.itertuples(index=False):
        speed = SPEED_KMH.get(row.road_class, DEFAULT_SPEED_KMH)
        attrs[row.segment_id] = ((row.length_m / 1000.0) / speed * 3600.0)  # travel_time_s

    max_risk = {}
    for t in types:
        vals = [risk.get(sid, {}).get(t, 0.0) for sid in sub_ids]
        vals = [v for v in vals if v > 0]
        max_risk[t] = max(vals) if vals else 1.0

    e = edges[edges['segment_id_a'].isin(sub_ids) & edges['segment_id_b'].isin(sub_ids)]
    G = nx.DiGraph()
    G.add_nodes_from(sub_ids)
    for row in e.itertuples(index=False):
        a, b = row.segment_id_a, row.segment_id_b
        if a not in attrs or b not in attrs:
            continue
        tt_a, tt_b = attrs[a], attrs[b]
        wab, wba = {}, {}
        for t in types:
            nr_b = risk.get(b, {}).get(t, 0.0) / max_risk[t]
            nr_a = risk.get(a, {}).get(t, 0.0) / max_risk[t]
            wab[f'w_{t}'] = tt_b * (1 + lam * nr_b)
            wba[f'w_{t}'] = tt_a * (1 + lam * nr_a)
        G.add_edge(a, b, **wab)
        G.add_edge(b, a, **wba)
    return G, sub


def shortest_path(G, s, t, vtype):
    try:
        return nx.shortest_path(G, s, t, weight=f'w_{vtype}')
    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


def jaccard(p, q):
    a, b = set(p), set(q)
    return len(a & b) / len(a | b) if (a or b) else 1.0


def main():
    args = parse_args()
    rng = np.random.default_rng(args.seed)
    types = C.VEHICLE_TYPES

    print(f'Loading {args.city}...')
    seg, edges = load_city(args.city)
    print(f'  {len(seg):,} segments, {len(edges):,} edges')

    rdf = pd.read_csv(args.risk)
    risk = {}
    for r in rdf.itertuples(index=False):
        risk.setdefault(r.segment_id, {})[r.vehicle_type] = float(r.risk_score)
    print(f'  risk surface: {len(risk):,} segments')

    seg_ids = seg['segment_id'].values
    cent = seg[['centroid_lat', 'centroid_lon']].values

    results = []
    pair = 0
    attempts = 0
    while pair < args.n_pairs and attempts < args.n_pairs * 20:
        attempts += 1
        i, j = rng.integers(0, len(seg), 2)
        o = (cent[i, 0], cent[i, 1]); d = (cent[j, 0], cent[j, 1])
        dist = haversine_km(*o, *d)
        if not (args.min_km <= dist <= args.max_km):
            continue
        bbox = make_bbox(o, d, args.padding)
        G, sub = build_bbox_graph(seg, edges, risk, bbox, args.lam, types)
        s = nearest_seg(sub, *o); tgt = nearest_seg(sub, *d)
        if s == tgt or s not in G or tgt not in G:
            continue
        paths = {t: shortest_path(G, s, tgt, t) for t in types}
        if any(p is None for p in paths.values()):
            continue

        uniq = len({frozenset(p) for p in paths.values()})
        # pairwise jaccard matrix
        pj = {}
        for a in range(len(types)):
            for b in range(a + 1, len(types)):
                pj[f'{types[a]}-{types[b]}'] = round(
                    jaccard(paths[types[a]], paths[types[b]]), 3)
        results.append({
            'pair': pair, 'dist_km': round(dist, 2),
            'source': s, 'target': tgt,
            'o': [float(o[0]), float(o[1])], 'd': [float(d[0]), float(d[1])],
            'distinct': uniq,
            'path_len': {t: len(paths[t]) for t in types},
            'paths': {t: list(paths[t]) for t in types},
            'pairwise_jaccard': pj,
        })
        print(f'  pair {pair}: dist={dist:.1f}km  distinct={uniq}/5  '
              f'min_jac={min(pj.values()):.2f}')
        pair += 1

    if not results:
        print('No valid pairs found.')
        return
    md = np.mean([r['distinct'] for r in results])
    print(f'\nMean distinct paths / 5 types = {md:.2f}   (over {len(results)} pairs, '
          f'lambda={args.lam})')

    out = args.out or f'routing_{args.city}_{Path(args.risk).stem}.json'
    with open(out, 'w') as f:
        json.dump({'lambda': args.lam, 'city': args.city, 'mean_distinct': md,
                   'pairs': results}, f, indent=2)
    print(f'Saved per-pair detail -> {out}')


if __name__ == '__main__':
    main()
