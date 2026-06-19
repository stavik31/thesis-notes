# Phase 3 — Wiki Log

Append-only chronological record for the active phase. One entry per operation.
Phase 1's log: `../PHASE1/log.md`. Phase 2's log: `../PHASE2/log.md`.
Parse with: `grep "^## \[" log.md | tail -10`

---

## [2026-06-17] structure | Phase 3 created — pivot to risk-aware routing + data niche
- Pages: [[PHASE3/PLAN]], [[PHASE3/positioning-memo]] (living), [[PHASE3/index]], this log.
- **Trigger: 2026-06-17 supervisor meeting** (after presenting the Phase 2 CRM/LLM memo).
  Decoded: (1) **drop the LLM** — faithfulness/hallucination unsolvable in the time,
  language is distracting + per-person, not solidified enough to anchor a thesis;
  (2) **route planning is the home** ("very good"); (3) **complexity over novelty** —
  "I don't always need novelty, but I always need complexity of the system"; (4) **find a
  data niche nobody explored** — e.g. condition routing on **vehicle type** (his example);
  (5) other datasets OK to open more niches if needed.
- **New direction:** risk-aware route planning (home = Jiang 2022 / Sarraf 2020), with
  **vehicle-type-conditioned segment crash risk** as the novelty, STATS19 as the engine
  (Gao 2024 lineage), **no NL/LLM layer**, output = ranked routes / vehicle-specific risk
  map. Full living statement in [[PHASE3/positioning-memo]].
- **Corpus status (honest):** risk-modeling lit is well-covered (inherited from Phase 2);
  the routing *home* (Jiang deep + Sarraf/de Souza abstracts) and the vehicle-type *niche*
  (Zhu abstract) are THIN → the target of this reading pass. Phase 2 deep reads on the
  LLM/explanation half (Zhang/Gyawali/Hussien/Smetana/Wu/TrafficRiskGPT/Tab-Text) are
  demoted to future-work.
- **Combining niches (user Q):** allowed and encouraged as a complexity feature, BUT
  multi-dimensional conditioning multiplies STATS19 sparsity (~96% zero-inflation, fatal
  ~1.5%) → design rule: vehicle type primary, weather/time secondary only where a per-cell
  count is significant, with graceful fallback. Logged in PLAN + positioning.
- Notable: **Next — Tier 1 reading pass (T-ITS, TR-C, AAP, ESWA) on routing + vehicle-type
  keywords.** Mirror Phase 2's lightweight per-journal `*-abstract-refs.md` records.

## [2026-06-19] ⏸ CHECKPOINT — end of day, read this first next session
- **State: AAP (Tier 1, Journal 3) sweep STARTED — keywords 1–2 of 5 done; both full-text keepers deep-read.**
- **What got done today:** (1) AAP keyword 1 `risk aware route planning` → 1 abstract keeper (Changsha
  demand-side), confirmed AAP isn't a routing-system venue; (2) AAP keyword 2 `motorcycle crash risk segment`
  → 5 abstract keepers + 2 full-text deep reads (Opus): **Pathivada 2025** (motorcycle segment SPF;
  per-type slice → **under-dispersion** → CMP/HTCMP not NB/ZITD; EB ranking; homogeneous segmentation) and
  **Barabino 2021** (★★ **R=H·V·E** per-bus-route risk → section-sum → quartile ranking = closest
  per-type→route-risk→ranked-output precedent). New folder `tier1_journal3/` with `AAP-abstract-refs.md`
  + `AAP-deepread.md`.
- **Decisions moved:** count model is now a **per-type choice, not a default** (new Open Decision #3b:
  ZITD vs CMP/HTCMP — measure dispersion in the probe); **EB** added as significance/screening gate
  candidate #4; **homogeneous segmentation** = cheap HSM-aligned answer to segment-definition #2; exposure
  confound reconfirmed (both papers use aggregate exposure). The **H·V·E decomposition** is now a concrete
  thing to adopt for the route-risk scalar.
- **Where each layer stands (unchanged headline):** routing home = STRONG; engine = solid (Gao) **+ now a
  per-type count-family fork (CMP/HTCMP) when under-dispersed**; significance gate = 4 candidates (Wei, Wang,
  Hu-CLQ, EB). **NICHE = still thin where it's load-bearing** — these confirm motorcycle *segment risk* is
  buildable but give NO **spatial-divergence-by-type** (different segments risky for different types).
- **Resume plan (next session):** (1) **AAP keywords 3–5** = top priority — `truck/HGV crash risk`,
  `vehicle type crash heterogeneity`, `vulnerable road user crash` — hunting the spatial-divergence brick;
  (2) light ESWA pass (Sarraf already deep-read); (3) then **STATS19 per-type density probe** (Open Decision
  #6) — and now it must report **per-type dispersion + zero rate** (picks ZITD vs CMP), plus the CLQ
  divergence analysis (generates the niche evidence + headline).
- **Two outstanding decisions (carried):** time-optimization axis (contribution vs borrow); per-type exposure
  (DfT AADF by vehicle type?).
- Nothing half-written; abstract-refs, deep-read record, positioning-memo, index, log all consistent. Committed + pushed at EOD.

## [2026-06-19] reading | AAP Tier-1 sweep started (kw 1–2) + 2 deep reads
- Records: [[AAP-abstract-refs]] (sweep) + [[tier1_journal3/AAP-deepread]] (full reads), new `tier1_journal3/`.
- **Keyword 1 `risk aware route planning`:** ~90 titles, 1 abstract keeper (Changsha ALPR — motorists
  do trade efficiency for safety at night/non-livelihood → demand-side brick, complements Kavta). AAP
  is not a routing-system venue (confirmed).
- **Keyword 2 `motorcycle crash risk segment`:** 5 abstract keepers + **2 full-text → deep-read (Opus):**
  - **Pathivada et al. 2025 — motorcycle segment SPF (Kentucky).** ★ Key finding: motorcycle-only
    segment crashes were **UNDER-dispersed** (variance < mean) → NB/ZITD (built for over-dispersion)
    inappropriate; needs **CMP/HTCMP**. First *real-data* signal that the per-type slice can **flip the
    count regime** → directly feeds Open Decision #6. Also donates **Empirical Bayes** high-crash ranking
    (gate/screening candidate #4, HSM-standard) + **homogeneous segmentation** (cut where road class/lanes/
    speed/AADT changes → cheap answer to #2). Caveat: controlled zeros to ~20% (not STATS19's true rate);
    aggregate-AADT exposure = per-type exposure confound again. Single-type, no divergence, no routing.
  - **Barabino et al. 2021 — bus crash risk, real network.** ★★ **structural precedent**: per-vehicle-type
    **R = H·V·E** (NB frequency × binary-logistic severity × passenger·km exposure), computed per
    homogeneous section → **summed to route risk** → quartile-cut 4-level ranking. The closest existing
    per-type → route-risk → ranked-output pipeline in the whole corpus (bus-only, fixed lines = *screening,
    not routing*). Donates the **H·V·E decomposition + section-sum + binary-severity collapse** for rare
    fatals. Bonus brick: third-party vehicle type shifts severity odds (heavy-veh 1.91×, 2/3-wheeler 2.16×
    vs car) = another "type matters."
- **Net moves:** (1) count model is now a **per-type decision, not a default** (ZITD vs CMP/HTCMP, measure
  dispersion in the probe → added Open Decision #3b); (2) EB joins the significance-gate shortlist (#4 with
  Wei/Wang/Hu-CLQ); (3) a complete per-type route-risk scalar (H·V·E) is now in hand to adopt; (4) exposure
  confound reconfirmed (both papers use aggregate exposure).
- **Niche still thin where it's load-bearing:** these confirm motorcycle *segment risk* is buildable, but
  give **no spatial-divergence-by-type** (different segments risky for different types). That's keywords 3–5
  + the CLQ-on-STATS19 probe. Gap test holds: no cross-type routing anywhere.
- Bookkeeping: deep-read record, abstract-refs (kw1+kw2, full-text → deep-read), positioning-memo (niche +
  gate tables, Open Decisions #2/#3/#3b/#6), index (+footer), log.
- Notable: **Next — AAP keywords 3–5** (`truck/HGV crash risk`, `vehicle type crash heterogeneity`,
  `vulnerable road user crash`), hunting the spatial-divergence brick; then light ESWA pass + STATS19 probe.

## [2026-06-18] ⏸ CHECKPOINT — end of day, read this first next session
- **State: Tier 1 Journals 1 (T-ITS) + 2 (TR-C) fully swept; all keepers deep-read.** Big productive day.
- **What got done today:** (1) deep-read all 6 carry-over PDFs → 3 per-journal records (T-ITS/ESWA/AAP);
  (2) filed standing+gap query [[2026-06-18-where-we-stand-and-remaining-gaps]] + sharpened PLAN keywords
  (added spatial-divergence + segmentation clusters; flagged feasibility = not-a-reading-question);
  (3) T-ITS sweep (4 kw → 1 weak keeper); (4) TR-C sweep (3 kw) → **5 deep reads**: Mansoor 2026 ★★★
  (class-specific route sets + mean-excess CVaR = the per-type routing mechanism), Sohrabi & Lord 2022
  (operational home; 8%→+23%), Kavta 2025 (demand-side niche), Chandra 2014 (user-conditioned routing +
  Pareto/Yen machinery), Hu 2018 (★ Colocation Quotient = per-type spatial significance gate / tool to
  GENERATE niche evidence); (5) pinned **Scope & depth** in positioning-memo and **corrected the
  novelty language** → distinctive *direction* (borrowed methods, new data) vs breakthrough novelty
  (not required); premise concern = **justification (does it diverge?), not novelty.**
- **Where each layer stands:** SYSTEM/routing home = STRONG (engine→router structure + per-type
  mechanism located). ENGINE = solid (Gao). SIGNIFICANCE GATE = 3 candidates (Wei case-crossover, Wang
  χ²-BN, Hu CLQ). **NICHE (vehicle-type) = still the thin spot** — only analogical premise evidence;
  but reframed (CLQ lets us manufacture it on STATS19).
- **Gap test (strongest yet):** T-ITS+TR-C, 2010–2026, **no paper routes on a data-driven per-vehicle-
  type risk surface.** White space confirmed; Mansoor hands the mechanism.
- **Resume plan (next session):** (1) **AAP vehicle-type sweep = top priority** — `motorcycle crash
  hotspot`, `vehicle class network screening`, `truck/HGV crash risk`, `vehicle type crash heterogeneity`
  (direct per-class evidence should live here); (2) light ESWA pass (Sarraf already deep-read); (3) then
  **STATS19 data analysis** — run the per-type density probe EARLY (Open Decision #6, feasibility +
  existential) and the CLQ divergence analysis (do motorcycle vs HGV vs car hotspots differ?) =
  generates the niche evidence + the headline result.
- **Two outstanding decisions:** time-optimization axis (contribution vs borrow → add routing-OR keyword
  cluster or not); per-type exposure (DfT AADF by vehicle type?).
- Nothing half-written; all records, evidence map, index, log consistent. Committed + pushed at EOD.

## [2026-06-18] reading | TR-C deep read — Hu 2018 colocation (method donor) + premise reframe
- Appended to [[TR-C-deepread]]. **Full read corrected the keeper note:** the results **combine** ped+cyclist
  and condition on **severity × intersection-type** (not ped-vs-cyclist, not motor-vehicle classes) → premise
  is **analogical, not direct.**
- **The prize is the METHOD — Colocation Quotient (GCLQ + LCLQ).** A per-category **spatial significance
  test**: "does crash-type A significantly colocate with feature-type B vs random?", expected value 1,
  **Monte-Carlo** p-values, **network-distance**, micro-level (**MAUP-aware**). → candidate **significance
  gate #3** (with Wei case-crossover, Wang χ²-BN) + input to **segmentation** decision; ties to Phase-1
  spatial/Cramér's-V assets.
- **Premise reframe (important):** spatial-divergence-by-type being thin in the literature is NOT evidence
  it's false — colocation-in-transport-safety is itself new (2018, "first effort"). **The thesis can
  MANUFACTURE the premise** by running CLQ on STATS19 per vehicle type. This makes the per-type density
  probe (Open Decision #6) doubly central: feasibility check *and* first step of producing niche evidence.
- Bookkeeping: deep-read record, abstract-refs status, positioning-memo (evidence map + reframe note +
  Open Decision #3 now lists CLQ), index, log.
- Notable: **TR-C fully done + all its keepers deep-read.** Next Tier-1 priority = AAP vehicle-type niche
  (motorcycle/HGV segment risk; spatial-divergence keywords) — and now we have the CLQ tool to apply to it.

## [2026-06-18] reading | TR-C keyword 3/3 (`crash risk routing`) — TR-C sweep COMPLETE
- Appended to [[TR-C-abstract-refs]]. Keyword mostly returns crash-*prediction* (Abdel-Aty/Quddus engine
  lineage, have Gao) + AV/behaviour noise; most routing hits already deep-read. **2 new keepers:**
  - ⏳ **Hu, Zhang, Shelton 2018 — dangerous intersections for pedestrians vs cyclists (colocation).**
    Full-text pending. Best **spatial-divergence-by-type** evidence yet + **colocation-quotient** method
    (per-type spatial significance test → significance-gate/segmentation candidate; ties to Phase-1 spatial
    assets). Caveats: ped/cyclist not motor-vehicle class; hotspot not routing.
  - ✓ **Yang, Ye, Zhao 2015 — speed limits/selection + network equilibrium** (abstract). Class-specific
    crash risk in route+speed choice at equilibrium = predecessor to Mansoor; speed→crash mechanism.
- **TR-C COMPLETE — all 3 keywords swept.** Tally: 4 deep-read (Mansoor, Sohrabi&Lord, Kavta, Chandra) +
  Hu pending full-text + abstract keepers (Dijkstra, Yang, bi-attribute NYC, NL Sustainable-Safety, hazmat
  CVaR). Gap test across 2010–2026: established crash-risk-routing/equilibrium + spatial-crash lineage,
  **vehicle type = the unfilled slot**; no motor-vehicle-class routing anywhere.
- Notable: awaiting Hu PDF. Next Tier-1 priority = **AAP vehicle-type niche evidence** (motorcycle/HGV
  segment risk; spatial-divergence keywords) — the one premise still thin.

## [2026-06-18] reading | TR-C keyword-2 deep read — Chandra 2014 + Scope&depth pinned
- Record: appended to [[TR-C-deepread]]. Also pinned **Scope & depth** section in [[positioning-memo]]
  (niche=novelty/risk layer; routing=system/complexity layer; both credible; depth-in-risk buys novelty,
  depth-in-routing buys complexity only — resolves the "optimization vs niche" confusion).
- **Chandra 2014 — closest user-conditioned routing precedent, but parametric.** Safe path-finding for
  two user types (older drivers, bicyclists), differentiated ONLY by speed + perception-reaction time;
  safety indicators are **generic, crash-data-free** (TTC from Poisson/GUE traffic density), **no per-type
  risk surface.** Strengthens the niche 3 ways: (1) gap brick — even the user-framed paper has no per-type
  risk surface; (2) contrast — Chandra avoids crash data, we exploit STATS19 per-type history (our novelty
  crystallises against it); (3) donates the **multi-objective Pareto/non-inferior shortest-path machinery**
  (Yen's p-shortest-paths → Pareto filter) for the routing layer + a crash-data-free TTC indicator as
  graceful-fallback material.
- **Gap test now spans 2014–2026, 4 papers, none with a data-driven per-vehicle-type risk surface in routing.**
- Bookkeeping: deep-read record, abstract-refs status, positioning-memo evidence map + scope note, index, log.
- Notable: TR-C keyword 3/3 `crash risk routing` still pending.

## [2026-06-18] reading | TR-Part-C keyword 2/3 (`risk-based navigation`) + time-axis flag
- Record appended to [[TR-C-abstract-refs]]. ~90% maritime/aviation/UAV/AV-control noise. 2 strong
  abstracts → **1 full-text keeper** (Safety-based path finding for older drivers & bicyclists —
  user-class-conditioned safe routing, crash-data-free indicators; PDF incoming) **+ 1 downgrade**
  (Adaptive vehicle routing for risk-averse travelers = travel-time reliability, not crash).
- **Gap-strengthening nuance:** the older-driver/bicyclist paper's safety indicators are "generic
  irrespective of road user type" → user-*motivated*, not user-*conditioned* in the risk layer. Even
  the vulnerable-road-user routing paper doesn't compute a per-type risk surface → niche still open.
- **Time-optimization axis flagged (user question):** math-heavy time+safety joint optimization is
  anchored by Mansoor 2026 (METT+MECRC/VI) + Sarraf (MCDM) + hazmat CVaR; the standalone routing-
  optimization literature (multi-objective/Pareto/time-dependent/stochastic shortest path) is NOT yet
  a swept pillar. Decision pending: routing optimization as contribution (add keyword cluster) vs
  borrowed component (Mansoor+Sarraf suffice).
- Notable: awaiting older-driver/bicyclist PDF; then keyword 3/3 `crash risk routing`.

## [2026-06-18] reading | TR-Part-C deep reads — 3 full-text from keyword 1
- Record: [[TR-C-deepread]] (`raw/papers/tier1/tier1_journal2/`). All 3 promoted papers now read in full.
- **Mansoor, Li, Chen 2026 ★★★ — the structural ancestor.** Class-specific route choice sets (route
  enters class m's set iff its safety score Θ ≥ class threshold Θ_req) + mean-excess CRC (CVaR on the
  fatal/serious tail), generalized cost = METT+MECRC, VI/two-stage. Classes by *safety preference*, not
  vehicle type — **re-key Θ_req on vehicle type = the per-type routing mechanism.** Also borrowable: the
  Dijkstra-2013 roadway-characteristic safety score (road-class shares + distance + intersection density;
  crash-data-FREE). Names heavy-vehicle risk in motivation; vehicle type absent even from future work.
  Scale caveat: network equilibrium/assignment, not individual navigation → conceptual ancestor, Sarraf
  stays the operational router.
- **Sohrabi & Lord 2022 — operational home + motivation.** 29,382 Texas segments; NB crash models
  **stratified by weather** (adverse vs clear; adverse 2.7× rate); route risk = complement of product of
  segment survival probs; safest≠shortest, **8% time → +23% crash**, safest route varies by weather. S-RGS
  requirement list ≈ thesis build spec. Dominique Lord co-author. No vehicle type.
- **Kavta et al. 2025 — demand-side niche brick.** SP experiment, delivery riders (Amsterdam/Copenhagen)
  trade time for safety (VRR/WTA); proves a vehicle class *wants* type-specific safe routing. Industry
  co-author (Just Eat Takeaway). Behavioural, not a build method.
- **Routing home now = 5 deep-read papers** (Jiang, Sarraf, + these 3). Gap test strongest yet: machinery
  + acknowledged heavy-vehicle risk exist, but unconnected — that connection is the thesis.
- Bookkeeping: TR-C-abstract-refs status → deep-read; positioning-memo evidence map + structural note
  updated; index + log. Notable: next TR-C keyword 2/3 `risk-based navigation`.

## [2026-06-18] reading | TR-Part-C sweep (Tier 1, Journal 2) — keyword 1/3
- Record: [[TR-C-abstract-refs]] (`raw/papers/tier1/tier1_journal2/`). Keyword: `safe route planning`
  (re-phrased from `safe routing`, which mis-fired into VANET secure-packet-routing — networking sense).
- **The routing HOME finally appears by title.** 8 safe-routing abstracts pulled → **3 promoted to
  full-text** (pending download): (1) **mean-excess network-equilibrium, class-specific safe routing**
  = structural ancestor of per-type routing ★; (2) **Navigating to Safety** (Texas 29k seg; 8% time →
  +23% crash; weather-varying) = home + motivation stat; (3) **food-delivery riders SP** = demand-side
  niche brick (a vehicle class wants type-specific safe routes). 3 abstract-only keepers (bi-attribute
  NYC; NL Sustainable-Safety; hazmat-CVaR borrow); 2 hazmat skip-logged.
- **Gap-test synthesis (strongest yet):** 8 safe-routing papers ~2008–2024, **none route by vehicle
  type**; the mean-excess paper even hands over the mechanism (class-specific route sets + crash-risk
  tail) to fill the gap, re-keyed on vehicle type.
- Notable: keyword 1/3 done; next `risk-based navigation`. 3 PDFs to fetch.

## [2026-06-18] reading | T-ITS Phase-3 sweep (Tier 1, Journal 1) — all 4 keywords
- Record: [[T-ITS-abstract-refs]] (`raw/papers/tier1/tier1_journal1/`).
- Keywords: `risk-aware route planning` (0) · `safest path routing` (0) · `safety-aware navigation`
  (0, AV-control/perception/maritime noise) · `vehicle type crash risk` (1 weak).
- **Result: 0 full-text keepers, 1 weak abstract-only keeper** — "Defining TTC Thresholds by Type of
  Lead Vehicle" (vehicle type modulates risk, but micro-TTC/non-lane-based → `niche-premise (weak)`).
  Jiang 2022 + Li 2025 re-surfaced (already in corpus).
- **Gap-test brick:** no vehicle-type *segment-risk* or *routing* paper on T-ITS under any keyword;
  confirms spatial-divergence premise must come from AAP / J. Safety Research (as predicted).
- Notable: T-ITS done. Next journal in Tier 1.

## [2026-06-18] query | Standing + gap analysis; reading-plan stress-test → keywords sharpened
- Page: [[wiki/queries/2026-06-18-where-we-stand-and-remaining-gaps]].
- **Question:** before reading more, where do we stand and will the PLAN keywords uncover the gaps?
- **Answer:** literature gaps (premise, TR-C routing gap test, eval) ARE covered — but two holes found:
  (1) the niche premise keywords only find "types differ in factors/severity," NOT the load-bearing
  **spatial-divergence** claim (different segments risky for different types); (2) segment-definition
  decision was only brushed. **And the biggest existential risk — per-type STATS19 density — is
  structurally OUTSIDE reading; only a data probe answers it.**
- **Actions:** PLAN.md — added a **spatial-divergence** keyword cluster (#1 priority: `motorcycle crash
  hotspot`, `vehicle class network screening`, `crash hotspot vehicle type spatial`, `vehicle-type crash
  spatial distribution`) + a **segmentation** cluster (`crash hotspot DBSCAN`, `road segmentation crash
  risk`, `spatial unit crash analysis`); recorded the "reading CANNOT resolve feasibility" caveat.
  positioning-memo — added **Open Decision #6** (per-type density probe + per-type exposure confound).
- Notable: **probe is parallel-tracked, not post-reading** — it covers a gap reading can't.

## [2026-06-18] reading | Deep-read all 6 carry-over PDFs → 3 per-journal records
- **Downloaded the two missing CORE papers** (Sarraf 2020 ESWA, Zhu 2025 T-ITS); all 6 carry-over
  PDFs now in `raw/papers/carry_over/`. Read all 6 in full (pdftotext extraction).
- **Records created** (per-journal, context + technical grounding): [[T-ITS-deepread]],
  [[ESWA-deepread]], [[AAP-deepread]].
- **Three findings that move the thesis:**
  1. **Jiang ≠ a router.** It outputs a risk score → heat map; routing is its own future work.
     The router is **Sarraf** (Dijkstra + MCDM). So the assembled stack = **engine (Jiang/Gao) →
     router (Sarraf)**, and the thesis conditions *both* on vehicle type. Jiang also **names our
     gap verbatim**: "risks are not dependent on … vehicle types or weather conditions."
  2. **Sarraf routes everyone the same** — WCR normalises by AADT but has **no vehicle-type term**.
     Strongest "slot is open" brick; we adopt its WCR (per type), AHP/PROMETHEE ranker, and
     Spearman/Average-Overlap/**DCG** eval suite (DCG = headline, it penalises a risky route ranked high).
  3. **Zhu reframed (honest downgrade):** "vehicle-**group**" = dynamic interaction clusters
     (trajectory/iTTC, real-time), NOT vehicle **type**; type is 1 of 8 node features. → weak niche
     premise, strong method-cousin (GNN+GNNExplainer). **Vehicle-type-heterogeneity evidence is
     still THIN** and is now the explicit reading priority.
- **Technical bridges locked:** Gao/Sarraf/STATS19 all severity-weight crashes into one segment
  scalar (Gao 1/2/3; Sarraf 30/15/5/2) → we compute it **per vehicle type**, ideally with per-type
  exposure. Gao = ZITD for ~96% zero-inflation + MPIW/PICP/AccHR@20 metrics. Wei = case-crossover
  matched-control gate; Wang = χ²-CI Bayesian-network gate (Bonferroni; BDs for sparse cells) →
  the two candidate significance gates for vehicle-type × condition cells.
- **Bookkeeping:** positioning-memo evidence map updated (all 6 → deep-read; Zhu premise reframed;
  engine-vs-router structural note added); index + this log updated.
- Notable: **Next — start the Tier 1 reading pass proper** (T-ITS / TR-Part-C / AAP / ESWA), top
  priority = motorcycle/HGV/vehicle-type *segment-risk* papers to fill the thin niche-evidence base.

## [2026-06-17] ⏸ CHECKPOINT — end of day, read this first next session
- **State: Phase 3 is fully scaffolded and ready to start reading.** Nothing committed to git
  (by choice — all saved to disk on the work machine).
- **Files in place:** [[PHASE3/PLAN]], [[PHASE3/positioning-memo]] (living), [[PHASE3/index]],
  this log, and `raw/papers/carry_over.md` + `raw/papers/carry_over/` (4 full-text PDFs:
  Jiang2022, Gao2024, Wei2024, Wang2025).
- **Carried-over papers — status:** the 4 deep-read papers that had PDFs are copied in full;
  all other surviving papers were abstract-only in Phase 2 (no PDF ever existed) and live as
  text in `carry_over.md`. **Two abstract-only papers are now CORE and must be downloaded:
  Sarraf & McGuire 2020 (ESWA — routing layer + eval metrics) and Zhu et al. 2025 (T-ITS —
  vehicle-type niche premise).**
- **Housekeeping done:** CLAUDE.md now points the active phase at PHASE3 (Phases 1 & 2 = read-only
  archives); PHASE2/positioning-memo.md got a SUPERSEDED banner; project memory + MEMORY.md index
  rewritten to the Phase 3 state.
- **Resume plan:** (1) re-read PLAN + positioning-memo; (2) read the 4 carried PDFs (Jiang = home,
  Gao = engine first); (3) download Sarraf 2020 + Zhu 2025; (4) begin Tier 1 reading pass
  (T-ITS, TR-Part-C, AAP, ESWA) on routing + vehicle-type keywords, recording lightweight
  per-journal `*-abstract-refs.md` files.
- **Direction recap (one line):** risk-aware route planning (home), novelty = vehicle-type-
  conditioned segment crash risk, STATS19 engine (Gao lineage), NO LLM, output = ranked routes /
  vehicle-type risk map; supervisor's bar = complexity of the system over novelty.
