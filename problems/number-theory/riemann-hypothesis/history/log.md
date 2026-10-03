# Riemann hypothesis history

## 2026-09-28: EXP-012 stopped at step 3

The step-3 value check of EXP-012 showed that Tang's dual weight has size
`|G(1/2+it)|=(H/sqrt T)sqrt(1/2)` on `|t|<<T/H` (mpmath, three heights), so the
dual moment is about `sqrt(h)sqrt(T)` per pair. The planned trivial bound then
gives only `nu<(2/3)(theta-1/2)` and a hybrid large-sieve sketch gives exactly
EXP-010's `theta-1/2`. The stop rule applied; the verdict is inconclusive and
the preflight target A' is withdrawn. The remaining lever is an asymptotic
evaluation of the dual family (RH-038).

## 2026-09-28: EXP-011 confirmed, EXP-012 declared

A structured test refuted the RH-034 candidate: six real triples around one
near-real conjugate pair violate `Q>=2N+3O-4S` for the Montgomery-Taylor
window. EXP-011 was declared (`9886f07`, Prediction C amended before
implementation in `136b40f`) and confirmed with Arb at 128 bits: slack
`-0.0582180002168...` for that configuration, and `(Q-2N)/O=2.35886369543...`
for a 10001-cell lattice, so no linear refinement with `beta>=2.365` holds for
this window, and with the EXP-010 detectors such refinements cannot reach
`theta=0.532`. The independent audit's first run failed a check because of an
inaccurate unsubdivided quadrature at large `|xi|` (kept); the corrected run
passed. EXP-012 was declared with a fixed proof plan for a short-window moment
with `nu<(2/3)(2theta-1)` through Tang-Khan reciprocity.

## 2026-09-27: route preflights RH-028 to RH-037

Every route in the post-review plan was worked with exploratory,
floating-point preflights (scripts in `context/2026-09-27-preflights/`).
RH-031 reproduced the EXP-010 onset and Steuding's 0.590 and 0.552, and
priced the RH-027 targets: a Tang-type range would move the onset to about
0.5257; a Steuding-type range would give positivity for every `theta>1/2`.
Closed with recorded reasons: RH-033 (Wang's `Delta_K` vanishes at the onset),
RH-028 (a Bui-Conrey-Young second piece gains below `1e-9` at short length;
the published 0.4105 implies a second-piece contribution twice ours, recorded),
RH-032 (no unconditional sign for Cohn-Elkies tails), RH-035 (below `1/2` needs
an explicit odd density of 8% to 36%), RH-036 (Zhu's window infimum replayed at
`2.047e-17`, no proportion channel). RH-037 fixed the records. Two declaration
candidates remain: RH-027 target A' (`nu<(2/3)(2theta-1)`, onset about 0.5307)
and RH-034, the finite inequality `Q>=2N+3O-4S`, which is false for
edge-concentrated windows but survives every stress test for the
Montgomery-Taylor window and would move the onset to about 0.5296. No
experiment was declared and no verdict changed.
[Route preflights](../context/2026-09-27-route-preflights.md).

## 2026-09-27: RH-030 primary-source verification

After network access was restored, the pinned archive was re-verified (68
documents) and six new sources were pinned. Full-text reading confirmed
Wang's short-interval theorem and pair formula as used, and sharpened the
Steuding correction: Theorem 2.1 fixes `P(x)=x` and `F=zeta+zeta'/L`, and the
`theta<3/8` cap comes from the constraint `G<=T^(5/6)` in the error balance.
Tang's short-window reciprocity constrains only `max{p,q}`, which suggests a
Tang-type target `nu<2theta-1` for RH-027. The RH-028 benchmark was already
met on 2026-09-26. Lamzouri's Proposition 2.1 requires compactly supported
`eta`, weakening RH-032. Two pinned documents (Anthropic page, Karatsuba URL)
no longer reproduce from their URLs. No verdict changed.
[Dossier section 6](../context/2026-09-27-literature-and-representation-sweep.md).

## 2026-09-27: literature sweep, RH-027 correction and strategic review

A sweep of 2026 zero-proportion results, short-interval moment technology,
Fourier optimization, families and function fields, and cross-field
reformulations found no external result above the EXP-009 constant or the
EXP-010 onset. Wang's printed global gain is `delta_0=6.66624e-8`, read from
the cached v1 source; EXP-009 is about `2.9e-8` above `C_0+delta_0`. The
Yang group retracted its density-one preprint on 2026-09-03. The review
corrected the RH-027 premise: Steuding's short-window error is proved for
degree-one `Q`, fixed shifts and `nu<3/8`, and `(3theta-1)/4` is an inference.
It also corrected the title of reference 28. arXiv, Zenodo and Springer full
text were unreachable, so snippet-level statements are gated behind RH-030.
The program adopted methodology 13 records (`research-governance.json`,
`manuscript-map.md`) with active focus `RH-F4` and added RH-030 to RH-037. No
experiment was declared and no verdict changed.
[Dossier](../context/2026-09-27-literature-and-representation-sweep.md).

## 2026-09-26: Levinson manuscript v0.01 published and EXP-010 promoted

EXP-010 merged to `develop` through PR #341 and was promoted to `main` through
PR #342. The ten-page manuscript *Levinson's method in short intervals and
simple zeros of the zeta function* is published at
[10.5281/zenodo.22984155](https://doi.org/10.5281/zenodo.22984155) (concept
[10.5281/zenodo.22984154](https://doi.org/10.5281/zenodo.22984154)). The DOI was
reserved first and printed in the header; the deposit build differs from the
reviewed build only in those two lines. A fresh unauthenticated download
matches all 387,975 bytes, SHA-256
`4fd71686d6dada90c41a2156f5cbecb428d4f1acd372028020896113b1033d67`.
Publication is not external peer review.

## 2026-09-26: EXP-010 moved the simple-critical onset to 0.534

Declaration `2f7aaa6b` froze the question, eight degree-201 detector
parameter sets and all thresholds before any runner existed. EXP-010 proves
that Levinson's method with Conrey's general operator polynomial localizes to
`(T,T+T^theta]` for mollifier exponents `nu<theta-1/2` (Young's short proof
with a window weight), and that on such windows it counts distinct sign
changes of `Z` with density `kappa=1-log(c)/R` for every `Q` with
`Q(x)+Q(1-x)` constant. Certified constants give `kappa>0.7170 nu`, five times
the Selberg slope. Through the EXP-006 product this gives a positive
proportion of simple critical zeros for every fixed `theta` in `[0.534,1)`,
against `0.5458838` for EXP-008; at `theta=0.5459` the bound exceeds
`0.0177638`, about 1000 times the EXP-008 value. The canonical run
(`3dba086f`), the independent quadrature audit and the counting-lemma controls
(`77000336`) all passed. Writing the proof exposed and fixed two gaps of the
first draft (the off-diagonal tail and the reflected factor) and wrong lemma
numbers for Young's paper. Two independent referee passes found no fatal or
major error; their minor fixes are applied, and Prediction A's extension to
arbitrary `Q` was corrected (the constant term is `Q(0)^2`).

## 2026-09-24: EXP-009 confirmed and release 0.73.000 live-verified

EXP-009 proved the sharp three-point ratio `R(alpha,beta)<=sqrt(2)` and, under
Wang's arXiv:2609.24167v1 framework, the global simple-critical proportion
`0.6725007995946757558...`. The seven-page preprint is public at
[10.5281/zenodo.22940291](https://doi.org/10.5281/zenodo.22940291). Release
0.73.000 is live-verified from main; the details are in
[state.md](../../../../program/riemann-hypothesis/state.md).

## 2026-09-24: release 0.72.000 live-verified

Release PR #330 and promotion PR #331 merged. Tag `v0.72.000` points exactly to
main commit `45c34c81`. Main CI and Pages passed on that commit. Eleven public
files byte-match the exact-main build, and eight live desktop/phone EN/ES
light/dark scenarios visited all six research tabs and captured 352 screenshots
with zero failures. The compact live receipt preserves replay v7, both portable
canonical result hashes, the onset brackets, and the explicit source boundary.

## 2026-09-23: release 0.72.000 candidate passed rendered QA

The versioned candidate passed 66 scoped Riemann/export tests, 22 frontend
tests, the production build, and all repository guards. Its final pointer-driven
browser matrix passed 20 scenarios, 120 tab visits, and 3,072 screenshots in
both languages, both themes, and five viewport sizes with zero failures. Visual
inspection found and corrected an overflowing eight-experiment workflow label
before the final receipt was recorded. Promotion and live verification remain.

## 2026-09-20: replay v7 merged and release 0.72.000 prepared

Research PR #325 merged the source-bound EXP-007/008 replay, the eight-record
bilingual workbench, and updated program documentation into `develop` after
the complete Linux repository gate passed. Release candidate 0.72.000 records
the fixed-finite-rank transfer, the attributed rank-six onset, the strict
spectral companion, and manuscript v0.07. Rendered and live deployment gates
remain required before the release can be called complete.

## 2026-09-20: EXP-008 confirmed an earlier source-certified rank-six onset

Declaration `2297d2fc` preceded implementation and computation. EXP-008 proves
that the local Selberg detector transfer works for every fixed finite rank and
then applies Pearce-Crump's stated $C_6$ interval. The public source does not
print the rank-six coefficient matrix, so the input remains attributed.

The exact certificate proves
`0.5458837<theta6<0.5458838`, compared with
`0.5458846<theta3<0.5458847`. At theta=0.545884, the rank-six term exceeds
`2.5541123454645702e-7` while the rank-three term is negative. At theta=0.5459,
the pointwise gain exceeds `9.263543061777356e-7`. The optimized EXP-007
companion is also strictly positive. The portable canonical result SHA-256 is
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.

## 2026-09-20: manuscript v0.07 published and verified

The 30-page manuscript integrates the spectral-defect parity theorem,
rank-independent localization, and the source-certified rank-six onset. Three
DOI-bearing compilation passes had zero warnings, undefined references, and
box errors. All pages were rendered and visually inspected after the final
author-metadata correction. Zenodo published v0.07 at
[10.5281/zenodo.22860012](https://doi.org/10.5281/zenodo.22860012). A fresh
unauthenticated download matches all 575,351 local bytes, SHA-256
`c7bda5f1acc0b34ac33b6a071e66586b4032ae6e385d93f7fdd2d197411dbf81`.
Publication is not external peer review and does not change the open status of
RH.

## 2026-09-20: canonical JSON made byte-portable

The EXP-007 and EXP-008 runners now write explicit UTF-8/LF bytes, so canonical
hashes survive Git checkout normalization on Windows and Unix. Fresh clean-run
receipts bind EXP-007 to
`98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947`
and EXP-008 to
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.
The exact Windows byte streams cited by the already published v0.07 manuscript
remain archived under each experiment's `artifacts/windows-canonical-v1/`
directory.

## 2026-09-20: EXP-007 confirmed a spectral-defect parity coupling

Declaration `a2abdcc8360399b3fa42aaea9245e4b83352c30f` preceded implementation
and computation. The proof retains the full simple-real Gram defect through
the EXP-006 parity product:

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

The parameterized rank-trace theorem and spectral profile are attributed prior
work. The new candidate contribution is their coupling to odd support and the
resulting strict improvement of every positive point of the EXP-006 curve.
At theta=0.5459 the correlated directed-rational certificate proves
`H-h3>1.3732525985593292701164661575215e-70`. The onset bracket remains
`(0.545884,0.545885)`.

The canonical CPU run started from clean commit
`d63111ffa8a348c51eb4fd06f5a1e70a51211576`, checked 652,260 rational spectra
and 18,479 multiplicity profiles, and overlapped every shared quantity with an
independent 100-digit interval replay. Its result hash is
`ad635c5b60c4bcae63199fb54a7979a02206ce0ee572853b2df13933dafc320c`.
Two failed attempts remain preserved: one corrected the relation between two
independent interval enclosures, and one removed an unjustified positive-sign
expectation from a diagnostic sensitivity control. The result does not solve
RH, lower the onset exponent, or establish external priority.

## 2026-09-20: EXP-006 manuscript v0.06 published and verified

The 26-page manuscript includes the sharp finite product, its complete proof,
the quadratic short-interval transfer, the root bracket, the scalar barrier,
and the EXP-006 verification appendix. Three DOI-bearing compilation passes
had zero warnings, undefined references, and box errors. All 26 pages were
inspected in seven uncropped contact sheets. Zenodo published v0.06 at
[10.5281/zenodo.22852479](https://doi.org/10.5281/zenodo.22852479). A fresh
unauthenticated download matches all 545,773 local bytes, SHA-256
`dde6f2c9a6c0a9b46e66c9d44efc5786d1239dd1ada7664083a6d2134c452082`.
The v0.05 source, PDF, metadata and receipts are archived unchanged. Publication
is not external peer review and does not change the open status of RH.

## 2026-09-20: EXP-006 confirmed a sharper threshold below 0.545885

Declaration `b1febcf8a6d5830218e1df386af1e8a92c3037be` preceded all
implementation and computation. The first exact run confirmed the declared
product inequality. A consistency audit then retained the simple-real term in
the attributed arbitrary-parameter Hilbert bound, strengthening the theorem to

$$
(Q-S)(N-O)\ge2(N-S)^2.
$$

The amended runner was committed before the canonical run at
`0d736fa22ce7e833200381a32e8cc89f77c660e8`. Its 18,479-profile census,
directed rational threshold calculation, scalar barrier witness and independent
100-digit interval replay all passed. The canonical result hash is
`82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.

The short-interval consequence has a unique positivity root in
$(0.545884,0.545885)$. At $\theta=0.5459$, where the EXP-005 linear term remains
negative, it proves a simple-critical lower proportion above
$0.0000168381638551244569880374399$. The result is asymptotic, recent-preprint
dependent, and internally reviewed. It does not solve RH or establish external
priority or peer acceptance.

## 2026-09-20: EXP-005 manuscript v0.05 published and verified

The 24-page manuscript integrates the explicit local Selberg theorem, its proof,
the threshold bracket $(0.5459,0.546)$, and the fixed $\theta=0.546$ witness. It
passed the scientific-voice gate, a three-pass build with zero warnings or box
errors, and a full final-page render review. Zenodo published v0.05 at
[10.5281/zenodo.22851518](https://doi.org/10.5281/zenodo.22851518). A fresh
unauthenticated download matches all 526,178 local bytes, SHA-256
`bcfefac4b138d2b41c5fe232c64590e3b6f0c309455d40e01451d9251c1e8acc`.
The v0.04 source, PDF and metadata are archived unchanged. Publication does not
constitute external peer review, an effective-height result, or a proof of RH.

## 2026-09-19: EXP-005 confirmed an explicit threshold below 0.546

Declaration `6fd59fec51dda399de40e0327107dba42deb5b45` preceded implementation
and all canonical execution. Pearce-Crump's coefficient-uniform Selberg
detector was localized by retaining the arbitrary-subinterval form of its
rational-frequency estimate. For every fixed $1/2<\theta<1$, the resulting
distinct odd-critical lower proportion is $(\theta-1/2)/(4eC_3)$. Combining it
with EXP-004 gives an explicit simple-critical positivity threshold in
$(0.5459,0.546)$, improving Wang's reported cosine threshold.

At $\theta=0.546$, a fixed legal mollifier exponent proves odd-critical
proportion above $0.00643869330937194$ and simple-critical proportion above
$0.0000976239413345397$. The exact certificate passed all fourteen controls;
its result hash is
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.
The analytic audit checked every shortened-interval error term, normalization,
count convention and limit order. Two serialization attempts are retained as
failed/superseded evidence. The result is asymptotic, recent-preprint dependent,
and not a solution of RH.

## 2026-09-12: EXP-004 confirmed and v0.02 published

Declaration `e03413b2301bf45ca68ff6e945f25add9a1c3a89` preceded implementation and
computation. Commit `fbc4f9f` records the complete proof, exact runner, canonical
artifacts, final verdict and proof-review binding. The parity transfer combines a
fixed positive classical odd-zero density seed with multiplicity excess and proves
a fixed exponent below Wang's cosine positivity root with positive simple-critical
liminf. It also gives a distinct proportion above one half on a nearby fixed range.
The classical constant, new exponent, effective height and numerical threshold remain
unquantified; general RH remains open.

The run passed two symbolic identities, 24 atom regressions, all 19,683 declared
vectors and 59,049 slack evaluations, 42 rational primal/dual cases, 36 sharpness
controls and one negative distinct-count control. Two independent raw census checks
passed. The 1,234,096-byte census and all generated receipts are retained under the
EXP-004 artifacts directory. The exporter requires the proof-review record and binds
the declaration revision, premises and raw hashes.

The v0.02 manuscript was built twice without warnings, rendered across all 21 pages,
and visually reviewed. It is published and freshly verified at
[10.5281/zenodo.22728744](https://doi.org/10.5281/zenodo.22728744), 498,500 bytes,
SHA-256 `56b0ce29935fe3d115d9d40432f87f82b030355b028f3ea942fd3d3c671e2b1c`.
The v0.01 PDF remains unchanged at DOI 10.5281/zenodo.22727389.

## 2026-09-12: source-led opening

The user requested a full review of the recent zero-proportion breakthrough and its successors,
source persistence, original investigation, and publication when validated novelty warrants it.
The supplied Anthropic PDF differs from the current linked revision. Lamzouri v2 and Wang's
short-interval paper postdate the old portfolio audit. AxiomMath and Anthropic formal sources
have different theorem assumptions and validation coverage.

Opened the dedicated record, preserving unrelated work through isolated worktrees. Declared
EXP-001 for source/constants and EXP-002 for a possible short-interval stability extension.
No improvement or publication claim has been made. Pure kernel optimization and aggregate
multiplicity refinements were recognized as prior work before expensive computation.

## 2026-09-12: experiments confirmed, exposition consolidating

EXP-001 reproduced the exact baseline constants, source hashes and normalization correction.
EXP-002 derived the finite stability transfer and strict improvement of Wang's positive
short-interval curve. Independent proof and analytic-input audits found no unresolved gap;
the numerical theta=3/4 certificate has 48,761 nodes and zero unresolved boxes, with a
second certified arithmetic evaluator replaying every accepted leaf. General RH remains open.

Pure kernel optimization and aggregate multiplicity refinements were excluded as prior art.
The new result is a candidate contribution with a limited search-based novelty assessment.
Advanced to consolidating after adversarial review; manuscript, publication and web release
gates remain pending and are recorded separately.

## 2026-09-12: preprint published and public bytes verified

Published v0.01, DOI 10.5281/zenodo.22727389, concept 10.5281/zenodo.22727388.
The 10-page PDF passed full visual inspection with zero LaTeX warnings or overflowing boxes.
A fresh unauthenticated download matches all 368,644 reviewed bytes; public metadata verifies
the sole author, ORCID, date, version, preprint type, license and both DOIs. The publication
receipt is persisted beside the frozen PDF. This is a self-published preprint, not peer review.
The research unit remains consolidating until the public replay and release gates pass.

## 2026-09-12: public replay gate passed

The complete six-section EN/ES replay and contextual architecture passed 20 automated
language/theme/viewport scenarios with 960 screenshots and separate visual inspections.
Supplementary lower-diagram/source-link scrolling passed all 16 combinations. The full
Python suite has 251 passing tests; the frontend tests, TypeScript/build, Ruff and applicable
guards pass. The gate evidence is in `program/riemann-hypothesis/release-0.64.000/`.

Adversarial release review corrected Windows-versus-Git newline provenance and made Riemann
modal records independent of dirty, staged-only or locally deleted files. The canonical
EXP-001 LF replay matches its original Git artifact exactly; no mathematical result or frozen
manuscript bytes changed. Lifecycle advances to published under the web-content gate.
Version 0.64.000 promotion and live deployment remain separately observed release actions.

## 2026-09-12: version 0.64.000 delivered and live-verified

Research PR #263 merged at `00eace9e2a746c0b4122c5b085b84d804f5f47a0`.
Release PR #264 merged to main at `08660dc2d6bc91eae0d3a5105447793f0fbc670c`,
tagged `v0.64.000`. Pages run 34706614866 succeeded. The
[release closeout](../../../../program/riemann-hypothesis/release-0.64.000/README.md)
and [live receipt](../../../../program/riemann-hypothesis/release-0.64.000/live-verification.json)
record 13 public files matching the reviewed bytes and all eight EN/ES light/dark
desktop/phone scenarios passing, with 224 screenshots and no console, page or HTTP
errors. The 5,958-byte receipt was copied without alteration and its two raw-receipt
hashes were checked. RH-008 is complete. The published EXP-002 theorem and frozen
manuscript remain unchanged; live delivery is not external mathematical acceptance.

## 2026-09-12: pressure-frame source preflight and EXP-003 declaration

The [new primary-source dossier](../context/2026-09-12-pressure-frame-prior-art.md)
audits the tawanerguo, trmdy, Yuhang Shi and related multi-point pressure constructions.
Two new MIT repository snapshots and five source documents extend the archive to
26 documents and six snapshots, all passing byte/hash verification. Existing archive
entries were preserved. Pressure terms, nonuniform capacities, mixed certificates and
cross-boundary packing are prior art; the exact proposed odd-frame short-interval
consequence was not located in this bounded search.

[EXP-003](../experiments/EXP-003-odd-frame-pressure/hypothesis.md) is declared to test
odd-frame amplification using the frozen triangle certificate, followed by a separately
bounded two-variable pressure search. The declaration and full source preflight must be
committed before implementation or computation. At this handoff the run and verdict are
pending, and no new numerical lower bound is asserted. Stage A and Stage B require
separate outcomes and adversarial checks. The first release remains the authoritative
published baseline for comparison.


## 2026-09-12: EXP-003 confirmed; investigation broadens

Declaration 8ed806d preceded all computation. Proof and coordinating audit e21618c
establish the odd-frame pressure theorem. Result commit abfa001 confirms both stages:
Stage A replays the prior certificate and improves its assembly; Stage B certifies
p=1/12500, epsilon=443239/10^9 with 16,797 nodes and both arithmetic evaluators.
The theta=3/4 bound is 0.419087888170111727959091183775. One floating design pass
froze three candidates; the first passed and the other two were not run. No failed
search was erased or represented as a proof of optimality.

The full repository suite passed 288 Python tests after committed-source export
validation. The user then explicitly requested cross-area alternatives and a more
relevant result. New source-only reviews investigate critical-zero parity/multiplicity,
negative-spectrum witnesses, and established RH reformulations. No experiment in
those new families is declared or run at this entry. Current manuscript expansion
and replay consolidation remain in progress; v0.01 and public v0.64.000 are the
latest delivered versions. Private coordination PRs #631/#632 were merged and their
develop/main heads verified at 2bde950d.

## 2026-09-12: cross-area review persisted and EXP-004 declared

Commit be5aac4 archives the spectral and alternative-reformulation dossiers and
the source manifest, with all 61 then-listed documents passing exact restoration
verification. The reviews retain precise barriers for finite positivity, omitted
Nyman-Beurling coordinates, approximation/tail transfer, and zero-time heat-flow
limits; unreviewed external computational candidates remain attributed as such.

The parity route passed independent source and paper preflight. Declaration
e03413b2301bf45ca68ff6e945f25add9a1c3a89 was committed and pushed before
implementation or computation. EXP-004 will check exact residual certificates,
a fixed count census, primal/dual scalar controls, and the legal short-interval
deduction. The proposed consequence is positive simple-critical density at some
fixed exponent below the zero of Wang's cosine curve. Its classical density is
unspecified; no new numeric exponent is asserted. Finite arithmetic, complete
proof review and the final verdict are still pending at this chronological entry.

Commit 235b261 preserves five byte-identical v0.01 manuscript/publication files
under versions/v0.01. The old public DOI and PDF are unchanged. Private draft PR
#633 carries the confirmed pressure mirror and tested version helper. No new
Zenodo version is reserved or published at this point.

2026-09-28. Release 0.74.000 exports replay v9 (EXP-010, EXP-011, EXP-012 bound
by committed bytes) and the twelve-experiment bilingual workbench. Research PR
#346 and promotion PR #347 are merged; main commit a464bdb passed CI and Pages,
and the live bytes match the exact-main build. Candidate QA: 466 Python and 28
frontend tests, 8-scenario browser matrix with 416 screenshots and 0 failures.
Tag v0.74.000 is pending because the session proxy refuses tag pushes. RH-026 is
done.

## 2026-10-03: source update, fixed-input cap and supported phase obstruction

Fresh primary-source reading and upstream commit checks update external
standing. Declaration 8db97480 preceded EXP-013/014; declaration 12fa7d70
preceded EXP-015. All three confirm their scoped predictions with exact
arithmetic, separate auditors and 20 focused adversarial/replay tests.
EXP-013 gives 0.83699291404068... for an attributed strip-wide distinct
count and a uniform m=1310 cap. EXP-014/015 prove the pointwise phase
threshold, the latter with nonzero basic Mobius coefficients.
No new onset, signed-sum barrier, external peer review or RH result.

The methodology-13 review retains RH-F4 with a narrowed signed reduction
obligation and closes RH-F6. No new manuscript or Zenodo version. Current
count-label errors are corrected without rewriting prior frozen evidence.
The old tag-pending receipt is supplemented by verified metadata: tag
v0.74.000 targets a464bdb5 and the release published 2026-09-30 UTC.
Live replay remains v9; new records await serialized integration RH-042.

## 2026-10-03: trace-aware follow-up EXP-016

Declaration 0ea1f332 preceded implementation. A zero-sum Jensen surplus
strengthens the clipping dichotomy and gives the exact attributed
distinct-strip bound 69341429073721/82845897125000. Uniform revised
cap m=1311; EXP-013's original-assembly cap remains intact.
The initial auditor failed an algebraic-expression structural equality;
its failure is retained, and the repaired zero-difference check passes.
Eleven new controls and the previous twenty focused tests pass.
Canonical SHA-256 `7b0346f7e5122efc2a5d48dc6ceb6c28f0e8341cc8a5cf57be6863a16d1c2d74`. No new onset, RH, Lean, interval-replay
or peer-review claim. RH-F7 closes; no new manuscript/Zenodo trigger.

## 2026-10-03: EXP-017 retained-energy envelope

Declared and pushed as 416bad0d before computation; issue #354. The
uniform sharp proof, independent quadratic minorant, exact candidate and
50 focused tests pass. Formula prior art was located and explicitly
attributed before closure. Bound 0.83699292567522... is a small attributed
distinct-strip improvement; no onset/RH/new-manuscript claim. RH-F8 closes.

## 2026-10-03: EXP-018 conditional nine-point transfer

Declared/pushed a1bf2178 before arithmetic, licensed packet pinned by
45fca5a2, issue #355. Conditional uniform counting proof, independent
audit, capacities, exact candidate and 66 affected tests pass. The result
is 3997934614153/4775549550000=0.83716744477146... under explicit local
and analytic premises. The upstream stale pending flag and absent packet
hash in the replay log are retained. RH-F9 closes; RH-046 / issue #356
owns independent packet-bound replay and manuscript reassessment. No
unconditional input upgrade, onset/RH claim or public release is made.

## 2026-10-03: EXP-021 complete shifted composite arithmetic layer

Declaration 8d45ddfc preceded controls; derivation 6b84615c preceded the
4.17-second exact run. Gcd classes, local shifted Euler numerators,
primitive conductor/parity and squarefree induction factors are retained.
The receipt binds the proof, declaration and source. Exact cyclotomic,
symbolic and independent rational controls pass and distinguish three
incorrect alternatives; Ruff passes. This classical supporting layer
does not prove uniform analytic reciprocity or signed cancellation and
does not improve the onset/proportions. No manuscript trigger; the user
objective remains unmet. The EXP-020 full certificate continues running.
