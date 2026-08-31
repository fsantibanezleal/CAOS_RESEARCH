# EXP-041 hypothesis - semantic sector tags across support mergers

Date: 2026-08-31. CPU only. Exact combinatorial profiling plus frozen exact rank evidence.

## Question and predictions

Use the complete signed combined presentation `M_(p,2)` and the exact EXP-039 unit-peeling order.
For each active row and column, record its module side, affine coefficient interval, and the counts
of exterior variables in every affine generator interval.

### P1. Interval tags separate the four pre-merger sectors

At `p=8`, the four defective components with defects `20,4,4,3` have distinct exact semantic
fingerprints. In particular, the defect-three component, called the finite `R` anchor, is
distinguished from both defect-four components without using component number, vertex count, rank,
or a post-run fitted threshold.

### P2. The isolated component changes lineage at p=11

The isolated defective components at `p=9` and `p=10` retain the unique coefficient-tag support of
the `p=8` `R` anchor. The isolated defect-seven component at `p=11` loses that support and acquires
the support of exactly one of the two `p=8` defect-four anchors. This is the declared semantic
switch behind the failed EXP-040 prediction `96+6`.

### P3. Distinguished-row localization

The distinguished EXP-035 selected row, if it survives unit peeling, belongs to a uniquely
identified lineage at every completed parameter. Its component membership must agree with P1/P2;
otherwise P3 is refuted even if aggregate fingerprints appear compatible.

## Exact tag dictionary

Degree-one exterior variables use these disjoint tags:

```text
L0=[1,p], L1=[3p,4p-2], H0=[6p,8p-2], H1=[8p,10p-2], H2={10p},
H3=[11p-1,12p-1], H4=[13p+1,14p-2], H5=[14p,15p-1],
H6={16p}, H7=[17p-1,18p-1].
```

Kernel-row coefficients use the eight complementary degree-two tags:

```text
C0={8p-1}, C1={10p-1}, C2=[10p+1,11p-2], C3=[12p,13p],
C4={14p-1}, C5=[15p,16p-1], C6=[16p+1,17p-2], C7=[18p,24p-1].
```

Source columns use `L0/L1`, kernel columns use `H0,...,H7`, and connecting rows use their exact
`A/B` product kind. A component fingerprint is the complete sorted histogram of

```text
(row-or-column, D/K/S kind, coefficient tag, exterior block-count vector).
```

P1 requires exact fingerprint inequality and a rank-free distinguishing tag support. P2 requires
the declared support persistence/switch, not visual similarity.

## Premise dependencies

- EXP-039 is refuted as a bounded-component model but freezes exact components through `p=9`.
- EXP-040 is refuted overall but freezes the exact `p=10,11` components and partitions.
- EXP-037/038 freeze aggregate ranks. EXP-041 does not recompute or strengthen them.
- The source-complete preflight is
  `context/2026-08-31-exp041-semantic-sector-tags-preflight.md`.

## Method and adversarial controls

1. Reconstruct the exact EXP-039 support and unit peeling without finite-field elimination.
2. Reproduce frozen component counts, support hashes, and defective component identities for every
   completed parameter.
3. Persist full semantic histograms only for defective components; persist compact hashes for all
   components.
4. Independently audit every stored histogram sum against its component row and column counts.
5. Permute component enumeration and reverse the interval-tag construction; hashes and lineage
   decisions must remain unchanged.
6. Refuse any lineage assignment based only on defect, component index, size, or a fitted numeric
   distance.

## What PASS and FAIL prove

- **P1 PASS** supplies a finite exact semantic classifier before the support merger. It does not
  prove that a classifier is an invariant subcomplex.
- **P1 FAIL** refutes coarse interval tags as sector identifiers and redirects to chain generators.
- **P2 PASS** establishes a finite exact component-lineage switch at `p=11`; it does not prove why
  the defect moves or establish the degree-six relation.
- **P2 FAIL** refutes the proposed switch interpretation. It may instead show persistent `R`
  identity with an internal relation, or that component-level lineage is undefined.
- **P3 PASS** localizes the distinguished row finitely. **P3 FAIL** prevents it from anchoring a
  bridge theorem.

## Resource gate

The `p=8` smoke run has a 600-second, 20-GB cap. The full `p=8,...,11` campaign has a 2,400-second,
36-GB cap, flushed progress, and atomic per-parameter checkpoints. A resource stop is inconclusive.
No manuscript or Zenodo gate opens from finite semantic profiles alone.
