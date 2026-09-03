# EXP-003 - cycle double covers, flows, oddness and resistance of the counterexamples

Declared 2026-09-03 before experiment code was run. Phase PC-P3. Backlog PCB-004.

## Question

For the certified counterexamples `G112`, `H112`, `G52`: does each have a 5-cycle double cover
(five even subgraphs covering every edge exactly twice)? A nowhere-zero 5-flow? What are their
oddness (minimum number of odd cycles in a 2-factor) and resistance (minimum number of edges
whose deletion leaves a 3-edge-colorable graph)?

## Motivation

The Petersen coloring conjecture implied the 5-cycle double cover conjecture (context dossier
section 2); the first counterexamples are its sharpest test cases. Oddness and resistance are
the standard measures of how far a snark is from 3-edge-colorability (Goedgebeur-Macajova-
Skoviera 2019 study oddness 4 with cyclic connectivity 4 `[U, title]`); the census literature
reports that the strongest cycle double cover variants hold through order 36 `[V, BGHM abstract]`.
Nowhere-zero 5-flows: Tutte's 5-flow conjecture is open in general; a nowhere-zero 4-flow of a
cubic graph is equivalent to 3-edge-colorability (classical `[U]`, used only as a control here).

## Fixed objects

The three graphs of EXP-001. Encodings from `pcclib.encoders`: `cycle_double_cover(count=5)`,
`nowhere_zero_flow(k=5)`, `nowhere_zero_flow(k=4)` (control), `oddness(bound)`,
`resistance(bound)`. Checkers: `check_cycle_double_cover`, `check_flow`,
`odd_cycles_of_two_factor`, `check_three_edge_colorable_minus`.

Controls: Petersen graph (5-cycle double cover exists: classical `[U]`, decided here; oddness 2
and resistance 2, classical `[U]`; nowhere-zero 4-flow UNSAT, 5-flow SAT), `K4` and prism
(4-flow SAT, oddness 0, resistance 0), `J5` (oddness 2, resistance 2 expected `[U]`).

## Falsifiable predictions

- P1: controls as listed; the Petersen 4-flow instance is UNSAT with a verified proof; the
  Petersen oddness-1 and resistance-1 instances are UNSAT with verified proofs.
- P2: each target has a 5-cycle double cover, decoded and checker-validated.
- P3: each target has a nowhere-zero 5-flow (validated witness); each target's 4-flow instance
  is UNSAT with a verified proof (consistent with non-3-edge-colorability from EXP-001).
- P4: oddness of each target is exactly 2: the bound-1 instance is UNSAT (verified proof; the
  value 1 is impossible for parity reasons anyway) and the bound-2 instance is SAT with a
  perfect matching whose 2-factor has exactly two odd cycles by the checker. Committed
  expectation: 2 for all three (no prior evidence).
- P5: resistance of each target is exactly 2: bound-1 UNSAT with proof, bound-2 SAT with a
  validated deletion set. Committed expectation: 2 for all three.
- P6: corrupted witness controls: a cycle double cover with one edge removed from one cycle is
  rejected; a flow with one value zeroed is rejected.

## One-sidedness

SAT answers are positive certificates; UNSAT answers with verified proofs are exact lower
bounds; TIMEOUT proves nothing. A P2 UNSAT would be a counterexample to the 5-cycle double cover
conjecture and would escalate to a dedicated follow-up before any claim.

## Premise dependencies

EXP-001 CONFIRMED (the graphs are the counterexamples; not 3-edge-colorable).

## Invariant-first note

The 5-cycle double cover instance of `G112` is the single deciding call and runs first.

## Compute budget and kill criterion

CPU only. Wall cap 30 minutes per SAT call, 60 minutes per proof check, whole run under 4
hours. A capped instance is INCONCLUSIVE; the verdict is then partial and says so.

## Verdict rules

- CONFIRMED only if P1, P2, P3, P6 pass and P4, P5 are decided (any value).
- REFUTED if a target 5-cycle double cover or 5-flow instance is UNSAT with a verified proof
  (escalates).
- INCONCLUSIVE if any target hits its cap.
