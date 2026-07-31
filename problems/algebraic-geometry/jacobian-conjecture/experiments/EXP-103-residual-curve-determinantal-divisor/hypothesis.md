# EXP-103: Determinantal divisor on the normalized residual curve

## Question

Does the full augmented GGHV matrix retain rank \(125\) at every point of the
normalized residual curve

\[
s=8u^7,\qquad t=8u^2+u^{-7},\qquad u\ne0?
\]

An affirmative result closes the complete two-parameter slice left open by
EXP-101 and EXP-102. It does not close the other 49 coefficient directions.

## Exact reformulation

Delete the structural constant-\(Q\) zero column from the augmented matrix.
The result has 125 columns. After multiplying every row by \(u^7\), its entries
are polynomials with exponents contained in

\[
\{0,7,9,14\}.
\]

The slice is inconsistency-certified for every \(u\ne0\) exactly when the gcd
of all \(125\)-minors has no nonzero root.

## Method

1. Reconstruct the full 289-by-125 polynomial matrix
   \[
   B(u)=A_t+u^7A_0+8u^9A_t+8u^{14}A_s.
   \]
2. Start with EXP-102's row chart and add pivot-row charts selected at exact
   integer values of \(u\).
3. For each chart, evaluate its determinant at a power-of-two root-of-unity
   grid over an NTT prime and invert the transform. This recovers the complete
   determinant polynomial modulo that prime without dense symbolic expansion.
4. Compute exact minimum- and maximum-degree assignment bounds from the entry
   supports. Accept a chart only if the recovered endpoint coefficients at
   both bounds are nonzero. The assignment bounds then prove that reduction
   modulo \(p\) preserved both endpoint degrees.
5. Divide only by the chart's proved exact power of \(u\), which is a unit on
   \(u\ne0\), and compute the gcd of the normalized chart determinants.
6. Stop successfully when the gcd is \(1\). Repeat the chart set at a second
   NTT prime as an adversarial implementation control.

## Why a modular gcd can prove the characteristic-zero statement

Let \(f_i\in\mathbb Z[u]\) be the selected minors after their proved exact
monomial valuations are removed. Their constant and leading coefficients are
nonzero modulo \(p\). Hence any nonconstant common divisor over
\(\mathbb Q[u]\) would reduce to a nonconstant, non-monomial common divisor
modulo \(p\). Therefore a modular gcd equal to \(1\) proves that the exact gcd
of the selected minors is \(1\), and a fortiori that the gcd of all maximal
minors is \(1\).

If the modular gcd is nonconstant, the experiment is inconclusive until the
factor is reconstructed or killed by another exact chart. A modular rank probe
alone is never treated as curve coverage.

## Falsifiable predictions

1. EXP-102's chart reconstructs with a nonzero determinant at \(u=1\).
2. Every accepted determinant attains its combinatorial endpoint bounds.
3. Two or a small number of independently selected row charts have normalized
   gcd \(1\).
4. A second NTT prime reproduces the gcd-one decision and endpoint gates.

Failure of prediction 2 invalidates the proof shortcut for that chart.
Failure of prediction 3 exposes an explicit residual polynomial factor for
the next rank-specialization experiment.

## Controls

- Direct determinant evaluations at \(u=1,2,-1\) must agree with the recovered
  polynomial.
- NTT forward/backward round trips are tested on a fixed control polynomial.
- Selected row sets must have 125 distinct rows and include the same 125
  nonstructural columns.
- The two primes use independent roots of unity.
- The persisted artifact records row labels, endpoint bounds and
  coefficients, determinant hashes, gcd degrees, and direct checks.

## Budget and stop condition

CPU only. Five-minute budget per prime, with progress emitted after every 256
determinants. Stop after four distinct row charts if the gcd remains
nonconstant. Checkpoint after every completed chart. No probabilistic sampling
can replace the endpoint and gcd gates.

Declared 2026-07-26 before creating or running `run.py`.
