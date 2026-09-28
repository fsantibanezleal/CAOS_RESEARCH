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

## Rank-six local transfer and spectral correction

EXP-007 proves the finite spectral-defect refinement
`(Q-S-D(G))(N-O) >= 2(N-S)^2` and certifies a strict, very small improvement
wherever the scalar Hilbert-parity curve is positive. EXP-008 proves the local
Selberg transfer for every fixed finite rank and applies Pearce-Crump's stated
rank-six constant interval. Its exact certificate moves the positivity onset
to `(0.5458837,0.5458838)` and gives a positive rank-six lower term at
`theta=0.545884`, where rank three remains negative. The coefficient matrix is
not printed by the source, so independent reconstruction remains open.

Manuscript v0.07 is published at DOI 10.5281/zenodo.22860012 and matches a
fresh public download byte for byte. Research PR #325 merged replay v7, both
new experiment records, and the bilingual workbench into `develop` after its
full Linux gate passed. At candidate freeze, rendered QA, promotion, main CI,
Pages deployment, and exact live verification remained as release gates.

Release and promotion PRs #330 and #331 are merged. Tag `v0.72.000` points to
exact main commit `45c34c81`. Main CI and Pages passed; eleven public files
byte-match the exact-main build, and eight live desktop/phone EN/ES light/dark
scenarios passed with 352 screenshots and no failures. Release 0.72.000 is
therefore live-verified. This deployment does not change the open status of RH
or remove the attributed-input boundary for the rank-six constant.

## Localized Levinson detector (EXP-010)

The 2026-09-26 preflight showed that the onset is governed by the slope of
the odd-support detector near `theta=1/2`, not by the Selberg constant `C_q`
(at most about `1e-5` of onset) or by the product inequality, which is sharp.
EXP-010 was declared at `2f7aaa6b` before implementation. It localizes
Levinson's method with Conrey's general `Q` to `(T,T+T^theta]` for
`nu<theta-1/2` by rerunning Young's short proof with a window weight, proves
that the localized method counts distinct sign changes of `Z`, and certifies
degree-201 detectors with `kappa>0.7170 nu`, five times the Selberg slope.
The EXP-006 product then gives a positive simple-critical proportion for every
fixed `theta` in `[0.534,1)`, with about 1000 times the EXP-008 density at
`theta=0.5459`.

The new manuscript `short-interval-levinson` is built from the verdict and
published at DOI 10.5281/zenodo.22984155. The public workbench (replay
v9) and a serialized release are separate later gates.

The next routes are set by the 2026-09-27 strategic review below.

## Strategic review after EXP-010 (2026-09-27)

A methodology 13 review followed a literature and cross-field sweep
([dossier](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-literature-and-representation-sweep.md)).
Full-text arXiv, Zenodo and Springer access was blocked in that session, so
its snippet-level statements are inputs to verify, not premises.

Findings that change the plan:

1. No external 2026 result improves the EXP-010 onset `0.534` or the EXP-009
   constant. Wang's printed global gain is `delta_0=6.66624e-8`; EXP-009 sits
   about `2.9e-8` above `C_0+delta_0`. Wang also states that his `Delta_K`
   refinement transfers to short intervals.
2. The Steuding range behind RH-027 was overstated. His short-window error
   `O(T^(1/3+eps)M^(4/3))` is proved for degree-one `Q`, fixed shifts,
   `nu<3/8`, orders at most two. `(3theta-1)/4` is inferred. The general-`Q`,
   uniform-shift version is a new theorem.
3. Kernel choice is nearly exhausted: the Montgomery-Taylor threshold is the
   recorded `0.55019`, and a Cohn-Elkies relaxation reaches only about
   `0.5487` in floating point. EXP-010 is already below both. Onset gains come
   from second-order inequalities (EXP-006 product, `Delta_K`, multi-point
   constraints) or from longer admissible mollifiers.
4. Of the cross-field representations reviewed, only finite compressions of
   Weil's Hermitian form have a proportion channel. Families and function
   fields support reading `theta=1/2` as an artifact of the approximate
   functional equation. Spectral triples, heat flow, Jensen polynomials,
   horocycles, Lee-Yang stability and multiplicative chaos remain a watch
   list.

Retained focus: `RH-F4`, the short-interval simple-critical onset and density
(see [research-governance.json](research-governance.json)). Ordered routes:

| Order | Item | Status 2026-09-27 |
|---|---|---|
| done | RH-030 source gate | Completed; dossier section 6 |
| done | RH-031 value of information | Tang-type onset 0.5257; Steuding-type positive for every `theta>1/2` |
| done | RH-033 `Delta_K` | Closed: cannot move any onset |
| done | RH-028 second piece | Closed: gain below `1e-9` at short length |
| done | RH-032 Cohn-Elkies | Closed: no unconditional sign beyond the support |
| done | RH-035 below 1/2 | Closed: needs an explicit odd density of 8% to 36% |
| done | RH-036 Zhu replay | Closed: `2.047e-17` inside Zhu's window, no proportion channel |
| done | RH-034 / EXP-011 | Confirmed barrier: (L) false for the Montgomery-Taylor window; `beta<=2.3589`; linear refinements capped near 0.5324 |
| in flight | RH-027 / EXP-012 | Declared: `nu<(2/3)(2theta-1)` via Tang-Khan reciprocity, onset about 0.5307 (scratch) |
| then | RH-026 | Serialized release with replay v9 |

Details: [route preflights](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-route-preflights.md).
EXP-011 removed (L); the remaining lever is the mollifier range (EXP-012).

Every route reproduces a known value before any new number is trusted. Each
new experiment still needs its own declaration and methodology 12 preflight.
RH-021 stays an integrity task. RH-026 waits for the RH-037 records hygiene.

RH-030 was completed later the same day after network access was restored:
the Steuding correction is confirmed and sharpened (the theorem also fixes
`P(x)=x`), Tang's short-window reciprocity gives a cheaper intermediate
target `nu<2theta-1` for RH-027, the RH-028 benchmark was already met by
the 2026-09-26 preflight, and Lamzouri's Proposition 2.1 weakens the
Cohn-Elkies route.

