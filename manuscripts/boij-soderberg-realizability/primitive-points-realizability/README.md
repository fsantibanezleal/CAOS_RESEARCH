# Primitive Betti points over k[x,y,z] and the Heisenberg enveloping algebra: the pure modules U/U(x^e,y^e), characteristic 2, and a census for d_3 <= 12

Version v0.01, 19 November 2026, not yet published: the version DOI and the concept DOI in the header block of `main.tex`
are placeholders (`10.5281/zenodo.NNNNNNNN`) that the release tool sets when the version DOI is reserved. The paper is a
preprint of the CAOS Research open-problems programme, problem `boij-soderberg-realizability` (backlog item BSB-013,
focus BSR-F2), written to the manuscript content bar.

## What the manuscript is

A research paper in LaTeX on Question 6.1 of Erman and Sam (is every integral point on a pure ray of the Boij-Soderberg
cone in three variables the Betti table of a finite length module over `k[x,y,z]` or over the enveloping algebra `U` of
the Heisenberg Lie algebra?). The question has a published negative answer (Jiang, Li, Sun, Wang, Xiao and Yu,
arXiv:2605.25259, Theorem 3.7); the paper studies the points that pass the Hilbert series parity test over `U`. It proves
and reports, each result with an evidence mark ([MV] machine-verified, [D] proved in the paper, [V] read on the source,
[U] not confirmed, [C] conjectural):

- Theorem A: `U/U(x^e, y^e)` has the pure resolution of type `(0, e, 3e, 4e)` with Betti table `(1, 2, 2, 1)` if and only
  if the characteristic is 0 or at least `2e` (seven-step proof; exact checks for `e <= 8`).
- Theorems B and C: in characteristic 2 no module with `a` generators and at most `a + 1` relations of one degree
  `e >= 2` has finite length over `U`, so the same point is realized over neither ring for every `e >= 2`.
- The primitive points of the ten rays with `d3 <= 12` that pass the parity test and are excluded over `k[x,y,z]`,
  realized over `U` in characteristic 0 by explicit modules.
- The census over `k[x,y,z]` of the 220 rays with `d3 <= 12` (realized, excluded, open; least multiples), its field scope, and a lift proposition with rank certificates that carries every realized ray to characteristic 0.
- In characteristic 0 no counterexample to the question has `d3 <= 9`; two dual rays with `d3 = 10` are counterexamples
  over every field.

The paper credits the negative answer, the obstructions over `k[x,y,z]` and the Kostant modules to their authors and
claims no priority; its literature searches are stated in the related work section.

## Files

| File | What it is |
|---|---|
| `main.tex` | the paper (inline bibliography of 26 works); reads `numbers.tex`, the `tab_*.tex` and the `fig_*.tex` |
| `make_tables.py` | reads the archived artifacts of EXP-001 to EXP-003, recomputes the finite statements of the proofs in exact arithmetic, stops with exit 1 when a value the text relies on differs, and writes `numbers.tex`, the tables and the figures |
| `numbers.tex` | every number of the text, as macros |
| `tab_*.tex` | the tabular bodies of the tables (captions are in `main.tex`) |
| `fig_*.tex` | the TikZ and pgfplots bodies of the figures, generated from the artifacts or, for the two diagrams, typed in `make_tables.py` |
| `zenodo.json` | the deposit metadata of v0.01 for the release tool (title, creator, description, keywords, related identifiers, references) |

`main.pdf` is not committed here; the release tool builds it.

## Regenerate and build

From the repository root, with the repository virtual environment:

```
python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py          # writes the outputs
python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py --check  # exit 1 if stale
```

Then two passes of `pdflatex main.tex` in this folder (packages: amsmath, amsthm, booktabs, hyperref, orcidlink, newfloat,
algpseudocode, tikz, pgfplots with the `groupplots` library; the algorithm float is declared with `newfloat`). No external
image is used. The script also reads the rank certificates of EXP-004 (lift to characteristic 0) and its second-system file.
