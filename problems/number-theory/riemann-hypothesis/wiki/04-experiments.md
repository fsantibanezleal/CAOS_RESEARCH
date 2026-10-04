# 4. Experiments, certificates, and reproduction

The mathematical evidence consists of five declared experiments. EXP-001/002
hypotheses were committed as `266486f`; EXP-003 was declared in `8ed806d`,
with its complete pressure-method source preflight before computation. EXP-004
was declared in e03413b before its implementation and exact census. EXP-005
was declared in 6fd59fec before implementation and canonical execution.
The [first verdict](../experiments/EXP-001-source-and-constant-audit/verdict.md)
is a reproduction and algebraic audit. The
[second verdict](../experiments/EXP-002-short-interval-stability/verdict.md)
confirms the short-interval refinement within its stated analytic scope.
Neither a numerical search nor a successful test suite is used as a substitute
for the proof in [Chapter 3](03-mechanism.md).

## EXP-001: exact arithmetic and source integrity

The [runner](../experiments/EXP-001-source-and-constant-audit/run.py) starts
from exact rational Taylor enclosures. If $a^2=\theta^2/2$ is rational, then

$$\cos a=\sum_{j\ge0}\frac{(-1)^j(a^2)^j}{(2j)!},\qquad
\frac{\sin a}{a}=\sum_{j\ge0}\frac{(-1)^j(a^2)^j}{(2j+1)!}.$$

For the evaluated arguments, the positive term magnitudes decrease. The even
partial sum through index 40 is an upper bound, and the following odd partial
sum through index 41 is a lower bound. Exact rational arithmetic preserves
these inequalities. The positive sinc denominator permits interval division:

$$a\cot a=\frac{\cos a}{\sin a/a},\qquad
\frac1{\sqrt2}\cot(\theta/\sqrt2)=\frac{a\cot a}{\theta}.$$

Thus the primary path need not evaluate a trigonometric function at an
irrational floating argument. The remaining $\sqrt2$ in $C_2$ is enclosed by
integer-square-root bounds. Every final enclosure has width below $10^{-95}$.
A separate 256-bit Arb evaluation contains every exact enclosure.

| Certified formula | Value, truncated |
|---|---:|
| $C_0$ | 0.672500703679411645734379790803 |
| $C_1$ | 0.836250351839705822867189895401 |
| $C_2$ | 0.887620008173354339866075859447 |
| $c(3/4)$ | 0.419075012975424333734553610698 |

The [machine-readable artifact](../experiments/EXP-001-source-and-constant-audit/artifacts/result.json)
contains the full rational endpoints and outward decimal bounds. Reproducing
these published constants is not a novelty claim.

The symbolic part expands the numerator identity used in Chapter 3 directly
in polynomial variables for the sines and cosines. Its difference vanishes
before imposing the unit-circle constraints; reduction under those
constraints is an additional check. The tangent-addition obstruction is
checked separately. This confirms finite identities, without certifying any
imported theorem about primes or zeros.

The source audit also derives the dyadic correction

$$N(2T)-N(T)-\left\lfloor\frac{T\log(T/(2\pi))}{2\pi}\right\rfloor
=\frac{(2\log2-1)T}{2\pi}+O(\log T).$$

The revised Anthropic PDF's stronger absolute-error assertion is inconsistent
with this main term. Since the discrepancy is $o(N)$, this correction does
not by itself refute its limiting proportion theorem. See the precise
source locations in the experiment verdict.

Full mode verifies four required PDF hashes against both built-in pins and
the [source manifest](../context/source-manifest.json). It rejects missing
files, changed bytes, absent provenance, and cache paths escaping the source
directory. A fresh full replay produces the canonical UTF-8/LF Git artifact
byte for byte: 13,276 bytes, SHA-256
`a472e624ce0bf95e5a700fc663f6a37c57905e844b257f0a105a60f14da8cd62`.
The initial Windows CRLF replay had 13,474 bytes and SHA-256
`963313dc7cc1c5add51ddf4e6eb2d561a48156289861f27f946e857fca1df483`;
it contains identical mathematics. Both experiment runners and the shared
checkpoint writer now specify UTF-8 and LF explicitly, preserving byte hashes
across platforms. Regression checks exercise the actual saved bytes.
Source verification covers byte identity and metadata, rather than the
correctness of everything asserted inside those bytes.

## EXP-002: a complete compact-domain certificate

[D] The general theorem has a fully explicit positive analytic gap for every
fixed $\theta_0<\theta<1$. Its proof does not require minimization software.
The numerical experiment supplies a substantially stronger illustrative
three-point gap at one specified exponent.

Define

$$E_\theta(u,v)=2\{K_\theta(u)^2+K_\theta(v)^2+K_\theta(u+v)^2\},
\qquad \mathcal T_R=\{u,v\ge0:u+v\le R\}.$$

[MV] For $\theta=3/4$ and $R=21/4$, the committed
[triangle certificate](../experiments/EXP-002-short-interval-stability/artifacts/triangle-certificate.json)
proves $E_\theta\ge1/7000$ on all of $\mathcal T_R$. It describes a complete
binary subdivision of the enclosing rational square. Every terminal box is
either disjoint from the target triangle or carries an energy lower bound.
No unresolved terminal boxes remain.

| Certificate feature | Verified record |
|---|---:|
| Total tree nodes | 48,761 |
| Accepted energy leaves | 24,252 |
| Leaves outside the triangle | 129 |
| Unresolved boxes | 0 |
| Discovery precision | 160 bits |
| Independent evaluator replay | 256 bits |

These counts are consistent with a full binary tree: there are 24,381 leaves
and $2\cdot24,381-1=48,761$ nodes. Counts alone do not prove coverage; the
verifier reconstructs the rational subdivisions and checks their geometry.

The first evaluator uses Arb through `python-flint==0.9.0`. Since $f_\theta$
is a probability density supported in $[-\theta/2,\theta/2]$,

$$|K_\theta'(t)|
\le2\pi\int |x|f_\theta(x)\,dx\le\pi\theta.$$

This controls variation over each complete cell. A low value at one grid
point would not establish a cell lower bound; a high value alone would not
establish one either. The committed discovery and verification routines
propagate rigorous interval bounds and this derivative estimate.

Every accepted leaf was replayed using a separately derived sinc Taylor
evaluator with a rigorous remainder at higher precision. That avoids relying
on the same closed-form cancellation near removable singularities. Both
evaluators still share Arb, partition reconstruction, and the Lipschitz
bound. The replay is an independent arithmetic expression, not an entirely
independent verifier and not an end-to-end Lean proof.

A ten-node smoke run deliberately exhausted its budget and wrote a resumable
exact checkpoint. Resuming the earlier $R=6$, $d=10^{-5}$ case completed with
8,365 nodes. The final stronger certificate completed within its ten-minute,
two-million-node budget. CPU computation sufficed; no GPU evidence is claimed.
The floating grid in [explore.py](../experiments/EXP-002-short-interval-stability/explore.py)
selected candidates only and contributes no certified lower bound.

## Turning the certificate into a zero-proportion bound

The finite operator proof yields

$$c_{*,d}=\frac{3c(\theta)-2d/R}{3-d}.
$$

The numerical threshold belongs to the limiting nonsmooth cosine density.
For each $\delta<d$, choose a fixed smooth approximation retaining energy
at least $\delta$, then take the zero-height limit. Next take the approximation
limit, and finally let $\delta\uparrow d$. This is why the full $d$ may appear
in the final formula. Using it directly inside an unquantified smoothing
step would omit a necessary argument.

The [result artifact](../experiments/EXP-002-short-interval-stability/artifacts/result.json)
gives

$$c_{*,1/7000}=0.41907682842530399673666578752712697788\ldots,$$

$$c(3/4)=0.41907501297542433373455361069824246616\ldots,$$

$$c_{*,1/7000}-c(3/4)
=0.00000181544987966300211217682888451171\ldots.$$

The corresponding distinct-zero bound is
$0.70953841421265199836833289376356\ldots$. These are asymptotic
lower proportions in $(T,T+T^{3/4}]$. They are neither observed proportions
from a finite list of zeros nor an effective guarantee at a specified height.

## Reproduction from the repository root

Use the repository's pinned Python environment. The source archive contains
62 source documents/pages and six permissively licensed code snapshots.
Raw files whose redistribution permission was not identified remain in the
ignored local cache; the public manifest records how to restore exact bytes.

```text
python problems/number-theory/riemann-hypothesis/code/restore_sources.py
python problems/number-theory/riemann-hypothesis/code/restore_sources.py --verify-only
python problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit/run.py --output-dir tmp/riemann-baseline
python problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/run.py --output-dir tmp/riemann-replay --radius 21/4 --threshold 1/7000
python -m pytest tests/test_riemann_baseline.py tests/test_riemann_certificates.py
```

Outputs go to new explicit directories so that replay does not overwrite
the committed canonical artifacts. Restoration fails closed if upstream bytes
change. A changed upstream URL requires a documented source revision, rather
than silently accepting a new file under the old hash.

The cheap baseline suite is also usable in CI without PDFs:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit/run.py --math-only --output-dir tmp/riemann-baseline-math
python -m pytest tests/test_riemann_baseline.py
```

Math-only mode reports `PASS_MATH_ONLY`, with `math_status: PASS` and
`source_verification.status: NOT_PERFORMED`. It does not read the source
manifest or cached PDFs. Eleven baseline tests check exact constants,
symbolic identities, deterministic artifacts, precision restoration,
cache-independent CLI behavior, and failure on synthetic changed sources
or escaping paths. The persisted verdict records all eleven passing.

## What remains outside machine verification

The mathematical transfer still imports Wang's inspected analytic theorem
and the classical zero-count asymptotic. The signed operator identities,
multiplicity bookkeeping, spectral pinching, triple overlap, smoothing, and
order of limits received an independent adversarial review. That is human-style
mathematical validation by separate agents, rather than community peer review.
The [audit](../experiments/EXP-002-short-interval-stability/adversarial-audit.md)
records what was checked and why tempting shortcuts were invalid.

Passing EXP-001/002 tests does not establish a new positivity exponent, a global
record, a starting height, a full upstream Lean replay, or the Riemann
hypothesis. The later EXP-004 range extension has its own universal proof below. The candidate contribution has a complete mathematical record;
its analytic acceptance and priority remain subject to outside scrutiny.

[Previous: full proof](03-mechanism.md) | [Next: open questions](05-open-questions.md)


## EXP-003: odd-frame amplification and a new pressure certificate

[The third verdict](../experiments/EXP-003-odd-frame-pressure/verdict.md) confirms
two separate predictions. Stage A checks the stronger alternating-frame assembly,
including 328 pair-incidence/span/boundary cases and two symbolic identities, then
replays the entire 48,761-node prior certificate. Its gain over EXP-002 increases
by the exact factor $20999/14000$.

Stage B performed one deterministic floating design pass over 16 pressure values,
using the previous EXP-002 exploration only as additional witness seeds. It froze
three rational candidates before certification. The first candidate passed; the
remaining two are recorded as not run after that success. A sampled minimum was
never accepted as a certificate. The full new tree has 16,797 nodes and its exact
parameters are $p=1/12500$, $\epsilon=443239/10^9$ at $\theta=3/4$.

The new acceptance functional is $E_3(u,v)+p(u+v)\ge\epsilon$. Its cutoff
$\epsilon/p=443239/80000$ is derived from the same rational parameters.
Pressure-only leaves use the exact inequality at each box's lower endpoints,
including equality. Other leaves certify the whole cell with an outward energy
bound plus the exact minimum pressure. The full square is reconstructed, and
pressure alone covers everything outside it in the nonnegative quadrant.

Construction genuinely resumes from its saved candidate partition. Replay validates
checkpoint identity and rechecks the prefix arithmetic before continuing; it does
not trust saved acceptance claims or promise to skip that work. The tiny smoke
forced a ten-node stop, checked flushed output and exact construction resume, and
rejected mismatched parameters. Budget time includes replay restoration. The
record distinguishes deterministic mathematical outputs from operational timings.

Canonical [result](../experiments/EXP-003-odd-frame-pressure/artifacts/result.json),
[frozen candidate list](../experiments/EXP-003-odd-frame-pressure/artifacts/candidates.json),
[runner](../experiments/EXP-003-odd-frame-pressure/run.py),
[checker](../code/riemann_pressure.py) and
[adversarial audit](../experiments/EXP-003-odd-frame-pressure/adversarial-audit.md)
preserve the complete evidence. The [replay guide](../../../../docs/guides/riemann-replay.md)
contains the current reproduction commands. Committed source hashes bind the reused
certificate, declaration, code, runner, exploration seeds and frozen candidates.


## EXP-004: exact parity transfer and a qualitative range extension

The [fourth verdict](../experiments/EXP-004-parity-density-transfer/verdict.md)
is confirmed. The full [Chapter 7 proof](07-parity-density-transfer.md) retains
odd critical support and multiplicity excess in the signed-operator inequality,
then combines one fixed classical density seed with Wang's fixed-test theorem.
Its precise quantifiers produce some fixed $\theta_1<\theta_0$, with positive
simple-critical density for every fixed exponent at least $\theta_1$ and below one.
No unspecified constant is replaced with a guessed numerical value.

The declaration froze two residual identities, multiplicity atoms, a census of
19,683 vectors with three slack values each, 42 rational relaxation controls,
36 sinc sharpness cases, and one false distinct-count control. All passed in the
single full run, 8.0353704 seconds against a 60-second budget. The 36 focused
software tests also passed. Two reviewers separately parsed every raw census
row with direct formulas, without importing the experiment runner.

The canonical result has SHA-256
`bc9e28ca1792657e24da77268e6e2108c3f52684b7e16504f07b32cfce014d6e`.
The 1,234,096-byte full census, original flushed stdout, operational timing,
exact witnesses, checkpoint and execution receipt are preserved under
[artifacts](../experiments/EXP-004-parity-density-transfer/artifacts/).
The runner reports finite arithmetic success separately from the all-height
claim. A [hashed review record](../experiments/EXP-004-parity-density-transfer/proof-review.json)
binds the final proof, audit, hypothesis, result and verdict. The public exporter
requires both gates; changed proof bytes invalidate the review binding.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/run.py --output tmp/riemann-parity-replay
pytest tests/test_riemann_parity.py
```

The elementary primal/dual result proves optimality only in its declared scalar
relaxation, not among all Gram methods or zeta arguments. Checkpoint prefixes
record interrupted work; the complete census is rechecked on fresh replay.

## EXP-005: explicit local Selberg transfer

The [fifth verdict](../experiments/EXP-005-local-selberg-transfer/verdict.md) is
confirmed. The paper proof localizes Pearce-Crump's optimized sign detector by
retaining the source's arbitrary-subinterval off-diagonal estimate. It gives
an explicit odd-critical density for every fixed exponent above one half and,
through EXP-004, brackets the new simple-critical positivity threshold in
$(0.5459,0.546)$.

The canonical certificate passed fourteen exact and interval controls. At
$\theta=0.546$, the fixed legal exponent $u=0.02299$ has strict localization
margin $1/50000$ and proves a simple-critical proportion above
$0.0000976239413345396825264438351212564$. The result JSON has SHA-256
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.

Two earlier artifacts are retained: one failed at Python's integer-to-string
serialization cap, and one passed mathematically but used nonportable JSON
number tokens. The final exact rationals use decimal strings and parse under
both Python and PowerShell. Five focused tests and Ruff passed.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/run.py --output-dir tmp/riemann-exp005-replay --budget-seconds 60
pytest tests/test_riemann_local_selberg.py
```

The [proof review](../experiments/EXP-005-local-selberg-transfer/proof-review.json)
binds the hypothesis, proof, audit, result and verdict. The computation cannot
replace the analytic localization proof, and neither constitutes external peer
review or an effective-height theorem.

## EXP-006: Hilbert dimension and parity compression

The [sixth verdict](../experiments/EXP-006-hilbert-parity-compression/verdict.md)
is confirmed. The original declared product passed, then the consistency audit
restored the simple-real term already present in the attributed Hilbert bound.
The final sharp theorem is

$$
(Q-S)(N-O)\ge2(N-S)^2.
$$

The earlier broad-bracket and weaker-transfer runs remain under the artifact
directory. The strengthened canonical run started from clean commit
`0d736fa22ce7e833200381a32e8cc89f77c660e8`, checked 18,479 multiplicity
profiles, directed rational transcendental bounds, a scalar barrier witness,
and containment of a separate 100-digit interval replay. Its result SHA-256 is
`82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.

At $\theta=0.5459$, EXP-006 proves the simple-critical lower proportion exceeds
$0.0000168381638551244569880374399$. It brackets the unique positivity root in
$(0.545884,0.545885)$.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/run.py --output-dir tmp/riemann-exp006-replay --budget-seconds 120
pytest tests/test_riemann_hilbert_parity.py tests/test_riemann_local_selberg.py tests/test_riemann_parity.py
```

The [proof review](../experiments/EXP-006-hilbert-parity-compression/proof-review.json)
binds the amended hypothesis, runner, focused tests, proof, audit, canonical
result and verdict. The finite census is diagnostic; the written argument proves
universality and the asymptotic transfer.

## EXP-007: spectral-defect parity coupling

The [seventh verdict](../experiments/EXP-007-spectral-defect-parity/verdict.md)
is confirmed. The finite theorem retains the simple-real spectral defect:

$$
(Q-S-D(G))(N-O)\ge2(N-S)^2.
$$

The pressure transfer then proves `H(theta)>h3(theta)` for every fixed exponent
where `h3` is positive. At `theta=0.5459`, the correlated exact gain exceeds
`1.3732525985593292701164661575215e-70`. This is a strict full-curve
improvement, not a lower onset exponent or a new printed headline decimal.

The portable canonical run checked 652,260 rational spectra and 18,479
multiplicity profiles. Its result SHA-256 is
`98094f267a78b88b8a976de6b6d816fbb25231869a6ad5dc8c941411bfa45947`.
Every shared exact interval overlaps an independent 100-digit replay. The
historical theta=3/4 control makes the coupled root worse while leaving the
pressure-only theorem stronger, and the result records that boundary.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/run.py --output-dir tmp/riemann-exp007-replay --budget-seconds 180
python -m pytest -q tests/test_riemann_spectral_defect_parity.py
```

The [proof review](../experiments/EXP-007-spectral-defect-parity/proof-review.json)
binds the declaration, runner, focused tests, proof, audit, canonical result,
and verdict. The two failed attempts remain preserved as audit evidence.

## EXP-008: rank-six local transfer

The [eighth verdict](../experiments/EXP-008-rank-six-local-transfer/verdict.md)
is confirmed relative to Pearce-Crump's stated source-certified rank-six
constant. The written proof first removes the rank-three restriction from the
EXP-005 localization argument. For every fixed finite rank $q$,

$$
\liminf\frac ON\ge\frac{\theta-1/2}{4eC_q}.
$$

Combining the $q=6$ curve with EXP-006 gives the onset brackets

$$
0.5458837<\theta_6<0.5458838
<0.5458846<\theta_3<0.5458847.
$$

At $\theta=0.545884$ the rank-six term is positive and the rank-three term is
negative. At $\theta=0.5459$, the rank-six lower bound exceeds
`0.0000177645181613023236390595079` and its improvement over rank three
exceeds `9.263543061777356e-7`. The optimized EXP-007 companion at
`rho=11/5` has a strict gain floor above `1.7766622541125682e-68`.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/run.py --output-dir tmp/riemann-exp008-replay --budget-seconds 120
python -m pytest -q tests/test_riemann_rank_six_local.py
```

The portable canonical result SHA-256 is
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.
The source prints the $C_6$ interval but not its coefficient matrix, so the
certificate validates the transfer and downstream arithmetic without claiming
an independent reconstruction. The [proof review](../experiments/EXP-008-rank-six-local-transfer/proof-review.json)
binds this limitation to the displayed result.

## EXP-009: sharp Wang kernel ratio

The [ninth verdict](../experiments/EXP-009-wang-kernel-sharpening/verdict.md)
confirms the exact bound `R(alpha,beta) <= sqrt(2)` with equality exactly at
`(0,1)` and `(1,0)`. The hyperbolic substitution reduces the two-variable
problem to monotonicity in one compact coordinate and the residual square
`(X^2-2)^2`.

Substitution into Wang's pinned v1 global framework certifies a simple-critical
proportion above `0.672500799594675755828355056296...`, a distinct-zero
companion above `0.836250399797337877914177528148...`, and a gain above the
baseline greater than `9.5915264110093975e-8`. The global transfer remains
relative to Wang arXiv:2609.24167v1.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-009-wang-kernel-sharpening/run.py --output-dir tmp/riemann-exp009-replay --budget-seconds 600
python -m pytest -q tests/test_riemann_wang_kernel_sharpening.py
```

The canonical result SHA-256 is
`0cea78e847d1bcec62eb8cd809b704ceaebd58f78f1c405f13ec40838fbb5a66`.
The proof review binds the declaration, strengthened amendment, runner,
focused tests, result, execution receipt, proof and audit. A separate
seven-page preprint is published at DOI `10.5281/zenodo.22940291`.

## EXP-010: localized Levinson detector

The [tenth verdict](../experiments/EXP-010-levinson-parity-transfer/verdict.md)
records three results. Young's short proof of the mollified second moment runs
on the window `(T,T+T^theta]` for mollifier exponents `nu<theta-1/2`; the
localized Levinson method with any `Q` satisfying `Q(x)+Q(1-x)` constant
counts distinct sign changes of `Z` with density `kappa=1-log(c)/R`; and
degree-201 detectors certify `kappa>0.7170 nu`. The EXP-006 product then gives
a positive proportion of simple critical zeros for every fixed `theta` in
`[0.534,1)`, with `h>0.0177638` at `theta=0.5459`.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-010-levinson-parity-transfer/run.py --output-dir tmp/riemann-exp010-replay
python problems/number-theory/riemann-hypothesis/experiments/EXP-010-levinson-parity-transfer/audit.py --canonical tmp/riemann-exp010-replay/result.json --output-dir tmp/riemann-exp010-audit
python problems/number-theory/riemann-hypothesis/experiments/EXP-010-levinson-parity-transfer/controls.py --output-dir tmp/riemann-exp010-controls
python -m pytest -q tests/test_riemann_levinson_parity.py
```

The canonical result SHA-256 is
`74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464`. The
auditor never forms the exact moment reduction; it integrates the original
integrand by validated quadrature from the Chebyshev generators. The controls
check the counting lemma on zeta windows at three heights and on test
functions with planted double and triple zeros.

## EXP-011: linear-refinement barrier

The [eleventh verdict](../experiments/EXP-011-linear-refinement-barrier/verdict.md)
is confirmed. For the Montgomery-Taylor window, six real triples around one
conjugate pair violate `Q>=2N+3O-4S` by `0.0582`, and a 10001-cell lattice has
`(Q-2N)/O=2.3589`, so no linear refinement of the EXP-006 product with
`beta>=2.365` holds. Replay:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-011-linear-refinement-barrier/run.py --output-dir tmp/riemann-exp011-replay
```

The audit recomputes the counterexample with a quadrature-evaluated kernel and
the lattice with an independent float64 sum. Chapter:
[linear-refinement barrier](14-linear-refinement-barrier.md).

## EXP-012: Tang-type short-window moment (stopped)

The [twelfth verdict](../experiments/EXP-012-tang-short-window-moment/verdict.md)
is inconclusive. Tang's short-window reciprocity trades the off-diagonal for a
dual moment of Dirichlet `L`-functions whose weight has size `H/sqrt(T)`; the
dual moment is about `sqrt(h)sqrt(T)` per twist pair, so trivial and
large-sieve bounds give at best EXP-010's range `nu<theta-1/2`. A longer
admissible mollifier needs an asymptotic evaluation of the dual family.

## EXP-013--015: fixed-input cap and supported phase obstruction

The [EXP-013 verdict](../experiments/EXP-013-mixed-gram-parameter-cap/verdict.md)
confirms the exact source-based distinct-strip parameter improvement and
uniform cap. [EXP-014](../experiments/EXP-014-short-window-phase-collision/verdict.md)
proves the generic phase threshold; [EXP-015](../experiments/EXP-015-squarefree-phase-collision/verdict.md)
extends it to nonzero basic Mobius coefficients. All are research records.

Each runner accepts --output-dir; its auditor accepts --artifact and --output.
Run the three experiment directories' run.py then audit.py entry points.
The corruption controls and byte-identical replay checks are:

```text
python -m pytest -q tests/test_riemann_parameter_and_phase.py
```

The threshold obstruction concerns uniform pointwise oscillation. It does
not exclude cancellation of the signed sum or change the onset 0.534.

## EXP-016: trace-aware clipping

[Verdict](../experiments/EXP-016-trace-aware-clipping/verdict.md): confirmed.
The trace-zero Jensen surplus permits m=1311 and improves the distinct-strip
bound to 0.83699291672944... with the same attributed source inputs.
Its runner/auditor use --output-dir and --artifact/--output respectively.
Run `python -m pytest -q tests/test_riemann_trace_clipping.py` for the
11 equality, missing-premise, corruption and byte-replay controls.

## EXP-017--024: stronger transfers, full covers and signed representation

[EXP-017](../experiments/EXP-017-sharp-energy-envelope/verdict.md) gives
the attributed distinct-strip bound 0.83699292567522..., with its scaled
prior-art attribution. [EXP-018](../experiments/EXP-018-nine-point-distinct-transfer/verdict.md)
is a conditional larger transfer whose local input remains unclosed.
EXP-019's source-identical cover is suspended with validated snapshots;
EXP-020's stronger-target cover subsequently completed and passed all final checks. Partial coverage is
not a universal local inequality.

[EXP-021](../experiments/EXP-021-composite-character-layer/verdict.md)
confirms the classical arithmetic layer and its exact controls.
[EXP-022](../experiments/EXP-022-pressure-duality-audit/verdict.md)
proves a ceiling for this fixed pressure assembly, not the true zero
proportion. EXP-023's separately bound changed-pressure full cover is
still incomplete. Its cost reviews and ownership controls are operational
evidence; no new zero-bound verdict is inferred.

[EXP-024](../experiments/EXP-024-gaussian-mellin-reduction/verdict.md)
closes the representation step in the scope described in the
[dual-moment chapter](15-dual-moment-range.md). Its signed main estimate
remains open. None of these finite controls proves RH or external peer
acceptance. The handoff records live bindings and current coverage.

## EXP-020 and EXP-025 completed consequences

## Completed distinct-zero results, 2026-10-03

EXP-020 completed all 96 shards and every final check: the stronger local
inequality gives 3997934614153/4775507750000=0.8371747724947154... for
distinct strip points. EXP-025's reviewed vector-pressure application gives
30945470743359/36955122080000=0.8373797460706156..., with Lavery's
external universal local theorem explicitly attributed and not locally
Lean-rebuilt. The corrected BGSTB integrated theorem and Knausgard's
mixed-Gram argument remain dependencies.

The focused companion `distinct-zero-gram` v0.01 is published and all three
files are live-byte-verified: [version DOI](https://doi.org/10.5281/zenodo.23128663),
[concept DOI](https://doi.org/10.5281/zenodo.23128662). Its PDF is 376,803 bytes,
SHA256 2d524ee456b330598a78bf56ab532e93ca027c500c846065b103dcfcd1cba0c4.
The exact-byte EXP-020 runtime and scoped mathematical source ZIPs are public.
Issues #356/#358 close the local input obligation; #364 tracks publication
and release. PR #363 remains draft and unmerged. No new live application
release or private main promotion is claimed yet.

EXP-023 remains 95/96 under its owned supervisor through the deadline
2026-10-04 02:48:12 UTC. Its larger 0.8373855610599298... candidate is
unproved and not in the published theorem. EXP-019 remains suspended.
RH is open; the short-window onset stays 0.534. Worldwide priority and peer
acceptance are unconfirmed. RH-F4 remains the active analytic focus.

The full derivation, exact inputs and claim boundaries are in
[the distinct-zero chapter](20-distinct-zero-certificates.md).
