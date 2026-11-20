# EXP-011 preflight: machine checks of the central-pair theorem (characteristic p dividing an odd e)

Date: 2026-11-20. Status: frozen before any computation of this experiment beyond the two settled pairs named below.
CPU only. Exact arithmetic (integers modulo a prime).

## Question

The note `context/2026-11-20-central-pair-theorem.md` proves on paper: in characteristic p dividing an odd e, with
s = (e - 1)/2, A and B forms of degree e in x^p, y^p without common factor and l_1, l_2 independent linear forms, the
pair f = A + z^s l_1, g = B + z^s l_2 is pure, with g f - f g = lambda z^e and an explicit minimal resolution
(1 -> (g, f); s_1 = (lambda z^e - f g, f^2), s_2 = (g^2, -(g f + lambda z^e))). The coordinating session checked the
identities, the length and the Betti table at (e, p) = (3, 3) and (5, 5) for three choices of (b, d) with A = x^e,
B = y^e, l_1 = b y, l_2 = d x (settled pairs).

Question: do the instruments of the repository confirm the statement in every case below, among them (7, 7), which is
open, and (9, 3), (11, 11), (13, 13), (15, 3), (15, 5), which were never examined?

## Cases (fixed here)

For each case: (i) the identities in U modulo p, by exact polynomial arithmetic with `uhlib.algebra`: A and B commute
with x and y; g f - f g = lambda z^e; the two syzygies and the relation g s_1 + f s_2 = 0. (ii) The Hilbert function
of M = U/(Uf + Ug) from the ranks of mu_n for e <= n <= 4e - 2, against h_e, and the length e^3. (iii) The Betti table
by `uhlib` (module construction and `tor.betti`) when e <= 9; for e >= 11 it is computed by the first instrument only
if one table takes less than 30 minutes, and otherwise the case is reported with (i), (ii) and the second instrument.
(iv) The Betti table by Singular 4.3.2 (Plural) from a script generated from the stored polynomials.

Family T (the theorem), with A = x^e, B = y^e:

| Case | (e, p) | (l_1, l_2) |
|---|---|---|
| T1, T2 | (3, 3) | (y, x); (x + y, x - y) |
| T3, T4 | (5, 5) | (y, x); (2 y, 3 x) |
| T5, T6, T7 | (7, 7) | (y, x); (3 y, 5 x); (x, y) |
| T8, T9 | (9, 3) | (y, x); (x + y, y) |
| T10 | (11, 11) | (y, x) |
| T11 | (13, 13) | (y, x) |
| T12 | (15, 3) | (y, x) |
| T13 | (15, 5) | (y, x) |

Family G (general central forms), l_1 = y, l_2 = x:

| Case | (e, p) | A, B (with X = x^p, Y = y^p) |
|---|---|---|
| G1 | (9, 3) | A = X^3 + X Y^2, B = Y^3 + X^2 Y + X^3 |
| G2 | (5, 5) | A = X + 2 Y, B = 3 X + 2 Y |
| G3 | (15, 5) | A = X^3 + X^2 Y, B = Y^3 + 2 X Y^2 + X^3 |

For G1 and G3 the routine first checks that A-bar and B-bar have no common factor (their resultant is not zero
modulo p); a case that fails this check is replaced by the same forms with the coefficient of X^3 in B changed to the
next value that passes, and the replacement is reported.

Family N (outside the hypotheses; counts only, no prediction of the table):

| Case | (e, p) | Pair | Why outside |
|---|---|---|---|
| N1 | (5, 5) | x^5, y^5 + x z^2 | l_1 = 0 |
| N2 | (5, 5) | x^5 + y z^2, y^5 + y z^2 | l_1, l_2 dependent |
| N3 | (5, 7) | x^5 + y z^2, y^5 + x z^2 | p does not divide e |
| N4 | (5, 3) | x^5 + y z^2, y^5 + x z^2 | p does not divide e |
| N5 | (9, 3) | A + z^4 y, B + z^4 x with A = X^3, B = X^2 Y (common factor) | A-bar, B-bar not coprime |

For family N: the commutator g f - f g, the Hilbert function to degree 4e + 2 (or the statement that the module is
not of finite length within degree 5e), and the Betti table when the length is finite and e <= 9.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). <x^5, y^5> over GF(11) is pure and over GF(5) is not (Theorem A and EXP-009); the pair
  <x^5 + y z^2, y^5 + x z^2> over GF(5) has the pure Betti table (the check of the coordinating session, to be
  reproduced by this routine, not copied).
- G2 (second instrument). Singular gives the same Betti table as `uhlib` in every case where both are computed.
- G3 (unit tests): the constructor of f and g against hand-written polynomials for T1 and T3; the commutator identity
  on T1; the resultant test on a coprime and a non-coprime pair; the Hilbert function routine on <x^4, y^4> over
  GF(13) against h_4.

## Predictions

- P1. In every case of families T and G: the identities hold, the Hilbert function is h_e, the length is e^3, and
  every Betti table computed, by either instrument, is (1, 2, 2, 1) on (0, e, 3e, 4e). Confidence 0.97 (a proof on
  paper, not yet reviewed, and two checked cases).
- P2. In N1, N2 and N5 the pair is not pure. Confidence 0.9. In N3 and N4 the pair does not have the pure Hilbert
  function. Confidence 0.8 (a probe of binomial pairs on settled cases found none of this shape at (5, 7) and (5, 3)).

What would falsify, and what each outcome means. A case of family T or G with a failed identity, another Hilbert
function or another Betti table refutes the theorem as stated (or shows an error in an instrument: the two
instruments are then compared on that case). All cases confirmed: the statement is machine-checked on these cases,
the point (1, 2, 2, 1) of (0, 7, 21, 28) is realized in characteristic 7 by an explicit pair confirmed in two
instruments, and the same for (0, 9, 27, 36) in characteristic 3; the proof still needs its review. Family N says
only what happens in five cases outside the hypotheses.

## Method and budget

- First instrument: `code/uhlib` (imported, not edited) and a routine of this experiment for the identities and the
  ranks (python-flint). Second instrument: Singular 4.3.2 with Plural through the script generator of EXP-009.
- At most 6 worker processes (EXP-010 is running on the same machine) and three hours of wall time. A case that does
  not finish is reported with what was done.

## Outputs

`run.py` (with its routine), the tests, `artifacts/results.json`, `artifacts/singular/` (scripts only),
`results-summary.md` generated from the results (one row per case: the identities, the Hilbert function against h_e,
the length, the Betti table from each instrument, the time). The verdict is written by the coordinating session after
its own re-check of T5 and T8 with a separate parser and the module construction of `uhlib`.
