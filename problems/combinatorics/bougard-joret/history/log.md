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

## 2026-09-05: publication and combined baseline

Published v0.02 at DOI `10.5281/zenodo.22341644`, same concept DOI `10.5281/zenodo.22315251`. All 343,535 public PDF bytes match, SHA-256 `faed3c5a760390a89bc77945e99837c85a55b09f6923570dcde50f289439d4b7`; unauthenticated metadata confirms concept-latest. The publish API returned legacy metadata rather than the expected native DOI shape; publication succeeded, and its existing public record was read to reconcile the receipt without repeating the publish action or creating another version.

Theorem/manuscript commit `91189c4` is pushed. Research PR #251 targets develop. Concurrent Huneke-Wiegand integration was incorporated at `ce7f68d`; the combined suite passes all 100 tests. Certificate serialization is explicitly LF, and recorded source/certificate bytes match staged Git blobs across the Windows/Linux boundary. The independent audit was rerun after that serialization repair and passes. Scoped PR integration remains at this entry; no global main promotion is included.

## 2026-09-05: merged round

Research PR #251 passed current-head CI on `be25aa4` and merged to develop at `8055fec`. Private mirror PR #611 merged at `a6d642fd`. The full-shell result, portfolio refresh, manuscript and verified public publication are complete. Final handoff documents these observed merges. No mathematical process remains, and no global main release was performed by this round.

## 2026-09-05: EXP-003 uniform next matching level

The repeated portfolio request reviewed all 13 unstarted and seven active rows, with six active checks explicitly carried forward from the same-day ledger and a deep new triangle-free source investigation. [The new dossier](../context/2026-09-05-next-matching-review.md) records source versions, alternative Hoa/Boij gates and the corrected September 2 Lamzouri submission date. EXP-003 preflight commit f3fdda6 preceded computation.

[EXP-003](../experiments/EXP-003-triangle-free-next-matching/verdict.md) proves T(d,d+1)=d squared plus d plus two for all d>=7. BET's construction is prior work; the new uniform upper bound resolves its 184-versus-185 benchmark at (13,14). The proof combines shortest-odd-cycle deficit, five-type equality exclusion and Tutte-Berge, with a separately checked AEY reduction. Internal mathematical and implementation audits pass; 48 exact graphs and 287,564 primary equality controls agree, with 48 independent full-connectivity checks and all 101 repository tests passing.

The failed direct-complement shortcut is retained: the known maximizer has complement connectivity d+1. Only the one-edge Bougard bracket is proved, with unbounded strict-interior discrepancy. A new coherent next-matching preprint is being prepared under its own concept DOI; the first-shell v0.02 remains unchanged. Publication and integration receipts follow after verification. Global main release remains separately serialized.
