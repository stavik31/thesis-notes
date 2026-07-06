# Phase 3 — Wiki Log

Append-only chronological record for the active phase. One entry per operation.
Phase 1's log: `../PHASE1/log.md`. Phase 2's log: `../PHASE2/log.md`.
Parse with: `grep "^## \[" log.md | tail -10`

## [2026-07-06] ⏸ CHECKPOINT — end of day. Stage 2 enriched + re-run; Stage 3 rewrite STARTED (in progress). Read this first next session.
- **State:** engine decision finalized + validated leakage-free (see the progress entry below). **Stage 2 was enriched and re-run** — `segments.gpkg` now carries `road_function`, `form_of_way`, `trunk_road`, `junction_degree` (for the explainability layer; the engine doesn't use them). **Stage 3 `train.py` rewrite is IN PROGRESS** — replacing the GAT with the cluster+share+XGBoost engine, section by section, with the user following each part to understand it.
- **`train.py` progress so far:** Section 1 (docstring + imports + constants — HISTORY/TARGET/HOLDOUT windows, MIN_CRASHES=30, AADF_COL, CITIES, SEG_COLS) and Section 2 (`load_data`, with `--city` filtering) are written. A `# BUILD-MARKER: next section below` comment marks where the next section goes.
- **▶ RESUME HERE: the next section is CRASH AGGREGATION (`severity_matrix`)** — build the severity-weighted `[N segments × 5 types]` array from crashes, called twice (HISTORY_YEARS → clustering/features, TARGET_YEARS → target; disjoint = the leakage guard). It was drafted + explained this session but deliberately **not** committed to the file yet (user paused for the day). Then, in order: (4) adjacency + per-type BFS clustering, (5) cluster aggregates + share target, (6) per-type features, (7) 5 fully separate XGBoost models, (8) `risk_scores.csv` output + `main()`.
- **`train.py` is mid-rewrite and NOT runnable** — expected; don't run Stage 3 until the rewrite is complete.
- **Port from:** `code/tests/cluster_risk/{common,run_xgb}.py` (validated reference). Full spec + test→main-file mapping: [[wiki/build/stage-3-cluster-share-engine]].
- Page: [[wiki/progress/2026-07-06]]

## [2026-07-06] progress | Engine rebuilt + validated LEAKAGE-FREE; decision finalized; explainability + Stage-3 rewrite blueprint
- Page: [[wiki/progress/2026-07-06]]
- Pages created: [[wiki/build/stage-3-cluster-share-engine]] (the implementation blueprint for the Stage 3 rewrite)
- Decisions extracted: [[wiki/concepts/vehicle-type-risk-divergence]] (2026-07-06 RESOLUTION section),
  [[PHASE3/positioning-memo]] (engine FINALIZED row + status), [[wiki/overview]] (Stage 3/4/5/6 status + next steps)
- Notable: the 2026-07-04 "validated" result had been run ad hoc and its code was **lost** (verified) —
  rebuilt as durable scripts in `code/tests/cluster_risk/`, reproduced exactly (national eval 158,237),
  then validated properly with **16-fold spatial CV + an unseen-2024 temporal holdout**: national
  out-of-sample cross-type ρ=−0.097 and **validity on the never-seen 2024 ≈ validity on target years =
  NO LEAKAGE** (answers the "too good?" worry — ρ≈0 is the noise floor, validity ~0.05–0.18 is the
  honest, modest, sufficient bar). **Method decision FINAL: per-type discrete network clustering +
  share-of-all-type-total target + 5 separate XGBoost models; GAT tested on the same recipe ties
  divergence but loses validity/simplicity → retired.** 07-04 open items closed: λ-too-weak hypothesis
  **refuted** (pair-9 is correct behaviour); GAT-vs-XGBoost done. Added two explainability layers (model
  SHAP + descriptive per-type road-attribute over-representation, e.g. HGV↔motorway 4.8×, cycle↔roundabout
  1.4×) and a working per-route explainer (London cycle route −65% risk for +0.2 min). Nothing folded into
  the main pipeline yet — the blueprint [[wiki/build/stage-3-cluster-share-engine]] maps every test script
  to its target main file for the guided rewrite next.

## [2026-07-04] progress | Routing-divergence gap pairs diagnosed; GAT-with-cluster-recipe queued as top next step
- Page: [[wiki/progress/2026-07-04-clustering-testing]] (updated, same-session addendum)
- Notable: diagnosed the 2 non-diverging O-D pairs from the end-to-end routing test. Pair 1 (1/5
  distinct paths) is a genuine geographic dead-end — top-5 pure-travel-time alternatives overlap
  at Jaccard=0.99, essentially one corridor exists regardless of risk weighting; not a prediction
  problem. Pair 9 (2/5 distinct) is more nuanced — a real, cheap alternative route exists (0.01
  overlap, +17.8% travel time), hgv/motorcycle correctly stay put (their own risk there is already
  low), but car (risk=0.70 on this corridor) also didn't move despite the cheap alternative —
  car's risk on that alternative wasn't checked yet, so this is either correct (alternative is
  equally risky for car) or a sign λ=1.0 is too weak to overcome a 17.8% time cost. **Next-session
  priorities reordered: (1) test GAT using the exact same validated recipe (discrete network
  clusters + share objective + fully separate models) for direct comparison against XGBoost, run
  the same way (spatial holdout + routing test); (2) resolve the pair-9 car/λ question.**

## [2026-07-04] progress | Clustering direction built and tested end-to-end — feature-based mechanism falsified, location-based mechanism validated
- Page: [[wiki/progress/2026-07-04-clustering-testing]]
- Decisions extracted: [[wiki/concepts/vehicle-type-risk-divergence]] (major update — mechanism
  extended: divergence lives in location, not volume; feature-based clustering falsified),
  [[PHASE3/positioning-memo]] (build architecture row updated), [[wiki/overview]] (Stage 3 status
  + next steps updated)
- Notable: built and tested the 2026-07-04 supervisor-meeting clustering plan in full. Its literal
  mechanism (cluster by road_class + own-AADF + length, feature similarity) **fails** — ρ≈0.65-0.9,
  no better than the original collapsed GAT — because car/lgv/hgv's own-AADF values are themselves
  correlated with each other in reality (busy roads are busy for everyone), so feature-similarity
  pooling re-collapses divergence even with genuinely type-specific inputs. **What works instead:
  discrete network/location-based clusters (BFS-grown per type until a minimum crash count) +
  predicting each type's SHARE of the cluster's all-type crash total (not raw count/rate) + fully
  separate per-type XGBoost models — no shared parameters, no shared clustering key.** Validated
  three ways: (1) genuine spatial-block holdout — an entire city (Manchester, 74,783 segments)
  completely excluded from training — ρ=0.201, beats best-GAT's 0.377; (2) a new "does predicted
  risk correlate with real future crashes" validity check (run for the first time in the whole
  investigation) — XGBoost beat the pure statistic for every single vehicle type; (3) an actual
  end-to-end routing test on a second held-out city (London) — mean 3.10/5 vehicle types take
  genuinely distinct routes for the same trip, vs. 2.00/5 for best-GAT and 1.00/5 with no risk
  weighting. Several methodological mistakes were made and corrected during the session (an early
  temporal leak, a circular cluster-construction issue, a random instead of spatial holdout split)
  — full audit trail, including what NOT to repeat, is in the progress note. Two open items from
  the original plan (routing-search grouping split, "zoom in" semantics) remain unresolved; new
  open items added (2 non-diverging routing pairs need diagnosis; GAT not yet tested with this
  recipe; validity check not yet run on other methods). Nothing from tonight is committed to the
  codebase — all tested ad hoc per explicit instruction.

## [2026-07-04] progress | Supervisor meeting — 2026-07-03 fork reframed into per-type clustering direction
- Page: [[wiki/progress/2026-07-04]]
- Decisions extracted: [[wiki/concepts/vehicle-type-risk-divergence]] (fork section updated —
  superseded, not resolved), [[PHASE3/positioning-memo]] (build architecture row updated)
- Notable: supervisor didn't pick statistical-vs-GAT-stacked directly — reframed root cause as
  sparsity at raw segment resolution (96–99.8% zero-crash segments/type) and steered toward
  per-type clustering (5 independent clusterings, own AADF, never shared) to pool enough data,
  with the statistical-vs-model choice re-tested at cluster level via the same ρ/Jaccard/CLQ gate.
  Full 8-step plan drafted: `/home/vik-esoc/Desktop/thesis/new-direction-plan-2026-07-04.md`
  (draft, not finalized). Two sub-questions (routing-search grouping split; "zoom in" semantics)
  remain genuinely open, not supervisor-confirmed despite being stated as defaults in the plan.

## [2026-07-03] progress | Full type-collapse investigation; EB shrinkage beaten; Task B killed; strategic fork
- Page: [[wiki/progress/2026-07-03]]
- Decisions extracted: [[wiki/concepts/vehicle-type-risk-divergence]] (major update — general
  mechanism confirmed across 4 settings, EB-shrinkage correction, stacked-GAT fix documented)
- Corrected: 2026-07-02's claim that EB shrinkage is a "safe secondary denoiser" — it isn't,
  same collapse mechanism as everything else, tested and beaten by ad hoc statistical smoothing
- Notable: 13 tests run. Architecture decoupling alone barely helps (0.894→0.785 even at full
  separation). Fix that worked: share-target objective + per-type output heads together
  (ρ=0.377, synergistic, **zero new input data**). General mechanism found and confirmed 4x:
  any type-agnostic/shared signal (GAT backbone, generic STATS19 feature, EB's covariate prior)
  collapses divergence; type-specific packaging of the *same* info fixes it. "Richer inputs"
  hypothesis for ML directly refuted (clean OS geometry features flat for both GAT and XGBoost).
  Task B (conditional risk by weather/light) premise-killed (Cramér's V 0.03-0.05, negligible).
  Open fork: ad hoc statistical smoothing still beats every model (~0.19-0.25 vs 0.377) but is
  unformalized/uncited (likely Network KDE, unverified) — logged for 2026-07-04 supervisor
  meeting in `/home/vik-esoc/Desktop/thesis/supervisor-notes-2026-07-03.md`.

## [2026-07-02] progress | Stage 3 retrain + full routing/divergence diagnostic chain
- Page: [[wiki/progress/2026-07-02]]
- Decisions extracted: [[wiki/concepts/vehicle-type-risk-divergence]] (new, ★ core),
  [[wiki/concepts/routing-risk-normalization]] (new)
- Corrected: [[wiki/progress/2026-06-30]] — "Stage 5 bug fixed" was necessary but insufficient
- Challenged: positioning-memo "Unified GAT" locked decision → under revision (type-collapse)
- Notable: **THE finding — GAT type-collapse.** Ground-truth per-type crash surfaces are
  near-orthogonal (ρ≈−0.05, 4% hotspot overlap, survives denoising = niche CONFIRMED), but the
  unified GAT smooths them to ρ=0.855. Ladder diagnostic: spatial smoothing saturates at ρ≈0.25,
  so the collapse is architecture (shared backbone / weak conditioning), not message passing or
  sparsity. Fix = decouple types (Stage 3). Routing sub-findings: capping is the lever, per-type
  norm > global, λ≈2; divergence real but modest (parallel-street swaps) on current surface;
  exposure-confound refuted (pred drives divergence, not the denominator).

---

## [2026-06-30] ⏸ CHECKPOINT — Stage 5 bug fixed and confirmed working. Bbox limitation documented. Stage 6 next.
- **State: Stages 1–5 complete and working. Stage 6 evaluation starts next session.**
- **Stage 5 bug fixed:** `load_risk()` was loading `risk_surface_filtered.csv` as edge weights — 85% of segments zeroed out → routes collapsed to pure travel time. Fixed by loading `risk_scores.csv` (raw GAT output) for edge weights and `risk_surface_filtered.csv` for hotspot flags only. Re-run confirmed: routes now differentiate on risk (rank 1 vs rank 2 = 32% risk difference on test London O-D pair).
- **Bbox limitation surfaced:** routing clips to a bbox around the O-D pair for performance. Routes outside the rectangle are never considered — real usability limitation for production. **Decision: stays in, documented as prototype limitation.** Thesis evaluation compares vehicle-type routes within the same bbox → divergence result is still valid. Production fix (contraction hierarchies) is out of scope; standard in research prototypes.
- **Next:** Stage 6 evaluation.
- Page: [[wiki/progress/2026-06-30]]

## [2026-06-29] ⏸ CHECKPOINT — Stages 3–5 code complete. One known bug in Stage 5 deferred to next session.
- **State: Stage 3 plots done. Stage 4 run + results analysed. Stage 5 code written but has a routing bug — fix identified, not yet applied.**
- **Stage 3 extras:** `make_plots.py` written — 6 presentation plots: loss curve with generalisation gap + gold stars for new best val epochs; KDE risk distributions (all 5 types, log scale); 5×5 Pearson correlation matrix; national hotspot map (top 0.5%); zero-exposure rates bar chart; risk stats (median/mean/p95) per type.
- **Stage 4 run + results:** `filter_and_clq.py` walked through section by section and run. 99th-percentile cap + 85th-percentile threshold applied per type. CLQ results: all 10 vehicle-type pairs show strong co-location (CLQ 3.5–6.1, p=1.0000 against divergence). 248,503 segments = hotspots for ALL 5 types (universal dangerous infrastructure). 296,730 segments = hotspots for exactly 1 type (type-specific risk layer). Thesis interpretation: most danger is infrastructure-level and shared, but each type has a distinct risk layer on top — route divergence comes from magnitude differences + unique hotspot segments.
- **Stage 5 code written:** `code/stage5_routing/route.py`. Segment-adjacency graph (dual graph — nodes = segment IDs, not junctions). One vehicle type per run (`--type car`). Yen's k-shortest paths via `nx.shortest_simple_paths`. MCDM/AHP ranking (40% time, 40% risk, 20% hotspots). Each rank = separate toggleable Folium layer. OSM tiles background (no segment geometry loaded nationally).
- **Stage 5 known bug — MUST FIX NEXT SESSION:** All k routes appear nearly identical (risk difference ≈ 0.01–0.02). Root cause: `risk_surface_filtered.csv` zeroes out 85% of segments (below 85th-percentile threshold), so edge weights collapse to pure travel time for most of the network. Yen's finds k near-identical travel-time paths. Fix: load `risk_scores.csv` (raw GAT output) for edge weights instead. Hotspot flag (map overlay) still comes from filtered surface. This is a two-line change — deferred at user's request.
- Notable: `graph_edges.csv` is segment-to-segment adjacency (not node-to-node) — graph is the dual of the road network.
- Page: [[wiki/progress/2026-06-29]]

## [2026-06-26] ⏸ CHECKPOINT — GAT teaching session complete. Stage 3 code starts tomorrow.
- **State: Stage 2 complete. GAT concepts understood. Ready to write Stage 3 code next session.**
- **What got done today:** teaching session on GNNs and GATs — no code written. Covered: message passing + weight matrices (confirmed user's baseline was correct); node embeddings vs vehicle-type embedding table (lookup mode selector); why type embedding goes before attention (so α_ij is type-conditioned); why crash counts + embedding are both needed (evidence vs query); layer stacking rationale (2-hop context); oversmoothing risk (representations converge → segment differences lost); GAT attention weights vs basic GNN equal aggregation.
- **Next session:** Stage 3 code — `code/stage3_gat_risk_model/train.py`. Inputs: `segments.gpkg`, `crashes_segmented.csv`, `graph_edges.csv` from Stage 2.
- Notable: user understands the architecture well enough to write and reason about the code. Math internalization ongoing (more videos/reading independently).
- Page: [[wiki/progress/2026-06-26]]

## [2026-06-25] ⏸ CHECKPOINT — Stage 2 complete. Ready for Stage 3.
- **State: Stage 2 ran successfully. All three outputs produced. Ready for Stage 3 (GAT risk model).**
- **What got done today:** walkthrough of `segment.py` section by section + `data_viewer.ipynb` map cell; two bugs fixed before running (wrong OS Roads path, missing `Data/` subdirectory; wrong column rename keys — `id` not `identifier`, `road_classification` not `roadClassification`); AADF sjoin dedup fix (+553 duplicate rows from equidistant count points); `low_memory=False` to suppress DtypeWarning; timing/progress prints added throughout.
- **Stage 2 outputs:** `segments.gpkg` — 3,961,077 segments; `crashes_segmented.csv` — 885,297 rows (99.6% match rate, 3,668 dropped outside 25m); `graph_edges.csv` — 6,878,621 edges. Total runtime 103s.
- **Vehicle type counts after map-matching:** car 640k, motorcycle 85k, cycle 81k, lgv 58k, hgv 21k.
- **Notable:** 41.7% of segments used road-class-mean AADF fallback (expected — DfT count points only cover major roads; documented thesis limitation).
- **Next — Stage 3:** GAT risk model with vehicle-type-conditioned attention. Build the per-(segment, vehicle_type) risk score.

## [2026-06-24] ⏸ CHECKPOINT — Stage 2 script written, data downloaded. Deep walkthrough next session.
- **State: Stage 2 script ready. All data in place. NOT yet run — deep code walkthrough first next session.**
- **What got done today (second session):** Stage 2 script written (`code/stage2_segmentation/segment.py`); DfT AADF (`dft_traffic_counts_aadf.csv`) and count points downloaded and unzipped to `code/data/`; OS Open Roads downloading (1.03 GB, update `OS_ROADS_FILE` path in script once unzipped); requirements updated (geopandas, shapely, networkx, pyogrio, folium, mapclassify); interactive visualization cell added to `data_viewer.ipynb` (folium map, segments + crashes, layer toggle); AADF file confirmed one row per count point per year — direction-aggregation step removed from script.
- **Install before running:** `code/.venv/bin/pip install geopandas shapely networkx pyogrio folium mapclassify`
- **One thing to do before next session:** unzip OS Open Roads, find the `.gpkg` file path, update `OS_ROADS_FILE` in `segment.py`.
- **Next session:** (1) deep walkthrough of `segment.py` — every step, what it does and why; (2) run Stage 2; (3) open visualization in `data_viewer.ipynb`.
- Notable: AADF nearest-count-point join is a known accuracy limitation for minor roads — documented as thesis limitation (standard approach across all routing papers cited).

## [2026-06-24] ⏸ CHECKPOINT — Stage 1 complete. Read this first next session.
- **State: Stage 1 done. crashes_clean.csv produced. Ready for Stage 2.**
- **What got done today:** full directory restructure (PHASE1/PHASE2/old code → archive/); positioning-memo revamped to BUILD PHASE; wiki/overview.md created; code/ scaffolded with 6-stage structure + fresh .venv; Stage 1 script written, walked through, and run successfully.
- **Stage 1 output:** `code/outputs/crashes_clean.csv` — 888,965 rows, one per vehicle per crash. Columns: collision_index, latitude, longitude, vehicle_type, severity_weight, accident_year. 5 types: car (642k), motorcycle (85k), cycle (81k), lgv (58k), hgv (21k). Years: 2020–2024 (train 2020–2023, holdout 2024).
- **Key decision made:** pedal cycles added as a 5th type (code 1, 81k records — spatial divergence TBC in Stage 4 CLQ).
- **Environment:** fresh venv at `code/.venv`; run scripts with `code/.venv/bin/python`; old `.venv` at thesis root is broken (NumPy incompatibility), ignore it.
- **Next — Stage 2:** (1) download OS Open Roads from ordnancesurvey.co.uk; (2) segment the road network (homogeneous segmentation); (3) map-match crashes onto segments. New dependency: geopandas.
- Notable: thesis root `.venv` is dead — always use `code/.venv` going forward.

## [2026-06-24] ⏸ CHECKPOINT — build phase begins. Read this first next session.
- **State: positioning-memo revamped; overview.md written; directory clean. Ready to build Stage 1.**
- **What got done today:** (1) positioning-memo full revamp — grounded in now-validated niche premise (Lee 2018 + STATS19 probe) and finalized build design (GAT + type-conditioned attention); all previously-open decisions resolved or closed except DfT AADF per-type (first check in Stage 2); status updated to BUILD PHASE. (2) wiki/overview.md created — thesis argument + project state + literature landscape in advisor-handable form. (3) directory committed to git — clean state before Stage 1 starts.
- **Lee et al. 2018 PDF** added to `tier1_journal3/` (paper already deep-read 2026-06-22; PDF just arrived).
- **Two queued tasks, in order:** (1) **Stage 1 build** — data prep (clone STATS19, join tables, severity-weight, tag by vehicle type, temporal holdout split); (2) **DfT AADF per-type check** — first thing in Stage 2; drives exposure normalisation approach.
- Notable: thesis direction is fully locked, niche premise is demonstrated, build design is committed. No further reading needed before Stage 1.

## [2026-06-24] progress | Positioning-memo revamp + wiki/overview.md created
- Positioning-memo revamped: [[positioning-memo]]. Key changes: status updated to BUILD PHASE; open decisions closed (GAT unified model, ML threshold, homogeneous segmentation, per-type dispersion check, output form = ranked routes + risk map); niche premise updated from "analogical" to "demonstrated" (Lee 2018 + STATS19 probe); Build Architecture section added with all locked decisions; evidence map marked complete.
- Overview created: [[wiki/overview]]. Covers thesis argument, project state (reading done, building starting), key open question (DfT AADF per-type), and literature landscape.
- Notable: positioning-memo is now the authoritative build-phase reference. The reading-phase uncertainty language is gone.

## [2026-06-23] ⏸ CHECKPOINT — system plan complete, build files created. Read this first next session.
- **State: 6-stage build plan fully designed. Reading phase closed. Ready to start building.**
- **What got done today:** full system planning session — walked all 6 stages, resolved architecture, created build files.
- **Key architectural decisions locked:**
  - **AI core = GAT (Graph Attention Network) with vehicle-type-conditioned attention** — single unified model across all types, type embeddings condition the attention weights per message-passing step. Justified by Gao 2024 (GNN on STATS19) + Zhu 2025. Separate models per type rejected (loses cross-type relationships, hurts sparse types).
  - **Stage 4 = threshold on GAT output** (not a separate statistical significance test). GAT already does spatial smoothing through message passing — the gate is implicit. CLQ demoted to post-hoc analysis tool (generates spatial divergence maps for results section, not a production pipeline component).
  - **Stage 5 = Yen's k-shortest paths + MCDM ranking** (AHP weights + PROMETHEE). Vehicle-type-conditioned edge weights produce different ranked routes per type for the same O-D pair. Mean-excess/CVaR (Mansoor) deferred — revisit with real risk surface.
  - **LLM explanation layer = out** (supervisor direction, confirmed). Risk breakdown per route is the explainability — no language generation.
  - **RL = not used** (poor fit for offline precomputed graph routing; no corpus justification).
- **Build files created** (all in `wiki/build/`): system-overview + stages 1–6.
- **Two queued tasks (in order):** (1) positioning-memo revamp (now that build design is settled); (2) start the build at Stage 1.
- **Open data question (still unresolved):** DfT AADF per-type availability at segment level — first thing to check in Stage 2.
- Notable: system plan covers the full thesis build. The GAT + type-conditioned attention is the distinctive AI contribution on top of the vehicle-type data-niche direction.

## [2026-06-23] build | System plan completed — 6-stage pipeline designed, build files created
- Pages created: [[wiki/build/system-overview]], [[wiki/build/stage-1-data-prep]], [[wiki/build/stage-2-segmentation]], [[wiki/build/stage-3-gat-risk-model]], [[wiki/build/stage-4-risk-surface-filtering]], [[wiki/build/stage-5-routing]], [[wiki/build/stage-6-evaluation]].
- Index updated with Build Plan section.
- **Pipeline:** data prep → segmentation → GAT risk model → risk surface filtering → Yen's k-shortest + MCDM routing → evaluation (Gao + Sarraf metrics + counterfactual).
- **AI components:** GAT with vehicle-type-conditioned attention (Stage 3); threshold on GAT output (Stage 4); CLQ as post-hoc analysis only.
- **Evaluation:** precision@X% (Gao), Spearman/AO/DCG (Sarraf), counterfactual divergence test (original).
- Notable: system plan is now the primary reference for the build phase. Positioning-memo revamp is next before starting Stage 1.

## [2026-06-17] structure | Phase 3 created — pivot to risk-aware routing + data niche
- Pages: [[PHASE3/PLAN]], [[PHASE3/positioning-memo]] (living), [[PHASE3/index]], this log.
- **Trigger: 2026-06-17 supervisor meeting** (after presenting the Phase 2 CRM/LLM memo).
  Decoded: (1) **drop the LLM** — faithfulness/hallucination unsolvable in the time,
  language is distracting + per-person, not solidified enough to anchor a thesis;
  (2) **route planning is the home** ("very good"); (3) **complexity over novelty** —
  "I don't always need novelty, but I always need complexity of the system"; (4) **find a
  data niche nobody explored** — e.g. condition routing on **vehicle type** (his example);
  (5) other datasets OK to open more niches if needed.
- **New direction:** risk-aware route planning (home = Jiang 2022 / Sarraf 2020), with
  **vehicle-type-conditioned segment crash risk** as the novelty, STATS19 as the engine
  (Gao 2024 lineage), **no NL/LLM layer**, output = ranked routes / vehicle-specific risk
  map. Full living statement in [[PHASE3/positioning-memo]].
- **Corpus status (honest):** risk-modeling lit is well-covered (inherited from Phase 2);
  the routing *home* (Jiang deep + Sarraf/de Souza abstracts) and the vehicle-type *niche*
  (Zhu abstract) are THIN → the target of this reading pass. Phase 2 deep reads on the
  LLM/explanation half (Zhang/Gyawali/Hussien/Smetana/Wu/TrafficRiskGPT/Tab-Text) are
  demoted to future-work.
- **Combining niches (user Q):** allowed and encouraged as a complexity feature, BUT
  multi-dimensional conditioning multiplies STATS19 sparsity (~96% zero-inflation, fatal
  ~1.5%) → design rule: vehicle type primary, weather/time secondary only where a per-cell
  count is significant, with graceful fallback. Logged in PLAN + positioning.
- Notable: **Next — Tier 1 reading pass (T-ITS, TR-C, AAP, ESWA) on routing + vehicle-type
  keywords.** Mirror Phase 2's lightweight per-journal `*-abstract-refs.md` records.

## [2026-06-22] ⏸ CHECKPOINT — TIER 1 CLOSED, reading phase done, system planning underway. Read this first next session.
- **State: all of Tier 1 swept (T-ITS · TR-C · AAP · ESWA). Reading phase essentially complete. Pivoted to designing the build.**
- **What got done today:** (1) finished the AAP sweep — keywords 3–5 (noise; `heterogeneity` = *statistical* het.,
  a semantic mis-hit) + the spatial-divergence keyword `motorcycle crash hotspot` → **deep-read Lee et al. 2018
  (AAP), THE spatial-divergence brick** (vehicle-type hot zones "substantially different across types," statewide
  Florida; donates EPP per-type screening gate). Niche premise upgraded *analogical → demonstrated*. (2) ESWA light
  pass: 2 keywords, both return only Sarraf (already deep-read) → **Tier 1 CLOSED**, recorded in new
  [[tier1_journal4/ESWA-abstract-refs]]. (3) **Direction validated on real data** — an informal STATS19 per-type
  probe (deliberately NOT written up as a wiki artifact, per user's call) confirmed the divergence **survives at
  segment level, beyond chance, volume-controlled**: motorcycle crashes 72% urban vs HGV 61% rural; moto~HGV per-cell
  count correlation 0.24 (vs 0.41 random) → types actively spatially segregated; HGV is the sparse one (≈80–91% of
  cells zero-HGV → the real engineering risk). So: gap is REAL and worth building; HGV sparsity is the thing to engineer around, not an existential threat.
- **Corpus standing:** ~14 deep reads + ~25–30 abstract keepers ≈ 40 citable papers (the user worried 8 was too few
  — clarified: deep-reads ≠ citations; the abstract tier is the breadth/citation layer and counts). Reading is
  *sufficient to start the build*; remaining reads happen just-in-time during the build.
- **SYSTEM PLANNING — where the teaching conversation paused (resume here):** Established the mental model and the map:
  - **Two halves:** OFFLINE = build per-vehicle-type risk maps (the "engine": Gao/Jiang/Pathivada/Barabino + count
    models + gates); ONLINE = answer a route query fast (the "router": Sarraf/Mansoor). Precompute the expensive
    statistics offline; leave only cheap path arithmetic for live.
  - **6-stage pipeline:** (1) data prep [≈done in probe — join tables, tag crash by vehicle involvement, severity-weight,
    keep collision_year for temporal holdout]; (2) **segmentation** [RECOMMENDED: **homogeneous road segments**
    (Pathivada) — real road so the router is happy, pooled so less sparse, HSM-standard/borrowed; with **EB shrinkage
    toward a coarse unit** to rescue sparse HGV. Needs OS Open Roads + map-matching crashes onto links. Build order
    suggested: v1 grid → v2 homogeneous segments]; (3) per-type risk modeling; (4) significance gate; (5) routing;
    (6) evaluation.
  - **PAUSED mid-bridge into Stage 3.** Pending question posed to the user: *why can't you just use the raw
    severity-weighted crash count as a segment's risk score?* **Intended answer (for resume):** two problems — (a) the
    **count/noise** problem they saw in the probe (sparse types → a raw count of 1–2 is mostly randomness, and
    dispersion regime varies by type: NB/ZITD for over-dispersed car/moto vs CMP/HTCMP for under-dispersed HGV — raw
    count ignores all this); (b) the **fairness-between-roads / exposure** problem — a road with 7 moto crashes and
    10k motorcycles/day is *safer* than one with 3 crashes and 100/day; raw count confounds risk with volume →
    must normalise by per-type exposure (DfT AADF by vehicle type — still an open data-availability check).
- **Two queued tasks, in order:** (1) **finish the system plan** (Stages 3→6), then (2) **full positioning-memo
  revamp** grounding the now-validated direction + the finalized technical/build design (deferred deliberately so the
  memo can bake in real build decisions, not literature guesses). Memo NOT touched today, per user.
- Bookkeeping today: AAP-abstract-refs (kw 3–6 + Lee→deep-read), AAP-deepread §3 + net-effect, positioning-memo
  (niche premise/reframe/evidence-map/gate table — Lee + EPP), index, ESWA-abstract-refs (new), this log. Not yet
  committed to git (EOD commit pending).

## [2026-06-22] reading | AAP sweep COMPLETE — the spatial-divergence brick found (Lee 2018)
- Records: [[AAP-abstract-refs]] (kw 3–6) + [[tier1_journal3/AAP-deepread]] (§3 Lee 2018).
- **Keywords 3–5 (`truck/HGV crash risk`, `vehicle type crash heterogeneity`, `vulnerable road user crash`):**
  noise. Critical lesson — **keyword 4 was semantically wrong**: "heterogeneity" in AAP = *statistical*
  unobserved heterogeneity (random parameters/latent class), NOT inter-vehicle-class differences. ~240
  titles across the three, only abstract-level keepers: Network-wide screening framework (P×S×E, method-borrow),
  French fatality-by-user-type (MTW 20–32× car, niche-premise strong), pro-vs-regular two-wheeler France/UK
  (demand-side), cyclist Poisson-Tweedie Lisbon (count-model brick — cyclists OVER-dispersed vs motorcycles
  UNDER-dispersed → confirms count family varies by type). 0 full-text from these three.
- **Keyword 6 `motorcycle crash hotspot` (SPATIAL-DIVERGENCE cluster — the one that was mis-prioritised earlier):**
  3 abstract keepers + **1 full-text → DEEP-READ (Opus): Lee, Yasmin, Eluru, Abdel-Aty & Cai 2018 (AAP 111:12–22).**
  - ★★★ **THE BRICK.** Mixed MNL fractional split on crash *proportions* by vehicle type, 8,129 TAZs statewide
    Florida, 8 types. **"the spatial pattern of hot zones is substantially different across vehicle types"** —
    HGV→rural, bicycle→metro, pedestrian→urban, motorcycle→rural. First real-data evidence in the whole corpus
    that vehicle-type hot zones diverge *as places*. **Upgrades the niche premise from analogical → demonstrated.**
  - Donates **EPP (Excess Predicted Proportion)** = observed − predicted proportion per type, HSM-analogous →
    significance/screening gate candidate #5 (inherently per-type, divergence-revealing; needs a fitted model,
    so complements model-free CLQ).
  - Limits keeping work for us: TAZ macro not segment; proportion not exposure-normalised risk; no routing. →
    *segment-resolution + GB/STATS19 + routing exploitation* is still the open space.
  - Also abstract-only: CLQ-on-crash-severity (College Station — validates CLQ on crash categorical data, Hu 2018
    stays primary ref); "A review of spatial approaches in road safety" (landscape reference).
- **Net moves:** (1) niche premise reframe — no longer "thin/manufacture it ourselves," now "replicate a
  demonstrated effect at finer resolution + exploit for routing" (much safer); (2) EPP added to gate shortlist
  (Wei/Wang/Hu-CLQ/EB/**EPP**); (3) count-family-varies-by-type reconfirmed (cyclist over- vs motorcycle
  under-dispersion).
- **Gap test holds at its strongest:** across T-ITS + TR-C + AAP, the spatial divergence is now *proven* (Lee)
  but **nobody routes on it**, and nobody does it at segment level — the segment + routing combo is the thesis.
- Bookkeeping: AAP-abstract-refs (kw 3–6 + Lee → deep-read), AAP-deepread §3 + net-effect, positioning-memo
  (niche premise paragraph, reframe note, evidence-map row, gate table + Open Decision #3), index (+footer), log.
- Notable: **AAP Tier-1 journal DONE.** Next — light ESWA pass (Sarraf already deep-read), then the **STATS19
  per-type density probe** (Open Decision #6): now a *segment-level confirmation* of Lee's TAZ-level divergence
  + dispersion/zero-rate measurement (picks ZITD vs CMP) + CLQ/EPP per-type screening.

## [2026-06-19] ⏸ CHECKPOINT — end of day, read this first next session
- **State: AAP (Tier 1, Journal 3) sweep STARTED — keywords 1–2 of 5 done; both full-text keepers deep-read.**
- **What got done today:** (1) AAP keyword 1 `risk aware route planning` → 1 abstract keeper (Changsha
  demand-side), confirmed AAP isn't a routing-system venue; (2) AAP keyword 2 `motorcycle crash risk segment`
  → 5 abstract keepers + 2 full-text deep reads (Opus): **Pathivada 2025** (motorcycle segment SPF;
  per-type slice → **under-dispersion** → CMP/HTCMP not NB/ZITD; EB ranking; homogeneous segmentation) and
  **Barabino 2021** (★★ **R=H·V·E** per-bus-route risk → section-sum → quartile ranking = closest
  per-type→route-risk→ranked-output precedent). New folder `tier1_journal3/` with `AAP-abstract-refs.md`
  + `AAP-deepread.md`.
- **Decisions moved:** count model is now a **per-type choice, not a default** (new Open Decision #3b:
  ZITD vs CMP/HTCMP — measure dispersion in the probe); **EB** added as significance/screening gate
  candidate #4; **homogeneous segmentation** = cheap HSM-aligned answer to segment-definition #2; exposure
  confound reconfirmed (both papers use aggregate exposure). The **H·V·E decomposition** is now a concrete
  thing to adopt for the route-risk scalar.
- **Where each layer stands (unchanged headline):** routing home = STRONG; engine = solid (Gao) **+ now a
  per-type count-family fork (CMP/HTCMP) when under-dispersed**; significance gate = 4 candidates (Wei, Wang,
  Hu-CLQ, EB). **NICHE = still thin where it's load-bearing** — these confirm motorcycle *segment risk* is
  buildable but give NO **spatial-divergence-by-type** (different segments risky for different types).
- **Resume plan (next session):** (1) **AAP keywords 3–5** = top priority — `truck/HGV crash risk`,
  `vehicle type crash heterogeneity`, `vulnerable road user crash` — hunting the spatial-divergence brick;
  (2) light ESWA pass (Sarraf already deep-read); (3) then **STATS19 per-type density probe** (Open Decision
  #6) — and now it must report **per-type dispersion + zero rate** (picks ZITD vs CMP), plus the CLQ
  divergence analysis (generates the niche evidence + headline).
- **Two outstanding decisions (carried):** time-optimization axis (contribution vs borrow); per-type exposure
  (DfT AADF by vehicle type?).
- Nothing half-written; abstract-refs, deep-read record, positioning-memo, index, log all consistent. Committed + pushed at EOD.

## [2026-06-19] reading | AAP Tier-1 sweep started (kw 1–2) + 2 deep reads
- Records: [[AAP-abstract-refs]] (sweep) + [[tier1_journal3/AAP-deepread]] (full reads), new `tier1_journal3/`.
- **Keyword 1 `risk aware route planning`:** ~90 titles, 1 abstract keeper (Changsha ALPR — motorists
  do trade efficiency for safety at night/non-livelihood → demand-side brick, complements Kavta). AAP
  is not a routing-system venue (confirmed).
- **Keyword 2 `motorcycle crash risk segment`:** 5 abstract keepers + **2 full-text → deep-read (Opus):**
  - **Pathivada et al. 2025 — motorcycle segment SPF (Kentucky).** ★ Key finding: motorcycle-only
    segment crashes were **UNDER-dispersed** (variance < mean) → NB/ZITD (built for over-dispersion)
    inappropriate; needs **CMP/HTCMP**. First *real-data* signal that the per-type slice can **flip the
    count regime** → directly feeds Open Decision #6. Also donates **Empirical Bayes** high-crash ranking
    (gate/screening candidate #4, HSM-standard) + **homogeneous segmentation** (cut where road class/lanes/
    speed/AADT changes → cheap answer to #2). Caveat: controlled zeros to ~20% (not STATS19's true rate);
    aggregate-AADT exposure = per-type exposure confound again. Single-type, no divergence, no routing.
  - **Barabino et al. 2021 — bus crash risk, real network.** ★★ **structural precedent**: per-vehicle-type
    **R = H·V·E** (NB frequency × binary-logistic severity × passenger·km exposure), computed per
    homogeneous section → **summed to route risk** → quartile-cut 4-level ranking. The closest existing
    per-type → route-risk → ranked-output pipeline in the whole corpus (bus-only, fixed lines = *screening,
    not routing*). Donates the **H·V·E decomposition + section-sum + binary-severity collapse** for rare
    fatals. Bonus brick: third-party vehicle type shifts severity odds (heavy-veh 1.91×, 2/3-wheeler 2.16×
    vs car) = another "type matters."
- **Net moves:** (1) count model is now a **per-type decision, not a default** (ZITD vs CMP/HTCMP, measure
  dispersion in the probe → added Open Decision #3b); (2) EB joins the significance-gate shortlist (#4 with
  Wei/Wang/Hu-CLQ); (3) a complete per-type route-risk scalar (H·V·E) is now in hand to adopt; (4) exposure
  confound reconfirmed (both papers use aggregate exposure).
- **Niche still thin where it's load-bearing:** these confirm motorcycle *segment risk* is buildable, but
  give **no spatial-divergence-by-type** (different segments risky for different types). That's keywords 3–5
  + the CLQ-on-STATS19 probe. Gap test holds: no cross-type routing anywhere.
- Bookkeeping: deep-read record, abstract-refs (kw1+kw2, full-text → deep-read), positioning-memo (niche +
  gate tables, Open Decisions #2/#3/#3b/#6), index (+footer), log.
- Notable: **Next — AAP keywords 3–5** (`truck/HGV crash risk`, `vehicle type crash heterogeneity`,
  `vulnerable road user crash`), hunting the spatial-divergence brick; then light ESWA pass + STATS19 probe.

## [2026-06-18] ⏸ CHECKPOINT — end of day, read this first next session
- **State: Tier 1 Journals 1 (T-ITS) + 2 (TR-C) fully swept; all keepers deep-read.** Big productive day.
- **What got done today:** (1) deep-read all 6 carry-over PDFs → 3 per-journal records (T-ITS/ESWA/AAP);
  (2) filed standing+gap query [[2026-06-18-where-we-stand-and-remaining-gaps]] + sharpened PLAN keywords
  (added spatial-divergence + segmentation clusters; flagged feasibility = not-a-reading-question);
  (3) T-ITS sweep (4 kw → 1 weak keeper); (4) TR-C sweep (3 kw) → **5 deep reads**: Mansoor 2026 ★★★
  (class-specific route sets + mean-excess CVaR = the per-type routing mechanism), Sohrabi & Lord 2022
  (operational home; 8%→+23%), Kavta 2025 (demand-side niche), Chandra 2014 (user-conditioned routing +
  Pareto/Yen machinery), Hu 2018 (★ Colocation Quotient = per-type spatial significance gate / tool to
  GENERATE niche evidence); (5) pinned **Scope & depth** in positioning-memo and **corrected the
  novelty language** → distinctive *direction* (borrowed methods, new data) vs breakthrough novelty
  (not required); premise concern = **justification (does it diverge?), not novelty.**
- **Where each layer stands:** SYSTEM/routing home = STRONG (engine→router structure + per-type
  mechanism located). ENGINE = solid (Gao). SIGNIFICANCE GATE = 3 candidates (Wei case-crossover, Wang
  χ²-BN, Hu CLQ). **NICHE (vehicle-type) = still the thin spot** — only analogical premise evidence;
  but reframed (CLQ lets us manufacture it on STATS19).
- **Gap test (strongest yet):** T-ITS+TR-C, 2010–2026, **no paper routes on a data-driven per-vehicle-
  type risk surface.** White space confirmed; Mansoor hands the mechanism.
- **Resume plan (next session):** (1) **AAP vehicle-type sweep = top priority** — `motorcycle crash
  hotspot`, `vehicle class network screening`, `truck/HGV crash risk`, `vehicle type crash heterogeneity`
  (direct per-class evidence should live here); (2) light ESWA pass (Sarraf already deep-read); (3) then
  **STATS19 data analysis** — run the per-type density probe EARLY (Open Decision #6, feasibility +
  existential) and the CLQ divergence analysis (do motorcycle vs HGV vs car hotspots differ?) =
  generates the niche evidence + the headline result.
- **Two outstanding decisions:** time-optimization axis (contribution vs borrow → add routing-OR keyword
  cluster or not); per-type exposure (DfT AADF by vehicle type?).
- Nothing half-written; all records, evidence map, index, log consistent. Committed + pushed at EOD.

## [2026-06-18] reading | TR-C deep read — Hu 2018 colocation (method donor) + premise reframe
- Appended to [[TR-C-deepread]]. **Full read corrected the keeper note:** the results **combine** ped+cyclist
  and condition on **severity × intersection-type** (not ped-vs-cyclist, not motor-vehicle classes) → premise
  is **analogical, not direct.**
- **The prize is the METHOD — Colocation Quotient (GCLQ + LCLQ).** A per-category **spatial significance
  test**: "does crash-type A significantly colocate with feature-type B vs random?", expected value 1,
  **Monte-Carlo** p-values, **network-distance**, micro-level (**MAUP-aware**). → candidate **significance
  gate #3** (with Wei case-crossover, Wang χ²-BN) + input to **segmentation** decision; ties to Phase-1
  spatial/Cramér's-V assets.
- **Premise reframe (important):** spatial-divergence-by-type being thin in the literature is NOT evidence
  it's false — colocation-in-transport-safety is itself new (2018, "first effort"). **The thesis can
  MANUFACTURE the premise** by running CLQ on STATS19 per vehicle type. This makes the per-type density
  probe (Open Decision #6) doubly central: feasibility check *and* first step of producing niche evidence.
- Bookkeeping: deep-read record, abstract-refs status, positioning-memo (evidence map + reframe note +
  Open Decision #3 now lists CLQ), index, log.
- Notable: **TR-C fully done + all its keepers deep-read.** Next Tier-1 priority = AAP vehicle-type niche
  (motorcycle/HGV segment risk; spatial-divergence keywords) — and now we have the CLQ tool to apply to it.

## [2026-06-18] reading | TR-C keyword 3/3 (`crash risk routing`) — TR-C sweep COMPLETE
- Appended to [[TR-C-abstract-refs]]. Keyword mostly returns crash-*prediction* (Abdel-Aty/Quddus engine
  lineage, have Gao) + AV/behaviour noise; most routing hits already deep-read. **2 new keepers:**
  - ⏳ **Hu, Zhang, Shelton 2018 — dangerous intersections for pedestrians vs cyclists (colocation).**
    Full-text pending. Best **spatial-divergence-by-type** evidence yet + **colocation-quotient** method
    (per-type spatial significance test → significance-gate/segmentation candidate; ties to Phase-1 spatial
    assets). Caveats: ped/cyclist not motor-vehicle class; hotspot not routing.
  - ✓ **Yang, Ye, Zhao 2015 — speed limits/selection + network equilibrium** (abstract). Class-specific
    crash risk in route+speed choice at equilibrium = predecessor to Mansoor; speed→crash mechanism.
- **TR-C COMPLETE — all 3 keywords swept.** Tally: 4 deep-read (Mansoor, Sohrabi&Lord, Kavta, Chandra) +
  Hu pending full-text + abstract keepers (Dijkstra, Yang, bi-attribute NYC, NL Sustainable-Safety, hazmat
  CVaR). Gap test across 2010–2026: established crash-risk-routing/equilibrium + spatial-crash lineage,
  **vehicle type = the unfilled slot**; no motor-vehicle-class routing anywhere.
- Notable: awaiting Hu PDF. Next Tier-1 priority = **AAP vehicle-type niche evidence** (motorcycle/HGV
  segment risk; spatial-divergence keywords) — the one premise still thin.

## [2026-06-18] reading | TR-C keyword-2 deep read — Chandra 2014 + Scope&depth pinned
- Record: appended to [[TR-C-deepread]]. Also pinned **Scope & depth** section in [[positioning-memo]]
  (niche=novelty/risk layer; routing=system/complexity layer; both credible; depth-in-risk buys novelty,
  depth-in-routing buys complexity only — resolves the "optimization vs niche" confusion).
- **Chandra 2014 — closest user-conditioned routing precedent, but parametric.** Safe path-finding for
  two user types (older drivers, bicyclists), differentiated ONLY by speed + perception-reaction time;
  safety indicators are **generic, crash-data-free** (TTC from Poisson/GUE traffic density), **no per-type
  risk surface.** Strengthens the niche 3 ways: (1) gap brick — even the user-framed paper has no per-type
  risk surface; (2) contrast — Chandra avoids crash data, we exploit STATS19 per-type history (our novelty
  crystallises against it); (3) donates the **multi-objective Pareto/non-inferior shortest-path machinery**
  (Yen's p-shortest-paths → Pareto filter) for the routing layer + a crash-data-free TTC indicator as
  graceful-fallback material.
- **Gap test now spans 2014–2026, 4 papers, none with a data-driven per-vehicle-type risk surface in routing.**
- Bookkeeping: deep-read record, abstract-refs status, positioning-memo evidence map + scope note, index, log.
- Notable: TR-C keyword 3/3 `crash risk routing` still pending.

## [2026-06-18] reading | TR-Part-C keyword 2/3 (`risk-based navigation`) + time-axis flag
- Record appended to [[TR-C-abstract-refs]]. ~90% maritime/aviation/UAV/AV-control noise. 2 strong
  abstracts → **1 full-text keeper** (Safety-based path finding for older drivers & bicyclists —
  user-class-conditioned safe routing, crash-data-free indicators; PDF incoming) **+ 1 downgrade**
  (Adaptive vehicle routing for risk-averse travelers = travel-time reliability, not crash).
- **Gap-strengthening nuance:** the older-driver/bicyclist paper's safety indicators are "generic
  irrespective of road user type" → user-*motivated*, not user-*conditioned* in the risk layer. Even
  the vulnerable-road-user routing paper doesn't compute a per-type risk surface → niche still open.
- **Time-optimization axis flagged (user question):** math-heavy time+safety joint optimization is
  anchored by Mansoor 2026 (METT+MECRC/VI) + Sarraf (MCDM) + hazmat CVaR; the standalone routing-
  optimization literature (multi-objective/Pareto/time-dependent/stochastic shortest path) is NOT yet
  a swept pillar. Decision pending: routing optimization as contribution (add keyword cluster) vs
  borrowed component (Mansoor+Sarraf suffice).
- Notable: awaiting older-driver/bicyclist PDF; then keyword 3/3 `crash risk routing`.

## [2026-06-18] reading | TR-Part-C deep reads — 3 full-text from keyword 1
- Record: [[TR-C-deepread]] (`raw/papers/tier1/tier1_journal2/`). All 3 promoted papers now read in full.
- **Mansoor, Li, Chen 2026 ★★★ — the structural ancestor.** Class-specific route choice sets (route
  enters class m's set iff its safety score Θ ≥ class threshold Θ_req) + mean-excess CRC (CVaR on the
  fatal/serious tail), generalized cost = METT+MECRC, VI/two-stage. Classes by *safety preference*, not
  vehicle type — **re-key Θ_req on vehicle type = the per-type routing mechanism.** Also borrowable: the
  Dijkstra-2013 roadway-characteristic safety score (road-class shares + distance + intersection density;
  crash-data-FREE). Names heavy-vehicle risk in motivation; vehicle type absent even from future work.
  Scale caveat: network equilibrium/assignment, not individual navigation → conceptual ancestor, Sarraf
  stays the operational router.
- **Sohrabi & Lord 2022 — operational home + motivation.** 29,382 Texas segments; NB crash models
  **stratified by weather** (adverse vs clear; adverse 2.7× rate); route risk = complement of product of
  segment survival probs; safest≠shortest, **8% time → +23% crash**, safest route varies by weather. S-RGS
  requirement list ≈ thesis build spec. Dominique Lord co-author. No vehicle type.
- **Kavta et al. 2025 — demand-side niche brick.** SP experiment, delivery riders (Amsterdam/Copenhagen)
  trade time for safety (VRR/WTA); proves a vehicle class *wants* type-specific safe routing. Industry
  co-author (Just Eat Takeaway). Behavioural, not a build method.
- **Routing home now = 5 deep-read papers** (Jiang, Sarraf, + these 3). Gap test strongest yet: machinery
  + acknowledged heavy-vehicle risk exist, but unconnected — that connection is the thesis.
- Bookkeeping: TR-C-abstract-refs status → deep-read; positioning-memo evidence map + structural note
  updated; index + log. Notable: next TR-C keyword 2/3 `risk-based navigation`.

## [2026-06-18] reading | TR-Part-C sweep (Tier 1, Journal 2) — keyword 1/3
- Record: [[TR-C-abstract-refs]] (`raw/papers/tier1/tier1_journal2/`). Keyword: `safe route planning`
  (re-phrased from `safe routing`, which mis-fired into VANET secure-packet-routing — networking sense).
- **The routing HOME finally appears by title.** 8 safe-routing abstracts pulled → **3 promoted to
  full-text** (pending download): (1) **mean-excess network-equilibrium, class-specific safe routing**
  = structural ancestor of per-type routing ★; (2) **Navigating to Safety** (Texas 29k seg; 8% time →
  +23% crash; weather-varying) = home + motivation stat; (3) **food-delivery riders SP** = demand-side
  niche brick (a vehicle class wants type-specific safe routes). 3 abstract-only keepers (bi-attribute
  NYC; NL Sustainable-Safety; hazmat-CVaR borrow); 2 hazmat skip-logged.
- **Gap-test synthesis (strongest yet):** 8 safe-routing papers ~2008–2024, **none route by vehicle
  type**; the mean-excess paper even hands over the mechanism (class-specific route sets + crash-risk
  tail) to fill the gap, re-keyed on vehicle type.
- Notable: keyword 1/3 done; next `risk-based navigation`. 3 PDFs to fetch.

## [2026-06-18] reading | T-ITS Phase-3 sweep (Tier 1, Journal 1) — all 4 keywords
- Record: [[T-ITS-abstract-refs]] (`raw/papers/tier1/tier1_journal1/`).
- Keywords: `risk-aware route planning` (0) · `safest path routing` (0) · `safety-aware navigation`
  (0, AV-control/perception/maritime noise) · `vehicle type crash risk` (1 weak).
- **Result: 0 full-text keepers, 1 weak abstract-only keeper** — "Defining TTC Thresholds by Type of
  Lead Vehicle" (vehicle type modulates risk, but micro-TTC/non-lane-based → `niche-premise (weak)`).
  Jiang 2022 + Li 2025 re-surfaced (already in corpus).
- **Gap-test brick:** no vehicle-type *segment-risk* or *routing* paper on T-ITS under any keyword;
  confirms spatial-divergence premise must come from AAP / J. Safety Research (as predicted).
- Notable: T-ITS done. Next journal in Tier 1.

## [2026-06-18] query | Standing + gap analysis; reading-plan stress-test → keywords sharpened
- Page: [[wiki/queries/2026-06-18-where-we-stand-and-remaining-gaps]].
- **Question:** before reading more, where do we stand and will the PLAN keywords uncover the gaps?
- **Answer:** literature gaps (premise, TR-C routing gap test, eval) ARE covered — but two holes found:
  (1) the niche premise keywords only find "types differ in factors/severity," NOT the load-bearing
  **spatial-divergence** claim (different segments risky for different types); (2) segment-definition
  decision was only brushed. **And the biggest existential risk — per-type STATS19 density — is
  structurally OUTSIDE reading; only a data probe answers it.**
- **Actions:** PLAN.md — added a **spatial-divergence** keyword cluster (#1 priority: `motorcycle crash
  hotspot`, `vehicle class network screening`, `crash hotspot vehicle type spatial`, `vehicle-type crash
  spatial distribution`) + a **segmentation** cluster (`crash hotspot DBSCAN`, `road segmentation crash
  risk`, `spatial unit crash analysis`); recorded the "reading CANNOT resolve feasibility" caveat.
  positioning-memo — added **Open Decision #6** (per-type density probe + per-type exposure confound).
- Notable: **probe is parallel-tracked, not post-reading** — it covers a gap reading can't.

## [2026-06-18] reading | Deep-read all 6 carry-over PDFs → 3 per-journal records
- **Downloaded the two missing CORE papers** (Sarraf 2020 ESWA, Zhu 2025 T-ITS); all 6 carry-over
  PDFs now in `raw/papers/carry_over/`. Read all 6 in full (pdftotext extraction).
- **Records created** (per-journal, context + technical grounding): [[T-ITS-deepread]],
  [[ESWA-deepread]], [[AAP-deepread]].
- **Three findings that move the thesis:**
  1. **Jiang ≠ a router.** It outputs a risk score → heat map; routing is its own future work.
     The router is **Sarraf** (Dijkstra + MCDM). So the assembled stack = **engine (Jiang/Gao) →
     router (Sarraf)**, and the thesis conditions *both* on vehicle type. Jiang also **names our
     gap verbatim**: "risks are not dependent on … vehicle types or weather conditions."
  2. **Sarraf routes everyone the same** — WCR normalises by AADT but has **no vehicle-type term**.
     Strongest "slot is open" brick; we adopt its WCR (per type), AHP/PROMETHEE ranker, and
     Spearman/Average-Overlap/**DCG** eval suite (DCG = headline, it penalises a risky route ranked high).
  3. **Zhu reframed (honest downgrade):** "vehicle-**group**" = dynamic interaction clusters
     (trajectory/iTTC, real-time), NOT vehicle **type**; type is 1 of 8 node features. → weak niche
     premise, strong method-cousin (GNN+GNNExplainer). **Vehicle-type-heterogeneity evidence is
     still THIN** and is now the explicit reading priority.
- **Technical bridges locked:** Gao/Sarraf/STATS19 all severity-weight crashes into one segment
  scalar (Gao 1/2/3; Sarraf 30/15/5/2) → we compute it **per vehicle type**, ideally with per-type
  exposure. Gao = ZITD for ~96% zero-inflation + MPIW/PICP/AccHR@20 metrics. Wei = case-crossover
  matched-control gate; Wang = χ²-CI Bayesian-network gate (Bonferroni; BDs for sparse cells) →
  the two candidate significance gates for vehicle-type × condition cells.
- **Bookkeeping:** positioning-memo evidence map updated (all 6 → deep-read; Zhu premise reframed;
  engine-vs-router structural note added); index + this log updated.
- Notable: **Next — start the Tier 1 reading pass proper** (T-ITS / TR-Part-C / AAP / ESWA), top
  priority = motorcycle/HGV/vehicle-type *segment-risk* papers to fill the thin niche-evidence base.

## [2026-06-17] ⏸ CHECKPOINT — end of day, read this first next session
- **State: Phase 3 is fully scaffolded and ready to start reading.** Nothing committed to git
  (by choice — all saved to disk on the work machine).
- **Files in place:** [[PHASE3/PLAN]], [[PHASE3/positioning-memo]] (living), [[PHASE3/index]],
  this log, and `raw/papers/carry_over.md` + `raw/papers/carry_over/` (4 full-text PDFs:
  Jiang2022, Gao2024, Wei2024, Wang2025).
- **Carried-over papers — status:** the 4 deep-read papers that had PDFs are copied in full;
  all other surviving papers were abstract-only in Phase 2 (no PDF ever existed) and live as
  text in `carry_over.md`. **Two abstract-only papers are now CORE and must be downloaded:
  Sarraf & McGuire 2020 (ESWA — routing layer + eval metrics) and Zhu et al. 2025 (T-ITS —
  vehicle-type niche premise).**
- **Housekeeping done:** CLAUDE.md now points the active phase at PHASE3 (Phases 1 & 2 = read-only
  archives); PHASE2/positioning-memo.md got a SUPERSEDED banner; project memory + MEMORY.md index
  rewritten to the Phase 3 state.
- **Resume plan:** (1) re-read PLAN + positioning-memo; (2) read the 4 carried PDFs (Jiang = home,
  Gao = engine first); (3) download Sarraf 2020 + Zhu 2025; (4) begin Tier 1 reading pass
  (T-ITS, TR-Part-C, AAP, ESWA) on routing + vehicle-type keywords, recording lightweight
  per-journal `*-abstract-refs.md` files.
- **Direction recap (one line):** risk-aware route planning (home), novelty = vehicle-type-
  conditioned segment crash risk, STATS19 engine (Gao lineage), NO LLM, output = ranked routes /
  vehicle-type risk map; supervisor's bar = complexity of the system over novelty.
