# EXP-043 hypothesis - exact rational rank by modular Hadamard certificates

Date: 2026-08-31. CPU only. Exact modular arithmetic and integer determinant bounds.

## Predictions

For each EXP-042 isolated matrix, set `r` to its exact `GF(3)` rank and `d` to its maximum column
degree.

### P1. Modular rank ceiling

Generate distinct verified 61-bit primes. Every selected prime has matrix rank exactly `r`:

```text
p=8,9,10,11 -> r=1002,1607,2450,3586.
```

Any rank above `r` refutes the proposed rational rank immediately.

### P2. Exact Hadamard coverage

For each parameter, accumulate `Q=product(q_i)` until

```text
Q^2 > 4*d^(r+1).
```

All `(r+1)` minors are then both divisible by `Q` and smaller than `Q/2`, so they vanish. Together
with the nonzero rank-`r` minor modulo three, this proves `rank_Q(M_p)=r`.

### P3. Complete finite 2-primary torsion

Combine P2 with the independently audited EXP-042 first-Bockstein ranks. The predicted complete
2-primary torsion of the four isolated cokernels is

```text
p=8: (Z/2)^3
p=9: (Z/2)^4
p=10: (Z/2)^5
p=11: (Z/2)^7.
```

An independent auditor must reverify primality, distinctness, every stored modular rank with the
opposite pivot convention, the exact product inequality, and the EXP-042 artifact hashes.

## Resource gate and claim boundary

The `p=8` smoke is capped at 300 seconds and 8 GB. The full matrix-artifact campaign is capped at
1,200 seconds and 12 GB with one parameter checkpoint at a time. A resource stop is inconclusive.
A pass is an exact finite Smith-theoretic result only. It does not prove the sequence, recurrence,
OI/FI compatibility, an all-parameter connecting theorem, or the complete lower strand. No
manuscript or Zenodo gate opens from finite certificates alone.
