# EXP-144 verdict: exact in-house check of Long's rank-two Poisson counterexample

Date: 2026-11-14. Hypothesis: `hypothesis.md` (frozen, unedited). Run: `run.py`, exit 0, 77 s, one process.

**Verdict: PASS.** All five predictions and both controls hold. Long's map `(R, T, D, S)` (arXiv:2608.23777v1, equations
(12) to (19)) is, as transcribed and recomputed exactly over Q, a Poisson endomorphism of `P_2` with `det JF = 1`, whose
fiber over `(0, 1/8, 0, 0)` is exactly the three printed rational points, and it is not an automorphism.

Source pin: PDF SHA-256 `5dd5861194bfea9130cddc10919510b060dab663f3a00222e57014125db5051a` (matched by `run.py`, which
exits 2 otherwise). Formulas were transcribed from the PDF page images (pages 4 and 5), never from the `.txt`.

## Bracket convention

Equation (8), page 3: `{f, g} = f_p g_x - f_x g_p + f_z g_q - f_q g_z` in the order `(x, q, p, z)`, so `{p, x} = {z, q} = 1`.
Page 3 (proof of Lemma 2.1): `Omega_0^(-1) = -Omega_0`; the random-point route uses this matrix, and `run.py` asserts it
equals the matrix of generator brackets computed by `bracket()`.

## Prediction table

| ID | Outcome | Evidence (`artifacts/run-log.txt`, `artifacts/results.json`) |
|---|---|---|
| P1 | PASS | Terms and degrees of beta, y, R, S, T, H, D = (4,3), (5,4), (2,3), (22,11), (47,15), (137,23), (139,23), identical to the table on page 5; `R - x(2 - 3xq)` expands to 0 |
| P2 | PASS | Symbolic bracket matrix of (R,T,D,S) equals that of (x,q,p,z), 0 mismatching entries; `{D,R} = {S,T} = 1`, the four mixed brackets 0; second route (Fractions, no sympy simplification, 50 points, seed 20261114): `JF Pi JF^T - Pi` has 0 nonzero entries |
| P3 | PASS | `det JF = 1` symbolically (Berkowitz, expanded) and at the same 50 points (single value 1) |
| P4 | PASS | Lex Groebner basis in 0.29 s: `2x - 3q`, `729q^2 + 256z + 32`, `q(64z + 89)`, `24p + 48z + 5`, `(8z + 1)(64z + 89)`; zero-dimensional; quotient dimension 3 equals the 3 distinct solutions, so the ideal is radical; solutions equal the three points of (7); each satisfies R=0, T=1/8, D=0, S=0 exactly |
| P5 | PASS | `factor_list(R) = (-1, [(x,1), (3qx - 2, 1)])`, reducible; fiber of 3 points, so not injective |
| C1 | PASS | With `D0`: `{D0,R} = 1` (the paper's (44), page 8) but `{D0,S}` and `{D0,T}` are nonzero polynomials; the checker reports failure (symbolic and random route, 20 nonzero entries at 5 points) |
| C2 | PASS | `125 -> 126` in H: the checker reports failure, 4 failing matrix entries (symbolic), 20 nonzero entries at 5 points (random route) |

The kill criterion for P4 did not trigger (0.29 s against 45 minutes).

## Adversarial-validation record

- Faithfulness of the transcription: P1 matches seven independent term counts and degrees, and P2 to P4 would fail on a
  wrong coefficient (C2 shows a single coefficient change is detected). No correction against the PDF was needed; the first
  transcription passed.
- Detection power of the checker: C1 and C2 fail as predicted, on both routes.
- Two independent routes for P2 (sympy symbolic brackets; Fraction evaluation of JF) and for P3 (sympy Berkowitz; Fraction
  elimination); P4 by Groebner basis, by sympy `solve` on the basis, and by substitution of the printed points.
- The P4 radical claim rests on quotient dimension 3 = number of distinct solutions (3), counted from the leading monomials
  of the lex basis.

## Consequence for the cascade paper's Poisson row

The row "PC(n) false for every n >= 2" can carry machine-verified [MV] for n = 2: Long's map is an exact, in-house verified
Poisson endomorphism of `P_2` that is not an automorphism, so PC(2) is false. The step to every n >= 2 by padding with
identity canonical pairs is not computed here and stays the cascade paper's own [D] step. The five textbook facts used in
P5 are [D].

## How could this be wrong?

- The bracket convention: if the intended convention had the opposite sign, the same checks apply to the transposed matrix;
  `{D,R} = 1, {S,T} = 1` would read `-1` and the matrix `Pi` flips sign, so JF Pi JF^T = Pi is unchanged. The conclusion is
  convention-independent for the Poisson property, but the stated `{D,R} = 1` is for the page-3 convention.
- A transcription error that preserves seven term counts, degrees, the Poisson identities, det 1 and the fiber is
  implausible; the Poisson identities are a very strong consistency check on the formulas.
- This is an exact computation over Q of the printed formulas only; it does not verify the paper's proofs, the Weyl-algebra
  appendix (out of scope) or the padding step, and it does not check the formulas against any other printed version
  than arXiv v1.
- The radical claim uses the quotient-dimension count; it is a finite exact computation, but its code is sympy's, trusted
  as in the other experiments.
