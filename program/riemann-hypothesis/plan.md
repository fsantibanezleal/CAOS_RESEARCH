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
The September 19 extension also includes Pearce-Crump arXiv:2609.15329v1 and
the open AxiomMath unconditional-formalization pull request at its pinned head.
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
21-page rendered review. The bilingual replay, scoped promotion, serialized
release, rendered checks, and exact live verification were completed in that
delivery round. The v0.01 publication and archive remain unchanged.

## Confirmed explicit local transfer

EXP-005 was declared in `6fd59fec` before implementation and canonical
execution. It is confirmed in `5132beed`. The source's arbitrary-subinterval
rational-frequency estimate gives an off-diagonal exponent
$1/2+2u-\theta$ and therefore an explicit odd-critical density throughout
$\theta>1/2$. The EXP-004 parity identity converts it into a simple-critical
positivity threshold in $(0.5459,0.546)$. The exact certificate, retained
serialization failures, analytic audit and proof-review binding are committed.
Manuscript v0.05 is published at DOI 10.5281/zenodo.22851518 after a clean
three-pass build, full 24-page render review and exact public-byte verification.
Release 0.70.000 completed the public replay, scoped promotion, and live
verification; none changes the open status of RH.

## Confirmed Hilbert-parity compression

EXP-006 was declared at `b1febcf8` before implementation. The first run passed
the declared weaker product. A subsequent consistency audit recovered the
simple-real contribution in the attributed arbitrary-parameter Hilbert bound;
the amended runner and tests were committed before a new canonical run. The
confirmed theorem is

$$
(Q-S)(N-O)\ge2(N-S)^2.
$$

The short-interval transfer has a unique positivity root in
$(0.545884,0.545885)$ and proves a simple-critical lower proportion above
$0.0000168381638551244569880374399$ at theta=0.5459. The proof, exact
certificate, scalar barrier witness, independent interval replay, audit and
proof-review bindings are committed. Manuscript v0.06 is published at DOI 10.5281/zenodo.22852479 after a
clean 26-page render review and exact public-byte verification. Replay v5 is
baked and tested. Research PR #316, release PR #317, and promotion PR #318 are
merged. Release 0.71.000 is tagged from exact main commit `8302be35`; main CI,
Pages, ten live byte comparisons, and eight live browser scenarios passed. This
delivery does not change the open status of RH.
