# EXP-012 preflight: machine checks of the central-commutator criterion (e = 0 or 1 modulo p), among them the open pairs (6, 5) and (7, 3)

Date: 2026-11-20. Status: frozen before any computation of this experiment on the open pairs. CPU only. Exact
arithmetic (integers modulo a prime).

## Question

The note `context/2026-11-20-central-commutator-criterion.md` states, in characteristic p >= 3 with X = x^p, Y = y^p
and Z = k[X, Y, z]: for f = A + beta_1 x + beta_2 y and g = B + delta_1 x + delta_2 y with A, B in Z_e and the
coefficients in Z_(e-1), D = beta_1 delta_2 - beta_2 delta_1 and n(f) = A^p + beta_1^p X + beta_2^p Y,

- g f - f g = - D z;
- the pair is pure if and only if it is of finite length, if and only if z D, n(f), n(g) have no common zero other
  than the origin;
- so the four explicit pairs of its corollary (cases A, B, C, D) are pure for every e >= 3 with e = 0 or 1 modulo p.

The coordinating session checked the criterion against the pure Hilbert function on 604 pairs of the settled cases
(3, 3), (5, 5), (4, 3), (6, 3) (no disagreement; 24 of 24 Betti tables pure). EXP-011 checks case A.

Question: do the instruments of the repository confirm the corollary in the cases below, among them (6, 5) and
(7, 3), open until now, and does the criterion agree with purity on random pairs of the class?

## Definitions fixed here

- The class V_e over GF(p): the span of the central monomials X^i Y^j z^l of degree e and of the products
  (X^i Y^j z^l) x, (X^i Y^j z^l) y with X^i Y^j z^l of degree e - 1, written in the PBW basis of `uhlib`.
- The criterion holds for a pair when the ideal (z D, n(f), n(g)) of GF(p)[X, Y, z] is zero-dimensional: a Groebner
  basis has a pure power of each of X, Y, z among its leading monomials.
- Pure Hilbert function, pure: as in EXP-010 (ranks of mu_n; the Betti table (1, 2, 2, 1) on (0, e, 3e, 4e) computed
  with `uhlib`).

## Cases (fixed here)

Family X, the explicit pairs of the corollary. For each: the identity g f - f g = - D z; the three identities of the
complex (the two syzygies s_1, s_2 with c = - D z, and g s_1 + f s_2 = 0); the criterion; the Hilbert function
against h_e and the length e^3; the Betti table by `uhlib` and by Singular.

| Case | (e, p) | f | g |
|---|---|---|---|
| B1 | (4, 3) | x^4 + z^2 | y^4 + z^2 |
| B2 | (6, 5) | x^6 + z^3 | y^6 + z^3 |
| B3 | (8, 7) | x^8 + z^4 | y^8 + z^4 |
| B4 | (10, 3) | x^10 + z^5 | y^10 + z^5 |
| B5 | (12, 11) | x^12 + z^6 | y^12 + z^6 |
| C1 | (6, 3) | x^6 + z^3 + y^4 z | y^6 + x^4 z |
| C2 | (10, 5) | x^10 + z^5 + y^6 z^2 | y^10 + x^6 z^2 |
| C3 | (12, 3) | x^12 + z^6 + y^4 z^4 | y^12 + x^4 z^4 |
| D1 | (7, 3) | x^7 + y z^3 + x^3 z^2 | y^7 + x z^3 |
| D2 | (11, 5) | x^11 + y z^5 + x^5 z^3 | y^11 + x z^5 |
| D3 | (13, 3) | x^13 + y z^6 + x^3 z^5 | y^13 + x z^6 |

Family R, random pairs of the class: for each of (4, 3), (6, 3), (6, 5), (7, 3), (7, 7), (8, 7), (9, 3), (10, 3),
200 pairs (f, g) with uniform coefficient vectors on the monomial basis of V_e over GF(p) (seed 20261120 + the index
of the pair in this list). For each pair: the identity g f - f g = - D z, the criterion, the pure Hilbert function;
the Betti table by `uhlib` for the first ten pairs with the pure Hilbert function.

Family N, pairs of the class for which the criterion should fail (counts only):

| Case | (e, p) | Pair | Why |
|---|---|---|---|
| N1 | (7, 3) | x^7 + y z^3, y^7 + x z^3 | case D without the term x^3 z^2 (remark 3 of the note) |
| N2 | (6, 5) | x^6, y^6 + z^3 | n(f) = X^6 vanishes on X = 0, where z D vanishes |
| N3 | (6, 3) | x^6 + y^4 z, y^6 + x^4 z | case C without z^3: everything vanishes at X = Y = 0 |

For family N: the criterion, the Hilbert function to degree 5e (or the statement that the module is not of finite
length within that degree).

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). <x^4 + z^2, y^4 + z^2> over GF(3) and <x^5 + y z^2, y^5 + x z^2> over GF(5) are pure, and
  <x^4, y^4> over GF(5) is not (probes of the coordinating session and EXP-009, reproduced by this routine, not
  copied). The criterion routine returns true on (z^3, X^2 + z^3, Y^2 + z^3) in GF(3)[X, Y, z] and false on
  (z X Y, X^2, Y^2 + z^3).
- G2 (second instrument). Singular 4.3.2 (Plural) gives the same Betti table as `uhlib` in every case of family X.
- G3 (unit tests): the basis of V_e against a hand-written list for (4, 3) and (6, 3); the passage from
  (A, beta_1, beta_2) to the PBW polynomial on B1 and D1; n(f) and D on B1; the identity g f - f g = - D z on C1;
  the criterion routine on the two ideals of G1.

## Predictions

- P1. In every case of family X: the identities hold, the criterion holds, the Hilbert function is h_e, the length is
  e^3, and both instruments give the Betti table (1, 2, 2, 1) on (0, e, 3e, 4e). Confidence 0.93 (a proof on paper,
  not yet reviewed; four settled cases checked).
- P2. In family R, on every pair: the identity holds, and the criterion holds exactly when the pair has the pure
  Hilbert function. Every Betti table computed is pure. Confidence 0.9.
- P3. In family N the criterion fails and the module is not of finite length. Confidence 0.9.

What would falsify, and what each outcome means. A case of family X with a failed identity, a failed criterion,
another Hilbert function or another Betti table refutes the corollary as stated (or shows an error in an instrument:
the two instruments are then compared on that case). A pair of family R on which the criterion and the pure Hilbert
function disagree refutes the equivalence of the theorem. All confirmed: the corollary is machine-checked on these
cases; the point (1, 2, 2, 1) is realized on (0, 6, 18, 24) in characteristic 5 and on (0, 7, 21, 28) in
characteristic 3 by explicit pairs confirmed in two instruments; the proof still needs its review.

## Method and budget

- First instrument: `code/uhlib` (imported, not edited) and a routine of this experiment for the class, the
  identities and the ranks (python-flint); the criterion by a Groebner basis over GF(p) (sympy). Second instrument:
  Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 6 worker processes (EXP-010 is running on the same machine) and three hours of wall time. A case that does
  not finish is reported with what was done.

## Outputs

`run.py` (with its routine), the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results. The verdict is written by the coordinating session after its own
re-check of B2 and D1 with a separate parser and the module construction of `uhlib`.
