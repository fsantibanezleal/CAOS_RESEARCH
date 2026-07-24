# EXP-088 - Verdict: n=3 is the unique incidence-affine dimension; dim 2 excluded from below

**Status: DECIDED (structural, all predictions [MV] except the [D] conclusion).**

Results (artifacts/output-2026-07-24.txt):
1. [MV] The 3D G_m-semigroup (weights 1,-1,-2) has unimodular basis (det 1):
   X_3 = A^3 has a clean TORIC explanation (not a coordinate accident).
2. [MV] The Danielewski core D_n = {x^{n-2}W = B^{n-2}-1} has n-2 boundary
   components: n=3 LINEAR (=> A^2 => X_3=A^3, unique), n>=4 has n-2 components
   (Cl(X_n) rank ~ n-3, excludes A^n), n=2 DEGENERATE (n-2=0: below the
   exceptional case).
3. [MV] The residual torus needs exactly 2 support points of H cap Delta:
   n=3 only. n=2: the small diagonal is a CONIC, tangent = 2p (Borel, the
   3D-excluded regime); n>=4: >=3 points, torus lost.
4. [D] CONCLUSION: the 2026 mechanism is exceptional to n=3, reaches all n>=3 by
   the classical reduction, but NOT n=2. Dimension 2 sits BELOW the exception on
   every axis (Borel regime; degenerate/toric-trivial core). No incidence-type
   planar counterexample; independently, any G_m-graded planar Keller map is
   linear by our published rigidity theorem (foundational ms, EXP-010).

## Connection to our program (important)
- NON-PROPERNESS: the conversation shows the counterexample's only obstruction is
  non-properness, with Jelonek set J(F) = the discriminant hypersurface V(D),
  D = -4 Disc(cubic); the map degenerates as x = 1/C'(zeta) -> infinity. This is
  EXACTLY our properness reformulation (JC(2) holds iff every planar Keller map
  has empty Jelonek set; EXP-014). The 3D counterexample has a nonempty Jelonek
  set BY the discriminant; the 2D question is whether a planar Keller map can.
- The A^2-fibration X_3 -> A^1 (topological C^3) is the recognition-of-affine-space
  route; in dim 2 recognition of A^2 is a THEOREM (Miyanishi-Sugie), so the 2D
  incidence surface is DECIDABLE.

## Next (declared)
- EXP-089: build the 2D incidence surface X_2 explicitly (conic in P^2, tangent
  line, ramification) and settle X_2 ~ A^2 by surface classification + the
  class-group discriminator; secure Miyanishi-Sugie primary source first.
