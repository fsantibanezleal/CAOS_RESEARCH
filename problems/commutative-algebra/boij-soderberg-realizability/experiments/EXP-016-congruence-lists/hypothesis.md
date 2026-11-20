# EXP-016 preflight: the pairs (x^e + b y^e, G(xy, z)) listed by one congruence, for e = 10 to 16 over prime fields and in three cases over a quadratic extension

Date: 2026-11-20. Status: frozen before any computation of this experiment on a pair that is not settled. CPU only.
Exact arithmetic (finite fields).

## Question

The note `context/2026-11-20-one-congruence-and-the-betti-table.md` (a derivation by the coordinating session, under
review when this file is frozen) states, for even e, m = e/2 and a monic form G of degree m in h = xy and z, with
z = 1:

- hypothesis (C) of the note `context/2026-11-20-pairs-over-the-invariants.md` (reviewed);
- the congruence (b): G(h - 2e) B_e(h) = lambda G(h + 2e) A_e(h) modulo G(h) for a nonzero scalar lambda, where
  A_e(h) = h (h + 1) ... (h + e - 1) and B_e(h) = (h - 1) ... (h - e);
- Theorem 1: under (C), the pair (x^e + b y^e, G(xy, z)) has the pure Hilbert function exactly when (b) holds;
- Theorem 2: under (C) and (b) the pair is pure, for every nonzero b;
- Theorem 3: for p = 2e - 1 prime a form with (C) and (b) exists over a finite field of characteristic p.

So the forms G over a finite field GF(q) with (C) and (b) can be listed by testing each of the q^m monic forms with
two polynomial reductions, without any computation in U. Call this list L(e, q).

Question: for which pairs (e, p) with e = 10, 12, 14, 16 and p an odd prime below 2e is L(e, p) not empty, and is
every form of every list a pure pair in U (two instruments)? A form of L(e, p) checked pure in U settles the pair
(e, p) over the prime field, whatever the status of the note. Secondary: three lists over GF(p^2).

State when this file is frozen. Settled by accepted verdicts or reviewed theorems: every odd p below 2e for
e <= 8; at e = 10 the primes 3, 5, 7, 11, 13; at e = 12 the primes 3, 5, 11; at e = 14 the primes 3, 7, 13; at
e = 16 the primes 3, 5, 7. Not settled: (10, 17), (10, 19), (12, 7), (12, 13), (12, 17), (12, 19), (12, 23),
(14, 5), (14, 11), (14, 17), (14, 19), (14, 23), (16, 11), (16, 13) and (16, p) for p >= 17. EXP-015 (running) looks
at another stratum at four of them. EXP-014 examined 150,000 random members of the stratum of these pairs at (12, 7)
and found none with the pure Hilbert function.

Computations already made by the coordinating session with the method of this experiment, all on settled pairs:
the lists L(e, p) for e = 4, 6, 8 named in family A below (their sizes are the known answers of gate G1), and the
Betti tables of the 42 forms of the lists at e = 4 and e = 6. At the pairs (10, 19), (12, 23) and (16, 31) only the
power series of Theorem 3 was computed (to order 8 in lambda); it says nothing about the prime field.

## Definitions fixed here

- A form is a monic polynomial G of degree m over GF(q), given by its coefficients of 1, h, ..., h^(m-1).
- G_j(h) = G(h + j). For 1 <= r <= e - 1: F_r = G_(r-2e) B_(e-r)(h); for -e <= r <= -1: F_r = G_(r+2e) A_(e+r)(h), with
  A_n(h) = h (h + 1) ... (h + n - 1), B_n(h) = (h - 1) ... (h - n). P_plus = G_(2e) A_e, P_minus = G_(-2e) B_e.
- (C): gcd(G_r, F_r) = 1 for every r with 1 <= |r| <= e - 1 and for r = -e, and gcd(G, P_plus) = 1 or
  gcd(G, P_minus) = 1.
- (b): the remainders R_minus, R_plus of P_minus, P_plus modulo G are not zero and R_minus = lambda R_plus for a
  scalar lambda, which is then not zero.
- L(e, q): the forms with (C) and (b), in the order of the enumeration (the coefficient vector read as a number in
  base q, lowest coefficient as the lowest digit; for GF(p^2) the elements a + b t numbered a + b p).
- The pair of a form: f = x^e + y^e and g = G(xy, z) written in the PBW monomials (G = sum gamma_a A_a(h) gives
  g = sum gamma_a x^a y^a z^(m-a)).
- Pure: the Betti table of U/(Uf + Ug) is (1, 2, 2, 1) on (0, e, 3e, 4e) and the length is e^3.

## Cases (fixed here)

Family A, known answers (prime fields): (4, 7), (4, 11), (4, 13), (4, 17), (6, 5), (6, 7), (6, 11), (6, 13),
(6, 17), (8, 3), (8, 5), (8, 7), (8, 11), (8, 13), and (10, 5), where p divides e.

Family B, the question (prime fields, every form):
- e = 10: p = 3, 7, 11, 13, 17, 19.
- e = 12: p = 5, 7, 11, 13, 17, 19, 23.
- e = 14: p = 3, 5, 11, 13, 17, 19, 23.
- e = 16: p = 3, 5, 7, 11, 13; then, only if the time allows, p = 17 and p = 19. (16, 23), (16, 29), (16, 31) are
  not run (more than 7 x 10^10 forms each).

Family X, quadratic extensions (every form): e = 8 over GF(9); e = 6 over GF(169); e = 14 over GF(9).

Family N, negative controls: at (6, 7), (8, 5) and (8, 13), the first five forms in the order of the enumeration
that have (C) and not (b); the length of the module of each.

Verification in U: for every case of families B and X, the first three forms of the list (all of them if fewer)
are checked in both instruments; for family A, the first form of each list.

Order of the run: gates, family A, family N, family B by increasing e and then p, family X, the two optional cases.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers, family A). The sizes of the lists are 1, 2, 16, 13 at e = 4 for p = 7, 11, 13, 17; 2, 2, 4, 0, 2
  at e = 6 for p = 5, 7, 11, 13, 17; 0, 1, 4, 1, 1 at e = 8 for p = 3, 5, 7, 11, 13; 0 at (10, 5). The list at (6, 7)
  is {h^3 + 3, h^3 + 4 h^2 + 3 h + 3}; the list at (8, 5) is {h^4 + 3 h^3 + h^2 + 2}; the list at (8, 13) is
  {h^4 + 11 h^3 + 3 h^2 + 11 h + 6}. (The forms at (6, 7), (8, 5), (8, 13) are those of pure pairs found by EXP-010
  and EXP-014 by search in U.)
- G2 (second instrument). Singular 4.3.2 (Plural), with a script generated from the stored polynomials, gives the
  same Betti table as `uhlib` on every form verified.
- G3 (unit tests): the fast test of (b) against a reference with exact polynomial arithmetic on every form of
  (6, 7) and (8, 5); (C) against the description by roots on every form of (4, 13) (no root in {2, ..., e} or
  {-(e-1), ..., -1}, no two roots differing by 2e, not both 0 and 1 as roots; roots taken in GF(13^2)); the rewriting
  of G in PBW monomials against the powers of xy computed by `uhlib`; the arithmetic of GF(p^2) against python-flint
  on random elements; the enumeration order.
- G4 (the theorem in U). Every form verified in families A, B and X is pure in the first instrument. A form of a
  list that is not pure refutes Theorem 2 or shows an error; the run stops.
- G5 (negative controls). Each of the fifteen forms of family N has a module of length different from e^3.

## Predictions

- P1 (the new pairs). L(e, p) is not empty: 0.75 each at (10, 17), (10, 19), (12, 13), (12, 17), (12, 19), (12, 23),
  (14, 5), (14, 11), (14, 17), (14, 19), (14, 23), (16, 11), (16, 13); 0.4 at (12, 7) (the sample of EXP-014 found
  none; if one form existed the sample would have missed its members with probability about 0.4). At least 9 of
  these 14 lists are not empty: 0.7. Base: the list is not empty in 13 of the 15 cases with e <= 8 and p not
  dividing 2e computed so far (empty at (6, 13) and (8, 3)).
- P2 (the settled pairs of family B). L(e, p) is not empty at (10, 3), (10, 7), (10, 11), (10, 13), (12, 5), and it
  contains the form G of every pure member stored by EXP-014 at these pairs: 0.85 (this holds if every pure pair of
  this shape satisfies (C), which is observed and not proved). At (12, 11), (14, 3), (14, 13), (16, 3), (16, 5),
  (16, 7): not empty, 0.7 each.
- P3 (Theorem 2). Gate G4 passes: 0.95.
- P4 (extensions). L(8, 9) is not empty: 0.6. L(6, 169) is not empty: 0.85. L(14, 9) is not empty: 0.6.
- P5 (sizes). No list over a prime field in family B has more than 3 p forms: 0.7 (the forms lie on a curve; the
  lists so far have at most 16 forms).

What would falsify, and what each outcome means. A form of a list that is pure in both instruments settles its pair
over GF(p), or over GF(p^2) in family X (then the point is realized over a field of characteristic p, not over the
prime field). An empty complete list says that no pair of this shape with (C) is pure over that field; it says
nothing about the pairs of this shape without (C) (none of those computed so far is pure, which is an observation),
about other shapes, or about larger fields. A failure of G4 refutes Theorem 2 as stated. A failure of G1 shows an
error in the implementation or in the counts of the note.

## Method and budget

- A routine of this experiment. The products P_minus and P_plus are linear in the coefficients of G: two integer
  matrices give them for a whole block of forms at once (numpy, integers modulo p), the reduction modulo the monic
  G is a synthetic division on the block, and (b) is the vanishing of the 2 x 2 minors of (R_minus, R_plus) with
  both rows not zero. The forms that pass are then checked exactly, with python-flint: (C) by greatest common
  divisors and (b) by polynomial reduction, which also gives lambda. For GF(p^2) the same with pairs of integer
  arrays (or python-flint for every form, if fast enough).
- First instrument in U: the module construction and `tor.betti` of `code/uhlib` (imported, not edited), over GF(p)
  or GF(p^2). Second instrument: Singular 4.3.2 with Plural through the script generator of EXP-009 (for GF(p^2), a
  ground field with a minimal polynomial).
- At most 8 worker processes and three hours of wall time. Results are stored per case as each finishes; a case that
  does not finish is reported with the part of the enumeration that was done, and its list is then a lower bound.
- Stored per case: e, p, the degree of the field, the number of forms, whether the enumeration is complete, the
  number passing the fast test, the number with (b) and without (C), the list with lambda for each form, and for
  the forms verified the polynomial g, the length and the two Betti tables.

## Outputs

`exp016_routine.py`, `run.py`, the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-check of the decisive forms with a separate script (its own test of (C) and (b), and the module construction of
`uhlib` on the stored polynomials).
