---
title: "Phase 2 — Literature Grounding & Application Context"
type: plan
date: "2026-06-09"
status: ACTIVE — this is the current working folder
tags: [phase2, literature-review, thesis-core, decision]
---

# Phase 2 — Find the Research Home

> **Phase 1 is archived in `../PHASE1/`** (everything built so far: narratives,
> fine-tuning, FAISS RAG, correlation/spatial analysis, slides, the full wiki).
> Phase 2 starts here. The way we work in this folder: I read papers, paste them
> in, and we talk through them together — building toward a defensible positioning
> for the thesis.

---

## Why we're here (the supervisor meeting, 2026-06-09)

Second meeting after the presentation. What he said, decoded:

1. **Evaluation is fine — stop working on it.** "Not bad at all, can be adjusted
   as needed." Temporal holdout / RAGAS design is good enough to defend; don't
   spend more time polishing it now. Parked.

2. **The "artificial" critique came back — that's the real signal.** Last round I
   answered "not justified" with an *internal* re-scoping (invisible-risk rule,
   pattern-not-event, the funnel — all in `../PHASE1/wiki/progress/NEW_FIX_PROF.md`).
   It didn't land. He still says it's artificial and the **why** is missing.
   Lesson: **a self-constructed justification isn't enough.** I invented my own gap
   ("nav says *that* a crash happened; mine says *why*") and argued it from first
   principles. He wants it **grounded in an existing research conversation.**

3. **"The context behind the system is missing."** The method right now is a
   *floating capability*: offline mining of segment-level, condition-conditioned,
   statistically-significant, non-obvious crash-risk patterns + grounded natural-
   language communication. It has no research *home* — that's what reads as artificial.

4. **"Explore contexts this can be applied to."** His examples — **risk assessment,
   route planning, automated vehicles** — are candidate *application domains*.
   "Apply my thing to X" = find an existing research area where my capability is
   either (a) the missing motivation/why, or (b) a component that plugs into and
   improves an existing pipeline. Then frame the thesis as *advancing that field*,
   with STATS19 as the case study.

5. **The method he prescribed:** read good-journal papers for a week; search by
   keywords like *smart transportation* / *risk assessment* to find prior work I can
   position against and plug into. **READ PAPERS FOR THE NEXT WEEK.**

**The payoff of finding the home field:** it hands me my introduction, my
related-work, my baselines, and my "why" for free — instead of defending a gap I
invented. That is exactly what de-artificializes the thesis.

---

## Goal of the week

Come back with a **one-page positioning memo** that answers:

- Which field does this thesis contribute to?
- What open problem *in that field* (with citations) does it address?
- How is the contribution framed in that field's language?
- What are the baselines / related work I now inherit?

---

## The three contexts he named, as starting hypotheses

Go in with these as hypotheses to test against real papers — not conclusions.

| Context | The established field | Where my method plugs in | As a "home" |
|---|---|---|---|
| **Risk assessment** | Road-safety *network screening* / hotspot ID — Safety Performance Functions, Empirical Bayes, Highway Safety Manual lineage | Traditional screening flags *where* with aggregate counts; mine adds *condition-specific, non-obvious cause diagnosis + human-readable communication* | **Strongest** — most established, data fits natively, clean gap |
| **Route planning** | Risk-aware / safety-aware routing ("safest path") | These need a per-segment risk cost; today they use crude crash counts. My conditioned, significance-tested, explained profiles = a richer risk layer | Strong secondary — clear integration story |
| **Automated vehicles** | AV/ADAS risk priors, risk maps, operational design domain (ODD) | Condition→mechanism profiles as risk priors keyed to weather/light/time | Trendiest but a stretch — better as broader-impact / future work |

Working hypothesis: **risk assessment = home, route planning = best "applied-to"
integration, AVs = aspirational framing.** Confirm or overturn with the literature.

---

## Where to look

There are **two families** of journals, and the thesis needs both. The supervisor's
recommended list (2026-06-09) is AI / intelligent-systems-heavy — a signal that the thesis
is expected to read as **applied AI**, not pure road safety. So pair them: domain journals
give the *risk-assessment home*; the supervisor's AI venues give the *applied-AI framing +
method/novelty home*. **IEEE T-ITS is the bridge — it sits in both.**

**Family A — Road-safety domain venues (the risk-assessment home, from round 1):**
- *Accident Analysis & Prevention* (AAP) — flagship road safety
- *Analytic Methods in Accident Research* (AMAR) — methods-heavy
- *Transportation Research Part C* (emerging tech), *Part F* (driver behaviour / distraction)
- *IEEE Trans. Intelligent Transportation Systems* (T-ITS) ← also Family B; *IEEE Trans. Intelligent Vehicles*
- *Journal of Safety Research*, *Transportation Research Record* (TRR)

**Family B — Supervisor's intelligent-systems / applied-AI list (curated subset):**
- *IEEE T-ITS* (#20), *Expert Systems with Applications* (#7), *Engineering Applications of AI* (#8), *Knowledge-Based Systems* (#5)
- *Smart Cities* (#21), *Decision Support Systems* (#16), *Int. J. Disaster Risk Reduction* (#23), *Internet of Things* (#19), *Sensors* (#9), *Advanced Engineering Informatics* (#10)
- *Machine Learning & Knowledge Extraction* (#3), *Big Data & Cognitive Computing* (#6), *ACM TIST* (#1), *Applied Sciences* (#24), *Sustainability* (#25), *Information* (#18)
- *Optional background only:* *Knowledge Engineering Review* (#11, surveys), *IEEE Intelligent Systems Mag* (#4), *Frontiers in AI* (#13), *Applied AI* (#14)
- *Skip (off-topic / too theoretical):* *Social Networks* (#17), *Smart Agricultural Technology* (#22), *Artificial Intelligence* (#2), *Computational Intelligence* (#12), *JETAI* (#15)

### Journal exploration order — which first, which next, what to search in each

Read in tiers, not all at once. Tier 1 is where the home most likely lives; stop and go
deep the moment a paper looks like a `home` or `integration` hit.

**Tier 1 — Core intersection of AI × road-safety (Days 1–2). START HERE.**
| Journal | What to search in it |
|---|---|
| **IEEE T-ITS** (#20) | `crash risk prediction`, `hotspot identification`, `risk-aware routing`, `LLM transportation` — the single richest venue; covers all three contexts |
| **Expert Systems w/ Applications** (#7) | `crash severity prediction`, `road safety decision support`, `accident risk machine learning` — applied-AI framing + ready baselines |
| **Engineering Applications of AI** (#8) | `traffic accident prediction`, `road risk assessment AI` |
| **Knowledge-Based Systems** (#5) | `crash prediction`, `risk assessment framework`, `knowledge extraction traffic` |
| *(parallel)* **AAP + AMAR** | `network screening`, `safety performance function`, `empirical Bayes`, `high-risk segments` — the risk-assessment methodology + the gap |

**Tier 2 — Application-context & framing venues (Days 3–4).**
| Journal | What to search in it |
|---|---|
| **Smart Cities** (#21) | `urban road safety`, `risk map`, `smart mobility safety` — the "smart transportation" keyword the prof named |
| **Decision Support Systems** (#16) | `driver advisory`, `route decision support`, `risk warning system` — frame the deliverable *as a DSS* |
| **Int. J. Disaster Risk Reduction** (#23) | `risk assessment framework`, `risk communication`, `early warning` — borrow risk-assessment + communication structure |
| **Internet of Things** (#19), **Sensors** (#9) | `connected vehicle risk`, `V2X safety`, `real-time traffic risk sensing` — the data-pipeline / route-planning / AV-input angle |
| **Advanced Engineering Informatics** (#10) | `infrastructure risk`, `spatial risk analytics` |

**Tier 3 — Method novelty & breadth sweep (Day 5).**
| Journal | What to search in it |
|---|---|
| **MAKE** (#3) | `explainable ML`, `pattern/knowledge extraction` — supports the "extract + explain" claim |
| **Big Data & Cognitive Computing** (#6) | `big-data crash analytics`, `spatial data mining` |
| **ACM TIST** (#1), **Applied Sciences** (#24), **Sustainability** (#25), **Information** (#18) | keyword sweeps: `LLM road safety`, `RAG transportation`, `natural language risk communication`, `accident pattern mining` — megajournals, lower signal, search-only |

**Keyword clusters (search by cluster):**
- *Risk assessment:* `network screening`, `hotspot identification`, `high-risk road segments`, `safety performance function`, `empirical Bayes crash`, `road segment crash risk`
- *Smart transportation:* `intelligent transportation systems risk`, `context-aware driving risk`, `real-time crash risk prediction`
- *Route planning:* `risk-aware route planning`, `safest path routing`, `safety-aware navigation`
- *AV / ADAS:* `autonomous vehicle risk map`, `ADAS risk prediction`, `operational design domain risk`
- *My novelty edge:* `large language model traffic safety`, `natural language road risk communication`

---

## Day-by-day

*(Maps onto the journal tiers above: Days 1–2 = Tier 1, Days 3–4 = Tier 2, Day 5 = Tier 3.)*

- **Days 1–2 — Risk assessment / network screening.** How the field finds & ranks
  risky locations (SPF, Empirical Bayes, hotspot methods). Output: state precisely
  what they *don't* do that I do.
- **Day 3 — Route planning.** How is per-segment risk represented in routing today?
  Where's the gap my profiles fill?
- **Day 4 — AVs/ADAS + driver behaviour (Part F).** Risk priors for AVs; and the
  anticipatory-awareness / distraction literature that justifies *why a briefing
  helps a human driver*.
- **Day 5 — LLM-in-transportation.** Who already uses LLMs for traffic/safety, for
  what, and where the white space is for my communication layer.
- **Days 6–7 — Synthesize.** Pick the primary home; write the positioning memo +
  annotated bibliography.

---

## How to read (so a week of papers converges)

1. **Triage first** — abstract + figures + conclusion, keep/discard in ~5 min.
   Don't deep-read everything.
2. For each keeper, extract a fixed template:
   **problem · method · data · how they represent risk · what's missing · where my
   method plugs in · is this my *home* or a *neighbour*?**
3. Tag each paper:
   - `home` — defines the field I contribute to
   - `integration` — my method feeds it
   - `related-work` — baseline / comparison
   - `borrow` — a method I can reuse (e.g. Empirical Bayes for the significance step)

---

## How we work in this folder

- I read and **paste papers in here**; we discuss each one against the template above.
- Each substantive paper gets ingested into the wiki via the standard workflow
  (source page + concept/entity updates) — see `../CLAUDE.md`.
- The end-of-week **positioning memo** becomes the basis for finally rewriting
  `overview.md` and `system-architecture.md` (they've correctly been waiting for the
  direction to settle).

---

## What Phase 1 leaves us (assets that survive into any direction)

- Tabular-to-text STATS19 narratives
- Fine-tuned Gemma severity adapter (domain adaptation)
- FAISS index + embeddings (retrieval substrate)
- MI / correlation + spatial/hotspot analysis (`../PHASE1/analysis/`)
- The segment-significance + condition-profiling design (`../PHASE1/wiki/progress/NEW_FIX_PROF.md`)

---

## Links

- `../PHASE1/wiki/progress/prof-feedback.md` — round-1 post-presentation feedback
- `../PHASE1/wiki/progress/NEW_FIX_PROF.md` — round-1 response (the design he still calls artificial)
- `../PHASE1/wiki/overview.md` — thesis argument, to be realigned after this week
- `../PHASE1/wiki/concepts/system-architecture.md` — to be rewritten after the home field is chosen
