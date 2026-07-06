#!/usr/bin/env python3
"""
Lambda sensitivity on a specific O-D (car/pair-9 follow-up).

car_check.py flags O-D pairs where, at lambda=1, car stayed on a high-risk
corridor despite a cheaper-risk alternative. This sweeps lambda for car on such
a pair and reports whether car's shortest path flips to the safer route, and at
what lambda. If it flips -> lambda was too weak (a routing-tuning issue, not a
risk-model problem); if it never flips -> the alternative was not actually
cheaper once car's own risk is charged.

Usage:
  python lambda_test.py --json routing_full_l1.json --risk london_xgb_full.csv --pair 5
"""

import argparse
import json
import sys

import numpy as np

import common as C
sys.path.insert(0, str(C.CODE_DIR / 'stage5_routing'))
from route import make_bbox  # noqa: E402
import routing_test as RT  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--json', required=True)
    p.add_argument('--risk', required=True)
    p.add_argument('--pair', type=int, required=True)
    p.add_argument('--type', default='car')
    p.add_argument('--lambdas', default='0,1,2,3,5,8,12')
    p.add_argument('--padding', type=float, default=0.5)
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.json) as f:
        data = json.load(f)
    pr = next(p for p in data['pairs'] if p['pair'] == args.pair)
    o = tuple(pr['o']); d = tuple(pr['d'])
    print(f"Pair {args.pair}: {pr['dist_km']}km  src={pr['source']} tgt={pr['target']}")

    seg, edges = RT.load_city(data['city'])
    import pandas as pd
    rdf = pd.read_csv(args.risk)
    risk = {}
    for r in rdf.itertuples(index=False):
        risk.setdefault(r.segment_id, {})[r.vehicle_type] = float(r.risk_score)

    bbox = make_bbox(o, d, args.padding)
    types = C.VEHICLE_TYPES

    base_path = None
    print(f"\n{'lambda':>7} {'car_time_min':>13} {'car_risk_raw':>13} "
          f"{'jac_vs_time':>12} {'changed':>8}")
    for lam in [float(x) for x in args.lambdas.split(',')]:
        G, sub = RT.build_bbox_graph(seg, edges, risk, bbox, lam, types)
        s = RT.nearest_seg(sub, *o); tgt = RT.nearest_seg(sub, *d)
        path = RT.shortest_path(G, s, tgt, args.type)
        if path is None:
            print(f'{lam:>7.1f}  no path'); continue
        # raw car risk + time along the path
        risk_sum = sum(risk.get(sid, {}).get(args.type, 0.0) for sid in path)
        tmin = 0.0
        for sid in path:
            nd_tt = G.nodes  # travel time not stored on node here; recompute
        # recompute time from route.py speed model
        from route import SPEED_KMH, DEFAULT_SPEED_KMH
        rc = dict(zip(sub['segment_id'], sub['road_class']))
        ln = dict(zip(sub['segment_id'], sub['length_m']))
        tmin = sum((ln.get(sid, 0) / 1000.0) /
                   SPEED_KMH.get(rc.get(sid), DEFAULT_SPEED_KMH) * 60.0 for sid in path)
        if lam == 0.0 or base_path is None:
            base_path = set(path)
        jac = len(set(path) & base_path) / len(set(path) | base_path)
        changed = 'yes' if jac < 0.99 else ''
        print(f'{lam:>7.1f} {tmin:>13.2f} {risk_sum:>13.2f} {jac:>12.3f} {changed:>8}')


if __name__ == '__main__':
    main()
