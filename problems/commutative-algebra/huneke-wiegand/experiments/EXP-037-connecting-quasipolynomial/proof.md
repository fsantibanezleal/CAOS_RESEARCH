# EXP-037 proof - exact refutation at the first out-of-sample cell

Date: 2026-08-30. Status: **REFUTED**. CPU-only exact arithmetic.

## Claim under test

For

```text
e_p=dim_GF(2) A_(p,2)-dim_GF(3) A_(p,2),
```

the six EXP-036 values `1,4,9,18,31,49` matched the first coefficients of

```text
(1+2x+x^2+x^3)/((1-x)^2(1-x^2)(1-x^3)).
```

With `n=p-4`, this candidate is

```text
floor((10n^3+63n^2+126n+89)/72)
```

and therefore predicted `e_10=73`. The stronger P2 prediction required an integral factor-two
core indexed by the corresponding 73 lattice points.

## Exact rank reduction

The complete `(p,t)=(10,2)` presentation has

```text
kernel codomain rows       17,356
kernel boundary columns    12,006
connecting source columns 773,790
connecting codomain rows 3,320,245.
```

No selected minor replaces this block. The exact-sum bases have hashes

```text
kernel codomain  5a8f41e3ea2b6a1265045e70514c48c4c71bd8d4ec3ee2a3048bff0200bf5626
kernel domain    f05f64a7e25e6f358b84c808850fd9c3340226d9b34b4c2e5ca9a2e649468d41
connecting source 497cc14907beaf4a0fb9d3cf4b326f63f92ccd5061ebc8be11da5ef22d6f041d.
```

The rank engine first cancels every degree-one row or column in the bipartite support graph. If
a row has one nonzero entry, its column is independent over every field and row operations clear
the rest of that column without changing the remaining submatrix. The transpose argument handles
a degree-one column. Every entry is `+1` or `-1`, so each cancellation is a unit pivot in every
tested characteristic. Count/XOR incidence sketches perform the first row pass without storing
the full transpose; a compact CSR core then supports two-sided cancellation. Only the resulting
2-core reaches field-specific elimination.

The field-independent reductions are

| matrix | unit pivots | residual 2-core | residual nonzeros |
|---|---:|---:|---:|
| kernel boundary | 6,523 | `4,978 x 3,058` | 12,382 |
| connecting boundary | 463,874 | `716,510 x 303,529` | 1,823,232 |
| combined block | 464,491 | `730,136 x 313,039` | 1,946,578 |

The primary low-degree order completed in 67.390048 seconds. Its exact ranks are

| field | rank kernel | kernel cokernel | rank connecting | rank combined | connecting image | surviving `A` |
|---|---:|---:|---:|---:|---:|---:|
| `GF(2)` | 9,042 | 8,314 | 725,343 | 738,459 | 4,074 | 4,240 |
| `GF(3)` | 9,042 | 8,314 | 725,343 | 738,531 | 4,146 | 4,168 |

Thus

```text
e_10=4240-4168=72.
```

The kernel and connecting-boundary ranks are characteristic-independent here. The entire
72-dimensional excess is created by the rank defect of the connecting image in the quotient,
continuing the mechanism seen for `5<=p<=9`.

## Independent audit

The audit changes two independent choices:

1. residual rows and columns use canonical order rather than static low-degree order;
2. `GF(5)` replaces `GF(3)` as the odd field.

The intermediate pivot trajectories differ, but every final `GF(2)` rank agrees and every
`GF(5)` rank agrees with `GF(3)`. The canonical-order audit completed in 66.547602 seconds and
again gives surviving dimensions `4240` and `4168`. The frozen artifact hashes are

```text
primary   ca97087466fdd705e22f69e79cdfecfc7dbce0684475b98bd99757cfed030d7b
alternate a8456b4d2de3fcf53cf97a63b63671656b4968fac80f8b8f151b76f43aba1b05.
```

`audit.py` verifies premise, basis, structural, same-field, cross-odd-field, and refutation
agreement. Its certificate hash is
`0c6e72a55202001cd3096e6c4999045eee6ce0aeb7b266d2403c83f93409ce42`.

## Preserved resource evidence

The first global-row bitset attempt was stopped after reaching 35.15 GB resident and 64.09 GB
private memory; it is not rank evidence. The Windows private-memory probe was repaired. A second
row-only peeling attempt reached partial core rank 226,798 after 250,000 columns before its tool
session was interrupted; it is also not rank evidence. Both records are retained because they
explain and test the fill-controlled redesign.

## Conclusion and scope

P1 is refuted by the exact mismatch `72 != 73` at its first out-of-sample point. P2 is also
refuted as stated: a factor-two basis indexed by the declared 73 lattice points cannot have the
computed 72-dimensional parity excess. The exact finite sequence is now

```text
p=4,5,6,7,8,9,10: 1,4,9,18,31,49,72.
```

By EXP-036's all-parameter cubic-source absence, this value transfers from `A_10` to `C_10` at
the same target. The result neither supplies a replacement all-parameter formula nor resolves the
Huneke-Wiegand conjecture. The simplest structurally meaningful redirect is to test whether the
one-unit deficit marks a first degree-six relation among the former lattice generators; that is a
new hypothesis and requires a separately declared experiment.
