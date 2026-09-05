# Bougard-Joret append-only history

## 2026-09-04: portfolio review and adjacent-strip theorem

Reviewed all 20 portfolio rows, preserving current active worktrees. The new source pass is [the portfolio audit](../context/report-source.md). Selected the adjacent diagonal above Das-Gupta's counterexample boundary.

Committed the falsifiable [EXP-001 hypothesis](../experiments/EXP-001-tree-strip/hypothesis.md) before any run (0c14bf1). The [verdict](../experiments/EXP-001-tree-strip/verdict.md) confirms an elementary uniform proof and complete extremal characterization. The adversarial audit caught the two-surviving-tree-vertices gap in an informal argument; the repaired case was already in the committed hypothesis. Exact integer controls passed with positive, star, disconnected-residual and deleted-edge controls.

Exploration: missing-neighbor fibers translate degree equality into a residual-graph problem. The tree case is complete; the wider shell is a new direction, not a claimed theorem. Manuscript v0.01 and wiki were transcribed from the proof and certificate. The original disproof remains credited to Das-Gupta.

## 2026-09-04: public preprint and integration

Published v0.01 at DOI `10.5281/zenodo.22315252`, concept DOI `10.5281/zenodo.22315251`. The fresh unauthenticated download matches the 319,548-byte rendered PDF, SHA-256 `a804014fddf8d47ae0dc3988c7b1e6a0d3619daf0a423b398724321095bbb323`. Full verification is in `manuscripts/bougard-joret/tree-strip/publication-verification.json`. All five pages visually inspected; 61 tests and structural/content guards pass. Research PR #248 carries the scoped round into develop. No global release is included.

## 2026-09-04: merged round

PR #248 merged to develop at `2507925` after current-head CI passed. The private mirror merged through PR #608 at `f09d60ee`. Publication and research-round integration are complete. The final handoff records these actual merge results; no main release, version bump or cross-problem bake is claimed.
