# EXP-014 preflight: the middle strata at e = 8, 9, 10, 12 (pairs x^e + b y^e with a form in xy and z, and their odd analogue)

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integers
modulo a prime).

## Question

EXP-010 examined every admissible stratum S(m; i, j) at e = 6 and 7 in the open characteristics (its family Q is
complete for (6, 5), (6, 7), (7, 3), (7, 5); checked by a re-count and a rebuild of nine pure members by the
coordinating session). Two regularities appear in its tables:

- Even e. At (6, 5), (6, 7) and at the control (6, 11) the stratum S(6; 0, 3) holds pure members, the simplest ones
  of the shape f = x^6 + b y^6, g a form of degree 6 in xy and z (weight 3), for example over GF(7)
  f = x^6 + y^6, g = x^3 y^3 + x^2 y^2 z + 3 z^3. At (4, 3) and (4, 5) the stratum S(4; 0, 2) holds pure members. At
  (6, 3), where p divides e, S(6; 0, 3) holds none (no member of rank r).
- Odd e. At (7, 3), (7, 5) and at the control (7, 11) the stratum S(4; 0, 3) holds pure members; at (5, 5) and
  (5, 7) the stratum S(3; 0, 2) does. This is the stratum S((e + 1)/2; 0, (e - 1)/2), with f = x^e + (forms of
  weight (e + 1)/2) and g = y^e + (forms of weight (e - 1)/2); it contains the central pairs when p divides e.
- The linear family S(e - 1; 0, 1) held pure members below 2e in the six pairs with 2e - p = 1 or 3 and in none
  with 2e - p >= 5 (EXP-009).

Question: do these three strata hold pure pairs at e = 8, 9, 10 and 12 in odd characteristic below 2e? Each pure
pair, confirmed by the second instrument, settles its pair (e, p). The pairs (8, 5), (8, 11), (8, 13) and every pair
with e = 9, 10, 12 below 2e that is not covered by the notes on the central commutator and on pull-backs are open.

## Definitions fixed here

As in EXP-010: the weight, the strata, the members of a stratum S(m; i, j) with i < j (pairs of nonzero coefficient
vectors, each normalized by its first nonzero coefficient, N of them), r = 2 u(2e) - 2, the pure Hilbert function
(ranks of mu_n), pure (the Betti table (1, 2, 2, 1) on (0, e, 3e, 4e) computed with `uhlib`). The routine of EXP-010
is imported, not edited.

- E-stratum (even e): S(e; 0, e/2). f lies in the span of x^e, y^e; g in the forms of weight e/2, a space of
  dimension e/2 + 1 spanned by x^(e/2 - c) y^(e/2 - c) z^c. N = (p + 1)(p^(e/2 + 1) - 1)/(p - 1).
- O-stratum (odd e): S((e + 1)/2; 0, (e - 1)/2).
- L-stratum: S(e - 1; 0, 1).

Budget of a stratum with budget B: all N members when N <= B, otherwise B random members (uniform coefficient
vectors on the supports, seed 20261120 + a fixed index of the case). For every member the rank of mu_(3e); when it
is r the remaining ranks of the pure Hilbert function; for the members with the pure Hilbert function, in the order
found, the Betti table, until 5 pure members are found or 40 tables are computed. A stratum stops once it has 5 pure
members.

## Cases (fixed here)

Family K, controls on settled pairs (the answer is known from EXP-010): the E-stratum at (4, 3), (4, 5), (6, 5),
(6, 7), (6, 11) and at (6, 3); the O-stratum at (5, 7), (7, 5), (7, 11); budget 30,000.

Family V, even e, the E-stratum:
- e = 8: p = 3, 5, 7, 11, 13; budget 500,000 (all members in every case).
- e = 10: p = 3, 7, 11, 13 (and p = 5 as a case with p dividing e); budget 300,000.
- e = 12: p = 5, 7; budget 150,000.

Family W, odd e = 9:
- the O-stratum S(5; 0, 4) at p = 7, 11, 13 (and p = 5 as a case with p dividing m); budget 300,000.
- the L-stratum S(8; 0, 1) at p = 11, 13, 17 (all members; N at most 94,249).

Order of the run: gates, family K, family V at e = 8, family W, family V at e = 10, family V at e = 12.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family K). Pure members in the E-stratum at (4, 3), (4, 5), (6, 5), (6, 7), (6, 11) and none of
  rank r at (6, 3); pure members in the O-stratum at (5, 7), (7, 5), (7, 11). The member f = x^6 + y^6,
  g = x^3 y^3 + x^2 y^2 z + 3 z^3 over GF(7) is pure.
- G2 (second instrument). For every case with a pure member, Singular 4.3.2 (Plural), with a script generated from
  the stored polynomials, gives the pure Betti table on the first three pure members.
- G3 (unit tests): the supports of the E-stratum and of the O-stratum against hand-written lists for e = 6 and e = 7;
  N for the E-stratum at (8, 5) (4,686) and the enumeration of a small stratum; the import of the routine of EXP-010
  on one known member.

## Predictions

- P1 (even e, p not dividing e). The E-stratum holds a pure member at (8, 3), (8, 5), (8, 7), (8, 11), (8, 13):
  confidence 0.6 each. At (10, 3), (10, 7), (10, 11), (10, 13) and (12, 5), (12, 7): 0.5 each.
- P2 (p dividing e). At (10, 5) no member of the E-stratum has rank r. Confidence 0.7 (as at (6, 3); P4 of EXP-010).
- P3 (odd e). The O-stratum S(5; 0, 4) holds a pure member at (9, 7), (9, 11), (9, 13): confidence 0.5 each. At
  (9, 5) no member has rank r: 0.7.
- P4 (the linear family). S(8; 0, 1) holds a pure member at (9, 17) and none at (9, 11) and (9, 13). Confidence 0.6
  for the three together (the rule 2e - p <= 3 read off seven pairs; the same rule predicts a pure member at (8, 13)
  and none at (8, 11) in family E of EXP-010, recorded before those results were known).

What would falsify, and what each outcome means. A pure member confirmed by the second instrument settles its pair
(e, p). A stratum enumerated in full without a pure member says that the stratum holds none over GF(p); a sampled
stratum without one says only that none was found. If P1 holds at e = 8 for p = 5, 11, 13, then with the notes on the
central commutator (p = 7) and on pull-backs (p = 3) the point (1, 2, 2, 1) of (0, 8, 24, 32) is realized in every
odd characteristic.

## Method and budget

- First instrument: the routine of EXP-010 (`exp010_routine.py`, imported) on `code/uhlib`; second instrument:
  Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 12 worker processes and four hours of wall time. Results are stored per case as each finishes; a case that
  does not finish is reported with what was done.
- Stored per case: e, p, the stratum, N, the members examined and whether they are all the members, the
  distribution of the rank of mu_(3e), the number of rank r, with the pure Hilbert function, the tables computed,
  the pure members with their polynomials and coefficient vectors (at most 50 with the pure Hilbert function).

## Outputs

`run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only), `results-summary.md` generated
from the results (one row per case; three pure members per case as polynomials). The verdict is written by the
coordinating session after its own re-check of the decisive members with a separate parser and the module
construction of `uhlib`.
