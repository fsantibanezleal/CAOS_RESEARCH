# Independent exact verification of the counterexample to Goemans' unsplittable-flow cost conjecture and of the 2026 lower-bound instances, with certified planarity and optimal pricing

Current public version: v0.04, published 2026-11-19 at
[10.5281/zenodo.24384160](https://doi.org/10.5281/zenodo.24384160), under concept DOI
[10.5281/zenodo.21554258](https://doi.org/10.5281/zenodo.21554258); 38 pages, 677,983 bytes, SHA-256
`e681d974abe714906a4c14ed41f20a0cba702e2de5efe0fd31e1feef070f88ec`. The committed `main.pdf` is that published version. It was reviewed by a reader other than the writer before release (proofs re-derived, 52 numbers checked against the
artifacts, the credits and dates checked on the archived sources), with two fix passes and a closing check. Version 0.03
was published on 2026-09-18 at [10.5281/zenodo.22835200](https://doi.org/10.5281/zenodo.22835200).

## What the source in this folder is

`main.tex` is the source of the published version v0.04. It is a LaTeX preprint of the research programme, rewritten to the
manuscript content bar. It reports, from the archived computations EXP-001 to EXP-007 of
`problems/optimization-geometry/unsplittable-flow-cost/experiments/`:

- the exact verification of the seven-vertex counterexample announced in July 2026 (not ours), the violation 16/15 it
  forces, the consistency battery against every proved result, the class boundary and the conflict triangle;
- the separation linear program with its proof, the single-terminal theorem and the two-terminal necessary condition;
- the frontier value, the exact Bland-rule simplex and the cutting-plane evaluator, with the proofs that justify the level search;
- the independent re-check of eleven instances of the 2026 lower-bound series (values, planarity certificates,
  optimality of their prices), among them the current general record of A. De la Fuente and the current planar record of
  S. Nikolenko; the instances and their values are credited to their authors;
- the exact checks of Muffatti's subfamily of the symmetric three-terminal template and of Afrasyab's odd-cycle family on C5.

The paper claims no new bound and no priority: the current lower bounds are De la Fuente's (general) and Nikolenko's
(planar); the value 9/8, both as a lower bound and as the supremum of the symmetric three-terminal family, is Muffatti's
(note of 24 July 2026) and, independently, Nikolenko's (Proposition 5.2 of his first preprint, 30 July 2026); the four-terminal
value (299 - 41 sqrt 41)/32 is Protti's (release of 23 July 2026) and Nikolenko's.

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

`pdflatex main.tex` three times (packages: amsmath, booktabs, hyperref, orcidlink, newfloat, algpseudocode, tikz, pgfplots with
the `groupplots` library; the algorithm float is declared with `newfloat`, because the `algorithm` package makes hyperref
write a second anchor for every table and figure). The figures are TikZ and pgfplots fragments generated from the artifacts; no external image is used.
