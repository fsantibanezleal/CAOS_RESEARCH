# manuscript-cascade/ - the consequences paper (C of three)

`main.tex` / `main.pdf`: "Consequences of the Three-Dimensional Jacobian Counterexample for Seven Neighbouring
Conjectures: Implications with Their Indices and Exactly Checked Witnesses". Current version: v0.11, published 2026-11-19 at [10.5281/zenodo.24382142](https://doi.org/10.5281/zenodo.24382142) (concept
[10.5281/zenodo.21503371](https://doi.org/10.5281/zenodo.21503371)); 45 pages, 716,901 bytes, SHA-256
`23c0d679be77d22e21a01bf1f2ce75e4ec59668168ce16e9123c348e99aa754d`. v0.11 states the Mathieu row after C. D. Long's direct
construction (arXiv:2609.16178 v1): the conjecture fails on SU(N) for every N >= 2, with the first-column argument
written out as three lemmas, a proposition and a corollary and reproduced exactly by computation EXP-148 (950 cells,
2 <= N <= 16, four routes); the homogeneous route for N >= 15 stays as a second route; Long's statement for every
nonabelian compact connected Lie group is cited, not reproduced. Reviewed adversarially with an independent
re-derivation of the proofs, one fix pass and a re-check. Version 0.10, published 2026-11-16 at
[10.5281/zenodo.24269044](https://doi.org/10.5281/zenodo.24269044) (35 pages, 616,102 bytes, SHA-256
`2df59a7f76061b3def880dddec6dc820afb7b493e46df90d3b537ce661586416`), added the page of each located primary statement,
corrected four citations and stated de Bondt's dimension results with their definitions and evidence marks. Version
0.09, published 2026-11-15 at [10.5281/zenodo.24239949](https://doi.org/10.5281/zenodo.24239949) (32 pages, 590,456
bytes, SHA-256 `abae32480123a9eef3b2d29ad4d1bcce2394766b1ce962583886a9c7531728e5`).

What the paper contains:

- A status table of the Jacobian conjecture and seven neighbouring conjectures (Mathieu, Dixmier, Poisson, Gaussian
  moments, vanishing, Image, Hessian and symmetric forms): the implication with its dimension index, the source theorem
  located, an evidence mark per ingredient ([MV], [D], [C], [V], [U]), the explicit witness with its dimension and the
  open indices. An implication graph and an index map are built from the same data.
- Six exact procedures in pseudocode, each with inputs, arithmetic domain, software and measured cost: the fibre by a
  lexicographic Groebner basis (EXP-001, EXP-144), the homogeneous-type test (EXP-136), the symmetrization with collision
  transport (EXP-041), the de Bondt homogenization (EXP-138), the Poisson-endomorphism check of Long's map (EXP-144) and
  the exact Haar moments of Long's pair of polynomials on SU(N) by four routes (EXP-148), with propositions proving the
  soundness of every reduction and, for SU(N), the moment identities of Long's pair (lemmas on the first column, the
  spherical laws and the constant-term identity on S^3, a proposition and a corollary).
- The explicit witnesses: Long's pair of polynomials on C^2 (Mathieu conjecture false for SU(N), every N >= 2), the
  dimension-15 homogeneous map (a second route, N >= 15), the dimension-48 gradient map with a Hessian-nilpotent quartic
  potential of 382 monomials (vanishing, Hessian and symmetric forms), and Long's rank-two Poisson map (Poisson
  conjecture false for n >= 2, index 1 open).
- A Validation section (every independent route with its numbers), an Ablation section (the negative controls), a
  Related work section of 45 cited works, and the SHA-256 of every primary text read.

Open in the paper: the two-variable Jacobian conjecture, Dixmier at ranks 1 and 2, Poisson at index 1. The Mathieu row
has no open index for SU(N), N >= 2. Mathieu's 1997 paper was not located; the direction and index of his implication
rest on Zwart's review, and the status of the row no longer depends on it.

Files:

- `make_status.py` reads the artifacts of computations EXP-001, EXP-041, EXP-136, EXP-138, EXP-144 and EXP-148 and writes
  `numbers.tex`, `status_table.tex`, `implication_graph.tex`, `index_map.tex`, `hash_table.tex`, `validation_table.tex`,
  `cost_table.tex`, `mathieu_table.tex` and the five `fig_*.tex` figures. It stops with exit 1 if a number differs from the one the text
  relies on; `python make_status.py --check` reports stale outputs. Run it from this folder (`--exp` names another
  experiments folder).
- `main.tex` includes the generated files. Build: `pdflatex` three times, after deleting `main.aux` and `main.out`.
- `zenodo.json`: deposit metadata (title, description matching the abstract, version notes).

Checks: `python scripts/check_manuscript_voice.py manuscripts/jacobian-conjecture/cascade` (repository root) and the
CAOS_MANAGE depth checker in research mode. See `manuscript/README.md` for the three-paper structure.
