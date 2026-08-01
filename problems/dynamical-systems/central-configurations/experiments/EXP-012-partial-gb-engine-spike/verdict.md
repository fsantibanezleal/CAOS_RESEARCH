# EXP-012 - Verdict: ENGINE HYPOTHESIS CONFIRMED, UNION BOUND LANDS INFORMATIVE-WEAK AT DIM <= 7 (2026-08-01; the EXP-011 wall was an engine artifact; the instrument now works and the menu, not the engine, is the remaining dial)

Hypothesis: `hypothesis.md` (declared before any run). Runner: `run.py`.
Artifacts: `artifacts/` (all Singular scripts and outputs, times.json,
union-leads.json, results.json, run log).

## Outcomes against the declared predictions

| Prediction | Outcome | Facts |
|---|---|---|
| P1a (toy three-engine control) | PASS | sympy QQ, Singular QQ and msolve mod 1073741827 agree on the leading ideal {x^2, y^2} |
| P1b (exact reproduction of EXP-011's job 3 against a grevlex-correct reference) | PASS | Singular's 16 leads match the fresh sympy recomputation exactly; Singular needed under one second where sympy needed about 93 |
| P2 (A/B on the identical 15 archived subideals, threshold >= 12 of 15 at 120 s) | CONFIRMED, 12/15 | the twelve completers each ran in 0.4 to 1 second (sympy baseline: one completer at about 100 s), a speedup above two orders of magnitude on identical inputs; subideals 1, 4 and 7 capped even for Singular |
| P3 (the lighter 16-subideal menu, threshold >= 12 of 16) | CONFIRMED, 16/16 | every local-Dziobek triple, every adjacent-pair subideal and the {Cayley-Menger, saturation} subideal completed in at most one second |
| P4 (union staircase bound, success threshold <= 4) | INFORMATIVE-WEAK per the declared scale | 466 distinct leading monomials from 28 completing subideals give d_pgb = 7 (witness independent set of size 7); the declared success value 4 was not reached, and the declared consequence (menu grows to triples and mixed pairings under a new declaration) applies |

## What is now established

1. **The EXP-011 wall was the engine, not the mathematics.** Identical jobs,
   identical caps: sympy 1 of 15, Singular 12 of 15 with the completers at
   sub-second cost. The Dias-Pan precedent transfers to our stack exactly as
   their paper suggested.
2. **The first sound deterministic bound of the lane:** dim <= 7 for the
   n = 5 spatial Dziobek cut in the torus, from grevlex-correct QQ leading
   monomials only (the EXP-011 harvest was vacuous AND order-inconsistent;
   this one is neither). Still 3 away from the expected 4; the gap is menu
   coverage, and with sub-second subideals a much larger menu costs minutes.
3. **A structural cost pattern worth recording:** the three Singular-capping
   subideals (1, 4, 7) are all _bc pairings of their quadruples (1234, 1235,
   1245), while the _bc pairings of 1345 and 2345 completed; the hard cases
   share the body pair {1, 2} inside the pairing structure. Unexplained,
   recorded as data for the menu design.
4. **The control discipline paid for itself on its first outing:** the P1b
   exact-reproduction control caught the lex-vs-grevlex harvester bug in its
   very first run (first launch failed controls and stopped; the correction
   set is commit 20d7b94), before any bound could be trusted.

## Soundness notes

- All verdict-carrying leading monomials come from Singular over QQ with
  degrevlex order and short=0 output; msolve's mod-p basis mode was used only
  in the toy control, per the screen-only rule declared in the hypothesis.
- The union-bound argument needs only membership of each monomial in the full
  ideal's grevlex leading-term ideal, which holds for leading monomials of
  ANY subideal's grevlex basis over the same ring; fewer completing subideals
  weaken but cannot falsify the bound.
- Caps enforced by `timeout` inside WSL; the 131 s wall readings on capped
  cells are the 120 s cap plus WSL overhead.

## Consequences (per the declared ladder)

1. CCB-037 v2 is VALIDATED as the lane's deterministic upper-bound
   instrument, with Singular as the workhorse and sympy as the
   control-and-verification layer.
2. The declared follow-up (menu growth: triples of products, mixed pairings,
   pairs WITH Cayley-Menger now that subideals are sub-second) is EXP-013
   territory, hypothesis first.
3. The n = 6 symmetric-strata campaign (CCB-036; 9-variable quotients) is
   UNBLOCKED on the engine side: the workload class that walled in sympy is
   sub-second in Singular, exactly what the Dias-Pan precedent predicted for
   systems of this size.
4. CCB-034 (witness sets) remains the lower-bound route; nothing here
   produces dimension lower bounds.
