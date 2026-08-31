# EXP-043 proof record - exact rational ranks and complete finite 2-primary torsion

Date: 2026-08-31. Status: **CONFIRMED** finitely for `p=8,...,11`. CPU-only exact modular and
integer arithmetic.

## Certificate theorem

Let `M` be an integer matrix, let `r` be a candidate rank, and let `d` be the maximum number of
nonzeros in a column. Every `(r+1)` square minor has absolute value at most
`d^((r+1)/2)` by Hadamard's inequality.

If distinct primes `q_i` all give `rank_GF(q_i)(M)<=r`, every `(r+1)` minor is divisible by their
product `Q`. The exact integer inequality

```text
Q^2 > 4*d^(r+1)
```

then puts the absolute value of every such minor below `Q/2`, forcing it to be zero. A rank-`r`
minor nonzero modulo three supplies the lower bound, so `rank_Q(M)=r`.

## Exact results

The selected 61-bit numbers are distinct and pass deterministic Miller--Rabin verification in the
64-bit range. Every modular rank equals the declared `GF(3)` rank. Each prime list is the shortest
prefix satisfying the exact squared Hadamard inequality.

| `p` | max column degree | `rank_Q(M_p)` | primes | product bits | complete 2-primary torsion |
|---:|---:|---:|---:|---:|---|
| 8 | 13 | 1002 | 31 | 1891 | `(Z/2)^3` |
| 9 | 15 | 1607 | 52 | 3172 | `(Z/2)^4` |
| 10 | 17 | 2450 | 83 | 5063 | `(Z/2)^5` |
| 11 | 19 | 3586 | 125 | 7625 | `(Z/2)^7` |

P1 and P2 pass. For P3, Smith normal form gives

```text
number of even nonzero factors = rank_Q(M_p)-rank_GF(2)(M_p).
```

These differences are `3,4,5,7`. EXP-042 proves that the first Bockstein has exactly those ranks,
so every even nonzero factor has 2-adic valuation one. Therefore the displayed elementary
2-groups are the complete 2-primary torsion of the four isolated cokernels. No additional factor
divisible by four is possible.

## Independent audit

The auditor:

1. verifies every matrix and result hash;
2. rechecks all 291 primes for primality and distinctness;
3. recomputes all 291 ranks with the opposite pivot convention;
4. reconstructs every exact prime product and squared Hadamard inequality;
5. verifies that deleting the last prime destroys coverage, so each prefix is minimal; and
6. recomputes the modulo-three lower rank and the EXP-042 Bockstein comparison.

The primary artifact SHA-256 is
`612d481eff7e00f5c5128d450a5eb05f79aacccb27bcd88c106dc0d5bf7426e6`. The audit certificate
has internal hash `16aaf97b3ae3c9b904d005d3b846df948aaa3935eedea896a34db73d0c2db5a0` and external SHA-256
`6bad2a878e72b54fd3f2db704cb90dff425aff06531cc55ccdd2fde6cff5f01e`.

## Scope and next route

This is a complete exact finite 2-primary theorem for the isolated matrices, obtained without a
full Smith computation. It does not prove the values for arbitrary `p`, the degree-six relation,
the fitted recurrence, or the full lower strand.

The high/low-pivot representative change in EXP-042 suggests that the torsion is carried by a
signed bridge between the normalized `D:B` and `K:C0` row families. The next experiment should
test relative row projections and then construct an integral matched-block reduction of that
bridge. Only a uniform reduction or compatible `p -> p+1` chain map can support an all-parameter
theorem. The finite result alone does not trigger a manuscript or Zenodo update.
