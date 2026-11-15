# EXP-144 - Exact in-house check of Long's rank-two Poisson counterexample

Date: 2026-11-14. Frozen before any code of this experiment is written or run.

- **Question.** C. D. Long, arXiv:2608.23777v1 (2026-07-22), Theorem 1.1, gives explicit polynomials `R, T, D, S` in
  `Q[x, q, p, z]` and states that `(x, q, p, z) -> (R, T, D, S)` is a Poisson endomorphism of the canonical Poisson
  algebra `P_2` that is not an automorphism, with Jacobian determinant 1 and a fiber over `(0, 1/8, 0, 0)` of exactly
  three points. The programme records the result as read in the primary text [V] (`context/2026-11-07-jcb102-reading.md`).
  Do the stated identities hold when recomputed exactly from the printed formulas?
- **Motivation.** The cascade paper (`manuscripts/jacobian-conjecture/cascade`) states the Poisson row "PC(n) false for
  every n >= 2" on Long's authority. The independent audit of 2026-11-10 (CAOS_MANAGE
  `wip/caos-research/msaudit-jac-2026-11-10.md`, D1 improvement plan item 1) asks for an exact in-house check in the
  EXP-136 style so that the row can carry machine-verified [MV], not only [V]. Methodology 03: claims imported from the
  literature are re-verified against the primary record.
- **Source.** The arXiv v1 PDF archived under the data root, `caos-research/jacobian-conjecture/sources/jcb102/2608.23777.pdf`
  (its SHA-256 recorded in the artifacts). The polynomials are transcribed from equations (12) to (19) of the PDF; the
  text extraction next to it loses exponents and Greek letters and is not a source for formulas.

## Falsifiable predictions (exact rational arithmetic, sympy)

1. **P1, transcription.** The transcribed polynomials reproduce the sizes printed under (19): nonzero terms 4, 5, 2, 22,
   47, 137 and 139 and total degrees 3, 4, 3, 11, 15, 23 and 23 for the seven expressions of that table, and `R`
   expands to `x(2 - 3xq)` in `(x, q, p, z)` (Lemma 3.1).
2. **P2, Poisson endomorphism.** With the canonical Poisson structure of the paper (Section 2, the matrix `Omega_0` in the
   coordinate order `(x, q, p, z)`), the bracket matrix of `(R, T, D, S)` equals that of `(x, q, p, z)`; equivalently
   `{D, R} = {S, T} = 1` and `{R, S} = {R, T} = {D, S} = {D, T} = 0` with the paper's sign convention. Checked
   symbolically, and by a second route that evaluates `JF Omega_0^(-1) JF^T - Omega_0^(-1)` at 50 random rational points
   (seed 20261114) with exact fractions.
3. **P3, volume.** `det JF = 1` identically.
4. **P4, fiber.** The ideal `(R, T - 1/8, D, S)` of `Q[x, q, p, z]` is zero-dimensional, and its zero set over the
   complex numbers is exactly the three points printed in (7), all rational: the reduced lex Groebner basis of the
   radical has exactly three solutions, each equal to one printed point, and each printed point satisfies the four
   equations exactly.
5. **P5, not an automorphism.** `R = x(2 - 3xq)` is reducible, so `(R, T, D, S)` cannot be an automorphism (every
   coordinate of a polynomial automorphism is irreducible); P4 gives the same conclusion independently, since an
   injective map has fibers of at most one point.
6. **Control C1.** Replacing `D` by the uncorrected `D0` of (17) keeps `{D0, R} = 1` (the paper's (44)) but makes at
   least one of `{D0, S}`, `{D0, T}` nonzero; the checker of P2 must report that failure.
7. **Control C2.** Changing one coefficient of `H` in (18) (the constant `125` to `126`) must make P2 fail.

## What PASS and FAIL prove

- PASS: the Poisson row of the cascade can carry [MV] for `n = 2`: Long's map is an exact, in-house verified Poisson
  endomorphism of `P_2` that is not an automorphism, so PC(2) is false, and PC(n) is false for every `n >= 2` by the
  standard padding with identity canonical pairs (a [D] step stated in the cascade paper).
- FAIL of P1: a transcription error; corrected against the PDF and rerun before any reading (no claim from a failed
  transcription).
- FAIL of P2, P3 or P4 after P1 passes: a discrepancy with the paper; reported as such, the row keeps [V] with the
  discrepancy stated, and the author's formulas are re-read before any conclusion.

## Premise dependencies

- The standard facts used in P5 (coordinates of automorphisms are irreducible; injective maps have singleton fibers)
  are textbook [D]; the padding to `n >= 2` is the cascade paper's own [D] step.
- No earlier verdict is a premise; the polynomials come from the primary source only.

## Compute budget and kill criterion

One hour of wall time, one process. If the Groebner basis of P4 does not finish within 45 minutes, P4 is decided
instead by substituting each printed point (membership) and by a resultant elimination giving a univariate polynomial
whose rational roots are counted; if neither finishes, P4 is reported undecided and the fiber statement stays [V].

## Invariant-first note

The Jacobian determinant alone (P3) cannot decide the Poisson property (many volume-preserving maps are not
symplectic); the bracket matrix (P2) is the deciding invariant, and the reducibility of `R` (P5) is the cheapest
certificate of non-automorphism.
