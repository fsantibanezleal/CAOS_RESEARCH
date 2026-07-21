# EXP-004 - Constructor v2 (potential form): the general seed family, ours

- **Question.** Is the corrected constructor (from EXP-003's failure analysis) correct and
  complete: does every admissible datum (p, k, q) yield a Keller counterexample on C^3, including
  seed degrees >= 3 and non-affine q, with explicit rational collisions?
- **Motivation.** EXP-003 refuted the v1 lift for deg p >= 3 and the failure analysis produced a
  potential form that makes the Keller property automatic; this is the generalization core of the
  program and is entirely our own derivation (no external source states it in this form).
- **The constructor (to be verified, stated precisely).** Data: a seed polynomial
  p(w) = sum_{i=1..d} p_i w^i with p(0) = 0, integral_0^1 p = 0, p(1) != 0, p'(1) != 2 p(1);
  a scale k != 0; a section polynomial q(v) with q(0) = k and
  q'(0) = beta := k (p(1) - p'(1)) / (p'(1) - 2 p(1)); arbitrary higher tail.
  Define Phi(w) = integral_0^w p, u = 1 + v, c1 = q(v) - t, w = u c1 / k, and
  b1 = k^2 p(w)/c1 + m with m = -k p(1) (a polynomial in (v, t)),
  a1 = u b1 / k - k^2 Phi(w) / c1^2 (a polynomial in (v, t)),
  F_{p,k,q} = (a1/x^2, b1/x, x c1) under v = xy, t = x^2 z.
- **Falsifiable predictions.**
  1. (General lemma, symbolic) For generic symbolic data of low degree, the skew-product identity
     det JF = -J2/c1^2 holds, and with the potential form J2 = m^2 c1^2 / k identically, so
     det JF = -m^2/k = -k p(1)^2, CONSTANT, for any q-tail.
  2. F (announced) is the instance p = 2w - 3w^2, k = 2, q = 2 - 3v.
  3. d = 3: p = w - 2w^3, k = 3 (so beta = -4, m = 3): a polynomial Keller map with det = -3 and
     generic fiber degree 4; explicit rational collision exists.
  4. d = 4: p = 8w - 12w^2 + 4w^3 - 5w^4, k = 14 (beta = -19, m = 70): det = -350, generic fiber
     degree 5; explicit rational collision exists.
  5. (Beyond the announced family) F's seed with q-tail v^2 (q = 2 - 3v + v^2, k = 2): still a
     Keller counterexample, det = -2, fiber degree 3; explicit rational collision exists. This
     instance lies OUTSIDE the shape of anything announced (different component degrees).
- **Method.** sympy over QQ; polynomiality checked by Laurent residue extraction; det computed
  directly in (x, y, z); fiber degree via the w-polynomial k^2 Phi(w) - (w Vt - Tt) at a random
  rational target with squarefreeness check; reconstruction verified modulo the fiber polynomial;
  collisions engineered by prescribing two rational w-roots and solving linearly for the target.
- **Success criterion.** Predictions 1-5 all verified exactly.
- **Failure criterion.** Any prediction fails; the verdict then localizes which step of the
  derivation is wrong.

Declared 2026-07-20 before the run.
