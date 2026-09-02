# EXP-046 proof record - relative unit-core obstruction

Date: 2026-09-02. Status: **REFUTED overall**, with P3 confirmed finitely. CPU-only exact
integer and finite-field arithmetic.

## Exact reductions

For each `p=8,...,11`, the runner reconstructs the frozen EXP-042 signed matrix and the EXP-045
row projections with masks `56`, `58`, `59`, and `62`. It repeatedly removes a degree-one
row-column or column-row pair. Every selected entry is `+1` or `-1`, so each removal is an
integral elementary cancellation of an identity summand. The remaining presentation therefore
has the same torsion as the original projection.

Both deterministic orders preserve the stored ranks over `GF(2)`, `GF(3)`, and `GF(5)`, the
first-Bockstein rank, and the free rank over `GF(3)`. They also return the same multiset of
component dimensions, ranks, and defects.

| `p` | mask | source rows x columns | cancellations | nonzero core rows x columns | positive defects |
|---:|---:|---:|---:|---:|---:|
| 8 | 56 | 1769 x 1094 | 74 | 1695 x 1005 | none |
| 8 | 58 | 2596 x 1094 | 19 | 2577 x 1062 | 1 |
| 8 | 59 | 2624 x 1094 | 0 | 2624 x 1085 | 3 |
| 8 | 62 | 2647 x 1094 | 0 | 2647 x 1094 | 3 |
| 9 | 56 | 3176 x 1729 | 92 | 3084 x 1620 | none |
| 9 | 58 | 4653 x 1729 | 21 | 4632 x 1693 | 2 |
| 9 | 59 | 4689 x 1729 | 0 | 4689 x 1718 | 4 |
| 9 | 62 | 4721 x 1729 | 0 | 4721 x 1729 | 4 |
| 10 | 56 | 5354 x 2607 | 114 | 5240 x 2474 | none |
| 10 | 58 | 7841 x 2607 | 23 | 7818 x 2567 | 3 |
| 10 | 59 | 7886 x 2607 | 0 | 7886 x 2594 | 5 |
| 10 | 62 | 7928 x 2607 | 0 | 7928 x 2607 | 5 |
| 11 | 56 | 8580 x 3785 | 141 | 8439 x 3623 | 1 |
| 11 | 58 | 12548 x 3785 | 25 | 12523 x 3741 | 5 |
| 11 | 59 | 12603 x 3785 | 0 | 12603 x 3770 | 7 |
| 11 | 62 | 12656 x 3785 | 0 | 12656 x 3785 | 7 |

Every residual is a single connected nonzero component. In particular, neither minimal full
carrier `59` nor `62` has even one integral unit leaf. Their defect does not split as the mask-58
defect plus two defect-one components. P1 and P2 are therefore refuted.

Mask `56` has defect zero at `p=8,9,10` and exactly one at `p=11`. Its normalized completion
aliases and column-atom set are identical at all four parameters, so the threshold occurs inside
persistent semantic support rather than through a new atom type. P3 passes finitely.

## Independent audit

The independent auditor does not call the runner's projection, peeling, rank, or Bockstein
routines. It reconstructs each projection, uses maximum-index column leaves before row leaves,
and recomputes all component ranks with reverse columns and low pivots. All 214 checks pass,
including premise hashes, recomposition, opposite-order component summaries, persistent mask-56
support, and zero cancellations for masks `59` and `62`.

The primary result SHA-256 is
`1e78f650ef041eb1f45b4e979ea90a78709ef59ff443e57613edbc9cc6ea15b0`, with internal artifact
hash `2c0d7ce8eb4bd170337f8b3e2ce5518cdf92a62f409168627adae6393805c447`. The audit certificate
has internal hash `d6956bd1e0eefbd20ff3556e598f3fe0a410dfc08b49b83423adad744b076c90` and external SHA-256
`cae21dd006af047179242b9e5c60b3022c344953da3d57b62f826e4c682ab35a`.

## What could make this wrong?

- Row projection is a diagnostic presentation operation, not an already-proved subcomplex or
  uniform deletion-contraction system.
- The finite range can miss new semantic atoms or new cancellation patterns at `p>=12`.
- Unit-leaf cancellation sees only degree-one integral pivots. General unimodular row and column
  operations can create unit pivots through fill, so this result does not refute algebraic Morse
  compression or a signed normal form in general.
- A first Bockstein identifies valuation-one factor-two directions only after the independently
  certified rational rank is supplied; that certification is inherited from EXP-043 for the full
  isolated matrices, not newly extended to every projected cokernel here.

The two independent implementations, frozen hashes, three-field recomposition, and exact
Bockstein agreement address implementation and arithmetic errors within the stated finite scope.

## Consequence and next proof gate

The leaf-core route is closed. The next reduction must create fill: build the exact relative
cokernel presentation for the inclusion of mask `58` in each minimal full carrier, then apply
fraction-free signed Hermite or Schur-complement elimination while retaining unimodular
certificates. The two completions have the same torsion increment two but different rational-rank
increments, so a successful comparison must isolate a small parity quotient after eliminating
their distinct free directions.

The separate `56 -> 58` comparison must explain why an unchanged atom alphabet changes rank at
`p=11`. No all-parameter theorem, manuscript update, or Zenodo version follows from this finite
negative route-selection result.
