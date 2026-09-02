# EXP-047 proof record - exact relative carrier modules

Date: 2026-09-02. Status: **CONFIRMED FINITELY** for `p=8,...,11`. CPU-only exact integer
arithmetic, with independent modular and determinant certificates.

## Exact sequence and construction

For a row inclusion `S subset T`, write the signed presentation as

```text
M_p(T) = [A; B],  A=M_p(S).
```

Projection to the `S` rows induces

```text
0 -> Q_p(S,T) -> coker M_p(T) -> coker M_p(S) -> 0,
Q_p(S,T) = Z^(T-S) / B(ker_Z A).
```

The runner computes a transformed row Hermite form `H=U*A^T`. Because `U` is unimodular, the
rows of `U` corresponding to the zero rows of `H` are a saturated basis of `ker_Z A`. Applying
the added-row block `B` produces a much smaller exact presentation of `Q_p(S,T)`, whose Smith
form is then computed.

The full campaign took 1,799.343 seconds. It used two transformed HNFs per parameter, sharing the
mask-58 kernel between both alternative completions.

## Exact relative Smith forms

All three declared predictions pass.

| `p` | inclusion | relative matrix | exact rank | unit factors | free rank | nonunit Smith factors |
|---:|---:|---:|---:|---:|---:|---:|
| 8 | `58->59` | 28 x 114 | 13 | 11 | 15 | `2,2` |
| 9 | `58->59` | 36 x 148 | 15 | 13 | 21 | `2,2` |
| 10 | `58->59` | 45 x 187 | 17 | 15 | 28 | `2,2` |
| 11 | `58->59` | 55 x 233 | 19 | 17 | 36 | `2,2` |
| 8 | `58->62` | 51 x 114 | 22 | 20 | 29 | `2,2` |
| 9 | `58->62` | 68 x 148 | 26 | 24 | 42 | `2,2` |
| 10 | `58->62` | 87 x 187 | 30 | 28 | 57 | `2,2` |
| 11 | `58->62` | 108 x 233 | 34 | 32 | 74 | `2,2` |
| 8 | `56->58` | 827 x 131 | 17 | 16 | 810 | `2` |
| 9 | `56->58` | 1477 x 168 | 20 | 18 | 1457 | `2,2` |
| 10 | `56->58` | 2487 x 210 | 23 | 20 | 2464 | `2,2,2` |
| 11 | `56->58` | 3968 x 259 | 26 | 22 | 3942 | `2,2,2,2` |

Consequently,

```text
Q_p(58,59) = Z^binom(p-2,2) direct-sum (Z/2Z)^2,
Q_p(58,62) = Z^(p^2-4p-3) direct-sum (Z/2Z)^2,
Q_p(56,58) = Z^f_p direct-sum (Z/2Z)^(p-7)
```

for the four tested parameters, where `f_p=rows(R1)-(3p-7)` in the third line. The formulas are
finite identities, not yet claims for every `p`.

The transformed HNFs also certify the rational ranks of masks `56` and `58`; relative-rank
recomposition certifies those of masks `59` and `62`. Together with the prior exact Bockstein
ranks, their complete tested 2-primary cokernel torsion is therefore

```text
mask 56: 0, 0, 0, (Z/2),
mask 58: (Z/2)^1, (Z/2)^2, (Z/2)^3, (Z/2)^5,
mask 59: (Z/2)^3, (Z/2)^4, (Z/2)^5, (Z/2)^7,
mask 62: (Z/2)^3, (Z/2)^4, (Z/2)^5, (Z/2)^7.
```

Thus the relative 2-primary orders multiply exactly across all three inclusion sequences. Because
all factors are elementary, each induced 2-primary short exact sequence splits noncanonically as
an `F_2`-vector-space sequence. This proves that the two relative classes account for the entire
completion increment and that the `p-7` threshold quotient plus the mask-56 class account for the
mask-58 sequence.

## Independent audit

The auditor reconstructs the source and added row sets and rehashes every compact relative
matrix. It then uses an unrelated sparse, low-pivot modular reducer. Products of one or two
verified 61-bit primes exceed exact Hadamard bounds for every next minor, proving all twelve
rational-rank ceilings.

For the top determinantal divisor, explicit Bareiss minors have sampled gcd `4` for every stable
completion and `2,4,8,16` for `56->58`. The mod-two rank losses show that these powers are spread
over exactly `2` or `p-7` even invariant factors. Therefore every nonunit factor is exactly `2`;
no odd torsion or higher 2-power is possible. All 202 audit checks pass.

The primary result SHA-256 is
`f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c`, with internal artifact
hash `d74557c6cd9ca4874bbee4c77b96b5c5d8dd19a7daf8c711766baacb45eec165`. The audit certificate
has internal hash `edf5d4f36fe16c666bb9ea4068c2007cbe3c7643f2e38b97a085e9f855083e28` and external SHA-256
`bbdfaca4f9ba2032beac04f23b9e1db13fd6f1ca37518b957d91a1f55321c028`.

## What could make this wrong?

- The transformed-HNF computation and its unimodular contract are in the primary FLINT trust
  boundary. The independent audit certifies the resulting compact matrices and their Smith data,
  but does not independently regenerate all twelve saturated source kernels.
- The masks are row projections of the finite isolated matrices; no uniform chain subcomplex or
  deletion-contraction functor has yet been constructed.
- Four consecutive parameters do not prove the displayed formulas for `p>=12`.
- Noncanonical splitting of elementary 2-primary groups does not supply a semantic chain map
  between the `R0` and `R2` completions.

Frozen source hashes, exact HNF annihilation, source/target rank recomposition, compact artifacts,
and the independent determinant certificates address arithmetic and serialization failure inside
the declared finite scope.

## Next proof gate and publication decision

The next gate is symbolic rather than another coefficient. Extract a certificate-producing
unimodular reduction of each compact relative matrix to

```text
I_(2p-5) direct-sum 2I_2,       for 58->59,
I_(4p-12) direct-sum 2I_2,      for 58->62,
I_(2p) direct-sum 2I_(p-7),     for 56->58,
```

plus zero rows and columns, then classify the pivot operations by the interval atoms that generate
them. A uniform proof requires formulas for those bases and compatibility under `p->p+1`; an
additional `p=12` HNF is lower priority.

EXP-047 is a strong finite exact module theorem and a relevant proof target, but it is not yet a
transferable all-parameter result or a complete lower strand. Manuscript v0.23 and Zenodo record
`22181972` therefore remain unchanged.
