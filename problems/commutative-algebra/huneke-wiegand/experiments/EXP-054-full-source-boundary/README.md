# EXP-054: original source-boundary audit

The naive original-source lift is refuted at all three training parameters. The reduced matrix
identities remain correct. Read [verdict.md](verdict.md) and [proof.md](proof.md) for the precise
scope. EXP-055 supplies the uniform one-column repair.

Run from the repository root:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-054-full-source-boundary/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-054-full-source-boundary/audit.py
```

Both runners accept `--output` for temporary reruns. The independent checker does not import the
primary multiplication or trust saved success flags. All computation is exact and CPU-only.
