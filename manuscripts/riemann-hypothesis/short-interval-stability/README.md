# A stability refinement for simple critical zeros in short intervals

Published version 0.01, 2026-09-12. Sole author: Felipe Santibanez-Leal,
ORCID [0000-0002-0150-3246](https://orcid.org/0000-0002-0150-3246).

This preprint derives a strict refinement of Wang's positive short-interval cosine curve,
using the attributed finite stability inequality and a quantitative kernel obstruction.
The certified example at theta=3/4 improves the simple-critical lower proportion from
0.4190750129754243337 to 0.4190768284253039967. It does not prove RH or claim a global record.
Automated adversarial review is distinguished from peer review and end-to-end formalization.

- [Paper PDF](main.pdf) and [LaTeX source](main.tex).
- [Experiment proof and certificate](../../../problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/).
- [Publication gate](publication-gate.json) records final content, PDF, rendered-page hashes and checks.
- Frozen version DOI: [10.5281/zenodo.22727389](https://doi.org/10.5281/zenodo.22727389).
- Latest-version concept DOI: [10.5281/zenodo.22727388](https://doi.org/10.5281/zenodo.22727388).

[The publication receipt](publication-receipt.json) records a fresh unauthenticated download
matching all 368,644 frozen PDF bytes and verifies metadata, author, ORCID, license and both DOIs.
Published bytes are never replaced; corrections require a new version and a new receipt.
The manuscript is CC BY 4.0 and research code is MIT.

Build from this directory using two passes of `pdflatex -interaction=nonstopmode
-halt-on-error main.tex`, then render every page with `pdftoppm -png` and inspect it.
The publication gate is tied to the reviewed PDF bytes, not merely a successful compilation.
