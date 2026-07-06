---
title: "Routing Risk Normalization"
type: concept
tags: [method, decision, thesis-core]
sources: ["[[wiki/progress/2026-07-02]]"]
last_updated: "2026-07-02"
---

# Routing Risk Normalization

How the per-(segment, type) risk score from Stage 3 is turned into a routing **edge weight**
in Stage 5, and why the naive version silently produced identical routes for every vehicle
type. This is a design decision, not just a bug fix — it determines whether the system can
demonstrate its central claim (vehicle-type-conditioned routes).

## Overview

Stage 5 edge weight (cost of entering segment *b* for type *t*):

```
w_t(a→b) = travel_time_b × (1 + λ × norm_risk_b_t)
norm_risk_b_t = risk_b_t / DENOM_t
```

Three knobs control `norm_risk`:
- **Capping** — cap `risk` at a percentile before normalising? (`off` vs Stage-4 `p99`)
- **Normalization scope** — `DENOM_t` = each type's own max (**per-type**) or one shared
  max across types (**global**)?
- **λ** — how much risk matters vs travel time (0 = pure time, ∞ = pure risk).

## Key Claims (established 2026-07-02, see [[wiki/progress/2026-07-02]])

1. **`risk_score` is an unbounded rate, and its raw max is an artifact.**
   `risk_score = pred_count / exposure_vkm`. Segments with near-zero exposure (little counted
   traffic of that type) produce inflated ratios. The single largest value in a bbox — often
   such an artifact (e.g. car max 0.976 at `exposure_vkm = 0.414`, vs national median ≈ 207) —
   becomes the normaliser, crushing every genuine difference toward zero. **Fix: cap at the
   Stage-4 p99 cap before normalising.** Capping is the single biggest lever on whether routes
   diverge by type — without it, types stay ~identical even at λ=8.

2. **Normalization scope is (within a type) just a λ rescaling.** Dividing a type's risk by
   `max_t` vs `global_max` multiplies the risk term by a constant, which is identical to
   scaling λ. So scope has **no independent effect on a single type's route**; it only changes
   the *relative* effective λ **across** types. This decomposes "types route differently" into:
   - **Channel 1 — spatial divergence:** different segments risky for different types (the niche).
   - **Channel 2 — magnitude:** same segments, different intensity (weaker; partly exposure).
   Per-type norm isolates Channel 1 (equal effective λ); global norm mixes 1 + 2.

3. **Per-type norm surfaces more divergence than global.** Global norm gives low-magnitude
   types (lgv, car) near-zero effective λ, collapsing them onto the pure-time shortest path;
   per-type gives every type full risk-aversion, so each follows its own risk pattern
   (n_distinct 3.67 vs 2.33 at λ=8, cap=p99). Caveat: "more distinct" ≠ "better policy" —
   per-type makes even trivially-low-risk lgv detour; whether that is desirable is unsettled.

4. **λ=0.5 (current default) undersells divergence; λ≈2 is a reasonable operating point.**
   Divergence is real but modest — detours observed were parallel-street swaps (~+100 m), not
   dramatic reroutes.

## Debates / Open Questions

- **Policy choice (per-type vs global norm):** unresolved. Per-type shows the niche most
  clearly but is arguably unrealistic for genuinely low-risk types. Global is more
  conservative but hides Channel 1. May report both.
- **Exposure confound (Channel 2b):** is the observed divergence the GAT's *learned*
  type-specific spatial patterns, or an artifact of the per-type exposure denominator that a
  trivial `crashes ÷ per-type traffic` baseline would reproduce? The sharpest reviewer attack;
  ties to the positioning-memo per-type-density existential risk. Deferred but flagged as the
  next experiment.
- **Route geometry confound:** O-D pairs with no alternate path show identical routes
  regardless of risk. Must filter for "flexibility" when measuring divergence rates.

## Related Concepts

- [[wiki/build/stage-5-routing]] — where this weight is applied (Yen's + MCDM).
- [[wiki/build/stage-4-risk-surface-filtering]] — source of the p99 cap and the hotspot flags.
- [[wiki/build/stage-3-gat-risk-model]] — produces `risk_score = pred_count / exposure`.

## Sources

- [[wiki/progress/2026-07-02]] — the diagnostic + Phase A factorial experiment.
