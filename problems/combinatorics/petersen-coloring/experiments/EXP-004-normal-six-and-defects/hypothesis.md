# EXP-004 - normal 6-edge-colorings and exact normality defects of the counterexamples

Declared 2026-09-03 before experiment code was run. Phase PC-P4. Backlog PCB-005, PCB-006.

## Question

For `G112`, `H112`, `G52`: does each admit a normal 6-edge-coloring, and a strong normal
6-edge-coloring (every edge rich)? What is the exact normal-5 defect (minimum number of edges
that are neither poor nor rich over all proper 5-edge-colorings) and the exact P-defect (minimum
number of vertices whose star is not mapped onto a star of `P` over all maps `E(G) -> E(P)`)?

## Motivation

Conjecture 6 of Goedgebeur-Jooken-Macajova-Mattiolo-Mazzuoccolo (attributed to Samal; stated in
Mazzuoccolo-Mkrtchyan 2020): every bridgeless cubic graph has a normal 6-edge-coloring `[V,
GJMMM Section 5]`; every simple cubic graph has a normal 7-edge-coloring `[V, Mazzuoccolo-
Mkrtchyan 2020 abstract]`. GJMMM verified a strong normal 6-edge-coloring of one 112-vertex
graph only. The defects quantify how far the first counterexamples are from colorable; no
source reports them (context dossier section 5). The normal chromatic index of each target is
therefore 6 or 7.

## Fixed objects

The three graphs of EXP-001. Encodings: `normal_coloring(k=6)`, `normal_coloring(k=6,
strong=True)`, `normal_coloring(k=5, defect_bound=d)` for increasing `d`, and
`petersen_coloring(defect_bound=d)` for increasing `d` (no symmetry breaking in defect mode).
Checkers: `normal_defect`, `is_strong_normal`, `petersen_defect`, all reading only the graph.

Controls: the Petersen graph (normal 5 exists, so normal-5 defect 0, P-defect 0; strong normal
6 status recorded), `J5` (defects 0), and the non-colorable targets themselves at defect bound
0, which must reproduce the EXP-001 UNSAT results.

## Falsifiable predictions

- P1: controls: Petersen and `J5` have normal-5 defect 0 and P-defect 0 (SAT at bound 0 with
  validated witnesses); every target at bound 0 is UNSAT with a verified proof (both
  encodings), reproducing EXP-001.
- P2: each target admits a normal 6-edge-coloring (validated witness); hence the normal
  chromatic index of each is exactly 6.
- P3: each target admits a strong normal 6-edge-coloring (validated witness); committed
  expectation: yes for all three (GJMMM found one for a 112-vertex graph).
- P4: the normal-5 defect of each target is decided exactly: the least `d` with SAT (validated
  witness with exactly `d` or fewer bad edges) after verified UNSAT at `d-1`. Committed
  expectation: 1 for every target (a single bad edge; no prior evidence).
- P5: the P-defect of each target is decided exactly, same protocol. Committed expectation: 1
  for every target.
- P6: corrupted witness: a normal 6-edge-coloring with two adjacent edges swapped is rejected
  by `check_proper` or `normal_defect`.

## One-sidedness

SAT gives explicit witnesses; UNSAT with verified proofs gives exact lower bounds; a TIMEOUT
leaves the corresponding value as an interval and the verdict partial. A P2 UNSAT would refute
Conjecture 6 and escalate.

## Premise dependencies

EXP-001 CONFIRMED (bound-0 instances are UNSAT).

## Invariant-first note

Normal 6 on `G112` is the first call (it decides the normal chromatic index).

## Compute budget and kill criterion

CPU only. Wall cap 30 minutes per SAT call (defect instances carry sequential counters and may
be slow; the bound ladder stops at the first SAT), 60 minutes per proof check, whole run under
6 hours. A capped instance is INCONCLUSIVE and recorded as an interval.

## Verdict rules

- CONFIRMED only if P1, P2, P6 pass and P3, P4, P5 are decided (any value).
- REFUTED if any target normal-6 instance is UNSAT with a verified proof (escalates).
- INCONCLUSIVE if any target hits its cap.
