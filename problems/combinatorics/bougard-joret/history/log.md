# Bougard-Joret append-only history

## 2026-09-04: portfolio review and adjacent-strip theorem

Reviewed all 20 portfolio rows, preserving current active worktrees. The new source pass is [the portfolio audit](../context/report-source.md). Selected the adjacent diagonal above Das-Gupta's counterexample boundary.

Committed the falsifiable [EXP-001 hypothesis](../experiments/EXP-001-tree-strip/hypothesis.md) before any run (0c14bf1). The [verdict](../experiments/EXP-001-tree-strip/verdict.md) confirms an elementary uniform proof and complete extremal characterization. The adversarial audit caught the two-surviving-tree-vertices gap in an informal argument; the repaired case was already in the committed hypothesis. Exact integer controls passed with positive, star, disconnected-residual and deleted-edge controls.

Exploration: missing-neighbor fibers translate degree equality into a residual-graph problem. The tree case is complete; the wider shell is a new direction, not a claimed theorem. Manuscript v0.01 and wiki were transcribed from the proof and certificate. The original disproof remains credited to Das-Gupta.

## 2026-09-04: public preprint and integration

Published v0.01 at DOI `10.5281/zenodo.22315252`, concept DOI `10.5281/zenodo.22315251`. The fresh unauthenticated download matches the 319,548-byte rendered PDF, SHA-256 `a804014fddf8d47ae0dc3988c7b1e6a0d3619daf0a423b398724321095bbb323`. Full verification is in `manuscripts/bougard-joret/tree-strip/publication-verification.json`. All five pages visually inspected; 61 tests and structural/content guards pass. Research PR #248 carries the scoped round into develop. No global release is included.

## 2026-09-04: merged round

PR #248 merged to develop at `2507925` after current-head CI passed. The private mirror merged through PR #608 at `f09d60ee`. Publication and research-round integration are complete. The final handoff records these actual merge results; no main release, version bump or cross-problem bake is claimed.

## 2026-09-05: full first interior shell

Refreshed all 13 unstarted and seven active problems in the [dated portfolio review](../context/2026-09-05-portfolio-refresh.md). Selected the complete first interior shell for its symbolic construction opportunity. The [EXP-002 preflight](../experiments/EXP-002-next-shell/hypothesis.md) was committed and pushed at `d15f240` before computation.

The [verdict](../experiments/EXP-002-next-shell/verdict.md) confirms the all-parameter formula $f(a+k+1,a,k)=\lceil k(a+k+1)/2\rceil$, $k\ge3$, $2\le a\le k+1$, and all alpha-two extremizers as complements of cycle unions with component lengths at least five. The degree-sum invariant led to residual Harary graphs, complement matchings and injective misses. The complete proof and final manuscript transcription passed independent reasoning audits. Seventy-five exact constructions and a separate NetworkX implementation pass; the order-six census agrees with EXP-001. A smoke wrapper status-string mismatch was corrected before the full run, with no mathematical change.

Manuscript v0.02 expands the original paper to ten pages. All pages were rendered and inspected; the final LaTeX log has no warnings. All 62 repository tests, lint, structure and content checks pass. Publication and scoped integration are the remaining delivery steps at this entry. The original general conjecture's disproof remains credited to Das-Gupta; the revised general regimes are not solved by this shell theorem. Earlier experimental records and unrelated sessions remain preserved.
