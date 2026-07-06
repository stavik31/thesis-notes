#!/usr/bin/env python3
"""
Stage 3 — Per-Type Cluster + Share Risk Model  (replaces the GAT)

Produces risk_scores.csv: one row per (segment_id, vehicle_type) with a risk
score used by Stage 4 (filtering) and Stage 5 (routing).

Why this replaces the GAT (see wiki/build/stage-3-cluster-share-engine.md):
the unified GAT collapsed the per-type divergence (cross-type ρ 0.855) because
any signal shared across types pulls every type's estimate toward a common
answer, and because the divergence lives in *location*, not volume. This engine
fixes both at once:

  1. pool sparse crash data by NETWORK LOCATION (per-type BFS clusters), so
     there is enough data per unit to estimate from at all;
  2. predict each type's SHARE of its cluster's all-type crash total (not the
     raw count), which removes the "how busy overall" magnitude that all types
     agree on;
  3. train 5 FULLY SEPARATE models — nothing shared across types anywhere.

Validated leakage-free 2026-07-06 (national out-of-sample ρ=-0.097; validity on
the never-seen 2024 year ≈ validity on the target years). This is the DEPLOYMENT
surface: trained on all history, predicting all segments. Generalisation/leakage
testing is Stage 6 (spatial CV + temporal 2024), not here.

Usage:
  python train.py                # full Great Britain
  python train.py --city london  # quick test on one bbox
"""

import argparse
import time
from collections import deque
from pathlib import Path

import numpy as np
import pandas as pd
import pyogrio
import xgboost as xgb

# ── Constants ─────────────────────────────────────────────────────────────────

VEHICLE_TYPES = ['car', 'motorcycle', 'cycle', 'lgv', 'hgv']

# Each crash type's own exposure / traffic column (from the DfT AADF join in
# Stage 2). Used as a per-type feature — kept identical to Stage 2's naming.
AADF_COL = {
    'car':        'cars_and_taxis',
    'motorcycle': 'two_wheeled_motor_vehicles',
    'cycle':      'pedal_cycles',
    'lgv':        'lgvs',
    'hgv':        'all_hgvs',
}

# The single most important guardrail in this file: the years that build the
# CLUSTERS + INPUT FEATURES must be disjoint from the years that form the
# TARGET. If they overlap, the model can copy its own input to its output and
# score perfectly while learning nothing that generalises (the temporal leak we
# hit in the ad-hoc phase). HOLDOUT_YEAR is touched by nothing here — it is
# reserved for the Stage 6 temporal-leakage check.
HISTORY_YEARS = [2020, 2021]   # clusters + input features
TARGET_YEARS  = [2022, 2023]   # training target
HOLDOUT_YEAR  = 2024           # reserved for Stage 6 only — never read here

# A cluster keeps growing over the road network until it has accumulated at
# least this much of a type's HISTORY crash weight — enough data to estimate a
# stable share from. Dense areas → many small clusters; sparse areas (e.g. HGV)
# → few coarse ones. 30 is the validated default.
MIN_CRASHES = 30.0

# Bounding boxes (lon_min, lat_min, lon_max, lat_max, WGS84) for --city testing.
CITIES = {
    'london':     (-0.51, 51.28,  0.33, 51.72),
    'birmingham': (-2.05, 52.35, -1.75, 52.60),
    'manchester': (-2.40, 53.33, -2.10, 53.55),
    'leeds':      (-1.70, 53.72, -1.45, 53.88),
}

CODE_DIR = Path(__file__).parent.parent
OUTPUTS  = CODE_DIR / 'outputs'

# Segment attribute columns the engine reads (no geometry — much lighter).
SEG_COLS = ['segment_id', 'road_class', 'length_m', 'all_motor_vehicles',
            'cars_and_taxis', 'lgvs', 'all_hgvs', 'two_wheeled_motor_vehicles',
            'pedal_cycles', 'aadf_fallback', 'centroid_lon', 'centroid_lat']

# ── Data loading ──────────────────────────────────────────────────────────────

def load_data(city=None):
    """Load the three Stage-2 outputs. With --city, clip all three to one bbox
    (by segment centroid) so a self-contained subgraph is loaded for quick tests.

    We read segment ATTRIBUTES only (read_geometry=False) — the engine never
    needs the polylines, only the columns — which is why 3.96M rows load in ~12s.
    """
    t0 = time.time()
    print('Loading segments.gpkg...', flush=True)
    segments = pyogrio.read_dataframe(OUTPUTS / 'segments.gpkg',
                                      read_geometry=False, columns=SEG_COLS)
    print(f'  {len(segments):,} segments  ({time.time()-t0:.1f}s)')

    if city:
        lon_min, lat_min, lon_max, lat_max = CITIES[city]
        m = ((segments['centroid_lon'] >= lon_min) & (segments['centroid_lon'] <= lon_max) &
             (segments['centroid_lat'] >= lat_min) & (segments['centroid_lat'] <= lat_max))
        segments = segments[m].reset_index(drop=True)
        print(f'  city={city}: {len(segments):,} segments')

    # WHY filter crashes AND edges by the same segment set: under --city we want a
    # self-contained subgraph where every crash and every edge refers to a segment
    # that exists in the filtered node set — otherwise clustering/features break.
    city_ids = set(segments['segment_id']) if city else None

    print('Loading crashes_segmented.csv...', flush=True)
    crashes = pd.read_csv(OUTPUTS / 'crashes_segmented.csv', low_memory=False,
                          usecols=['segment_id', 'vehicle_type',
                                   'severity_weight', 'accident_year'])
    if city:
        crashes = crashes[crashes['segment_id'].isin(city_ids)].reset_index(drop=True)

    print('Loading graph_edges.csv...', flush=True)
    edges = pd.read_csv(OUTPUTS / 'graph_edges.csv')
    if city:
        edges = edges[edges['segment_id_a'].isin(city_ids) &
                      edges['segment_id_b'].isin(city_ids)].reset_index(drop=True)

    return segments, crashes, edges

# BUILD-MARKER: next section below
