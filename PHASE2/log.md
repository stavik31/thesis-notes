# Phase 2 — Wiki Log

Append-only chronological record for the active phase. One entry per operation.
Phase 1's log is archived at `../PHASE1/log.md`.
Parse with: `grep "^## \[" log.md | tail -10`

---

## [2026-06-09] ⏸ RESUME POINT — read this first
- **Where we are:** Phase 2 = *grounding* mode (find the research home so the system stops
  reading as "artificial"). **Tier 1, Journal 1 (IEEE T-ITS) is done.** Two papers deep-read
  and recorded in `raw/papers/tier1_journal1/T-ITS-abstract-refs.md` (full reads on top,
  5 abstract-only refs below).
- **What the two reads established:** direction is *confirmed* (multimodal/LLM crash work is
  live + segment risk-for-drivers is accepted), home field located = **road-safety risk
  assessment (SPF / Empirical Bayes / Highway Safety Manual)** layered with multimodal ML.
  Sobering finding: our route-risk-map *deliverable already exists* (Jiang 2022) → our novelty
  is narrower than the NEW_FIX_PROF framing and lives ONLY in **condition-conditioning + the
  natural-language WHY + significance/overrepresentation**.
- **The sharpened gap (carry this):** the field either encodes crash text → *predicts* an
  outcome (event-level, enforcement — Li 2025) or aggregates crashes → *numeric risk score*
  → heat map (segment-level, routing — Jiang 2022). **Neither conditions on the live
  situation, neither explains *why* in natural language.** That white space is the thesis.
- **Test question to carry into every future paper:** *is anyone doing condition-conditioned,
  explanation-generating segment risk?* Every "no" is a brick in the gap.
- **NEXT:** Tier 1, Journal 2 = **Expert Systems with Applications**. Search:
  `crash severity prediction`, `road safety decision support`, `accident risk machine learning`.
- **Working style (locked):** record papers as lightweight per-journal md entries (full title
  + progress phrase), NOT the full wiki INGEST workflow. Model: Sonnet for triage, Opus for
  deep reads. Progress so far ≈ 15% of the reading. Correct road, long to go.
- **The plan in full:** [[PHASE2/PLAN]] · triage state: [[wiki/progress/journal-triage]].

## [2026-06-09] structure | Project split into PHASE1 (archive) + PHASE2 (active)
- Moved all Phase 1 work into `../PHASE1/` via `git mv` (history preserved); kept
  CLAUDE/git/Obsidian/env infrastructure at root.
- Created `PHASE2/` with `PLAN.md` + a fresh wiki (index, log, overview, raw/).
- Updated `CLAUDE.md`: directory structure, read-only archive rule, session-start
  protocol now point at PHASE2.
- Notable: fresh-but-linked chosen over continue-in-place — Obsidian resolves
  `[[wikilinks]]` vault-wide so PHASE1 stays reachable while the reframe gets a clean slate.

## [2026-06-09] reading | T-ITS Tier-1 deep reads — multimodal twin + safe route mapping
- Record: `raw/papers/tier1_journal1/T-ITS-abstract-refs.md` (full reads on top + 5 abstract refs)
- Li et al. 2025 (Multimodal crash risk of violations): closest twin; validates text+tabular+LLM
  direction; clean inversion (they encode→predict event-level for enforcement; we generate→explain
  segment-level for drivers). Borrow: TabNet, text-categorisation pipeline, imbalance handling.
- Jiang et al. 2022 (Safe Route Mapping): the bigger find — roots us in SPF/Empirical Bayes/HSM
  (the risk-assessment home) AND shows our route-risk-map deliverable already exists → novelty
  must live in condition-conditioning + NL why + significance.
- Notable: gap now sharply defined across both papers; our raw idea is NOT novel on its own —
  this is good to learn now. Next journal: Expert Systems with Applications.

## [2026-06-09] progress | Journal triage log started — T-ITS shortlist
- Page: [[wiki/progress/journal-triage]]
- Workflow set: search → shortlist titles → abstracts (decide) → full text for keepers →
  deep-read + ingest, one journal at a time.
- T-ITS: 7 of ~25 results kept for abstract review (multimodal-crash-risk twin, risk-assessment
  survey, XAI severity, vehicle-group prediction, safe-route mapping, in-vehicle warning, GAN
  imbalance); rest skipped at title stage as off-layer micro-AV/control work.

## [2026-06-09] plan | Journal exploration strategy added to PHASE2/PLAN
- Page: [[PHASE2/PLAN]]
- Folded the supervisor's 25-journal list into the plan: triaged to a relevant subset,
  paired with the round-1 road-safety domain venues into two families (domain = risk-
  assessment home; AI list = applied-AI framing/method home; T-ITS bridges both).
- Added a 3-tier exploration order with per-journal search terms: Tier 1 = AI×road-safety
  intersection (T-ITS, ESWA, EAAI, KBS + AAP/AMAR), Tier 2 = application/framing (Smart
  Cities, DSS, IJDRR, IoT, Sensors), Tier 3 = method/breadth sweep (MAKE, BDCC, megajournals).
- Notable: the prof's list being AI-heavy is itself a signal — the thesis is expected to
  read as applied AI, so the framing should foreground the intelligent-systems angle.

## [2026-06-09] progress | Phase 2 kickoff — supervisor pushed for literature grounding
- Page: [[wiki/progress/2026-06-09]]
- Notable: eval declared fine by supervisor (stop polishing); the "artificial" critique
  returned, meaning the contribution needs an external research home, not more internal
  self-justification; week of reading planned around risk assessment / route planning / AVs.
