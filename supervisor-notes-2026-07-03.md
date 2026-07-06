# Talking points — supervisor 2026-07-04

One-liner: **niche is real & stronger than expected. GAT hides it. Fixed it partway. Simple stats
still wins outright. Need his input on which engine ships.**

---

### 1. Statistical method
- What it does: for a segment with no crash history, look at nearby segments on the road network
  and borrow from them instead
- Not a cited method yet — closest real match is "Network KDE," haven't confirmed this yet
- How different types actually are (ground truth): types crash in almost completely different
  places from each other
- This method's score: best of anything tried tonight, but not yet backed by a citation

### 2. GAT — why, what's different, the best version
- Why GAT: road network is a graph, so let each segment learn from its neighbors; wanted one
  model to handle all 5 vehicle types by giving it a "which type am I answering for" signal
- What's different from XGBoost: GAT shares one network across all 5 types; XGBoost trains 5
  completely separate models, one per type
- Best version uses the exact same input data as the original — nothing new was added
- Best version changed two things: (1) instead of predicting the raw number of crashes, predict
  what share of the risk belongs to each type; (2) give each type its own separate final answer
  step instead of forcing all 5 through one shared step
- Result: went from 0.894 down to 0.377 (lower = types look more different from each other = better)
- Checked it in actual routing: routes started differing by type more (went from all 5 types
  taking the identical route, to about 2 of 5 taking a different one) — but each type's *worst*
  segments still overlapped a lot, unchanged

### 3. Other things tried (brief)
- GAT: original (0.894) · share-only, same shared final step (0.563) · separate final step only,
  same question (0.816) · fully separate networks, same question (0.785) · + clean road-geometry
  features (0.822)
- XGBoost: used specifically to test which extra features were worth adding
  - clean road-geometry features → no help (0.681 vs 0.650)
  - "did any vehicle crash here before" (same value for every type) → made it worse (0.79)
  - same info, but "did THIS type crash here before" (different value per type) → best
    non-GAT result (0.552)
  - takeaway: no new feature helped; reusing existing info, but kept separate per type, did
- Standard textbook statistical method (Empirical Bayes shrinkage) → 0.412, worse than the ad
  hoc statistical method above

### 4. Why ML kept failing
- The original ask was "guess how many crashes happen at this segment." For every vehicle type,
  the easiest answer to that question is the same: guess how busy/dangerous the place is in
  general. A junction bad for cars is usually bad for cyclists and HGVs too, just by different
  amounts — so every type's "easiest good answer" ends up looking alike.
- Tried giving each type its own final answer step, then went further and used 5 fully separate
  networks with nothing shared at all. Barely helped (0.894 → 0.816 → 0.785). Splitting the
  networks apart didn't change the *question* — even 5 completely independent networks, each
  asked "how many crashes happen here," will each land on "guess the general danger level"
  separately, because that's still the easiest good answer to that specific question.
- What actually worked was changing the question, not who answers it: predict what *share* of
  the risk belongs to each type instead of the raw count. This removes "how dangerous overall"
  from the question entirely — now there's an actual reason to learn what makes types different.
  Big improvement alone (0.894 → 0.563).
- Not enough alone, though — all 5 answers were still funnelled through one shared final step,
  which blurred them back together somewhat even if real differences existed underneath.
- Best version does both at once: ask the better question AND let each type give its own
  separate final answer. Together this worked much better than either alone — one gives the
  model a reason to find real differences, the other lets it actually show them without
  blurring back together.
- Same story explains the other 2 failures: a "did anyone crash here" feature, and the standard
  statistical method (Empirical Bayes) — both lean on "how dangerous is this place generally,"
  which pulls every type toward the same answer, even when the models are already fully
  separate (XGBoost has no shared network at all, and it still happened).
- Best GAT and worst GAT used the exact same input data — nothing new was added. The fix was
  entirely about what question was asked and how the answer came out, not richer data.

### 5. Where this leaves it
- Killed: risk depending on weather/light conditions — tested the premise directly, the effect
  is too small to matter (not an ML failure, the pattern itself barely exists)
- Open decision: statistical method (best score, not cited yet) vs GAT (worse score, fully
  defensible right now)
- **Accuracy vs. explainability — three methods, not two:**
  - ad hoc smoothing (most accurate) has no variables at all — just borrows nearby history —
    so it can never say *why* a segment is risky, only that it is
  - Empirical Bayes (the textbook statistical method) *does* use variables (traffic, length) and
    could offer some explanation through them — but it was the *least* accurate of everything tried
  - GAT sits in between on accuracy, and is *structurally* the kind of model that could be
    interrogated for which variables matter — but that explanation was never actually built or
    tested tonight, so it can't be claimed as a result, only as a reason to keep ML in the system
  - so it's not "stats = accurate, ML = explainable" — the most accurate method is also the
    least informative one, and explainability for ML is a real but *untested* next step
- The core idea — vehicle types are genuinely at risk in different places — is not in question,
  it's better evidenced than when the thesis was scoped
- Ask him: which engine to use, and whether the GAT investigation itself (found the failure,
  explained it, fixed most of it, tested it against the textbook method and beat it) counts as
  a real contribution on its own, regardless of which engine ships

---
Full detail if needed: `PHASE3/wiki/progress/2026-07-03.md`
