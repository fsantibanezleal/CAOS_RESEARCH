# Simple critical zeros in short intervals: stability, parity, localization, Hilbert compression, and spectral defect

Version `v0.07`, dated 20 September 2026.

This version contains two new linked results. First, the local Selberg argument
is proved for every fixed finite-rank admissible vector profile. Applying it to
Pearce-Crump's source-certified six-square constant and then to the sharp
Hilbert-parity product gives

`0.5458837 < theta_6 < 0.5458838`.

At `theta=0.545884`, where the fully reproducible rank-three term is still
negative, the rank-six term is greater than
`2.5541123454645702e-7`. At `theta=0.5459`, it is greater than
`0.0000177645181613023236390595079`, improving the rank-three value by more
than `9.2635430617773560e-7`.

Second, the manuscript retains the simple-real Gram spectral defect in the
sharp finite product

`(Q-S-D(G))(N-O) >= 2(N-S)^2`.

Using the radius ratio `11/5` gives a strict spectral correction at every
positive point of the rank-six curve. At `theta=0.5459`, the correlated exact
gain is greater than `1.7766622541125682e-68`.

The six-square profile and constant are attributed to Pearce-Crump. The public
source prints the certified constant interval but not the profile matrix, so
the localization and scalar consequences are independently checked while the
constant itself is not independently reconstructed. The result is asymptotic,
internally reviewed, and not peer reviewed. It does not solve the Riemann
hypothesis.

Evidence:

- [EXP-008 rank-six local transfer](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/).
- [EXP-007 spectral-defect parity](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/).
- [EXP-006 Hilbert-parity compression](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-006-hilbert-parity-compression/).
- Concept DOI: [10.5281/zenodo.22727388](https://doi.org/10.5281/zenodo.22727388).
- The v0.07 version DOI is reserved before the final build and inserted into
  the manuscript header.
