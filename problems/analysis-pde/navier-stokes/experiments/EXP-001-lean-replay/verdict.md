# EXP-001 verdict: Navier-Stokes CONFIRMED, Euler INCONCLUSIVE on this machine

Date: 2026-09-12. Hypothesis committed before the run in
[`hypothesis.md`](hypothesis.md). Subject: `openai/NavierStokesAndEuler` at last push
2026-09-10T15:14:13Z. Toolchain `leanprover/lean4:v4.34.0-rc2` installed via elan into `E:/_Temp/elan`.
Logs: `E:/_Temp/lean-build/`.

## Result, Navier-Stokes: CONFIRMED

The smoke stage built `NavierStokes.ComparatorSolution`, which transitively pulls the entire
Navier-Stokes development.

```
[9371/9371] Built NavierStokes.ComparatorSolution
Build completed successfully (9371 jobs).
smoke exit=0
```

The decisive output is the axiom report that `ComparatorSolution.lean` emits for both headline
declarations:

```
'NavierStokes.Comparator.navier_stokes_breakdown_R3'       depends on axioms: [propext, Classical.choice, Quot.sound]
'NavierStokes.Comparator.navier_stokes_breakdown_periodic' depends on axioms: [propext, Classical.choice, Quot.sound]
```

Three checks, all clean:

| check | result |
|---|---|
| build of all 9,371 targets | succeeded |
| `sorryAx` anywhere in the log | **0** |
| axioms of both theorems | exactly the three standard Lean axioms |

`sorryAx` is the conclusive one. A Lean proof containing `sorry` reports `sorryAx` in its axiom
dependencies; neither declaration does, and the string does not occur anywhere in the build output.
So the proofs of Fefferman's alternatives **(C)** and **(D)**, as stated in the comparator module we
audited on 2026-09-11, type-check under the Lean kernel on an independent machine with no admitted
gaps.

A caution about the three "error" matches a naive grep finds in the smoke log: they are the module
names `NavierStokes.ErrorHarmonics`, `GlobalBaseError` and `GaussianErrorNaturality`. Grepping for
"error" without looking is how a clean build gets reported as a broken one.

## Result, Euler: INCONCLUSIVE, and the cause is this machine

The full build, which additionally compiles the Euler development, was disrupted. It produced 25
errors, and their distribution is the whole story:

| error kind | count |
|---|---|
| `failed to read file` | 19 |
| `Lean exited with code 3221226505` | 5 |
| unknown identifier, type mismatch, sorry, or any other mathematical error | **0** |

The 19 read failures are on **nineteen different, unrelated files**:
`Mathlib/SetTheory/Ordinal/Basic.olean.private`, `Mathlib/Topology/Separation/Hausdorff.olean.private`,
`Mathlib/Tactic/FieldSimp.olean`, `Mathlib/Tactic/ITauto.ir`, and among them
`elan/toolchains/.../Lean/Elab/Tactic/Omega/Frontend.olean.private`, which is part of **the Lean
toolchain itself and not of the project under test**. `3221226505` is `0xC0000409`, a Windows process
crash, consistent with reads returning truncated or locked data.

The named files exist and are intact: `Ordinal/Basic.olean.private` is 1,058,760 bytes on disk. The
cache holds 8,371 `.olean.private` files against 8,381 `.olean`.

The cause is external and was visible while it happened. During this stage, free space on E: went from
12 GB to 337 GB to 3,917 GB as several hundred gigabytes were deleted by something outside this
session. Heavy concurrent deletion on the same volume is a sufficient explanation for scattered
transient read failures and crashed reader processes, and no other explanation accounts for a failure
inside the toolchain's own files.

**Per the hypothesis committed before the run: this is evidence about the machine, not about the
artifact, and it is not reported as a defect.** The Euler half is re-run once the volume is quiet; the
outcome is recorded here when it lands.

## What this does and does not establish

Establishes: the Navier-Stokes certificate compiles from a clean checkout on independent hardware, and
its two headline theorems depend only on the standard axioms, with no `sorry`.

Does not establish: that the 165-page manuscript contains the arguments the Lean encodes; that
Comparator and the external kernel re-checkers (`lean4export`, `nanoda_bin`) accept the solution
module against the challenge module, which needs `landrun` and those two binaries and was not
attempted; or anything about whether the mathematical community accepts the result. The statement
audits of 2026-09-11 and 2026-09-12 remain the reason to believe the theorem is the right theorem; this
experiment only shows the proof of it is machine-checkable.

## Cost, against the declared budget

| stage | budget | actual |
|---|---|---|
| toolchain plus mathlib cache | 90 min | about 46 min, exit 0 |
| smoke build of the Navier-Stokes comparator module | 2 h | about 60 min, exit 0 |
| full build including Euler | 8 h | disrupted, rerun pending |
| disk floor | abort below 5 GB free | low-water mark about 12 GB, never triggered |
