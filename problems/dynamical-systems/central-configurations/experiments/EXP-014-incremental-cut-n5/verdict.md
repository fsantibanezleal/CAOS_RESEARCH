# EXP-014 - Verdict: SANITY AND NONZERO NORMAL FORM CONFIRMED, INCREMENTAL EXTENSION INCONCLUSIVE-CAP (2026-08-01; the n = 5 deterministic state stands at products = 5 exact, cut <= 5; the 5-to-4 question moves to witness sets and the strata campaign proceeds)

Hypothesis: `hypothesis.md` (declared before any run). Runner: `run.py`.
Artifacts: `artifacts/` (the single Singular script, its output through the
cap, results, run log).

## Outcomes against the declared predictions

| Prediction | Outcome | Facts |
|---|---|---|
| Smoke (products basis reproduced in-session) | PASS | size(S) = 2436, byte-level agreement with EXP-013's archived count |
| P1 (NF(cm, S) nonzero) | PASS | reduce(cm, S) is a nonzero normal form: Cayley-Menger is NOT in the products ideal, consistent with the 4-simplex separation the EXP-011 smoke gate established |
| P2 (incremental std(S, cm) within 1800 s) | INCONCLUSIVE-CAP | the extension ran its full declared budget (about 1860 s of engine time inside the cap wrapper) without terminating |
| P3 (exact cut dimension, two-way agreement) | UNTESTED | no completed basis |

## Where the n = 5 dimension question now stands, deterministically

- dim(products variety in the torus) = 5, EXACT (EXP-013's completed basis).
- dim(cut) <= 5, PROVEN (menu union bound, EXP-013).
- Cayley-Menger is not a member of the products ideal (this experiment's P1),
  so the cut is a proper subvariety of the products variety; whether the top
  5-dimensional components all survive the cut (which would keep dim 5) or
  all get sliced (dim 4, the expected value) is exactly what neither the
  from-scratch nor the incremental Groebner computation could decide at
  declared budgets.
- Per the declared consequence ladder: the dimension question at n = 5 moves
  to the witness-set lane (CCB-034: certified numerical irreducible
  decomposition would list the top components of the products variety and
  evaluate CM on witness points, which is precisely the 5-vs-4 test), and
  the k = 2, p = 2 symmetric-stratum campaign proceeds regardless, since its
  9-variable quotient systems are smaller than everything that walled here
  and the cost law (keep realizability equations out of the Groebner core)
  is now measured twice.

## Adversarial validation record

- The in-session recomputation of S removes any dependence on the archived
  file; the 2436 agreement is the reproducibility check.
- A ZERO normal form would have been reported as a BUG, not a finding, per
  the hypothesis; the nonzero outcome also independently re-confirms the
  EXP-011 three-way smoke separation.
- The cap was enforced by `timeout` inside WSL on a single Singular process;
  no partial output from the capped std(S, cm) stage was parsed or used.
