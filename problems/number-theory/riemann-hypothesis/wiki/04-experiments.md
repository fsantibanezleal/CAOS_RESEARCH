# 4. Experiments, certificates, and reproduction

The mathematical evidence consists of three declared experiments. EXP-001/002
hypotheses were committed as `266486f`; EXP-003 was declared in `8ed806d`,
with its complete pressure-method source preflight before computation.
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
21 primary-source documents and four permissively licensed code snapshots.
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

Passing the tests does not establish a new positivity exponent, a global
record, a starting height, a full upstream Lean replay, or the Riemann
hypothesis. The candidate contribution has a complete mathematical record;
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
