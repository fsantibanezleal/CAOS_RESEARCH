# EXP-002 - Verdict: CONFIRMED (2026-07-20)

All of H1-H4 verified exactly (`artifacts/output-2026-07-20.txt`), independently of the secondary
web analysis. What is now OUR verified ground:

1. **H1 scaling symmetry.** F(lambda x, y/lambda, z/lambda^2) = (P/lambda^2, Q/lambda, lambda R)
   identically: F is equivariant for the weight action (1, -1, -2) -> (-2, -1, 1).
2. **H2 z-linearity.** Each component is affine in z with coefficient vector (u^3, 3x u^2, -x^3),
   u = 1 + xy.
3. **H3 invariant reduction.** a1 = x^2 P, b1 = x Q, c1 = R/x are polynomials in v = xy,
   t = x^2 z alone; c1 = 2 - 3v - t; a1 = (v + 1)(t(v + 1)^2 + 3v^3 + 4v^2) after factoring.
4. **Structural determinant (new, ours).** With output invariants V' = QR, T' = P R^2, the reduced
   2-variable Jacobian satisfies the identity **J2 = det d(V', T')/d(v, t) = 2 c1^2**, and the
   skew-product chain rule gives det JF = -J2/c1^2 = -2. This re-derives EXP-001's determinant by
   an independent structural route (closing the single-route risk noted there), and isolates WHERE
   the Keller property lives: in a two-variable identity, not a three-variable miracle.
5. **H4 fiber cubic.** With w = u c1/2: Phi(w) = w^2 - w^3 satisfies
   Phi(w) = (w QR - P R^2)/4 identically. At the EXP-001 target the w-values of the three
   preimages are (1, 0, 0), exactly the roots (with multiplicity) of Phi(w) = 0.
6. **Generating identity (new, ours).** a1 = u b1/2 - u^2 + u^3 c1/2: the whole map is generated
   by the PAIR (b1, c1); the first component carries no independent information.

## Adversarial validation record

- Route 1 (independent re-derivation): the determinant is obtained both by direct 3x3 expansion
  (EXP-001) and via the reduced skew-product identity (this run); the fiber structure is obtained
  both by Groebner elimination (EXP-001) and by the w-cubic (this run). The pairs agree exactly.
- All checks are polynomial-identity checks over QQ with zero residual; no numerics anywhere.

## How could this be wrong?

- The chain-rule sign convention in the skew-product formula was verified as an identity (not
  derived and trusted), so orientation slips are excluded by the check itself.
- These results are specific to F; the general-seed statements are NOT yet established and are
  exactly EXP-003's subject.

## Consequences

- The generalization program has a concrete shape: construct maps from a seed pair (b1, c1) in
  the invariant plane subject to the reduced Keller identity J2 = const * c1^2; EXP-003 derives
  the constraint set for general seeds and attempts new explicit counterexamples with rational
  collisions via the reconstruction inverse (u = mkw/(V-tilde - k^2 w h(w)), then x = C/c1).
- For the 2D question: the mechanism's Keller condition is intrinsically 2-variable; what needs
  the third ambient dimension is the WEIGHTED LIFT (a negative-weight coordinate pair). EXP-004
  formalizes exactly this obstruction.
