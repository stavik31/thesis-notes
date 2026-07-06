---
title: "2026-07-04 — Testing the clustering direction: feature-based clustering falsified, location-based clustering + share-target XGBoost validated"
type: progress
date: "2026-07-04"
tags: [progress, experiment, decision]
---

# 2026-07-04 (night session) — Testing the clustering direction end to end

Direct continuation of [[wiki/progress/2026-07-04]] (the supervisor-meeting redirect toward
per-type clustering). This session actually built and tested that direction — all of it ad hoc,
in Bash/Python, nothing committed to the codebase yet. It ends with a validated, holdout-tested,
routing-tested result, but it is **not the plan as originally written** — the plan's literal
mechanism (feature-based clustering) was tested and falsified; what actually works is a different
mechanism (location-based clustering) discovered through iteration. Read this note in full before
picking the work back up — several early results in this session were later found to be wrong or
methodologically shaky and corrected; the numbers below are the corrected, final ones, with the
wrong ones kept in the test log for context on what NOT to repeat.

**Headline: discrete, network/location-based clusters per type (not feature-based) + predicting
each type's SHARE of the cluster's all-type crash total (not raw count or rate) + fully separate
per-type XGBoost models beats every method tested to date — best-GAT, Empirical Bayes, ad hoc
smoothing, and the plan's own literal clustering design. Validated on a genuine spatial holdout
(an entire city held out from training) and on an actual end-to-end routing test (3.10/5 types
take distinct routes, vs. best-GAT's 2.00/5).**

---

## Test log, in order run (corrected numbers; see "process notes" for what was wrong along the way)

All ρ/Jaccard figures are mean pairwise cross-type Spearman correlation / top-N hotspot Jaccard,
same methodology as [[wiki/progress/2026-07-03]], measured on the 158,237 segments with ≥1 crash
2022-23 unless stated otherwise (lower ρ = more divergence preserved = better).

### 1. The plan's literal mechanism (Steps 1-3: feature-based clustering) — FAILS

| variant | ρ | Jaccard |
|---|---|---|
| Cluster by road_class + own-AADF + length, rate-normalised | 0.896 | 0.183 |
| Same, minus road_class (own-AADF + length only) | 0.791 | 0.166 |
| Same clusters, pooled raw count instead of rate | 0.791 | 0.047 |
| Same clusters, **share** of all-type total instead of rate/count | 0.656 | 0.012 |

Even with share-reframing (the GAT fix), feature-based clustering never gets close to best-GAT's
0.377. **Diagnosis:** car/lgv/hgv's own-AADF values are themselves highly correlated with each
other in reality (busy roads carry lots of cars *and* vans *and* trucks at once — confirmed via
direct correlation check: car-lgv AADF r=0.977, car-hgv r=0.82). Clustering by AADF-quantile
similarity (even each type's own AADF) assigns segments to similarly-ranked bins across types,
which is why it collapses. **This directly falsifies the plan's Step 2 assumption** that
feature-based clusters can be "geographically scattered by design" without cost — see mechanism
section below.

### 2. Location-based smoothing (not clustering, continuous) — the breakthrough

| variant | ρ | Jaccard |
|---|---|---|
| Network 2-hop smoothing (own crash history, no model, no clustering) | **0.181** | 0.085 |
| Adaptive-radius network smoothing (Step 2's data-sufficiency logic, location as axis) | 0.289 | 0.078 |

Pooling by **road-network proximity** instead of feature similarity beat every model tested,
including best-GAT (0.377), using literally no learned parameters — just an average of neighbours'
crash counts. This matches 07-03's own diagnostic ladder (1-hop=0.191, 2-hop=0.221) and the ad hoc
smoothing baseline from that session almost exactly, now confirmed at national scale.
**Counter-intuitive finding: the adaptive/expanding version is *worse* than the flat one** —
chasing "30 crashes" pushed nearly every segment (even car, the densest type) out to the maximum
radius tested, because national crash density is too sparse for that bar to be cleared locally.
Bigger radius = more oversmoothing = worse divergence preservation. Statistical stability and
divergence-preservation pull in opposite directions here; specificity (small radius) wins.

### 3. Discrete (non-overlapping) network clusters — real partitions, not continuous smoothing

| variant | ρ | Jaccard |
|---|---|---|
| Discrete clusters (BFS-grown per type until 30 crashes), pure statistical rate | 0.247 | 0.016 |
| Same clusters + XGBoost (cluster_rate + AADF + road_class + length), **raw count** target | 0.773 | 0.206 |
| Same clusters, pure statistical **share** (in-sample, later found circular — see below) | -0.088 | 0.002 |
| Same clusters + XGBoost, **share** target, fully separate per-type models (in-sample) | 0.096 | 0.024 |

Predicting raw count on top of clustering made things *worse* than the pure cluster statistic
(0.247→0.773) — the model leaned on AADF/road_class (both correlate with "how busy is this
place") since that's the easy way to fit raw count, recreating the exact collapse mechanism from
07-03 inside XGBoost. Switching the objective to **share of the cluster's all-type total** (the
GAT fix, applied here) fixed it decisively.

### 4. Validation — was any of this leakage?

The in-sample share result (-0.088 / 0.096) was flagged as suspicious and checked two ways:

**a) Random 80/20 segment holdout**, clusters+share built from `HISTORY_YEARS=[2020,2021]` only,
evaluated against `TARGET_YEARS=[2022,2023]`:
- pure statistical: ρ=-0.072, Jaccard=0.013
- XGBoost (trained on 80% train segments only): ρ=0.114, Jaccard=0.051
- **New check, run for the first time in this whole investigation:** does predicted risk actually
  correlate with each type's *real* future crashes? car 0.016(stat)/0.190(ML), motorcycle
  0.050/0.069, cycle 0.059/0.064, lgv 0.010/0.037, hgv 0.012/0.035 — **ML beat pure stats for
  every single type**, though all absolute values are modest.
- Flagged residual issue: random split lets clusters straddle the train/test boundary (a test
  segment's own history can leak, diluted, into the cluster label used for training) — not a
  clean generalisation test.

**b) Spatial block holdout (fully clean)** — Manchester (74,783 segments) **entirely** excluded:
its own crash history zeroed, fully excluded from cluster construction and from XGBoost training:
- pure statistical: ρ=0.044, Jaccard=0.058
- XGBoost: **ρ=0.201**, Jaccard=0.122
- Validity vs. real Manchester crashes: car 0.027/0.161, motorcycle 0.003/0.027, cycle
  -0.005/0.039, lgv 0.009/0.043, hgv 0.001/0.041 — **ML beat stats for every type again**, numbers
  consistent with the random-split version. The result is real, not a leakage artefact — it just
  wasn't quite as strong as the (mildly optimistic) random-split number suggested.

### 5. End-to-end routing test — does it actually change routes?

London (272,204 segments) held out the same way as Manchester (own history zeroed, fully excluded
from training). Production risk scores computed for all segments, fed into `route.py`'s exact
edge-weight formula (cost charged to destination segment, directed, per-type normalised), 10
random O-D pairs, single shortest path per type:

| metric | no-risk baseline | best-GAT (07-03) | **this method** |
|---|---|---|---|
| mean distinct paths / 5 types per O-D pair | 1.00 | 2.00 | **3.10** |

8 of 10 pairs showed real divergence (e.g. one pair: car-hgv route Jaccard=0.03, essentially
completely different roads). 2 of 10 pairs (pair 1 = 1/5 distinct, pair 9 = 2/5 distinct) showed
little/no divergence — **diagnosed same session:**

- **Pair 1 (1/5, fully collapsed): genuine geographic dead-end, not a prediction problem.**
  Checked against a pure travel-time (zero risk weighting) top-5 alternatives search: all 5
  near-identical, Jaccard=0.99 overlap — essentially one corridor exists for this trip regardless
  of risk weighting. Risk scores along the path *do* differ substantially by type (car 0.6-0.7 vs
  hgv 0.03) — the model isn't collapsed here, there's just nowhere else to go.
- **Pair 9 (2/5 distinct — car/hgv/motorcycle identical, others diverged): more nuanced.** A
  genuine, cheap alternative route *does* exist for this pair (0.01 overlap with the shortest path
  — 99% different roads — for only a 17.8% travel-time penalty). hgv (risk 0.03) and motorcycle
  (risk 0.08) not diverging looks correct — their own risk on this corridor is already low, nothing
  to gain by moving. **Car not diverging despite high risk here (0.70) and a cheap alternative
  existing is the open item** — car's risk score *on the alternative route* was not checked; if
  the alternative is equally/more risky for car, staying is correct; if it's genuinely safer and
  car still didn't move, that points at λ=1.0 possibly being too weak to overcome a 17.8% time
  cost — a routing-tuning question, not a prediction-quality problem.

---

## The general mechanism (why this works, generalising 07-03's finding)

07-03 established: any signal shared equally across types (shared GAT backbone, a type-agnostic
feature, EB's generic covariate prior) collapses divergence. This session adds a second axis:

**Divergence lives in location, not in volume.** The niche premise itself (Lee 2018; this
project's own STATS19 probes) is that different vehicle types crash in different *places*.
Feature-based clustering — even using each type's own AADF — pools by traffic-volume similarity,
which is correlated across types (busy roads are busy for everyone) and throws away exactly the
axis the divergence lives on. Location-based pooling (network proximity) preserves it because
it's the same axis the real signal is expressed on. **This is true independent of whether a model
is involved** — it explains both why the original GAT (which does use location, via message
passing) still collapsed to ρ=0.894 (its shared backbone actively fought the location signal it
had access to) and why pure network averaging with zero learned parameters beat every model
tested. The combination that finally worked (discrete location clusters + share objective +
separate models) satisfies both rules at once: pooled by location (preserves the divergence axis)
and targeted at share, not volume (removes the "how busy" confound), with nothing shared across
types anywhere in the pipeline.

---

## Process notes — mistakes made and corrected this session (read before repeating any of this)

Keeping this honest since it's the audit trail:
- Initially implemented the plan's literal feature-based clustering without checking it against
  the core spatial-divergence premise first — should have been caught immediately, not after
  several failed experiments.
- Conflated "flat 2-hop smoothing" (a diagnostic, not the plan) with "adaptive-radius clustering"
  (the actual modified-plan test) when asked "is this the plan" — gave a wrong answer, corrected.
- An early XGBoost run had a real temporal leak: the network-smoothed feature was built from the
  same target-year data it was predicting. Caught and fixed by switching to `HISTORY_YEARS`-only
  construction.
- The in-sample discrete-cluster share result had a circularity: clusters were grown by chasing
  *that type's own* target-year crashes, so measuring that type's share within a cluster shaped
  around its own crashes was somewhat tautological. Caught, fixed with the history-year +
  holdout construction.
- First holdout attempt used a **random** segment split, which still let clusters straddle the
  train/test boundary — a real but subtler contamination. Corrected with a genuine spatial block
  holdout (whole city excluded).
- Added extra features (AADF/road_class/length) to a test the user had asked to run using only
  the location signal — corrected after clarification that combining location + features was
  actually the intent (to get feature-importance/explainability, not just match the pure stat
  number).

---

## Decisions extracted

- **The plan's Steps 1-3 (feature-based clustering) are falsified, not just "under-performing."**
  They must not be built as literally written. See update to
  [[wiki/concepts/vehicle-type-risk-divergence]].
- **New validated direction:** discrete, per-type, network/location-based clusters (BFS-grown
  until a minimum crash count, not feature/AADF-based) + share-of-all-type-total objective (not
  raw count/rate) + fully separate per-type XGBoost models. This is now the best-validated
  ML method across the whole investigation (beats best-GAT 0.377 with 0.201 on a real spatial
  holdout, and produces measurably more routing divergence: 3.10/5 vs. GAT's 2.00/5).
  [[PHASE3/positioning-memo]] build-architecture row updated accordingly.
- **Step 6's premise (keep a separate purely-spatial grouping apart from the risk-estimation
  clusters) needs re-examination** — risk estimation is now inherently location-based, so the
  clean separation Step 6 assumed may not hold the way it was originally framed. Not resolved,
  flagged for next session.
- **A new evaluation axis was opened and only tested on one method:** "does predicted risk
  actually correlate with real future crashes" (not just cross-type divergence). This should be
  run on best-GAT and the ad hoc smoothing baseline too, for a fair comparison — this is a Stage 6
  (evaluation) concern, not a blocker for the current direction.
- GAT was deliberately **not** retested with this new recipe (discrete location clusters + share
  target) — deprioritised in favour of validating XGBoost first, since XGBoost already performs
  very well with much simpler, off-the-shelf explainability (feature importances/SHAP) than an
  interrogated GNN would need. Worth trying later, not urgent.

## Next (in priority order)

1. **Test GAT using this exact validated recipe** — discrete network-based clusters (BFS-grown per
   type), share-of-all-type-total objective, fully separate per-type models — in place of
   XGBoost. Deliberately deprioritised this session in favour of validating XGBoost first; now the
   natural next comparison, run the *same* way (spatial holdout + routing test) so the two are
   directly comparable.
2. **Check car's risk score on pair 9's alternative route** (see pair-9 diagnosis above) — the one
   unresolved piece of the routing-divergence check. If the alternative is genuinely lower-risk for
   car and car still didn't move, test whether raising λ (currently 1.0) makes it diverge — a cheap
   routing-tuning experiment, not a re-test of the risk model itself.
3. Run the "predicted risk vs. real future crashes" validity check on best-GAT and ad hoc
   smoothing, for a fair comparison against tonight's XGBoost numbers.
4. Formalise/cite the winning mechanism — likely a spatial/network-constrained cluster-detection
   method; "Network KDE" (07-03's guess) may or may not be the right literature home for this
   specific discrete-partition version — not yet checked.
5. Resolve Step 6's premise (see Decisions extracted above) before building anything final on
   routing-search grouping.
6. None of tonight's code has been committed to the codebase (all ad hoc, per explicit
   instruction). If this direction holds up, it needs a real, clean implementation as an actual
   Stage 3 replacement script eventually.

## Links

- [[wiki/progress/2026-07-04]] — the supervisor-meeting redirect this session tested
- [[wiki/progress/2026-07-03]] — the original type-collapse investigation and mechanism this
  session's findings generalise
- [[wiki/concepts/vehicle-type-risk-divergence]] — core concept page, updated with this outcome
- [[PHASE3/positioning-memo]] — build architecture decision updated
- [[wiki/overview]]
