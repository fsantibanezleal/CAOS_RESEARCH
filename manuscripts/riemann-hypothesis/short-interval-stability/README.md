# Simple critical zeros in short intervals: stability, pressure, and parity

Published version 0.02, 2026-09-12. Sole author: Felipe Santibanez-Leal,
ORCID [0000-0002-0150-3246](https://orcid.org/0000-0002-0150-3246).

This preprint combines the attributed finite stability inequality with an odd-multiplicity
parity transfer and a pressure certificate. EXP-004 proves a qualitative extension of the
simple-critical positivity range below Wang's cosine root, with an unspecified fixed
classical density constant. EXP-003 gives a certified theta=3/4 simple-critical lower
proportion of 0.4190878881701117279 and distinct companion 0.7095439440850558640.
It does not prove RH or claim a global record. Automated adversarial review is distinguished
from external peer review and end-to-end formalization.

- [Paper PDF](main.pdf) and [LaTeX source](main.tex).
- [EXP-004 proof and exact certificate](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-004-parity-density-transfer/).
- [EXP-003 pressure proof and certificate](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-003-odd-frame-pressure/).
- [Publication gate](publication-gate.json) records final content, PDF, rendered-page hashes and checks.
- Version DOI: [10.5281/zenodo.22728744](https://doi.org/10.5281/zenodo.22728744).
- Latest-version concept DOI: [10.5281/zenodo.22727388](https://doi.org/10.5281/zenodo.22727388).

[The publication receipt](publication-receipt.json) records a fresh unauthenticated download
matching all 498,500 published PDF bytes and verifies metadata, author, ORCID, license and both DOIs.
Version 0.01 remains byte-identical in [the archive](versions/v0.01/); future corrections require
a new version and receipt. The manuscript is CC BY 4.0 and research code is MIT.

Build from this directory using two passes of `pdflatex -interaction=nonstopmode
-halt-on-error main.tex`, then render every page with `pdftoppm -png` and inspect it.
The publication gate is tied to the reviewed PDF bytes, not merely a successful compilation.
