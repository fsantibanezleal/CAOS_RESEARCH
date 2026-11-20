# EXP-003 verdict: CONFIRMED. In characteristic 2 no pair of quadrics of U(H) has a finite length quotient; the proof steps of the family U/U(x^e, y^e) hold by machine for e <= 8; the family is special for e >= 4

Date: 2026-11-19. Hypothesis frozen in commit 8028f796 before any computation. Exact arithmetic (the library `uhlib`
over QQ, prime fields and GF(2^k); Singular Plural as the second instrument). Run: `run.py`, exit 0, 83 tasks, 152 s;
36 library tests pass; the EXP-002 run reproduces unchanged after the library additions.

## Outcome per claim

| Claim | Outcome |
|---|---|
| C0 calibration | Holds; the two instruments agree on 127 of 127 finite length modules compared in this run. |
| A1 | Holds, exhaustively: all 35 two-dimensional subspaces of U_2 over GF(2) and all 357 over GF(4) give a quotient that is nonzero in every degree from 2 to 20. Every subspace contains a nonzero central quadric (28 and 336 with a one-dimensional central part, 7 and 21 entirely central), as the derivation states; the determinant of right multiplication by the non-central generator on U/Uc is zero (6 and 10 subspaces) or a form of degree 8 (22 and 326). |
| A2 | Holds on 200 random subspaces over GF(16) and 200 over GF(256). |
| B1 (search, characteristic 2) | (0,1,5,6), (0,1,7,8), (0,1,9,10), (0,1,11,12) and (0,3,5,8) are realized over U(H) in characteristic 2: generic presentations give the primitive pure table over GF(2), GF(4) and GF(16) (for example 12, 20 and 38 of 40 seeds on (0,1,5,6); 3, 19 and 33 of 40 on (0,3,5,8)), both instruments agreeing on the hits. (0,3,9,12) (pairs of cubics) and (0,2,10,12) (2 by 3 matrices of quadrics) are never of finite length in 120 seeds each in characteristic 2, while they are pure on 20 of 20 seeds over GF(32003). (0,5,7,12) is not reached by generic presentations over any field tried, GF(32003) included (six general quintics give a non-pure table), so its characteristic 2 outcome is not interpreted. |
| C1 | Holds for e = 2, ..., 8 over QQ (and over GF(32003)): the dimension of every (weight, degree) piece of M_e equals D_q(n') of the context note; the kernel of y is the span of the classes z^c g_a; the socle is one-dimensional, of weight 0 and degree 4e - 4; the Hilbert series is (1 + ... + t^(e-1))^2 (1 + t^2 + ... + t^(2e-2)); lengths 8, 27, 64, 125, 216, 343, 512. |
| C2 | Holds for e = 2, ..., 5: as a k[z]-module, M_e is the sum of one summand k[z]/(z^(2e-1-a-b)) generated in degree a + b for each a, b < e. |
| C3 | Holds: for e = 2, 3, 4, 5 the primes p <= 23 at which U/U(x^e, y^e) is not pure over GF(p) are exactly the predicted ones: {2, 3}, {2, 3, 5}, {2, 3, 5, 7}, {2, 3, 5, 7}. |
| D1 | Holds: a random pair of forms of degree e has the maximal-rank Hilbert function for e = 2, 3, 4, 5, 10, and its Betti table is pure for e = 2, 3 and not pure for e = 4, 5, 10 (0 of 5 pairs each). |
| D2 (exploration) | The primitive point (2,3,3,2) of (0,3,15,18) is realized over GF(32003) by the cokernel of a random 2 by 3 matrix of cubics (10 of 10) and by the presentation of the Kostant module L(1,1) with x^3, y^3 substituted for x, y; the same substitution with squares gives (0,2,10,12). |

## Verdict

CONFIRMED on every claim with a prediction (A1, A2, C1, C2, C3, D1; B1 as predicted for the rays with odd d1 and for
(0,2,10,12), not as predicted for (0,3,9,12), which generic pairs of cubics realize over GF(32003) and never in
characteristic 2).

## What is established, and by what

1. Characteristic 2, the ray (0,2,6,8). The derivation of the hypothesis (x^2, y^2 and z are central; two independent
   quadrics always span a nonzero central quadric c or are both central; the quotient is then a finitely generated
   module over a two-dimensional polynomial ring cut by one square matrix, of infinite length) is a proof over every
   field of characteristic 2, and A1 checks its case analysis on every subspace over GF(2) and GF(4). A module with table
   (1,2,2,1) on (0,2,6,8) is a quotient of U by two independent quadrics, so over a field of characteristic 2 that point
   is not realizable over U(H); it is not realizable over k[x,y,z] in any characteristic (two generators cannot cut out a
   finite length quotient). So the primitive point of (0,2,6,8) is a counterexample to Erman-Sam Question 6.1 over every
   field of characteristic 2, with d3 = 8, and it is realizable over U(H) in characteristic 0 and in every characteristic
   other than 2 by a pair of quadrics (EXP-002: the pair (x^2, y^2) outside characteristics 2 and 3, other pairs in
   characteristic 3). The answer to Question 6.1 on that point depends on the characteristic. [D with machine support;
   to be read by a reviewer before it is claimed in a paper.]
2. The family U/U(x^e, y^e) in characteristic 0. Every step of the derivation of the context note is confirmed for
   e <= 8, including the structure over k[z] and the exact set of bad primes for e <= 5, which the derivation predicts
   from factorials and rectangular tableau counts. The statement for every e rests on the derivation, which is complete
   on paper (Hilbert series, socle, resolution) and awaits review.
3. The family is special. For e >= 4 a general pair of forms of degree e is not pure: the pair (x^e, y^e) has a larger
   quotient than a general pair (by one dimension in degree 4e - 4 at e = 4), so the points (1,2,2,1) on (0,e,3e,4e) with
   e >= 4 are realized by a special left ideal and are out of reach of a random search.
4. The family of (0,1,5,6). The substitution of x^e, y^e in the presentation of L(1,1) realizes (2,3,3,2) on
   (0,e,5e,6e) for e = 2, 3 (over GF(32003)), which suggests the same statement for every Kostant module and every e.

## Open after this experiment

- Characteristic 2 on (0,3,9,12) and (0,2,10,12): never realized in the searches. For pairs of cubics f = ax + by,
  g = cx + dy with a, b, c, d central quadrics, the element (ad - bc) x lies in the left ideal and the support of the
  quotient contains the points of the surface ad - bc = 0 where the common direction of f and g squares to zero, a
  curve for a general pair; whether some special pair escapes is not decided. Candidates for further
  characteristic-dependent points, not claims.
- (0,5,7,12) in positive characteristic (the Kostant module L(4,0) realizes it in characteristic 0; general quintics do
  not).
- A proof of the substitution statement of item 4.

## Deviations from the hypothesis

- A numpy build of the quotient module was added to the library (tested equal to the reference build) to make the
  characteristic 2 searches feasible; QQ computations use the reference build with exact fractions.
- D1 used five pairs per degree; C2 reads the pattern with the generator degree a + b, which the hypothesis did not fix.
- The first full run had a defect in the flag that compares the Hilbert series with the product formula (trailing
  zeros); it was fixed and everything rerun; the artifacts are those of the second run.

## Adversarial validation

Two instruments on every finite length module (127 agreements, no disagreement); exhaustive enumeration with the count
checked against the Gaussian binomials 35 and 357; Hilbert functions cross-checked on ten subspaces per field by a
second build and by Singular; the GF(32003) control of B1, which separates "not reached by generic presentations" from
"not realized in characteristic 2"; the prediction of the bad primes fixed before the run and met exactly.

## How could this be wrong?

- The machine shows nonzero pieces up to degree 20 only; infinite length in characteristic 2 rests on the derivation.
- A search miss proves nothing: (0,3,9,12) and (0,2,10,12) are open in characteristic 2, not excluded.
- C1 to C3 are finite checks; the statement for every e is the derivation's.
- The realizations in characteristic 2 are over GF(2), GF(4) and GF(16); they pass to every field of characteristic 2
  by base change.

## Addendum 1 (2026-11-19): the derivations after an independent review

A reader other than the writer re-derived both derivations step by step and ran an independent computation (own code
built only from xy = yx + z; record `bs-proofs-review-2026-11-19` in the coordination repository). Verdict: both correct
after minor fixes, no blocker. The hypothesis file is frozen; the corrections it calls for are recorded here.

Characteristic 2 on (0,2,6,8): the argument, with the steps the review asked to state.

1. In characteristic 2, x^2, y^2 and z are central (x^2 y - y x^2 = 2xz, y^2 x - x y^2 = -2yz), C = k[x^2, y^2, z] is a
   polynomial ring in three generators of degree 2, and U is free over C on 1, x, y, yx. U_2 = C_2 + k xy, of dimensions
   4 = 3 + 1.
2. A two-dimensional subspace V of U_2 meets C_2: either V lies in C_2, or V = span(c, f) with c in C_2 nonzero and f not
   central. In both cases the left ideal generated by V is Uc + Uf with c, f in V.
3. V inside C_2: the ideal is two-sided and U/U(f, g) is free of rank 4 over C/(f, g), which has Krull dimension at
   least 1 (Krull's height theorem in C), so the quotient has infinite length.
4. V = span(c, f): R = C/(c) is a polynomial ring in two generators. U/Uc is free of rank 4 over R. Right multiplication
   by f is well defined on U/Uc (u c f = u f c because c is central), is R-linear for the left action of R, has image
   (Uf + Uc)/Uc and cokernel U/(Uf + Uc). It is homogeneous of degree 2, so its determinant is 0 or a homogeneous element
   of degree 8, a non-unit. If the determinant is 0 the cokernel has positive rank over R. If it is not 0, then for
   every prime P of R containing it the localized map has a non-unit determinant and is not surjective, so P lies in
   the support: the support of the cokernel is exactly the zero set of the determinant, of dimension 1. In both cases the
   cokernel has infinite length.
5. A module with the Betti table (1,2,2,1) on (0,2,6,8) has Hilbert series (1 + t)^2 (1 + t^2), a polynomial, so it has
   finite length; beta_0 = 1 makes it cyclic and beta_1 = 2 in degree 2 makes it U/U(f, g) with f, g independent
   quadrics. By steps 2 to 4 no such module exists. Nothing uses the size of k: the statement holds over every field of
   characteristic 2, finite or infinite. A non-cyclic module is excluded by beta_0 = 1, right modules give nothing new (U
   is isomorphic to its opposite), and the grading is the one of Erman and Sam.

Position against the literature (correction of item 1 of "What is established"). Question 6.1 of Erman and Sam already
has a negative answer over every field: Jiang, Li, Sun, Wang, Xiao and Yu, arXiv:2605.25259, Theorem 3.7, the point
(1,2,9,8) on (0,6,20,21), excluded over U(H) because the numerator of its Hilbert series does not vanish at t = -1. The
result here is of a different kind: a point that passes that numerical test, is realized over U(H) in characteristic 0
and in every odd characteristic, and is realized over neither ring in characteristic 2. It is to be stated as a
dependence of the answer on the characteristic, with that theorem cited, never as the first negative answer.

Realizations of (0,2,6,8) outside characteristic 2, made explicit. The pair (x^2, y^2) realizes the point exactly in
characteristic 0 and in characteristic p >= 5 (the family U/U(x^e, y^e) is pure exactly when the characteristic is 0 or
at least 2e; context note, steps 2 to 7). In characteristic 3 the pair f = x^2 + y^2 + yx, g = x^2 + yx - z over GF(3) has
the Betti table (1,2,2,1) on (0,2,6,8) (found by the reviewer; re-computed with `uhlib`, full Betti table), and it passes
to every field of characteristic 3 by base change. The Hilbert function alone does not certify purity: over GF(3) the
pair f = 2x^2 + 2y^2 + z + yx, g = y^2 + 2z has the Hilbert function (1,2,2,2,1) and Betti numbers in degrees 7 as well.

The family U/U(x^e, y^e) (item 2 of "What is established"): the statement is now sharp. For a field k and e >= 1, the
module has the pure resolution of type (0, e, 3e, 4e) with table (1,2,2,1) if and only if char k = 0 or char k >= 2e;
for every prime p <= 2e - 1 it is nonzero in degree 4e - 2. Claim C3 (the bad primes for e <= 5) is the instance e <= 5
of that statement; a re-check with `uhlib` gives the same pattern at e = 6 (not pure for p <= 11, pure at p = 13).

