# EXP-108: Residual-fiber third chart

## Question

Does a third 125-row maximal minor eliminate all twelve geometric points left
by the first two EXP-107 charts?

## Exact modular target

EXP-107 shows that the second determinant is independent of \(y\) and has
support

\[
G(z)=(8z+1)^{14}.
\]

At its only geometric zero \(z=-1/8\), the first determinant becomes a
squarefree degree-12 polynomial \(Q(y)\) modulo \(998244353\). Therefore a
candidate third determinant \(H(z,y)\) closes the modular geometric fiber
exactly when

\[
\gcd\bigl(Q(y),H(-1/8,y)\bigr)=1.
\]

This fixed-fiber test needs only a 64-point univariate NTT per candidate chart,
not another full bivariate reconstruction.

## Pilot

1. Rebuild the full 289-by-125 augmented matrix at \(z=-1/8\).
2. Select 125 pivot rows at deterministic base-field probe values of \(y\),
   varying the row order if needed.
3. Reconstruct each selected determinant \(H(-1/8,y)\) on a 64-point NTT
   grid and verify it at independent off-grid values.
4. Stop at the first chart with \(\gcd(Q,H)=1\). If none appears within four
   distinct charts, persist the surviving factors and redirect to
   factor-local row selection.
5. Repeat a successful cover at independent primes and lift an exact
   certificate before making a characteristic-zero claim.

## Decision boundary

A gcd-one fiber result proves that the three modular chart polynomials have no
common geometric point over the pilot field's algebraic closure. It does not
by itself close the characteristic-zero slice and has no direct JC(2)
consequence.

Declared 2026-07-26 after EXP-107 and before implementation.
