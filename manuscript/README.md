# manuscript/ - the FOUNDATIONAL paper (A of three)

`main.tex` / `main.pdf`: "The Jacobian Conjecture after the Three-Dimensional
Counterexample". The stable, near-final record of the three-dimensional aftermath:
exact validation, the structure of the counterexample, the seed family and its degree laws,
the asymptotic variety and real census, characteristic p, the weighted-landscape uniqueness,
and two-dimensional equivariant rigidity as the bridge out.

Split decision (2026-07-22, session 23): the record is THREE manuscripts so each audience
reads a self-contained document while the repository history log stays the single
chronological record.

- A (this folder): the foundational 3D paper: stable; grows only on 3D-side findings.
- B `manuscript-planar/`: the active planar program (the JC(2) machine, the unconditional
  Newton-polygon exclusion theorems, the staircase transport, the recalibrated frontier);
  grows per session.
- C `manuscript-cascade/`: the consequence cascade + the explicit dimension-48 witness.

Nothing was deleted in the split: the planar sections moved to B with their EXP labels
intact; both papers cite each other.

Build (MiKTeX or any TeX distribution):

```powershell
pdflatex -interaction=nonstopmode main.tex; pdflatex -interaction=nonstopmode main.tex
```

Rules (methodology/05): findings enter only after adversarial validation; every claim is
labeled [MV] machine-verified, [D] derived (instance-certified), or [C] conjecture.
