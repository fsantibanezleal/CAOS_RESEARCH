# EXP-009 preflight: the linear family L_e in odd characteristic below 2e, for e = 4 to 7

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (integers
modulo a prime; extension fields by exact tables).

## Question

For e >= 4 and characteristic 0 or at least 2e, every member of the family

    L_e(a, b, c, d) = < x^e + a x y^(e-1) + b y^(e-2) z ,  y^e + c x^(e-1) y + d x^(e-2) z >

lies in the rank locus D_e and the general member is pure (context note `2026-11-20-linear-family-weight-argument.md`,
reviewed). The proof does not apply below characteristic 2e: there <x^e, y^e> is not pure and the characters of the
kernel and cokernel of mu_(3e)(W_0) change. The review of the note nevertheless observed, on samples of 2,000 members
of L_6 over GF(11) and of L_7 over GF(13), that no member has rank of mu_(3e) above r, and that about 72 percent have
rank exactly r. It computed no Betti table there.

Question: in odd characteristic p < 2e, does L_e contain a pure member over GF(p), or over GF(p^2)? One pure member
settles the characteristic p for that e: the point (1,2,2,1) of (0, e, 3e, 4e) is then realized over U in
characteristic p. The family has p^4 members over GF(p), so the search is exhaustive there.

Known before the run (EXP-006): pure pairs exist over GF(3), GF(5), GF(7) at e = 4 and over GF(3) at e = 5, found by
random search in the whole Grassmannian; nothing is known for e = 5 at p = 5, 7 or for e >= 6 below 2e (EXP-008, frozen
the same day and running, searches e = 5 at p = 5, 7 and e = 6 at p = 3 at random).

## Cases (fixed here)

Family X(e, p), exhaustive: all p^4 members of L_e over GF(p), for the fifteen pairs with p < 2e,
e = 4: p = 3, 5, 7; e = 5: p = 3, 5, 7; e = 6: p = 3, 5, 7, 11; e = 7: p = 3, 5, 7, 11, 13; and for five control
pairs where the proposition applies, e = 4: p = 11, 13; e = 5: p = 11, 13; e = 6: p = 13.

For each member: the rank of mu_(3e). For each member of rank exactly r = 2 u(2e) - 2, in the lexicographic order of
(a, b, c, d): the Hilbert function to degree 4e + 2 and, when it is h_e, the Betti table. In a pair (e, p) the second
stage stops once 40 pure members are found; the rank is computed for all members in every case.

Family Y(e, p), only for the pairs (e, p) with p < 2e in which X finds no pure member: 20,000 random members of L_e
over GF(p^2) (seed 20261120 + index, the four parameters uniform in the field), the same computations, stopping at 10
pure members; at most 40 Betti tables are computed per pair.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). L_4(0, 0, 0, 0) is pure over GF(11) and GF(13) and not over GF(3), GF(5), GF(7); L_4(1, 0, 0, 0)
  is pure over GF(13) (EXP-007 lists it pure over the rationals; the review found it pure over GF(13)); in the control
  pairs every member has rank at most r (the proposition), and at least half of the members of rank r whose table is
  computed are pure.
- G2 (second instrument). For every pair (e, p) with a pure member, Singular 4.3.2 (Plural), with a script generated
  from the stored polynomials, gives the pure Betti table on the first five pure members.
- G3 (unit tests) of the family constructor against the printed polynomials, of the enumeration (p^4 members, each
  once), and of the rank routine at e = 6, 7 against the module construction of `uhlib` on five members per field.

## Predictions

- P1 (the inclusion survives). In every pair (e, p) with p < 2e, every member of L_e over GF(p) has rank of mu_(3e) at
  most r. Confidence 0.7 (the review's two samples; no proof).
- P2 (pure members when e < p < 2e). In each of the pairs (4, 5), (4, 7), (5, 7), (6, 7), (6, 11), (7, 11), (7, 13)
  the family has a pure member over GF(p). Confidence 0.55 for each.
- P3 (pure members when p <= e). In the pairs (4, 3), (5, 3), (5, 5), (6, 3), (6, 5), (7, 3), (7, 5), (7, 7), a pure
  member exists over GF(p) or GF(p^2). Confidence 0.3 for each: for p dividing or below e the family is small over
  GF(p) and the monomials x y^(e-1), x^(e-1) y interact with p-th powers.

What would falsify, and what each outcome means: a member of rank above r refutes P1 for that pair (and shows that the
inclusion needs the hypothesis of the proposition). A pair without a pure member over GF(p) and among the members
tried over GF(p^2) says that this family does not settle that characteristic; it says nothing about other pairs of
forms. A pure member found and confirmed by the second instrument settles the characteristic p for that e.

## Method and budget

- First instrument: the routines of EXP-006 and EXP-007 (imported, not edited) on top of `code/uhlib`; second
  instrument: Singular 4.3.2 with Plural through the generator of EXP-005.
- At most 8 worker processes and five hours of wall time. A pair that does not finish is reported with what was done.
- Stored: per pair the distribution of the rank over all members; for the members of rank r examined, the parameters,
  the Hilbert function class and the Betti table; the pure members with their polynomials.

## Outputs

`run.py`, its tests, `artifacts/results.json`, `artifacts/run.log`, `artifacts/singular/`, `results-summary.md`
generated from the results (a table of the pairs (e, p) with the counts and three pure members per pair as
polynomials). The verdict is written by the coordinating session after its own re-check of the pure members.
