# EXP-011 - is every adjacent vertex pair critical in the new 102-vertex counterexamples?

Declared 2026-09-18 before any experiment code was run. Round 2. Backlog PCB-027. Research lines
PCR-7 and PCR-10.

## Question

All five known counterexamples are universally 2-critical: for EVERY pair of vertices there is an
edge map into `E(P)` whose only bad vertices are the two of the pair (EXP-006, EXP-008). This is
exactly what blocks the search for a cyclically 4-edge-connected cubic graph of Petersen defect at
least 3 (threshold proposition, `context/2026-09-18-defect-unbounded.md`): if `G` is universally
2-critical, then for every vertex set `X` with at least two vertices the multipole `G - X` is
Petersen colorable (a witness for a critical pair inside `X` restricts to it), so the only
non-colorable pieces one can cut from `G` have 2 or 3 dangling edges, and graphs assembled from
such pieces have cyclic edge connectivity at most 3.

Conversely, a counterexample `G` with a NON-critical pair of adjacent vertices `u, v` gives a
non-colorable 4-pole `G - {u, v}` (a coloring of the 4-pole, completed by any labels on the five
edges at `u` and `v`, has bad set inside `{u, v}`; by the parity theorem the bad set would be
exactly `{u, v}`, that is, the pair would be critical). Copies of such a 4-pole force one bad
vertex each wherever they are embedded.

EXP-010 produced ten new counterexamples, the dot products `D = (G52 - e1 - e2) + (G52 - {u, v})`
on 102 vertices (no Petersen coloring, checked proofs; defect exactly 2). Are all their ADJACENT
pairs critical?

## Fixed objects

The ten dot products of EXP-010 addendum 2 (`artifacts/dot-products.json` there, rebuilt by
`EXP-010/run_dot.py:dot_product` from `G52`). For each, the 153 adjacent pairs.

## Falsifiable predictions

- P1 (control): for `G52` the 78 adjacent pair relaxations are SAT (reproduces EXP-006 on the
  adjacent pairs with this runner).
- P2 (the question): committed expectation, moderate confidence (three quarters): every adjacent
  pair of every dot product is critical. A pair that is UNSAT with a verified proof REFUTES the
  expectation and yields a non-colorable connected 4-pole with 100 vertices; the experiment then
  checks its cyclic joins (order `100 t`) for cubicity and cyclic 4-edge-connectivity on the
  instance `t = 3`, and the consequence for statement (e) of Mattiolo, Mazzuoccolo, Mkrtchyan is
  recorded.
- P3: every SAT witness has exactly the two relaxed vertices bad (independent checker).

## One-sidedness

SAT: explicit witness checked from the graph. UNSAT: DRAT proof checked by drat-trim. Timeouts
decide nothing and are listed.

## Premise dependencies

EXP-010 addendum 2 (the dot products are counterexamples); the parity theorem; the relaxed
encoder of EXP-006.

## Invariant-first note

No invariant is known to decide pair criticality; the cut-space class of the two bad vertices must
agree (checked on stored witnesses), which does not exclude any pair a priori.

## Compute budget and kill criterion

CPU only, six workers, 10 minutes per pair, 8 hours overall, started only after EXP-010 has
released its workers.

## Verdict rules

CONFIRMED if P1, P3 pass and P2 is decided for all ten graphs (either direction, a refuted
expectation preserved); INCONCLUSIVE for graphs with undecided pairs.
