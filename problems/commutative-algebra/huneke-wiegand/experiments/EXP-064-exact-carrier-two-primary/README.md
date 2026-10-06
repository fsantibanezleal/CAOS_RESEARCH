# EXP-064 exact carrier two-primary groups

This experiment upgrades EXP-063's finite mod-two comparison to an exact
finite integral classification for masks `56,58,59,62` at `p=8,...,11`.
Read `hypothesis.md`, `proof.md`, and `verdict.md` in that order.

Canonical producer:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-064-exact-carrier-two-primary/run.py --p-min 8 --p-max 11 --budget-seconds 1200 --memory-gib 12
```

Independent audit:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-064-exact-carrier-two-primary/audit.py --budget-seconds 1200 --memory-gib 12
```

The certificate is finite and uses rational-rank/Hadamard bounds plus the
first integral Bockstein. It does not give a uniform source formula or classify
the complementary full cokernel.
