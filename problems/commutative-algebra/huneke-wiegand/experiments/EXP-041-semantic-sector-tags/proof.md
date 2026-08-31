# EXP-041 proof record - a persistent twelve-atom isolated sector

Date: 2026-08-31. Status: **REFUTED** overall; P1 passes finitely, while P2 and P3 fail.
CPU-only exact combinatorics over frozen exact rank evidence.

## Declared predictions

EXP-041 replaced component index and size matching by exact semantic atoms recording module side,
affine coefficient interval, and the full exterior interval-count vector. It predicted:

1. the four defective `p=8` components have distinct exact fingerprints, with the defect-three
   `R` anchor identifiable without ranks or component numbers;
2. the isolated components at `p=9,10` retain `R` support, but the defect-seven component at
   `p=11` switches to one of the two defect-four `L` anchors; and
3. the distinguished EXP-035 row localizes one lineage whenever it survives peeling.

## Exact results

The implementation reproduced every frozen support hash and every defect partition:

| `p` | defective partition | isolated defect | isolated rows/columns |
|---:|---|---:|---:|
| 8 | `20+4+4+3` | 3 | `2675/1094` |
| 9 | `45+4` | 4 | `4757/1729` |
| 10 | `67+5` | 5 | `7973/2607` |
| 11 | `95+7` | 7 | `12711/3785` |

P1 passes finitely. The defect-three `p=8` component is the unique defective component omitting
both `column:K:H1` and `row:K:C1`. Its complete eight coefficient tags are

```text
column:K:H0, column:K:H2, column:S:L0, column:S:L1,
row:D:A, row:D:B, row:K:C0, row:K:C2.
```

P2 is refuted. Exactly those eight tags occur in the isolated component at every parameter
`p=8,...,11`. More strongly, after subtracting `p` from the `L0` and `L1` exterior counts, all
four profiles have the same twelve semantic atoms. Their common normalized skeleton has SHA-256
`d0c296e39c7c4f10ffd886b23b3b3d4d9cea0a291dd1aed6fcc079998c57676d`.

The defect therefore changes `3,4,5,7` inside one persistent finite semantic skeleton. The jump at
`p=11` is not evidence of a switch from `R` to an `L` component. It is an internal signed-rank
event that a chain-level normal form must explain.

P3 is refuted as an anchor. The selected EXP-035 row is absent from every defective profile in
the completed range. The profiler does not establish whether it was removed by a particular
pivot, so no stronger claim about its peeling history is made.

## Adversarial controls

An independent audit verifies disjoint and complete affine interval partitions, the frozen
component hashes and dimensions, every histogram sum and atom shape, forward/reversed tag-order
agreement, exact twelve-atom persistence, and omission of `H1/C1`. The primary, reverse, and audit
artifact SHA-256 hashes are respectively

```text
069e587b779bd1571d72e1a47bf74f4d1640dae5fbbf09907d2bf798c4941534
eafad05553cb7401c27ebeafcf686da6b436a25031dbc0f89e638096a6e02a1b
41b7ce59e354d841d82fe97ec3f74b0c5cc06836e85f332dc0318622b1a41cd2.
```

The audit certificate's internal hash is
`6f1f66bc469715f9c90f2fd2f8e6f637d422742cc7af2fed8b533cc6f4994530`.

## Interpretation and boundary

This is a relevant structural reduction: one difficult component family is now described by a
fixed finite atom alphabet rather than changing support labels. It narrows the next task to the
signed differential among those atom families. It does not yet construct a chain isomorphism,
prove representation stability, identify the integral torsion, prove the proposed recurrence, or
establish an all-parameter lower-strand theorem.

The broad Huneke--Wiegand conjecture is already false; the unresolved CAOS target is the
all-parameter characteristic-two connecting quotient for the EXP-009 family and, ultimately, the
remaining lower strand. This finite structural result does not trigger a manuscript revision or a
Zenodo version.
