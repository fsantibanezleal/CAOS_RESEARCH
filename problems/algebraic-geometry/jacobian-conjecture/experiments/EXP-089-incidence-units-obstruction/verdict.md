# EXP-089 - Verdict: the incidence mechanism CANNOT produce a planar counterexample

**Status: DECIDED [MV]. The exact structure of the 2026 counterexample is
excluded in dimension 2.**

## Results (artifacts/output-2026-07-24.txt)
1. [MV] In dim 2 (L, Q both linear), the two normalizations {Res(L,Q)=1,
   [LQ]_{TS}=1} force x*delta=1 and beta*gamma=0: the source is REDUCIBLE (two
   components, beta=0 and gamma=0), hence not irreducible, hence NOT A^2.
2. [MV] Independently, in the finite-root chart X_2 = A^2 minus the discriminant
   hyperbola {2 c2 zeta + 1 = 0}; the discriminant (2 c2 zeta + 1) is a
   nonconstant UNIT on X_2, but O(A^2)^* = C^* (only constants). So X_2 is not
   isomorphic to A^2 - by the simplest possible invariant, units.
3. [D] Contrast: in dim 3 the identical construction gives a smooth irreducible
   X_3 ~ A^3 (weights (1,-1,-2), unimodular semigroup, EXP-088). The
   discriminant-complement is again affine space in dim 3 but provably NOT in
   dim 2.

## Meaning
The 2026 counterexample IS the incidence/root-selection map pi|X_H, and it
produces a Keller counterexample precisely because X_3 ~ A^3 (Tao-ChatGPT
derivation: observations (a) local injectivity from coprimality+resultant
weights, (b) noninjectivity from multiple root choices, (c) X_H ~ A^n the only
dimension-specific miracle). We prove (c) FAILS in dim 2: X_2 is reducible / has
nonconstant units. Therefore this entire construction - the only known
mechanism for a constant-Jacobian noninvertible polynomial map - CANNOT yield a
planar counterexample.

This is a clean, complete exclusion of the incidence-type counterexample class
for JC(2). It is independent of, and consistent with, our published 2D
G_m-equivariant rigidity theorem (foundational manuscript, EXP-010: every
G_m-equivariant planar Keller map is linear). Two different invariants (the
equivariant rigidity; the units of the discriminant complement) both forbid the
planar analog.

## Honest scope
This excludes the incidence/multiplication/root-selection class - the structure
of every known counterexample. It does NOT prove JC(2): a planar counterexample
of some entirely different (unknown) structure is not ruled out. But it removes
the single mechanism that actually produced the 2026 result, with a one-line
invariant proof, and explains structurally why dimension 2 differs.
