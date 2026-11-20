# EXP-018 preflight: the pairs x^e + alpha(xy, z) y^t, y^e + beta(xy, z) x^t with the largest exponent t that the characteristic allows, at (11, 13), (11, 17), (13, 17), (13, 19), (14, 23)

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integers
modulo a prime).

## Question

For t with the parity of e and 1 <= t <= e - 2, the pairs

    f = x^e + alpha(h, z) y^t,      g = y^e + beta(h, z) x^t,      h = xy,   alpha, beta forms of degree (e - t)/2

are (up to scalars on x^e and y^e) the members of the weight-class stratum S((e + t)/2; 0, (e - t)/2): f lies on the
weights 0 and (e + t)/2, g on (e - t)/2 and e. For t = e - 2 this is the stratum of the linear family, for t = 1 the
stratum of the central pairs; at e = 9, t = 5 and t = 3 are S(7; 0, 2) and S(6; 0, 3), where EXP-015 found pure pairs
over GF(11) and GF(13).

Two statements bear on which t can hold a pure pair in characteristic p:

- the note `context/2026-11-20-weight-zero-projection.md` (reviewed): the D-weights of these pairs are e, -t, t, -e,
  so a0 = b0 = t and every member has a module of infinite length when 2t >= p + 1;
- the working notes `context/2026-11-20-linear-family-structure-working-notes.md` (not reviewed) suggest that the
  members with the pure Hilbert function are cut out by e - t - 2 conditions on e - t + 1 parameters, so that their
  density among the members is of the order p^(-(e-t-2)): the larger t, the more frequent.

So for a pair (e, p) with p > e the stratum to search is the one with the largest t of the parity of e such that
2t <= p - 1 and t <= e - 2. Question: at the five pairs below, which are not settled, does that stratum hold a pure
pair over GF(p)? And does the stratum with t + 2, where the proposition applies, hold none?

State when this file is frozen: (11, 13), (11, 17), (13, 17), (13, 19), (14, 23) are not settled (EXP-016 started the
list of another stratum at (14, 23) and did not finish it). No computation was made for the strata of family T at
these pairs. Of family Z, the two strata of the linear family, at (11, 17) and (13, 19), were examined by EXP-015 (no
member with the pure Hilbert function); the three others were not computed.

## Definitions fixed here

As in EXP-010, EXP-014 and EXP-015: the weight, the strata, the members and their number N, r = 2 u(2e) - 2, the pure
Hilbert function, pure (the Betti table computed by `uhlib` is (1, 2, 2, 1) on (0, e, 3e, 4e)). The routine of
EXP-010 is imported, not edited, with the replacement of its tensor of structure constants that EXP-015 and EXP-017
use (each coefficient reduced modulo p before it is stored), which is needed at e = 13. A case with budget B: all N
members when N <= B, otherwise B random members (seed 20261120 + a fixed index of the case); the Betti table for the
members with the pure Hilbert function until 5 pure members are found or 40 tables are computed; a case stops once
it has 5 pure members.

## Cases (fixed here)

Family T, the question (the largest t allowed):

| (e, p) | t | Stratum | Conditions e - t - 2 | Budget |
|---|---|---|---|---|
| (11, 13) | 5 | S(8; 0, 3) | 4 | 1,500,000 |
| (11, 17) | 7 | S(9; 0, 2) | 2 | 100,000 |
| (13, 17) | 7 | S(10; 0, 3) | 4 | 1,500,000 |
| (13, 19) | 9 | S(11; 0, 2) | 2 | 100,000 |
| (14, 23) | 10 | S(12; 0, 2) | 2 | 100,000 |

Family Z, the stratum with t + 2 at the same pairs, where 2(t + 2) >= p + 1 (budget 50,000 each): S(9; 0, 2) at
(11, 13); S(10; 0, 1) at (11, 17) (the stratum of the linear family); S(11; 0, 2) at (13, 17); S(12; 0, 1) at (13, 19);
S(13; 0, 1) at (14, 23).

Family K, controls with known answers (EXP-015): S(7; 0, 2) at (9, 11) (pure members; budget 20,000) and S(6; 0, 3) at
(9, 13) (pure members; budget 1,000,000).

Order of the run: gates, family K, family Z, family T in the order (11, 17), (13, 19), (14, 23), (11, 13), (13, 17).

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family K): pure members in both controls. (EXP-015 found 9 pure members among 8,000 members of
  the first and 2 among 200,000 of the second; with these budgets a miss has probability far below one in a thousand
  at the first, and at the second about one in twenty thousand if the density is the one seen and below one in a
  hundred if it is half of it.) And the member f = - 5 x^9 + 5 x^2 y^7 - 4 y^5 z^2, g = 2 y^9 - 4 x^7 y^2 + 2 x^6 y z
  - 4 x^5 z^2 over GF(11) is pure.
- G2 (second instrument). For every case with a pure member, Singular 4.3.2 (Plural), with a script generated from the
  stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the supports of S((e + t)/2; 0, (e - t)/2) for (e, t) = (11, 5) and (14, 10) against hand-written
  lists (f: x^e and the monomials x^a y^(a+t) z^c with 2a + t + 2c = e; g: y^e and the x^(a+t) y^a z^c); the replaced
  tensor against the original at e = 9; the import of the routine of EXP-010 on the fixed member of G1.

## Predictions

- P1 (the largest t holds a pure pair). (11, 17): 0.8. (13, 19): 0.8. (14, 23): 0.75. (11, 13): 0.5. (13, 17): 0.45.
  (For the three with two conditions the expected share of the pure Hilbert function is of the order p^(-2); for the
  two with four conditions it is of the order p^(-4), about 3.5 x 10^(-5) and 1.2 x 10^(-5), times a constant that
  was between 0.1 and 0.5 in the cases seen, so the budgets give a few members at best.)
- P2 (the proposition). No member of any stratum of family Z has the pure Hilbert function. Confidence 0.97 (it is a
  reviewed proposition; a member with the pure Hilbert function there would refute it).
- P3 (the density). In every case of families T and K where at least 10 members with the pure Hilbert function are
  found, their share among the members examined is between 0.03 and 3 times p^(-(e-t-2)). Confidence 0.5.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles its pair
(e, p) over GF(p). A case of family T without a pure member says only that none was found in the sample. A member
with the pure Hilbert function in family Z refutes the proposition on the weight-zero projection or shows an error.

## Method and budget

- First instrument: the routine of EXP-010 (imported) on `code/uhlib`; the runner of EXP-015 as the pattern; second
  instrument: Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 12 worker processes and two hours of wall time. Results are stored per case; a case that does not finish
  is reported with what was done.
- Stored per case: as in EXP-015.

## Outputs

`run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only), `results-summary.md` generated
from the results. The verdict is written by the coordinating session after its own re-check of the decisive members
with a separate parser and the module construction of `uhlib`.
