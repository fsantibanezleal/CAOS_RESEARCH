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

## Completed first release and current bounded round

The first source review, EXP-001, EXP-002, wiki and version 0.01 preprint are complete.
Research PR #263 and release PR #264 merged; main `08660dc` is tagged `v0.64.000`.
Pages run 34706614866 succeeded. The
[live receipt](release-0.64.000/live-verification.json) closes the first delivery round:
13 public files match the reviewed bytes, and all eight desktop/phone EN/ES light/dark
scenarios pass with 224 screenshots. The separate predeployment matrix and visual reviews
remain in [the release evidence](release-0.64.000/README.md).

[EXP-003](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/verdict.md) is now confirmed in both stages. Its odd-frame
assembly strengthens the entire positive curve; a 16,797-node pressure certificate
gives the stronger explicit theta=3/4 result. The declared source/compute sequence,
budgets, checkpoint semantics and unattempted lower-ranked candidates are persisted.

The latest user instruction expands the objective beyond constant optimization.
Three bounded primary-source reviews examine parity/multiplicity transfer, full
negative-spectrum information, and alternative RH reformulations. New computational
families require a fresh source-complete declaration; an already known theorem or
an unsupported infinite-limit step rejects a proposed novelty claim.

Those dossiers are now persisted. EXP-004 was declared in e03413b before computation,
and is confirmed in fbc4f9f with exact parity/multiplicity certificates, a complete
qualitative below-threshold theorem, and independent proof adjudication. The classical
density constant and new decimal exponent remain unquantified. Retain the other
source-reviewed routes as separate hypotheses with their missing arithmetic or
infinite-limit inputs explicit.

The release owner preserved EXP-003 while the reviews ran. The revised manuscript is
now frozen and published as v0.02 at DOI 10.5281/zenodo.22728744 after a two-pass,
21-page rendered review. Finish the bilingual replay, scoped promotion, serialized
release, all-page/rendered checks and exact live verification in the same delivery
round. The v0.01 publication and archive remain unchanged.
