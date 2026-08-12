# EXP-019 preflight - graded torsion and Buchsbaum anatomy

Date: 2026-08-12.

## Why this path

EXP-018 proves that the conductor tangent cone

```text
G_p=gr_(T_p)(R_p)
```

has depth zero for every `p>=4`, but the Valabrega--Valla kernel by itself does not determine the
full finite-length torsion or its annihilator. A larger parameter sweep would not resolve that
structural question. The next finite target is therefore the complete graded module
`H^0_(M_p)(G_p)` and the Buchsbaum condition, where

```text
M_p=(m_p/T_p) direct-sum G_(p,+)
```

is the homogeneous maximal ideal.

## Source boundary

D'Anna, Mezzasalma, and Micale study the one-dimensional criterion that an associated graded ring
is Buchsbaum exactly when its homogeneous maximal ideal annihilates its zeroth local cohomology:

- M. D'Anna, M. Mezzasalma, and V. Micale, *On the Buchsbaumness of the Associated Graded Ring of
  a One-Dimensional Local Ring*, Communications in Algebra 37 (2009), 1594--1603,
  `https://doi.org/10.1080/00927870802116521`.

D'Anna, Micale, and Sammartano give the corresponding graded local-cohomology viewpoint for
numerical semigroup rings:

- M. D'Anna, V. Micale, and A. Sammartano, *On the associated graded ring of a semigroup ring*,
  Journal of Commutative Algebra 3 (2011), 147--168,
  `https://doi.org/10.1216/JCA-2011-3-2-147`.

The present filtration is by the conductor `T_p`, not by the maximal ideal. Accordingly, EXP-019
will prove its colon-saturation formula directly for `gr_(T_p)(R_p)` and use only the general
one-dimensional Buchsbaum criterion. Maximal-ideal-specific Apery formulas from the cited papers
will not be imported.

## Pre-implementation profile

For a homogeneous monomial class represented by `t^v` in degree `n`, membership in zeroth local
cohomology is equivalent to

```text
t^v T_p^k subset T_p^(n+k+1)
```

for some `k`. EXP-017 gives `v(T_p^k)=[4ks,infinity)` for every `k>=4`. Therefore the saturation
threshold is predicted to be `v>=4(n+1)s`. Comparing that threshold with the exact power profiles
from EXP-016--018 predicts

```text
H^0_(M_p)(G_p)_0 = span_k{t^(5s+h)+T_p : h in H_p},
H_p={2p-1,4p-1} union [4p+1,5p-2],
H^0_(M_p)(G_p)_n = 0 for n>=1.
```

Thus the full torsion should have length `p`, not merely contain a length-`p` kernel. Since every
positive value in `R_p` is at least `4s`, every product of a listed torsion representative with
either `m_p` or `T_p` has value at least `9s`; the exact profiles contain `[9s,infinity)` in
`T_p` and in `T_p^2`. This predicts `M_p H^0_(M_p)(G_p)=0` and hence a Buchsbaum, non-Cohen--Macaulay
tangent cone with unbounded Buchsbaum invariant `p`.

This prediction is not a result until the separately declared experiment passes its symbolic,
exact-campaign, independent-audit, and adversarial-control gates.
