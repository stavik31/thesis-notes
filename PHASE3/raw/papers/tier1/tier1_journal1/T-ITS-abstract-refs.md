# T-ITS — Phase 3 Reading-Pass Record (Tier 1, Journal 1)

**Pass:** 2026-06-18, risk-aware-routing + vehicle-type-niche direction. Lightweight per-journal
record (titles → abstracts → full-text), mirroring the Phase 2 style. Carry-over papers already
deep-read live separately in [[T-ITS-deepread]] (Jiang 2022, Zhu 2025) — this file is the *new*
sweep of the four T-ITS keywords.

**Keywords swept (all 4 done):** `risk-aware route planning` · `safest path routing` ·
`safety-aware navigation` · `vehicle type crash risk`.

**Pass result: 0 full-text keepers, 1 weak abstract-only keeper.** The dedicated niche keyword
surfaced essentially one vehicle-type-conditioned paper, and it is micro/surrogate — **no
vehicle-type *segment-risk* or *routing* work exists on T-ITS.** Strong brick for the gap test.

---

## Keeper (abstract-only, weak)

- **Defining Time-to-Collision Thresholds by the Type of Lead Vehicle in Non-Lane-Based Traffic
  Environments** — *(vehicle type crash risk; abstract read 2026-06-18)*
  *Copula-based (bivariate Frank) framework modelling the dependence between TTC and centerline
  separation in staggered-following events, by **lead-vehicle type**, on video trajectory data
  from urban non-lane-based traffic. Finds TTC risk thresholds decrease with lead-vehicle size →
  "risk level varies by the type of front vehicle ahead." **Tag: `niche-premise (weak)` /
  `related-work`.** Independent brick for the GENERAL premise (vehicle type modulates risk), but
  the weak form: surrogate TTC (not historical segment crash), micro not spatial, lead-vehicle
  type in a car-following pair (not ego/own-vehicle-class segment risk), non-lane-based context.
  Good for one related-work sentence; copula/TTC method not borrowable; NOT full-text-worthy. Does
  NOT supply the load-bearing spatial-divergence claim.*

## Already in corpus (surfaced again, not new)
- **Safe Route Mapping of Roadways…** = Jiang 2022 → [[T-ITS-deepread]] (home/engine, deep-read).
- **Leveraging Textual Description & Structured Data…Multimodal** = Li 2025 (Phase 2; LLM/multimodal
  — out of scope since the LLM was cut).

## Skipped at title level (representative, not exhaustive)
- *Driver behaviour / profiling lineage:* Data-Driven Driving Safety Risk (Arbabzadeh-Jafari);
  Forecasting Habitual Driving Behaviors; Detecting Aggressiveness from Driving Signals; Driving
  Behavior Guidelines. — per-*driver*, not per-vehicle-type or routing.
- *AV control / motion planning / perception:* NavDrive; Occlusion-Aware Trajectory/MPC Risk Fields;
  Perceptual-Uncertainty Motion Planning; Interaction-Aware Trajectory Opt; DMP; 3D Reconstruction;
  Affect Recognition; "Do AVs Reduce Crash Risk"; AV overtaking behaviour.
- *Lane-change / merge / intersection behaviour (vehicle-blind):* Crash Risk from Lane Changing;
  Vehicle Merging in Work Zones; Social Gap Game Theory; Cycle-Level Crash Risk at Intersections.
- *Off-domain / infra:* maritime path-planning ×2; air-traffic flow management; EV-charging
  navigation; V2X security credential; V2V warning impact; in-vehicle assistance; accident
  detection from text (TIME-VAD); acoustic pedestrian hazard; UAV attacks; session recommendation;
  context-aware navigation *protocol* (V2X comms, not crash-risk routing).

## Gap-test bricks from this journal
- No risk-aware **routing** paper appeared under any of the four keywords (incl. the two routing
  keywords) — T-ITS's "navigation" skews to AV control/perception, not route-planning-on-crash-risk.
- No **vehicle-type segment-risk** or **vehicle-type routing** paper. The single vehicle-type-
  conditioned hit is micro-TTC. → spatial-divergence premise must come from AAP / J. Safety Research,
  as predicted ([[2026-06-18-where-we-stand-and-remaining-gaps]]).

## Links
- [[T-ITS-deepread]] — carry-over deep reads (Jiang, Zhu)
- [[PLAN]] — keyword clusters · [[positioning-memo]] — evidence map
- [[2026-06-18-where-we-stand-and-remaining-gaps]] — the gap analysis this sweep tests
