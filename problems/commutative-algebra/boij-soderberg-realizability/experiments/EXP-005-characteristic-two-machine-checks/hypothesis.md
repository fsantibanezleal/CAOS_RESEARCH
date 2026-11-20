# EXP-005 preflight: the machine checks of the characteristic 2 theorem and of the family at e = 6 and 7, run with the repository's instrument and archived

Date: 2026-11-20. Status: frozen before any computation of this experiment. CPU only. Exact arithmetic (finite fields
by exact tables or integers modulo a prime; the rationals as fractions).

## Question

Two statements of the programme are proved on paper and reviewed, and the manuscript (v0.01) states them as theorems:

- S1 (the characteristic 2 theorem; context note `2026-11-19-characteristic-two-general.md`). Over a field of
  characteristic 2, let e >= 2, a >= 1 and 0 <= b <= a + 1, and let F_1, ..., F_b be arbitrary elements of (U_e)^a,
  U = U(H). Then M = U^a / (U F_1 + ... + U F_b) has infinite length.
- S4 (the family). U/U(x^e, y^e) has the pure resolution of type (0, e, 3e, 4e) with Betti table (1, 2, 2, 1) if and
  only if the characteristic is 0 or at least 2e.

The independent machine checks that the reviewers ran for them (pairs of quartics and quintics over GF(2), GF(4) and
GF(16), all 651 two-dimensional spaces of cubics over GF(2), matrices of cubics, the examples with b = a + 2, the family
at e = 6 and 7) used scratch code that was deleted at the end of each review; the repository archives only the cases of
EXP-002 and EXP-003 (quadrics exhaustively over GF(2) and GF(4), the family for e <= 5 and the primes up to 23). Does
the repository's own instrument reproduce every one of those checks, with artifacts that a reader can rerun?

This experiment adds no statement. A proof is not made more true by a computation; the computation guards the proof
against an error in a step and gives the manuscript an artifact to cite for each machine claim.

## Derived predictions (from the context note, before any run)

- S2 (the eventual Hilbert function). Write e = 2m or e = 2m + 1 and L.L = 2 m^2 (e even) or 2 m (m + 1) (e odd). For
  a presentation with b = a + 1 whose degeneracy locus on the quadric surface is finite, dim M_n = (a (a + 1) / 2) L.L
  for every large n, in both parities of n. The values used below: a = 1: e = 2, 3, 4, 5, 6, 7 give 2, 4, 8, 12, 18,
  24; a = 2: e = 2, 3 give 6, 12; a = 3: e = 2 gives 12.
- With b <= a, or with a positive-dimensional degeneracy locus (possible over a small field), the Hilbert function
  grows without bound; it is never eventually zero.
- S3 (sharpness of b <= a + 1). With b = a + 2 general relations the module has finite length in characteristic 2.

## Cases (fixed here; a random case is drawn with the seed 20261120 + its index in its family)

| Family | Field | a, b, e | Cases | Degree bound D |
|---|---|---|---|---|
| C1a | GF(2) | 1, 2, 2 | all 35 two-dimensional subspaces of U_2 (known answers of EXP-003) | 18 |
| C1b | GF(2) | 1, 2, 3 | all 651 two-dimensional subspaces of U_3 | 18 |
| C1c | GF(2) | 1, 1, 3 | all 63 one-dimensional subspaces of U_3 | 18 |
| C2a | GF(2), GF(4), GF(16) | 1, 2, 4 | 120 random pairs per field | 24 |
| C2b | GF(2), GF(4), GF(16) | 1, 2, 5 | 120 random pairs per field | 28 |
| C2c | GF(16) | 1, 2, 6 | 10 random pairs | 30 |
| C2d | GF(16) | 1, 2, 7 | 10 random pairs | 32 |
| C2e | GF(2), GF(4), GF(16) | 2, 3, 3 | 20 random 2 by 3 matrices per field | 22 |
| C2f | GF(16) | 2, 3, 2 | 20 random 2 by 3 matrices | 20 |
| C2g | GF(16) | 3, 4, 2 | 5 random 3 by 4 matrices | 18 |
| C3 | GF(16) | (1, 3, 2), (1, 3, 3), (1, 3, 4), (2, 4, 2) | 10 random presentations per shape | 24 |
| C4 | QQ and every prime p <= 31 | U/U(x^e, y^e), e = 6, 7 | 2 by 12 = 24 modules | as in EXP-003, claim C3 (the Betti table through Tor against the resolution of the trivial module) |

GF(4) = GF(2)[w]/(w^2 + w + 1) and GF(16) = GF(2)[w]/(w^4 + w + 1). A random form has independent uniform
coefficients on the monomial basis of U_e used by `uhlib`.

Classification of a computed Hilbert function h(0..D) of a module generated in degree 0:

- finite length: h(n) = 0 for some n <= D (then it is 0 from there on);
- eventually constant with value c: h(n) = c > 0 for the last six computed degrees;
- growing: neither, and h(D) >= h(D - 6) > 0;
- anything else is recorded as unclassified with its function, and counts against P2.

## Gates (a failed gate stops the run and no verdict is drawn until it is explained)

- G1 (known answers). On the 35 subspaces of C1a the Hilbert functions agree, case by case, with those stored by
  EXP-003 (`artifacts/results.json`), up to the smaller of the two degree bounds.
- G2 (two code paths). The Hilbert function routine of this experiment and the module construction of `uhlib`
  (`quotient_module`) give the same function up to degree 12 on 40 random presentations per field over GF(2), GF(4),
  GF(16) and GF(32003), ten each of the shapes (a, b, e) = (1, 2, 3), (1, 2, 4), (2, 3, 2), (1, 3, 2).
- G3 (second instrument). Singular 4.3.2 (Plural), with scripts generated from the stored relations and sharing no
  arithmetic code with the first instrument, gives the same Hilbert function up to the degree bound on a fixed
  sample: the first ten cases of C2a over GF(2) and over GF(4), the first ten of C2e over GF(2), the first five of
  C2b over GF(16), all 40 of C3, and the 24 modules of C4 (for these, the Betti table).
- G4 (unit tests). Tests of the field arithmetic of GF(4) and GF(16) (the field axioms, exhaustively), of the
  Hilbert function routine on modules with known functions (U itself, U/(x, y), U/U(x^e, y^e) for e = 2, 3 over
  GF(32003)), and of the classifier.

## Predictions

- P1. No case of C1 or C2 has finite length. (This is S1. A finite length case would be a defect of the instrument or
  a refuted proof: the run stops and the case is examined before anything else is done.)
- P2. Every case of C1 and C2 with b = a + 1 that is eventually constant has the value of S2, and no case is
  unclassified. Over GF(16) at most 5 percent of the random cases grow; over GF(2) a larger share may (a
  positive-dimensional degeneracy locus is possible over a small field). Every case of C1c (b = a) grows.
- P3. In each of the four shapes of C3 at least 8 of the 10 presentations have finite length.
- P4. For e = 6 the module of C4 has the pure Betti table (1, 2, 2, 1) on (0, 6, 18, 24) exactly over QQ and for
  p = 13, 17, 19, 23, 29, 31, and for e = 7 the pure table on (0, 7, 21, 28) exactly over QQ and for p = 17, 19, 23,
  29, 31; for the other primes up to 31 the table is not that one. The Betti table is computed by the first instrument
  as in EXP-003 (claim C3) and by the second instrument in G3.

What would falsify: a finite length case in C1 or C2 (P1); an eventually constant value other than the predicted one,
or different values in the two parities (P2); fewer than 8 finite length cases in a shape of C3 (P3, a statement about
general presentations: examined before any conclusion); a prime on the wrong side of 2e (P4).

## Method and budget

- First instrument: `code/uhlib` (the algebra, the fields) with a Hilbert-function routine for a presentation
  U(-e)^b to U^a that computes, degree by degree, the rank of the span of the left multiples of the relations; over
  GF(2^k) the linear algebra may use exact lookup tables or bit operations, never floating point.
- Second instrument: Singular 4.3.2 with Plural in WSL, as in EXP-003 (`singular_i2.py`).
- At most 8 worker processes, at most 20 minutes per case, at most four hours of wall time in total. A case that
  reaches its limit is recorded as unfinished with what was computed, and is not counted for or against a prediction.
- Every case is stored with its field, shape, seed and relations, so that it can be rebuilt without the generator.

## Outputs

`run.py`, the routine and its tests; `artifacts/results.json` (one record per case: field, shape, seed, relations,
Hilbert function, classification; the gate outcomes; the counts per prediction), `artifacts/run.log`,
`artifacts/singular/` (the generated scripts of G3) and `results-summary.md` generated from the results. The verdict
is written by the coordinating session after its own re-checks.
