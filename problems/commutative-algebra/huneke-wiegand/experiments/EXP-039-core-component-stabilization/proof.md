# EXP-039 proof record - bounded defect-one components are refuted

Date: 2026-08-30. Status: **REFUTED**, with a new finite sector decomposition.
CPU-only exact arithmetic.

## Exact component campaign

The frozen complete signed combined presentation was reconstructed for every `(p,2)`,
`4<=p<=9`.  Degree-one rows and columns were cancelled only by signed unit pivots.  The remaining
bipartite support was decomposed into connected components, and each component was ranked
separately over `GF(2)` and `GF(3)`.

Component ranks sum to the complete frozen aggregate ranks at every parameter:

| `p` | all components | defective components | defect partition | complete ranks `GF(2)/GF(3)` | largest component vertices |
|---:|---:|---:|---|---:|---:|
| 4 | 27 | 1 | `1` | `588/589` | 190 |
| 5 | 56 | 4 | `1+1+1+1` | `2935/2939` | 627 |
| 6 | 100 | 4 | `4+2+2+1` | `11548/11557` | 5,264 |
| 7 | 173 | 4 | `10+3+3+2` | `38611/38629` | 17,003 |
| 8 | 289 | 4 | `20+4+4+3` | `113694/113725` | 42,669 |
| 9 | 447 | 2 | `45+4` | `302169/302218` | 354,085 |

The exact result artifact has external SHA-256
`831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c`.
The deterministic partition/control audit passes with internal certificate hash
`2835a0001cba10ffc204a687c7cccc604f59d4b78654ff53f13cc30223c814ad` and external SHA-256
`55e3159dd01f9c412ad56a5808eda1f428672341b57ce5dd6eb4e2f266051534`.

## Refutation

P1 predicted that every defective component through `p=9` would contribute one and have at most
5,000 vertices.  It fails first at `p=6`: one component contributes four and has 5,264 vertices.
At `p=9`, a component with 354,085 vertices contributes 45.  The proposed interpretation of
`e_p` as the number of independent connected blocks is therefore false.

P2 predicted recurring bounded normalized signed types.  No such type persists under the declared
normalization, and the support merger at `p=9` contradicts the stated bounded-component model.
P2 is refuted as stated.

## Orientation controls

Every defective component detects both adversarial controls.  Erasing all signs strictly raises
its `GF(3)` rank; flipping the first sign raises its `GF(3)` rank by exactly one.  The `GF(2)` rank
is unchanged by either sign operation.  Thus the characteristic defect is not a property of the
unsigned support graph: the signed orientation is essential.

## New finite sector law

Although P1 fails, the defect partitions expose a stronger redirect.  For `p=6,7,8`, they are
exactly

```text
binom(p-2,3), p-4, p-4, p-5.
```

At `p=9`, the first three support sectors merge into one connected component but retain the sum

```text
35+5+5=45,
```

while the fourth contributes `4`.  Hence the latent free-sector total through `p=9` is

```text
binom(p-2,3)+2(p-4)+(p-5).
```

Extending this law to `p=10` gives 73, exactly the refuted EXP-037 candidate, whereas the exact
value is 72.  The one-unit discrepancy is therefore naturally reinterpreted as a first relation
among four growing signed sectors, rather than a missing parity generator.  This is an exact
finite observation plus a testable interpretation; the sectors have not yet been identified by
an all-parameter chain map.

## How this could be wrong

- The component ranks reuse the frozen rank accumulator, although their sums independently match
  the previously audited complete ranks.
- The semantic normalization is canonical but not proved to be the correct affine translation
  action; failure to repeat its hashes does not exclude a subtler equivalence.
- The four latent sectors are inferred from exact defect partitions, not extracted as invariant
  subcomplexes after the `p=9` support merger.
- Finite polynomial agreement through `p=9` does not prove a sector law for larger `p`.

## Consequence

EXP-039 is **REFUTED**, but it supplies the first component-level explanation of the old numerical
candidate and a precise location for the corrected degree-six relation.  The next experiment must
tag the four sector families before they merge, transport those tags to `p=10`, and test whether
one signed cross-sector relation reduces their free total `73` to the exact `72`.  This finite
structural result does not trigger manuscript v0.24 or a Zenodo update.
