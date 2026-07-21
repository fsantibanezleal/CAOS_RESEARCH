# EXP-005 - The 2D obstruction: where the mechanism needs dimension 3

- **Question.** Why does the counterexample mechanism (weighted skew-product + seed family,
  EXP-002/EXP-004) require ambient dimension >= 3, and can any part of it transplant to N = 2?
- **Motivation.** JC(2) is open; Felipe's directive targets what transfers. The mechanism uses a
  Gm-action with TWO independent weight-0 invariants (v = xy, t = x^2 z); in C^2 a nontrivial
  Gm-action has only ONE independent invariant. This experiment makes the obstruction exact and
  probes the 2D boundary honestly.
- **Derived reduction (ours, to be machine-verified).** A Gm-equivariant polynomial map of C^2
  with weights (1, -a), a >= 1, has components P = x^{b1} f(v), Q = x^{b2} g(v), v = x^a y, and
  det JF = x^{b1 + b2 + a - 1} (b1 f g' - b2 f' g). Keller forces
  b1 + b2 = 1 - a and b1 f g' - b2 f' g = const != 0.
- **Falsifiable predictions.**
  1. (Determinant reduction) The displayed det identity holds symbolically for generic f, g.
  2. (2D equivariant null result) For a in {1, 2}, b1 in a small window, and deg f, deg g <= 3,
     EVERY solution of the Keller condition yields an INJECTIVE map (fiber count 1 at random
     rational targets, checked by Groebner). No 2D counterexample arises in this class. (If one
     arises, that is a refutation of JC(2) and the run will say so; we predict it does not.)
  3. (Collapse without t) In the 3D reduced system, forcing t-independence (s = q(v) instead of
     the free coordinate s = q(v) - t) makes the reduced Jacobian J2 vanish identically, so no
     Keller map arises: the second invariant is LOAD-BEARING. Verified on the P2 and P3 seeds.
  4. (No Keller slices) No coordinate 2x2 slice of the announced F (fixing one input variable at
     a generic rational value and picking two output components) has constant nonzero Jacobian
     determinant.
- **Method.** sympy over QQ: symbolic identity for 1; undetermined-coefficient solves + Groebner
  fiber counts for 2; direct reduced-Jacobian computation for 3; exhaustive slice determinant
  scan for 4.
- **Success criterion.** Predictions 1, 3, 4 verified; prediction 2 resolved either way (the
  expected outcome is the null result; a counterexample outcome would be a major positive).
- **Failure criterion.** Prediction 1 or 3 fails: our structural reading of the mechanism is
  wrong and must be revised.

Declared 2026-07-20 before the run.
