# EXP-007 - The asymptotic variety: where and how preimages escape

- **Question.** Compute exactly WHERE the announced map F (and the family) fails properness: the
  asymptotic variety A(F) (targets whose fibers are deficient because preimages escaped to
  infinity), and demonstrate an escape concretely with exact arithmetic.
- **Motivation.** JC-P2. EXP-002/004 identified non-properness as the mechanism; this experiment
  makes the locus explicit. Working hypothesis found while designing the run (to be verified as
  prediction 1): in the potential form, s = (BC - k^2 p(w))/m equals -W'(w)/m where
  W(w) = k^2 Phi(w) - w BC + A C^2 is the fiber polynomial; so an escape root (s(w0) = 0 with
  W(w0) = 0) is EXACTLY a multiple root of W: the asymptotic variety over C != 0 is the
  DISCRIMINANT locus of the fiber polynomial. Escapes happen precisely where two fiber sheets
  merge, and they merge at infinity.
- **Falsifiable predictions** (for F, seed 2w - 3w^2, k = 2, m = 2):
  1. W'(w) = k^2 p(w) - BC identically, hence s = -W'(w)/m: multiple fiber roots and escape
     roots coincide. Machine-check the identity.
  2. disc_w(W) is a nonconstant polynomial D(A, B, C); the engineered escape target
     (A, B, C) = (0, 1, 1) (built by imposing s(1/2) = 0) satisfies D = 0, and its exact fiber
     (lex Groebner) contains EXACTLY ONE point, which reconstruction predicts to be
     (2, -1/2, 9/8): two of the three sheets escaped.
  3. Over the plane C = 0 with generic rational (A, B): the exact fiber of F has EXACTLY ONE
     point, namely the flat-sheet point (0, B, A - 4B^2): the curved sheets escape; so
     {C = 0} lies in A(F).
  4. The collision target (-16, -16, 1) of EXP-004 has D != 0 and a full 3-point fiber (all
     finite): collisions are a generic phenomenon, not confined to the asymptotic locus.
  5. Family-wide: the same identity W' = k^2 p - BC holds for the P3 instance (seed w - 2w^3,
     k = 3), so the discriminant characterization is a family theorem, not an F accident.
- **Method.** sympy over QQ: polynomial identities; discriminant via sympy; fibers via lex
  Groebner with exact root extraction; reconstruction cross-check.
- **Success criterion.** Predictions 1-5 verified exactly.
- **Failure criterion.** Any fails; in particular if the (0, 1, 1) fiber has 3 points the
  discriminant characterization is wrong and the verdict must localize why.

Declared 2026-07-20 before the run.
