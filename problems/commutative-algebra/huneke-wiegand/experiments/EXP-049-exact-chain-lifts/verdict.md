# EXP-049 verdict

Status: **REFUTED overall**; P1 and P2 fail, while P3 passes finitely.

The four literal zero-one completion chains from EXP-048 are not integral order-two vectors. For
both chains in both inclusions and every `p=8,...,11`, exact row-Hermite membership gives

```text
2a not in im_Z(R).
```

An independent reversed-order HNF audit confirms all sixteen failures. The chains remain correct
mod-two Bockstein representatives, but an exact torsion representative must include a nonzero even
correction `b=a+2c`.

The dual side succeeds. Low-pivot and high-pivot binary solvers independently construct two
functionals annihilating `R` and pairing as the identity with the two named chains in every case.
All supports have size at most four. For `58->62`, the low-pivot supports satisfy the two explicit
uniform candidate formulas in `proof.md` throughout the tested range; the 98-check audit rebuilds
and verifies them.

This is a proof-route correction, not a loss of the `(Z/2)^2` result. The next primal action is to
carry exact Bockstein provenance and classify the necessary even corrections. The uniform lower
bound should be attacked first through the bounded duals; the upper bound remains a separate
relative-Morse or free-complement theorem.

No manuscript or Zenodo update is triggered.
