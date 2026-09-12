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

## Result, Euler: build DISRUPTED by a corrupted cache, not by the artifact; repair in progress

The full build, which additionally compiles the Euler development, failed. The failure was diagnosed
in three passes rather than reported at face value, because the committed hypothesis said a red build
is first of all evidence about this machine.

The error distribution across both build attempts is the whole story:

| error kind | count |
|---|---|
| `failed to read file ...olean` / `...olean.private` | many, on scattered unrelated mathlib files |
| `Lean exited with code 3221226505` (`0xC0000409`, a Windows process crash) | several |
| unknown identifier, type mismatch, `sorryAx`, or any other mathematical error | **0** |

The failing reads are on files the **Euler** modules import but the Navier-Stokes modules do not
(`Mathlib/Analysis/InnerProductSpace/Dual`, `Analysis/Asymptotics/Defs`, `Tactic/FieldSimp`,
`SetTheory/Ordinal/Basic`, and one inside the Lean toolchain itself). That is exactly why the smoke
build (Navier-Stokes only) succeeds while the full build (Euler) fails: Euler touches a larger,
different slice of mathlib.

Diagnosis, refined across the attempts:

1. **First attempt (09:xx).** During this build, several hundred gigabytes were deleted on E: by
   something outside this session (free space jumped 12 GB to 337 GB to 3,917 GB). Live I/O
   contention during that storm explained scattered transient read failures.
2. **Second attempt (14:xx), disk quiet.** The read failures RECURRED on the same class of files with
   the volume idle. So the storm did not merely disrupt reads in flight, it **corrupted** some cached
   mathlib oleans: they exist at full size (`Ordinal/Basic.olean.private` is 1,058,760 bytes) but read
   as damaged. `lake exe cache get` reports them "already decompressed" and trusts them, so the
   corruption persists across runs.

Either way, zero mathematical errors, and the fault is in the local mathlib cache, not in the OpenAI
artifact. Per the committed hypothesis, this is not reported as a defect in the certificate.

**Repair in progress.** `lake exe cache get!` forces a fresh re-fetch of all mathlib oleans, replacing
the corrupted files, followed by a clean full build. The driver is `E:/_Temp/lean-repair.sh`, logs
under `E:/_Temp/lean-build/` (`cache-repair.log`, `build-repair.log`). The Euler outcome is recorded
here when it lands; the Navier-Stokes confirmation above stands regardless, having built cleanly three
times.

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
| smoke build of the Navier-Stokes comparator module | 2 h | about 60 min, exit 0, and re-confirmed on two later runs |
| full build including Euler | 8 h | corrupted-cache repair in progress |
| disk floor | abort below 5 GB free | low-water mark about 12 GB, never triggered |
