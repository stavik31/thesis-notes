---
title: "System Architecture — Route-Level Crash Cause Briefing"
type: concept
tags: [thesis-core, method, architecture, rag, llm]
sources: ["[[sources/crashsage]]", "[[sources/tab-text]]"]
last_updated: "2026-06-04"
---

# System Architecture — Route-Level Crash Cause Briefing

> **Redirected 2026-06-04.** This page previously described a real-time, per-GPS-point crash
> advisor. Supervisor feedback ([[progress/prof-feedback]]) retired that design: it assumed
> data exists everywhere, led with severity, and delivered output in the worst possible moment
> (mid-drive). The current design below is **offline segment cause-profiling + a pre-trip route
> briefing.** Some open design decisions are flagged explicitly rather than invented.
>
> **This design is an exploratory candidate, not a committed decision** (as of 2026-06-04). It
> is being investigated because real-time delivery broke under the feedback — not because the
> route-precompute approach is locked in. Other delivery models remain open.

## The Problem

Drivers have no access to localized knowledge of *why* crashes happen on the roads they are
about to travel. Risk is concentrated at specific **segments** and tied to specific
**conditions** — a bend that produces wet-surface skidding in the dark; a junction that
produces failure-to-give-way collisions. That signal exists in historical records but is
locked in tables no driver can read.

The system answers one question, for a route the driver is *about to* take:

> *"On the route I'm about to drive, which segments have a history of specific,
> condition-linked crash patterns I should anticipate — given when I'm driving?"*

This is **not** severity prediction and **not** a real-time alert. It is **offline,
segment-level cause profiling, surfaced as a pre-trip briefing.**

---

## Three design commitments (and why)

### 1. Cause, not severity
The deliverable is *what to watch for and why* (condition→mechanism), not a Slight/Serious/
Fatal label. Severity is the *outcome*; what transfers to a live driver is the
*condition→mechanism link*. Severity classification survives only as a sanity-check that the
model understands crash data — see [[concepts/crash-severity-inference]].

### 2. Pre-trip, not real-time
Real-time per-point LLM generation fails three ways at once:
- **Latency** — generation takes seconds; the warning arrives after the hazard.
- **Distraction** — an in-drive interruption competes with driving; distraction is itself a
  leading crash cause, so the delivery mechanism fights the safety goal.
- **Fixed radius is wrong** — relevant lookahead is a *time horizon*, not a distance. A 1 km
  radius is 36 s at 100 km/h but 6 min at 10 km/h.

Computing the **entire route up front** removes all three: no in-drive latency, no in-drive
interruption, and the segment (not a speed-dependent radius) becomes the unit.

### 3. Only speak where data exists
Crashes are spatially sparse (~503k over 5 years across the whole UK network). The old design
silently assumed local data everywhere; it only demoed where clusters happened to exist. The
new design makes sparsity the unit of analysis: **the system only profiles segments with a
statistically meaningful crash cluster, and stays silent elsewhere.** Silence is correct, not
a failure.

---

## Architecture Overview

```
OFFLINE (build once)
─────────────────────────────────────────────────────────────
STATS19 (collision + vehicle + casualty tables)
    │
    ▼
[1] Tabular-to-text conversion
    Each crash → natural-language narrative (scene, road/conditions,
    vehicles, mechanics). One narrative per crash.  [done]
    │
    ▼
[2] Domain-adapted LLM (LoRA on gemma-3-4b-it)
    Severity-trained adapter, used as domain adaptation for
    verbalization — NOT a deployed classifier.  [done; objective under review]
    │
    ▼
[3] Spatial segmentation
    Partition the network into segments (road link / grid cell /
    DBSCAN cluster — OPEN DECISION) and assign each crash to one.
    │
    ▼
[4] Segment cause-profiling
    For each segment with enough crashes, compute which conditions/
    mechanisms are OVERREPRESENTED vs the network baseline
    (Mutual Information + base-rate ratio + significance test).
    Output: per-segment profile, e.g.
      "wet surface ×3.1, darkness ×2.4, skidding ×2.8 vs baseline".
    │
    ▼
[5] Retrieval index over segment crashes (FAISS)
    Narrative + structured-feature + keyword variants (ablation).


TRIP-PLANNING (per route, before departure)
─────────────────────────────────────────────────────────────
Origin + Destination + Departure time
    │
    ▼
[6] Route → segments
    Map the route to the segments it passes through; keep only the
    high-risk ones (those with a significant profile).
    │
    ▼
[7] Per-segment retrieval + pre-aggregation
    For each high-risk segment, retrieve its crashes, pre-aggregate
    the cause profile, and FILTER/weight by conditions matching the
    departure context (time of day, season, weather if available).
    │
    ▼
[8] LLM verbalization
    The LLM turns the structured per-segment profiles into a
    prioritized, non-redundant route briefing — its job is synthesis
    and phrasing, not counting (counting is done in code).
    │
    ▼
Pre-trip route briefing (read/heard before driving)
  + optional HEAT MAP (per-cause risk surface — macro artifact)
```

---

## Component Details

### [1] Tabular-to-text — done
See [[concepts/tabular-to-text-transformation]] and the field-level decisions in
[[entities/stats19-field-reference]]. Under the pivot, lean harder on the **condition and
mechanism** fields (road_surface, light, weather, junction_detail, vehicle_manoeuvre,
skidding_and_overturning, first_point_of_impact) — these are the substrate for "cause."

### [2] Domain-adapted LLM — done, objective under review
LoRA on `gemma-3-4b-it`, trained narrative→severity. Kept as domain adaptation for now.
**Open decision:** if verbalization quality is poor, re-train on a cause-summarization
objective (narrative → condition/mechanism summary) instead of severity. Decision deferred
until after the grounding test — see [[concepts/llm-domain-adaptation]].

### [3] Spatial segmentation — OPEN DECISION
The new core methodological choice. Candidates: road-link (semantically clean, needs map
matching), uniform grid cell (simple, arbitrary boundaries), DBSCAN clusters of crash points
(data-driven, variable size). Whatever is chosen defines what a "segment" means everywhere
downstream.

### [4] Segment cause-profiling — the heart of the system
For each segment, compare its condition/mechanism distribution against the network baseline
and surface what is overrepresented, with a significance test so rare-but-real patterns are
kept and noise is dropped. This is where the [[concepts/crash-severity-inference]] correlation
work (Mutual Information over Cramér's V) is promoted from feature selection to the actual
product. **Open decision:** minimum crash count per segment, and the significance threshold —
Fatal at 1.5% is data-starved, so fatal-specific profiles need care.

### [5] Retrieval indices — survives from [[progress/future-plan]]
Three variants built from the same corpus, now scoped to within-segment (or
condition-similar) retrieval rather than a 1 km GPS radius:
- **Dense semantic** (all-MiniLM-L6-v2 + FAISS) — current
- **Feature-based** (structured one-hot vectors) — condition similarity
- **BM25 keyword** — non-neural floor
Compared in the ablation; a hybrid re-ranker (late fusion of semantic + feature overlap) is
the planned best configuration.

### [6–8] Trip-planning pipeline
Pre-aggregation ([[progress/future-plan]] Part 1) is now load-bearing: the LLM receives
*computed* per-segment statistics plus exemplar crashes and only has to write. Conditioning on
departure context is the fix for the "context is missing regardless of what happened"
critique. **Open decision:** briefing delivery format (text summary, audio pre-brief,
glanceable map) and whether the heat map is a co-deliverable or a separate analysis figure.

---

## What the System Does Not Do

- No real-time / in-drive generation (replaced by pre-trip precompute; real-time is future work)
- No per-GPS-point advisory (the unit is a segment on a planned route)
- No crash-probability or severity prediction as output (severity = sanity-check only)
- No output for segments without a statistically significant cluster (stays silent — by design)
- No claim of *causation* — surfaces overrepresented *patterns*, framed honestly as such

---

## Evaluation

| What to evaluate | How |
|---|---|
| Profile validity | Are surfaced conditions genuinely overrepresented vs the network baseline? (base-rate ratio + significance test) |
| Retrieval quality | Do retrieved crashes share the query segment's conditions? Feature overlap on 5 key fields. |
| Grounding / faithfulness | RAGAS faithfulness across bare vs force-cite vs pre-aggregation prompts (50 queries). |
| Temporal holdout | Profile segments on crashes up to date X; test whether profiles predict the conditions of post-X crashes at the same segments. |
| Usefulness / theory of change | Does a pre-trip cause briefing plausibly change driver anticipation? Human rubric or proxy — the open justification question. |
| Severity sanity-check | Fine-tuned vs XGBoost vs zero-shot F1 — confirms domain understanding only, never the headline. |

The temporal holdout is the strongest objective test; the theory-of-change is the hardest open
question (see [[progress/prof-feedback]]).

### Retrieval ablation
Reframed from [[progress/future-plan]] Part 3: dense vs feature-based vs keyword (and the
α-weighted hybrid re-ranker), scored by feature overlap and RAGAS faithfulness, to recommend
which retrieval strategy surfaces the most condition-relevant evidence for a segment.

---

## Build Order

1. ~~Tabular-to-text conversion~~ — done (503k narratives)
2. ~~Domain-adapt LLM~~ — done (`gemma-3-4b-it`, QLoRA r=16); objective under review
3. ~~Severity baselines~~ — done (now sanity-check only)
4. ~~Build FAISS index~~ — done
5. **Define segment unit + significance test** ← new core decision
6. **Segment cause-profiling** (pre-aggregation as the product)
7. **Route → segments → pre-trip briefing** pipeline
8. **Heat map** (per-cause risk surface)
9. **Evaluation** — profile validity, faithfulness, retrieval ablation, temporal holdout, usefulness

---

## Related

- [[progress/prof-feedback]] — the redirection that produced this design
- [[progress/future-plan]] — pre-aggregation + RAGAS + retrieval ablation, now serving this architecture
- [[concepts/rag-narrative-generation]] — earliest framing, superseded
- [[concepts/tabular-to-text-transformation]] — narrative templates (step 1)
- [[concepts/llm-domain-adaptation]] — fine-tuning rationale (step 2), objective under review
- [[concepts/crash-severity-inference]] — correlation analysis, promoted to cause-profiling
- [[entities/stats19]] / [[entities/stats19-field-reference]] — dataset + condition/mechanism fields
