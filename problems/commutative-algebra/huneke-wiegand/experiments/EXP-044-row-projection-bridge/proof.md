# EXP-044 proof record - row-projection localization of the signed bridge

Date: 2026-08-31. Status: **REFUTED overall**, with P1 and P3 confirmed finitely for
`p=8,...,11`. CPU-only exact integer and finite-field arithmetic.

## Construction

The runner verifies the frozen EXP-042 script, result, and four signed matrix artifacts before
loading them. In each matrix it identifies the two pivot-dependent representative atoms

```text
D:B  = ["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]
K:C0 = ["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]
```

and forms four exact row projections: delete either atom, delete both, and retain only their
union. Zero columns remain in the presentations. Every projected matrix is reduced over
`GF(2)`, `GF(3)`, and `GF(5)`, and its first Bockstein is computed in both column orders.

## Exact results

The three field ranks agree in every projected matrix. The common ranks and Bockstein ranks are:

| `p` | delete `D:B` | delete `K:C0` | delete both | only union | all projected Bocksteins |
|---:|---:|---:|---:|---:|---:|
| 8 | 510 | 987 | 495 | 915 | 0 |
| 9 | 802 | 1588 | 783 | 1493 | 0 |
| 10 | 1205 | 2426 | 1181 | 2304 | 0 |
| 11 | 1742 | 3557 | 1713 | 3403 | 0 |

Therefore P1 passes: removing either marked atom eliminates the full finite Bockstein, so each is
necessary in the row-projection sense. P2 is refuted: their union alone also has Bockstein zero,
not `3,4,5,7`. P3 passes: forward/reverse reductions agree, the two odd fields agree, and every
odd-minus-two rank gap equals the computed Bockstein rank, namely zero.

The logical conclusion is narrower than an integral normal form. The marked atoms are necessary
interfaces but not a sufficient two-atom carrier. At least one additional row atom participates
essentially in the signed circuit visible to these projections.

## Independent audit

The auditor does not call the runner's projection routine. It reconstructs every row map from the
frozen atom tables, recomputes ranks with reverse column order and low row pivots, and recomputes
the first Bockstein with low pivots. All 158 checks pass, including every premise hash, projection
hash, dimension, nonzero count, atom count, field rank, and Bockstein rank.

The primary result SHA-256 is
`6766b6ca249f1b02ba9a83a6fb8434eea4e511172c982840fc3c6db6a192e886`. The audit certificate has
internal hash `21dfcfee3f8d2d6b58aa4e582880ca93c7e3b2ec3f3cb8af510f217be0a33930` and external SHA-256
`324c98de4cdcf98b4fb6010343df9ceeab4c6347938c36c2614e2850cad254e1`.

## Boundary and next proof gate

Row projection is not a unimodular equivalence, so necessity here does not prove a canonical
subcomplex. The next exact gate is the complete lattice of the six normalized row atoms: test all
64 subsets, identify every minimal subset preserving the full Bockstein, and compare that set
across `p=8,...,11`. Only after the circuit is stable should an integral Morse matching be built.
No recurrence, all-parameter theorem, manuscript, or Zenodo update follows from EXP-044.
