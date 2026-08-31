# EXP-042 preflight - Bockstein normal form of the persistent isolated sector

Date: 2026-08-31. Source-complete for this experiment declaration.

## Evidence entering the gate

EXP-041 exactly reproduces the frozen `p=8,...,11` component partitions and proves finitely that
the isolated components share one normalized twelve-atom semantic skeleton. Their row/column
sizes remain small enough for bit-packed exact mod-two reduction:

```text
p=8:  2675 x 1094, defect 3
p=9:  4757 x 1729, defect 4
p=10: 7973 x 2607, defect 5
p=11: 12711 x 3785, defect 7.
```

The frozen odd-prime ranks agree over `GF(3)` and `GF(5)`. EXP-042 does not reinterpret that
agreement as a rational-rank proof.

## Mathematical construction

Let `M_p` be the signed integer presentation matrix of the isolated component. Reduce its columns
canonically over `GF(2)` while tracking a basis `z_j` of `ker(M_p mod 2)`. For each binary lift,
`M_p z_j` is entrywise even. Define

```text
beta_p(z_j) = (M_p z_j)/2 mod (2, im(M_p mod 2)).
```

This is the first matrix Bockstein from the mod-two kernel to the mod-two cokernel. Its rank is
basis-independent. A nonzero class is a direct certificate of a factor divisible by two but not
four in the corresponding elementary-divisor direction. Without a rational-rank upper bound, the
calculation is stated as an exact lower bound on order-exactly-two directions, not a complete
Smith normal form.

## Source check

Algebraic discrete Morse theory permits homology-preserving cancellation of invertible matched
entries in free chain complexes (<https://arxiv.org/abs/math/0501179>). Squarefree divisor
complexes encode multigraded Betti numbers of numerical semigroup rings
(<https://arxiv.org/abs/1804.06632>), and characteristic dependence is naturally tied to torsion
in such homology (<https://arxiv.org/abs/1009.4243>). OI/FI noetherianity can stabilize compatible
resolution families (<https://arxiv.org/abs/1710.09247>), while the more general combinatorial-
category framework can force rational Hilbert series (<https://arxiv.org/abs/1409.1670>).

These sources support the selected tools but do not provide the CAOS block, its Bockstein, a
transition map, or the desired recurrence. The experiment remains an original finite exact
calculation.

## Route decision

The Bockstein route dominates another coefficient sweep because it targets the arithmetic cause
of the rank gap. Full Smith form is deferred until exact cancellation makes it resource-safe.
Representation stability is downstream: an identical atom alphabet is not a functor, so explicit
`p -> p+1` chain maps remain mandatory.

No manuscript or Zenodo gate is open at declaration.
