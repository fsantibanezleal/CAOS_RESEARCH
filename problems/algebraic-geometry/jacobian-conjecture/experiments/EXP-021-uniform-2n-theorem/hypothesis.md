# EXP-021 - The uniform (2, n) theorem: the whole column at once

- **Question.** Close JCB-025: prove, uniformly in n, that every normalized planar Keller map
  whose first component has degree 2 is invertible, with one explicit inverse formula.
- **Motivation.** EXP-019/020 established: the consistency variety forces P = x + ell^2 with
  ell = alpha x + beta y (rank-1 top), and n = 3, 4, 5 each closed with explicit inverses.
  Design analysis (to certify): in shear coordinates (u1, u2) = (ell, x) the Keller condition
  becomes the LINEAR first-order PDE 2 u1 Qt_{u2} - Qt_{u1} = c, whose characteristic
  invariant is exactly P = u2 + u1^2. Hence the COMPLETE solution space is
  Q = ell/beta + H(P), H an arbitrary polynomial (the free tails B_11, B_15 seen at n = 4, 5
  are H's coefficients), and the inverse is one closed formula:
  ell = beta (q - H(p)), x = p - ell^2, y = (ell - alpha x)/beta.
- **Falsifiable predictions.**
  1. [MV] (Sufficiency, generic) For generic symbolic H of degree up to 4 (so deg Q up to 8):
     J(x + ell^2, ell/beta + H(x + ell^2)) = 1 identically over QQ(alpha, beta, H-coeffs).
  2. [MV] (Completeness, per degree) For n = 3..8 and sampled (alpha, beta) (3 rational
     samples, beta != 0): the exact kernel dimension of the linear operator
     L(Q) = J(P, Q) on polynomials of degree <= n EQUALS #{H(P) : deg <= n} =
     floor(n/2) + 1: the H-solutions are ALL solutions (no exotic kernel).
  3. [MV] (The explicit inverse, generic) The closed formula G(p, q) =
     (p - beta^2 (q - H(p))^2, (beta (q - H(p)) - alpha (p - beta^2 (q - H(p))^2))/beta)
     satisfies G o F = id and F o G = id identically with generic symbolic H (degree <= 4).
  4. [D] (The theorem) 1-3 plus the consistency ideals (EXP-019/020: degree-2 P must have
     rank-1 top; beta = 0 forces affine) plus Wang's degree-2 case yield: EVERY planar Keller
     map with min(deg P, deg Q) <= 2 is invertible, uniformly, with the closed inverse. The
     first open frontier moves to min degree 3 (both components of degree >= 3).
- **Method.** sympy over QQ(alpha, beta, ...): polynomial identities; exact kernel dimensions
  via linear algebra on coefficient matrices at rational samples.
- **Success criterion.** 1-3 verified; 4 recorded as the assembled theorem with its
  dependency list.
- **Failure criterion.** An exotic kernel element (completeness fails: the classification is
  wrong; escalate), or a residual in the identities (formula wrong; fix or refute).

Declared 2026-07-21 before the run.
