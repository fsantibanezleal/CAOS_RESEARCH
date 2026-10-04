# Pressure-family audit

`proof.md` and `ceiling-declaration.md` give the uniform argument. The two
auditors need only python-flint, the pinned packet, window receipt and
recorded pressure-duality.json; they do not import the floating optimizer.

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-022-pressure-duality-audit/audit.py
python problems/number-theory/riemann-hypothesis/experiments/EXP-022-pressure-duality-audit/ceiling_audit.py
```

The optional exploration source is `code/pressure_duality_audit.py` and
its actual dependency versions are pinned in requirements-exploration.txt.
Use an isolated environment or dependency target. This run used SciPy in
E:/_Datos/caos-research/riemann-hypothesis/experiment-dependencies/exp022,
with OPENBLAS_NUM_THREADS=1 and OMP_NUM_THREADS=1. Both pre-math setup
failures are retained. Do not overwrite sealed receipts on reproduction;
run into a separate output directory or copy the experiment first.

The cap is on this fixed packet counting method. No new universal local
lower inequality, zeta proportion, other-method ceiling or RH result is
implied by the optimizer or this barrier.
