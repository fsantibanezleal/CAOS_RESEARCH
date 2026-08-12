# EXP-012 pseudo-Frobenius and reduced-type proof

## Theorem

For every integer `p>=4`, put `s=6p` and let `Lambda_p` be the EXP-011 endomorphism semigroup.
For complements in `[0,s-1]`, define

```text
B^c = [0,p] union {2p-1} union [3p,4p-1] union [4p+1,5p-2],
Q^c = [0,p] union {2p-1} union [2p+1,4p-1] union [4p+1,6p-1],
C^c = [2p+1,3p-1] union [5p-1,6p-1].
```

Then

```text
PF(Lambda_p) = (6s+B^c) union (7s+Q^c) union (8s+C^c).
```

Consequently the associated numerical semigroup ring has Cohen-Macaulay type and reduced type
`10p`, hence maximal reduced type. The semigroup is not almost symmetric, so its completed
semigroup ring is not almost Gorenstein.

## 1. Every final-window gap is pseudo-Frobenius

EXP-011 proves that `Lambda_p` has multiplicity `m=4s`, conductor `c=9s`, and blocks

```text
L_4=A, L_5=[0,s-1], L_6=B, L_7=Q, L_8=C,
L_k=[0,s-1] for k>=9.
```

If a gap `f` lies in `[c-m,c-1]=[5s,9s-1]`, then every positive `lambda` in `Lambda_p` satisfies
`lambda>=m`, hence `f+lambda>=c` and `f+lambda` belongs to `Lambda_p`. Thus every such gap is
pseudo-Frobenius. Level 5 is full, so the final-window gaps are exactly

```text
(6s+B^c) union (7s+Q^c) union (8s+C^c).
```

The displayed complement formulas follow directly from the EXP-009/011 definitions of `B`, `Q`,
and `C`. Their cardinalities are `3p`, `5p`, and `2p`, respectively.

## 2. Explicit witnesses exclude every lower gap

Every value `5s+b`, with `0<=b<s`, is a minimal generator of `Lambda_p`.

Let `f=ks+r` be a gap below `4s`, where `0<=k<=3` and `0<=r<s`.

- If `k=0`, then `r>=1`. Choose `b=s-r`. The sum is `6s`, whose residue zero is absent from `B`.
- If `k=1` and `r=0`, choose `b=0`; again the sum is the gap `6s`. If `r>0`, choose `b=s-r`;
  the sum is `7s`, whose residue zero is absent from `Q`.
- If `k=2`, choose `b=s-1-r`. The sum is `7s+(s-1)`, and `s-1` is absent from `Q`.
- If `k=3`, choose the same `b=s-1-r`. The sum is `8s+(s-1)`, and `s-1` is absent from `C`.

In every case a minimal generator sends `f` to a gap, so `f` is not pseudo-Frobenius.

It remains to treat a level-4 gap `f=4s+r`, where `r` is not in `A`. Since `4s+a` is a minimal
generator for every `a` in `A`, it suffices to find `a` such that `r+a<s` and `r+a` is not in `C`.

- If `r` is not in `C`, take `a=0`.
- The remaining set `C` minus `A` is `[p+1,2p] union [4p-1,5p-2]`.
- For `r` in `[p+1,2p]`, take `a=2p+1-r`, which lies in `[1,p]` and gives the gap residue `2p+1`.
- For `r` in `[4p-1,5p-2]`, take `a=5p-1-r`, which lies in `[1,p]` and gives the gap residue
  `5p-1`.

Thus no gap below `5s` is pseudo-Frobenius. Combined with Section 1, this proves the formula.

## 3. Type, reduced type, and almost symmetry

For a numerical semigroup ring, the Cohen-Macaulay type is the cardinality of the
pseudo-Frobenius set. Therefore

```text
type = 3p+5p+2p = 10p.
```

Maitra-Mukundan Theorem 2.13 identifies reduced type with the number of gaps in the final
multiplicity window. Section 1 shows that this is also `10p`; equivalently, Proposition 3.7 shows
that the ring has maximal reduced type.

Finally, EXP-011 gives genus `g=38p-1` and Frobenius number `F=54p-1`. An almost-symmetric
numerical semigroup satisfies `2g=F+type`, but here

```text
2g = 76p-2,
F+type = 64p-1,
2g-(F+type) = 12p-1 > 0.
```

Hence `Lambda_p` is not almost symmetric for every `p>=4`, and the associated completed numerical
semigroup ring is not almost Gorenstein.

## 4. Computational support

The all-parameter proof above does not depend on a finite sweep. The exact implementation checked
every `p=4,...,300` by two routes:

1. a global bitset intersection tests every gap against every minimal generator;
2. an independently organized Apéry-poset computation extracts maximal Apéry elements modulo
   `4s` and subtracts the multiplicity.

A separate implementation rehashes all 297 rows and reconstructs complete gap and generator
semantics at `p=4,5,17,73,151,300`. A deleted predicted PF value and an injected lower gap are
both rejected.
