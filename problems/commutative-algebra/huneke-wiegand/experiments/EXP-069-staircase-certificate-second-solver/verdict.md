# EXP-069 verdict: CONFIRMED

Date: 2026-11-14. Hypothesis frozen at `a1974bc0` before any code was written. Every number below is read from
`artifacts/results.json` and `artifacts/run-log.txt`; `run.py` reproduces them from the repository root (solver
times are the only nondeterminism).

## Result

The 16 Presburger obligations behind Theorem 7.2 of the curvilinear fiber-cone paper (EXP-026) are decided `unsat`
by a second solver, cvc5 1.4.2 (logic `LIA`, 600 s limit per leaf, default options), on queries whose digests equal
the certified ones. Z3 4.16.0 also decides the exported SMT-LIB texts `unsat`. All four perturbed controls are
`sat` for both solvers with a cvc5 model that an exact integer evaluator written for this experiment accepts.

## Prediction table

| prediction | outcome | evidence |
|---|---|---|
| P1 the 16 rebuilt query digests equal the stored digests | PASS, 16 of 16 (`digest_match`), the digest taken after the native Z3 check exactly as EXP-026 took it; every native check was `unsat` | `artifacts/results.json`, `leaves[*].digest_match`, `leaves[*].z3_native` |
| P2 cvc5 returns `unsat` on each of the 16 within its limit | PASS, 16 of 16 `unsat`, none `unknown`, none `sat`; 13.98 s in all, the slowest leaf `quartic-completeness` at 10.95 s (Z3 took 51.0 s in EXP-026) | `leaves[*].cvc5`, `summary.cvc5_total_seconds` |
| P3 Z3 returns `unsat` on each of the 16 exported texts | PASS, 16 of 16, 33.94 s in all | `leaves[*].z3`, `summary.z3_roundtrip_total_seconds` |
| P4 both solvers `sat` on C1 to C4 and the cvc5 model satisfies the perturbed formula under the exact evaluator | PASS on all four | `controls[*]` |

Controls (cvc5 model, evaluator verdict on the perturbed formula, evaluator verdict of the same model on the
unperturbed obligation):

| control | obligation | cvc5 model | evaluator, perturbed | evaluator, unperturbed |
|---|---|---|---|---|
| C1 | `cubic-completeness` without `X_p^3` | `p=4`, `(4,4,4)` | true | false |
| C2 | `cubic-soundness` with `(0,0,0)` added | `p=8`, `(0,0,0)` | true | false |
| C3 | `tail-c1-first` with tail `(0,3p,10p+1)` | `p=4`, `i=1` | true | false |
| C4 | `tail-quartic` with `i >= 1` | `p=4`, `i=1` | true | false |

The exported queries are stored in `artifacts/smt2/<leaf>.smt2` (controls as `C<k>-<leaf>.smt2`) with their SHA-256
in `results.json` (`smt2_sha256`).

## What this proves and does not prove

The obligations are decided `unsat` by two solvers with different quantifier procedures (Z3 model-based
quantifier instantiation, cvc5 counterexample-guided instantiation) on the certified queries. The evidence class of
Theorem 7.2 stays machine-verified [MV], now by two solvers. No proof object is checked and the soundness of both
solvers is a premise, so the theorem does not become derived [D]. The experiment changes no claim of EXP-026.

## Adversarial-validation record

- Route 1, "the rebuilt queries are not the certified ones". The first driver run computed the digest before the
  native check and found 5 of 16 mismatches (`quartic-soundness`, `tail-c1-first`, `tail-c1-last`,
  `tail-c2-last`, `tail-c3-last`). Cause (reproduced by hashing `solver.sexpr()` before and after `check()` on `tail-c1-first`): EXP-026 hashes `solver.sexpr()` after
  `solver.check()`, and for those leaves the check renames the let-bound subterms of the printed text, so the text
  differs while the formula does not. The run was repaired to take the digest after the same native check (and to
  record the digest before it, `query_sha256_before_check`); then 16 of 16 match. The first run is not the
  reported one.
- Route 2, "cvc5 cannot say `sat` here". The four controls: cvc5 answers `sat` with a model on all four.
- Route 3, "the evaluator accepts anything". The evaluator is not a solver: it parses the exported text with its own
  s-expression parser and enumerates the bounded quantifiers; it raises on an unbounded quantifier (unit test). The
  same model that satisfies a perturbed formula is rejected on the unperturbed obligation in all four controls
  (last column above).
- Route 4, "the export is faulty". Z3 decides the exported text `unsat` on all 16 (P3); on the one leaf
  (`cubic-soundness`) whose `to_smt2` text differs before and after the native check, cvc5 also returns `unsat` on
  the text from before the check.
- A defect found and fixed in the instrument: Z3's export ends with `(check-sat)`, which cvc5's parser executes
  while reading, so a first timing showed 0.00 s; the driver now skips that command and times `checkSat` alone
  (times above are the repaired ones).

## Consequences for the papers

The curvilinear fiber-cone paper can state that the sixteen obligations of Theorem 7.2 were decided by two
independent solvers (Z3 4.16.0 and cvc5 1.4.2) on identical queries, with the controls, and keep the [MV] class;
it must not call the result proved by a checked certificate. The hand proof by case analysis over the eleven blocks
(audit plan item 2a) remains the only route to [D] and is not attempted here.

## How could this be wrong?

- Both solvers could share a wrong reading of the SMT-LIB text; the exact evaluator and the controls test the
  reading only on four `sat` instances, not on the 16 `unsat` ones (an `unsat` has no model to check).
- The obligations encode Theorem 7.2 through EXP-026's formulas; an error in that encoding (for example a wrong
  candidate family) would be shared by every solver. EXP-026's finite sweep up to `p = 300` is the independent
  check of the encoding, not of this experiment.
- A solver bug in quantified linear arithmetic would have to coincide in two unrelated implementations.
- cvc5 ran with default options and without proof production; an `unsat` answer without a proof is a claim about
  the solver, not a checked proof.
