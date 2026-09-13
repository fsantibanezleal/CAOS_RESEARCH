# EXP-001 hypothesis, committed before the result

Date declared: 2026-09-12, before the build finished. Per methodology 02, the hypothesis and the
meaning of each outcome are fixed in advance so that whatever happens is informative rather than
rationalized afterwards.

## Question

Does `openai/NavierStokesAndEuler` build, and do the two Comparator challenges accept the solution
modules against the reference statements?

This is the only verification of the September 2026 claims that is mechanically available to a third
party today. It is not a check of the mathematics; it is a check that the certificate the world has
been pointed at is a real certificate.

## What each outcome would prove

| outcome | what it proves | what it does NOT prove |
|---|---|---|
| build succeeds, Comparator accepts | the 641,332 lines type-check under the Lean kernel, and the proved declarations have the same type as the third-party-derived reference statements | that the manuscripts contain the arguments, or that the mathematics is right in any sense a referee would accept |
| build fails | either the artifact is incomplete, or our environment is wrong. **A failure here is much more likely to be ours than theirs**, and must be diagnosed before it is reported as anything | nothing about the claim, unless the failure is reproduced on a clean environment matching the documented toolchain |
| Comparator rejects | the proved statement differs in type from the reference statement, which would be a serious finding | |
| kill criterion reached | only that this hardware could not host the check | |

**The asymmetry is deliberate and is stated up front**: a green build is weak positive evidence, and a
red build is, in the first instance, evidence about our machine. Reporting a red build as a defect in
the artifact without reproducing it cleanly would be exactly the error this problem has already
caught four times in other forms.

## Setup

- Clone of `openai/NavierStokesAndEuler` at last push 2026-09-10T15:14:13Z, at `E:/_Temp/lean-ns`.
- Toolchain pinned by the repository: `leanprover/lean4:v4.34.0-rc2`, installed through elan into
  `E:/_Temp/elan` so nothing lands on the system drive.
- Stages: `lean --version` (which triggers the toolchain fetch), `lake exe cache get` for the mathlib
  oleans, a **smoke build of one module** (`NavierStokes.ComparatorSolution`) before the full build,
  then `lake build`.
- Driver: `E:/_Temp/lean-build.sh`, logs under `E:/_Temp/lean-build/`.

## Declared budget and kill criterion

- Wall clock: 90 minutes for the cache stage, 2 hours for the smoke build, 8 hours for the full build,
  each enforced by `timeout`.
- Disk: **abort if free space on E: falls below 5 GB**, checked between every stage. E: began the run
  at 27 GB free.
- One heavy job at a time.

## Preflight notes recorded before the run

- An earlier attempt failed with `lake: command not found` because the exported `PATH` did not reach
  the child, and the driver's trailing `echo` masked exit code 127 as a success. Both fixed: absolute
  executable paths, and exit codes propagated rather than swallowed.
- Progress must be read from the artifact, not the process. The parent `lake` process shows flat
  accumulated CPU for the whole cache stage because the work happens in children; the olean count
  under `.lake` is the honest signal and rose steadily at about 250 per minute.
