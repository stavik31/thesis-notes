# AAP — Carry-Over Deep-Read Record (Tier 1, Journal 5)

**What this is.** Full-text deep reads of the three Accident Analysis & Prevention papers
carried over from Phase 2: **Gao et al. 2024** (the STATS19 risk **engine**), **Wei et al. 2024**
and **Wang & Wang 2025** (the two **significance-gate ancestors**). All three were deep-read in
Phase 2; this record adds the **technical grounding** layer (the actual estimators and how they
transfer) on top of the **context grounding** already established. AAP is the flagship road-safety
venue, so these are the methodological anchors for the engine + the conditioning-significance gate.

**Headline:** Gao is the engine on our exact dataset (UK STATS19, London) and severity-weights
crash counts the *same way* Sarraf's WCR does — but aggregates across all vehicles. Wei and Wang
supply two independent, citable ways to test whether a condition (and, by extension, a vehicle-
type × condition cell) is *significantly* over-represented on a segment versus a matched baseline.

---

## Gao, Jiang, Haworth, Zhuang, Wang, Chen, Law 2024 — Uncertainty-aware probabilistic GNN for road-level crash prediction (STZITD-GNN) ★★★ THE STATS19 ENGINE

### Context grounding
The single most important engine paper: **road-/segment-level crash-risk prediction on UK STATS19
itself** (DfT data, three London boroughs — Westminster, Lambeth, Tower Hamlets), in AAP, from UCL
SpaceTimeLab (Haworth/Law/Chen). It proves the *dataset*, the *domain*, and the *state of the art*
in one shot, and its **~96% zero-inflation** is literally our central data problem. What it does
**not** do is the contrast that defines our delta: output is a single severity-weighted risk score
per road (+ uncertainty interval) rendered as a choropleth; weather is an *input feature*, not an
output conditioning axis; **no vehicle-type stratification — risk is aggregated across all vehicles**;
no significance gate; no routing. So Gao is the realisation of Jiang's NB/EB idea in a modern
probabilistic-GNN form on our data — the baseline our per-vehicle-type engine extends.

### Technical grounding
- **Target (Definition 1):** `y_it = Σ_k C_it,k · l_k`, a severity-weighted crash count per road per
  day, with l = 1/2/3 for minor/serious/fatal. **Same severity-collapse move as Sarraf's WCR**
  (30/15/5/2) and the natural STATS19 severity encoding — the three engines agree on "one scalar per
  segment that bakes in severity." Our move: compute this **per vehicle type**.
- **Graph:** road **segment = node** (not intersection-as-node), edges = connections, adjacency A;
  enables road-specific features and node-level prediction. (Same road-as-node choice as our intended
  segmentation.)
- **Encoder:** GRU (temporal) + GAT (spatial, attention-weighted neighbours) → spatiotemporal
  embedding. **Decoder:** four parameter heads output the parameters of a **Zero-Inflated Tweedie
  (ZITD)** distribution per road per step:
  - **π** = zero-inflation (excess-zero mass) — handles the ~96% no-crash road-days end-to-end,
    cleaner than separate SMOTE/undersampling;
  - **μ** = mean, **φ** = dispersion, **ρ** = index parameter. Tweedie with ρ ∈ (1,2) is a compound
    Poisson–Gamma — exactly the "many exact zeros + continuous positive tail" shape of crash data.
    Empirically the learned **ρ → ~2**, confirming the heavy-tail choice.
  - Trained by **likelihood loss** (not regression MSE) → uncertainty-aware. 14-day multistep.
- **Zero-inflation rates (the borrowable headline):** **95.72% (Westminster), 96.71% (Lambeth),
  96.28% (Tower Hamlets)**. This is the number to cite for "STATS19 segment-days are ~96% zero," and
  it gets *worse* under multi-axis conditioning (vehicle-type × weather × time cells) — the sparsity
  argument that justifies graceful fallback as a *complexity feature*.
- **Metric suite (adopt for the engine side):** point — MAE/MAPE/RMSE; uncertainty — **MPIW** (mean
  interval width, lower=tighter) and **PICP** (interval coverage, higher=better); zero-handling —
  **ZR** (true-zero rate); and **AccHR@20** = precision among the top-20% predicted-risk roads.
  Best result: **76.59% AccHR@20 on Lambeth**, MAPE up to 49% better than the next model, MPIW
  47–55% better. AccHR@top-X% is the natural "did we rank the right segments high" metric for a
  *per-vehicle-type* risk surface.

**Borrow:** ZITD / Zero-Inflated-Tweedie for ~96% zero-inflation; road-as-node + GAT spatial
encoding; severity weighting 1/2/3; the MPIW/PICP/ZR/AccHR@20 evaluation suite (temporal holdout,
*per vehicle type*). **Extend:** stratify the whole thing by vehicle type → per-type risk surface
that feeds the Sarraf router. Tag: `engine` (the keystone baseline).

---

## Wei, Das, Wu, Li, Zhang 2024 — Lagged impacts of hourly weather and speed on segment crash risk: a space-time-stratified case-crossover design ★ SIGNIFICANCE-GATE ANCESTOR #1

### Context grounding
The strongest methodological ancestor for the **conditioning-significance gate**: it isolates the
effect of a *condition* on a *segment's* crash risk by comparing crash-hours against **matched
non-crash control-hours on the same segment**. That matched-comparison logic is exactly what we need
to answer "is this vehicle-type × condition cell genuinely over-represented, or just noise?" Data:
Texas rural interstates, 2019 (TxDOT RHiNO segments + NPMRDS speed + ASOS weather + CRIS crashes),
hourly. Validates the STATS19-adjacent condition set (precipitation / visibility / temperature /
speed-variation ≈ weather / road-surface / light) and the segment × condition × time design that
justifies our *secondary* conditioning axes.

### Technical grounding
- **Space-time-stratified case-crossover:** each crash-hour (case) is matched to 3–4 control-hours
  with **identical road ID + year + month + day-of-week + hour-of-day** (Table 1). This *strata*
  construction controls spatial + temporal confounds *by design* — the segment is its own control,
  so anything left is the condition's effect. Final set: 27,400 zero-crash + 8,022 one-crash (+175
  two, +23 three) hourly observations. **This is the cleanest blueprint for our gate:** within a
  segment, compare the condition distribution on crash-events vs matched non-events; for the niche,
  compare the *vehicle-type* mix on a segment's crashes vs the matched baseline mix.
- **Estimator:** **quasi-Poisson** regression (handles over-dispersion) with **Distributed Lag
  Model (DLM)** and **Distributed Lag Nonlinear Model (DLNM)** — basis functions over the *lag space*
  (DLM) and over both lag *and* exposure space (DLNM, via Gasparrini's cross-basis). Lets the effect
  of a condition be **distributed over preceding hours** rather than instantaneous.
- **Findings (the kind of non-obvious pattern a gate surfaces):** precipitation risk *peaks at lag
  2–4 h* (residue + resumed speed after rain stops), not at lag 0; visibility and speed-SD are
  immediate-only; low temperature has a delayed effect DLNM catches but DLM misses. DLNM slightly
  beats DLM on AIC.

**Borrow:** the **case-crossover matched-stratum design** as the significance-gate skeleton (segment
as its own control); the quasi-Poisson over-dispersion handling; the validated condition variable
set for the secondary axes. **Adapt:** for STATS19 we likely don't need the lag machinery (no hourly
exposure time-series) — the *matched-comparison* idea is the transferable core, not DLM/DLNM itself.
Tag: `significance-gate ancestor` + `secondary-axis evidence`.

---

## Wang & Wang 2025 — Causal relationship discovery via semi-data-driven Bayesian network (EKC-BN) ★ SIGNIFICANCE-GATE ANCESTOR #2

### Context grounding
The second, independent way to gate conditioning — a **Bayesian network** whose structure is built
by **chi-square conditional-independence tests** (with Bonferroni correction) constrained by expert
knowledge. Where Wei tests *one condition at a time* via matched controls, Wang tests the *whole
conditional-dependence structure* among calendar/weather/volume variables and crash, on 951 crash +
37,352 non-crash hourly cases (HuNing Highway, Suzhou, 2022, 10 camera segments). Useful both as a
gate and as a citable interpretability/causality framing (trust, transferability, heterogeneity).

### Technical grounding
- **EKC structure learning (the borrowable gate):**
  1. **Skeleton** — for each candidate arc, expert knowledge labels it True / False / **Unknown**;
     every *Unknown* arc is decided by a **chi-square conditional-independence test** `χ² = Σ(O−E)²/E`
     with **Bonferroni** correction (`p = α/m`) for multiple comparisons. This χ² CI test is the
     concrete statistical instrument we can lift directly to ask "is vehicle-type independent of
     crash-occurrence on this segment class, or significantly associated?"
  2. **Direction** — v-structure detection + acyclicity → DAG.
  3. **Parameters** — **Bayesian estimation** of CPDs (chosen over MLE *specifically because of the
     large proportion of zero values* — our exact situation).
  4. **Inference** — variable elimination across all scenario combinations → crash probability per
     scenario → rank the most dangerous.
- **Scoring (model selection):** K2 / BDeu / **BDs** / BIC. Note **BDs is "appropriate for high-
  dimensional and sparse datasets"** — i.e. the recommended score precisely when cells are sparse,
  which is the multi-axis (vehicle-type × condition) regime.
- **Findings:** only Temperature and Volume are *direct* predictors of crash (calendar variables act
  indirectly through physical conditions); medium volume is most dangerous; snowy weather highest.
  Non-obvious, interaction-driven patterns — the value proposition of a structured gate over a flat
  one-number summary.

**Borrow:** the **χ²-conditional-independence test (Bonferroni-corrected)** as the concrete
significance gate for "is this type×condition cell non-random?"; Bayesian/BDs estimation for sparse
cells; the expert-knowledge-constraint pattern to keep the structure search tractable and
interpretable. Tag: `significance-gate ancestor` + `sparsity-aware estimation`.

---

## Gap test (Phase 3)
- **Gao 2024:** STATS19 segment risk, severity-weighted, probabilistic — **aggregated over all
  vehicles, no conditioning gate, no routing.** NO (but it's the engine we extend).
- **Wei 2024 / Wang 2025:** validate that conditions can be *significantly* gated at the segment
  level — neither conditions on **vehicle type**, neither routes. The gate machinery exists; the
  vehicle-type application of it does not.

Net: AAP hands us a mature engine (Gao) and two mature significance gates (Wei, Wang), all
vehicle-blind. The thesis re-keys the engine and the gate on **vehicle type** and pipes the result
into the Sarraf router ([[ESWA-deepread]]). The still-missing piece across all three: **direct
evidence that segment risk genuinely differs by vehicle class** — not in this carry-over set;
priority to find in the AAP vehicle-type sweep.

## Links
- [[T-ITS-deepread]] — Jiang 2022 (the NB/EB engine idea Gao realises on STATS19) + Zhu 2025
- [[ESWA-deepread]] — Sarraf 2020 router; Gao's severity-weighted score plugs into its WCR slot
- [[positioning-memo]] — evidence map (Gao/Wei/Wang confirmed deep-read; engine + gate locked)
