# Riemann hypothesis: zero-proportion research program

Opened for source-led investigation on 2026-09-12. Scope: `number-theory/riemann-hypothesis`.
Tracking issue: <https://github.com/fsantibanezleal/CAOS_RESEARCH/issues/262>.

## Objective and boundaries

Review the 2026 simple-critical-zero breakthrough, its simplifications, formal certificates,
and subsequent extensions. Pursue independently checkable improvements and simplifications.
The Riemann hypothesis itself is not claimed solved. Finite zero verification, numerical
optimization, a repository headline, and a certified finite inequality are different forms
of evidence and cannot be substituted for a proof of an asymptotic zero-proportion theorem.

## Source baseline

The primary baseline consists of the original and revised Anthropic PDFs, Alpoge-Furman
arXiv:2608.13637, Lamzouri arXiv:2609.02882v1/v2, Wang arXiv:2609.07918v1, the BGSTB
pair-correlation papers, AxiomMath/ZetaZerosV2, and anthropics/formal-math. The later
ainta/trmdy stability candidates are audited separately from the established source theorem.
Version-pinned downloads, source licenses, hashes, and reproducibility instructions belong
in `problems/number-theory/riemann-hypothesis/context/`.

## Strategy and active lenses

1. Exclusion spine: audit each analytic dependency and exclude unjustified strengthening.
2. Anatomy: identify equality and stability mechanisms in the Hilbert/rank-trace argument.
3. Reformulation: transfer finite stability inequalities to the short-interval setting.
4. Invariant first: use the cosine kernel's zero-addition obstruction before numerical search.
5. Adversarial audit: independently derive constants, counting factors, and support conditions.

Every experiment is declared and committed before running. Positive results require exact
proof or certified arithmetic and an independent refutation attempt. Failed and preempted
routes remain in the record. Candidate directions are ranked by novelty, proof completeness,
certification feasibility, and compute cost, not by the numerical size of a headline.

## Execution and release

Finish the source inventory; reproduce baseline formulas; test the short-interval stability
extension and its precise counting constants; transcribe verdicts to the wiki and a manuscript
if the novelty gate is met. Publish coherent validated manuscripts to Zenodo under methodology
09. Promote research rounds through a scoped PR to develop. The final serialized release owns
versioning, data bake, frontend replay, rendered checks, and the develop-to-main deployment.
The initial finite calculations are CPU tasks. GPU use requires a demonstrated search workload
and a separate exact/certified validation path.
