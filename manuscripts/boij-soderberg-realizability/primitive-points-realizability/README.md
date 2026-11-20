# Primitive Betti points over k[x,y,z] and the Heisenberg enveloping algebra: the point (1,2,2,1) on (0,e,3e,4e) fails only in characteristic 2 for 2 <= e <= 5, the pure pairs of forms form a family, and a census for d_3 <= 12

Current public version: v0.02, published 2026-11-20 at
[10.5281/zenodo.24388904](https://doi.org/10.5281/zenodo.24388904), under concept DOI
[10.5281/zenodo.24385386](https://doi.org/10.5281/zenodo.24385386); 66 pages, 921,730 bytes, SHA-256
`2ea9a3fab443b83b1edff39bff56e864f9a5c9fee244289b9e0e790f868a1f69`. The committed `main.pdf` is that published version. The paper is a preprint of the CAOS Research
open-problems programme, problem `boij-soderberg-realizability`, written to the manuscript content bar (22,449 words,
22 display equations, 9 figures, 29 tables, 27 references, 7 algorithms). Before release it was read by a reader other
than the writer (the new proofs compared with their reviewed notes, 154 generated numbers checked against the
artifacts, the printed pairs rebuilt from their text, the three experiment verdicts read against their results), with
a fix pass, a closing check and a final confirmation. Version 0.01 was published on 2026-11-20 at
[10.5281/zenodo.24385387](https://doi.org/10.5281/zenodo.24385387); v0.02 adds the results on odd characteristic and on the family of pure pairs, the
archived machine checks of the characteristic 2 theorem, and corrects the manifest table of v0.01 (it printed the size
and hash of a copy of one file with CRLF line ends).

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

In the v0.02 source the paper also states (each with its evidence mark and its limits):

- Odd characteristic below `2e`: explicit pure pairs of forms over `F_3`, `F_5` (`e = 3`), `F_3`, `F_5`, `F_7` (`e = 4` and `e = 5`) and `F_3` (`e = 6`), so that for `2 <= e <= 5` the point `(1,2,2,1)` of `(0, e, 3e, 4e)` is realized over `U` exactly when the characteristic is not 2, and at `e = 6` it is realized in characteristic 3; `e = 6` at `p = 5, 7, 11` and `e >= 7` below `2e` are open (EXP-006, EXP-008).
- Theorem D: the pure pairs of forms of degree `e` are open in a determinantal locus and every component of the pure locus has dimension at least `4e - 4`; the published modules form a subfamily of dimension 2. The tangent space of the locus at `<x^e, y^e>` has dimension exactly `4e - 4` over the rationals for `e = 4, ..., 7`; explicit pure pairs over the rationals lie outside the orbit; a four-parameter linear family is proved to lie in the locus, with a pure general member, for every `e >= 4` in characteristic 0 or at least `2e` (EXP-007).
- The machine checks of the characteristic 2 theorem and of the family at `e = 6, 7`, archived (EXP-005).

The paper credits the negative answer, the obstructions over `k[x,y,z]` and the Kostant modules to their authors and
claims no priority; its literature searches are stated in the related work section.

## Files

| File | What it is |
|---|---|
| `main.tex` | the paper (inline bibliography of 27 works); reads `numbers.tex`, the `tab_*.tex` and the `fig_*.tex` |
| `make_tables.py` | reads the archived artifacts of EXP-001 to EXP-008, recomputes the finite statements of the proofs and the Hilbert functions, ranks and orbit dimensions of the printed pairs in exact arithmetic, stops with exit 1 when a value the text relies on differs, and writes `numbers.tex`, the tables and the figures; hashes of text artifacts are taken on LF-normalized bytes |
| `numbers.tex` | every number of the text, as macros |
| `tab_*.tex` | the tabular bodies of the tables (captions are in `main.tex`) |
| `fig_*.tex` | the TikZ and pgfplots bodies of the figures, generated from the artifacts or, for the two diagrams, typed in `make_tables.py` |
| `zenodo.json` | the deposit metadata of v0.02 for the release tool (title, creator, description, keywords, related identifiers, references); the same file is kept in the programme's deposit records |
| `main.pdf` | the published PDF of v0.01 (the SHA-256 above); it is replaced at the release of v0.02 |
| `build-report.json`, `render-report.json`, `publication-gate.json` | the measured build (three passes, no warning, no overfull or underfull box), the page renders that were read, and the approval record of the release |

`main.pdf` is the published file; a rebuild is compared with it through the reports above.

## Regenerate and build

From the repository root, with the repository virtual environment:

```
python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py          # writes the outputs
python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py --check  # exit 1 if stale
```

Then three passes of `pdflatex main.tex` in this folder (packages: amsmath, amsthm, booktabs, hyperref, orcidlink, newfloat,
algpseudocode, tikz, pgfplots with the `groupplots` library; the algorithm float is declared with `newfloat`). No external
image is used. The script also reads the rank certificates of EXP-004 (lift to characteristic 0) and its second-system file, and the results files of EXP-005 to EXP-008.

The generator is tested by `tests/test_bs_manuscript_tables.py` (from the repository root: `python -m pytest tests/test_bs_manuscript_tables.py -q`): the printed bytes and SHA-256 of the manifest table equal those of the committed blobs, `make_tables.py --check` reports the outputs current, and the guards on the artifacts of EXP-005 to EXP-008 refuse mutated copies.
