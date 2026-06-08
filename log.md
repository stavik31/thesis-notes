# Wiki Log

Append-only chronological record. One entry per operation.
Parse with: `grep "^## \[" log.md | tail -10`

---

## [2026-06-08] ⏸ RESUME POINT — read this first
- **Where we are:** Direction worked out in discussion and written up for the supervisor in
  [[progress/NEW_FIX_PROF]] (**NOT FINAL** — a discussion draft to bring to the prof). The
  delivery model evolved from "pre-trip briefing" to **driver-focused, offline-precompute +
  live lookup**: heavy work (segmentation → significance test → profiling → per-condition LLM
  lines) is offline; the live system reads current conditions and plays the matching
  pre-written line (no live LLM, no latency, voice/terse/rare delivery).
- **Key reframes locked in discussion (not yet in the formal wiki pages):** (1) only speak
  when the risk is *invisible* from the road; (2) warn about *patterns*, not *events*;
  (3) silence where there's no significant cluster is correct, not a failure; (4) the
  500-crashes-per-route problem is solved by a funnel — crashes are offline training data
  that collapse to ~1–2 segment warnings, never processed live.
- **Anchor claim:** existing nav reports *that* a crash happened; this explains the
  *non-obvious, condition-specific pattern* and what it implies.
- **What's captured:** [[progress/NEW_FIX_PROF]] (new direction + architecture + training/RAG
  depth + eval + open decisions), [[progress/prof-feedback]] (the feedback this answers),
  [[wiki/overview]] + [[concepts/system-architecture]] (earlier pivot rewrite — now need
  updating to match NEW_FIX_PROF), [[progress/future-plan]] (pre-agg/RAGAS/ablation, now core).
- **Next decision when resuming (still all OPEN):** (a) **segment definition** — road link /
  grid / DBSCAN — gates everything; (b) **significance test + threshold** vs which baseline;
  (c) **training objective** — keep severity adapter as domain adaptation + add RAFT/DPO, or
  retrain on cause-summarisation (decide after a grounding test); (d) **why-LLM-vs-template**
  defence; (e) delivery form sanity check (voice vs roadside sign).
- **After prof meeting:** fold whatever he agrees to into [[concepts/system-architecture]] and
  [[wiki/overview]], then start on the segment definition.

## [2026-06-08] progress | New direction + architecture proposal written for supervisor
- Page: [[progress/NEW_FIX_PROF]]
- Decisions explored (NOT committed): driver-focused in-vehicle delivery; offline-precompute +
  live-lookup (lookup table indexed by STATS19 condition categories, not a fixed recording);
  segment significance test as the new methodological core; invisible-risk + pattern-not-event
  rules as the scope filters; severity demoted to sanity-check; sign/authority directions
  considered and set aside as weaker-novelty
- Notable: resolved the "system isn't useful" spiral by bounding scope (speak only on
  significant + non-obvious + condition-matched patterns, stay silent otherwise); 1,000-crashes-
  per-route handled by an offline funnel (segment → significance → profile → obviousness →
  condition gate → prioritise) ending in 1–2 warnings; added research depth axes (RAFT, DPO,
  three-index ablation, cross-encoder rerank, segment-level borrowing for sparse classes);
  evaluation headline = temporal holdout (train yrs 1–4, validate yr 5). Doc is explicitly a
  discussion draft for the supervisor, not a final decision.

## [2026-06-04] concept | Overview + System Architecture rewritten for the pivot
- Pages updated: [[wiki/overview]], [[concepts/system-architecture]]
- Notable: overview thesis argument restated around localized cause communication + pre-trip route briefing (general method, STATS19 as case study); removed the "competitive on implied severity prediction" framing that contradicted the feedback; system-architecture replaced the real-time per-GPS-point pipeline with offline segment cause-profiling + pre-trip briefing (+ optional heat map), with open design decisions (segment unit, significance threshold, FT objective, delivery format) flagged explicitly rather than invented; future-plan's pre-aggregation/RAGAS/ablation re-scoped to serve the new architecture

## [2026-06-04] progress | Supervisor feedback — post-presentation redirection
- Page: [[progress/prof-feedback]]
- Decisions extracted: drop real-time; pivot to offline segment cause-profiling + pre-trip route briefing (end-to-end precompute); severity demoted to sanity-check; fine-tuning objective decision deferred until after grounding test
- Pages flagged for rewrite: [[wiki/overview]] (still claims "competitive on implied severity prediction" — now contradicts feedback), [[concepts/system-architecture]] (online per-GPS-point pipeline superseded)
- Notable: feedback was about justification + usability, not implementation; the unit of analysis shifts from GPS point → road segment, the deliverable from severity warning → conditioned cause briefing, and delivery from real-time → pre-trip; most infrastructure (narratives, FAISS, MI analysis, pre-aggregation) survives and the pre-aggregation grounding fix is now the core of the system

## [2026-05-31] progress | Slides 8–10 drafted — experimental setup, future work, summary
- Page: [[progress/presentation-slides-8-10]]
- Notable: experimental slide covers fine-tuning results (3-way F1 table), RAG demo walkthrough, and suggested diagrams (SHAP bar, crash map, class distribution); future work and summary slides written slide-ready; two open questions pending (real vs generic RAG output, which diagrams to generate)

## [2026-05-31] progress | Presentation plan updated — slide content finalised with accurate paper numbers, data slide added, architecture narration notes added
- Page: [[progress/presentation-2026-06-02]]
- Notable: Related Studies slide rewritten with exact numbers (Tab-Text F1 0.4587, CrashSage F1 0.7361, RAG-Driver BDD-X SoTA); Data slide added covering STATS19 collection, structure, scale; Architecture slide confirmed as diagram-only with offline/online split; corpus vs query set terminology adopted; internal mechanics of Sentence Transformer and FAISS documented for verbal narration

## [2026-05-31] progress | Presentation plan written — 2026-06-02
- Page: [[progress/presentation-2026-06-02]]
- Notable: related work expanded to three tiers — crash classification (Tab-Text, CrashSage), AV explanation (RAG-Driver, RAG-SafeAdapt), then the gap; 9-slide structure finalised

## [2026-05-26] progress | RAG online phase complete — end-to-end pipeline working
- Page: [[progress/2026-05-26]]
- Decisions extracted: FastLanguageModel over AutoModelForCausalLM; token-length slicing for generation; coords lookup from collision.csv not metadata
- Notable: system works end-to-end but generates generic warnings — prompt engineering identified as next step before evaluation; presentation prep starts now (due 2026-06-02)

## [2026-05-25] progress | RAG offline phase complete — FAISS index built
- Page: [[progress/2026-05-25]]
- Decisions extracted: train+val only in corpus (test excluded for eval integrity); live API deferred to future work; IndexFlatL2 for simplicity; embedding cache added
- Notable: offline phase complete — embeddings.npy (701MB), faiss_index.bin (701MB), metadata.jsonl (47MB) all saved to disk; query.py (online phase) is next session

## [2026-05-21] plan | RAG Phase 2 plan written
- Page: [[progress/RAG_PLAN]]
- Notable: selected "filter then retrieve" approach (spatial radius first, semantic re-rank within subset); build order is 6 steps from encoding to generation; key watch-outs documented (context window, cold start, hallucination)

## [2026-05-21] progress | Phase 1 complete — three-way baseline comparison done, RAG phase begins
- Page: [[progress/2026-05-21]]
- Decisions extracted: fine-tuned Gemma selected as RAG backbone; XGBoost retained as tabular baseline; zero-shot dropped from Phase 2; classification F1 is proxy metric only, not thesis claim
- Notable: fine-tuned Gemma (0.408) > XGBoost (0.350) > zero-shot (0.149); zero-shot never predicts Fatal without domain adaptation; Serious is the hard class for all three systems; evaluation prompt fixed to "Reply with one word only." for consistency

## [2026-05-20] progress | LLM fine-tuning complete — test results logged, zero-shot baseline next
- Page: [[progress/2026-05-20]]
- Decisions extracted: downsample over oversample; classification F1 is proxy metric only; Gemma3 Processor quirk documented
- Notable: Macro F1 0.397 on test set (Slight 0.693, Serious 0.364, Fatal 0.134); model confirmed as gemma-3-4b-it 4B; zero-shot baseline is the immediate next step before drawing any conclusions

## [2026-05-18] progress | LLM fine-tuning plan updated — model switch, training rationale, phase context
- Page: [[progress/llm-finetune-plan]]
- Changes: model updated from LLaMA3-8B to Gemma IT (non-thinking, 7–12B, exact ID TBC); training rationale section added explaining why classification is the proxy task; three-system comparison table added to Step 9; Phase 1/2 context section added; summarisation fine-tuning deferred to RAG phase
- Notable: classification fine-tuning is Phase 1 only — same LoRA adapter plugs into RAG in Phase 2 with no retraining; summarisation fine-tuning is not a planned step, only a contingency if RAG output quality is poor

## [2026-05-14] progress | LLM fine-tuning plan written
- Page: [[progress/llm-finetune-plan]]
- Notable: 9-step plan covering Unsloth install, LLaMA3-8B-Instruct access, train/val/test split, instruction format, LoRA config, training args, weighted sampling for class imbalance, adapter saving, and evaluation against XGBoost and zero-shot baselines.

## [2026-05-14] concept | System Architecture — Location-Based Crash Risk Advisor
- Page: [[wiki/concepts/system-architecture]]
- Supersedes: [[concepts/rag-narrative-generation]] (earlier framing was generation-first; new framing is location-specific factor surfacing with advisory output)
- Notable: thesis direction clarified — the system gives drivers location-specific warnings about which crash factors are historically overrepresented at their current location, not just narrative descriptions. Architecture has two phases: offline (tabular-to-text → LoRA fine-tune → FAISS index) and online (GPS → spatial retrieval → grounded LLM warning). Correlation analysis to be rerun with Mutual Information to fix Cramér's V limitations on high-cardinality fields.

## [2026-04-30] concept | RAG-Based Crash Risk Narrative Generation
- Page: [[wiki/concepts/rag-narrative-generation]]
- Overview updated: thesis argument rewritten around generation-first framing; literature gap explicitly stated
- Notable: the thesis contribution is now clearly distinct from both prior papers — neither Tab-Text nor CrashSage produces human-readable output; this system does, grounded in retrieved historical evidence rather than baked weights

## [2026-04-30] progress | Supervisor meeting — RAG + spatial analysis as primary direction
- Page: [[wiki/progress/2026-04-30]]
- Decisions extracted: thesis direction shifted from CrashSage replication to RAG with spatial analysis; CrashSage plan demoted to baseline context
- Overview updated: thesis argument, state of project, key open questions all revised
- Notable: three interconnected directions — correlation analysis to find which variables matter, RAG for LLM inference-time retrieval, spatial/hotspot analysis as both a standalone finding and a RAG retrieval dimension

## [2026-04-28] query | Why fine-tune? Zero-shot ablation design
- Page: [[wiki/queries/why-finetune-zero-shot-ablation]]
- Replication plan updated: zero-shot baseline added to deviations table
- Notable: augmentation is inference-only (no learning, label never shown); fine-tuning is where task knowledge is injected; paper omits zero-shot baseline entirely — running it costs almost nothing and any outcome (fine-tuned wins, zero-shot matches, CatBoost beats both) is a valid thesis finding

## [2026-04-24] query | Tabular-to-text implementation guide for STATS19
- Page: [[wiki/queries/tabular-to-text-stats19-implementation]]
- Notable: Full sentence-level templates for all four narrative blocks (scene, road/conditions, vehicles, casualties); complete field skip list; label leakage warning on casualty_severity; output JSONL format defined; implementation order specified

## [2026-04-09] reference | STATS19 field reference written
- Page: [[wiki/entities/stats19-field-reference]]
- Notable: 503,475 collisions (2020–2024), severity split Fatal=7,491 / Serious=109,977 / Slight=386,007; recommended field inclusion list for narratives; join key structure documented

## [2026-04-09] progress | CrashSage replication plan written
- Page: [[wiki/progress/crashsage-replication-plan]]
- Decisions extracted: none (plan only, no decisions made yet)
- Notable: 8-step pipeline covering schema integration, tabular-to-text, augmentation, SFT (LoRA), evaluation, and gradient attribution; includes a deviation table tracking STATS19-specific adaptations vs. the original WSDOT paper

## [2026-04-08] progress | Session 1 — dataset confirmed, implementation plan set
- Page: [[wiki/progress/2026-04-08]]
- Dataset: STATS19, 5 years, ~500k–700k records, 3 relational tables, 3-class severity
- Decision: build CrashSage on STATS19 first, identify gap empirically
- Notable: thesis angle emerging around contributing factors / causation, not just severity outcome prediction

## [2026-04-08] ingest | CrashSage + Tab-Text (both papers, sequential)
- Source pages: [[wiki/sources/tab-text]], [[wiki/sources/crashsage]]
- Concept pages created: [[wiki/concepts/tabular-to-text-transformation]], [[wiki/concepts/crash-severity-inference]], [[wiki/concepts/multimodal-crash-modeling]], [[wiki/concepts/llm-domain-adaptation]], [[wiki/concepts/gradient-based-attribution]]
- Entity pages created: [[wiki/entities/llama3-8b]], [[wiki/entities/electra]], [[wiki/entities/catboost]]
- Overview updated with thesis landscape
- Notable: These two papers are best read as two competing answers to the same question — Tab-Text keeps tabular + text; CrashSage goes all-in on narrative + generative LLM. Neither tests both approaches on the same dataset.

## [2026-04-08] setup | Wiki initialized
- Schema written: CLAUDE.md
- Index created: index.md
- Log created: log.md (this file)
- Directory structure: raw/papers/, raw/notes/, raw/misc/, raw/assets/, wiki/sources/, wiki/concepts/, wiki/entities/, wiki/progress/, wiki/queries/
- Context: Senior undergraduate thesis, ~1 year scope
- Status: Ready for first ingest

## [2026-06-02] progress | Speaker notes written — slides 1–7 complete, 8–12 pending
- Page: [[progress/speaker-notes]]
- Slide changes flagged: add Waze to slide 3; sharpen hypothesis on slide 4 (remove latency claim); add explicit gap bullet to slide 5; add LLM fine-tuning box to slide 7 offline diagram; fix slide 8 cutoff; add grounding limitation label to slide 10
- Notable: slides 8–12 (live system, experiments Part 2, RAG demo, next phase, summary) to be written next session; checkpoint pushed to GitHub for remote access

## [2026-06-02] plan | Six-week future implementation plan written
- Page: [[progress/future-plan]]
- Covers: (1) pre-aggregation grounding fix — summarise_retrieved() before build_prompt(); (2) RAGAS faithfulness evaluation across Variant A vs B vs B+agg on 50 queries; (3) three-index ablation — dense semantic (current) vs feature-based FAISS vs BM25 keyword, measured by feature overlap on 100 queries
- Notable: grounding test run today confirmed prompt engineering works — Variant B achieved 3+ crash citations on every query vs 0 for bare prompt; pre-aggregation is the next step to produce the Expansionist's target output quality; this plan closes the research arc from hypothesis to measured result

## [2026-06-02] experiment | Grounding test run — three prompt variants on 5 queries
- Page: [[progress/future-plan]]
- Result: Variant A (bare) = 0/49 crash refs; Variant B (force-cite) = 16/49, consistent 3-4 refs per query; Variant C (chain-of-thought) = 12/49, inconsistent (0 refs on 3/5 queries)
- Notable: grounding is achievable via prompt engineering alone — the Contrarian's risk (task mismatch requiring retraining) did not materialise; Variant B is the reliable baseline to build on

## [2026-06-01] progress | Presentation slides updated — full evaluation plan, three-index ablation, limitations, end goal documented
- Pages updated: [[progress/presentation-slides-8-10]], [[progress/presentation-2026-06-02]]
- Notable: generic output named explicitly as known limitation (prompt not grounded in retrieved context); three-index ablation (spatial + feature-based + dense) documented as core experiment; RAGAS faithfulness + three retrieval quality proxies (feature overlap, severity distribution shift, held-out probe) documented as evaluation framework; joint embedding flagged as future work out of scope; 6-week implementation timeline locked
