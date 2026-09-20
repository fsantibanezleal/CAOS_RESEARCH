# Riemann hypothesis: short-interval zero proportions

[D+MV] EXP-006 strengthens the finite transfer by keeping Lamzouri's Hilbert
dimension before scalar compression. For every conjugation-invariant finite
multiset in the kernel setting,

$$
(Q-S)(N-O)\ge2(N-S)^2.
$$

Together with EXP-005, this gives the explicit short-interval term

$$
h_3(\theta)=\frac{3+k_3(\theta)-
\sqrt{(1-k_3(\theta))(9-k_3(\theta)-8c(\theta))}}4.
$$

Its unique positivity threshold satisfies
$0.545884<\theta_{\rm HP}<0.545885$. At the previously excluded exponent
$\theta=0.5459$, the exact certificate proves
$\liminf S/N>0.0000168381638551244569880374399$, while the EXP-005 linear
term remains negative. The [complete proof](09-hilbert-parity-compression.md)
and [confirmed verdict](../experiments/EXP-006-hilbert-parity-compression/verdict.md)
state the attribution and limits. General RH remains open.

[D+MV] EXP-005 supplies the first explicit interval-range improvement in this
record. For every fixed $1/2<\theta<1$, it proves

$$
\liminf\frac{O(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{\theta-1/2}{4eC_3},
$$

where $O$ counts distinct odd-multiplicity critical zeros and $C_3$ is
Pearce-Crump's certified rank-three constant. Combining this with EXP-004
places the simple-critical positivity threshold in $(0.5459,0.546)$, below
Wang's reported cosine threshold $0.550193964744154\ldots$. At
$\theta=0.546$, a fixed legal mollifier proves
$\liminf S/N>9.7623941\times10^{-5}$. The
[complete local proof](08-local-selberg-transfer.md) and
[confirmed verdict](../experiments/EXP-005-local-selberg-transfer/verdict.md)
state the assumptions and limits. General RH remains open.

[D+MV] EXP-004 proves a qualitative extension of the interval range for a
positive proportion of simple critical zeros. Let

$$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2,$$

and let $\theta_0$ be its unique zero. With $\alpha=51/100$, there is one fixed
$\kappa>0$ such that, for every fixed $\theta\in(\alpha,1)$,

$$\liminf S/N\ge\max\{0,c(\theta),(c(\theta)+2\kappa)/3\},$$

$$\liminf Z/N\ge\max\{\kappa,(1+c(\theta))/2,(3+2c(\theta)+\kappa)/6\}.$$

The counts concern $(T,T+T^\theta]$: $N$ counts every nontrivial zero copy,
$S$ simple critical zeros, and $Z$ distinct complex zeros. Classical odd-zero
density and the retained multiplicity excess supply the additional input.
The [complete parity proof](07-parity-density-transfer.md) proves that

$$\theta_1=\theta_0-\min\{(\theta_0-\alpha)/2,\kappa/4\}<\theta_0$$

has $\liminf S/N\ge\kappa/3>0$ for every fixed $\theta\in[\theta_1,1)$.
This strictly extends the positivity range of Wang's displayed cosine bound.
There is also a distinct-above-one-half extension with the separate
$\kappa/16$ shift. No value of $\kappa$, new decimal exponent, uniform moving
exponent, or effective starting height is proved. General RH remains open.

The [confirmed verdict](../experiments/EXP-004-parity-density-transfer/verdict.md)
binds the universal argument to its primary-source audits. Exact checks include
19,683 census vectors, 59,049 slack evaluations, 42 rational primal/dual controls,
36 sharpness configurations, and a negative control rejecting the false distinct
half-sum shortcut. Finite checks do not replace the analytic proof. Independent
automated reviews are not external peer review or end-to-end formal verification.

## Explicit pressure improvement retained from EXP-003

[D+MV] EXP-003 strengthens the earlier stability refinement and certifies a new
all-gap pressure inequality. At the fixed exponent $\theta=3/4$, the asymptotic
simple-critical proportion is at least

$$c_B=0.419087888170111727959091183775\ldots,$$

with distinct-zero companion $(1+c_B)/2=0.709543944085055863979545591887\ldots$.
All denominators count nontrivial zero copies with multiplicity in
$(T,T+T^{3/4}]$. The Riemann hypothesis remains open.

| Evidence | Simple-critical lower bound |
|---|---:|
| Wang's baseline | $0.419075012975424333734553610698\ldots$ |
| EXP-002, published v0.01 example | $0.419076828425303996736665787527\ldots$ |
| EXP-003 A, reuse of the same compact certificate | $0.419077736020568836833221725071\ldots$ |
| EXP-003 B, new pressure certificate | $0.419087888170111727959091183775\ldots$ |

The new gain above Wang is $0.000012875194687394224537573076981\ldots$ in
proportion. The target compared this gain with $5/4$ of Stage A's gain, and the
outward-rounded comparison is strictly positive. This does not mean a 25%
increase in the full zero proportion. The [confirmed verdict and exact enclosures](../experiments/EXP-003-odd-frame-pressure/verdict.md)
specify the theorem, computation and source boundaries.

[D] More generally, every fixed positive point of Wang's cosine curve

$$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2$$

receives a strictly stronger bound than EXP-002 using its same analytic compact
energy input. Pair-disjoint triples inside an odd-sized frame share vertices but
do not duplicate pair energy; their spans telescope. The known spectral cap and
disjoint-frame pinching convert this into a stronger counting inequality.

The finite stability, root obstruction, global pressure and capacity frameworks
are attributed prior work. The scoped contribution is their stronger short-interval
consequence, with full multiplicity and limit accounting. The [expanded prior-art audit](../context/2026-09-12-pressure-frame-prior-art.md)
did not locate an identical short-interval theorem; it does not guarantee priority.

1. [Statement, counting conventions and history](01-statement.md)
2. [Known results, barriers and formal scope](02-known-results.md)
3. [First finite-operator and short-interval proof](03-mechanism.md)
4. [Experiments, certificates and reproduction](04-experiments.md)
5. [Open questions and rejected approaches](05-open-questions.md)
6. [Complete odd-frame pressure theorem](06-odd-frame-pressure.md)
7. [Complete parity density transfer and interval-range theorem](07-parity-density-transfer.md)
8. [Explicit local Selberg transfer and numerical positivity threshold](08-local-selberg-transfer.md)
9. [Hilbert dimension, parity compression, and the improved threshold](09-hilbert-parity-compression.md)
10. [Spectral-defect parity coupling and the strict full-curve improvement](10-spectral-defect-parity.md)
10. [Spectral-defect parity coupling and the strict full-curve improvement](10-spectral-defect-parity.md)

The new certificate uses $p=1/12500$, $\epsilon=443239/10^9$, $k=2256$ and
frame size $4513$. All 16,797 partition nodes were checked, with 8,351 energy-plus-pressure
leaves, 48 pressure-only leaves and no unresolved cells. Construction used Arb at
160 bits; complete replay used a separate sinc-Taylor evaluator at 256 bits.
Both paths share Arb, partition geometry and a Lipschitz estimate. They are not an
independent complete verifier or an end-to-end Lean proof.

The [source manifest](../context/source-manifest.json) records 64 source documents/pages and seven
licensed repository snapshots with versions, sizes, hashes and licenses. Original
documents remain in the local repository cache where redistribution rights were
not identified. Licensed snapshots retain their notices. The [bibliography](../references.md)
distinguishes source theorems, un-replayed candidate claims and formal hypotheses.

The manuscript series is [Simple critical zeros in short intervals: stability, parity, localization, and Hilbert compression](https://doi.org/10.5281/zenodo.22727388).
The first published version is [v0.01](https://doi.org/10.5281/zenodo.22727389);
The Hilbert-parity theorem forms the published v0.06 expansion, with version
DOI [10.5281/zenodo.22852479](https://doi.org/10.5281/zenodo.22852479). The [manuscript directory](../../../../manuscripts/riemann-hypothesis/short-interval-stability/)
and publication receipts record the actual publication state. A preprint is not
peer review or mathematical community acceptance.

Evidence labels: **[D]** derived with a persisted proof and refutation attempt;
**[MV]** machine-verified finite assertion; **[C]** conjectural direction. This work
establishes an explicit positivity threshold below $0.545885$. It does not give
an effective height, global record, universal simplicity theorem, or solution
of RH.
