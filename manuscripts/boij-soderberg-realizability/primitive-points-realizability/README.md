# Primitive Betti points over k[x,y,z] and the Heisenberg enveloping algebra: the point (1,2,2,1) on (0,e,3e,4e) fails only in characteristic 2 for 2 <= e <= 10, is realized whenever an odd prime p divides e(e-1), and a census for d_3 <= 12

Current public version: v0.02, published 2026-11-20 at
[10.5281/zenodo.24388904](https://doi.org/10.5281/zenodo.24388904), under concept DOI
[10.5281/zenodo.24385386](https://doi.org/10.5281/zenodo.24385386); 66 pages, 921,730 bytes, SHA-256
`2ea9a3fab443b83b1edff39bff56e864f9a5c9fee244289b9e0e790f868a1f69`. The committed `main.pdf` is that published version.
The source in this folder is v0.03, not released: it states the results obtained after v0.02 (listed below). The paper is
a preprint of the CAOS Research open-problems programme, problem `boij-soderberg-realizability`, written to the manuscript
content bar (the source measures 48,755 words, 44 display equations, 11 figures, 57 tables, 39 references and 10 algorithms by
`tools/zenodo/check_manuscript_depth.py`; v0.02 had 22,449 words, 22 display equations, 9 figures, 29 tables, 27 references
and 7 algorithms). Version 0.01 was published on 2026-11-20 at
[10.5281/zenodo.24385387](https://doi.org/10.5281/zenodo.24385387); v0.02 added the results on odd characteristic and on
the family of pure pairs, the archived machine checks of the characteristic 2 theorem, and corrected the manifest table of
v0.01 (it printed the size and hash of a copy of one file with CRLF line ends).

The code, the computational records and the artifacts that the paper cites are on the branch `develop` of
[CAOS_RESEARCH](https://github.com/fsantibanezleal/CAOS_RESEARCH), in
[`problems/commutative-algebra/boij-soderberg-realizability/`](https://github.com/fsantibanezleal/CAOS_RESEARCH/tree/develop/problems/commutative-algebra/boij-soderberg-realizability).

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
- Odd characteristic below `2e`: explicit pure pairs of forms over `F_3`, `F_5` (`e = 3`), `F_3`, `F_5`, `F_7` (`e = 4` and `e = 5`) and `F_3` (`e = 6`), so that for `2 <= e <= 5` the point `(1,2,2,1)` of `(0, e, 3e, 4e)` is realized over `U` exactly when the characteristic is not 2 (EXP-006, EXP-008).
- Theorem D: the pure pairs of forms of degree `e` are open in a determinantal locus and every component of the pure locus has dimension at least `4e - 4`; the published modules form a subfamily of dimension 2. The tangent space of the locus at `<x^e, y^e>` has dimension exactly `4e - 4` over the rationals for `e = 4, ..., 7`; explicit pure pairs over the rationals lie outside the orbit; a four-parameter linear family is proved to lie in the locus, with a pure general member, for every `e >= 4` in characteristic 0 or at least `2e` (EXP-007).
- The machine checks of the characteristic 2 theorem and of the family at `e = 6, 7`, archived (EXP-005).

The v0.03 source adds (each with its evidence mark and its limits):

- Theorem M (criterion): in characteristic `p >= 3`, for `f = A + b1 x + b2 y` and `g = B + d1 x + d2 y` with `A, B` of degree `e` and the `b`, `d` of degree `e - 1` in the centre `k[x^p, y^p, z]`, the commutator `gf - fg = -Dz` is central, and the pair is pure, with an explicit resolution, if and only if `U/(Uf + Ug)` has finite length, if and only if `zD`, `n(f)`, `n(g)` have no common zero other than the origin. Explicit pure pairs (cases A to D) exist for every `e >= 3` with `e = 0` or `1` modulo `p`, so `(1,2,2,1)` on `(0, e, 3e, 4e)` is realized whenever an odd prime `p` divides `e(e - 1)`. Theorem N: the elementary proof for an odd multiple of `p`, with arbitrary central forms. Machine checks: EXP-011 (16 central pairs up to `e = 15`, 5 pairs outside the hypotheses) and EXP-012 (11 explicit pairs up to `e = 13`, 1,600 random pairs of the class where the criterion and the pure Hilbert function agree, 3 pairs built to violate the criterion).
- Theorems O and P: the explicit sequence of a pair is a complex exactly when the commutator commutes with the pair; those pairs are the images of `(x, y)` under graded endomorphisms of `U`; a nonzero such commutator is central (Theorem O, central or nothing); pure pairs of this kind exist only in characteristic `p` dividing `e(e - 1)`, never in characteristic 0 for `e >= 2`; pulling back along such an endomorphism of degree `d` multiplies every degree of every Betti table by `d` (Theorem P, scaling), so the set of `e` with `(1,2,2,1)` realized in characteristic `p` is closed under multiplication by `d >= 3` with `d = 0` or `1` modulo `p` (new pairs `(8,3)`, `(12,5)`, `(14,3)`, `(16,7)`). Proved on paper; ten pull-backs are checked by machine (EXP-013).
- The class weight and the strata `S(m; i, j)`: a necessary condition for pure pairs homogeneous for the weight classes modulo `m`, the admissible and refined admissible strata for `e = 4, ..., 10` computed by the generator from the definition, and the exclusion of the part of `S(e - 1; 0, 1)` outside the linear family.
- The linear family below `2e` (EXP-009): pure members over `F_p` at `(e, p) = (4,5), (4,7), (5,7), (6,11), (7,11), (7,13)`, none for `p <= e` in the eight pairs computed and none at `(6,7)`; no member of rank above `r` in any of the fifteen pairs below `2e`.
- The state of the point for every `e` and every odd `p < 2e` (the table of the state for `e <= 10`, the two tables of the sources for `e <= 14`, the grid for `e <= 16`): for `2 <= e <= 10` the point is realized over `U` if and only if the characteristic is not 2; `e = 12` is complete too; the open pairs are `(11,3)`, `(13,7)`, `(13,11)`, `(14,5)`, `(14,11)` and the pairs with `e >= 15` that no result reaches.
- Proposition on the characteristic dividing the modulus: in odd characteristic `p <= e` no pair homogeneous for the class weight modulo `p` is pure, so no stratum with `p` dividing `m` holds a pure pair (the pairs of EXP-010 have no member of rank `r` there).
- Pairs over the invariants: for `f = x^e + b y^e` and `g` a form in `xy` and `z` the module decomposes over `k[xy, z]` into `2e` cyclic modules, the Hilbert function does not depend on `b`, and under the hypothesis (C) the conditions for the pure Hilbert function are those of Theorem E (`(m - 1)^2` conditions on `g` with `m = e/2`, not independent); the quintic at `e = 4` and pure pairs over the rationals.
- Theorems F, G and H on the pairs over the invariants: under (C) the pure Hilbert function holds if and only if one congruence modulo `G` holds (Theorem F), and then the Betti table is pure (Theorem G); existence of forms with (C) and the congruence over a finite field of characteristic `p = 2e - 1` or `p > 2e` (not necessarily the prime field) and in characteristic 0 (Theorem H); nothing for the primes between `e` and `2e - 1`. Independent checks are hand computations, not archived.
- Projection on the weight-zero summand: strata with a gap in the weights, and the stratum of the linear family when `p <= 2e - 5`, hold no pure pair (theorem); rule of the linear family, pure members exactly when `2e - p <= 3` in the computed pairs (EXP-015); filter in the stratum of the central pairs (not proved) with pure pairs at `(9,11)`, `(9,13)`, `(11,7)`, `(13,5)` (EXP-017); lists of forms by one congruence (EXP-016) with pure pairs at eleven pairs not settled when the lists were fixed, among them `(12,7)`, `(12,13)`, `(16,13)`, and empty lists at `(14,5)`, `(14,11)`; stratum with the largest exponent allowed by the projection (`2t <= p - 1`, EXP-018): pure pairs at `(11,13)`, `(11,17)`, `(13,17)`, `(13,19)`, `(14,23)`, none with the pure Hilbert function in the strata with `t + 2`.
- Searches in the strata (EXP-010, EXP-014): pure pairs over `F_p` at `(6,5)`, `(6,7)`, `(7,3)`, `(7,5)`, `(7,7)`, at `e = 8` for `p = 3, 5, 7, 11, 13`, at `e = 10` for `p = 3, 7, 11, 13`, at `(12,5)`, `(9,7)`, `(9,17)`; no pure Hilbert function in a stratum that is not admissible; the failed expectations at `(8,3)`, `(12,7)`, `(9,11)`, `(9,13)` and the amendment of one control are reported as the computations record them.
- Pull-backs (EXP-013): ten cases, the Betti table of the pull-back is the table with every degree multiplied by `d` in two instruments; pure pairs of degrees 8, 12, 16, 24.

The paper credits the negative answer, the obstructions over `k[x,y,z]` and the Kostant modules to their authors and
claims no priority; its literature searches are stated in the related work section.

## Files

| File | What it is |
|---|---|
| `main.tex` | the paper (inline bibliography of 39 works); reads `numbers.tex`, the `tab_*.tex` and the `fig_*.tex` |
| `make_tables.py` | reads the archived artifacts of EXP-001 to EXP-018, recomputes the finite statements of the proofs, the Hilbert functions, ranks, commutators and orbit dimensions of the printed pairs, the admissible strata and the cells of the grid of pairs in exact arithmetic, stops with exit 1 when a value the text relies on differs, and writes `numbers.tex`, the tables and the figures (69 files); hashes of text artifacts are taken on LF-normalized bytes |
| `numbers.tex` | every number of the text, as macros |
| `tab_*.tex` | the tabular bodies of the tables (captions are in `main.tex`); the sources of the state are in `tab_statesrc.tex` (`e <= 10`) and `tab_statesrcb.tex` (`11 <= e <= 14`) |
| `fig_*.tex` | the TikZ and pgfplots bodies of the figures, generated from the artifacts or, for the two diagrams, typed in `make_tables.py` |
| `zenodo.json` | the deposit metadata of v0.03 for the release tool (title, creator, description, version notes, keywords, related identifiers, references); the references equal the bibliography of `main.tex` in the same order, and the related identifiers cite the works of the bibliography that print a DOI or an arXiv number |
| `main.pdf` | the published PDF of v0.02 (the SHA-256 above); it is replaced at the release of v0.03 |
| `build-report.json`, `render-report.json`, `publication-gate.json` | the measured build, the page renders that were read, and the approval record of the release of v0.02; they are replaced at the release of v0.03 |

`main.pdf` is the published file; a rebuild is compared with it through the reports above.

## Regenerate and build

From the repository root, with the repository virtual environment:

```
python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py          # writes the outputs
python manuscripts/boij-soderberg-realizability/primitive-points-realizability/make_tables.py --check  # exit 1 if stale
```

Then three passes of `pdflatex main.tex` in this folder (packages: amsmath, amsthm, booktabs, hyperref, orcidlink, newfloat,
algpseudocode, tikz, pgfplots with the `groupplots` library; the algorithm float is declared with `newfloat`). No external
image is used. The script also reads the rank certificates of EXP-004 (lift to characteristic 0) and its second-system file, the results files of EXP-005 to EXP-018 and the record `stored-members-filter.json` of EXP-017.

The generator is tested by `tests/test_bs_manuscript_tables.py` (from the repository root: `python -m pytest tests/test_bs_manuscript_tables.py -q`): the printed bytes and SHA-256 of the manifest table equal those of the committed blobs, `make_tables.py --check` reports the outputs current, the guards on the artifacts of EXP-005 to EXP-018 refuse mutated copies, the admissible and refined admissible strata equal the counts of the independent computation, and the rule of the grid of pairs gives the hand-checked cells, with and without the searches in the strata.
