# EXP-042 proof record - exact first Bockstein of the isolated sector

Date: 2026-08-31. Status: **CONFIRMED** finitely for `p=8,...,11`. CPU-only exact
integer and finite-field arithmetic.

## Construction

For each persistent isolated signed matrix `M_p`, canonical mod-two column reduction supplies a
basis of `ker(M_p mod 2)`. If `z` is a binary lift of one such vector, `M_p z` is entrywise even.
The first matrix Bockstein is

```text
beta_p(z) = (M_p z)/2 mod (2, im(M_p mod 2)).
```

In Smith coordinates, its rank is the number of nonzero elementary divisors whose 2-adic
valuation is exactly one. It therefore detects genuine factor-two arithmetic, not only a
difference between two field ranks.

## Exact results

The independent extractor reproduced every frozen support hash, signed hash, dimension, nonzero
count, and available finite-field rank. New `GF(5)` ranks at `p=8,9` equal the frozen `GF(3)`
ranks, as declared.

| `p` | isolated matrix | ranks `GF(2)/GF(3)/GF(5)` | mod-two kernel | `rank(beta_p)` |
|---:|---:|---:|---:|---:|
| 8 | `2675 x 1094`, 6747 nonzeros | `999/1002/1002` | 95 | 3 |
| 9 | `4757 x 1729`, 11849 nonzeros | `1603/1607/1607` | 126 | 4 |
| 10 | `7973 x 2607`, 19654 nonzeros | `2445/2450/2450` | 162 | 5 |
| 11 | `12711 x 3785`, 31073 nonzeros | `3579/3586/3586` | 206 | 7 |

Thus P1, P2, and P3 pass finitely. The Bockstein ranks are exactly `3,4,5,7`, matching the
odd-minus-two rank defects. Consequently the four isolated integer matrices have respectively
exactly `3,4,5,7` nonzero Smith factors of 2-adic valuation one. This does not yet exclude
additional factors divisible by four because the rational rank has not been upper-certified.

## Adversarial audit and correction

The auditor reconstructs all stored matrices from their signed columns, recomputes ranks over
three fields with separate code, reproduces every forward/reverse kernel and witness hash, and
then repeats the Bockstein with the opposite pivot convention. All four implementations give
ranks `3,4,5,7`.

The representative atom is not intrinsic. High-pivot reduction places all independent image
representatives in

```text
row:D:B:[-2,-3,2,0,0,0,0,0,0,0],
```

while low-pivot reduction places them in

```text
row:K:C0:[-2,-2,1,0,0,0,0,0,0,0].
```

This is evidence for a bridge between the two row families, but it forbids claiming that either
atom alone canonically carries the torsion.

The primary result SHA-256 is
`3c4ae292fb17a5daf473aee0ed37e473000de686607b5da0a0f4c357a8216ee2`. Matrix artifact hashes
for `p=8,9,10,11` are respectively

```text
7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff
00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c
c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d
69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9.
```

The audit certificate has internal hash
`a173de6a8454f44a84914d64273c12a61250e0d95ae7719117f1d3720a9467d8` and external SHA-256
`e35f38a86c4d6ab807d32cb3e8cd99b348e310df1d1a6840818a9ab84157cb8a`.

## Boundary and next proof gate

EXP-042 proves finite exact Bockstein statements, not the all-parameter recurrence or lower-strand
theorem. The strongest next finite gate is an exact rational-rank upper certificate. If
`rank_Q(M_p)=rank_GF(3)(M_p)`, the Bockstein rank equals the total number of even Smith factors and
the isolated 2-primary torsion is completely `(Z/2)^(3,4,5,7)` at the four parameters.

A Hadamard-plus-multiple-prime certificate can prove that upper bound without a full Smith form:
make every `(r+1)` minor divisible by a product of distinct primes larger than twice its Hadamard
bound. This is the next declared-experiment candidate. EXP-042 alone does not trigger a manuscript
or Zenodo update.
