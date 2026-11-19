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
