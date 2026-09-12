# 5. Open questions, rejected routes, and falsification targets

The current confirmed results are the explicit pressure improvement in
[EXP-003](../experiments/EXP-003-odd-frame-pressure/verdict.md) and the qualitative
interval-range improvement in [EXP-004](../experiments/EXP-004-parity-density-transfer/verdict.md).
The Riemann hypothesis remains open. The questions below go beyond those proved results.

## Further improve the explicit short-interval example

EXP-003 has completed one pressure-certificate improvement and the odd-frame
transfer. The next question is whether a separately declared campaign can improve
its current bound further or certify a range of exponents.

[C] The original certified choice $R=21/4$, $d=1/7000$ is conservative. For fixed
$\theta$, let

$$d_\theta(R)=\min\left(1,\inf_{u,v\ge0,\ u+v\le R}
2\{K_\theta(u)^2+K_\theta(v)^2+K_\theta(u+v)^2\}\right).$$

Chapter 3 proves this is positive for finite $R$. Any rigorous lower bound
$d\le d_\theta(R)$ gives gain

$$\frac{d\{c(\theta)-2/R\}}{3-d}.$$

Increasing $R$ improves the span penalty $2/R$ but enlarges the domain over
which energy must be bounded. The actual optimization concerns their
combination. A sampled larger minimum cannot replace an exhaustive enclosure.
An independently implemented rational Taylor verifier would also reduce
shared arithmetic and geometry assumptions in the existing certificate.

A useful next experiment would declare a finite rational grid of exponents,
radii, and thresholds, use floating exploration only for ordering candidates,
and certify each accepted pair. Its claim should be limited to the declared
parameter values unless a joint interval certificate covers all intermediate
exponents. The falsification target is an unresolved box or a rigorously
enclosed energy value below the proposed threshold.

## Retain still more of the actual Gram matrix

[D] EXP-003 now supplies a valid larger-frame assembly and a stronger short-interval
bound. The open task is to go beyond this elementary unit-cap frame family.

[C] Consecutive triples lose information when convex pinching removes
interactions between blocks. Larger windows might make the defect larger.
For a PSD unit-diagonal $m$-point Gram matrix the same spectral quantity

$$D(G)=\operatorname{tr}\Psi(G)$$

is available, but the combinatorial overlap penalty and the compact-domain
dimension also increase. The
[Ainta](https://github.com/ainta/zeta-simple-zeros/tree/040c5e899e658aed7b56a2a87f501798fe10761d)
and [trmdy](https://github.com/trmdy/zeta-simple-zeros-673137/tree/1610b97b7895ff34982260f8dcaf04a0f7b82cf7)
global window refinements are direct prior art for this direction. EXP-003 supplies that transfer for its alternating schedule. Any further
novelty claim must compare with the expanded pressure-frame source dossier.

Any proposed improvement must prove a valid disjoint partition or fractional
cover inequality. Adding defects of overlapping principal submatrices with
coefficient one is unjustified. EXP-002's factor $1/3$ comes from three actual
partitions; it cannot be changed to $1/2$ merely because each gap belongs to
two consecutive triples.

## Quantify the new positivity range

[D] EXP-004 answers the qualitative range question by supplying the missing
odd-zero input and retaining multiplicity excess. Its [complete proof](07-parity-density-transfer.md)
gives a fixed $\theta_1<\theta_0$, with no numerical value assigned to the
classical density $\kappa$. Pressure amplification by itself still requires a
positive baseline and does not prove this extension.

[C] A certified decimal exponent would require a quantitative classical seed
and explicit control of its conversion to $O/N$. Assigning a convenient small
number to an unspecified positive constant is invalid. The scalar parity
relaxation is already sharp; a stronger transfer needs additional information.

## Cross-area routes and their unresolved interfaces

The [critical-mass dossier](../context/2026-09-12-critical-mass-and-multiplicity-route.md)
also studies weighted Gram defects and high-degree short mollifiers. A local
weighted-block deduction is recorded, but no new asymptotic theorem is claimed
from it. The CFKL route still needs a suitable detected count, an arbitrary-degree
localized moment theorem, and a certified numerical seed. A table entry does not
discharge those requirements.

The [spectral dossier](../context/2026-09-12-spectral-optimization-alternatives.md)
retains negative spectral mass and proposes optimization witnesses. Near-line
pairs make their negative eigenvalues arbitrarily small, so counting negative
directions alone supplies no uniform extra gain. Proposed third-moment witnesses
lack the required unconditional short-interval arithmetic input.

The [alternative-reformulation dossier](../context/2026-09-12-alternative-rh-reformulations.md)
examines Nyman-Beurling approximation, Li/Weil positivity, spectral realizations,
and heat flow. Sparse-prime approximation has a known positive-distance
obstruction. A coupled approximation/tail objective is proposed with its exact
infinite-limit criterion; no finite optimizer has proved that limit. Finite
positivity and heat-flow limits cannot simply be extrapolated to all zeros.

These routes were source-reviewed and adversarially evaluated. They were not
declared or run as additional computational experiments and are not discoveries
establishing RH. Their rejected shortcuts remain documented.

## Effective height and uniformity

[C] A practical threshold $T_0(\theta)$ would require explicit versions of the
imported analytic estimates and controlled smoothing constants. The existing
argument fixes a test function, sends $T\to\infty$, and only then changes its
bandwidth and cutoff. It does not permit those choices to depend on $T$ for
free.

The [Wang transfer audit](../context/2026-09-12-wang-transfer-audit.md) gives
the normalized fixed-test error

$$O_f\!\left(\frac1{\log T}
+T^{\lambda-\theta}\log T\right),\qquad\lambda<\theta.$$

The subscript $f$ matters: a sequence of narrower transition layers can make
the hidden constant large. An effective-height experiment must derive that
dependence before combining numerical cutoffs with finite-height claims.
Verification of many initial zeros would remain a separate computational
statement and would not justify uniform control of later zeros.

## Formalize the exact finite transfer

[C] A bounded formal target is the finite selfadjoint construction and the
two strengthened inequalities

$$s\ge2N-Q+D(G),\qquad
D_Z\ge\frac{3N-Q+D(G)}2.$$

This would connect the explicit remainder inertia argument to an existing
formal finite-multiset framework. A useful development must keep the square
$K(z-w)^2$ at complex arguments, rather than silently replacing it by an
absolute square. It must also allow repeated zero multiplicities and singular
Gram matrices.

Such a finite formalization is narrower than a full analytic proof. The
[formalization audit](../context/2026-09-12-formalization-audit.md) already
distinguishes Axiom's explicit analytic assumptions, Anthropic's broader
current source, default-library CI, and comparator replay. A future release
must identify precisely which theorem statements, toolchain, source head,
and verification command were checked.

## Directions rejected as new discoveries

| Proposed route | Reason it cannot currently support novelty |
|---|---|
| Reoptimize the single cosine density | The Montgomery-Taylor extremal problem and broader bandlimited optimum are already solved. |
| Certify more digits of $C_0,C_1,C_2$ | Arithmetic reproduction does not improve the theorem. |
| Introduce a free coefficient in the multiplicity block inequality | Anthropic's pinned `RankTraceMult.lean` already proves the arbitrary-parameter result, with abstract sharpness in `TightMult.lean`. |
| Claim the additive-root obstruction itself | It occurs in the inspected Ainta line of work. |
| Transfer a higher conditional pair-correlation constant unconditionally | The missing analytic hypothesis does not follow from finite optimization. |
| Infer the distinct bound from a naive simple-zero count inequality | Higher multiplicities invalidate that heuristic; the valid companion uses the stronger signed-operator inequality. |
| Treat a DOI or a high-precision optimizer as analytic validation | Neither proves an asserted moment identity or transport estimate. |

The exact derivations and citations are in [Chapter 2](02-known-results.md)
and the [successor dossier](../context/2026-09-12-original-and-successor-review.md).
The Yang-Yang 79.62 percent claim remains quarantined pending resolution of
its analytic transport and truncation objections. It is not a baseline that
this program has independently validated.

## Priority and review

The live search cutoff is 2026-09-12. Searches included the exact Wang arXiv
identifier, short intervals with stability, simple zeros with Gram methods,
and the direct Ainta/trmdy successor sources. No matching short-interval
strict-improvement theorem was located. This is positive evidence for a
candidate contribution, not proof that no earlier or concurrent result exists.

The most useful external review would challenge the actual interfaces: the
unweighted analytic pair sum, signed finite operator, inertia count, trace
pinching, span normalization, and order of limits. Finding a defect in one of
those steps would affect the theorem. Improving the conservative numerical
constant would affect the example without invalidating the analytic proof
of a positive gain.

The [published preprint](https://zenodo.org/records/22727389) provides versioned
dissemination. It does not replace independent mathematical acceptance. Any
later correction should preserve the original experiment artifacts and state
whether it changes the theorem, numerical example, attribution, or release
metadata.

[Previous: experiments](04-experiments.md) | [Return to overview](README.md)
