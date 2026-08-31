# EXP-045 hypothesis - complete row-atom carrier lattice

Date: 2026-08-31. CPU only. Exact integer and finite-field arithmetic.

## Question and atom universe

EXP-044 proves that the pivot-dependent `D:B` and `K:C0` atoms are necessary row-projection
interfaces but that their union is insufficient. The isolated matrices have exactly six
normalized row atoms. Give them stable aliases in sorted semantic order:

```text
R0 = ["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]
R1 = ["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]
R2 = ["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]
R3 = ["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]
R4 = ["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]
R5 = ["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]
```

For each frozen `p=8,9,10,11` matrix, retain every one of the `2^6=64` row-atom subsets, keep all
columns including zero columns, and compute exact ranks over `GF(2)`, `GF(3)`, and `GF(5)` plus
the first-Bockstein rank in opposite reduction conventions.

## Predictions

### P1. Six-way essentiality

Deleting any one atom from the full presentation kills the first Bockstein for every parameter.
Thus all six semantic row atoms are individually necessary under row projection.

### P2. Unique full carrier

The full six-atom set is the only subset with nonzero Bockstein. It has ranks `3,4,5,7`; every
proper subset has rank zero. A refutation must report every inclusion-minimal subset with nonzero
Bockstein and every inclusion-minimal subset carrying the full source rank.

### P3. Cross-parameter carrier stability

The family of inclusion-minimal nonzero and full carriers is identical across `p=8,...,11`.
Forward/high and reverse/low reductions agree, both odd fields agree, and the odd-minus-two rank
gap equals the first-Bockstein rank for every subset.

## Audit and claim boundary

The runner verifies all frozen EXP-042 matrix hashes and the EXP-044 result hash. The independent
auditor must reconstruct all 256 projected matrices without calling the runner's projection code,
use reverse columns and low row pivots, and verify the complete subset table and minimal-carrier
antichains.

The `p=8` smoke is capped at 300 seconds and 8 GB. The full campaign is capped at 1,800 seconds
and 20 GB, checkpointed by parameter. A resource stop is inconclusive. Even a complete pass is a
finite row-projection theorem, not a unimodular equivalence, compatible family map, recurrence,
or all-parameter lower-strand theorem. No manuscript or Zenodo gate opens from this result alone.
