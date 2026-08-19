# EXP-011 source and premise preflight

Date: 2026-08-10. This preflight was completed before EXP-011 implementation or execution.

## Primary-source and public-record check

- Leamer, *Torsion and Tensor Products Over Domains and Specializations to Semigroup Rings*,
  arXiv:1211.2896, supplies the two-generated ideal dictionary already calibrated by EXP-001.
- Dey and Lyle, *Centers of Endomorphism Rings and Reflexivity*, arXiv:2510.02210v2, supplies the
  endomorphism-center consequences used in EXP-002. The arXiv record still identifies v2 as the
  current version, updated 2025-10-03. The current PDF was archived before the verdict at
  `E:/_Datos/caos-research/huneke-wiegand/sources/dey-lyle-2510.02210v2.pdf`, SHA-256
  `2f1521f79510ef50fb81d5f029935d5a2c9b7e4c030bc698b7e4f5caacf56fad`. Proposition 4.1(2) and
  Theorems 4.2, 4.3, and 4.4 were reread directly against the EXP-011 family hypotheses.
- Landeros et al., *Families of numerical semigroups and a special case of the Huneke-Wiegand
  conjecture*, arXiv:2404.12519v1, remains a positive result for generalized arithmetic-sequence
  semigroups. EXP-009 already proves that its family lies outside that class.
- The public candidate repository at
  `https://github.com/sonpham-org/huneke-wiegand-candidate-verification` remains a seed-example
  verification package. Its tree and status record contain no parametric family or uniform
  endomorphism-semigroup theorem.

A targeted GitHub repository/code search found no separate public infinite-family result. That
negative search is not a novelty proof. The mathematical claim must stand on the committed exact
derivation, and priority for the first public counterexample remains Son Pham's.

## Premise audit

1. EXP-009 proves the exact blocks of `Gamma_p`, symmetry, generation, and rigidity for every
   integer `p>=4`.
2. EXP-002 confirms for the public seed that, for `J=(1,t^s)` with value set
   `V=Gamma union (s+Gamma)`, the endomorphism values are the adjacent-layer intersection
   `Lambda={n: n and n+s belong to V}`. Its Dey-Lyle dependency map is theorem-level and does not
   depend on the seed's particular exponents.
3. The family rings are one-dimensional Gorenstein local domains because their numerical
   semigroups are symmetric. Their ideals are faithful, torsion-free, two-generated, nonprincipal,
   and rigid by EXP-009.

No unresolved premise is used to derive the proposed block formula. The only external theorem use
after the semigroup calculation is the already audited Dey-Lyle implication map.

## Invariant-first derivation

Write residues in `[0,s-1]`. From EXP-009, the value set
`V_p=Gamma_p union (s+Gamma_p)` has residue blocks

```text
V_0={0}, V_1={0}, V_2=V_3=empty,
V_4=A, V_5=V_6=[0,s-1], V_7=B, V_8=C,
V_k=[0,s-1] for every k>=9.
```

Therefore the endomorphism block at level `k` is simply `V_k intersect V_(k+1)`. The only new
nontrivial block is

```text
Q = B intersect C = [p+1,2p-2] union {2p,4p}.
```

This predicts `Lambda_p=Gamma_p union (7s+Q) union {13s-1}` without a search.
