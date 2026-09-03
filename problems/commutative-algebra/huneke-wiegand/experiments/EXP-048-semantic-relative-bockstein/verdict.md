# EXP-048 verdict

Status: **REFUTED overall**; P1 passes finitely, while P2 and P3 fail.

The canonical relative first-Bockstein ranks reproduce the complete EXP-047 factor-two ranks:
`2`, `2`, and `p-7` for `58->59`, `58->62`, and `56->58` at `p=8,...,11`. Forward and reverse
relation traversals yield the same semantic image subspace in all twelve cases.

The declared bounded completion templates do not exist in this canonical section. Instead, the
two completion bases are interval chains with exact support laws

```text
58->59: (p-4,p-4),
58->62: (2p-8,p-4).
```

Their rows satisfy the explicit `alpha_(p,j)` and `beta_(p,j)` formulas in `proof.md` at every
tested parameter. A separate 78-check audit regenerates those formulas and matches every row.
This is the actionable result: the next symbolic step can target four named chains rather than an
opaque HNF basis.

The `56->58` prediction is refuted more substantially. Its `p-7` canonical classes have multiple
support skeletons and irregular support sizes, so a single translation-family proof is not the
right route in this quotient section. Use dual parity characters or a relative Morse filtration
for that threshold block.

The completion formulas were found after the declared bounded-template prediction failed. They
are exact finite classifications and conjectural all-parameter targets, not an infinite theorem.
No manuscript or Zenodo update is triggered.
