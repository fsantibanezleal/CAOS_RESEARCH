# EXP-057: four-row endpoint representative

This experiment tests a single-column cancellation of the EXP-056 `K`-side chain. The declared
P3 has a sign error: the correct original-source identity uses `s+q`, not `s-q`. The frozen
hypothesis is preserved, and the overall verdict must remain REFUTED even if the independently
retained endpoint reduction passes.

Read [proof.md](proof.md) for the complete all-parameter face argument and exact scope.

From the repository root, run the initial smoke gate:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-057-four-row-kernel-normal-form/run.py --output E:/_Temp/hw057-smoke.json
```

It records the `p=8` P3 refutation and stops. To explicitly continue independent validation of
P1/P2 and the corrected plus identity through `p=100`:

```powershell
.venv/Scripts/python.exe problems/commutative-algebra/huneke-wiegand/experiments/EXP-057-four-row-kernel-normal-form/run.py --continue-retained
.venv/Scripts/python.exe -m pytest tests/test_hw_endpoint_reduction.py
```

The canonical artifact is deterministic: it contains hashes, support counts, mutation outcomes,
and the exact six-row `p=8` counterexample, but no timestamps or elapsed durations. Each parameter
is checkpointed. The default budget is 60 seconds. Budget exhaustion or an unexpected arithmetic
disagreement exits nonzero and retains the latest checkpoint. A successfully certified hypothesis
refutation is a recorded mathematical outcome, not an execution error.

No HNF, full-basis construction, original `p=11` source reconstruction, manuscript build, or
publication is performed. Tests write only to temporary paths and read the canonical certificate
for integrity validation.
