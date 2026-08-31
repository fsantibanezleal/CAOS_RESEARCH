# EXP-045 proof record - complete row-atom carrier lattice

Date: 2026-08-31. Status: **REFUTED overall**, with a stable full-carrier antichain retained for
`p=8,...,11`. CPU-only exact integer and finite-field arithmetic.

## Exhaustive construction

The runner verifies the four frozen EXP-042 matrix hashes and the EXP-044 result hash. For each
matrix it retains every one of the 64 subsets of the six normalized row atoms, including the empty
and full subsets. All columns, including zero columns, remain in each presentation. It computes
exact ranks over `GF(2)`, `GF(3)`, and `GF(5)` and first-Bockstein ranks with forward/high and
reverse/low reductions.

Thus the experiment evaluates 256 exact projected matrices, not a sampled collection.

## Exact carrier lattice

Write a mask in the alias order `R0,...,R5` from the hypothesis. The complete nonzero carrier
sets are:

```text
p=8,9,10: all and only supersets of 58 = {R1,R3,R4,R5}
p=11:     all and only supersets of 56 = {R3,R4,R5}.
```

The full-Bockstein carrier set is identical for every parameter:

```text
{59,62,63}, with minimal antichain {59,62},
59 = {R0,R1,R3,R4,R5},
62 = {R1,R2,R3,R4,R5}.
```

The intersection mask `58` and the full ranks decompose as follows:

| `p` | minimal nonzero mask | `beta(58)` | minimal full masks | full Bockstein | completion increment |
|---:|---:|---:|---:|---:|---:|
| 8 | 58 | 1 | 59, 62 | 3 | 2 |
| 9 | 58 | 2 | 59, 62 | 4 | 2 |
| 10 | 58 | 3 | 59, 62 | 5 | 2 |
| 11 | 56 | 5 | 59, 62 | 7 | 2 |

At `p=11`, mask `56` has Bockstein one. This is the first tested parameter where the mandatory
triad `R3,R4,R5` alone carries torsion. Adding `R1` raises the core to five; adding either `R0` or
`R2` to mask `58` completes the full rank seven.

All three declared predictions are refuted as written. Not all six atoms are essential, the full
set is not the unique carrier, and the minimal nonzero carrier changes at `p=11`. The stronger
retained result is the stable full-carrier antichain and constant two-class completion.

## Independent audit

The auditor reconstructs all 256 projections without calling the runner's projection function.
It uses reverse columns and low row pivots, recomputes every three-field rank and first Bockstein,
and verifies the complete subset tables and minimal antichains. All 2,855 checks pass.

The primary result SHA-256 is
`569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8`. The audit certificate has
internal hash `b86be9527e4ba80e9d09a44da614a44c8ff7180c81ac31e623b1a317d2419dc5` and external SHA-256
`a1a5bc105ecb7171970dd9b0b8daf4d823190a56b9a0f8e1e64a59479dcac3dd`.

## Boundary and next proof gate

The result is a complete finite theorem about row projections, not an integral chain equivalence.
The strongest next gate compares the inclusions `58 -> 59` and `58 -> 62`: extract relative
integer presentations, prove that both add the same two factor-two directions, and determine why
the `R0` and `R2` completions are interchangeable for 2-primary torsion. In parallel, isolate the
new `p=11` class in `56 -> 58`. A uniform signed matching and explicit parameter maps remain
necessary for an all-parameter theorem. No manuscript or Zenodo update follows from EXP-045.
