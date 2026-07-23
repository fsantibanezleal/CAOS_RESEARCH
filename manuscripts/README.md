# manuscripts/ - the global manuscript tree

One subfolder per problem; inside it, one folder per manuscript. Each manuscript
folder holds `main.tex` and its built `main.pdf` (committed per release; two-pass
pdflatex). Relocated from three root-level folders on 2026-07-23; git history is
preserved through the rename.

| Problem | Manuscript | DOI (published on Zenodo, 2026-07-23) | What it records |
|---|---|---|---|
| [jacobian-conjecture](jacobian-conjecture/) | [foundational/](jacobian-conjecture/foundational/) | [10.5281/zenodo.21503366](https://doi.org/10.5281/zenodo.21503366) | Paper A: the counterexample validation, structure, family, escape geometry, char-p certificates, the 3D aftermath. |
| [jacobian-conjecture](jacobian-conjecture/) | [planar/](jacobian-conjecture/planar/) | [10.5281/zenodo.21503368](https://doi.org/10.5281/zenodo.21503368) | Paper B: the planar program: the theorem ladder, staircase transport, GGHV frontier and the (72,108) campaign. |
| [jacobian-conjecture](jacobian-conjecture/) | [cascade/](jacobian-conjecture/cascade/) | [10.5281/zenodo.21503372](https://doi.org/10.5281/zenodo.21503372) | Paper C: the consequence cascade, including the dimension-48 Hessian witness. |

The web app links each problem's manuscripts directly from its problem page.

Concept DOIs (always resolve to the latest version): A 10.5281/zenodo.21503365 ·
B 10.5281/zenodo.21503367 · C 10.5281/zenodo.21503371. Versions are frozen once
published; updates go through "New version" on the same record.
