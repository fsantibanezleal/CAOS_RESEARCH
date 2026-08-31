# EXP-040 proof record - first correction localized, simple translation split refuted

Date: 2026-08-30. Status: **REFUTED** overall; P1 passes and P2 fails. CPU-only exact arithmetic.

## Declared predictions

EXP-039 found four latent finite sectors and a support merger.  EXP-040 predicted that their first
two corrected partitions would be

```text
p=10: (56+6+6)-1, 5 = 67+5,
p=11: (84+7+7)-2, 6 = 96+6.
```

The second cell was conditional on the first passing.

## Exact results

Every residual connected component was ranked independently over `GF(2)`, `GF(3)`, and `GF(5)`.
The component sums reproduce the previously audited complete ranks:

| `p` | complete ranks `GF(2)/GF(3)/GF(5)` | defective partition | largest component vertices |
|---:|---:|---|---:|
| 10 | `738459/738531/738531` | `67+5` | 842,604 |
| 11 | `1683307/1683409/1683409` | `95+7` | 1,845,713 |

At `p=10`, the large component has ranks `218451/218518/218518` and the small component has
`2445/2450/2450`.  This proves the finite P1 partition `67+5`: the first one-unit correction is
localized exactly inside the merged support sector while the second component contributes five.

At `p=11`, the large component has ranks `454186/454281/454281`, while the small component has
`3579/3586/3586`.  Thus the exact partition is `95+7`, not the declared `96+6`.  P2 is refuted.
The total remains the audited 102, but one unit is distributed differently between the two
components than the naive translated-sector model predicts.

The standalone `p=10` artifact and the combined artifact have external SHA-256 hashes

```text
8107af8e2810414144e5ee94f4caeaa634ca81e14af92b26050b3f50d48648b6
ad1fec04199ff94b803f95f98650c8c8ab386386240d584f447afbb9fe27668b.
```

The deterministic audit passes with internal certificate hash
`6a778b46a93fa59b9361608b20fa570ee3fb9c462b213101a65889c7e2eb271a` and external SHA-256
`625f9ac10b8aaaf1e2cf4f8ba0d2d12cf1fe3b68745d2c418707c1e8be501482`.

## Adversarial controls

`GF(3)` and `GF(5)` agree on every component, not only on the complete rank.  For each of the four
defective components across `p=10,11`, erasing signs strictly raises the odd rank, while flipping
one sign raises it by exactly one.  The partitions are therefore orientation-sensitive exact
invariants rather than unsigned support counts.

## Interpretation

P1 is a relevant finite localization: the first correction from 73 to 72 is carried by the merged
component.  P2 shows that its most direct translation law is wrong.  Between `p=10` and `p=11`,
the large defect grows `67 -> 95` and the small defect grows `5 -> 7`; the latter is not the
predicted linear `p-5` continuation.  Either the semantic identity of the smaller component
changes, or the pre-merge sector tags do not transport componentwise after the support merger.

P3 was not attempted because its premise P2 failed.  A new experiment must profile the semantic
row/column labels inside the defective components and construct tag maps before attempting bridge
deletion or an all-parameter relation.

## How this could be wrong

- Component ranks use the frozen EXP-039 decomposition, although complete sums and two odd fields
  provide independent aggregate and arithmetic checks.
- Connected components are canonical for support but need not coincide with algebraically natural
  sector submodules.
- The finite `67+5` localization does not identify a relation vector or prove its degree.
- The `95+7` redistribution may reflect a different semantic component rather than literal motion
  of one class; label-level comparison is still missing.

## Consequence

EXP-040 is **REFUTED** because P2 fails.  P1 remains an exact finite result and sharpens the search
for the degree-six correction.  No recurrence, lower-strand theorem, or Huneke--Wiegand resolution
is claimed.  No manuscript v0.24 or Zenodo update is triggered.
