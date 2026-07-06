---
title: "Vehicle-Type Risk Divergence (and the GAT Type-Collapse Problem)"
type: concept
tags: [thesis-core, experiment, decision]
sources: ["[[wiki/progress/2026-07-02]]", "[[wiki/progress/2026-07-03]]", "[[wiki/progress/2026-07-04]]", "[[wiki/progress/2026-07-04-clustering-testing]]", "[[wiki/progress/2026-07-06]]"]
last_updated: "2026-07-06"
---

# Vehicle-Type Risk Divergence — and why every tested model hides it

The single most important empirical finding of the build. It settles the thesis's existential
question **and** identifies the current system's core bottleneck. Established 2026-07-02,
substantially deepened 2026-07-03, strategic fork reframed 2026-07-04, clustering direction tested
and revised same night, and **resolved + validated leakage-free 2026-07-06** — see
[[wiki/progress/2026-07-02]], [[wiki/progress/2026-07-03]], [[wiki/progress/2026-07-04]],
[[wiki/progress/2026-07-04-clustering-testing]], [[wiki/progress/2026-07-06]].

**2026-07-06 RESOLUTION, read this first.** The 2026-07-04 recipe had been run ad hoc and the code
was lost; it was rebuilt as durable scripts (`code/tests/cluster_risk/`), reproduced (national eval
= 158,237 segments, *exact* match), and then validated properly: a **16-fold spatial cross-validation
+ an unseen-year 2024 temporal holdout** give national out-of-sample **cross-type ρ = −0.097** with
**no leakage** (validity vs the never-seen 2024 ≈ validity vs the target years). **Method decision is
now final: the Stage 3 engine is per-type discrete network clustering + share-of-all-type-total
target + 5 fully separate XGBoost models.** GAT was tested on the *same* recipe and ties on
divergence but loses on validity (goes negative for some types), simplicity, and explainability —
retired to a documented alternative. Honest framing pinned down: ρ≈0 is the *noise floor* (random
surfaces give ≈0.05), so the real bar is **validity**, which is modest (~0.05–0.18) but positive
everywhere and comparable to the statistical baseline — *sufficient*, since the contribution is
explainable per-type divergence, not accuracy. Full detail + the implementation blueprint:
[[wiki/progress/2026-07-06]], [[wiki/build/stage-3-cluster-share-engine]].

**2026-07-04 night-testing update, read this first:** the clustering direction from the
supervisor meeting was built and tested. **Its literal mechanism (feature-based clustering — road
class + own-AADF + length) is falsified**, not just underperforming: it never beat ρ≈0.65-0.9,
worse than best-GAT. The reason: car/lgv/hgv's own-AADF values are themselves correlated with each
other in reality, so pooling by traffic-volume similarity re-collapses divergence even when the
volume figure is genuinely type-specific. **What actually works is pooling by network/location
proximity instead of feature similarity** — because the divergence itself lives in *where* each
type crashes, not in how much of each type there is. The validated recipe: discrete,
network-based clusters per type (not feature-based) + predicting each type's **share** of the
cluster's all-type crash total (not raw count/rate) + fully separate per-type XGBoost models.
Validated on a genuine spatial holdout (a whole city excluded from training: ρ=0.201, beats
best-GAT's 0.377) and on an actual routing test (3.10/5 types take distinct routes for the same
trip, vs. best-GAT's 2.00/5). Full detail: [[wiki/progress/2026-07-04-clustering-testing]].

**2026-07-04 supervisor-meeting update:** the 2026-07-03 fork ("formalize the statistical estimate"
vs. "ship GAT-stacked") was brought to the supervisor and **reframed rather than answered
directly**. Root cause of every method's struggle is sparsity itself (96–99.8% zero-crash
segments for a given type at raw resolution) — his steer was to **pool segments into per-type
clusters before estimating risk**, then re-decide statistical-vs-model *at cluster level*, where
there's actually enough data either way to answer the question. See
[[wiki/progress/2026-07-04]] for the original plan (its clustering mechanism is now superseded by
the night-testing update above — the plan's *intent* (cluster before estimating) survived; its
literal feature-based method did not).

**2026-07-03 update, read this first:** the "decouple the types" fix proposed below on
2026-07-02 was tested exhaustively — architecture decoupling alone (separate heads, even fully
separate models) barely helped. What actually worked, and the general mechanism now confirmed
across **four independent settings** (GAT architecture, a leak-free generic STATS19 feature, and
Empirical Bayes shrinkage), is stated precisely in **The general mechanism** section below. EB
shrinkage — the literature-standard statistical method — was tested and **also collapses
divergence**, for the same reason. This corrects the 2026-07-02 claim that EB was a "safe
secondary denoiser."

## The good news: the niche is real (much stronger than the 2026-06-22 probe)

On raw STATS19 (severity-weighted crash counts per segment, 2022–23), measured across the
158,237 segments that had ≥1 crash:

- **Cross-type Spearman ρ ≈ −0.047** (essentially zero / slightly negative).
- **Top-1000 hotspot overlap (Jaccard) = 0.042** — the 1,000 worst segments for each type
  overlap only **4%**.

**Vehicle types crash in almost completely different places.** Cyclist, HGV, motorcycle and
car black-spots are genuinely different roads. This confirms — far more strongly than the
informal 2026-06-22 probe — the load-bearing premise: type-aware risk is *not* redundant with
aggregate risk. Lee 2018 (Florida) found the same; now confirmed on GB.

**It is not a sparsity artifact.** Pooling all 5 years to remove noise barely changed it
(ρ −0.047 → 0.049; Jaccard 0.042 → 0.081). The divergence survives denoising.

## The problem: the GAT collapses this divergence

The trained GAT (Stage 3) outputs a per-type risk surface that is **ρ = 0.855 correlated
across types** (Jaccard 0.298) — i.e. it takes a genuinely divergent ground truth and smooths
it into a nearly-shared surface. It does **not reproduce the divergence in its own training
target.** This is why downstream routing barely differentiates by type (parallel-street swaps,
~1% median risk reduction — see [[wiki/concepts/routing-risk-normalization]]).

## The diagnostic ladder — the culprit is architecture, not message passing or sparsity

Same 158,237 active segments, five surfaces:

| surface | cross-type ρ | top-1k Jaccard |
|---|---|---|
| 1. RAW target (2022–23, noisy) | −0.047 | 0.042 |
| 2. POOLED all 5 years (pure denoise) | 0.049 | 0.081 |
| 3. + 1-hop spatial smooth (≈ GAT message passing) | 0.211 | 0.103 |
| 4. + 2-hop spatial smooth | 0.247 | 0.127 |
| 5. **GAT pred_count** | **0.855** | **0.298** |

- **Denoising (2) keeps divergence** → the effect is real, not noise.
- **Spatial smoothing (3–4) saturates at ρ≈0.25** — 1-hop→2-hop barely moves, so even infinite
  neighbour-averaging (what message passing *is*) plateaus far below the model. Message passing
  is **not** the main smoother.
- **The 0.247 → 0.855 jump is unexplained by geometry** → the collapse comes from the
  **shared learned backbone with weak type conditioning**: the network learns one common surface
  and the type embedding only nudges it. On sparse targets, regressing to a shared smooth surface
  is the low-loss solution. This is **type-collapse**, worse than classic GAT oversmoothing.

## The general mechanism (established 2026-07-03, supersedes the 2026-07-02 "decouple" fix)

Architecture decoupling alone does not fix this. Ladder on raw counts: shared-head GAT ρ=0.894 →
per-head (shared backbone, 5 output heads) ρ=0.816 → 5 fully independent models ρ=0.785. Going
all the way to zero shared weights barely moved the number. The real cause, confirmed
identically in **four separate settings**:

1. GAT's shared backbone + weak (16-dim embedding + 1 history scalar) type-conditioning.
2. A leak-free but *type-agnostic* STATS19 feature ("did any type crash here pre-2022") fed to
   5 separate XGBoost models: ρ went from 0.650 (no feature) to **0.79** (worse) — despite zero
   data leakage, despite being a real historical signal.
3. The *identical* feature, but computed **per type** ("did a cyclist crash here pre-2022"):
   ρ = **0.55** — the best non-graph result found. Same information, different packaging.
4. **Empirical Bayes shrinkage** (Poisson-SPF + NB dispersion, the literature-standard method,
   matching Pathivada 2025's approach): ρ = **0.412** — worse than a crude ad hoc spatial-smoothing
   baseline (~0.19–0.25). EB's prior comes from regressing on exposure covariates (AADF, length)
   that are similar in *shape* across types, so sparse segments get shrunk toward a shared,
   non-divergent baseline.

**The rule: any signal shared equally across all 5 types — a shared output head, a shared
backbone, a type-agnostic input feature, or a generic covariate-based statistical prior —
pulls every type's estimate toward a common answer.** It doesn't matter whether the shared
thing is a neural network, a gradient-boosted tree's feature, or a textbook GLM. Divergence
survives only when the type-specific information has its own dedicated pathway, all the way
through.

## What worked, and what didn't (2026-07-03 experiments — full detail in [[wiki/progress/2026-07-03]])

**Fix that worked, GAT side — "stacked" model:** per-type output heads (decoupled final layer)
**+** reframe the objective from raw counts to per-type **share/composition** (removes the
shared-crash-density dominance from the loss), trained together. Result: **ρ = 0.377** — best
model result found, and *synergistic* not additive (naive sum of the two fixes separately
predicts ~0.48). **Uses the exact same input features as the original collapsing GAT — no new
data.** Ran end-to-end through Stage 4 (CLQ) + Stage 5 (routing): routing divergence improved
genuinely (mean distinct paths per O-D pair went 1.00→2.00 across 10 London routes), but CLQ
(hotspot-tail divergence, self-calibrated caps, verified non-degenerate) stayed flat at 0/10
pairs diverging — the gain lives in the mid-range of the risk distribution, not each type's
*most* dangerous segments.

**Fix that worked, non-graph side:** XGBoost + type-specific historical crash feature → ρ=0.552
(point 3 above).

**Fixes that did NOT work:** new input features generally. Clean OS road-geometry
(`form_of_way`/`road_function`/`primary_route`/`trunk_road`, 100% network coverage, no
missingness) added to either XGBoost (ρ 0.650→0.681, no help) or GAT (ρ 0.894→0.822, small) —
essentially flat. **Directly refutes the "give the model richer inputs" hypothesis** — the best
GAT and the worst GAT saw identical features; the fix was training design, not data.

**Killed, separately:** a proposed second ML pillar — predicting risk *conditional on driving
conditions* (weather/light/road-surface) — was premise-tested via chi-square + Cramér's V on
~880k crash-vehicle rows. All three condition variables: statistically "significant" only
because of huge n, but **Cramér's V = 0.029–0.050, below the 0.1 "negligible" threshold.** Not
an ML failure — the underlying pattern is too weak for any method.

## Implication (fix direction, revised)

- The primary lever was **training design** (objective + architecture together), not Stage 2/3
  input richness and not simple architecture decoupling. This **reverses the 2026-07-02 note's
  claim** that decoupling alone would work.
- The positioning-memo's "Unified GAT with type embeddings" locked decision is still
  **under revision**, but the correct replacement is the **stacked (share-target + per-head)**
  design, not naive full separation.
- **EB shrinkage is not a safe fallback** — it fails for the same reason the GAT does. This
  corrects the 2026-07-02 note.
- **Fork superseded 2026-07-04 (see [[wiki/progress/2026-07-04]]):** the "statistical vs.
  GAT-stacked" choice was not made directly. Instead, the supervisor's steer was that the root
  cause is sparsity at raw segment resolution — the fix is per-type clustering (pool segments so
  every unit has enough data to estimate from), test the simple pooled statistical estimate first,
  and only build a cluster-level model if that estimate demonstrably falls short by the same
  ρ/Jaccard/CLQ metrics.
- **Clustering mechanism revised, same night (see [[wiki/progress/2026-07-04-clustering-testing]]):**
  the plan's literal clustering mechanism — pool by feature similarity (road_class + own-AADF +
  length) — was built and tested. **It fails** (ρ≈0.65-0.9, no better than the original collapsed
  GAT), because car/lgv/hgv's own-AADF values are themselves correlated with each other in
  reality, so feature-similarity pooling re-collapses divergence even though the AADF figure is
  genuinely type-specific. **The rule from 2026-07-03 needed a second clause**: it's not just
  "any type-agnostic signal collapses divergence" — it's also that **divergence lives in
  location, not volume**, so pooling by anything other than network/geographic proximity throws
  away the axis the signal is expressed on, regardless of how type-specific the pooling feature
  is. The validated replacement mechanism: discrete network-based clusters (BFS-grown per type,
  not feature-based) + share-of-all-type-total objective (not raw count/rate) + fully separate
  per-type XGBoost models. ρ=0.201 on a genuine spatial holdout (whole city excluded from
  training), beating best-GAT's 0.377; 3.10/5 types take distinct routes on an actual end-to-end
  routing test, vs. best-GAT's 2.00/5. Full detail, test-by-test numbers, and the mistakes made
  and corrected along the way: [[wiki/progress/2026-07-04-clustering-testing]].

## Related Concepts

- [[wiki/concepts/routing-risk-normalization]] — the downstream symptom (identical/near-identical routes).
- [[wiki/build/stage-3-cluster-share-engine]] — **the final Stage 3 engine** (cluster + share +
  per-type XGBoost) that fixes the collapse; implementation blueprint for the rewrite.
- [[wiki/build/stage-3-gat-risk-model]] — the superseded GAT design where the collapse happened
  (audit trail).
- [[PHASE3/positioning-memo]] — the "Unified GAT" decision this finding challenges; the divergence premise it confirms.

## Sources

- [[wiki/progress/2026-07-02]] — raw-data probe + smoothing-ladder diagnostic.
- [[wiki/progress/2026-07-03]] — architecture ladder, feature ablations (leak found + fixed),
  stacked-GAT fix, EB shrinkage test, Task B premise kill, strategic fork.
- [[wiki/progress/2026-07-04]] — supervisor meeting, fork reframed into per-type clustering.
- [[wiki/progress/2026-07-04-clustering-testing]] — clustering built and tested; feature-based
  mechanism falsified; location-based mechanism validated on spatial holdout + routing test.
