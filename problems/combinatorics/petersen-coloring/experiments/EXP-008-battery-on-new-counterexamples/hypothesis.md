# EXP-008 - the full invariant battery on the second 52-vertex and the 68-vertex counterexamples

Declared 2026-09-18 before the battery code was run on these graphs. Round 2. Backlog PCB-020.

## Question

EXP-001 to EXP-006 computed, for `G112`, `H112` and `G52`: certified non-colorability, perfect
matching covers and index, 5-cycle double covers, nowhere-zero flows, oddness, resistance, normal
chromatic index, Petersen defect with universal 2-criticality, and the normal-5 defect. House of
Graphs entries 57278 (`G52b`, the second 52-vertex counterexample of arXiv:2608.10028v3) and 57280
(`G68`) became retrievable on 2026-09-18. What are the same invariants on these two graphs?

Goedgebeur et al. (v3, 2026-09-11) report for all five graphs: Berge-Fulkerson covers, perfect
matching index at most 4, 5-cycle double covers, strong normal 6-edge-colorings, proper
5-edge-colorings with exactly two abnormal edges. Those items are reproductions here. Not reported
there: oddness, resistance, flows, the Petersen defect and pair criticality, the lower bound of the
normal-5 defect.

## Fixed objects

`data/gjmmmu-52-b.edgelist` (digest `d30a423a...1477`), `data/hog-57280-68.edgelist` (digest
`19c7c22a...5ab2`). Structure already measured when the files were registered: cubic, simple,
girth 5, edge connectivity 3, no cycle-separating cut of size below 4. P0 of EXP-007 (no Petersen
coloring, no normal 5-edge-coloring, checked proofs) is the certification step and is cited, not
repeated.

## Falsifiable predictions (committed)

- P1 (covers): both graphs have a Berge-Fulkerson cover, a Berge cover by five perfect matchings,
  a Fan-Raspaud triple and a cover by four perfect matchings; perfect matching index exactly 4.
- P2 (cycles and flows): both have a 5-cycle double cover and a nowhere-zero 5-flow; neither has a
  nowhere-zero 4-flow (they are snarks; this is a consistency check of P0).
- P3 (oddness and resistance): `G52b` has oddness 2 and resistance 2, by analogy with `G52`
  (moderate confidence). `G68`: oddness 2 and resistance 2 (low confidence; the 112-vertex graphs
  have 4 and 3).
- P4 (normal 6): both have normal and strong normal 6-edge-colorings; normal chromatic index 6.
- P5 (Petersen defect): both have Petersen defect exactly 2, and EVERY vertex pair is critical
  (1,326 pairs for `G52b`, 2,278 for `G68`), as found for the first three graphs (moderate
  confidence; a non-critical pair would be the first known and refutes the expectation).
- P6 (normal-5 defect): both have a proper 5-edge-coloring with exactly two abnormal edges. Lower
  bound 2 by single-edge relaxations over one representative per edge orbit of the listed
  automorphisms, 15 minutes per edge; decided only if every representative is refuted with a
  verified proof.

## One-sidedness

Witnesses are re-verified by the `pcclib.checkers` functions from the graph alone; refutations
carry DRAT proofs checked by drat-trim. An undecided instance is reported as undecided.

## Premise dependencies

Encoders and checkers of EXP-002, EXP-003, EXP-004, EXP-006 (all CONFIRMED with controls); the
parity theorem (no map has exactly one bad vertex), which makes single-vertex relaxations
unnecessary.

## Invariant-first note

No cheaper invariant decides oddness or the pair criticality; the perfect matching index lower
bound 4 is the snark property.

## Compute budget and kill criterion

CPU only. 30 minutes per instance of P1 to P4 and P6 upper bound; 10 minutes per pair; 15 minutes
per edge representative; 8 hours overall. The battery starts when the EXP-007 runs on the 52-vertex
graphs have released the machine.

## Verdict rules

Each prediction PASS, REFUTED or UNDECIDED on its own; the experiment is CONFIRMED if P1, P2, P4
pass and P3, P5, P6 are decided (whatever their direction, with refuted expectations preserved).

## Addendum 1 (2026-09-18, 12:10): the edge-orbit stage of P6 is withdrawn

The lower bound 2 of P6 needs no computation. Mattiolo, Mazzuoccolo, Mkrtchyan (arXiv:2104.09241,
Proposition 3, read 2026-09-18 `[V]`) prove that no proper 5-edge-coloring of a cubic graph has
exactly one abnormal edge; independently, Lemma 1 of `context/2026-09-18-defect-unbounded.md`
(`pd <= ab`) with the parity theorem (`pd` is never 1) gives `ab >= 2` for every cubic graph
without a Petersen coloring `[D]`. So `ab = 2` for a counterexample as soon as a witness with two
abnormal edges exists. The edge stage was stopped after its first instances hit the 15-minute
limit on a machine saturated by EXP-007 (two TIMEOUT entries per graph, no decision, logs kept);
P6 is decided by the battery witnesses plus the cited proposition.
