# EXP-039 - Verdict: CONFIRMED; the (3, n) column closes (2026-07-22). JCB-021 done

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **The top force, proved by elimination + orbits [MV].** For generic P_3, the linear map
   Q_4 -> J(P_3, Q_4) is 6 x 5; all 5 x 5 minors vanish on the cube parametrization
   (s x + t y)^3, every minor lies in the Hessian-covariant ideal, and the completeness
   direction is closed by GL2-equivariance (J(f o A, g o A) = det(A) J(f, g) o A, verified
   identically) plus the 3-orbit classification of nonzero binary cubics: both non-cube
   representatives (x^2 y and x y (x + y)) have FULL rank 5. Rank drops EXACTLY on cubes:
   a bidegree-(3, 4) pair forces P_3 = c ell^3, the precise analog of the (2, n)
   discriminant-square ideal. An instrument note recorded honestly: direct radical
   membership of the Hessian generators in the minors ideal was NOT reached at powers
   <= 8 (grevlex Groebner); the orbit argument replaced it soundly and more cheaply.
2. **The cube stratum completes and inverts [MV].** 64 samples of P = x + y^3 + P_2:
   exactly 4 consistent at exact bidegree (3, <= 4), all 4 Keller-verified and inverted
   with explicit polynomial inverses via lex Groebner extraction; the consistent set is
   precisely the triangular slice (P_2 free of x), matching the vertex dichotomy.
3. **Non-cube emptiness replications [MV].** x + x^2 y, x + x^3 + y^3, x + x^2 y - x y^2:
   EMPTY at (3, <= 4), (3, <= 5), (3, <= 7): nine window certificates.
4. **Coverage closure [D].** gcd(3, n) is 1 or 3 for every n: Magnus 1954 covers gcd 1,
   Appelgate-Onishi 1985 / Nagata covers gcd 3 (prime), and (3, 3) is also machine-closed
   (EXP-022). The whole (3, n) column is classically settled; the machine's contribution
   at (3, 4) is the explicit constructive loop (consistency variety + inverses), stated
   as replication, per the EXP-025 recalibration discipline.

## What this changes

- JCB-021 CLOSES: the queued staged (3, 4) elimination is replaced by the cheaper and
  complete top-force argument; remaining (3, n) strata need no machine work beyond
  replication value.
- The machine loop's pattern at (3, 4) (top form forced to a perfect power, then the
  stratum inverts) is the third instance (after (2, 3)-(2, 5) and (3, 3)) of the same
  shape, consistent with the leading-form cascade (EXP-013).

## How could this be wrong?

- Part B samples the cube stratum on a 64-point rational grid, not all parameters; the
  triangular-slice characterization at (3, 4) is sample-level (the all-parameter
  statement follows from Magnus classically, not from this run).
- The orbit argument uses the standard fact that a nonzero binary cubic is GL2-equivalent
  to x^3, x^2 y or x y (x + y); this classical fact is assumed, not machine-derived.
