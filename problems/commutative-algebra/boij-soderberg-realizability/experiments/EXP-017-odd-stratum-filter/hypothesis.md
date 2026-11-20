# EXP-017 preflight: the pairs (x^e + alpha(xy, z) y, y^e + beta(xy, z) x) for odd e, searched through two congruences, at (9, 11), (9, 13), (11, 7) and (13, 5)

Date: 2026-11-20. Status: frozen before any computation of this experiment on a pair that is not settled. CPU only.
Exact arithmetic (integers modulo a prime).

## Question

For odd e and s = (e - 1)/2 the stratum S((e + 1)/2; 0, (e - 1)/2) of the weight-class note consists of the pairs

    f = x^e + alpha(h, z) y,      g = y^e + beta(h, z) x,      h = xy,   alpha, beta forms of degree s in D = k[h, z]

(up to scalars on f and g). It holds the central pairs and every pure pair found so far for odd e in small
characteristic: at (7, 3), (7, 5), (7, 7) (EXP-010) and at (9, 7) (EXP-014, one pure member among 300,000 random
ones). At (9, 11) and (9, 13) EXP-014 found none among 300,000 random members each; if pure members had there the
density p^(-6) seen at (9, 7), that sample would have held 0.17 and 0.06 of them on average, so it says little.

The working notes `context/2026-11-20-linear-family-structure-working-notes.md` (not reviewed) give a decomposition
of U/(Uf + Ug) into D-modules for these pairs, governed by one form. With z = 1:

    Delta = alpha(h) beta(h + e - 1) - A_(e-1)(h),     X = (h - 2) Delta(h - e - 1),     X' = (h + e) Delta(h + e + 1),

where A_n(h) = h (h + 1) ... (h + n - 1). A probe on settled pairs suggests the following filter, which is NOT
proved and is used here only to choose which pairs to compute in U:

    (F0)  Delta has degree 2s and is coprime to X and to X';
    (F1)  X' alpha = c X  modulo Delta  for a polynomial c of degree at most s;
    (F2)  X beta(h + e - 1) = c' X'  modulo Delta  for a polynomial c' of degree at most s;
    (F3)  c c' is not equal to A_(e-1).

Evidence for the filter, all on settled pairs: the Hilbert function predicted by the decomposition equals the one
computed in U on 600 random members at (5, 3), (5, 5), (5, 7); at (5, 7), the three members with the pure Hilbert
function among 640 random members with a stronger form of (F0) satisfy (F1) and (F2), and among 60 random members with
(F0), (F1), (F2) the pure Hilbert function occurs exactly when (F3) holds or for one special factorization of A_(e-1);
and every one of the 59 pure members of this stratum stored by EXP-010 and EXP-014, at (5, 5), (5, 7), (7, 3), (7, 5),
(7, 7), (7, 11) and (9, 7), satisfies (F0) to (F3). Members with (F0) to (F3) need not be pure: about two in three of
the stored members with the pure Hilbert function that pass the filter have another Betti table or were not tabled.

(F1) and (F2) are 2 (s - 1) = e - 3 conditions on the 2s + 1 = e parameters of (alpha, beta) up to the scaling
(alpha, beta) -> (t alpha, beta/t), which comes from x -> lambda x, y -> mu y. So the members that pass are expected
with density about p^(-(e-3)) among all members, and can be found by a random search of feasible size where a search
in U could not afford the same number of members.

Question: at (9, 11) and (9, 13), the two pairs of e = 9 that the stratum can settle (at (9, 5) the characteristic
divides the modulus 5 of the stratum, which excludes it), does a member that passes the filter have the pure Betti
table? A pure pair confirmed by the second instrument settles its pair (e, p), whatever the status of the filter.
Secondary: the same at (11, 7) and (13, 5), which no theorem or search has reached.

State when this file is frozen: (9, 11), (9, 13), (11, 7), (13, 5) are not settled. EXP-015 (running) examines other
strata at (9, 11) and (9, 13). No computation of any kind was made by the coordinating session for this stratum at
these four pairs.

## Definitions fixed here

- A member: (alpha, beta), two polynomials in h of degree at most s over GF(p), given by their coefficients of
  1, h, ..., h^s. Its pair: f = x^e + sum of gamma_a x^a y^(a+1) z^(s-a) with alpha = sum of gamma_a A_a(h), and
  g = y^e + sum of gamma'_a x^(a+1) y^a z^(s-a) with beta(h - 1) = sum of gamma'_a A_a(h).
- The filter: (F0) to (F3) above, with greatest common divisors and linear algebra over GF(p) (exact).
- r = 2 u(2e) - 2, the pure Hilbert function and "pure" as in EXP-010 (its routine is imported, not edited). Pure
  means: the Betti table computed by `uhlib` is (1, 2, 2, 1) on (0, e, 3e, 4e) and the length is e^3.
- A case with budget B: B random members (uniform coefficients, alpha not zero; seed 20261120 + a fixed index of the
  case). For every member the filter; for every member that passes, the staged test of the pure Hilbert function;
  for the members with the pure Hilbert function, in the order found, the Betti table, until 5 pure members are found
  or 60 tables are computed. A case stops once it has 5 pure members.

## Cases (fixed here)

Family K, controls with known answers (pure members exist in the stratum): (5, 7) with budget 200,000; (7, 5) with
budget 2,000,000; (7, 11) with budget 20,000,000; (9, 7) with budget 60,000,000.

Family Q, the question: (9, 11) with budget 200,000,000 and (9, 13) with budget 400,000,000.

Family X, exploratory, only within the budget of time: (11, 7) with budget 300,000,000; (13, 5) with budget
200,000,000.

Order of the run: gates, family K, family Q in the order (9, 11), (9, 13), then family X.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family K). Each control finds members that pass the filter and, among them, at least one pure
  member. (The budgets are set so that a miss is not a matter of sampling if the density of pure members is within a
  factor 20 of the one observed: about 1 in 300 at (5, 7), 1 in 6,000 at (7, 5), 1 in 47,000 at (7, 11) and 1 in
  300,000 at (9, 7) among all members of the stratum.) And the fixed member: at (9, 7) the pure pair of EXP-014, f = 4
  x^9 + 5 x^4 y^5 + 6 x^3 y^4 z + 3 x^2 y^3 z^2 + 5 x y^2 z^3 + 3 y z^4, g = x^5 y^4 + 3 x^4 y^3 z + 2 x^3 y^2 z^2 + 2
  x^2 y z^3 + 6 x z^4 + 4 y^9, rescaled to the form above, passes the filter.
- G2 (second instrument). For every case with a pure member, Singular 4.3.2 (Plural), with a script generated from the
  stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the conversion between (alpha, beta) and the pair (f, g) against products computed by `uhlib` on
  random members at e = 5; the filter on the 59 stored pure members named above (all pass) and on ten stored members
  that fail it; (F1) by linear algebra against a brute-force search of c on every member of a small case (e = 5, p =
  3); the seed and the order of the members.

## Predictions

- P1 (density of the filter). In every case the share of members that pass (F0) to (F3) is between 0.05 and 2 times
  p^(-(e-3)). Confidence 0.6 (at (5, 7) the probe gave about 0.4 times 7^(-2) among members with (F0)).
- P2 (the question). A pure member is found at (9, 11): 0.5. At (9, 13): 0.5. At least one of the two: 0.65.
- P3 (exploratory). A pure member is found at (11, 7): 0.35. At (13, 5): 0.3.
- P4 (the filter and the Hilbert function). In every case at least half of the members that pass the filter have
  the pure Hilbert function. Confidence 0.6.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles its pair
over GF(p). A case of family Q without a pure member says only that none was found among the members that pass the
filter in a random sample; the filter is not proved to contain every pure member, and the stratum is one of many. A
failure of G1 at a control shows that the filter loses known pure pairs or that the implementation is wrong.

## Method and budget

- The filter with python-flint (polynomials and small matrices over GF(p)); the pure Hilbert function with the rank
  routine of EXP-010 (imported); the Betti tables with `code/uhlib`; second instrument: Singular 4.3.2 with Plural
  through the script generator of EXP-009.
- At most 12 worker processes and three hours of wall time. Results are stored per case as blocks finish; a case that
  does not finish is reported with the number of members done.
- Stored per case: the number of members examined, those passing each of (F0) to (F3) in turn, those with the pure
  Hilbert function, the tables computed, the pure members with alpha, beta, c, c', the polynomials f and g and their
  coefficient vectors (at most 50 members with the pure Hilbert function per case).

## Outputs

`exp017_routine.py`, `run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-check of the decisive members with a separate parser and the module construction of `uhlib`.
