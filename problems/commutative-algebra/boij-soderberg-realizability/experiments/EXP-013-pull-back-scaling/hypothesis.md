# EXP-013 preflight: machine checks of the pull-back along an endomorphism (degrees multiplied by d = 0 or 1 modulo p)

Date: 2026-11-21. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integers
modulo a prime).

## Question

The note `context/2026-11-21-pull-back-and-scaling.md` states: in characteristic p >= 3, if (f, g) is a pure pair of
degree d with central commutator and phi is the endomorphism of U with phi(x) = f, phi(y) = g, then for every
finitely generated graded left U-module M' = U^m/(rows of R) the module phi^* M' = U^m/(rows of phi(R)) has the
Betti table of M' with every degree multiplied by d, and length d^3 times that of M'. In particular a pure pair
(f', g') of degree e' gives the pure pair (phi(f'), phi(g')) of degree d e'.

Question: do the instruments of the repository confirm this in the cases below, among them pairs of degree 8 over
GF(3), 12 over GF(5) and 16 over GF(7), where p does not divide e(e - 1) and nothing was known?

## Definitions fixed here

- The endomorphisms (each is a pair of the corollary of the criterion note; phi(z) = phi(x) phi(y) - phi(y) phi(x)):
  A3 over GF(3): x -> x^3 + y z, y -> y^3 + x z (d = 3). A5 over GF(5): x -> x^5 + y z^2, y -> y^5 + x z^2 (d = 5).
  B4 over GF(3): x -> x^4 + z^2, y -> y^4 + z^2 (d = 4). B6 over GF(5): x -> x^6 + z^3, y -> y^6 + z^3 (d = 6).
  B8 over GF(7): x -> x^8 + z^4, y -> y^8 + z^4 (d = 8).
- phi of a polynomial: every PBW monomial x^a y^b z^c is replaced by phi(x)^a phi(y)^b phi(z)^c, with the products
  taken in U.
- The modules M' (left modules, cyclic, given by the generators of a left ideal):
  Q3 over GF(3): U/(U(x^2 + y^2 + yx) + U(x^2 + yx - z)), the pure pair of quadrics of EXP-003.
  P2 over GF(5) and GF(7): U/(U x^2 + U y^2). P3 over GF(7): U/(U x^3 + U y^3). (Pure by Theorem A.)
  C3 over GF(3): U/(U(x^3 + y z) + U(y^3 + x z)) (the central pair, pure by EXP-011).
  L over GF(3) and GF(5): U/(U x + U y^2), of length 3. T over GF(3): U/(U x^2 + U x y + U y^2 + U z), of length 3.

## Cases (fixed here)

For each case: the Betti table and the length of M' and of phi^* M', each by `uhlib` and by Singular; the comparison
"table of phi^* M' = table of M' with degrees multiplied by d" and "length of phi^* M' = d^3 times the length of M'".

| Case | Field | phi | M' | Degree of the pair, or what is compared |
|---|---|---|---|---|
| S1 | GF(3) | A3 | Q3 | pair of degree 6 (a settled pair (e, p), a new pair of forms) |
| S2 | GF(3) | B4 | Q3 | pair of degree 8; (8, 3) was open |
| S3 | GF(5) | B6 | P2 | pair of degree 12; (12, 5) was open |
| S4 | GF(5) | A5 | P2 | pair of degree 10 |
| S5 | GF(7) | B8 | P2 | pair of degree 16; (16, 7) was open |
| S6 | GF(3) | A3 | C3 | pair of degree 9 (the composition of A3 with itself) |
| S7 | GF(7) | B8 | P3 | pair of degree 24; (24, 7) was open; only if one Betti table takes less than 40 minutes |
| T1 | GF(3) | A3 | L | a table that is not pure: degrees of L multiplied by 3 |
| T2 | GF(5) | B6 | L | the same, multiplied by 6 |
| T3 | GF(3) | B4 | T | the same for T, multiplied by 4 |

Family N (outside the hypotheses; outcomes only):

| Case | Field | Map | M' | Why outside |
|---|---|---|---|---|
| N1 | GF(5) | x -> x^5, y -> y^5 | P2 | an endomorphism with phi(z) = 0, not of finite colength; the result is the power pair of degree 10 |
| N2 | GF(7) | x -> x^5 + y^3 z, y -> y^5 + x^3 z | P2 | a pure pair of degree 5 (EXP-009) whose commutator is not central: the substitution is applied to x^2 and y^2 only, giving the pair of the two squares, of degree 10 |

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). Each of the five pairs (phi(x), phi(y)) is pure, with a central commutator (it commutes with x
  and y); Q3, P2 over GF(5) and GF(7), P3 over GF(7) and C3 are pure; L and T have length 3. Recomputed by this
  routine, not copied.
- G2 (second instrument). Singular 4.3.2 (Plural) gives the same Betti table as `uhlib` on M' and on phi^* M' in every
  case of families S and T.
- G3 (unit tests): the substitution on monomials against hand-written products for A3; phi(u v) = phi(u) phi(v) on
  twenty random pairs u, v of forms of degree at most 3 for A3 and B4; the scaling of a table; the comparison
  routine on a case built to differ.

## Predictions

- P1. In every case of families S and T: the table of phi^* M' is the table of M' with degrees multiplied by d, in
  both instruments, and the length is d^3 times that of M'. So the pairs of S1 to S7 are pure, with lengths 216, 512,
  1728, 1000, 4096, 729, 13824. Confidence 0.9 (a proof on paper that rests on the criterion note; neither is
  reviewed yet).
- P2. In N1 the pair is not pure. Confidence 0.95 (Theorem A: the power pair of degree 10 is not pure in
  characteristic 5). No prediction for N2.

What would falsify, and what each outcome means. A case of S or T where the table is not the scaled table refutes
the theorem of the note (or shows an error in an instrument: the two are then compared). All confirmed: the point
(1, 2, 2, 1) is realized on (0, 8, 24, 32) in characteristic 3, on (0, 12, 36, 48) in characteristic 5 and on
(0, 16, 48, 64) in characteristic 7 by explicit pairs confirmed in two instruments; the proof still needs its review.

## Method and budget

- First instrument: `code/uhlib` (imported, not edited) with a routine of this experiment for the substitution.
  Second instrument: Singular 4.3.2 with Plural through the script generator of EXP-009, with the left ideal given by
  its stored generators.
- At most 6 worker processes and three hours of wall time. A case that does not finish is reported with what was
  done (S5 and S7 are the largest: lengths 4096 and 13824).

## Outputs

`run.py` (with its routine), the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results (per case: the generators of both ideals, both tables from both
instruments, the lengths, the comparison). The verdict is written by the coordinating session after its own re-check
of S2 and S3 with a separate parser and the module construction of `uhlib`.
