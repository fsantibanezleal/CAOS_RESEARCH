# EXP-134 hypothesis - exact transverse graph section

Declared: 2026-08-01

## Question

Let `D_124(A,B,C,T)` be the 125-by-125 determinant of the accepted EXP-124
row section after adjoining `T = epsilon_(2,8)`. Does its restriction to the
EXP-123 exceptional graph remain exactly independent of `T` in characteristic
zero?

Equivalently, with `X=A^3`, `Y=A^2 C`, and

`G(X,B,Y) = R(X,B) + Y S(X,B)`,

does the `T`-dependent part of the invariant numerator of `D_124` lie in the
principal ideal `(G)`? A positive answer retains the exact EXP-124 residual
divisor `F3*F6*F7` unchanged and converts the first transverse graph step from
a new elimination problem into an exact divisibility certificate.

## Premise and route gate

- EXP-124 proves `D_124(A,B,C,0) = k A^90 N(A^3,B)` for a nonzero rational
  constant `k` and `N=F3*F6*F7`.
- EXP-133 observes degree zero in `T` on four graph controls over two primes,
  but this does not prove a characteristic-zero identity.
- Direct normalization on the graph is invalid because the EXP-123 defining
  section is singular there. The accepted EXP-124 section is normalized at
  the rational anchor `(A,B,C,T)=(1,0,0,0)` and reconstructed through joint
  SCC blocks before graph reduction.
- Polynomial-matrix Smith or Popov form remains a conditional later lens. No
  structured-divisor hypothesis has been proved for this matrix, so the exact
  Fitting/divisibility calculation is decisive here.

## Falsifiable predictions

1. Adding the `(2,8)` direction to the exact EXP-124 normalized operators
   leaves the largest joint SCC at most 45.
2. The determinant is at most affine in `T` after invariant reconstruction.
3. Every positive `T` coefficient reduces to zero modulo
   `G=R+YS` in `QQ[X,B,Y]`.
4. The `T=0` coefficient reproduces the accepted EXP-124 invariant numerator
   and its `F3*F6*F7` factorization.

Prediction 3 is the decision. Predictions 1, 2, and 4 are cost and regression
controls.

## Exact controls

- Rebuild the complete 302-row augmented matrix and both `(2,9)` and `(2,8)`
  directions from the bracket equations.
- Load the EXP-124 row basis and anchor from accepted artifacts and record
  their SHA-256 hashes.
- Reconstruct determinants over `QQ`; modular values may be used only as
  independent controls, never as the proof.
- Verify the reconstructed full determinant against direct 125-by-125
  determinants at at least four rational off-graph controls, including
  nonzero `T`.
- Verify the graph reduction both by exact polynomial remainder and by direct
  rational substitutions at controls with `A*S != 0`.

## Budget and kill criteria

- Smoke gate: 30 seconds to build matrices, invert the anchor, and report SCCs.
- Exact worker gate: 300 seconds; total gate: 420 seconds.
- Work componentwise and checkpoint after every exact block.
- Stop before a block expansion if its joint SCC exceeds 45, or if any single
  exact block exceeds 240 seconds. Persist the obstruction and redirect to
  coefficient interpolation with an explicit degree bound.
- Do not interpolate an identity without a proved degree bound.

## Interpretation

If all positive `T` coefficients are divisible by `G`, EXP-124 supplies an
exactly unchanged first chart on the transverse rational graph. This does not
cover the residual curves; EXP-129 transverse lifts remain necessary. If the
divisibility fails, persist the exact residual coefficient and select row
bases directly on its intersection with `F3*F6*F7`.

No outcome closes the complete rational graph by itself, the finite base
locus, the `A!=0,d=1` sector, the transverse `d=0` quotient, the
five-coefficient restriction, the 24-parameter core, `(72,108)`, the planar
degree floor, or JC(2).

## Exact redirects

Attempt 001 reached the gate on the size-33 ambient determinant over
`QQ[A,B,C,T]`. Attempt 002 substituted the rational graph first, but the
cleared size-33 determinant over `QQ[A,B,T]` also reached the gate. Neither
attempt produced a coefficient identity.

The accepted third route uses an exact degree bound rather than a broader
expansion. On the size-33 block the normalized `(2,8)` operator has rank 7;
all 86 singleton blocks have zero transverse diagonal. Therefore the complete
determinant has degree at most 7 in `T`. Exact equality with the `T=0`
determinant at the eight values `T=0,...,7` proves ambient `T`-inertness by
the root bound. The degree bound is proved by rank, so this is exact
evaluation, not assumption-based interpolation.
