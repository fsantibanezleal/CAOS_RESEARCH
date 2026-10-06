# Simple critical zeros in short intervals: stability, pressure, parity, and localization

Published version 0.05, 2026-09-20. Sole author: Felipe Santibáñez-Leal,
ORCID [0000-0002-0150-3246](https://orcid.org/0000-0002-0150-3246).

The new result localizes Pearce-Crump's optimized Selberg detector. For every fixed
`1/2 < theta < 1`, it gives a lower asymptotic proportion
`(theta-1/2)/(4 e C3)` of distinct odd-multiplicity critical zeros in
`(T,T+T^theta]`, where the reproducible rank-three constant is
`C3 = 0.6567752140190419405677628751089899133...`.

Combining the local odd-zero density with the finite parity transfer proves the
simple-critical lower bound

`max(0, c(theta), (c(theta)+(theta-1/2)/(2 e C3))/3)`.

Its third numerator is strictly increasing, and exact interval arithmetic places its
unique zero in `(0.5459,0.546)`. At `theta=0.546`, a fixed legal mollifier witness gives
a simple-critical lower proportion greater than `0.0000976239413345`; direct evaluation
of the optimized curve gives `0.0000994910410327`. This improves the previously available
explicit positivity threshold `0.550193964744154...` for this short-interval result.

This is a self-published preprint. It does not prove the Riemann hypothesis, give an
effective starting height, or establish a global zero-density record. Automated
adversarial review is separate from external peer review and end-to-end formalization.

- [Paper PDF](main.pdf) and [LaTeX source](main.tex).
- [EXP-005 proof and exact certificate](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/).
- [EXP-004 parity transfer](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/).
- [EXP-003 pressure certificate](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/).
- [Publication gate](publication-gate.json), [render review](render-review.json), and
  [public download receipt](publication-receipt.json).
- Version DOI: [10.5281/zenodo.22851518](https://doi.org/10.5281/zenodo.22851518).
- Latest-version concept DOI: [10.5281/zenodo.22727388](https://doi.org/10.5281/zenodo.22727388).

The public receipt records an unauthenticated download matching all 526,178 published
PDF bytes. The previously published v0.04 source, PDF, and metadata remain byte-identical
in [the archive](versions/v0.04/). The manuscript is CC BY 4.0 and research code is MIT.

Build from this directory with three passes of
`pdflatex -interaction=nonstopmode -halt-on-error main.tex`, then render every page with
`pdftoppm -png` and inspect it. The publication gate is tied to the reviewed PDF bytes.
