# Cyclically 4-edge-connected cubic graphs of unbounded Petersen defect

Current public version: v0.03, published 2026-11-15 at
[10.5281/zenodo.24239832](https://doi.org/10.5281/zenodo.24239832), under concept DOI
[10.5281/zenodo.22847192](https://doi.org/10.5281/zenodo.22847192). The 805,518-byte committed PDF has SHA-256
`0eedaae3e928469738e585a97bf76e545ec07c3209fa67b6e5527febefa54417` (35 pages). v0.02 (2026-10-06):
[10.5281/zenodo.23196817](https://doi.org/10.5281/zenodo.23196817).

Focused paper for EXP-012 (with the distance sets of EXP-010): the conduction lemma for 4-poles, alternating rings of two 4-poles cut from the first 52-vertex counterexample, and the theorem that cyclically 4-edge-connected cubic graphs of girth 5 on 102t vertices have Petersen defect at least t, so statement (e) of the Mattiolo-Mazzuoccolo-Mkrtchyan conjecture is false and the conjectured equivalence holds.

v0.02 adds Proposition 5.3 (`pd(R_3) = 3`, EXP-012 addendum 4) and Section 6 (EXP-013, EXP-014): the 64 classes modulo the cut space, the core `{0, E, D2}` of the 6-poles of the Petersen graph, J5, J7 and the dodecahedron, transfer relations and their semigroups, every ring of claws and Petersen superedges is Petersen colorable, the junctions of flower snarks, cyclically 5-edge-connected snarks of girth 5 among the superedge rings, and the control on `G52`.

Versions: v0.01 [10.5281/zenodo.22847193](https://doi.org/10.5281/zenodo.22847193) (2026-09-19, first version); v0.02 (2026-10-06).

Build: three-pass `pdflatex main.tex` in this folder. Version history and publication receipts:
`_CAOS_MANAGE/manuscripts/petersen-coloring/unbounded-defect/metadata.md` (private vault).

Source of v0.03 (not yet released): `make_tables.py` regenerates `numbers.tex`, `table-*.tex` and `fig-*.tex` from the experiment artifacts (`python make_tables.py`); `main.tex` inputs them together with `related.tex`, `theory6.tex`, `methods.tex`, `design.tex`, `results6.tex`, `ablation.tex` and `closing.tex`. `zenodo.json` holds the v0.03 deposit metadata. The PDF in this folder is still v0.02; the release builds the new one.
