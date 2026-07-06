# New technical direction — cluster-based risk estimation + routing

Status: **draft skeleton, not finalized.** Written after the 2026-07-04 supervisor meeting.
Read through, adjust, fill gaps — this is meant to be edited, not executed as-is.

---

## Why this direction (one paragraph)

Segment-level risk estimation failed because 96–99.8% of segments (worse for rarer types like
HGV) have zero recorded crashes for a given type — there's nothing for any method, statistical
or learned, to estimate from at that resolution. Every model tested (GAT, XGBoost, Empirical
Bayes) either collapsed vehicle-type divergence or simply had nothing to work with on most of
the network. Clustering segments before estimating risk pools enough data per unit to make
estimation possible at all, while still ultimately producing a per-segment number the existing
routing code can consume unchanged.

## Lessons from 2026-07-03 that this plan must not violate

1. **Any signal shared equally across vehicle types collapses divergence between them** — a
   shared model, a shared feature, a shared statistical prior, doesn't matter which. Whatever
   groups/estimates risk must stay separated by type, all the way through.
2. **A signal driven by general traffic/exposure looks similar in shape across all 5 types** —
   any method that leans on "how busy is this place" as its main signal (including a
   regression-based prior like Empirical Bayes) will underperform at preserving divergence.
3. **Richer input features are not automatically better** — road geometry alone didn't help
   either GAT or XGBoost. What helped was keeping information type-specific, not adding more of it.
4. **Don't assume ML is needed — test it.** Simple statistical smoothing beat every model tried
   tonight. This plan must test a cluster-level statistical baseline before assuming a
   cluster-level model is worth building.

---

## Step 1 — Build per-type clustering features

**What:** for each vehicle type separately, build a feature table covering *every* segment in
the network (not just ones with crashes): road class, road function, form of way, segment
length, and **that type's own AADF** (not combined traffic volume).

**How:** reuse the existing OS Open Roads join (already built tonight, `Tier 1` fields) plus the
per-type AADF columns already in `segments.gpkg`. No new data collection needed.

**Why:** these features exist for 100% of the network, so even a segment with zero crash history
can be assigned to a sensible cluster. Using each type's own AADF (not shared traffic volume)
keeps the clustering itself type-specific from the very first step — directly following lesson 1.

## Step 2 — Choose the clustering method and granularity, per type

**What:** cluster each type's segments **separately** — 5 independent clusterings, not one
shared clustering reused across types.

**How:**
- Use **hierarchical (agglomerative) clustering**, not plain K-means. It produces a full tree
  that can be cut at any depth — this gives the "zoom in" multi-resolution structure directly,
  instead of needing two separate clustering passes for coarse vs. fine.
- Choose where to cut the tree **based on data sufficiency, not an arbitrary K**: keep the tree
  as deep (fine-grained) as possible while requiring every resulting cluster to contain at least
  some minimum number of that type's historical crashes (a number to decide empirically — start
  from the NB-dispersion math already used in tonight's EB test to reason about what's "enough"
  for a stable estimate).
- Expect **very different granularity per type** — car can likely support many fine clusters;
  HGV (99.8% zero-crash segments) will need far fewer, coarser ones. Don't force the same
  resolution across types.

**Why:** a shared clustering forces all 5 types into the same groups, recreating exactly the
"shared signal collapses divergence" failure from tonight (lesson 1) — a roundabout and a plain
junction might be "similar" in general traffic terms but very different in risk for a cyclist vs.
an HGV. Per-type clustering avoids this by construction. Tying granularity to data sufficiency
(not a fixed K) ties the method directly to the problem it exists to solve.

## Step 3 — Estimate risk within each cluster, per type

**What:** for each type, and each of that type's clusters, compute a risk estimate pooling all
crash history from every segment in the cluster.

**How:**
- Use pooled/all-years crash data for the production version (matches how the statistical
  smoothing baseline was built tonight).
- **Test a simple pooled/statistical estimate first** (e.g. severity-weighted count per cluster,
  normalised by pooled exposure) before building anything more complex — lesson 4.
- If a regression-based prior (EB-style) is used at this stage, be cautious that it doesn't lean
  primarily on traffic volume as the dominant covariate (lesson 2) — a generic "busy place, more
  predicted crashes" prior can still wash out real local variation *within* a single type's own
  pattern, even without any cross-type collapse involved.
- **Note:** because clustering is per-type throughout, the specific cross-type collapse mechanism
  from tonight (shared backbone/objective across 5 types) doesn't directly apply here — there's
  no shared model across types left to collapse. The share-vs-raw-count fix was a fix for *that*
  specific architecture, not a universal rule to reapply blindly at this step.

**Why:** this is the actual sparsity fix — pooling within a cluster gives enough data to produce
a stable estimate even where any single segment has none.

## Step 4 — Decide whether a model is needed here, or if statistics still wins

**What:** before committing to a GAT/XGBoost component at cluster level, test whether the simple
pooled/statistical estimate from Step 3 already preserves divergence well, using the same
metrics as tonight (cross-type ρ, CLQ).

**How:** rerun the same evaluation pipeline built tonight (`ρ`, top-N hotspot Jaccard, CLQ) on
the cluster-derived, segment-assigned risk surface.

**Why:** tonight's single clearest lesson was "don't assume ML helps — check." Clustering
directly targets the sparsity problem; it's a real, open question whether that alone is enough,
or whether a model is still needed on top. Don't skip this test just because a model "feels"
more sophisticated.

## Step 5 — If a model is warranted: cluster-level prediction, per type

**What:** only if Step 4 shows the simple estimate falls short — train a model (GAT or XGBoost,
per type, fully separate, no cross-type sharing) to predict/refine risk at the cluster level, or
to refine specific segments *within* a chosen cluster.

**How:** cluster-level or within-cluster problems are much smaller and denser than national
segment-level prediction — this is a task suited to a model, unlike raw segment-level prediction.

**Why:** this is the legitimate re-entry point for GAT discussed with the supervisor — not
predicting raw segment risk from scratch (which failed), but refining an already-reasonable
cluster-level estimate, a smaller and more tractable problem.

## Step 6 — Separate geographic grouping for routing search efficiency

**What:** build a **second, purely spatial** grouping (grid cells or geographic clustering),
independent of the feature-based clusters from Steps 1–3, used only to narrow the search space
for national-scale routing.

**How:** keep this entirely separate from the statistical clustering — don't reuse the same
clusters for both purposes.

**Why:** feature-based clusters (Steps 1–3) can be geographically scattered by design — that's
what lets sparse segments borrow strength from similar-but-distant ones. A routing search needs
geographically *contiguous* regions to narrow down to. Conflating the two would break one or the
other. **This is one of two things to confirm with the supervisor** — my working assumption is
this spatial grouping is for computational pruning only, not a hard constraint on which regions
a route is allowed to pass through (see Open Questions below).

## Step 7 — Feed into existing Stage 5 routing — unchanged

**What:** assign each segment its cluster's risk estimate (per type), refined by the segment's
own features if useful. Output in the same `segment_id, vehicle_type, risk_score` format Stage 5
already consumes.

**How:** no changes to `route.py`'s routing logic (Yen's k-shortest + MCDM) — only the risk
surface it reads is different, now covering far more of the network than before.

**Why:** confirms the earlier "is GAT out of the picture" answer — the routing algorithm itself
doesn't need to change. Only the risk-estimation layer feeding it does.

## Step 8 — Evaluation plan

1. **Same divergence metrics as tonight** (cross-type ρ, top-N hotspot Jaccard, CLQ) on the
   final cluster-derived, segment-level risk surface — direct comparability to tonight's numbers.
2. **New primary test — the held-out-block sparsity check:** take a contiguous block of segments
   with real, known crash history, hide their own history *and* their neighbors' (to genuinely
   simulate a data-sparse/novel area), estimate their risk using only the cluster method, and
   check against the real, known values. This is the test that actually validates whether
   clustering solved the coverage problem it exists to solve — nothing tonight tested this directly.
3. **Re-run the Phase A/B routing experiments** (2026-07-02) on the new risk surface — all of
   that was run on the old, collapsed surface and needs redoing once this is built.

---

## Open questions — need his input, defaults used below if not resolved first

1. **Spatial vs. feature-based clustering** — is the geographic grouping (Step 6) meant to be
   the *same* clusters used for risk estimation (Steps 1–3), or separate? Plan above assumes
   **separate** — confirm before building.
2. **What "zoom in" routing means** — computational pruning of the search space (assumed above),
   or a genuine two-stage decision where the coarse cluster choice constrains the fine search?
   The second could produce suboptimal routes (a good path might cross a coarse region ruled out
   early) — worth raising directly.

---

## What this does NOT change

- Stages 1–2 (data prep, segmentation) — unchanged.
- Stage 5 (routing algorithm) — unchanged, per Step 7.
- The core thesis premise (vehicle types are genuinely at risk in different places) — already
  strongly confirmed, not affected by this pivot.
