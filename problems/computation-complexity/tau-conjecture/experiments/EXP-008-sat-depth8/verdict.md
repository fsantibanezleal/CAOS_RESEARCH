# EXP-008 verdict: INCONCLUSIVE (solver-intractable); encoding semantics validated; residual routed

Runs 2026-08-03..19 (three launches + two diagnostics), repo venv, z3
4.16.0. Raw record: `artifacts/sat8.json` (absent phases never resolved),
`run_detached.log`, and the diagnostics below.

## Outcome

The final-$\pm$ question at depth 8 (does an 8-gate 7-rooter with final
addition/subtraction exist?) is NOT decided. $z_{\max}(8)$ therefore
remains: $= 6$ unless such a polynomial exists (EXP-006/007 decided
everything else at depth 8). Per the amendment's escape clause, the
residual routes to the depth-8 census backend (TCB-005) or a future
PROPOSITIONAL encoding.

## The solver record (the honest product of this experiment)

1. Launch 1 (2026-08-03): plain NIA; the known-answer validation did not
   complete its cap in foreground and the detached run died with a
   session teardown before any checkpoint (no per-phase checkpoint had
   been written: fixed thereafter).
2. Launch 2 (2026-08-19): QF_NIA + value-bounded known-answer. Entered a
   DEGENERATE CEGAR loop: 179,649 consecutive zero-polynomial models in
   6.7 h; the phase cap existed only as a per-check solver timeout.
   Killed. Lessons fixed as amendment 2: a structural $f \ne 0$
   constraint (one evaluation column at a fresh point $y$ with
   $f(y) \ne 0$: excludes exactly the zero polynomial) and loop-level
   budgets (block cap + wall cap; INCONCLUSIVE(budget) as an outcome).
3. Launch 3 (2026-08-19, fixed): the known-answer (6 gates, 5 roots,
   bound 8) returned `unknown` at its 30-min cap; the runner correctly
   halted the ladder ("encoding not trusted").
4. Diagnostic A: the same instance with all five roots CONCRETE
   ($-2..2$): still `unknown` at 5 min: the STRUCTURE search, not the
   root search, is what defeats Z3's nonlinear-integer engine.
5. Diagnostic B: the instance with the ENTIRE witness program pinned
   (structure + roots): SAT in 0.5 s, and the replay reproduces
   $\mp x(x^2-1)(x^2-4)$ with roots $\{0,\pm1,\pm2\}$ exactly.
   **The encoding semantics are CORRECT; the lane is solver-bound.**

## What survives

- The evaluation encoding (V11 object) is validated and reusable: gate
  semantics, the $f \ne 0$ column, the CEGAR replay harness, and the
  budget discipline are all in place for a future engine (candidate:
  bit-blasted propositional SAT at fixed value width, the actual
  Fuhs-Schneider-Kamp pattern, which is Boolean SAT, not SMT NIA; their
  solvers handled comparable structure spaces).
- Two methodology upgrades now standing: per-phase immediate
  checkpoints + detached long runs (survive session teardown), and
  loop-level kill criteria (a per-check timeout is not a phase budget).

## Predictions scorecard

Prediction 1 (known-answer SAT) FAILED in the operative sense: not
because the encoding is wrong (diagnostic B) but because the solver
cannot search it: recorded as the refutation of our TRACTABILITY
judgment, the round's honest null. Predictions 2-3 were never reached.

## Consequences

- TCB-029 stays open, re-scoped: "decide the final-$\pm$ residual by a
  bit-blasted propositional encoding or the depth-8 census" (the NIA
  route is closed by this record).
- Paper v0.03 (TCB-028) stays queued: no $z_{\max}(8)$ resolution yet.
- The depth-8 census backend (TCB-005) is now the leading route for the
  residual AND for $z_{\max}(8)$ in full.
