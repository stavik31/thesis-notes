# Overview — Phase 2

> Status memo for the active phase. Phase 1's overview is archived at
> [[../PHASE1/wiki/overview]]. This page will be rewritten into the real thesis
> argument once the week of reading settles the research home.

## Thesis Argument (in flux — being grounded this week)

The technical capability is settled: **mine historical crash data offline to find road
segments where a specific, non-obvious, condition-dependent risk pattern is statistically
overrepresented, and communicate it in grounded natural language.** What is *not* settled
— and what Phase 2 exists to fix — is the **research home**: which established field this
contributes to, stated in that field's language, with its citations, gap, and baselines.

The supervisor's repeated "artificial" critique means the current first-principles
justification ("nav reports *that* a crash happened; mine explains *why*") is not enough.
The argument must be re-anchored to an existing literature. Three candidate homes are under
test: **road-safety risk assessment / network screening** (leading hypothesis),
**risk-aware route planning** (best integration story), and **AV/ADAS risk priors**
(aspirational). See [[PHASE2/PLAN]].

## State of the Project

- **Phase 1: complete and archived** (`../PHASE1/`). Built: tabular-to-text STATS19
  narratives, a fine-tuned Gemma severity adapter, a FAISS RAG pipeline, MI/correlation
  and spatial/hotspot analyses, and the segment-significance + condition-profiling design
  ([[../PHASE1/wiki/progress/NEW_FIX_PROF]]).
- **Phase 2: just started (2026-06-09).** Mode is *grounding*, not building. One week of
  structured reading to find the home field; eval work is explicitly parked (the
  supervisor judged it fine).
- **Next:** ingest papers as they're read → end-of-week positioning memo → realign this
  overview and a new architecture page.

## Key Open Questions

1. Which field is the **home** vs. a *neighbour* / integration target?
2. What is the precise, **cited** gap in that field that this work fills?
3. What baselines and related work does that field hand us?
4. (Deferred) Does the LLM earn its place over a template, in that field's terms?

## Literature Landscape

To be built this week. Entry points: *Accident Analysis & Prevention*, *Analytic Methods
in Accident Research*, *Transportation Research Part C/F*, *IEEE T-ITS / T-IV*. Keyword
clusters and method anchors (SPF, Empirical Bayes, network screening, risk-aware routing)
are listed in [[PHASE2/PLAN]].

## Links

- [[PHASE2/PLAN]] — the reading plan this overview will be rebuilt from
- [[wiki/progress/2026-06-09]] — Phase 2 kickoff note
- [[../PHASE1/wiki/progress/prof-feedback]] — round-1 feedback
- [[../PHASE1/wiki/progress/NEW_FIX_PROF]] — the design the "artificial" critique targets
