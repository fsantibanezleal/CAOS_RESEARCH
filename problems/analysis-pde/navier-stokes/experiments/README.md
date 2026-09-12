# navier-stokes experiments

Empty at open time, 2026-09-11. No experiment has been run and none will start before the plan in
`program/navier-stokes/plan.md` is validated.

Each experiment gets its own directory `EXP-00N-<slug>/` holding, per methodology 02: the hypothesis
committed **before** the run, the exact command and environment, the raw outputs, the controls (at
least one positive and one deliberately corrupted negative), and the verdict. A verdict is CONFIRMED,
REFUTED, INCONCLUSIVE or DECIDED-IN-PART, and a refuted prediction is preserved rather than edited
away.

Queued, with budgets and kill criteria already declared in `program/navier-stokes/backlog.md`:

- **EXP-001** (NS-003): build `openai/NavierStokesAndEuler` and run both Comparator challenges. The
  only verification of the September 2026 claims that anyone can perform today.
- **EXP-002** (NS-005, NS-006): reproduce the inviscid modulation system and validate it against a
  direct 2D pseudo-spectral Boussinesq simulation through one growth, steering and holding cycle.
  Positive control that the reduction tracks the PDE; negative control with a corrupted coefficient
  that must fail the same comparison.
- **EXP-003** (NS-007): add the time budget and the hold-interval damping to the cascade recursion,
  then sweep the dissipation threshold as a batched GPU ensemble.

The preflight check that already exists, `../code/modulation_smoke.py`, is not an experiment. It is
the tooling smoke test methodology 12 requires before machine time, and it has already done its job
once by refuting the first reading of the threshold.
