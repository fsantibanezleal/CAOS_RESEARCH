# EXP-063 triangle-to-isolated comparison

This experiment gives an exact finite labelled bridge between the uniform
triangle classes of EXP-062 and the persistent isolated component of
EXP-042. Read `hypothesis.md`, `proof.md`, and `verdict.md` in that order.

Canonical producer:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-063-triangle-isolated-comparison/run.py --p-min 8 --p-max 11 --budget-seconds 900 --memory-gib 12
```

Independent audit:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-063-triangle-isolated-comparison/audit.py --budget-seconds 900 --memory-gib 12
```

The result is finite. It identifies exact surviving target coordinates and
their mod-two quotient relation spaces; it is not an all-parameter comparison,
an integral classification of the projected carriers, or an upper bound for
the full cokernel.
