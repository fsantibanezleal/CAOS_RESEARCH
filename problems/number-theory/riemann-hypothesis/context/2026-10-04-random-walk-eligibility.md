# Random-walk and entropy viewpoint: eligibility review

Reviewed 2026-10-04. Supporting source review for RH-F4 / issue #360;
no new experiment, moment estimate, onset or manuscript claim.

Primary source: Ali Mohammadi, *Bilinear Kloosterman sums over small boxes
and uniformity of a random walk*, [arXiv:2608.01203v1](https://arxiv.org/abs/2608.01203v1),
submitted 2 August 2026, CC BY 4.0. The versioned PDF is preserved in the
external source cache and bound by `source-manifest-random-walk-20261004.json`.
This review inspected the theorem hypotheses and the Fourier/mixing proof;
it does not independently validate the entire bilinear estimate.

Theorem 1 concerns bounded separated weights over coordinate boxes in a
finite field, with product cardinality at least `q^(1/2+epsilon)` and phase
`axy + b/(xy)`, `b != 0`. The gain is expressed in the characteristic `p`.
Theorems 2 and 3 concern independent, uniform box increments. Fourier
factorization yields exponential decay for their additive convolution;
Parseval then bounds chi-square divergence and entropy loss. Full-distribution
mixing requires more steps than a single linear projection. These statements
are attributed source results, not CAOS discoveries.

## Conversion obligations for the current signed moment

The following are deductions from comparing those hypotheses with EXP-024's
interface; no estimate for our moment is asserted.

1. `F_(p^n)` is not `Z/p^n Z` when `n > 1`. Prime-power conductors in the
   composite character reduction cannot be relabelled as finite fields.
   A ring-level estimate, or a justified reduction to prime conductors with
   controlled bad factors, is required.
2. Even squarefree CRT factorization of the phase does not factor global
   integer interval cutoffs or signed mollifier coefficients into independent
   local box measures. Any decomposition must retain its coefficient norm,
   truncation loss and all conductor/gcd factors.
3. The weighted bilinear theorem permits separated complex weights, so their
   signs alone do not exclude that theorem. The random-walk entropy corollary,
   however, uses probability measures and independent increments. Our signed
   family has not been identified with such a convolution.
4. Replacing a one-step distribution by its `k`-fold convolution changes the
   quantity being estimated. The identity `hat(mu^(*k)) = hat(mu)^k` cannot
   be used to multiply cancellation in the original sum without an exact
   factorization or a proved comparison inequality. Introducing random
   increments numerically would therefore provide no analytic certificate.
5. A prime-modulus component would still need matching phase, support sizes,
   separated coefficient bounds and uniformity in height, shifts and moduli.
   No explicit height threshold follows from the asymptotic source statement.

## Decision

Do not import a mixing gain or start a synthetic random-walk simulation as
an RH-F4 experiment. The useful next analytical gate is to derive the actual
prime-conductor component of EXP-024's signed average and test whether its
phase and coefficient tensor admit a bounded-norm box decomposition. Failure
of that decomposition is an obstruction to this route; success would justify
a separately declared estimate with its complete accumulated losses. The
existing non-abelian and subdyadic routes remain separate possibilities.
No additional manuscript or companion version is warranted by this review.
