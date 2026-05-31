# Wiki Log

Append-only chronological record. One entry per operation.
Parse with: `grep "^## \[" log.md | tail -10`

---

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
