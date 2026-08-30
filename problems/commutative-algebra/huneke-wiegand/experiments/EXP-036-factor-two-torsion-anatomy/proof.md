# EXP-036 proof - repeated characteristic dependence and its two mechanisms

## 1. Statement and scope

Retain the EXP-035 family target

```text
b_(p,t)=10p+t,
F_(p,t)=[3p,4p-2] union {t} union [t+2,p],
i_(p,t)=2p-t-1,
tau_(p,t)=4p^2+6p-t(t-1)/2,
```

for integers `p>=4` and `2<=t<=p-2`.  Write `Delta_(p,t)` for the complete integral
kernel-incidence boundary in this multidegree and `M_(p,t)` for the complete block matrix that
also contains the `D_p` boundary and the connecting map in

```text
0 -> K_p -> A_p -> D_p -> 0.
```

EXP-036 proves three results.

1. Characteristic dependence is not isolated at `(p,t)=(4,2)`: eight further exact target cells
   are computed, and seven of them are characteristic-dependent after the connecting quotient.
2. Two mechanisms occur.  Some cells already have a mod-two rank defect in `Delta_(p,t)`, while
   every tested `t=2` cell with `5<=p<=9` has a characteristic-independent kernel cokernel and
   acquires its characteristic dependence solely from the connecting-image rank.
3. For every declared `(p,t)`, not merely the computed cells, the shifted cubic summand is absent.
   Hence the exact `A_p` values at these targets equal the corresponding `C_p` values.

The finite campaign does not prove that characteristic dependence persists for every `p`, nor
does it give a closed formula for the `t=2` excess.

## 2. Complete exact-sum construction

The canonical route reconstructs the EXP-034 two-layer Artinian kernel.  Its degree-one offsets
are the `10p-1` nonzero elements of `G_p`; the low offsets are

```text
[1,p] union [3p,4p-2],
```

and the remaining `8p` offsets are high.  Its degree-two offsets are the `10p` missing products
in `[6p,24p-1]`.  A basis element in the selected multidegree is a labelled pair `(E,c)` with
fixed cardinality and exact sum.  The implementation enumerates only subsets that can attain the
required sum: a memoized feasibility recursion prunes branches below the minimum or above the
maximum remaining sum.  It never traverses the ambient binomial family and filters afterward.

At `(4,2)` this reconstruction returns exactly the frozen EXP-035 data:

```text
kernel codomain rows       79
kernel boundary columns   119
D_p source columns        710
```

All three ordered-basis hashes and every GF(2), GF(3), and GF(1000003) rank agree with EXP-035.
This regression gate is checked before a larger parameter is accepted.

For any field `k`, exact sparse elimination computes

```text
dim_k coker(Delta) = rows(Delta)-rank_k(Delta),
rank_k(connecting image) = rank_k(M)-rank_k(d_D)-rank_k(Delta),
dim_k A target = rows(Delta)+rank_k(d_D)-rank_k(M).             (1)
```

No selected-coordinate submatrix is substituted for the complete target.

## 3. Finite propagation and two distinct mechanisms

The complete `p<=6` triangle and the targeted `t=2` cells through `p=9` give the following exact
dimensions.  Each pair is `GF(2) / odd characteristic`; GF(3) and GF(1000003) agree everywhere.

| `(p,t)` | `dim coker(Delta)` | connecting-image dimension | `dim A=dim C` | excess in characteristic two |
|---|---:|---:|---:|---:|
| `(4,2)` | `5 / 4` | `1 / 1` | `4 / 3` | `1` |
| `(5,2)` | `39 / 39` | `15 / 19` | `24 / 20` | `4` |
| `(5,3)` | `5 / 3` | `2 / 1` | `3 / 2` | `1` |
| `(6,2)` | `178 / 178` | `83 / 92` | `95 / 86` | `9` |
| `(6,3)` | `113 / 111` | `69 / 74` | `44 / 37` | `7` |
| `(6,4)` | `3 / 3` | `1 / 1` | `2 / 2` | `0` |
| `(7,2)` | `579 / 579` | `279 / 297` | `300 / 282` | `18` |
| `(8,2)` | `1570 / 1570` | `762 / 793` | `808 / 777` | `31` |
| `(9,2)` | `3776 / 3776` | `1843 / 1892` | `1933 / 1884` | `49` |

Thus P1 passes already at `(5,3)`, where the kernel boundary loses two ranks in characteristic
two.  More importantly, `(5,2)` exhibits a different effect: the kernel cokernel has dimension
`39` over every tested field, but the connecting image is four dimensions smaller over `GF(2)`.
The same connecting-only mechanism occurs at every tested `t=2` cell with `5<=p<=9`.  It cannot
be explained by propagating only the factor-two Smith block of `Delta_(4,2)`.

The data also reject two attractive extrapolations.  The first three `t=2` excesses are
`1,4,9`, suggesting `(p-3)^2`, but this predicts `16` rather than the exact value `18` at `p=7`.
The four values `4,9,18,31` for `p=5,6,7,8` fit `2p^2-17p+39`, but that polynomial predicts `48`
rather than the exact value `49` at `p=9`.  Neither interpolation is evidence for an infinite
formula.

## 4. Integral localization at `(4,2)`

Exact unimodular row and column operations cancel 74 unit pivots in the integral `79` by `119`
matrix `Delta_(4,2)`.  The residual is `5` by `45`, has four zero rows, and has just two nonzero
entries, both `-2`, in its remaining row.  Its Smith profile is therefore

```text
free cokernel rank 4,   torsion Z/2Z.
```

The transformation certificate traces the active residual back to the original basis.  In this
deterministic reduction its low-variable support is

```text
{1,2,3,4,12,13,14},
```

and its full exterior support adds `{24,25,26,27,28,29,30}`.  This confirms a compact algebraic
factor-two core.  It does not realize the declared six-low-variable real-projective-plane model,
so the strong recognition clause is rejected for this canonical reduction.  No claim is made
that a different sequence of unimodular operations can never expose a six-variable model.

## 5. All-parameter absence of the cubic contribution

The EXP-033 minimal cone is

```text
B_(C_p)(x,z)=B_(A_p)(x,z)+x z^3 B_(D_p)(x,z).
```

At the EXP-036 target, a cubic contribution would have to come from homological degree

```text
k=i_(p,t)-1=2p-t-2
```

and shifted offset `tau_(p,t)-3p`.  The first high interval starts at `6p` and contains enough
consecutive offsets for all `2<=t<=p-2`.  Hence the least possible sum of `k` distinct high
offsets is

```text
6p+(6p+1)+...+(6p+k-1).
```

Subtracting the required shifted offset gives

```text
g(p,t)=10p^2-8pt-20p+t^2+2t+3.                              (2)
```

Its forward difference in `t` is

```text
g(p,t+1)-g(p,t)=2t-8p+3<0
```

throughout the declared interval.  Thus the minimum occurs at `t=p-2`, where

```text
g(p,p-2)=3(p-1)^2>0.                                        (3)
```

The shifted `D_p(-3)` diagonal is therefore zero for every integer `p>=4` and
`2<=t<=p-2`.  Consequently

```text
beta_(i,(i+2,tau))(C_p)=beta_(i,(i+2,tau))(A_p)              (4)
```

at every target in the family.  Equations (2)--(4) are deductive all-parameter statements; the
characteristic-dependent values in the table remain finite exact statements.

## 6. Independent validation and trust boundary

The independent route reconstructs the Artinian bases directly from numerical-semigroup ideal
powers.  It uses iterative dynamic programming for exact sums, rather than the canonical
feasibility DFS, and eliminates columns and pivots in reverse order.  On every audited cell it
matches the three canonical basis hashes and the complete GF(2)/GF(3) rank records; its separate
GF(5) control agrees with GF(3).  This route passes all eight cells through `(8,2)`.  At `(9,2)`
the deliberately different enumerator crossed 47.5 GB of private memory before producing a rank;
that attempt is preserved as `INCONCLUSIVE_RESOURCE_BUDGET` and is not mathematical evidence.
The canonical `(9,2)` result retains two agreeing odd-prime controls.  The symbolic route
rechecks (2)--(3), all nine finite cubic
inequalities, every odd-field equality, the localization invariants, and the two deliberately
failed interpolations.

The results prove repeated characteristic-dependent multigraded Betti cells and an
all-parameter transfer from `A_p` to `C_p` at the declared targets.  They do not determine a
complete lower strand, an infinite formula for the connecting-image defect, or the full minimal
resolution.  The next structural target is the parity-sensitive connecting complex itself, not
another polynomial fit to finite dimensions.
