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

The next [declared round, EXP-003](../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/hypothesis.md),
has not yet run. Its completed
[source preflight](../../problems/number-theory/riemann-hypothesis/context/2026-09-12-pressure-frame-prior-art.md)
identifies pressure frames, nonuniform pair weights, mixed certificates and global
capacitated matching as prior art. The prospective result is a stronger short-interval
consequence, with the general RH and global records outside its claim.

Stage A first checks a pair-disjoint alternating-triple cover inside an odd frame,
reusing the already certified EXP-002 energy floor. Its decisive invariants are pair
incidence, telescoping span, the spectral cap, shifted-partition boundary counts and
the order of analytic limits. After that audit, Stage B permits one bounded
two-variable pressure exploration and at most three rational certificate candidates
under the hypothesis's time, node, checkpoint and independent-replay limits. Stage
outcomes are recorded separately; a failed search cannot erase a validated symbolic
result or justify an undeclared larger campaign.

Commit the declaration and source preflight before implementation or computation.
Any new bound enters derived documentation only after a complete verdict and
independent adversarial review. Preserve the first release's frozen manuscript,
publication bytes and replay evidence throughout the new round.
