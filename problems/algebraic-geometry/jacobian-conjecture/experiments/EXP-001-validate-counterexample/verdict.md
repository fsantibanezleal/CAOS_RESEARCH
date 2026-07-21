# EXP-001 - Verdict: CONFIRMED (2026-07-20)

All checks pass in exact rational arithmetic (`artifacts/output-2026-07-20.txt`):

1. det JF = -2 identically (fully expanded symbolic determinant).
2. F(0, 0, -1/4) = F(1, -3/2, 13/2) = F(-1, 3/2, 13/2) = (-1/4, 0, 0); the three preimages are
   pairwise distinct. Hence F is a Keller map that is not injective: the Jacobian conjecture is
   FALSE for N = 3, and (adding dummy coordinates) for every N >= 3.
3. Beyond the announcement: the lex Groebner basis of the fiber ideal shows the fiber over
   (-1/4, 0, 0) is EXACTLY those three points. Eliminant in z: (2z - 13)(4z + 1)/8. On the fiber:
   3x + 2y = 0 and 12 y^2 = 4z + 1.

## Adversarial validation record

- Route 1 (exact re-derivation): the determinant was computed by sympy's default Berkowitz/
  cofactor path on the expanded matrix AND cross-checked by expanding the full symbolic
  determinant to a polynomial in (x, y, z) whose nonconstant coefficients all cancel; the fiber
  was computed by Groebner elimination, independent of the pointwise substitution check.
- Route 4 (stress): substitution used exact Rationals (no floats anywhere); distinctness asserted
  on exact tuples.
- Follow-up EXP-002 re-verifies the determinant along an independent structural route
  (block/weighted decomposition), closing the remaining "same-library" residual risk.

## How could this be wrong?

- Single-library risk (sympy) remains until EXP-002's independent structural derivation; the
  computation is however short enough to check by hand for the substitution part.
- Attribution details (who found what, exact announcement wording) are journalistic, not
  mathematical; they do not affect this verdict.

## Consequences

- The program's ground truth is established: JC(N >= 3) is false; JC(2) is open. All further work
  builds on this map F as the founding object.
