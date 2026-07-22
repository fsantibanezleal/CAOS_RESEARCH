# EXP-057 - The structural lemmas: all-orders solvability and the termination invariant (route N2)

- **Question.** Replace the compute-bound corrector ladder (EXP-056) with structure:
  (i) is every rung solvable for a STRUCTURAL reason; (ii) what forces termination?
- **Motivation (the declared derivation).** A rung solves iff its rhs lies in
  RowSpace(M0) = ker_right(M0)-perp. If M0 has FULL COLUMN RANK (right kernel zero),
  EVERY conceivable rhs is admissible: all-orders solvability follows for free, which
  is exactly what the perfect 276/276 record predicts. An all-t certificate is a
  square 125 x 125 minor with determinant a nonzero polynomial in t whose roots (if
  any) are covered by a second minor. For termination, the ladder's support dynamics
  (each rung's covector support is the previous one shifted by column offsets
  -(p, q) + (1, 1) and row offsets +(P0-monomial) - (1, 1)) must exit the fixed pool
  under a monotone invariant; the candidate is measured, not assumed.
- **Falsifiable predictions.**
  1. [MV] Numeric-t ranks of M0 equal 125 (full column rank) at several rational t.
  2. [MV] A 125 x 125 minor has determinant a NONZERO polynomial in t; its roots (if
     any) are covered by a second minor: rank 125 for ALL t: **ALL-ORDERS SOLVABILITY
     IS PROVED** (lemma i), and the 276/276 record is explained.
  3. [MV] The computed rungs' supports (orders 1-2, persisted) exhibit a monotone
     invariant (candidate: min total degree strictly increasing, or an i - j band
     drift); the measured law is recorded.
  4. [D] If 3 yields a strict monotone bound against the finite pool: TERMINATION AT
     A COMPUTABLE ORDER [D], and the universal covector exists: the reduced stratum
     closes modulo the invariant's formal proof (stated precisely).
- **Method.** sympy; numeric ranks; one or two symbolic minor determinants (sparse
  selection); support statistics from EXP-056 artifacts. Parts under the cap;
  background if needed.
- **Success criterion.** 1-2 verified (lemma i proved); 3 measured; 4 stated.
- **Failure criterion.** Rank < 125 (then compute ker_right explicitly and test the
  Jacobi/annihilation condition directly: the fallback derivation in the log).

Declared 2026-07-22 before the run.
