# EXP-002 - Reverse-engineer the structure of F, exactly and independently

- **Question.** What internal structure makes the counterexample F work? Specifically: does F have
  (H1) a weighted scaling symmetry, (H2) z-linearity with a structured coefficient vector, (H3) an
  exact reduction to weight-0 invariant coordinates, and (H4) a one-variable polynomial identity
  governing its fibers (so that generic fibers have exactly 3 points)?
- **Motivation.** A public secondary analysis (jacobianfun.org, July 2026) claims such a
  structure (weights (1, -1, -2), invariants v = xy, t = x^2 z, seed p(w) = 2w - 3w^2, fiber
  cubic). Our record must not rest on an unverified web page: this experiment derives the
  structure from F itself, in exact arithmetic, and states precisely what we proved. It also
  closes EXP-001's residual single-route risk on det JF by re-deriving it structurally.
- **Falsifiable predictions.**
  - (H1) F(lambda x, y/lambda, z/lambda^2) = (A/lambda^2, B/lambda, lambda C) as an identity in
    (x, y, z, lambda), where (A, B, C) = F(x, y, z). Fails if the identity has a nonzero residual.
  - (H2) each component of F is degree <= 1 in z; the z-coefficient vector is
    (u^3, 3x u^2, -x^3), u = 1 + xy.
  - (H3) x^2 P, x Q, R/x are polynomials in (v, t) alone (v = xy, t = x^2 z); explicitly
    computable.
  - (H4) there exist weight-0 combinations of the OUTPUTS, and a polynomial w-coordinate on the
    source, such that a univariate identity Phi(w) = linear-in-w expression in the outputs holds
    identically, with deg Phi = 3; the identity must reproduce the 3-point fiber of EXP-001 when
    specialized to the target (-1/4, 0, 0).
- **Method.** sympy over QQ: polynomial identity checks (H1, H2); rewriting in (v, t) via exact
  substitution x = x, y = v/x, z = t/x^2 and cancellation checks (H3); for (H4), an undetermined-
  coefficients search for w as a polynomial in (v, t) of low bidegree satisfying
  Phi(w) = w * (QR)/4 - (P R^2)/4 with Phi(w) = w^2 - w^3, run as an exact linear/polynomial
  solve; if that ansatz fails, widen the ansatz (document every widening).
- **Success criterion.** H1-H3 verified exactly; H4 produces an explicit w(v, t) and an identity
  with zero residual, consistent with EXP-001's fiber.
- **Failure criterion.** Any H fails after honest ansatz widening; then the secondary analysis is
  (at least partially) wrong and our record says so.

Declared 2026-07-20 before the run.
