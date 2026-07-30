# EXP-115 - Weighted residual component gate

## Question

Does the rank-deficient locus contain any whole irreducible component of
EXP-114's weighted \(T_B\) residual, or do alternative complete-row minors
remove the generic point of every component?

Write
\[
a=\varepsilon_{(0,1)},\qquad
b=\varepsilon_{(0,5)},\qquad
d=1+\varepsilon_{(1,0)}.
\]
EXP-114 gives a selected 36-core determinant proportional to
\[
G_{54}(a,b,d)H_{63}(a,b,d).
\]

## Motivation

A full chart cover is not yet affordable in the 24-parameter core. The
strongest next gate is instead component-theoretic: determine whether any
factor of the selected minor is a component on which the complete 302-row
augmented matrix remains rank-deficient.

If every residual component has an alternative nonzero minor at one exact
point, then no component is trapped in the rank-deficient locus. The remaining
exceptional set has strictly higher codimension and can be targeted by
resultants or residual ideals rather than another full-family determinant.

## Exact preflight

On the weighted open chart \(d\ne0\), set
\[
a=A u^7,\qquad b=B u^3,\qquad d=u^9.
\]
The selected factors become powers of \(u\) times
\(G_{54}(A,B,1)\) and \(H_{63}(A,B,1)\). Both depend on \(A\) only through
\(X=A^3\). The preflight will factor them exactly over
\(\mathbb Q[X,B]\).

On the boundary \(d=0\), the selected determinant has the reduced component
support
\[
A=0,\qquad B=0,\qquad
30720000A^3+48828125B^7=0.
\]
The last component has the rational parametrization
\[
A=-9t^7,\qquad B=\frac{12}{5}t^3
\]
after rescaling \(t\); \(t=1\) supplies an exact control point.

## Premise dependencies

- [MV] EXP-111 supplies the complete 302-row, 125-column effective augmented
  system.
- [MV] EXP-112 supplies the deterministic pinned row basis and exact
  normalization.
- [MV] EXP-114 supplies \(G_{54}\), \(H_{63}\), and weights \((7,3,9)\).
- [D] If an irreducible factor \(F\in\mathbb Q[A,B]\) divided every
  alternative minor, then after reduction at a good prime every zero of
  \(F\bmod p\) would annihilate every reduced minor. A certified point with
  \(F=0\) and one nonzero alternative minor disproves that divisibility.

## Predictions

1. [D] \(G_{54}(A,B,1)\) is irreducible over \(\mathbb Q[A,B]\).
2. [D] \(H_{63}(A,B,1)\), viewed in \(X=A^3\), splits into a linear and a
   quadratic factor over \(\mathbb Q[X,B]\).
3. [C] The complete augmented matrix has rank 125 at a good-prime point on
   each of the three weighted-open components, with the other factors
   nonzero.
4. [C] The complete matrix has exact rank 125 at a rational point on each of
   the three \(d=0\) boundary components.
5. [C] Each full-rank witness requires only a small row-basis transition from
   EXP-112's pinned chart.

## Method

1. Reconstruct the complete effective augmented system from EXP-112.
2. Factor the shifted \(d=1\) and \(d=0\) residuals exactly.
3. At a deterministic good prime, search points separately on the
   \(G\), \(H_{\mathrm{linear}}\), and \(H_{\mathrm{quadratic}}\) components.
   Require all non-target factors to be nonzero.
4. Compute exact finite-field row pivots for the full 302-by-125 matrix.
   Persist one alternative 125-row basis and its nonzero determinant per
   component.
5. Repeat over \(\mathbb Q\) at
   \[
   (A,B,d)=(0,1,0),\quad(1,0,0),\quad(-9,12/5,0)
   \]
   for the three boundary components.

## One-sidedness

- PASS proves that no displayed residual component is wholly contained in
  the rank-deficient locus of the complete augmented system.
- PASS does not cover the proper closed intersections left on those
  components.
- Modular witnesses are used only for exact non-divisibility at a good
  prime, not as numerical evidence for global rank constancy.
- Failure to find a witness at the declared prime is inconclusive and
  triggers another prime or an exact extension-field calculation.

## Adversarial validation

- The selected pinned minor must vanish at every witness.
- Every target factor must vanish and every declared non-target factor must
  be nonzero.
- Each persisted alternative basis must have a directly recomputed nonzero
  determinant in the same exact field.
- Boundary points and ranks are computed over \(\mathbb Q\), not modulo a
  prime.
- The pinned point remains a rank-125 positive control.

## Compute budget and kill criterion

CPU-only, two-minute budget. Stop after two good primes or 120 seconds. Do not
attempt bivariate symbolic determinants in this round. If a whole component
resists a rank-125 witness, promote it as the next exact extension-field
target rather than inferring rank deficiency.

Declared 2026-07-29 before implementation or run.
