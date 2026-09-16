# EXP-006 verdict: the Lean kernel accepts the whole certificate, not just the elaborator

Date: 2026-09-16. Hypothesis committed first at [`hypothesis.md`](hypothesis.md) (commit `b3dd0a2`).
Runner: `E:/_Temp/exp006-fresh.sh`; logs and exit codes in `E:/_Temp/exp006/`. Toolchain
`leanprover/lean4:v4.34.0-rc2`, the version the certificate itself pins.

**Verdict: CONFIRMED.** Both halves of `openai/NavierStokesAndEuler` replay clean through the Lean
kernel from an EMPTY environment.

| target | constants replayed | wall clock | exit |
|---|---|---|---|
| `NavierStokes` | the module's entire closure, mathlib and core included | 2,972 s (49.5 min) | 0 |
| `Euler` | the same, for the unforced Euler half | 1,588 s (26.5 min) | 0 |

## What this adds to EXP-001

[EXP-001](../EXP-001-lean-replay/verdict.md) established that the package BUILDS (11,424 jobs, zero
`sorryAx`, the four headline theorems reporting exactly `propext`, `Classical.choice`, `Quot.sound`).
Both of those readings come from the environment the **elaborator** produced.

`leanchecker --fresh` imports a module's closure and replays every constant in it into a fresh kernel
environment, so each declaration is type-checked by the kernel alone. Its own documentation is blunt
about the scope, and the verdict inherits that wording: it is "not an external verifier, simply a tool
to detect environment hacking". That is exactly the gap worth closing here: a successful build leaves
open, in principle, declarations that entered the environment through metaprogramming paths rather
than through a kernel check. They did not.

Availability mattered and was checked rather than assumed: the separate `lean4checker` repository is
deprecated (its last commit, 2026-03-25, is the deprecation notice), because the checker now ships
with every toolchain from Lean v4.28.0 as `leanchecker`. The certificate pins v4.34.0-rc2, which is
installed here, so this ran at the exact pinned version with no toolchain bump and no third-party
build.

## Gates

- **E1, every module replays.** Met in the stronger `--fresh` form: rather than replaying each module
  against its own imports, the entire closure of each root module was replayed into an empty
  environment. Exit status 0 for both.
- **E2, the count is checked rather than assumed.** This is why the strategy changed mid-experiment,
  and the change is recorded rather than smoothed over. The first attempt swept all 2,659 package
  modules by prefix. `leanchecker` queues one task per module and each task loads its own import
  closure, which on this machine is I/O bound: after 80 minutes it had accumulated 144 seconds of CPU
  and 11.6 GB resident, with no module finished. It was killed and replaced by the `--fresh` runs
  above, which import once and are CPU bound. The `--fresh` form makes the count question moot, since
  a run that replayed nothing could not take 50 minutes of CPU, and `-v` confirms the target.
- **E3, negative control.** Two are on record. `leanchecker NavierStokes.ThisDoesNotExist` fails with
  "Could not find any oleans", exit 1, so a mistyped target cannot pass silently. And the same binary
  invoked without a project environment fails on the manifest module (`FluidEquations`), which is how
  the CLI semantics were pinned down: they were read from `src/LeanChecker.lean` in the Lean
  repository rather than guessed.
- **E4, the headline theorems are inside the closure.** Both root modules are the aggregators the
  headline theorems live under, and EXP-001 already pinned the axiom sets of the four theorems by
  name; a fresh replay of the roots' closures covers every constant those proofs use.

## What it does not establish

- Nothing about whether the STATEMENTS are the right ones. That is what the two statement audits are
  for, and the strongest fact there remains that the reference statement was adapted from DeepMind's
  Formal Conjectures, written by a third party before the claim existed.
- Nothing about the mathematics being correct in the sense a referee means. A kernel-accepted proof of
  a faithfully stated theorem is a strong artifact, not a substitute for the community reading it.
- Nothing about the parts of the pipeline outside Lean: the manuscripts' prose, and the reasoning that
  chose the construction, are unaffected by any machine check.

## Cost

Two CPU-bound runs, 76 minutes total, at most 6.4 GB resident, alongside the GPU work of EXP-005. The
abandoned per-module strategy cost 80 wall-clock minutes and is the reason the runner now uses
`--fresh`.
