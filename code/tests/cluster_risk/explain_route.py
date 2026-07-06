#!/usr/bin/env python3
"""
Per-route, per-type risk explanation (simple version).

A generated route is an ordered list of segments; we have a per-type risk score
AND segment-level road attributes for each. This explains ONE route in three parts:

  1. Which segments drive the route's risk (top contributors + their road type).
  2. Road-attribute composition of the route (share of risk by carriageway form,
     road function, trunk road, roundabout).
  3. Why this route vs the fastest one (what risky segments it detours around).

Attributes are segment-level OS Open Roads only (road_function, form_of_way incl.
Roundabout, trunk_road, junction degree) — all known for every segment on a route.
No pedestrian-crossing / crash-only fields (not available per arbitrary segment).

Descriptive, not causal; risk_score is the model's per-type surface.

Usage:
  python explain_route.py --json routing_full_l1.json --risk london_xgb_full.csv \
         --pair 3 --type hgv
"""

import argparse
import json
import sys

import numpy as np
import pandas as pd
import pyogrio

import common as C
sys.path.insert(0, str(C.CODE_DIR / 'stage5_routing'))
from route import SPEED_KMH, DEFAULT_SPEED_KMH, make_bbox   # noqa: E402
import routing_test as RT                                   # noqa: E402

OS_GPKG = C.CODE_DIR / 'data' / 'oproad_gpkg_gb' / 'Data' / 'oproad_gb.gpkg'


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--json', required=True)
    p.add_argument('--risk', required=True)
    p.add_argument('--pair', type=int, required=True)
    p.add_argument('--type', required=True, choices=C.VEHICLE_TYPES)
    p.add_argument('--padding', type=float, default=0.5)
    return p.parse_args()


def load_os_attrs():
    """Segment-level road attributes + derived junction degree, indexed by id."""
    df = pyogrio.read_dataframe(OS_GPKG, layer='road_link', read_geometry=False,
                                columns=['id', 'road_function', 'form_of_way',
                                         'trunk_road', 'start_node', 'end_node'])
    deg = pd.concat([df['start_node'], df['end_node']]).value_counts()
    df['jdeg'] = np.maximum(df['start_node'].map(deg).values,
                            df['end_node'].map(deg).values)
    df = df.set_index('id')
    return df


def route_time_min(path, road_class):
    t = 0.0
    for sid in path:
        rc = road_class.get(sid)
        spd = SPEED_KMH.get(rc, DEFAULT_SPEED_KMH)
        # length pulled from seg attrs below; handled by caller
    return t


def main():
    args = parse_args()
    with open(args.json) as f:
        data = json.load(f)
    pr = next(p for p in data['pairs'] if p['pair'] == args.pair)
    route = pr['paths'][args.type]
    o, d = tuple(pr['o']), tuple(pr['d'])

    print(f'Explaining {args.type.upper()} route for pair {args.pair} '
          f'({pr["dist_km"]} km, {len(route)} segments)\n')

    # risk surface for this type
    rdf = pd.read_csv(args.risk)
    rdf = rdf[rdf['vehicle_type'] == args.type]
    risk = dict(zip(rdf['segment_id'], rdf['risk_score']))

    # segment geometry (length, road_class) + OS attributes
    seg, edges = RT.load_city(data['city'])
    length = dict(zip(seg['segment_id'], seg['length_m']))
    rclass = dict(zip(seg['segment_id'], seg['road_class']))
    os_attrs = load_os_attrs()

    def attr(sid, col):
        try:    return os_attrs.at[sid, col]
        except (KeyError, Exception): return None

    def seg_time_min(sid):
        spd = SPEED_KMH.get(rclass.get(sid), DEFAULT_SPEED_KMH)
        return (length.get(sid, 0) / 1000.0) / spd * 60.0

    # per-segment table for the route
    recs = []
    for sid in route:
        recs.append({
            'sid': sid, 'risk': risk.get(sid, 0.0),
            'len_m': length.get(sid, 0.0), 'time_min': seg_time_min(sid),
            'form_of_way': attr(sid, 'form_of_way'),
            'road_function': attr(sid, 'road_function'),
            'trunk': bool(attr(sid, 'trunk_road')),
            'jdeg': attr(sid, 'jdeg'),
        })
    rt = pd.DataFrame(recs)
    total_risk = rt['risk'].sum()
    total_time = rt['time_min'].sum()

    # ── 1. top risk-contributing segments ──
    print('1. SEGMENTS DRIVING THE RISK')
    print(f'   route total: {total_time:.1f} min, risk score {total_risk:.2f}')
    top = rt.sort_values('risk', ascending=False).head(5)
    for _, r in top.iterrows():
        share = 100 * r['risk'] / total_risk if total_risk else 0
        rd = 'roundabout' if r['form_of_way'] == 'Roundabout' else (r['form_of_way'] or '?')
        print(f'   {share:4.0f}% of risk  risk={r["risk"]:.3f}  {rd}, '
              f'{r["road_function"] or "?"}'
              f'{", trunk" if r["trunk"] else ""}, '
              f'junction-degree {int(r["jdeg"]) if pd.notna(r["jdeg"]) else "?"}')

    # ── 2. attribute composition (share of risk) ──
    print('\n2. ROAD COMPOSITION (share of route risk by attribute)')
    for col, lab in [('form_of_way', 'carriageway form'), ('road_function', 'road function')]:
        g = rt.groupby(col)['risk'].sum().sort_values(ascending=False)
        parts = ', '.join(f'{k} {100*v/total_risk:.0f}%'
                          for k, v in g.items() if v > 0)
        print(f'   by {lab}: {parts}')
    rr = 100 * rt[rt['form_of_way'] == 'Roundabout']['risk'].sum() / total_risk if total_risk else 0
    tr = 100 * rt[rt['trunk']]['risk'].sum() / total_risk if total_risk else 0
    print(f'   roundabout segments carry {rr:.0f}% of risk; trunk-road {tr:.0f}%')

    # ── 3. why this route vs the fastest ──
    print('\n3. WHY THIS ROUTE (vs the fastest path)')
    bbox = make_bbox(o, d, args.padding)
    G, sub = RT.build_bbox_graph(seg, edges, risk_wrap(risk, args.type), bbox,
                                 0.0, [args.type])   # lambda=0 -> pure time
    s = RT.nearest_seg(sub, *o); tgt = RT.nearest_seg(sub, *d)
    fastest = RT.shortest_path(G, s, tgt, args.type)
    if fastest is None:
        print('   (could not compute fastest path)')
    else:
        chosen_set, fast_set = set(route), set(fastest)
        fast_time = sum(seg_time_min(x) for x in fastest)
        fast_risk = sum(risk.get(x, 0.0) for x in fastest)
        avoided = [x for x in fastest if x not in chosen_set]   # on fastest, not taken
        if set(route) == fast_set:
            print('   This IS the fastest path — no risk detour was worth taking here.')
        else:
            print(f'   fastest path: {fast_time:.1f} min, risk {fast_risk:.2f}')
            print(f'   this route:   {total_time:.1f} min (+{total_time-fast_time:.1f}), '
                  f'risk {total_risk:.2f} ({100*(total_risk-fast_risk)/max(fast_risk,1e-9):+.0f}%)')
            av = sorted(avoided, key=lambda x: risk.get(x, 0), reverse=True)[:4]
            print(f'   avoids {len(avoided)} segment(s) on the fast route, incl. the riskiest:')
            for x in av:
                fw = attr(x, 'form_of_way'); rf = attr(x, 'road_function')
                rd = 'roundabout' if fw == 'Roundabout' else (fw or '?')
                print(f'      risk={risk.get(x,0):.3f}  {rd}, {rf or "?"}')


def risk_wrap(risk, t):
    """RT.build_bbox_graph expects {sid: {type: score}}."""
    return {sid: {t: v} for sid, v in risk.items()}


if __name__ == '__main__':
    main()
