# EXP-003 verdict - CONFIRMED

Run date: 2026-08-01. Phase HW-P3. Backlog HWB-003.

## Result

All predeclared predictions P1-P6 pass with Z3 4.16.0 and a separate standard-library checker.

- The candidate membership vector pinned at `(F,s)=(181,14)` is SAT in 34.51 seconds.
- The extracted vector has SHA-256
  `8bf4cd6f17f12068a5755533a6852f2c36fbe9cb704c17a778a94789745fd80b` and exactly
  matches the independently recomputed candidate semigroup.
- The solver-independent checker verifies symmetry, additive closure, nonprincipality and
  `D=E+E` on `0 <= n <= 363`. Since `min(E)=56`, the automatic tail actually starts at 238;
  the encoded `2F+1` bound is conservative and complete.
- Flipping candidate membership at 1 is rejected independently for both symmetry and closure.
- For the control `Gamma=<4,5>`, every nonzero gap is rejected. The first explicit values in
  `D` missing from `E+E` are:

| shift `s` | 1 | 2 | 3 | 6 | 7 | 11 |
|---|---:|---:|---:|---:|---:|---:|
| first missing value | 14 | 8 | 9 | 4 | 5 | 4 |

Each fully pinned control query is also UNSAT, agreeing with direct checking.

## What is established

The finite encoding faithfully recognizes the known counterexample and rejects a known-positive
hypersurface control. Every emitted SAT model is independently checkable without Z3, and the
finite-to-infinite tail is explicit.

## What is not established

This calibration does not show that the candidate is unique or minimal. The pinned control UNSAT
queries are instrument tests, not a certified lower-frontier computation. Any frontier claim still
requires proof-producing SAT with independently checked certificates or a separate exhaustive
enumerator. EXP-004 owns that gate.
