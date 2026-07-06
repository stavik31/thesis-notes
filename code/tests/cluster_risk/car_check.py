#!/usr/bin/env python3
"""
Car / pair-9 diagnosis (2026-07-04 open item #2).

The 07-04 routing test had a pair (pair 9) where car stayed on a high-risk
corridor even though a cheap, low-overlap alternative existed. The question:
is car's risk ON that alternative actually lower? If yes and car still didn't
move, lambda=1.0 is too weak; if the alternative is just as risky for car,
staying is correct.

This re-usable tool, for a routing_*.json produced by routing_test.py:
  * finds pairs where car did NOT take a distinct path (car clumped with others),
  * for every distinct path taken by ANY type on that O-D, evaluates car's own
    total risk and travel time on that path,
  * flags the "pair-9 pattern": a path exists that is lower car-risk than car's
    chosen path for a modest time penalty (car should have diverged but didn't).

Then rerun routing_test.py at higher lambda on the flagged O-D to confirm.

Usage:
  python car_check.py --json routing_london_london_xgb_full.json --risk london_xgb_full.csv
"""

import argparse
import json

import numpy as np
import pandas as pd

import common as C
import sys
sys.path.insert(0, str(C.CODE_DIR / 'stage5_routing'))
from route import SPEED_KMH, DEFAULT_SPEED_KMH  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--json', required=True)
    p.add_argument('--risk', required=True)
    p.add_argument('--type', default='car')
    p.add_argument('--time-tol', type=float, default=0.25,
                   help='Max fractional extra travel time for an alternative to '
                        'count as "cheap" (0.25 = +25%)')
    return p.parse_args()


def main():
    args = parse_args()
    with open(args.json) as f:
        data = json.load(f)

    seg = C.load_segments()
    m = C.in_city(seg, data['city'])
    seg = seg[m]
    length = dict(zip(seg['segment_id'], seg['length_m']))
    rclass = dict(zip(seg['segment_id'], seg['road_class']))

    rdf = pd.read_csv(args.risk)
    rdf = rdf[rdf['vehicle_type'] == args.type]
    risk = dict(zip(rdf['segment_id'], rdf['risk_score']))

    def path_time_min(path):
        t = 0.0
        for sid in path:
            spd = SPEED_KMH.get(rclass.get(sid), DEFAULT_SPEED_KMH)
            t += (length.get(sid, 0) / 1000.0) / spd * 60.0
        return t

    def path_risk(path):
        return sum(risk.get(sid, 0.0) for sid in path)

    print(f'Car-divergence diagnosis on {args.json}  (type={args.type})\n')
    flagged = []
    for pr in data['pairs']:
        paths = pr['paths']
        car_path = paths[args.type]
        car_key = frozenset(car_path)
        # distinct alternative paths taken by any type
        alts = {}
        for t, p in paths.items():
            alts[frozenset(p)] = p
        car_r = path_risk(car_path); car_t = path_time_min(car_path)

        best_alt = None
        for key, p in alts.items():
            if key == car_key:
                continue
            r = path_risk(p); tt = path_time_min(p)
            # lower car-risk for modest extra time?
            if r < car_r * 0.98 and tt <= car_t * (1 + args.time_tol):
                if best_alt is None or r < best_alt[1]:
                    best_alt = (p, r, tt)

        tag = ''
        if best_alt is not None:
            tag = '  <-- PAIR-9 PATTERN (cheaper-risk alt car ignored)'
            flagged.append(pr['pair'])
        print(f"pair {pr['pair']}: dist={pr['dist_km']}km distinct={pr['distinct']}/5  "
              f"car_risk={car_r:.3f} car_time={car_t:.1f}min{tag}")
        if best_alt is not None:
            p, r, tt = best_alt
            print(f"    alt: car_risk={r:.3f} ({100*(r-car_r)/car_r:+.0f}%)  "
                  f"time={tt:.1f}min ({100*(tt-car_t)/car_t:+.0f}%)  "
                  f"src={pr['source']} tgt={pr['target']}")

    print(f'\nFlagged pairs (car ignored a cheaper-risk alternative): {flagged}')
    if flagged:
        print('Re-run routing_test at higher lambda on these O-Ds to test whether '
              'car then diverges. If it does -> lambda was too weak; if not -> '
              'the alternative was not actually better for car.')


if __name__ == '__main__':
    main()
