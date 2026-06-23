# ESWA — Phase-3 Reading-Pass Record (Tier 1, Journal 4)

**Pass:** 2026-06-22, risk-aware-routing direction. Light confirmatory pass — Sarraf & McGuire 2020
(the one ESWA paper that matters) was already deep-read on 2026-06-18, see
[[ESWA-deepread]] (`carry_over/`). Goal of this pass: confirm no *second* routing gem hides in ESWA.

**Keywords swept:** `safe route planning` / MCDM safe route (2026-06-22) ·
`crash risk route recommendation` (2026-06-22).

**Result: 0 new keepers across both keywords. ESWA pass = Sarraf only. TIER 1 CLOSED.**

## What the sweeps returned

Both keyword runs returned almost entirely **wrong-domain noise**:
- **Robotics / UAV / USV / AGV motion planning** ("path planning" in the *move-a-robot-through-space*
  sense, not the *rank-road-routes-by-crash-risk* sense): RRT*, ant-colony UAV planning, manipulator
  roadmaps, maritime collision avoidance, humanoid footstep planning, etc. Same overloaded-term trap as
  TR-C's `safe routing` → VANET networking.
- **General expert-systems grab-bag:** LLMs, cybersecurity (DDoS/intrusion detection), finance/business
  (TOPSIS airline competition, Z-score bankruptcy), driver-monitoring (EEG/fatigue), supply chains.

**The only on-domain hit under BOTH keywords was the same paper:**
- **Sarraf & McGuire 2020 — "Integration and Comparison of Multi-Criteria Decision Making Methods in
  Safe Route Planner"** — already deep-read (the MCDM router: Dijkstra + AHP/PROMETHEE; WCR risk score
  normalised by AADT; Spearman / Average-Overlap / DCG eval suite; vehicle-blind). See [[ESWA-deepread]].

Two borderline-and-rejected: *"Critical Factors for Emergency Vehicle Routing Expert Systems"*
(emergency dispatch, not crash-risk route ranking) and *"Smart Streetlight Framework for Collision
Prediction"* (prediction, not routing). Neither earned an abstract read.

## Conclusion
ESWA's contribution to the thesis was always **Sarraf** (router + eval template), and it is fully
captured. Two keyword sweeps confirm there is **no second safe-routing paper** in ESWA under the
crash-risk sense. **Tier 1 (T-ITS · TR-C · AAP · ESWA) is now fully swept and CLOSED.**

**Gap-test note:** even ESWA — the MCDM safe-routing home — yields **no vehicle-type-conditioned**
safe routing. The gap holds across all four Tier-1 journals.

## Links
- [[ESWA-deepread]] (`carry_over/`) — Sarraf deep read (router + WCR + eval suite)
- [[TR-C-deepread]] — Mansoor/Sohrabi&Lord/Kavta/Chandra/Hu (routing mechanism + CLQ gate)
- [[tier1_journal3/AAP-deepread]] — Pathivada/Barabino/Lee (engine + the spatial-divergence brick)
- [[positioning-memo]] — evidence map · [[PLAN]] — keyword clusters
