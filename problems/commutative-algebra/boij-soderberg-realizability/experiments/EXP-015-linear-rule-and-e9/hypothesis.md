# EXP-015 preflight: the rule of the linear family up to e = 13, and the three pairs still open at e = 9

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integers
modulo a prime).

## Question

Two things are left by EXP-009, EXP-010 and EXP-014 (the latter two still closing; the facts used here are counts
re-checked by the coordinating session).

(1) The linear family. The stratum S(e - 1; 0, 1), which contains the four-parameter linear family, was examined in
every member over GF(p) in twelve pairs with e < p < 2e: it holds pure members at (4, 5), (4, 7), (5, 7), (6, 11),
(7, 11), (7, 13), (8, 13), (9, 17), where 2e - p is 1 or 3, and none at (6, 7), (8, 11), (9, 13), (9, 11), where
2e - p is 5 or 7. The prediction "pure members exactly when 2e - p <= 3" was recorded for (8, 11), (8, 13) before
their results were known and held, and it was frozen as P4 of EXP-014 for e = 9 and held. Question: does the rule
hold for e = 10 to 13?

(2) e = 9. After the central pairs (p = 3), EXP-014 (p = 7 in S(5; 0, 4); p = 17 in S(8; 0, 1)) the pairs (9, 5),
(9, 11), (9, 13) are open: S(5; 0, 4) holds no pure member among 300,000 at p = 11, 13 and none of rank r at p = 5,
and S(8; 0, 1) holds none at p = 11, 13. Question: does another admissible stratum hold a pure pair there?

## Definitions fixed here

As in EXP-010 and EXP-014 (weight, strata, members and their number N, r = 2 u(2e) - 2, the pure Hilbert function,
pure). The routine of EXP-010 is imported, not edited. Budget of a case with budget B: all N members when the stratum
has i < j and N <= B, otherwise B random members (seed 20261120 + a fixed index of the case); the Betti table for
the members with the pure Hilbert function until 5 pure members are found or 40 tables are computed; a case stops
once it has 5 pure members.

## Cases (fixed here)

Family L, the stratum S(e - 1; 0, 1), budget 100,000:

| e | p with 2e - p <= 3 | p with 2e - p >= 5 |
|---|---|---|
| 10 | 17, 19 | 13, 11 |
| 11 | 19 | 17, 13 |
| 12 | 23 | 19, 17 |
| 13 | 23 | 19 |

Family R, e = 9, the pairs (9, 5), (9, 11), (9, 13); the admissible strata not yet examined there, with their
budgets:
- S(7; 0, 2): budget 500,000.
- S(6; 0, 3), S(6; 1, 4), S(6; 2, 5): budget 200,000 each.
- S(4; 0, 1): budget 200,000.
- S(3; i, j) for the six pairs i <= j: budget 100,000 each.
- S(2; 0, 1): budget 300,000.
At (9, 5) the strata with m = 5 are left out (EXP-014 found no member of rank r there, and the note on the weight
classes gives a reason).

Family K, controls with known answers (budget 100,000, which is at least N in each): S(8; 0, 1) at (9, 17) (pure
members), at (9, 13) (none); S(7; 0, 1) at (8, 13) (pure members) and at (8, 11) (none).

Order of the run: gates, family K, family L by increasing e, family R in the order (9, 5), (9, 11), (9, 13) with the
strata in decreasing order of m.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family K; the two controls without pure members are enumerated in full, and in the two with
  pure members about a third of the members are pure, so a miss is not a matter of sampling): pure members at
  (9, 17) and (8, 13); no member with the pure Hilbert function at (9, 13) and (8, 11); the member
  f = x^9 + x y^8, g = y^9 + x^7 z over GF(17) is pure.
- G2 (second instrument). For every case with a pure member, Singular 4.3.2 (Plural), with a script generated from
  the stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the supports of S(e - 1; 0, 1) for e = 10 against a hand-written list; N for S(11; 0, 1) at e = 12 and
  p = 23 (553^2 = 305,809); the list of strata of family R against the admissible list of the note for e = 9 (m = 2: (0,1);
  m = 3: all six; m = 4: (0,1); m = 5: (0,4); m = 6: (0,3), (1,4), (2,5); m = 7: (0,2); m = 8: (0,1)).

## Predictions

- P1 (the rule). In family L the stratum holds a pure member in each pair with 2e - p <= 3 ((10, 17), (10, 19),
  (11, 19), (12, 23), (13, 23)) and in no pair with 2e - p >= 5 ((10, 13), (10, 11), (11, 17), (11, 13), (12, 19),
  (12, 17), (13, 19)). Confidence 0.7 for the twelve outcomes together (the rule held in twelve pairs out of twelve;
  no proof). In the pairs with 2e - p >= 5 the stratum is enumerated in full when N <= 100,000 and sampled
  otherwise; a sampled case without a pure member counts as "none found".
- P2 (e = 9). A pure member is found in at least one of (9, 5), (9, 11), (9, 13). Confidence 0.5. For each pair
  separately: 0.3 at (9, 5), 0.35 at (9, 11), 0.35 at (9, 13). The expected share in S(2; 0, 1), about half of
  p^(-12), is far below the budget, so a hit there is not expected; the smaller strata carry the prediction.

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles its pair
(e, p). In family L a pure member in a pair with 2e - p >= 5, or none in a pair with 2e - p <= 3 where the stratum was
enumerated or sampled with thousands of members of rank r, refutes the rule. In family R a pair without a pure
member stays open: the strata were sampled, except those enumerated in full.

## Method and budget

- First instrument: the routine of EXP-010 (imported) on `code/uhlib`; the runner of EXP-014 as the pattern; second
  instrument: Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 16 worker processes and four hours of wall time. Results are stored per case; a case that does not finish
  is reported with what was done. Family L and family K come first; family R uses the time that is left.
- Stored per case: as in EXP-014.

## Outputs

`run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only), `results-summary.md` generated
from the results. The verdict is written by the coordinating session after its own re-check of the decisive members
with a separate parser and the module construction of `uhlib`.
