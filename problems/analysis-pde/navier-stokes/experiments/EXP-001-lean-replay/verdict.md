# EXP-001 verdict: the full certificate CONFIRMED to build (Navier-Stokes and Euler)

Dates: run and Navier-Stokes confirmation 2026-09-12; Euler confirmation 2026-09-13 after a cache
repair. Hypothesis committed before the run in
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

## Result, Euler: CONFIRMED, after repairing a corrupted and contended local cache

The full build completed on 2026-09-13: **`Build completed successfully (11424 jobs)`**, zero `sorryAx`
anywhere, zero `error:` lines. The axiom report now covers all four declarations:

```
'NavierStokes.Comparator.navier_stokes_breakdown_R3'       depends on axioms: [propext, Classical.choice, Quot.sound]
'NavierStokes.Comparator.navier_stokes_breakdown_periodic' depends on axioms: [propext, Classical.choice, Quot.sound]
'Euler.euler_breakdown_R3'                                 depends on axioms: [propext, Classical.choice, Quot.sound]
'Euler.exists_compact_smooth_euler_singularity'            depends on axioms: [propext, Classical.choice, Quot.sound]
```

So the proofs of **both** unforced-Euler theorems (the breakdown statement and the quantitative
finite-lifespan singularity with the maximality clause audited on 2026-09-12) type-check under the Lean
kernel on an independent machine with no admitted gaps and only the three standard axioms. Together
with the Navier-Stokes result above, **the entire OpenAI certificate compiles clean**.

Getting there took a two-part environmental repair, documented below because the failure was
instructive and because the committed hypothesis demanded a red build be diagnosed, not reported at
face value.

### The two-part diagnosis, in order

The build failed repeatedly with `failed to read file` on mathlib oleans and `0xC0000409` process
crashes, **never a mathematical error**. Two distinct causes, peeled apart across attempts:

1. **Corruption.** The external multi-hundred-GB disk deletion during the first attempt damaged some
   cached mathlib oleans; they kept their size, so `lake exe cache get` trusted them ("already
   decompressed") and the read failures recurred with the disk idle. Fixed by `lake exe cache get!`
   plus, decisively, `lake exe cache unpack!`, which force-overwrote all 8,747 oleans from freshly
   downloaded archives. The decompression itself hung twice on stale file locks from interrupted runs;
   it completed once the killed processes were cleared and it wrote into unlocked files.
2. **Read contention.** After a fully repaired cache, the build STILL failed on ~34 reads per pass, but
   on a **different rotating set of files each pass, including a Lean toolchain olean that was never
   re-fetched**. Files that were never corrupted were failing. That is not corruption; it is runtime
   contention: dozens of parallel Lean processes on E: colliding with transient file locks (a
   real-time antivirus scan on open is the usual cause). This Lake version exposes no `-j`/`--jobs`
   flag to lower parallelism.

### The fix: an incremental convergence loop

Lake is incremental: every module it compiles persists. So repeated `lake build` passes each make net
progress, because a different subset of dependency oleans is transiently locked each time, blocking a
different subset of project modules. The read-error count converges to zero:

| pass | read errors | crashes | completed |
|---|---|---|---|
| 1 | 22 | 5 | no |
| 2 | 11 | 1 | no |
| 3 | 9 | 1 | no |
| 4 | 5 | 0 | no |
| 5 | **0** | **0** | **yes** |

Five passes, monotone decrease, terminating in a clean full build. The loop (`E:/_Temp/lean-build-loop.sh`)
also carried a no-progress guard to stop honestly rather than spin if the count had plateaued; it did
not fire.

### What this establishes

The complete certificate compiles from a clean checkout on independent hardware, and all four headline
theorems depend only on the standard axioms with no `sorry`. This is the strongest form of the one
mechanically-available check, and it now covers the mathematically stronger unforced-Euler claim as
well as the Millennium (C)/(D) claim.

## Superseded diagnosis, preserved

The section below was written while the Euler build was still failing and before the read-contention
cause was isolated. It is kept as the honest in-progress record; the resolution is the section above.

## Result, Euler (earlier, in-progress): build DISRUPTED by a corrupted cache, not by the artifact

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

Establishes: the entire certificate compiles from a clean checkout on independent hardware, and all
four headline theorems (Fefferman C and D, and both unforced-Euler theorems) depend only on the three
standard axioms, with no `sorry`.

Does not establish: that the 165-page Navier-Stokes manuscript (and the 56-page Euler manuscript)
contain the arguments the Lean encodes; that Comparator and the external kernel re-checkers
(`lean4export`, `nanoda_bin`) accept the solution modules against the challenge modules, which needs
`landrun` and those two binaries and was not attempted; or anything about whether the mathematical
community accepts the result. The statement audits of 2026-09-11 and 2026-09-12 remain the reason to
believe these are the right theorems; this experiment shows the proofs of them are machine-checkable.

## Cost, against the declared budget

| stage | budget | actual |
|---|---|---|
| toolchain plus mathlib cache | 90 min | about 46 min, exit 0 |
| smoke build of the Navier-Stokes comparator module | 2 h | about 60 min, exit 0, and re-confirmed on two later runs |
| full build including Euler | 8 h | completed on 2026-09-13 after a cache repair; 11,424 jobs, five incremental passes |
| disk floor | abort below 5 GB free | low-water mark about 12 GB, never triggered |
