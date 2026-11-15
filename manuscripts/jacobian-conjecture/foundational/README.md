# manuscript/ - the FOUNDATIONAL paper (A of three)

`main.tex` / `main.pdf`: "The Three-Dimensional Counterexample to the Jacobian Conjecture: Exact
Validation, a Proved Seed-Family Constructor, the Discriminant Wall of Non-Properness, and Planar
Equivariant Rigidity". It covers the exact validation of the announced map and its full fiber, the
skew-product structure, the seed family with the proof of its Keller property and the degree law on
the verified seeds, the asymptotic variety and the image of the map, the real census, characteristic
p, the weight-system survey, and planar equivariant rigidity as the bridge out.

Version 0.15, published 2026-11-15 at [10.5281/zenodo.24240161](https://doi.org/10.5281/zenodo.24240161) (concept
[10.5281/zenodo.21503365](https://doi.org/10.5281/zenodo.21503365)); 30 pages, 670,311 bytes, SHA-256
`aa7de7e613b5c57dca56507786706bd493d459c21d1ff1f38cf85cfb547199bc`. It corrects v0.14: the announced map is not
surjective and the plane C = 0 is not asymptotic (EXP-145).

The record is THREE manuscripts so each audience reads a self-contained document:

- A (this folder): the foundational 3D paper.
- B `../planar/`: the planar program (the JC(2) machine, the Newton-polygon exclusion theorems, the
  staircase transport, the recalibrated frontier).
- C `../cascade/`: the consequence cascade and the explicit dimension-48 witness.

Generated files (do not edit by hand): `numbers.tex`, `tab-*.tex`, `fig-*.tex`. They are written by

```powershell
python gen_tables.py          # rewrite from the stored experiment outputs
python gen_tables.py --check  # exit 1 when a generated file is out of date
```

from the outputs of EXP-001, EXP-004, EXP-006 to EXP-012 and EXP-145 under
`problems/algebraic-geometry/jacobian-conjecture/experiments/`.

Build (MiKTeX or any TeX distribution; three passes, delete `main.aux` and `main.out` first):

```powershell
pdflatex -interaction=nonstopmode main.tex; pdflatex -interaction=nonstopmode main.tex; pdflatex -interaction=nonstopmode main.tex
```

Rules (methodology/05 and 09): every result is labeled [MV] machine-verified, [D] derived, or [C]
conjecture; statements about the literature carry [V] (read in the primary text) or [U] (not
confirmed in a primary source). Gate: `python scripts/check_manuscript_voice.py manuscripts/jacobian-conjecture/foundational`.
