# manuscripts/ - the global manuscript tree

One subfolder per problem; inside it, one folder per manuscript. Each manuscript
folder holds `main.tex` and its built `main.pdf` (committed per release; two-pass
pdflatex). Relocated from three root-level folders on 2026-07-23; git history is
preserved through the rename.

| Problem | Manuscript | What it records |
|---|---|---|
| [jacobian-conjecture](jacobian-conjecture/) | [foundational/](jacobian-conjecture/foundational/) | Paper A: the counterexample validation, structure, family, escape geometry, char-p certificates, the 3D aftermath. |
| [jacobian-conjecture](jacobian-conjecture/) | [planar/](jacobian-conjecture/planar/) | Paper B: the planar program: the theorem ladder, staircase transport, GGHV frontier and the (72,108) campaign. |
| [jacobian-conjecture](jacobian-conjecture/) | [cascade/](jacobian-conjecture/cascade/) | Paper C: the consequence cascade, including the dimension-48 Hessian witness. |

The web app links each problem's manuscripts directly from its problem page.
