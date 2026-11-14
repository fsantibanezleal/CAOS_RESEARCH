# EXP-069 hypothesis: the EXP-026 Presburger certificate decided by a second solver

Date: 2026-11-14. Frozen before any code of this experiment is written or run.

## Why

The curvilinear fiber-cone paper (`manuscripts/huneke-wiegand/curvilinear-fiber-cones`, v0.04) rests the completeness
and soundness of the cubic and quartic boundary of its grevlex staircase (Theorem 7.2), for every `p >= 4`, on the 16
Presburger obligations of EXP-026 `symbolic_certificate.py`, each answered `unsat` by Z3 4.16.0 with no checked proof
object (EXP-026 `proof.md`, "Trust boundary"). The independent audit of 2026-11-10 (CAOS_MANAGE
`wip/caos-research/msaudit-hw-other-2026-11-10.md`, D1 finding 1 and plan item 2b) asks for an independent cross-check by
a second solver. This experiment is that cross-check; it changes no claim of EXP-026.

## Instrument

- The obligations are rebuilt by EXP-026's own code (`symbolic_certificate.py`, imported, not copied), one obligation per
  fresh process, exactly as EXP-026 ran them, so that fresh-variable names and the query text coincide.
- Identity of the queries: the SHA-256 of `solver.sexpr()` of each rebuilt obligation (with `p >= 4`) is compared with
  `query_sha256` of the same leaf in EXP-026 `artifacts/symbolic-certificate.json`.
- Export: `z3.Solver.to_smt2()` of the same solver (SMT-LIB 2, linear integer arithmetic with quantifiers), stored per
  leaf under `artifacts/smt2/` with its SHA-256.
- Second solver: cvc5 1.4.2 (Python API, PyPI `cvc5`), logic `LIA`, a fresh solver per leaf, time limit 600 s per leaf,
  default options otherwise. cvc5 decides quantified linear integer arithmetic by counterexample-guided quantifier
  instantiation; it shares no code with Z3.
- Round trip: Z3 4.16.0 also decides the exported SMT-LIB text (parsed back with `z3.parse_smt2_string`), so that a
  faulty export cannot pass silently.

## Predictions

- P1 (same obligations): the 16 rebuilt query digests equal the 16 stored digests of EXP-026.
- P2 (second solver): cvc5 returns `unsat` on each of the 16 exported obligations within its time limit.
- P3 (faithful export): Z3 returns `unsat` on each of the 16 exported texts.
- P4 (the solvers can say `sat` here): on each of the following perturbed obligations, built with the same code and
  exported the same way, both cvc5 and Z3 return `sat`, and the model returned by cvc5, substituted into the perturbed
  formula and evaluated by an exact integer evaluator written for this experiment (not by either solver), satisfies it:
  - C1: `cubic-completeness` with the single family `X_p^3` removed from the candidate set (that monomial is a minimal
    boundary element, so a counterexample exists);
  - C2: `cubic-soundness` with the triple `(0,0,0)` added to the candidate set (`X_0^3` is standard, hence not a
    boundary element);
  - C3: `tail-c1-first` with the declared tail `(0, 3p, 10p)` replaced by `(0, 3p, 10p+1)` (no longer weight-equal);
  - C4: `tail-quartic` with its index range widened to include `i = 1` (the tail offset `6p-1` is not in `G_p`).

## What PASS and FAIL prove

- PASS: the 16 obligations behind Theorem 7.2 are decided `unsat` by two independent solvers with different quantifier
  procedures, on queries shown identical to the certified ones, and both solvers return verified `sat` answers on four
  perturbations. The evidence class of the theorem stays machine-verified [MV], now by two solvers; no proof object is
  checked, so it does not become derived [D].
- FAIL of P2 by a `sat` answer: the cvc5 model is a candidate counterexample to Theorem 7.2; it is checked by the exact
  evaluator and by the EXP-026 finite sweep at the corresponding `p`, and the paper's claim is suspended until resolved.
- `unknown` or time-out on any leaf: that leaf is reported as not cross-checked; nothing is claimed for it.
- FAIL of P1 or P3: the export or the rebuild is wrong; the run is invalid and is repaired before any reading.

## Budget

At most 16 x 600 s for P2 plus the controls; the Z3 times of EXP-026 were 62.5 s in all (51.0 s for
`quartic-completeness`). One process at a time; no WSL.
