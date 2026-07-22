# EXP-043 - Verdict: CONFIRMED; the B = 16 core IS a staircase transport; full attacks are block-cheap (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`. Literature input: the 2026-07-22
literature-pass dossier (GGV J. Algebra 471 (2017) B = 16 data).

## Findings

1. **GGV structure verified [MV].** R0 = x(xy^4 - lambda_0)^3 is (4,-1)-homogeneous of
   weight 4 with collinear x-anchored support {(1,0), (2,4), (3,8), (4,12)};
   R1 = y(xy^2 - lambda_1) is (-2,1)-homogeneous; R0-power pairs are Jacobian-dependent.
2. **The x^m-anchored edge operator [MV].** New closed formula, verified identically in
   symbolic edge coefficients: J(x^m phi(z), x^a y^b) = x^{m+a-1} y^{b-1}
   [b m phi + (b k - a l) z phi'] for z = x^k y^l. Theorem 3's operator is the m = 1
   case; the whole GGV leading form R0^m = x^m (z - lambda_0)^{3m} has exactly this
   shape.
3. **The constant is unreachable from the edge for m >= 2 [MV].** On the grid, the only
   constant-reaching case is m = 1 with g = y (term -lambda_0^3). For every standard
   B = 16 pair (m >= 2), the Keller constant CANNOT be manufactured on the R0^m edge:
   it must travel the lower Newton boundary. THE B = 16 PROBLEM IS FORMALLY A STAIRCASE
   TRANSPORT PROBLEM, the exact object EXP-037/042 instrumented.
4. **Our theorems bite the shape [MV].** The pure m = 1 shape (normalized) has x as a
   Newton vertex and is excluded by Theorem 4 (window replication EMPTY); swallowed
   variants with x^d fillers are EMPTY at window 8: the staircase territory extends to
   the B = 16 shape family.
5. **Scoping, better than predicted [D/MV].** Exact block histograms: the (48, 64)
   attack under (4,-1) has 2142 window unknowns in 315 classes with LARGEST DIAGONAL
   BLOCK 13; the (72, 108) attack has 5992 unknowns in 535 classes with largest block
   22. The classwise transport replaces one monolithic solve by hundreds of solves of
   size <= 22: each block is trivial; the work is the coupling bookkeeping (off-diagonal
   injections and kernel tracking), i.e. exactly what the EXP-037 instrument automates.
   The prediction said "low hundreds"; the truth is low TENS.

## What this changes

- JCB-040 is not aspirational: the attack decomposes into tiny exact blocks. Next step:
  run the transport sweep on the F1-family shape ((m, n) = (3, 4), degrees (48, 64),
  the classical case 64) as the validation target (literature says empty: Moh/Heitmann),
  then the open B = 16 territory beyond max 150, then (72, 108).
- The x^m-anchored operator formula is the missing generalization of Theorem 3 for
  pairs without linear parts; it belongs in the planar-program manuscript.

## How could this be wrong?

- Part D windows are shallow (N = 8) relative to degree-16 shapes; they are replication
  probes, not new exclusions.
- The block histogram counts diagonal sizes only; off-diagonal coupling volume is not
  yet measured (the (48, 64) validation run will).
