# EXP-019 preflight: the pairs x^e + alpha(xy, z) y^t, y^e + beta(xy, z) x^t searched through two congruences for every exponent t, at the open pairs (13, 7), (13, 11), (14, 5), (14, 11) and at nine open pairs with e = 15, 16

Date: 2026-11-20. Status: frozen before any computation of this experiment on a pair that is not settled. CPU only.
Exact arithmetic (integers modulo a prime).

## Question

For t with the parity of e, 1 <= t <= e - 2, and d = (e - t)/2, the pairs

    f = x^e + alpha(h, z) y^t,      g = y^e + beta(h, z) x^t,      h = xy,   alpha, beta forms of degree d in D = k[h, z]

are (up to scalars on f and g) the members of the stratum S((e + t)/2; 0, (e - t)/2). EXP-017 searched the case
t = 1 (odd e) through a filter of two congruences and found pure pairs at four open pairs; EXP-018 searched the
largest t allowed by the characteristic at random, which costs a sample of about p^(e-t-2) members in U per member
with the pure Hilbert function and stops being feasible at the pairs that are left: (13, 7), (13, 11), (14, 5),
(14, 11) need e - t - 2 = 8, 6, 10, 8.

The decomposition of U/(Uf + Ug) into D-modules that gave the filter of EXP-017 is the same for every t (working
notes `context/2026-11-20-linear-family-structure-working-notes.md`, not reviewed; the computation below was made by
hand by the coordinating session on 2026-11-20 and is not reviewed either). With z = 1, sigma: h -> h + 1,
A_n(h) = h (h + 1) ... (h + n - 1), w = e + t:

- the module splits over the classes of the index modulo w; the classes of -t, ..., t give cyclic summands and the
  other e - t - 1 classes give summands N_m on two generators v_(-m-t), v_(e-m), 1 <= m <= e - t - 1, with first
  relations (after sigma^m)  alpha a + A_m b = 0,  sigma^m(A_(e-t-m)) a + sigma^(e-t)(beta) b = 0,  of determinant

      Delta = alpha(h) beta(h + e - t) - A_(e-t)(h)        (degree e - t = 2d);

- with X = (h - t - 1)(h - t - 2) ... (h - 2t) Delta(h - e - t) and X' = (h + e)(h + e + 1) ... (h + e + t - 1) Delta(h + e + t),
  the summands of the classes of -t and t are D/(Delta, X, X' alpha) and D/(Delta, X', X sigma^(e-t)(beta)), and their
  length is the one of the pure Hilbert function, e (e - t), exactly when two congruences hold.

The filter, which is NOT proved and is used here only to choose which pairs to compute in U:

    (F0)  Delta has degree 2d and is coprime to X and to X';
    (F1)  X' alpha = c X  modulo Delta  for a polynomial c of degree at most d;
    (F2)  X beta(h + e - t) = c' X'  modulo Delta  for a polynomial c' of degree at most d;
    (F3)  c c' is not equal to A_(e-t).

For t = 1 it is the filter of EXP-017. (F1) and (F2) are d - 1 conditions each, e - t - 2 together.

Evidence, all on settled pairs (probe of the coordinating session, scripts and logs under the data root,
`caos-research/boij-soderberg-realizability/EXP-019-probe/`):

- on every member that EXP-010, EXP-014, EXP-015 and EXP-018 stored in a stratum of this shape with a computed Betti
  table (strata with t = 1 to t = e - 2, e = 5 to 14; the same stratum stored by two experiments is counted twice):
  the 317 pure members pass (F0) to (F3); of the 128 members with the pure Hilbert function and another table, 108
  fail (F0) and 20 fail (F3); none passes;
- random members at four settled pairs: (9, 11) with t = 5: 220 of 100,000 pass, 0.27 times p^(-(e-t-2));
  (9, 13) with t = 3: 12 of 600,000, 0.57 times; (11, 17) with t = 7: 336 of 300,000, 0.32 times; (8, 7) with t = 2:
  27 of 300,000, 0.22 times; all 119 passing members examined have the pure Hilbert function (the staged test of
  EXP-010). The plain test runs at 45,000 to 75,000 members per second on one process.

Question: at the open pairs below, does a member that passes the filter for the largest exponent t that the two
reviewed exclusions allow have the pure Betti table? A pure pair confirmed by the second instrument settles its pair
(e, p) over GF(p), whatever the status of the filter.

State when this file is frozen: (13, 7), (13, 11), (14, 5), (14, 11) and the eleven pairs (15, p), p = 11, 13, 17, 19,
23, 29, and (16, p), p = 17, 19, 23, 29, 31, are not settled; (11, 3) is not settled and is outside this family (the
only exponent with 2t <= p - 1 is t = 1, and 3 divides the modulus 6 of its stratum). No computation was made for any
of these pairs in these strata.

## Definitions fixed here

- A member: (alpha, beta), two polynomials in h of degree at most d over GF(p), given by their coefficients of
  1, h, ..., h^d, alpha not zero. Its pair: f = x^e + sum of gamma_a x^a y^(a+t) z^(d-a) with
  alpha = sum of gamma_a A_a(h), and g = y^e + sum of gamma'_a x^(a+t) y^a z^(d-a) with
  beta(h - t) = sum of gamma'_a A_a(h).
- The filter: (F0) to (F3) above, exact (greatest common divisors and inverses modulo Delta over GF(p)). The stage of
  a member: the number of the tests (F0), (F1), (F2), (F3) it passes in turn, 0 to 4.
- The exponent of a pair (e, p): the largest t of the parity of e with t <= e - 2, 2t <= p - 1 (the note on the
  weight-zero projection excludes the others) and, when p <= e, p not dividing (e + t)/2 (the weight-class note).
- r = 2 u(2e) - 2, the pure Hilbert function and "pure" as in EXP-010 (its routine is imported, not edited, with the
  replacement of its tensor used by EXP-015, EXP-017 and EXP-018). Pure means: the Betti table computed by `uhlib` is
  (1, 2, 2, 1) on (0, e, 3e, 4e) and the length is e^3.
- A case with budget B: B random members (uniform coefficients, alpha not zero; seed 20261120 + a fixed index of the
  case; the members are drawn in blocks, each block from the seed and its own number, so that the member with a given
  index does not depend on the number of processes). For every member that passes the filter, the staged test of the
  pure Hilbert function; the Betti table for the members with the pure Hilbert function, in the order of their
  index, until 5 pure members are found or 40 tables are computed. A case stops once it has 5 pure members (the
  blocks are small enough that a case with many passing members stops soon after).

## Cases (fixed here)

Family K, controls with known answers (pure pairs found by EXP-015 and EXP-018 in these strata):

| (e, p) | t | d | Stratum | Budget |
|---|---|---|---|---|
| (9, 11) | 5 | 2 | S(7; 0, 2) | 100,000 |
| (9, 13) | 3 | 3 | S(6; 0, 3) | 2,000,000 |
| (11, 17) | 7 | 2 | S(9; 0, 2) | 100,000 |
| (13, 17) | 7 | 3 | S(10; 0, 3) | 5,000,000 |

Family X, the open pairs with e <= 14:

| (e, p) | t | d | Stratum | Conditions e - t - 2 | p^(e-t-2) | Budget |
|---|---|---|---|---|---|---|
| (13, 11) | 5 | 4 | S(9; 0, 4) | 6 | 1.8 x 10^6 | 300,000,000 |
| (13, 7) | 3 | 5 | S(8; 0, 5) | 8 | 5.8 x 10^6 | 1,000,000,000 |
| (14, 5) | 2 | 6 | S(8; 0, 6) | 10 | 9.8 x 10^6 | 1,500,000,000 |
| (14, 11) | 4 | 5 | S(9; 0, 5) | 8 | 2.1 x 10^8 | 3,000,000,000 |

Family Y, open pairs with e = 15 and e = 16:

| (e, p) | t | d | Stratum | Conditions | Budget |
|---|---|---|---|---|---|
| (15, 29) | 13 | 1 | S(14; 0, 1) | 0 | 200,000 |
| (16, 29) | 14 | 1 | S(15; 0, 1) | 0 | 200,000 |
| (16, 31) | 14 | 1 | S(15; 0, 1) | 0 | 200,000 |
| (15, 23) | 11 | 2 | S(13; 0, 2) | 2 | 1,000,000 |
| (15, 19) | 9 | 3 | S(12; 0, 3) | 4 | 50,000,000 |
| (16, 23) | 10 | 3 | S(13; 0, 3) | 4 | 50,000,000 |
| (15, 17) | 7 | 4 | S(11; 0, 4) | 6 | 1,500,000,000 |
| (16, 17) | 8 | 4 | S(12; 0, 4) | 6 | 1,500,000,000 |
| (16, 19) | 8 | 4 | S(12; 0, 4) | 6 | 2,000,000,000 |

Not attempted here: (15, 11) and (15, 13) (t = 5, eight conditions: about 2 x 10^8 and 8 x 10^8 members for one that
passes, if the factor is the one seen), and (11, 3).

Order of the run: the gates; family K; the six cases of family Y with d <= 3 in the order of the table; family X in
the order (13, 11), (13, 7), (14, 5); the three cases of family Y with d = 4; (14, 11) last.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). (a) On the stored members named above (every member with a computed table that EXP-010,
  EXP-014, EXP-015 and EXP-018 stored in a stratum S((e + t)/2; 0, (e - t)/2)): every pure member passes the filter
  and no member with another table passes it (317 and 128 by the probe; the counts are recomputed, and a difference
  from these two numbers is reported). (b) Each control of family K holds a pure member. (With the shares seen, the
  budgets of the first three hold about 220, 40 and 110 passing members; at (13, 17) the share was not measured and
  the budget is 60 times p^(e-t-2), so 12 to 35 passing members at the factors seen.)
- G2 (second instrument). For every case with a pure member, Singular 4.3.2 (Plural), with a script generated from the
  stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the conversion between (alpha, beta) and the pair (f, g) for t = 2, 3 against the products
  alpha(xy, z) y^t and beta(xy, z) x^t computed with the structure constants of `uhlib` on random members at e = 6, 7;
  the filter for t = 1 against the filter of EXP-017 on 2,000 random members at (7, 5) and (9, 7) (the same stage);
  (F1) and (F2) through the inverse modulo Delta against the linear algebra of EXP-017 for t = 2 on random members
  of (8, 7); the supports of the strata of (13, 11), (14, 5) and (16, 17) against hand-written lists; the exponent of
  each case from the rule above; the seed and the order of the members; the plan of the cases.

## Predictions

- P1 (family X: a pure pair, confirmed by both instruments). (13, 11): 0.85. (13, 7): 0.8. (14, 5): 0.6.
  (14, 11): 0.55. (The budgets are 170, 170, 150 and 14 times p^(e-t-2); with the factor 0.2 to 0.6 seen, the first
  three hold tens of passing members and the last about 3 to 8; the lower values at (14, 5) and (14, 11) are for the
  small prime, where (F0) removes more, and for the small expected count.)
- P2 (family Y: a pure pair, confirmed by both instruments). (15, 29), (16, 29), (16, 31): 0.9 each. (15, 23): 0.9.
  (15, 19): 0.85. (16, 23): 0.85. (15, 17): 0.7. (16, 17): 0.7. (16, 19): 0.65.
- P3 (the filter and the Hilbert function). Every member that passes the filter, in every case, has the pure Hilbert
  function. Confidence 0.9.
- P4 (the filter and the Betti table). Every Betti table computed on a member that passes the filter is pure.
  Confidence 0.85.
- P5 (the density). In every case where at least 10 members pass, their share among the members examined is between
  0.1 and 3 times p^(-(e-t-2)). Confidence 0.6.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles its pair
(e, p) over GF(p). A case without a passing member, or whose passing members are not pure, says only that none was
found: the filter is not proved to describe the pure members of the stratum, and other strata exist. A passing member
without the pure Hilbert function refutes the reading of (F1), (F2) as the two conditions on the end summands, or
shows that further summands impose conditions for that t.

## Method and budget

- First instrument: the filter with python-flint, the staged test and the Betti tables of the routine of EXP-010
  (imported) on `code/uhlib`; the runner of EXP-017 as the pattern (blocks, seeds, storage per case, resumable);
  second instrument: Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 12 worker processes and five hours of wall time. Results are stored per case as blocks finish; a case that
  does not finish is reported with what was done, and the cases not started are named.
- Stored per case: the counts by stage, the members with the pure Hilbert function (at most 50: index, alpha, beta,
  c, c', f, g, the Betti table when computed), the seconds.

## Outputs

`exp019_routine.py`, `run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-check of the decisive members with a separate parser and the module construction of `uhlib`.
