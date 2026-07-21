# EXP-001 - Validate the announced N=3 counterexample to the Jacobian conjecture

- **Question.** Is the polynomial map announced by Levent Alpöge (X post, 2026-07-19/20, credited
  to Claude Fable 5) a genuine counterexample to the Jacobian conjecture for N = 3?
- **Motivation.** Entry event of the whole problem program; context dossier section 5. No arXiv
  paper exists; independent exact verification is required before anything is built on it.
- **Falsifiable prediction.** In exact rational arithmetic: (A) det JF is identically -2;
  (B) the three points (0, 0, -1/4), (1, -3/2, 13/2), (-1, 3/2, 13/2) are pairwise distinct and
  all map to (-1/4, 0, 0). If either fails, the counterexample claim is refuted.
- **Method.** sympy 1.14 over QQ: symbolic Jacobian determinant, exact substitution; additionally
  (best-effort) the FULL fiber over (-1/4, 0, 0) by lex Groebner basis, to characterize the
  non-injectivity completely rather than pointwise.
- **Success criterion.** All asserted checks pass exactly (script exits 0).
- **Failure criterion.** Any check fails; then the announcement is refuted by this record.

Declared 2026-07-20 before the run (run performed the same day in the management-repo wip and
migrated here verbatim as the problem's founding experiment; see verdict).
