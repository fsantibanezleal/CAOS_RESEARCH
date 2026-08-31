# EXP-041 preflight - semantic tags across the parity-sector merger

Date: 2026-08-31. Scope: HWB-068 inside the EXP-035 connecting-parity programme.

## Decision-bearing question

EXP-039 found four characteristic-defect sectors at `p=6,7,8`, followed by a support merger at
`p=9`. EXP-040 localized the first correction at `p=10`, but its componentwise transport failed
at `p=11`: the exact partition is `95+7`, not `96+6`. The next question is therefore not another
rank total. It is:

> Do interval labels identify the isolated components at `p=9,10` with the finite `p-5` sector,
> and does the isolated component change semantic lineage at `p=11`?

The answer gates every bridge-deletion attempt. Connected support alone is already known to be too
coarse.

## Primary-source completion and fresh sweep

The previously frozen source basis remains:

- Bruns and Herzog, *Semigroup rings and simplicial complexes*,
  <https://doi.org/10.1016/S0022-4049(97)00051-0>, for the relative
  squarefree-divisor-complex formula and the characteristic boundary;
- Autry et al., *Squarefree divisor complexes of certain numerical semigroup elements*,
  <https://arxiv.org/abs/1804.06632>, for explicit realization and classification techniques;
- Stamate, *Betti Numbers for Numerical Semigroup Rings*,
  <https://arxiv.org/abs/1801.00153>, for the computational and characteristic-dependent Betti
  landscape.

A fresh 2026-08-31 arXiv sweep also checked:

- Gimenez and Srinivasan, *Gluing and splitting of homogeneous toric ideals*,
  <https://arxiv.org/abs/2402.17112>. Their tensor-product resolution requires an actual splitting
  of the toric ideal after gluing. No such splitting is established for the signed connecting
  presentation here, so the result motivates a decomposition test but does not supply one.
- Landeros et al., *Families of numerical semigroups and a special case of the Huneke-Wiegand
  conjecture*, <https://arxiv.org/abs/2404.12519>. Their positive theorem concerns generalized
  arithmetic-sequence semigroups. The EXP-009 generator set has several disjoint affine intervals
  and isolated generators, so it is outside that stated class.

No checked source identifies the four finite sectors or settles their merger. EXP-041 therefore
remains a new internal anatomy experiment, not a replication of a published decomposition.

## Frozen premises

| premise | status used here |
|---|---|
| EXP-036 | confirmed finite characteristic dependence and all-parameter cubic-source absence |
| EXP-037 | refuted candidate, exact audited `e_10=72` |
| EXP-038 | inconclusive recurrence, exact audited `e_11=102`, `e_12=138` |
| EXP-039 | refuted bounded blocks, exact component partitions through `p=9` |
| EXP-040 | refuted transport, exact partitions `67+5` and `95+7` |

EXP-039/040 artifacts and their audits are immutable rank and component-identity gates. EXP-041
must reproduce their component counts, support hashes, and defect partitions before a semantic
profile is accepted.

## Invariant-first profile

Each active row or column receives an exact semantic atom:

```text
(side, module kind, coefficient interval tag, exterior interval-count vector).
```

The degree-one generator tags are the ten affine blocks already defining the EXP-009 family. The
degree-two coefficient tags are the eight complementary intervals in `[6p,24p-1]`. Connecting
rows retain their exact `A` or `B` product kind. For every component, EXP-041 records atom
multiplicities, coefficient-tag supports, exterior occupancy bounds, and whether the distinguished
EXP-035 selected row survives in that component.

This is cheaper and more discriminating than another finite-field elimination. No Smith form or
`p=12` component rank is allowed before this gate.

## One-sidedness and stop rules

- A positive tag lineage is finite evidence only. It can justify a later signed bridge experiment,
  but cannot prove a graded module or recurrence.
- Failure of the coarse interval signature refutes interval labels as a component-level grading and
  redirects to matched-block or relative-homology generators inside the merged component.
- The smoke run is `p=8`, with a 600-second and 20-GB cap. It must emit progress and an atomic
  checkpoint.
- The campaign is `p=8,...,11`, with a 2,400-second and 36-GB cap and one checkpoint per parameter.
  A cap stop is `INCONCLUSIVE_RESOURCE_BUDGET` at the last complete parameter.
- No finite-only outcome triggers manuscript v0.24 or a Zenodo version.

## Exploration moment

The gluing/splitting paper suggests a stronger future recognition question: whether the merged
signed core admits a chain-level sum or tensor decomposition after a small bridge set is removed.
That question is deliberately downstream. EXP-041 first tests the necessary semantic separation;
bridge removal without it would repeat EXP-040's unsupported component transport.
