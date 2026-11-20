# Independent exact verification of the counterexample to Goemans' unsplittable-flow cost conjecture and of the record lower-bound instances, with certified planarity and optimal pricing

Current public version: v0.03, published 2026-09-18 at
[10.5281/zenodo.22835200](https://doi.org/10.5281/zenodo.22835200), under concept DOI
[10.5281/zenodo.21554258](https://doi.org/10.5281/zenodo.21554258). The committed `main.pdf` is that published version.

## What the source in this folder is

`main.tex` is the source of the next version (v0.04, not yet released: the version DOI macro holds the concept DOI as a
placeholder until the release tool reserves the DOI). It is a LaTeX preprint of the research programme, rewritten to the
manuscript content bar. It reports, from the archived computations EXP-001 to EXP-007 of
`problems/optimization-geometry/unsplittable-flow-cost/experiments/`:

- the exact verification of the seven-vertex counterexample announced in July 2026 (not ours), the violation 16/15 it
  forces, the consistency battery against every proved result, the class boundary and the conflict triangle;
- the separation linear program with its proof, the single-terminal theorem and the two-terminal necessary condition;
- the frontier value, the exact Bland-rule simplex and the cutting-plane evaluator, with the proofs that justify the level search;
- the independent re-check of the eleven record instances of S. Nikolenko and A. De la Fuente (values, planarity
  certificates, optimality of their prices), credited to their authors;
- the exact checks of Muffatti's symmetric three-terminal family and of Afrasyab's odd-cycle family on C5.

The paper claims no new bound and no priority: the lower bounds are Nikolenko's and De la Fuente's, 9/8 as the supremum of
the symmetric three-terminal template is Nikolenko's, the family that approaches it is Muffatti's.

## Files

- `main.tex`: the paper. It reads `numbers.tex`, the `tab_*.tex` tables and the `fig_*.tex` figures.
- `make_tables.py`: reads the experiment artifacts (EXP-001 to EXP-007), checks every value the text relies on (it stops with
  exit 1 on a mismatch), recomputes the seven-vertex routing table with `ufclib`, and writes `numbers.tex`, the tables and the
  figures. Run from the repository root with the repository `.venv`:
  `python manuscripts/unsplittable-flow-cost/counterexample-verification/make_tables.py` writes the outputs, and `--check`
  reports stale outputs (exit 1). `--data-root <dir>` (or the environment variable `CAOS_RESEARCH_DATA`) also re-hashes the
  archived PDFs of the Nikolenko series and the instance file.
- `zenodo.json`: the deposit metadata of v0.04, for the release tool (the vault copy is
  `manuscripts/unsplittable-flow-cost/counterexample-verification/zenodo.json` of CAOS_MANAGE).

## Build

`pdflatex main.tex` three times (packages: amsmath, booktabs, hyperref, orcidlink, algorithm, algpseudocode, tikz, pgfplots with
the `groupplots` library). The figures are TikZ and pgfplots fragments generated from the artifacts; no external image is used.
