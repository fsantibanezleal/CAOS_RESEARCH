# manuscript-cascade/ - the consequences paper (C of three)

`main.tex` / `main.pdf`: "Consequences of the Three-Dimensional Jacobian Counterexample for Seven Neighbouring
Conjectures: Located Implications and Exactly Checked Witnesses". Version 0.09 (2026-11-14).

What the paper contains:

- A status table of the Jacobian conjecture and seven neighbouring conjectures (Mathieu, Dixmier, Poisson, Gaussian
  moments, vanishing, Image, Hessian and symmetric forms): the implication with its dimension index, the source theorem
  located, an evidence mark per ingredient ([MV], [D], [C], [V], [U]), the explicit witness with its dimension and the
  open indices. An implication graph and an index map are built from the same data.
- Five exact procedures in pseudocode, each with inputs, arithmetic domain, software and measured cost: the fibre by a
  lexicographic Groebner basis (EXP-001, EXP-144), the homogeneous-type test (EXP-136), the symmetrization with collision
  transport (EXP-041), the de Bondt homogenization (EXP-138) and the Poisson-endomorphism check of Long's map (EXP-144),
  with a proposition proving the soundness of every reduction.
- The explicit witnesses: the dimension-15 homogeneous map (Mathieu conjecture false for SU(N), N >= 15), the
  dimension-48 gradient map with a Hessian-nilpotent quartic potential of 382 monomials (vanishing, Hessian and symmetric
  forms), and Long's rank-two Poisson map (Poisson conjecture false for n >= 2, index 1 open).
- A Validation section (every independent route with its numbers), an Ablation section (the negative controls), a
  Related work section of 43 cited works, and the SHA-256 of every primary text read.

Open in the paper: the two-variable Jacobian conjecture, Dixmier at ranks 1 and 2, Poisson at index 1, Mathieu for
SU(N) with 3 <= N <= 14. Mathieu's 1997 paper was not located; that row rests on Zwart's review.

Files:

- `make_status.py` reads the artifacts of computations EXP-001, EXP-041, EXP-136, EXP-138 and EXP-144 and writes
  `numbers.tex`, `status_table.tex`, `implication_graph.tex`, `index_map.tex`, `hash_table.tex`, `validation_table.tex`,
  `cost_table.tex` and the four `fig_*.tex` figures. It stops with exit 1 if a number differs from the one the text
  relies on; `python make_status.py --check` reports stale outputs. Run it from this folder (`--exp` names another
  experiments folder).
- `main.tex` includes the generated files. Build: `pdflatex` three times, after deleting `main.aux` and `main.out`.
- `zenodo.json`: deposit metadata (title, description matching the abstract, version notes).

Checks: `python scripts/check_manuscript_voice.py manuscripts/jacobian-conjecture/cascade` (repository root) and the
CAOS_MANAGE depth checker in research mode. See `manuscript/README.md` for the three-paper structure.
