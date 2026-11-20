# EXP-007 preflight: the family of pure pairs through <x^e, y^e>: tangent space of the rank locus, explicit pure pairs over the rationals, a linear family and a plane section, archived

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (fractions over
the rationals; integers modulo a prime).

## Question

The context note `2026-11-20-pure-pairs-family-dimension.md` proves, and an independent review confirms, that the
two-dimensional spaces W of forms of degree e with U/(U W) pure of type (0, e, 3e, 4e) are open in the locus
D_e = {rank mu_(3e)(W) <= r}, r = 2 u(2e) - 2, and form a family of dimension at least 4e - 4 through
W_0 = <x^e, y^e> in characteristic 0 or at least 2e. The review added computations that make the statement concrete:
the tangent space of D_e at W_0 has dimension exactly 4e - 4 over the rationals for e = 4 to 7; explicit pure pairs
over the rationals lie outside the orbit of W_0; a four-parameter linear family lies in D_e; a plane section of D_4 is
a plane with an explicit equation. Those computations ran once, in a scratch folder that was deleted, with one
instrument. Do the repository's instruments reproduce each of them?

The numbers below are the review's (record `bs-pure-family-dimension-review-2026-11-20` in the coordination
repository). They are predictions of this experiment in the sense that it can contradict them; none was computed for
this file.

## Definitions

- u(n) = dim U_n, h_e(n), mu_n(W), D_e and r as in the context note. PBW monomials x^i y^j z^k.
- Tangent space at a point of rank exactly r. Let A = mu_(3e)(W_0), a matrix with 2 u(2e) rows (the products m w for m
  a PBW monomial of degree 2e and w in the basis x^e, y^e of W_0) and u(3e) columns. In the chart
  W = <x^e + f, y^e + g>, f and g in the span of the PBW monomials of degree e other than x^e and y^e
  (2 (u(e) - 2) coordinates), mu_(3e)(W) = A + B(f, g) with B linear. The tangent space of D_e at W_0 is the space of
  (f, g) such that lambda(k B(f, g)) = 0 for every k in the left kernel K of A (kA = 0) and every linear form lambda
  that vanishes on the row space of A.
- Orbit test: the orbit of W_0 under the graded automorphisms consists of the spaces <l_1^e, l_2^e>, all contained in
  the span S_e of the e-th powers of linear forms (dimension e + 1 in characteristic 0). A space W with
  dim (S_e + W) > e + 1 is outside the orbit, over every extension of the field.

## Statements under test

- T1 (tangent space over the rationals). For e = 4, 5, 6, 7: rank A = r, dim K = 2, the cokernel of A has dimension
  h_e(3e) (1, 2, 4, 6), and the tangent space of D_e at W_0 has dimension 4e - 4 (12, 16, 20, 24). The two tangent
  directions of the orbit (the derivatives of x^e under x to x + t y and of y^e under y to y + t x) lie in it.
- T2 (tangent space in positive characteristic at least 2e). Dimension 12 at e = 4 and 16 at e = 5 over GF(13),
  GF(17), GF(32003); at e = 6: 22 over GF(13), 20 over GF(17) and GF(32003); at e = 7: 26 over GF(17), 24 over
  GF(32003).
- T3 (explicit pure pairs over the rationals, outside the orbit). Each of the following has rank mu_(3e) = r, the pure
  Betti table (1, 2, 2, 1) on (0, e, 3e, 4e), and lies outside the orbit of W_0:
  - P1 = <x^4 + x y^3, y^4>;
  - P2 = <x^4 + 31 x^2 y^2 - 8 x y z, y^4>;
  - P3 = <x^4 + 59 x^2 y^2 - 4 z^2, y^4>;
  - P4 = <x^4 + 2 x y^3 - 3 y^2 z, y^4 + 5 x^3 y + 7 x^2 z>;
  - P5 = <x^5 + 2 x y^4 - 3 y^3 z, y^5 + 5 x^4 y + 7 x^3 z>.
  Controls: W_0 at e = 4 and 5 is pure and inside the orbit (dim (S_e + W_0) = e + 1); C1 = <x^4 + x^2 y^2, y^4> has
  rank mu_12 = 49 and is not pure; C2 = <x^4 + x y^3, y^4 + x^3 y> has rank mu_12 = 46 and infinite length.
- T4 (the linear family). For e = 4 and e = 5 let
  L_e(a, b, c, d) = <x^e + a x y^(e-1) + b y^(e-2) z, y^e + c x^(e-1) y + d x^(e-2) z>. Every member has
  rank mu_(3e) <= r, over the rationals for (a, b, c, d) in {-2, -1, 0, 1, 2}^4 (625 members for each e) and over
  GF(32003) for 200 random members. Among the 200 random members over GF(32003) at least 190 are pure and outside the
  orbit, for each e.
- T5 (the plane section at e = 4). For integers alpha, beta, gamma in {-4, ..., 4}, the space
  <x^4 + alpha x^2 y^2 + beta x y z + gamma z^2, y^4> over the rationals has rank mu_12 <= 48 if and only if
  8 alpha + 31 beta + 118 gamma = 0. (729 spaces; the points of the plane in the grid are those with that equation.)
  Over the rationals, each space of the section with (alpha, beta, gamma) = t (31, -8, 0) or t (59, 0, -4), t = 1, 2, 3,
  is pure.
- T6 (the common-factor locus). Over GF(32003), for 20 random spaces W whose two forms have images in U/(z) = k[x, y]
  with a common linear factor (e = 4): rank mu_12 <= 48 and M_W has infinite length (nonzero in every degree up to 24).
  For e = 5 with a common factor of degree 2: rank mu_15 <= 70. For e = 6 with a common factor of degree 4:
  rank mu_18 <= 96.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). W_0 is pure over the rationals for e = 4, 5, 6, 7 (Theorem A; Betti table computed), and its
  rank of mu_(3e) is r.
- G2 (the tangent routine on cases with a known answer). With the chart replaced by all matrices (B the identity
  of the space of matrices), the routine gives the dimension of the generic determinantal variety at a point of rank
  exactly r: 10 for 3 by 4 matrices of rank at most 2 at a random matrix of rank 2, and 3 for 2 by 2 matrices of rank
  at most 1 at a matrix of rank 1.
- G3 (second instrument). Singular 4.3.2 (Plural) gives the same Betti table as the first instrument on W_0 (e = 4,
  5), on P1 to P5 and on C1, and the same Hilbert function up to degree 24 on C2, from scripts generated from the
  polynomials.
- G4 (unit tests) of the chart, of the matrix B(f, g) against a direct product in `uhlib`, of the orbit test (inside
  for <l_1^4, l_2^4> with random rational l_1, l_2; outside for a random W), and of the routine of G2.

## Predictions

- P1: T1 holds for e = 4, 5, 6, 7.
- P2: T2 holds in each field named.
- P3: T3 holds for the five pairs and the four controls, in both instruments.
- P4: T4 holds.
- P5: T5 holds.
- P6: T6 holds.

What would falsify, and what each outcome means: a tangent dimension above 4e - 4 over the rationals (the locus is
then not shown smooth of the minimal dimension at W_0, and the exactness reported by the review is withdrawn; the
bound of the note is not affected); a pair of T3 that is not pure or lies in the orbit (the example is withdrawn); a
member of L_e outside D_e or a grid point contradicting the plane equation (the weight argument of the review has an
error, to be found before anything is stated).

## Method and budget

- First instrument: `code/uhlib` (algebra with fractions and prime fields, the module construction, the Betti table
  through Tor against the resolution of the trivial module) and exact linear algebra (fractions or integers modulo a
  prime; never floating point). The routines of EXP-005 and EXP-006 may be imported.
- Second instrument: Singular 4.3.2 with Plural in WSL, with scripts generated from the polynomials.
- At most 8 worker processes, at most two hours of wall time, at most 20 minutes per case.

## Outputs

`run.py`, the routine and its tests; `artifacts/results.json` (per statement: the cases with their fields, the
matrices' sizes and ranks, the tangent dimensions, the spaces with their polynomials, ranks, Hilbert functions, Betti
tables in both instruments and orbit test; the gates), `artifacts/run.log`, `artifacts/singular/`, and
`results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-checks.
