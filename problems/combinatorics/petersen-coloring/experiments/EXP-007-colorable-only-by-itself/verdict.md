# EXP-007 verdict - CONFIRMED for both 52-vertex counterexamples: they are colorable only by themselves

Date: 2026-09-19 (runs 2026-09-18 and 2026-09-19). Hypothesis committed at `af266d02` before any
run; addenda 1 to 6 each committed before the runs they govern (method, reduction lemmas, scope
extension, tooling, the two forms of the statement, portfolio and post-hoc checks). Runners
`run_inc.py`, `run.py`, `certify_existing.py`, `portfolio_certify.sh`, `agreement.sh`, `run_p0.py`;
encoder `code/pcclib/hcolor.py`. Artifacts under `artifacts/`; formulas and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-007/`. Theory:
`context/2026-09-18-hcoloring-reduction-lemmas.md`.

## Result

| graph | target orders refuted with verified proofs | undecided |
|---|---|---|
| `G52` (52 vertices) | 2, 4, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50 | 6 to 22 |
| `G52b` (52 vertices) | 40, 42, 44, 46, 48, 50 | 2 to 38 |
| `G68` (68 vertices) | 62, 64, 66 | 2 to 60 |

Every refutation is a DRAT proof accepted by drat-trim on the final formula (base plus the attach
clauses; no instance needed a lazily learned cut). Proof sizes reach 2.4 GB (`G52b`, order 40,
solved by the default configuration of the portfolio in 4,421 s and checked in 5,196 s).

Unconditional statement: for each listed order `k`, no loopless cubic graph on `k` vertices colors
the graph with a vertex map of kind (O), (E0) or (E1); by the corollary of the reduction lemmas
these are the only kinds, so no connected bridgeless cubic graph of that order colors it.

Conditional statement (on Observation 9 of arXiv:2608.10028v3: every bridgeless cubic graph on at
most 38 vertices has a Petersen coloring). A graph that colors a counterexample is a
counterexample, and a counterexample with parallel edges yields a smaller one (suppress the digon;
the two edges of the 2-edge cut around it carry equal labels in any Petersen coloring). So only
target orders from 40 to `n - 2` can occur:

- `G52` and `G52b` are colorable only by themselves: both belong to `H_3`.

This answers the question of arXiv:2608.10028v3, Section 5.4, for both of their 52-vertex
counterexamples. For `G68` the orders 40 to 60 are open.

Predictions:

| prediction | outcome |
|---|---|
| P1 (controls) | PASS: `K4` and the prism colored by smaller graphs; the Petersen graph and the flower snarks refuted at the expected orders; 21 of 21 control instances agree between the reduced and the unreduced encodings |
| P2 (every even order refuted for `G52`) | PASS in the conditional form and for 16 of the 25 orders unconditionally; the orders 6 to 22 hit the 6-hour limit |
| P3 (checker and proofs) | PASS: every SAT control accepted by the independent checker, every UNSAT verified by drat-trim |
| P0 (addendum 3: the two graphs added from House of Graphs are counterexamples) | PASS: no Petersen coloring and no normal 5-edge-coloring for `G52b` and `G68`, four verified proofs |

## What made it work

Attempt 1 (the unknown target with a free part, connectivity and bridge cuts learned lazily)
learned about 2,000 cuts per order in 35 minutes and decided nothing. Two lemmas
(`context/2026-09-18-hcoloring-reduction-lemmas.md`) remove the free part: all fibers of the vertex
map have the same parity, and unused target vertices reduce to at most one by the splitting lemma.
With them every decided order was refuted with no lazy cut at all, and the reduced and unreduced
encodings agree on all 21 controls.

## Adversarial validation record

- The reduced encoding is compared with the unreduced one on 21 control instances (`K4`, the
  prism, the Petersen graph, the flower snarks `J3` and `J5`, every even order below their own).
- Controls in both directions: colorable graphs are colored by smaller graphs at the expected
  orders with checker-accepted targets; the Petersen graph is refuted at every smaller even order.
- The certificates do not depend on the in-process solver: the final formula is refuted by an
  external solver and checked by drat-trim.
- An orphaned driver of attempt 1 ran old code for four hours next to the rerun; no result file
  came from it (every result carries `"reduced": true` and its own certificate), and the incident
  is recorded in the hypothesis.

## How could this be wrong?

- The unconditional statement rests on drat-trim and on the two reduction lemmas, which have
  full proofs on file; the conditional statement adds Observation 9 of v3, whose 12 CPU-year
  computation is not reproduced here.
- Orders 6 to 22 of `G52`, 2 to 38 of `G52b` and 2 to 60 of `G68` are undecided; they matter only
  for the unconditional form.
