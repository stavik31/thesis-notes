#!/usr/bin/env python3
"""
Descriptive per-type road-attribute association (the honest explainability layer).

NOT a model. For each vehicle type and each road attribute, computes:
  over-representation = P(attribute | this type) / P(attribute | all crashes)
  (>1 = this type's crashes are distinctively concentrated on that attribute)
plus Cramer's V + chi-square for "does this attribute associate with type at all".

This is descriptive epidemiology on crash distribution — it makes no causal claim
and does not depend on any model predicting well. Caveat printed in output: it is
a crash-distribution comparison, NOT exposure-normalised risk.

Features (9), all confidently labelled:
  STATS19 collision (join by collision_index):
    urban_or_rural_area, speed_limit, road_type, junction_control,
    junction_detail (binary at-junction), pedestrian_crossing (binary present)
  OS Open Roads / segments (join by segment_id):
    road_function, trunk_road, junction_degree (derived from node connectivity)
"""

import numpy as np
import pandas as pd
import pyogrio
from scipy.stats import chi2_contingency

import common as C

COLL_CSV = C.CODE_DIR / 'data' / 'dft-road-casualty-statistics-collision-last-5-years.csv'
OS_GPKG  = C.CODE_DIR / 'data' / 'oproad_gpkg_gb' / 'Data' / 'oproad_gb.gpkg'

# ── confident code -> label maps ────────────────────────────────────────────────
ROAD_TYPE = {1: 'Roundabout', 2: 'One-way street', 3: 'Dual carriageway',
             6: 'Single carriageway', 7: 'Slip road'}          # 9/-1 = unknown -> drop
JUNCTION_CONTROL = {1: 'Authorised person', 2: 'Auto traffic signal',
                    3: 'Stop sign', 4: 'Give way / uncontrolled'}  # 0/9/-1 -> drop
URBAN_RURAL = {1: 'Urban', 2: 'Rural'}                          # 3/-1 -> drop
# binary, label-safe (0 is unambiguous under the 2024 spec)
def bin_junction(v):      # junction_detail
    if v == 0:  return 'Not at junction'
    if v in (-1, 99): return None
    return 'At / near junction'
def bin_pedx(v):          # pedestrian_crossing
    if v == 0:  return 'No crossing <=50m'
    if v in (-1, 99): return None
    return 'Crossing facility <=50m'


def load_crashes_with_attrs():
    print('Loading crashes + collision attributes...')
    cr = pd.read_csv(C.OUTPUTS / 'crashes_segmented.csv', low_memory=False,
                     usecols=['collision_index', 'vehicle_type', 'segment_id'])
    coll = pd.read_csv(COLL_CSV, low_memory=False,
                       usecols=['collision_index', 'road_type', 'speed_limit',
                                'junction_detail', 'junction_control',
                                'urban_or_rural_area', 'pedestrian_crossing'])
    df = cr.merge(coll, on='collision_index', how='left')

    print('Loading OS road_function / trunk_road...')
    os_attr = pyogrio.read_dataframe(OS_GPKG, layer='road_link', read_geometry=False,
                                     columns=['id', 'road_function', 'trunk_road'])
    os_attr = os_attr.rename(columns={'id': 'segment_id'})
    df = df.merge(os_attr, on='segment_id', how='left')

    print('Deriving junction degree...')
    seg = pyogrio.read_dataframe(OS_GPKG, layer='road_link', read_geometry=False,
                                 columns=['id', 'start_node', 'end_node'])
    deg = pd.concat([seg['start_node'], seg['end_node']]).value_counts()
    seg['jdeg'] = np.maximum(seg['start_node'].map(deg).values,
                             seg['end_node'].map(deg).values)
    def bin_deg(d):
        if d <= 1: return '1 (dead-end)'
        if d == 2: return '2 (through-link)'
        if d == 3: return '3 (T-junction)'
        return '4+ (complex)'
    seg['jdeg_lab'] = seg['jdeg'].map(bin_deg)
    df = df.merge(seg[['id', 'jdeg_lab']].rename(columns={'id': 'segment_id'}),
                  on='segment_id', how='left')
    return df


def labelled(df):
    """Return dict attribute-name -> labelled Series (None = drop that row)."""
    out = {}
    out['urban_or_rural']   = df['urban_or_rural_area'].map(URBAN_RURAL)
    out['speed_limit']      = df['speed_limit'].where(df['speed_limit'] > 0).map(
                                  lambda v: f'{int(v)} mph' if pd.notna(v) else None)
    out['road_type']        = df['road_type'].map(ROAD_TYPE)
    out['junction_control'] = df['junction_control'].map(JUNCTION_CONTROL)
    out['at_junction']      = df['junction_detail'].map(bin_junction)
    out['ped_crossing']     = df['pedestrian_crossing'].map(bin_pedx)
    out['road_function']    = df['road_function'].where(
                                  df['road_function'].notna())
    out['trunk_road']       = df['trunk_road'].map({True: 'Trunk road',
                                                     False: 'Non-trunk'})
    out['junction_degree']  = df['jdeg_lab']
    return out


def cramers_v(ct):
    chi2, p, _, _ = chi2_contingency(ct)
    n = ct.values.sum()
    r, k = ct.shape
    phi2 = chi2 / n
    denom = min(r - 1, k - 1)
    return np.sqrt(phi2 / denom) if denom > 0 else 0.0, p


def main():
    df = load_crashes_with_attrs()
    types = C.VEHICLE_TYPES
    attrs = labelled(df)

    print('\n' + '=' * 78)
    print('PER-TYPE ROAD-ATTRIBUTE ASSOCIATION')
    print('over-representation = P(attr | type) / P(attr | all crashes)   '
          '>1 = distinctive')
    print('CAVEAT: crash-distribution comparison, NOT exposure-normalised risk.')
    print('=' * 78)

    rows_out = []
    for aname, series in attrs.items():
        sub = pd.DataFrame({'vt': df['vehicle_type'], 'a': series}).dropna()
        ct = pd.crosstab(sub['a'], sub['vt'])           # rows=attr, cols=type
        ct = ct.reindex(columns=types, fill_value=0)
        v, p = cramers_v(ct)

        # over-representation: column-normalised / overall-normalised
        col_share = ct / ct.sum(axis=0)                 # P(attr | type)
        base = ct.sum(axis=1) / ct.sum().sum()          # P(attr | all)
        over = col_share.div(base, axis=0)              # ratio

        print(f'\n■ {aname}   (Cramer V = {v:.3f}, p = {p:.1e})')
        header = '    ' + f'{"category":<26}' + ''.join(f'{t:>11}' for t in types)
        print(header)
        for cat in over.index:
            line = f'    {cat:<26}' + ''.join(f'{over.loc[cat, t]:>11.2f}' for t in types)
            print(line)
        for cat in over.index:
            for t in types:
                rows_out.append({'attribute': aname, 'category': cat,
                                 'vehicle_type': t,
                                 'over_representation': round(over.loc[cat, t], 3),
                                 'cramers_v': round(v, 3)})

    # highlight the standout per-type associations
    print('\n' + '=' * 78)
    print('STANDOUT per-type associations (over-representation >= 1.3, ranked)')
    print('=' * 78)
    od = pd.DataFrame(rows_out)
    for t in types:
        top = od[(od['vehicle_type'] == t) & (od['over_representation'] >= 1.3)] \
              .sort_values('over_representation', ascending=False).head(6)
        print(f'\n{t}:')
        for _, r in top.iterrows():
            print(f'    {r["over_representation"]:.2f}x  {r["attribute"]}={r["category"]}')

    out = 'road_association.csv'
    od.to_csv(out, index=False)
    print(f'\nSaved -> {out}')


if __name__ == '__main__':
    main()
