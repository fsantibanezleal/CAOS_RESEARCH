# EXP-066 uniform endpoint face collapse

This experiment tests the frozen support-one endpoint formula on the untouched
`p=11` carrier and proves or refutes its direct all-parameter face
classification in the full semantic row projection.

Canonical producer and independent audit:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-066-uniform-endpoint-face-collapse/run.py
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-066-uniform-endpoint-face-collapse/audit.py
```

The hypothesis was committed before execution.  Its `10p-1 where admissible`
negative control is realized by the nearest admissible degree-one neighbour
`10p-2`: `10p-1` is a degree-two singleton and cannot label a source exterior.
