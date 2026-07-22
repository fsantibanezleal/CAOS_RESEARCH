# EXP-056 - Verdict: CONFIRMED 1-2 (100 percent solvability, 276 correctors); prediction 3 REFUTED as declared; PIVOT to the structural route (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`, `artifacts/lambda1-2026-07-22.txt`
(first-order correctors persisted). Runtimes: 1414 s (order 1), 12326 s (order 2),
background per the cap discipline.

## Findings

1. **[MV] Solvability is perfect at every computed order.** 26/26 first-order and
   250/250 second-order correctors exist with the (2,0)-pin (the pairing stays
   exactly 576). Not one equation failed across 276 solves: strong evidence the
   solvability is STRUCTURAL (every rhs lies in RowSpace(M0)).
2. **[MV] Termination at order 2 REFUTED as declared:** 1134/6500 order-3
   combinations nonzero. The profile is monotone (nonzero fraction 100 -> 71 -> 17
   percent) but rung cost grows combinatorially (order 2 took 3.4 hours): the brute
   ladder is compute-bound, not idea-bound.

## The pivot (next round, EXP-057)

Replace rung-climbing with two lemmas: (i) ALL-ORDERS SOLVABILITY: show every ladder
rhs annihilates the right kernel of M0 (a Jacobi/Leibniz argument in the bracket
calculus, the annihilation-lemma pattern that closed Theorems 2-4); (ii) A PRIORI
TERMINATION: the corrector supports live in a fixed finite row pool and each rung
raises the minimum eps-degree, so the series is a polynomial for degree reasons once
supports stabilize (bound the order by the pool diameter). Together they yield the
universal covector WITHOUT computing the rungs: the reduced stratum closes.

## How could this be wrong?

- The 17 percent order-3 residue could hide a genuinely non-terminating direction;
  lemma (ii) must be proved, not extrapolated.
- All computations on the declared row pool (525 rows); pool-boundary effects are the
  standard caveat (enlarge and re-verify at the end).
