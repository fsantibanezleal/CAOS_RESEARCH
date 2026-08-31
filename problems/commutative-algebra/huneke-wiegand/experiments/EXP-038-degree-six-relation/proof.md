# EXP-038 proof record - two exact recurrence passes without a structural proof

Date: 2026-08-30. Status: **INCONCLUSIVE** for P1/P2; both declared finite gates pass.
CPU-only exact arithmetic over declared prime fields.

## Claim under test

For

```text
e_p=dim_GF(2) A_(p,2)-dim_GF(3) A_(p,2),
```

EXP-038 asks whether

```text
sum_(p>=4) e_p x^(p-4)
  =(1+2x+x^2+x^3-x^6)/((1-x)^2(1-x^2)(1-x^3))              (P1)
```

and whether the correction `-x^6` is induced by a first homogeneous degree-six relation among
the proposed parity classes `(P2)`.  The numerator was fitted only through `p=10`; it predicted
the new values `e_11=102` and `e_12=138` before either complete block was computed.

## Complete exact computations

No selected minor replaces either presentation.  The complete basis dimensions are

| `p` | kernel rows | kernel columns | connecting columns | connecting rows |
|---:|---:|---:|---:|---:|
| 11 | 32,644 | 20,374 | 1,749,529 | 8,436,587 |
| 12 | 58,599 | 33,068 | 3,735,675 | 20,010,799 |

Exact degree-one row and column cancellation uses only signed unit pivots and is therefore valid
over every field.  Only the residual bipartite 2-core reaches field-specific sparse elimination.
The primary low-degree-order runs give

| `p` | field | rank `K` | coker `K` | rank `D` | rank `[D|K]` | image | surviving `A` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 2 | 15,599 | 17,045 | 1,659,351 | 1,683,307 | 8,357 | 8,688 |
| 11 | 3 | 15,599 | 17,045 | 1,659,351 | 1,683,409 | 8,459 | 8,586 |
| 12 | 2 | 25,698 | 32,901 | 3,575,985 | 3,617,762 | 16,079 | 16,822 |
| 12 | 3 | 25,698 | 32,901 | 3,575,985 | 3,617,900 | 16,217 | 16,684 |

Consequently

```text
e_11=8688-8586=102,
e_12=16822-16684=138.
```

Both declared out-of-sample predictions pass.  The primary runs completed in 330.533246 and
440.771096 seconds for `p=11` and `p=12`, respectively.

## Independent audit

The audit changes two choices at both parameters:

1. canonical residual order replaces static low-degree order;
2. `GF(5)` replaces `GF(3)` as the odd field.

It reproduces all complete-basis hashes, field-independent unit-peel profiles, `GF(2)` ranks,
and odd-field ranks.  The frozen external artifact hashes are

| `p` | primary SHA-256 | alternate SHA-256 |
|---:|---|---|
| 11 | `7b72b272338acfbd26dfe8e82a7fa425174e5d3fc3729ed785948f7d868a6ca1` | `4f7b60229c5e782891f3369ad6075c636a1452455d5df195844e919a2f3a47f1` |
| 12 | `960585dff4288a19242d0388f0c229a13701c2112dfa2f9cae415f5a2ff3d14e` | `dbf5f7b34bead8dba6fda769b9561ee311455f62215df8b07370b051f8359097` |

The combined audit certificate passes with internal hash
`6208c2677a5a99fb62565ce49d744e7cd7576d4d21a9b3d33d1d9f7078100fc0` and external file
SHA-256 `3b5d2871d893b29871b8e58d9e66d00ee65e86c5545fe90909b322ecb5623b39`.

## What the two passes establish

The exact finite sequence is now

```text
p=4,...,12: 1,4,9,18,31,49,72,102,138.
```

Writing

```text
Q(x)=(1-x)^2(1-x^2)(1-x^3)
    =1-2x+x^3+x^4-2x^6+x^7,
```

P1 implies, for `n=p-4>=7`,

```text
e_n-2e_(n-1)+e_(n-3)+e_(n-4)-2e_(n-6)+e_(n-7)=0.
```

The exact `p=11` and `p=12` values make the first two available recurrence residuals zero.  The
old numerator's errors at `p=10,11,12` are `1,2,4`, exactly the first three coefficients of
`1/Q(x)` introduced by subtracting `x^6/Q(x)`.  This is coherent finite evidence for a single
degree-six correction, not a derivation of it.

For `p>=5`, the ranks of `K` and `D` agree across all tested fields, and the entire excess is the
rank difference of the combined connecting presentation.  This localizes the next proof search:
it must explain signed-versus-mod-two dependence inside the combined residual core.

## Why this is not a proof

- Nine coefficients do not determine an all-parameter rational series.
- The recurrence has only two genuinely out-of-sample checks.
- Equal ranks over `GF(3)` and `GF(5)` do not supply an integral Smith certificate.
- P2 requires an explicit cycle/relation and a proof that its translates generate all defects;
  no such chain-level object has been extracted.
- Both audits share the frozen basis constructor, so a common modelling error remains possible.

## Consequence

P1 and P2 remain unresolved, so the experiment is **INCONCLUSIVE** despite two successful finite
gates.  A raw `p=13` computation would give only a third recurrence check and grows the complete
presentation substantially.  The stronger redirect is component/local-block analysis of the
combined 2-core, seeking a bounded signed template whose translates explain the defect and whose
first syzygy occurs in degree six.  No manuscript v0.24 or Zenodo update is triggered without that
structural theorem.
