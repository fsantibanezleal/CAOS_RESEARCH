# EXP-006 hypothesis: does the Lean KERNEL accept the certificate, and not just the elaborator?

Committed 2026-09-15, before the run.

## The gap this closes

[EXP-001](../EXP-001-lean-replay/verdict.md) established that `openai/NavierStokesAndEuler` builds
clean on an independent machine (11,424 jobs, zero `sorryAx`, all four theorems reporting exactly
`propext`, `Classical.choice`, `Quot.sound`). That is a statement about what `lake build` and
`#print axioms` report. Both read the environment the ELABORATOR produced.

The elaborator is a large program with escape hatches. Declarations can enter an environment through
paths that a per-declaration kernel check would have to re-examine: `implemented_by` and `extern`
replace compiled behaviour, `native_decide` moves a decision procedure out of the kernel (it announces
itself with an axiom, but only if it is used the intended way), and unsafe metaprogramming can add
constants directly. None of that is a claim that this certificate does any of it. It is the reason a
kernel-only replay is a different check from a successful build, and the reason mathlib runs one on
every release.

Since Lean v4.28.0 the checker ships with the toolchain as `leanchecker`, replacing the separate
`lean4checker` repository (now deprecated). The certificate pins `leanprover/lean4:v4.34.0-rc2`, which
is installed here, so the check is available at the exact toolchain version, with no version bump and
no third-party build.

## The two levels, and which one is being run

| level | what it does | cost |
|---|---|---|
| module replay | re-checks the declarations each module ADDS, starting from the environment its imports provide | comparable to elaboration |
| `--fresh` replay | re-checks every constant reachable from the module, mathlib included, in a fresh environment | much larger |

The certificate's own content is what is in question, so the primary run is a module replay over every
module of the package. A `--fresh` replay of the two headline modules is attempted afterwards and
reported with its cost; if it exceeds the budget it is recorded as not run rather than quietly skipped.

## Gates

- **E1.** Every module of the package replays with exit status 0.
- **E2.** The number of modules actually replayed equals the number of package `.olean` files found,
  and both are printed. A checker invoked on nothing exits 0, so without this count the gate could not
  see its own subject (the failure mode of F-017 and of the vacuous negative control in EXP-002).
- **E3.** Negative control: a byte-flipped copy of one module's `.olean` must make the checker fail.
  This shows the checker is reading and validating the content of the files it is pointed at. It does
  NOT show that the checker would detect an unsound proof, and the verdict must say so.
- **E4.** The four headline theorems are among the constants replayed, checked by name against the
  module list, so a pass cannot be reported from replaying only support modules.

## Budget and kill criterion

Wall clock 6 h for the module replay, 4 h for the optional `--fresh` attempt. Abandon a run whose
resident memory exceeds available RAM, or a single module exceeding 30 min, and record what was reached.

## What each outcome means

A clean replay raises EXP-001's verdict from "the build succeeds and the reported axioms are standard"
to "the kernel independently accepts every declaration the package adds". It still says nothing about
whether the STATEMENTS are the right ones, which is what the two statement audits are for, and nothing
about the mathematics being correct in the sense a referee means. A failure would be the most
consequential outcome available in this problem and would need to be reported to the authors before
anything else is written about it.
