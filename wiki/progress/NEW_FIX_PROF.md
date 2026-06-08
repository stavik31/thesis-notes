---
title: "New Direction & Architecture Proposal — For Supervisor Discussion"
type: progress
date: "2026-06-08"
tags: [progress, decision, thesis-core]
status: NOT FINAL — discussion draft
---

# New Direction & Architecture Proposal

> **⚠️ NOT FINAL.** This is a discussion draft to talk through with my supervisor.
> It captures how the project responds to the post-presentation feedback, the
> direction I'm now proposing, and the architecture that follows from it. The big
> decisions are flagged as open at the bottom — I'm bringing them to discuss, not
> presenting them as settled.

---

## TL;DR (the one paragraph)

Existing navigation systems only ever say *"crash ahead"* or *"crashes have happened
here"* — they report **that** crashes occurred, never **what the recurring pattern is**
or **what it means for the driver right now**. My thesis fills that gap: mine historical
crash data **offline** to find road segments where a **specific, non-obvious, condition-
dependent risk pattern is statistically overrepresented**, and surface a short, grounded
warning to the driver **only** when that pattern is invisible from the road and the
matching conditions actually hold. Everything heavy is precomputed; the live system just
reads current conditions and plays the relevant pre-written line.

---

## Part 1 — What you flagged last time (so you know I listened)

Your feedback after the presentation wasn't about implementation — it was about
**justification and usability**. The key points:

1. The system **assumes crash data exists everywhere** — it doesn't; crashes are sparse.
2. It was framed as a **UK-only artifact**, not a general method.
3. **Severity classification isn't the point** — yet I led with the F1 table.
4. The **live driver's own context is missing**, so output comes out generic.
5. **Real-time delivery risks distracting** the driver — distraction is itself a crash cause.
6. **Real-time is physically wrong**: a fixed radius ignores speed, and LLM latency means
   the warning arrives after the hazard.
7. Suggestion: a **heat map**, or **precompute the whole route** up front.

This document is my answer to all seven.

---

## Part 2 — The direction change

| | **Old (presented)** | **New (proposed)** |
|---|---|---|
| Unit of analysis | GPS point | **Road segment** |
| Deliverable | Severity warning | **Conditional risk pattern** ("what + why") |
| When computed | Live, per point | **Offline, precomputed** |
| When delivered | Real-time, always | Only when **invisible + conditions match** |
| Severity F1 | The headline | **A sanity-check only** |
| Framing | UK / STATS19 system | **General method**, STATS19 as case study |

**The single sentence that anchors the whole thesis:**
> Existing systems report *that* a crash happened. Mine explains the *non-obvious,
> condition-specific pattern* and what it implies — and stays silent when it has nothing
> non-obvious to add.

---

## Part 3 — The ideas that resolve the objections

These are the reframes that turn "this isn't useful" into a defensible scope.

- **Only speak when the risk is invisible.** If the hazard is obvious from the road (a
  sharp turn warns about itself), the system says nothing — the driver is already alert.
  It only speaks about what a driver *cannot* see: e.g. *"this bend is fine in daylight
  but overrepresents wet-night skidding 4× because it drains badly and is unlit."*
- **Patterns, not events.** Nav apps warn about *events* ("crash ahead" — has a location
  and a duration). I warn about *standing properties* of a segment ("this place has a
  wet-skid pattern"). A property has no "how long will it last" problem.
- **Silence is correct, not a failure.** Because crashes are sparse, the system speaks
  only where a real cluster exists. Everywhere else, staying quiet is the *right* answer —
  this directly answers the "assumes data exists everywhere" critique.
- **The live driver's context is handled by condition-gating.** The warning only fires
  when *current* weather/light/time match the pattern's conditions, so output is specific
  to the moment, not generic.

---

## Part 4 — The proposed architecture

### The core problem it solves: a single route can pass 1,000 crashes. How do you get from 1,000 crashes to 2 useful warnings?

You **never** process 1,000 crashes live. They are offline training data that collapse
into a handful of segment profiles. The funnel:

| Stage | What happens | Effect |
|---|---|---|
| 1. Segment | Snap each crash to its road segment (a route = a sequence of segments) | 1,000 crashes → ~30 segments |
| 2. **Significance** | Keep only segments where some condition is **statistically overrepresented vs the network baseline** (rate-ratio / chi-square) | ~30 → ~5 |
| 3. Profile | Summarise each survivor's crashes into its dominant condition→mechanism pattern | ~40 crashes → 1 line |
| 4. Obviousness filter | Drop anything inferable from road geometry | ~5 → ~3 |
| 5. Condition gate *(live)* | Only fire segments whose conditions match **now** | 3 → 1–2 |
| 6. Prioritise *(live)* | Cap at top 1–2 by significance × severity so the driver isn't overloaded | final output |

**Stage 2 (significance) is the new methodological core.** It is what separates "crashes
happen everywhere there's traffic" from "this specific place has a *non-random* pattern."
This is the part of the thesis that is genuinely new.

### Offline vs. live (this is the key architectural insight)

- **Offline (heavy, one-time):** segmentation → significance test → profiling → LLM writes
  a short line for **each condition cell** of each surviving segment (e.g. dry-day,
  wet-day, wet-night).
- **Live (instant, dumb):** as the driver nears a segment, read current conditions (weather
  API + clock + speed), **look up** the matching pre-written line, and deliver it.

So *"precompute and play later"* is **not** a fixed recording — it's a lookup table. The
*answers* are precomputed; the *actual condition* is read live at the moment, so changing
weather is handled automatically (each segment re-samples conditions as you reach it). No
LLM runs live → **no latency** (answers critique #6). Delivery is voice, terse, and rare →
**minimises distraction** (answers #5). The unit is a fixed route segment, not a radius →
**the radius-vs-speed problem disappears** (#6).

### What the architecture gains vs. the old system

The old system was a thin pipeline (narratives → severity LoRA → flat FAISS → radius →
top-k → live generate). The new direction adds genuinely new components: a **segmentation
layer**, a **significance-testing layer**, an **aggregation/profiling layer**, a
**per-condition matrix**, an **obviousness filter**, a **route/map-matching layer**, and a
**runtime condition-gate + prioritiser**. The centre of gravity moves from a live text
generator to an offline profiling + significance engine — richer and harder to dismiss.

---

## Part 5 — Where the research depth is (training + retrieval)

The original RAG was deliberately simple (flat L2 index, top-k, stuff the prompt). The new
direction has room for real methodological depth, and each option below is a potential
ablation/experiment rather than decoration:

**Training (the original fine-tune was just LoRA → severity, which is now demoted):**
- Keep the severity adapter only as **domain adaptation**.
- Explore **RAFT (Retrieval-Augmented Fine-Tuning)** — train the model to ground its output
  in retrieved crashes and ignore irrelevant ones (directly attacks the "generic output"
  problem).
- Explore **preference tuning (DPO/ORPO)** — align output toward grounded, concise,
  condition-specific warnings (this is how the LLM's value is *measured*, not asserted).
- Cheap methodology ablations: QLoRA vs LoRA vs **DoRA**, rank/alpha sweep.

**Retrieval (richer than the flat top-k):**
- **Three-index ablation:** dense semantic vs feature-based vs keyword (BM25) — which
  surfaces the most relevant crashes for a segment's profile.
- **Hybrid retrieval + cross-encoder re-ranking** (two-stage retriever).
- **Segment-level retrieval for sparse data:** when a segment has too few crashes (e.g.
  fatal-class is only ~1.5% of data), retrieve *similar well-characterised segments* and
  borrow their pattern.
- **Aggregation-before-generation:** summarise the retrieved crash set into a profile
  *before* writing the line — the single biggest output-quality lever.

---

## Part 6 — How it gets evaluated

You can't measure "prevented a crash" — that's explicitly out of scope. What *is*
measurable:

1. **Are the patterns real? → Temporal holdout (the headline test).** Build profiles on
   years 1–4, then check year 5: does a segment's overrepresentation *still hold* on data
   it wasn't built from? If yes, the pattern is real and predictive. Gives a hard number,
   no human study needed.
2. **Are they non-obvious? → Small human check.** Show drivers a segment's context, ask
   what risk they'd expect; measure how often the flagged pattern was *not* anticipated.
3. **Is the generated text faithful? → Grounding / RAGAS.** Does the sentence match the
   profile numbers, or did the model embellish?

---

## Part 7 — What this is NOT (honest scope)

A thesis bounds its limitations rather than removing them. Stated plainly:
- It works **only** where there is a statistically significant, non-obvious,
  condition-specific pattern. Elsewhere it is silent — by design.
- The "causes" are **correlational patterns, not proven causes** — our STATS19 dump has no
  contributory-factors table, so risk is inferred from overrepresented conditions. Output
  is framed as *patterns*, never *proven causes*.
- It does not claim to anticipate every crash; many crashes have no recurring,
  data-visible pattern, and those are out of reach for any data-driven system.

---

## Part 8 — Open decisions (what I want to discuss — NOT decided)

1. **Segment definition.** Road link vs grid cell vs DBSCAN cluster of crash points. This
   gates the whole build. (Leaning DBSCAN, but want your view.)
2. **Significance test + threshold.** What baseline (network-wide? road-class-specific?)
   and how many crashes before a profile is "real" given fatal crashes are ~1.5% of data.
3. **Training objective.** Keep severity adapter as domain adaptation and add RAFT/DPO on
   top — or retrain on a cause-summarisation objective? (Want to decide *after* a grounding
   test, evidence-first.)
4. **Why the LLM over a template.** I need to defend that the LLM's synthesis (merging
   co-occurring factors into one prioritised, condition-conditioned, route-level sentence)
   is worth more than a print statement. Is this convincing, or should the LLM be demoted
   to a verbalisation layer?
5. **Delivery form.** In-vehicle voice is the lead candidate; a roadside variable-message
   sign was considered but looks like a weaker thesis (mature tech, small novelty gap, LLM
   adds little). Worth a sanity check.

---

## Questions for you (supervisor)

- Does the **"report that a crash happened" → "explain the non-obvious conditional
  pattern"** framing read as a real, defensible gap?
- Is **statistical significance of segment-level patterns** a strong enough methodological
  core to carry the thesis?
- Is the **temporal-holdout** evaluation rigorous enough as the headline result, given a
  behavioural "does it prevent crashes" study is infeasible?

---

## Links

- [[progress/prof-feedback]] — the full post-presentation feedback this responds to
- [[concepts/system-architecture]] — to be rewritten to match this proposal
- [[progress/future-plan]] — pre-aggregation / RAGAS / three-index work, now core here
- [[entities/stats19-field-reference]] — condition/mechanism fields are the risk substrate
- [[wiki/overview]] — thesis argument, to be aligned with this direction
