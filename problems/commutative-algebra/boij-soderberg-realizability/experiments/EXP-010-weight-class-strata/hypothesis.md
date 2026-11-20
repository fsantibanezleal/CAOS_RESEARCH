# EXP-010 preflight: pure pairs in the weight-class strata, for e = 6 and 7 in the five open characteristics

Date: 2026-11-20. Status: frozen before any computation of this experiment on an open pair. CPU only. Exact
arithmetic (integers modulo a prime).

## Question

After EXP-009 the point (1,2,2,1) of (0, e, 3e, 4e) over U is open in five pairs (e, p) with e <= 7: (6, 5), (6, 7),
(7, 3), (7, 5), (7, 7). A random search in the whole Grassmannian does not reach them (EXP-008: shares of the order of
p^(-2 h_e(3e)), that is p^(-8) and p^(-12)), and the four-parameter linear family holds no pure member there
(EXP-009).

The note `context/2026-11-20-weight-class-strata.md` gives the weight w = b + c of x^a y^b z^c, the strata

    S(m; i, j) = { <f, g> :  f supported on the monomials of weight = i mod m,  g on those of weight = j mod m },

a necessary condition for a stratum to hold a pure pair (the admissible strata, a finite list for each e that does
not depend on the field), and a probe on settled pairs: over GF(5) and GF(7) at e = 5 and over GF(3) at e = 6 the
stratum S(2; 0, 1) holds members with the pure Hilbert function at 9 to 23 times the share of a random search, about
0.3 to 0.7 times p^(-h_e(3e)); the linear family is the stratum S(e - 1; 0, 1).

Question: for each of the five open pairs, does an admissible stratum hold a pure pair over GF(p)? One pure pair,
confirmed by the second instrument, settles the characteristic p for that e. Secondary: which strata hold pure pairs,
and at what share.

## Definitions fixed here

- Weight of the monomial x^a y^b z^c of `uhlib` (PBW order, yx = xy - z): w = b + c. Class of a monomial for m: w mod m.
- d_i(e, m): the number of monomials of degree e and class i.
- Members of S(m; i, j), i < j: pairs (f, g) of nonzero coefficient vectors on the two supports, each normalized so
  that its first nonzero coefficient (in the order of `uhlib.algebra.monos(e)`) is 1. Their number is
  N = ((p^(d_i) - 1)/(p - 1)) ((p^(d_j) - 1)/(p - 1)).
- Members of S(m; i, i): pairs (f, g) of coefficient vectors on the one support; only sampled, never enumerated. A
  stratum with d_i < 2 is empty.
- Admissible: the definition of the note (some classes (s_1, s_2, t) make every H_k(n) >= 0 for 0 <= n <= 4e + 6m + 2).
- r = 2 u(2e) - 2. Pure Hilbert function: rank of mu_(3e) equal to r, mu_(3e-1) injective, and rank of mu_n equal to
  u(n) - h_e(n) for n = 3e + 1, ..., 4e - 3. (These ranks give the Hilbert function h_e in every degree: a kernel
  element of mu_n with n <= 3e - 2 would give at least u(2) = 4 independent kernel elements in degree 3e, and
  I_n = U_n at n = 4e - 3 gives I_n = U_n above it, the ideal being generated in degree e and U in degree 1.)
- Pure: the Betti table is (1, 2, 2, 1) on (0, e, 3e, 4e), computed with `uhlib` (module construction and `tor.betti`).

## Cases (fixed here)

Budget of a stratum with budget B: all N members when i < j and N <= B; otherwise B random members (uniform
coefficient vectors on the supports, seed 20261120 + a fixed index of the stratum). For every member: the rank of
mu_(3e); when it is r, the remaining ranks of the pure Hilbert function, stopping at the first that fails; for the
members with the pure Hilbert function, in the order found, the Betti table, until 5 pure members are found or 40
tables are computed in that stratum. A stratum stops once it has 5 pure members (chunks already started finish).

Family Q, the question. The pairs (6, 5), (6, 7), (7, 3), (7, 5), (7, 7); every admissible stratum with
2 <= m <= e + 1; budget B(e, p) = max(20,000, 30 p^(h_e(3e))): 20,000 at (6, 5), 72,030 at (6, 7), 21,870 at (7, 3),
468,750 at (7, 5), 3,529,470 at (7, 7). (h_6(18) = 4, h_7(21) = 6.)

Family C, controls on settled pairs. The pairs (4, 3), (4, 5), (5, 3), (5, 5), (5, 7), (6, 3), (6, 11), (7, 11),
(7, 13); every stratum with 2 <= m <= e + 1: budget 20,000 for an admissible stratum and 3,000 for one that is not.

Family E, e = 8, exploratory, run last and only within the budget of time:
- (8, 3): the strata S(2; 0, 0), S(2; 0, 1), S(2; 1, 1) with budget 600,000 each; every other admissible stratum with
  3 <= m <= 7 with budget 100,000.
- (8, 5) and (8, 7): the admissible strata with 5 <= m <= 7, that is S(5; 0, 3), S(6; 0, 2), S(6; 0, 4), S(6; 2, 4),
  S(7; 0, 1), with budget 2,000,000 each.
- (8, 11) and (8, 13): the stratum S(7; 0, 1), which contains the linear family, with budget 100,000 (all members).

Order of the run: gates, family C, family Q in the order (6, 5), (6, 7), (7, 3), (7, 5), (7, 7), then family E in
the order (8, 11), (8, 13), (8, 3), (8, 5), (8, 7). Within a pair, strata in decreasing order of m.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, before the families).
  (a) <x^e, y^e> is pure over GF(13) for e = 4, 5, 6 and over GF(17) for e = 7, and is not pure over GF(5) for e = 4.
  (b) <x^6 + y^4 z, y^6 + 3 x^4 z> over GF(11) and <x^7 + y^5 z, y^7 + x^5 z> over GF(13) are pure (EXP-009) and are
  members of S(5; 0, 1) and S(6; 0, 1).
  (c) The rank routine of this experiment agrees with the rank computed through the module construction of `uhlib` on
  50 random pairs for each of (6, 5), (6, 11), (7, 3), (7, 13) and each degree n = 3e - 1, 3e, 3e + 1, 4e - 3.
  (d) The list of admissible strata for e = 4 to 8 equals the table of the note (17, 19, 34, 34, 58 strata).
- G1 (known answers, after family C). At (5, 5): pure members in S(2; 0, 1) and in S(3; 0, 2), and no member of
  S(4; 0, 1) with the pure Hilbert function (EXP-009: none in the linear family). At (5, 7): pure members in
  S(2; 0, 1), S(3; 0, 2) and S(4; 0, 1). At (6, 3): pure members in S(2; 0, 1). At (6, 11), (7, 11), (7, 13): pure
  members in S(e - 1; 0, 1).
- G2 (second instrument). For every pair with a pure member, Singular 4.3.2 (Plural), with a script generated from
  the stored polynomials, gives the pure Betti table on the first two pure members of each stratum that has one (at
  most ten members per pair, strata in decreasing order of m).
- G3 (unit tests): the weights and supports against a hand-written list for e = 4; the number of members N and the
  enumeration (each normalized member once) on two small strata; the admissible list for e = 5 against the note; the
  rank routine against `uhlib` (as G1 (c), on a small case); the pure Hilbert function test on <x^4, y^4> over GF(13)
  (true) and GF(5) (false); the early stop.
- G4 (the exclusion, family C). No member of a stratum that is not admissible has the pure Hilbert function. One such
  member refutes the proposition of the note or shows an error in the routine; the run stops.

## Predictions

- P1 (the open pairs). An admissible stratum holds a pure member over GF(p) in each of the five pairs. Confidence:
  0.8 at (6, 5), 0.75 at (6, 7), 0.7 at (7, 3), 0.65 at (7, 5), 0.55 at (7, 7).
- P2 (the share in S(2; 0, 1)). In every pair of families Q and C where S(2; 0, 1) holds members with the pure
  Hilbert function, their share among the members examined is between 0.1 and 1.5 times p^(-h_e(3e)). Confidence 0.6
  (the probe gave 0.31, 0.72, 0.41 on three settled pairs).
- P3 (the exclusion). Gate G4 passes. Confidence 0.97.
- P4 (characteristic dividing m). In families Q and C no member of a stratum with p dividing m has rank of mu_(3e)
  exactly r. Confidence 0.7 (observed in the probe at (4, 3), (5, 5), (6, 3); no proof).
- P5 (e = 8). S(7; 0, 1) holds a pure member at (8, 11) and at (8, 13): confidence 0.6 each (EXP-009: the linear
  family held one in six of the seven pairs with e < p < 2e). A pure member is found at (8, 3): 0.5; at (8, 5): 0.3;
  at (8, 7): 0.3.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles the
characteristic p for that e. A pair of family Q without a pure member says that no pair of forms with one of these
cyclic symmetries was found within the budget; where a stratum was enumerated in full it says that the stratum holds
no pure pair over GF(p); it says nothing about pairs without such a symmetry, and nothing about extensions of GF(p).
If all five pairs are settled, the point is realized over U for 2 <= e <= 7 exactly in the characteristics other
than 2. A failure of G4 refutes the necessary condition as stated.

## Method and budget

- First instrument: a routine of this experiment on `code/uhlib` (imported, not edited): the matrices of mu_n are
  assembled from the structure constants of `uhlib.algebra.mono_mul` reduced modulo p, and their ranks are computed
  with python-flint; the Betti tables with the module construction and `tor.betti` of `uhlib`. Second instrument:
  Singular 4.3.2 with Plural, through the script generator of EXP-009.
- At most 16 worker processes and five hours of wall time. Results are stored per stratum as each finishes, so a run
  that is interrupted or reaches the budget of time is reported with what was done; a pair that did not finish is
  named as such.
- Stored per stratum: m, i, j, admissible or not, d_i, d_j, N, the number of members examined and whether they are all
  the members, the distribution of the rank of mu_(3e), the number with rank r, with the pure Hilbert function, the
  tables computed, the pure members with their polynomials and coefficient vectors (at most 50 per stratum with the
  pure Hilbert function).

## Outputs

`exp010_routine.py`, `run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results (per pair, the strata with their counts; three pure members per
stratum as polynomials). The verdict is written by the coordinating session after its own re-check of the decisive
members with a separate parser and the module construction of `uhlib`.
