# The Two 52-Vertex Counterexamples to the Petersen Coloring Conjecture Are Colorable Only by Themselves If No Counterexample Has at Most 38 Vertices

Public version on record: v0.02, published 2026-11-14 at [10.5281/zenodo.24230853](https://doi.org/10.5281/zenodo.24230853), under concept DOI
[10.5281/zenodo.22859074](https://doi.org/10.5281/zenodo.22859074). v0.01 (2026-10-06,
[10.5281/zenodo.22859075](https://doi.org/10.5281/zenodo.22859075)) carried the title "Which Counterexamples to the Petersen Coloring Conjecture Are Colorable Only by Themselves?" and stated the membership without its condition.

Focused paper for EXP-007: fiber-parity and unused-vertex lemmas for H-colorings with an unknown target, the propositional encoding in full (variables, clauses, sizes, symmetry breaking with a soundness proof, the attach clauses and the proof that they are implied), the certification pipeline with its parameters and commands, certified refutations of every even target order from 40 to 50 for both 52-vertex counterexamples, which with Observation 10 of arXiv:2608.10028v4 places both in H_3, and the tables of undecided orders, controls, ablation and SHA-256 hashes.

Parts, assembled into `main.tex` by `assemble.py`: `skeleton.tex`, `abstract.tex`, `body-sections-1-3.tex` (introduction, related work, problem formulation), `body-sections-4-6.tex` (fibers, method, theory), `body-sections-7-13.tex` (design, results, ablation, discussion, limitations, reproducibility, conclusions, appendix, bibliography), `results-theorem.tex`, `fig-fibers.tex`, and the parts written by `make_tables.py` from the EXP-007 result files (`results-table.tex`, `table-*.tex`, `fig-*.tex`). `python make_tables.py --check-hashes` rebuilds every certified formula with the encoder and compares its SHA-256 with the result files; `--facts` prints the numbers quoted in the prose.

Build: `python make_tables.py`, `python assemble.py`, then two or three passes of `pdflatex main.tex` in this folder. `zenodo.json` is the metadata of v0.02 as published. The committed PDF is 696126 bytes, SHA-256 `4a0cab3e962f5f338899873b8387aa17c6afbac7d7c727a7274b21d6e3039563`.
Version history and publication receipts: `_CAOS_MANAGE/manuscripts/petersen-coloring/colorable-only-by-itself/metadata.md` (private vault).
