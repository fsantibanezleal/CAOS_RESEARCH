# EXP-033 - Closing the edge fan: k = 0, m = 0, and the vertex dichotomy

- **Question.** JCB-035 opening moves. Theorem 3 excluded x-anchored edges with interior
  direction (k, m >= 1). Two boundary directions remain, and their closure assembles into a
  dichotomy: (A) k = 0: E = x phi(y); (B) m = 0: E = x phi(x); (C) THE VERTEX DICHOTOMY: if
  the monomial x is a VERTEX of the Newton polygon of a Keller component P (linear part x),
  then P = x + f(y) exactly (triangular); components where x is swallowed inside the
  polygon (e.g. x + (x + y)^2) escape, and only they can be non-triangular.
- **Motivation (derivations, declared).** (A) With weights (1, 0), P = x phi(y) is
  homogeneous and L preserves each x-degree class: L(x^s q(y)) = x^s (phi q' - s phi' q).
  The constant's class (s = 0) reads phi(y) h'(y) = 1: no polynomial solution once
  deg phi >= 1 (phi would divide 1). Kernels: class-s kernel is (x phi)^s. (B) With
  P = x phi(x): P_y = 0, so J(P, Q) = (x phi)'(x) Q_y = 1 forces a non-polynomial Q_y
  unless phi is constant. (C) Assembly: any support point x^i y^j (i >= 1, (i,j) != (1,0))
  makes the FIRST right-boundary edge from the vertex (1,0) divisible by x, hence an
  excluded shape by Theorem 3 / (A) / (B); the only allowed edges at the vertex go to pure-y
  vertices (0, d), whose segments contain no interior lattice points, giving edge forms
  c x + c' y^d: the triangular signature. Hence the dichotomy. The escape route (x not a
  vertex) is real: x + (x + y)^2 is a genuine component. Strategic frame: after a linear
  gauge rotation the analysis re-applies to non-triangular components: the germ of an
  induction; recorded as the program's route, not claimed proved.
- **Falsifiable predictions.**
  1. [MV] (k = 0 class structure) L(x^s q(y)) = x^s (phi q' - s phi' q) exactly (symbolic
     phi, deg <= 3, s <= 4); the s = 0 truncated systems are inconsistent over
     QQ(coefficients); class-s kernels equal (x phi)^s (s <= 2).
  2. [MV] (k = 0 windows and certificate) Full completion windows empty for x(1 + y),
     x(1 + y)^2, x(1 + y + y^2), including with pure-y tails (x(1+y) + y^3); certificate
     over QQ(c1) for P = x(1 + c1 y): pairing gcd a pure c1-power.
  3. [MV] (m = 0) Full windows empty for x + x^2, x + x^3 + x^2 (and the one-line reason
     recorded: J = (x phi)' Q_y).
  4. [MV] (The dichotomy boundary, three-sided) (i) P's with vertex x AND a mixed monomial
     (several shapes whose polygon puts (1,0) as a vertex): windows EMPTY; (ii) triangular
     P = x + y^2, x + y^3 - 2 y^2: consistent (they are components); (iii) x-swallowed
     P = x + (x + y)^2 and x + (x + 2y)^3: consistent: all three sides of the dichotomy
     behave exactly as derived.
- **Method.** sympy over QQ and QQ(coeffs); class matrices; full windows; the certificate
  instrument. Caps 570 s.
- **Success criterion.** 1-4 verified; Theorem 3+ (all edge directions) and the vertex
  dichotomy recorded with proofs ([MV]-shadowed derivations; the dichotomy's polygon
  reasoning is elementary given the edge theorems); the induction-by-rotation route
  recorded as strategy [C].
- **Failure criterion.** A consistent vertex-x mixed sample (the dichotomy is wrong:
  analyze immediately); a k = 0 or m = 0 window that completes (the boundary derivations
  are wrong).

Declared 2026-07-22 before the run.
