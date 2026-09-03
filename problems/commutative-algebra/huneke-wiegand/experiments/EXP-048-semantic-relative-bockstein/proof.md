# EXP-048 proof record - semantic relative Bockstein chains

Date: 2026-09-02. Status: **REFUTED overall**, with P1 confirmed finitely and explicit uniform
completion-chain candidates retained. CPU-only exact integer and binary arithmetic.

## Canonical finite object

For each EXP-047 relative matrix `R`, the runner computes

```text
ker(R mod 2) -> coker(R mod 2),  z |-> Rz/2 mod 2.
```

The rows are first placed in a fixed lexicographic order by their exact interval coordinates. The
image of `R mod 2` and the Bockstein image are then put in reduced row-echelon form over `F_2`.
This makes the stored representative subspace canonical relative to that semantic order. Reversing
the relation-column traversal gives the same certificate in all twelve cases.

Original row labels were independently reconstructed from the full `(p,2)` presentation. Every
isolated signed hash, relative added-row hash, and frozen shape agrees with EXP-042 and EXP-047.

## Declared predictions

P1 passes. The three relative Bockstein ranks are

| `p` | `58->59` | `58->62` | `56->58` |
|---:|---:|---:|---:|
| 8 | 2 | 2 | 1 |
| 9 | 2 | 2 | 2 |
| 10 | 2 | 2 | 3 |
| 11 | 2 | 2 | 4 |

These agree exactly with `rank_Q(R)-rank_F2(R)` from EXP-047, so the Bockstein images account for
every relative elementary factor-two class.

P2 is refuted. The canonical representatives are small and linear, not bounded:

```text
58->59 support sizes: (p-4,p-4),
58->62 support sizes: (2p-8,p-4).
```

P3 is also refuted. Although the rank is exactly `p-7`, the threshold representatives do not have
one nonnumeric support skeleton. Their support sizes are

```text
p=8:  13,
p=9:  18,14,
p=10: 24,19,32,
p=11: 31,25,38,20.
```

Thus the fixed canonical quotient section does not turn `56->58` into translates of one local
class.

## Explicit completion-chain candidates discovered

The P2 failure is structured enough to replace the rejected bounded-template model. Put

```text
L0=[1,p],  L1=[3p,4p-2].
```

Let `rho_A(U;V;q)` denote the added `R0` row with exterior set

```text
(L0 minus U) union (L1 minus V) union {6p,10p},
```

product kind `A`, and product value `q`. Let `rho_B(u;V;q)` denote the analogous added `R2` row
with `L0` missing only `u`, `L1` missing `V`, product kind `B`, and product value `q`.

For every tested `p`, the two canonical `58->59` Bockstein representatives are exactly

```text
alpha_(p,j)
 = sum rho_A({p-1-j,w}; {3p,3p+j}; p+w-3),       j=1,2,
       4<=w<=p, w != p-1-j.
```

Their supports have size `p-4`. The two canonical `58->62` representatives are exactly

```text
beta_(p,1)
 = sum_(r=1,2) sum_(v=3)^(p-2)
     rho_B(p-2; {3p,3p+r,3p+v}; 4p+v+r-4),

beta_(p,2)
 = sum_(v=3)^(p-2)
     rho_B(p-3; {3p,3p+2,3p+v}; 4p+v-3).
```

Their supports have sizes `2p-8` and `p-4`. An independent formula audit regenerates these four
sets without reading their stored hashes and matches every row at `p=8,...,11`.

These formulas were discovered after the declared P2 failed. They are therefore exact finite
classifications and all-parameter conjectural definitions, not confirmatory evidence for every
`p`.

## Independent audit

The separate auditor performs 78 checks. It:

- verifies the frozen run, result, and EXP-047 hashes;
- recomputes each Bockstein rank as `rank_Q-rank_F2` from EXP-047;
- rehashes every stored representative;
- checks every reverse-traversal agreement;
- regenerates all four `alpha/beta` chain formulas directly; and
- verifies the four linear support laws.

All 78 checks pass. The primary result SHA-256 is
`ba44eae4c9193bc941411b059dc7a7d7a4c69dff3d818e05d3395338e125a400`, with internal artifact
hash `e19814f026ca775fe6780440ec45389cbc75883bc53b6f39009377cd7af95bf8`. The audit certificate
has internal hash `880e428c8abe78a7430546b1fb3d2e67b48b17e1c3a85b6e04fa402aff75e8da` and external SHA-256
`738d3b8e77c3a7cf2ca82692d7d7c9b1b4b97799a82ed3d808f8a6a1e621efed`.

## What could make this wrong?

- The `alpha/beta` formulas are post-result discoveries on four parameters. They require a
  symbolic lift before they can be asserted for every `p`.
- Canonical representatives depend on the declared semantic row order. The Bockstein subspace is
  intrinsic, but these particular representatives are not claimed to be basis-independent.
- A Bockstein representative only describes the factor-two class modulo the relative image. A
  uniform integral proof still needs source-domain cycles whose exact boundaries are twice these
  chains, or an equivalent unimodular/Morse reduction.
- EXP-048 independently reconstructs labels but deliberately reuses the validated EXP-036/037
  presentation engines. The frozen signed hashes protect that trust boundary.

## Consequence and next proof gate

The strongest route splits. The stable completions now have explicit targets: construct semantic
source-domain cycles `x_(p,j)` and `y_(p,j)` satisfying

```text
A_p x_(p,j)=0,  B_p x_(p,j)=2 alpha_(p,j),
A_p y_(p,j)=0,  B_p y_(p,j)=2 beta_(p,j),
```

up to an explicitly controlled relative boundary, and prove independence by two parity
functionals. This would establish the completion `(Z/2)^2` uniformly without a full Smith form.

The threshold `56->58` should not be forced into the same model. Its canonical representatives
are nonuniform, so dual parity characters or a relative algebraic-Morse filtration now outrank
direct representative fitting.

No manuscript or Zenodo update is triggered. The result identifies a concrete uniform proof
target but remains finite.
