# EXP-065 dual-guided endpoint decoder

This experiment extracts explicit integral mask-58 sources for the two endpoint
triangle rows. It uses exact dual-guided column generation and preserves original
semantic column labels.

Smoke test:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-065-dual-guided-endpoint-decoder/run.py --p-min 8 --p-max 8 --target-limit 1 --max-rounds 2 --budget-seconds 120 --memory-gib 4 --output E:/_Temp/exp065-smoke.json --checkpoint E:/_Temp/exp065-smoke-checkpoint.json
```

Canonical training run:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-065-dual-guided-endpoint-decoder/run.py --p-min 8 --p-max 10 --target-limit 2 --max-rounds 6 --max-columns 900 --budget-seconds 900 --memory-gib 8
```

Independent audit:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-065-dual-guided-endpoint-decoder/audit.py
```

The `p=11` carrier is a locked holdout for a later experiment. EXP-065 does not
run it and does not claim an all-parameter formula.
