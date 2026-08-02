# EXP-003 - SAT encoding calibration

Declared 2026-08-01 before installing or invoking a SAT/SMT dependency, before implementation,
and before any run. Phase HW-P3. Backlog HWB-003.

## Question

Can a finite Boolean formulation faithfully represent symmetric numerical semigroups and the
rigidity equality for a nonprincipal two-generated monomial ideal, without importing the public
candidate verifier?

For fixed odd Frobenius number `F` and positive gap `s`, use Boolean `h[n]` for membership in
Gamma on `0 <= n <= F`; membership is true above F. Enforce zero, Frobenius, additive closure,
and symmetry `h[n] iff not h[F-n]`. Define

```text
E(n) = h(n) and h(n+s)
D(n) = h(n) and h(n+s) and h(n+2s).
```

The reverse inclusion `E+E subset D` follows from additive closure. Encode `D subset E+E`
for `0 <= n <= 2F+1`. This window is complete: `min(E) <= F+1`, so every `n >=
2F+2` has `n=min(E)+(n-min(E))` with both summands in E.

## Committed predictions

- P1: pinning `h` to the EXP-001 candidate at `(F,s)=(181,14)` is satisfiable.
- P2: an independent standard-library checker accepts the extracted candidate model and proves
  the exact equality through `2F+1` plus the conductor-tail argument.
- P3: the same checker rejects a deliberately corrupted candidate membership vector.
- P4: pinning the known-positive control `Gamma=<4,5>` at `F=11` with each nonzero gap `s`
  yields no rigid nonprincipal case; direct checking identifies an explicit failed D value for
  each gap.
- P5: every SAT model emitted by this experiment is rechecked without the solver for zero,
  Frobenius, symmetry, closure, nonprincipality and the exact rigidity window.
- P6: the implementation records solver version, constraints, model hashes, runtimes and all
  control witnesses; a solver `unknown` or unchecked model cannot pass.

## Scope and gates

EXP-003 calibrates machinery only. SAT at `(181,14)` does not establish uniqueness or
minimality. An UNSAT frontier requires either proof-producing SAT with an independently checked
certificate or a separate exhaustive implementation. Dependency installation is permitted only
after this declaration is committed.

Wall cap: five minutes per calibration query. Exact integers and deterministic seeds only.

