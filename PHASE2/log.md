# Phase 2 — Wiki Log

Append-only chronological record for the active phase. One entry per operation.
Phase 1's log is archived at `../PHASE1/log.md`.
Parse with: `grep "^## \[" log.md | tail -10`

---

## [2026-06-09] ⏸ RESUME POINT — read this first
- **Where we are:** Phase 2 just started. After the 2026-06-09 supervisor meeting the
  project pivoted from *building* to *grounding*. The system works but reads as
  "artificial" because it has no research home — the **why/context is missing**.
- **The task:** spend the next week reading good-journal papers to find the field this
  work contributes to (hypotheses: risk assessment = home, route planning = applied-to,
  AVs = aspirational). Eval is fine per the supervisor — do **not** keep polishing it.
- **Structure change:** all prior work moved to `../PHASE1/` (frozen archive); Phase 2
  is a fresh wiki here. `CLAUDE.md` updated to point the schema at `PHASE2/`.
- **Deliverable:** end-of-week positioning memo (which field, cited gap, framing,
  baselines) → then realign overview + architecture.
- **The plan in full:** [[PHASE2/PLAN]].

## [2026-06-09] structure | Project split into PHASE1 (archive) + PHASE2 (active)
- Moved all Phase 1 work into `../PHASE1/` via `git mv` (history preserved); kept
  CLAUDE/git/Obsidian/env infrastructure at root.
- Created `PHASE2/` with `PLAN.md` + a fresh wiki (index, log, overview, raw/).
- Updated `CLAUDE.md`: directory structure, read-only archive rule, session-start
  protocol now point at PHASE2.
- Notable: fresh-but-linked chosen over continue-in-place — Obsidian resolves
  `[[wikilinks]]` vault-wide so PHASE1 stays reachable while the reframe gets a clean slate.

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
