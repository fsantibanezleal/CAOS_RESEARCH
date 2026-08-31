# EXP-044 verdict

Status: **REFUTED overall** for `p=8,...,11`. P1 and P3 pass; P2 fails.

Deleting either pivot-dependent row atom `D:B` or `K:C0` eliminates every tested first
Bockstein, confirming that both are necessary interfaces. However, retaining only their union
also gives equal ranks over `GF(2)`, `GF(3)`, and `GF(5)` and Bockstein rank zero at every
parameter. The proposed two-atom bridge is therefore not sufficient.

The finite torsion belongs to a larger signed circuit involving additional normalized row atoms.
This redirects the proof search from a guessed two-block normal form to an exhaustive six-atom
subset lattice, followed by integral matching only after a stable minimal carrier is identified.
The result is an exact localization correction, not an all-parameter theorem, and it does not
trigger a manuscript or Zenodo update.
