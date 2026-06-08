---
title: "Supervisor Feedback — Post-Presentation Redirection"
type: progress
date: "2026-06-04"
tags: [progress, decision, thesis-core]
---

# Supervisor Feedback — Post-Presentation Redirection

Feedback received after the 2026-06-02 class presentation. This is the most significant
course-correction of the thesis so far. Captured here in full because it reframes the
contribution, the unit of analysis, and the delivery model all at once. The wiki's
`overview.md` and `system-architecture.md` are now stale against this and flagged for rewrite.

---

## The core of the feedback

Almost none of it was about implementation. It was about **justification and usability**:
*you've shown you can build it; you haven't shown why a driver wants it or how it reaches
them without making things worse.* Every specific comment is a facet of that.

### Decomposed critiques

1. **"Artificial, not justified, assumes data exists."** The system silently assumes crash
   data exists wherever the driver is. It doesn't — crashes are spatially sparse (503k over
   5 years across the whole UK network). The demo works only where clusters happen to exist.
   *Note: our own architecture page already listed this as the cold-start limitation. The
   designer's known weakness and the examiner's first objection are the same thing.*

2. **"Too UK-focused."** Presented as a STATS19/UK artifact rather than a general problem.
   The method should be framed as jurisdiction-agnostic, with STATS19 as the case study.

3. **"Severity classification is not important."** We already held this internally (F1 was
   logged as "proxy metric only"), but the presentation *led* with the three-way F1 table as
   the headline, signalling that severity was the deliverable. Consequence: the Phase 1
   fine-tuning objective (narrative → severity label) may have trained the model on the wrong
   task for the actual goal.

4. **"Context is missing regardless of what actually happened."** A retrieved historical
   crash describes someone else's situation; the *live* driver's context (speed, current
   weather, time, vehicle) is absent from the reasoning, so output comes out generic. The
   actionable atom is **condition → mechanism** (e.g. "vehicles skid on this wet bend in the
   dark"), and it's only useful if those conditions hold *now*. Severity is the outcome; the
   condition→mechanism link is what transfers to the live driver.

5. **"How does it help and not distract/annoy the driver?"** Driver distraction is itself a
   leading crash cause — an intrusive in-drive system could *increase* risk. The delivery
   mechanism is in tension with the safety goal.

6. **"Real-time is problematic — radius vs speed."** A fixed radius is physically wrong: the
   relevant lookahead is a *time horizon*, not a distance (1 km = 36 s at 100 km/h but 6 min
   at 10 km/h). And LLM generation latency means a per-point warning arrives after the hazard
   has passed. Real-time per-point LLM generation is architecturally doomed for in-drive use.

7. **Constructive suggestion:** a **heat map**, or **route precompute** — driver gives start +
   end, the entire output is computed up front rather than generated live.

---

## The pivot

> **Old:** Real-time GPS → retrieve nearby crashes → LLM generates a per-location,
> severity-flavoured warning.
>
> **New:** *Offline*, mine STATS19 for high-risk road **segments** and their dominant
> **condition→mechanism cause profiles**. At *trip-planning* time, the driver gives
> origin + destination + departure time; the system precomputes a **route briefing** naming,
> for each high-risk segment on the route, the specific actionable causes relevant to the
> **current conditions** — delivered around the drive, not as an in-drive interruption.
> Severity is demoted to a model sanity-check; the deliverable is conditioned cause
> communication. A **heat map** (risk surface, ideally split per cause-type) is the
> complementary macro artifact and the way to present "the overall problem" rather than
> UK anecdotes.

The route-precompute model resolves critiques 4–6 simultaneously: no in-drive latency, no
in-drive distraction, the radius/speed problem dissolves (route is fixed, segment is the
unit), and sparsity is handled because the system only speaks about segments that *have*
a meaningful cluster. Silence elsewhere is correct, not a failure.

---

## Direction (this session) — EXPLORATORY, not committed

**Important: nothing is locked.** The offline segment-profiling + pre-trip route-briefing design
is a **candidate being explored**, not a final decision. The user explicitly does *not* want to
commit to it yet — only to capture it as a direction worth investigating.

- **Real-time is being dropped / questioned** as the delivery model — it's the part the feedback
  most clearly broke (latency, distraction, fixed-radius). The user finds the offline
  end-to-end approach more sensible and *architecturally more interesting and harder* than the
  "artificial" real-time-LLM approach — but is exploring, not deciding.
- **All delivery options stay open** (route briefing, heat map, even a reworked real-time) —
  nothing is foreclosed.
- **Fine-tuning objective: decide after the grounding test.** Keep the existing severity
  adapter as domain adaptation for now; only re-train on a cause-summarisation objective if
  verbalisation quality proves poor. Evidence-driven, no premature retraining.

---

## What survives / what changes

| Existing work | Fate under the pivot |
|---|---|
| Tabular-to-text narratives | **Survives** — substrate for retrieval + verbalisation; lean harder on condition/mechanism fields (skidding, manoeuvre, surface, light, junction) |
| FAISS + embeddings | **Survives** — retrieval now feeds segment aggregation + condition filtering |
| Pre-aggregation grounding fix ([[progress/future-plan]]) | **Promoted to core** — aggregating retrieved crashes into a cause profile *is* the product |
| MI / correlation analysis | **Promoted to core** — it's how overrepresented conditions (the "causes") are found |
| Fine-tuned Gemma (severity adapter) | **Partially survives** — domain adaptation kept; severity *objective* under review |
| Three-way F1 result | **Demoted** to sanity check — never the headline again |
| Real-time online pipeline | **Replaced** by route precompute; real-time kept as explicit future work |
| Three-index retrieval ablation | **Survives, reframed** — retrieval serves segment cause-profile construction |

---

## Open questions / risks to pre-empt (his likely next round)

1. **Is a pre-trip briefing actually used / effective?** The justification problem is moved,
   not yet solved. Need an explicit theory of change: briefing → primed anticipation →
   behaviour change → safer outcome. Lean on anticipatory-awareness road-safety literature;
   ideally a small proxy evaluation.
2. **The "causes" are correlational, not causal.** STATS19 in our dump has **no contributory-
   factors table** — cause is *inferred* from overrepresented conditions + crash mechanics.
   Output must be framed as *patterns*, not proven causes, or it overclaims.
3. **Segment definition + statistical significance.** What is a "segment" (road link? grid
   cell? DBSCAN cluster?) and how many crashes before a profile is real, not noise? With
   Fatal at 1.5%, fatal-specific profiles are data-starved. Needs a base-rate comparison
   (segment distribution vs network baseline) with significance testing. **This is likely the
   new core methodological contribution.**
4. **Why does the LLM earn its place?** If output is "segment X overrepresents wet-skidding
   3×," a template can say that. The LLM must justify itself via synthesis of co-occurring
   factors into prioritised, non-redundant, condition-conditioned, route-level natural
   language. Confront this directly or the "artificial" critique relocates onto the LLM.

---

## Next steps

1. Rewrite `overview.md` — thesis argument restated around cause communication + route
   precompute; remove the "competitive on implied severity prediction" framing (now a
   direct contradiction with this feedback).
2. Rewrite / supersede [[concepts/system-architecture]] — replace the online per-GPS-point
   pipeline with the offline segment-profiling + route-briefing architecture.
3. Define the "segment" unit and the statistical-significance test for a cause profile.
4. Reconcile with [[progress/future-plan]] — the pre-aggregation and three-index work now
   serve the new direction; re-scope accordingly.

---

## Links

- [[progress/future-plan]] — pre-aggregation grounding fix + three-index ablation, now core
- [[progress/speaker-notes]] — the presentation that drew this feedback
- [[concepts/system-architecture]] — superseded by this pivot; flagged for rewrite
- [[concepts/crash-severity-inference]] — severity demoted to sanity check
- [[entities/stats19-field-reference]] — condition/mechanism fields are the new cause substrate
- [[wiki/overview]] — thesis argument now stale, flagged for rewrite
