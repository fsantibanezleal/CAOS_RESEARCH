# EXP-010 verdict: INCONCLUSIVE (engine-bound in QF_BV as well); the solver lane closes

Run 2026-08-20; artifact `artifacts/bv.json` + `run_detached.log`.

## Outcome

The pure bit-vector ladder validated its semantics (the pinned known
witness satisfies the constraints in 5.4 s with exact tclib replay) but
the FREE-STRUCTURE known-answer search (6 gates, 5 roots, bound 8,
width 64) hit its 1 h cap: z3's QF_BV engine, like its NIA engine
(EXP-008), cannot search this structure space at validation scale. Per
the pre-declared gate, the ladder halted itself and the residual phase
never ran.

## The lane's closing record

Two independent backends (NIA with CEGAR + structural nonzero column;
pure QF_BV with overflow guards), both with correct semantics proven on
pinned witnesses, both unable to complete the SMALLEST known-answer
search within generous caps. Conclusion, recorded for the program: the
per-gate guarded-selector evaluation encoding creates a search space
that defeats general-purpose solvers at 6+ gates, and further solver
engineering (custom symmetry breaking, incremental layering, other
solvers) is NOT justified while the census route stands: EXP-011's
pipeline is fully validated (validate PASS 185 s; scan8 smoke PASS
463 s reproducing z_max(7) = 5 over 25.8M states) and decides
z_max(8) exactly and UNCONDITIONALLY, subsuming this experiment's
question. The encodings, the f != 0 column, the CEGAR harness and the
incident lessons are retained as reusable method notes.

## Prediction scorecard

Prediction 1 (QF_BV passes the known-answer) REFUTED: the second
tractability judgment to fall; the emptiness predictions (2) were never
reached. Honest null recorded.
