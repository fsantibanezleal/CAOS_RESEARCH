# EXP-032 - The full-edge theorem: multiplication structure and the univariate kill

- **Question.** JCB-034 first half. What happens when the TOP EDGE itself carries several
  monomials? Design derivation (to certify): let z = x^k y^m (k, m >= 1) and
  E = x phi(z), phi(0) = 1, deg phi = g >= 1 (the general w-homogeneous edge anchored at
  the vertex x: it carries g + 1 lattice monomials). On the y-class ray
  g_s = x^{ks} y^{ms+1}, the operator is MULTIPLICATION:
  J(E, g_s) = [(ms + 1) phi(z) + k z phi'(z)] e_s, with e_t identified with z^t. The class
  equation becomes: find a polynomial f with m z phi f' + (phi + k z phi') f = 1; the top
  coefficient of the left side at degree D + g is (mD + kg + 1) phi_g c_D with every factor
  positive: c_D = 0, induction kills f, contradiction. THEOREM 3: E = x phi(z) is never the
  leading form of a Keller component; with the Theorem-2 machinery (kernels = powers of E;
  absorption; annihilation), P = x phi(z) + R (R lower-weight) is never a Keller component,
  at any degree.
- **Motivation.** This subsumes the weight-class theorem (phi = 1 + a z^g with only the top
  coefficient) and Theorem 2's leading forms, closes the same-edge half of the frontier in
  one stroke, and reduces the whole obstruction to a one-line univariate statement: the
  strongest simplification the program has found. The boundary stays honest: edges NOT
  anchored at x (quasi-triangular tops y^d) escape the shape and components live there.
- **Falsifiable predictions.**
  1. [MV] (Multiplication formula) For k, m in 1..3, g in 1..3 with SYMBOLIC phi
     coefficients, s <= 4: J(x phi(z), g_s) equals [(ms+1) phi + k z phi'] z^s times e_0,
     exactly.
  2. [MV] (Univariate kill) The truncated class systems (f of degree <= D <= 8) are
     inconsistent over QQ(phi coefficients) with the top coefficient inverted; the
     certificate pairing is a pure power of phi_g times a positive rational (grid of
     (k, m, g)).
  3. [MV] (Full windows, same-edge binomial and trinomial) P = x + b x^2 y + a x^3 y^2
     (edge g = 2) and P = x + b x^2 y + c x^3 y^2 + a x^4 y^3 (g = 3): full completion
     windows inconsistent at numeric samples INCLUDING perfect-square/cube phi (e.g.
     phi = (1 + z)^2: b = 2, a = 1): the factorization of phi does not rescue.
  4. [MV] (Certificates) Over QQ(a, b) at window <= 8 for the binomial edge: the pairing
     gcd vanishes only where the TOP coefficient a = 0 (pure a-power, b-free or
     b-involvement only through the edge-degeneration locus a = 0).
  5. [MV] (Kernels and tails) ker of J(E, .) on class jv equals E^j (j <= 2, binomial
     edge); adding lower-weight tails keeps full windows inconsistent; the quasi-triangular
     control stays consistent (the boundary is real).
- **Method.** sympy over QQ with symbolic edge coefficients; the certificate instrument;
  univariate class matrices. Caps 570 s.
- **Success criterion.** 1-5 verified; THEOREM 3 recorded with the univariate proof and the
  same honest labels as Theorems 1-2 (the tail-absorption step inherits Theorem 2's [D]
  annihilation gap; the leading-form kill is unconditional).
- **Failure criterion.** A phi with a consistent class system (a rescuing edge: analyze
  immediately: it would be a candidate leading form for genuine components of a new kind);
  a formula mismatch (back to the anatomy).

Declared 2026-07-22 before the run.
