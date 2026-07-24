# EXP-090 - Verdict: n-2 is THE invariant; n=3 unique; dim 2 fails at the root

**Status: DECIDED [MV]. A single invariant unifies the whole "why n=3" story.**

The resultant Res(L,Q) has weight n-2 = (deg Q - deg L) under the relative scaling
(L,Q) -> (lam L, lam^-1 Q). This one number controls everything:
- n=2: weight 0. The resultant is INVARIANT under the relative scaling the
  multiplication forgets, so it cannot rigidify the normalization; the incidence
  mechanism degenerates (X_2 reducible / G_m x A^1, never A^2). Dim 2 fails at the
  most basic level - before any Danielewski or units argument.
- n=3: weight 1. The resultant rigidifies AND the Danielewski core {xW = B-1} is
  LINEAR, so X_3 = A^3. The UNIQUE working dimension.
- n>=4: weight >=2. Rigidifies, but the core {x^{n-2}W = B^{n-2}-1} is nonlinear
  (n-2 boundary components, Cl rank ~ n-3), so X_n != A^n.

n-2 is simultaneously: (i) the resultant weight (etale/rigidify test), (ii) the
Danielewski core degree, (iii) the boundary-component count at x=0, (iv) the
residual-torus support count minus one. EXP-086/087/088/089 were all shadows of
this single invariant. n=3 is exceptional because n-2=1 is the unique value that
is both nonzero (rigidifies) and linear (=A^n). Dimension 2 (n-2=0) is excluded at
the root: the resultant is blind to the relative scaling.

This is the cleanest statement of why the 2026 mechanism lives in dimension 3 and
cannot reach the plane. It complements our G_m-equivariant rigidity theorem
(EXP-010): both forbid the planar analog, now from a one-parameter invariant.
