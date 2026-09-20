# EXP-064 proof and certificate interpretation

Date: 2026-09-20. Scope: exact finite integral result for `p=8,9,10,11`.

## 1. Rational-rank certificates

For each frozen signed component matrix and mask `m` in `56,58,59,62`, let
`A_(p,m)` be the exact row projection. Its entries are `0,+1,-1`. The rank
over `GF(3)` supplies a lower bound `r` for its rational rank.

For every distinct verified 61-bit prime `q_i`, sparse exact elimination gives
rank exactly `r`. Hence every `(r+1)` minor is divisible by
`Q=product(q_i)`. If `d` is the maximum squared Euclidean norm of a column,
Hadamard's inequality bounds the absolute value of every such minor by
`d^((r+1)/2)`. The stopping condition

```text
Q^2 > 4*d^(r+1)
```

therefore makes a nonzero divisible minor impossible. Thus the rational rank
is exactly `r`. The last prime is necessary in every certificate: removing it
makes the strict coverage inequality fail.

The certified ranks are:

| `p` | mask 56 | mask 58 | mask 59 | mask 62 |
|---:|---:|---:|---:|---:|
| 8 | 963 | 980 | 993 | 1002 |
| 9 | 1561 | 1581 | 1596 | 1607 |
| 10 | 2397 | 2420 | 2437 | 2450 |
| 11 | 3526 | 3552 | 3571 | 3586 |

## 2. Why the first Bockstein determines the exponent

Put an integer matrix in Smith form with nonzero diagonal entries `d_i`.
Unimodular source and target changes preserve rational rank, rank modulo two,
and the first Bockstein. Then

- `rank_Q-rank_F2` counts the even `d_i`;
- on an even diagonal coordinate, the first Bockstein is multiplication by
  `d_i/2 mod 2`;
- consequently its rank counts exactly the `d_i` with 2-adic valuation one.

Equality of the rank gap and Bockstein rank proves that every even invariant
has valuation exactly one. The complete 2-primary torsion is therefore an
elementary abelian group of that rank. The diagonal controls `[2]` and `[4]`
give Bockstein ranks one and zero, respectively, preventing the invalid
inference from rank gap alone.

For all 16 carrier matrices the equality holds. Their exact 2-primary types
are:

| `p` | mask 56 | mask 58 | mask 59 | mask 62 |
|---:|---:|---:|---:|---:|
| 8 | `0` | `(Z/2)^1` | `(Z/2)^3` | `(Z/2)^3` |
| 9 | `0` | `(Z/2)^2` | `(Z/2)^4` | `(Z/2)^4` |
| 10 | `0` | `(Z/2)^3` | `(Z/2)^5` | `(Z/2)^5` |
| 11 | `(Z/2)^1` | `(Z/2)^5` | `(Z/2)^7` | `(Z/2)^7` |

## 3. Exact integral consequence for the triangle classes

EXP-062 supplies an integral source with boundary `+/-2x_T`, so every triangle
image has order dividing two. EXP-063 identifies the literal carrier
coordinates and computes their complete images in `coker(A_(p,m) mod 2)`.

If the 2-primary torsion of a finitely generated abelian group `G` has exponent
two, the natural map from its order-two subgroup to `G/2G` is injective:
after decomposing `G` into free, primary and odd parts, it is the identity on
each `Z/2` factor. Thus an order-two candidate that is zero modulo two is
integrally zero. Mod-two-independent order-two candidates remain integrally
independent.

Applying this lemma gives the exact finite conclusions:

- In masks 59 and 62, all triangle images form the complete 2-primary subgroup.
- In mask 58, `(0,1,p-3)` and `(0,2,p-4)` vanish integrally. Every other
  triangle image is nonzero, independent, and together they form the complete
  2-primary subgroup.
- In mask 56, all triangle images vanish for `p=8,9,10`. At `p=11`, only
  `(2,3,4)` is nonzero, and it generates the complete 2-primary subgroup.

This argument proves integral vanishing without constructing new source
coefficients. It is exact but nonconstructive at that witness level.

## 4. Independent audit and limits

The auditor independently reconstructs all 16 projections, verifies 1,100
stored primes, recomputes every modular rank with reversed column order and
low pivots, checks all 16 exact products and minimally sufficient coverage
prefixes, rejects 16 entry mutations, and checks the two synthetic exponent
controls plus all 16 triangle consequences.

The theorem is finite. It does not prove these ranks or elementary exponents
for all `p`, give uniform integral endpoint sources, determine free or odd
parts, classify the full original cokernel, or establish the lower-strand
recurrence.
