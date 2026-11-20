# EXP-020 preflight: the members x^e + alpha(xy, z) y^t, y^e + beta(xy, z) x^t fixed by the exchange of x and y, enumerated completely at (14, 11), (15, 11), (15, 13), (15, 17), (16, 17), (16, 19)

Date: 2026-11-20. Status: frozen before any computation of this experiment on a pair that is not settled. CPU only.
Exact arithmetic (integers modulo a prime).

## Question

U has the automorphism omega with omega(x) = y, omega(y) = x, omega(z) = -z. For the pairs of EXP-019,

    f = x^e + alpha(h, z) y^t,      g = y^e + beta(h, z) x^t,      h = xy,   alpha, beta forms of degree d = (e - t)/2,

omega(f) = y^e + alpha(h - z, -z) x^t (because yx = h - z). Write alpha^omega(h, z) = alpha(h - z, -z). The torus
x -> lambda x, y -> mu y acts on the members by (alpha, beta) -> (kappa alpha, beta/kappa), and the filter of EXP-019
does not change under it. So for the members with

    beta = c alpha^omega,       c a scalar not zero,

the left ideal Uf + Ug is carried to itself by omega followed by an element of the torus (over a field with enough
roots), and omega exchanges the two end summands M_(-t) and M_t of the decomposition of the note
`context/2026-11-20-pairs-with-exponent-t.md`. Their lengths are then equal, so the two congruences (F1) and (F2)
should hold together: d - 1 conditions on the d + 1 coefficients of alpha, instead of 2 (d - 1) conditions on
2 (d + 1) coefficients. If that is right, the members of this kind that pass the filter are about p^2 in number for
each c, and they can be listed by a complete enumeration of alpha, of p^(d+1) members, where the random search of
EXP-019 needs about p^(2d-2) members for each one that passes. By the theorem of the note (reviewed), a member
that passes has the pure Hilbert function when 2t <= p - 1, and by its Theorem 2 it is a pure pair when moreover
Delta has no common factor with A_(e-t).

Up to the torus, (alpha, c) and (kappa alpha, c/kappa^2) give the same member, so c runs over 1 and one scalar that
is not a square.

Evidence, all on settled pairs (probe of the coordinating session, scripts and logs under the data root,
`caos-research/boij-soderberg-realizability/EXP-020-probe/`), complete enumerations of alpha with c = 1 and c the
least non-residue:

| (e, p) | t | d | members | with (F0) where (F1) and (F2) differ | pass (F0) to (F3) | of them with (C1) |
|---|---|---|---|---|---|---|
| (8, 7) | 2 | 3 | 4,800 | 0 | 28 | 18 |
| (9, 13) | 3 | 3 | 57,120 | 0 | 116 | 74 |
| (11, 17) | 7 | 2 | 9,824 | 0 | 286 | 286 |
| (13, 11) | 5 | 4 | 322,100 | 0 | 94 | 94 |

and the first 30 passing members of each (28 at (8, 7)) have the pure Hilbert function by the staged test in U.

Question: at the six pairs with e <= 16 that are not settled and where an exponent is allowed, does the complete
list of these members hold a pure pair over GF(p)?

State when this file is frozen: (14, 11), (15, 11), (15, 13), (15, 17), (16, 17), (16, 19) are not settled. EXP-019 is
running a random search at (14, 11) (127 million members examined, none passing so far) and examined 13 million
random members at (15, 17) without a passing one; (15, 11) and (15, 13) were not attempted. No computation was made
for the members of this experiment at these six pairs.

## Definitions fixed here

- A member: (alpha, c) with alpha a polynomial in h of degree at most d over GF(p), not zero, given by its
  coefficients a_0, ..., a_d of 1, h, ..., h^d, and c in {1, nu}, nu the least positive integer that is not a square
  modulo p. Then beta(h) = c times the sum of the a_i (h - 1)^i (-1)^(d-i), and the pair (f, g), the filter (F0) to
  (F3), the stage of a member and (C1) are those of EXP-019 and of the note (exact arithmetic; the routine of EXP-019
  is imported, not edited).
- The exponent t of a pair (e, p): as in EXP-019 (the largest t of the parity of e with t <= e - 2, 2t <= p - 1 and,
  when p <= e, p not dividing (e + t)/2).
- The enumeration of a case: every alpha in the lexicographic order of (a_0, ..., a_d), the last coefficient varying
  fastest, with c = 1 and then c = nu for each alpha; the index of a member is 2 times the rank of alpha plus 0 or 1.
  Complete: 2 (p^(d+1) - 1) members.
- For every member that passes the filter: (C1), and the staged test of the pure Hilbert function of EXP-010 (through
  the routine of EXP-019). The Betti table with `uhlib` for the passing members in the order of their index, until 5
  pure members are found or 40 tables are computed. The enumeration is always completed (the counts are of the whole
  list).
- Pure means: the Betti table computed by `uhlib` is (1, 2, 2, 1) on (0, e, 3e, 4e) and the length is e^3.

## Cases (fixed here)

Family K, controls (the counts of the table above must be reproduced; pure pairs exist there by EXP-015, EXP-018
and EXP-019): (9, 13) with t = 3, (11, 17) with t = 7, (13, 11) with t = 5.

Family X, the open pairs:

| (e, p) | t | d | Stratum | Members 2 (p^(d+1) - 1) |
|---|---|---|---|---|
| (14, 11) | 4 | 5 | S(9; 0, 5) | 3,543,120 |
| (15, 11) | 5 | 5 | S(10; 0, 5) | 3,543,120 |
| (15, 13) | 5 | 5 | S(10; 0, 5) | 9,653,616 |
| (15, 17) | 7 | 4 | S(11; 0, 4) | 2,839,712 |
| (16, 17) | 8 | 4 | S(12; 0, 4) | 2,839,712 |
| (16, 19) | 8 | 4 | S(12; 0, 4) | 4,952,196 |

Order of the run: the gates; family K; family X in the order of the table.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family K): the numbers of members, of members with (F0) where (F1) and (F2) differ (0), of
  passing members and of passing members with (C1) equal those of the table of the probe at (9, 13), (11, 17) and
  (13, 11); each control holds a pure member.
- G2 (second instrument). For every case with a pure member, Singular 4.3.2 (Plural), with a script generated from the
  stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the formula for beta against omega computed in U (for random alpha at e = 6, t = 2 and e = 7,
  t = 3: the image of f under the substitution x -> y, y -> x, z -> -z, computed with the structure constants of
  `uhlib`, equals y^e + alpha^omega x^t); the enumeration (the order, the index, the number of members, the least
  non-residue) at (8, 7); the complete counts at (8, 7) with t = 2 (4,800 members, 0 where (F1) and (F2) differ, 28
  passing, 18 with (C1)); the exponent of each case; the plan of the cases.

## Predictions

- P1 (a pure pair, confirmed by both instruments). (14, 11): 0.85. (15, 11): 0.85. (15, 13): 0.85. (15, 17): 0.9.
  (16, 17): 0.9. (16, 19): 0.9. (At the four pairs of the probe the passing members are 0.29, 0.34, 0.49 and 0.39
  times 2 p^2.)
- P2 ((F1) and (F2) together). In every case, no member with (F0) satisfies exactly one of (F1), (F2). Confidence 0.95.
- P3 (the theorems, as checks of the computation). Every passing member has the pure Hilbert function (confidence
  0.98; every case has 2t <= p - 1), and every Betti table computed on a passing member with (C1) is pure
  (confidence 0.98). Every Betti table computed on a passing member without (C1) is pure: 0.9.
- P4 (the count). In every case of family X the number of passing members is between 0.1 and 1 times 2 p^2.
  Confidence 0.7.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles its pair
(e, p) over GF(p). A case without a passing member says that no member of this kind passes the filter there, the
list being complete; it says nothing about the other members of the stratum or about other strata. A passing member
without the pure Hilbert function, or a passing member with (C1) and another table, contradicts the reviewed note or
shows an error of the computation.

## Method and budget

- First instrument: the filter of EXP-019 (imported), the staged test and the Betti tables of the routine of EXP-010
  on `code/uhlib`; second instrument: Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 12 worker processes and one hour of wall time; at e = 15 and 16 at most 6 processes for the tests in U.
  Results are stored per case; a case that does not finish is reported with what was done.
- Stored per case: the counts by stage, the number of members with (F0) where (F1) and (F2) differ, every passing
  member (index, alpha, c, beta, the forms c and c' of the filter, (C1), the staged test, the Betti table when
  computed, f and g), the seconds.

## Outputs

`exp020_routine.py`, `run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-check of the decisive members with a separate parser and the module construction of `uhlib`.
