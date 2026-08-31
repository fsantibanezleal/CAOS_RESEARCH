# EXP-039 hypothesis - bounded components behind the parity defect

Date: 2026-08-30. CPU only. Exact arithmetic over declared prime fields.

## Question

Let `M_(p,2)` be the complete signed combined presentation used in EXP-037/038.  After every
degree-one row or column is cancelled by a unit pivot, let `G_p` be the bipartite support graph of
the residual 2-core.

### P1. Bounded defective components

For `5<=p<=9`, every connected component whose rank over `GF(3)` exceeds its rank over `GF(2)`
has at most 5,000 total row and column vertices, and its defect is one.  Thus `e_p` is the number
of defective connected components in the declared finite range.

### P2. Recurring normalized types

After relabelling rows and columns by their affine positions within the interval blocks defining
the semigroup family, the defective components fall into finitely many recurring signed types.
Their birth multiplicities are compatible with generator degrees `0,1,1,2,3` and a first relation
in degree six, as suggested by the EXP-038 Hilbert numerator.

P2 requires explicit component hashes, signed ranks, and relabelling data.  Agreement of total
defects alone cannot establish it.

## Premise dependencies

- EXP-036 proves the exact finite `p<=9` target values and the all-parameter absence of the shifted
  cubic source.
- EXP-037 supplies the exact two-sided unit-peeling engine and its audited `p=10` refutation.
- EXP-038 is **INCONCLUSIVE** for its all-parameter claims but exactly audits `e_11=102` and
  `e_12=138`.  Neither the formula nor the relation is treated as a premise.
- The Bruns--Herzog squarefree-divisor-complex dictionary motivates the topology lens; it does not
  imply P1 or P2.

Frozen SHA-256 premise hashes are

```text
EXP-038 proof       829eaa8645258d065f2d0b8bb7e6ee9dbad9ee439d4b659faf31e621e8e40213
EXP-038 verdict     90ccf41cd338378bed687292d593aeab6897be919827f9fd5851506d94a40b7b
EXP-038 audit       3b5d2871d893b29871b8e58d9e66d00ee65e86c5545fe90909b322ecb5623b39
EXP-037 rank engine 1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0
```

## Method and adversarial controls

1. Import the frozen basis constructor and independently rebuild the complete combined columns.
2. Reproduce the frozen aggregate ranks at `(4,2)` and `(5,2)`.
3. Perform signed unit row/column peeling; compute connected components of the exact residual
   bipartite graph.
4. Rank each component independently over `GF(2)` and `GF(3)` and verify that component sums equal
   the aggregate rank in every completed cell.
5. Canonically hash component dimensions, degree multisets, signed columns, and rank pairs.
6. On a positive recurring type, rerun its endpoint instances in canonical order with `GF(5)`.
7. Adversarial controls erase signs and perturb one incidence; a claimed signed type must detect
   at least the sign-erased control whenever its odd-characteristic rank depends on orientation.

## What PASS and FAIL prove

- **P1 PASS** proves only finite localization through the largest completed parameter.  It makes
  an explicit translation theorem plausible but does not prove an infinite formula.
- **P1 FAIL** refutes connected components as the source of independent parity generators.  It
  redirects immediately to matched-block/relative-homology decomposition; it does not refute the
  EXP-038 numerical series.
- **P2 PASS** requires recurring signed component certificates and a proved normalization map in
  the tested range.  It still needs an all-parameter extension before confirming EXP-038 P2.
- **P2 FAIL** rejects the simple free-generator/one-relation component model.

## Invariant-first and resource gate

Connected support is the cheapest exact block invariant; no Smith computation is attempted before
it.  The campaign is `p=4,...,9`, with a 1,800-second and 20-GB cap and a checkpoint after every
cell.  Crossing either limit yields **INCONCLUSIVE** at the last checkpoint.  No manuscript or
Zenodo update opens from a finite component table alone.
