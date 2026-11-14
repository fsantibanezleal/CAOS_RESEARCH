# Exact invariants of the known counterexamples to the Petersen coloring conjecture: covers, flows, defect two and unbounded abnormal edges

Current public version: v0.06, published 2026-10-06 at
[10.5281/zenodo.23195171](https://doi.org/10.5281/zenodo.23195171), under concept DOI
[10.5281/zenodo.22285164](https://doi.org/10.5281/zenodo.22285164). The 408,503-byte committed PDF has SHA-256
`b1790f612337f4ff104d6c6ed0414b8ca8bf7466a5bcb3360351d8468e78b2f6`. (The v0.06 title was "Berge-Fulkerson covers, cycle double covers, flows and exact normality defects of the first counterexamples to the Petersen coloring conjecture".)

Consequence audit of the five retrievable counterexamples (EXP-001 to EXP-006, EXP-008 to EXP-011): certification, perfect matching covers and index 4, 5-cycle double covers, flows, oddness and resistance, normal chromatic index 6, the parity theorem and pair criticality, abnormal edges with statements (c) and (d) of the Mattiolo-Mazzuoccolo-Mkrtchyan conjecture, and Theorem 5.9 (statement (e) is a two-defect statement).

The source in this folder is the v0.07 revision (pending release; the release sets the version DOI and the committed PDF): encodings with an algorithm, variable and clause counts, solver settings and commands for every invariant; consolidated tables of the invariants, pair sweeps (with the cut-space classes of the 17,362 witnesses), rings and frames, and 4-poles; validation (controls, corrupted witnesses, ablation of the symmetry units, independent routes); related work, discussion, limitations, conclusions; six figures; the claim marks [MV], [D], [C]; a proof of the 3-connectivity of frames; the rings renamed C_t; updated citations.

Contents:

- `main.tex`: the paper (inputs `tables/*.tex`).
- `make_tables.py`: reads the archived manifests and witnesses of `problems/combinatorics/petersen-coloring/experiments/` and writes every table and data-driven figure to `tables/`; `--check` also builds all the formulas with the repository encoders and asserts the printed encoding formulas and the archived sizes. Run it before building.
- `tables/`: the generated files (committed so that the paper builds without the artifacts).
- `zenodo.json`: deposit metadata of the revision.

Build: `python make_tables.py`, then three-pass `pdflatex main.tex` in this folder. Version history and publication receipts:
`_CAOS_MANAGE/manuscripts/petersen-coloring/consequence-audit/metadata.md` (private vault).
