# EXP-064: exact finite carrier two-primary groups

Declared 2026-09-20 before computation. Status: **DECLARED, NOT RUN**.
CPU-only exact modular arithmetic and integer determinant bounds.

## Frozen matrices and predictions

For each `p=8,9,10,11`, project the frozen EXP-042 persistent signed matrix to
the row masks `56,58,59,62`. Let `r_(p,m)` be the following frozen EXP-045
rank over `GF(3)`:

| `p` | mask 56 | mask 58 | mask 59 | mask 62 |
|---:|---:|---:|---:|---:|
| 8 | 963 | 980 | 993 | 1002 |
| 9 | 1561 | 1581 | 1596 | 1607 |
| 10 | 2397 | 2420 | 2437 | 2450 |
| 11 | 3526 | 3552 | 3571 | 3586 |

- **P1 (exact rational ranks):** every projected matrix has rational rank
  `r_(p,m)`. Certify this by verifying the same rank over distinct 61-bit
  primes until their product `Q` satisfies
  `Q^2 > 4*d^(r+1)`, where `d` is the maximum projected squared column norm.
- **P2 (complete 2-primary types):** combine P1 with independently frozen
  mod-two ranks and first-Bockstein ranks. The complete 2-primary torsion is

  ```text
  mask 56: (Z/2)^(0,0,0,1)
  mask 58: (Z/2)^(1,2,3,5)
  mask 59: (Z/2)^(3,4,5,7)
  mask 62: (Z/2)^(3,4,5,7)
  ```

  in parameter order `p=8,9,10,11`. Explicitly require
  `rank_Q-rank_F2=rank(first Bockstein)`; do not infer exponent two from a rank
  gap alone.
- **P3 (exact finite triangle images):** combine P2 with EXP-062/063. In masks
  59 and 62, all triangle images form the complete 2-primary subgroup. In mask
  58, the endpoint classes `(0,1,p-3)` and `(0,2,p-4)` vanish integrally, while
  all remaining triangle images form its complete 2-primary subgroup. In mask
  56, every triangle image vanishes for `p=8,9,10`; at `p=11`, only `(2,3,4)`
  is nonzero and it generates the complete 2-primary subgroup.

## Producer and independent audit

1. Verify SHA-256 pins for EXP-042, EXP-043, EXP-045 and EXP-063 code and
   artifacts. Rebuild every row projection from the signed frozen columns.
2. Verify the projected shapes, rank-2/rank-3 values, Bockstein ranks and
   projection hashes against EXP-045 before generating new primes.
3. Use deterministic verified 61-bit primes and high-pivot sparse modular
   elimination. Check the exact squared-Hadamard inequality with Python
   integers after every prime.
4. The auditor independently verifies every prime, product and inequality,
   recomputes every modular rank with low pivots, and reconstructs the Smith/
   Bockstein implication. Include synthetic `[2]` and `[4]` controls, removal
   of the last prime from a minimally covered certificate, and a mutated
   projected entry.
5. Cross-check P3 only by group-theoretic consequences of the persisted
   EXP-062 order-two sources and EXP-063 exact relation spaces. Do not claim
   explicit new integral source coefficients when the exponent argument is
   nonconstructive.

## Resource gate and claim boundary

- Smoke `p=8`: at most 300 seconds and 8 GiB.
- Full producer and independent auditor: each at most 1,200 seconds and 12 GiB,
  one process, with an atomic checkpoint after each parameter.
- Stop on a premise, projection, rank, Bockstein, prime or coverage mismatch.
  A resource stop is inconclusive. Preserve partial and failure artifacts.
- Do not expand beyond the four declared parameters or run HNF/SNF.

A pass is an exact finite integral result. It does not solve the uniform
comparison or the original conjecture and does not by itself trigger a
manuscript or Zenodo revision.
