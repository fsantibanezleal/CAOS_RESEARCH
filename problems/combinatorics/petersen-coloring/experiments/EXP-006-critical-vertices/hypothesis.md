# EXP-006 - critical vertices and edges: the exact Petersen defect by designated relaxation

Declared 2026-09-03 before experiment code was run. Phase PC-P4 (continuation of EXP-004).
Backlog PCB-006.

## Question

EXP-004's defect ladders stalled at bound 1 under the 30-minute cap because the sequential
counter lets the solver choose which unit to relax. Here the relaxed unit is designated: for
each vertex `v` of `G` (respectively each edge `e`), decide whether `G` has a map
`E(G) -> E(P)` whose star condition fails at most at `v` (respectively a proper 5-edge-coloring
that is normal everywhere except possibly at `e`). Which vertices (edges) are critical in this
sense? If any exists, the P-defect (normal-5 defect) is exactly 1.

## Fixed objects

`G52`, `G112`, `H112`. Encodings: `petersen_coloring` with the pair constraints at the
designated vertex removed (variant `relaxed_vertex`), and `normal_coloring(k=5)` with the
normality clauses of the designated edge removed (variant `relaxed_edge`). Symmetry breaking
as in EXP-001 is valid for the relaxed instances (edge-transitivity of `P` is unaffected).
Checkers: `petersen_defect` must return exactly 1 with the bad vertex equal to the designated
one (0 is impossible by EXP-001); `normal_defect` likewise.

Order: the vertices of `G52` first (52 Petersen instances, seconds each), then the 16 non-`F`
vertices of `G112` and `H112` (EXP-005's packing found 12 disjoint copies of `F` and 16 free
vertices in each 112-vertex graph), then the remaining 96 vertices of each. Edges: the 24 edges
incident with the free vertices of each 112-vertex graph and all 78 edges of `G52`; the
normal-5 instances of the 112-vertex graphs cost about 20 minutes each when UNSAT, so the full
edge sweep of the 112-vertex graphs is budgeted separately.

## Falsifiable predictions

- P1: `G52` has at least one critical vertex; therefore its P-defect is exactly 1. Committed
  expectation: the critical vertices include the four free vertices.
- P2: `G112` and `H112` have at least one critical vertex among their 16 free vertices; P-defect
  exactly 1. Committed expectation: the four vertices of the final claw (the last connector of
  `G = 3L + C`) are critical.
- P3: the set of critical vertices is a proper subset of `V(G)`: some vertex is not critical
  (relaxing it leaves the graph uncolorable), decided with a verified proof for at least one
  vertex of `G52`.
- P4: `G52` has a critical edge, so its normal-5 defect is exactly 1.
- P5: a corrupted witness (the relaxed-vertex coloring with a swap at a non-relaxed vertex) is
  rejected by the checker, and the bound-0 instance of `G52` is UNSAT again (reproduction).

## One-sidedness

Every SAT answer is a witness (defect exactly 1 at the designated unit); every UNSAT answer with
a verified proof says the designated unit alone cannot absorb the obstruction. A TIMEOUT leaves
that unit undecided.

## Premise dependencies

EXP-001 CONFIRMED (bound 0 UNSAT, so defect at least 1).

## Invariant-first note

The free vertices are the natural first candidates (the obstruction lives in the connectors in
Jooken's proof).

## Compute budget and kill criterion

CPU only. 10 minutes per Petersen instance, 30 minutes per normal-5 instance; whole run under
8 hours; undecided units are listed.

## Verdict rules

- CONFIRMED if P1, P2, P4, P5 pass and P3 is decided.
- REFUTED if every vertex of some graph is non-critical with verified proofs (P-defect at least
  2 for that graph).
- INCONCLUSIVE if the deciding instances time out.

## Addendum declared 2026-09-03 13:00, before any pair instance ran

The first single-vertex relaxations of `G52` (its four free vertices and the first vertices of
the copies of `F`) are UNSAT with verified proofs, so P1 is heading to REFUTED: no single vertex
of `G52` absorbs the obstruction. A new, separately declared question follows, tested by the
runner `run_pairs.py` after the single sweep completes:

- P6: is the P-defect of `G52` exactly 2? For every unordered pair `{u, v}` of vertices, decide
  whether an edge map exists whose star condition fails only at `u` and `v` (encoding
  `petersen_relaxed_vertices` with both pair-constraint sets removed; symmetry breaking on an
  edge disjoint from both). If some pair is SAT with a checker defect of exactly 2, the
  P-defect is 2 and the critical pairs are listed; if every pair is UNSAT with verified proofs,
  the P-defect is at least 3 (and the budget decides whether triples are attempted). Committed
  expectation: some pair is SAT; the critical pairs are not confined to the free vertices.
- Budget: 1,326 Petersen instances of `G52` at about 2 to 10 seconds each; cap 10 minutes per
  instance; whole sweep under 4 hours. The 112-vertex graphs are out of scope for pairs in this
  round (6,216 instances at about a minute each).

## Addendum 2 declared 2026-09-03 13:10, before the 112-vertex pair instances ran

Result so far: all 52 single relaxations of `G52` UNSAT (verified), all 1,326 pair relaxations
SAT with checker defect exactly 2. The single-vertex outcome has a proof for every cubic graph
(context note `2026-09-03-defect-parity-lemma.md`: the bad set's label vector sum lies in the
cut space of `P`, and an odd cut of size 1 or 3 in `P` is a star). Therefore P2 (a critical
single vertex in the 112-vertex graphs) is REFUTED by theorem, and the 112-vertex single sweep
is stopped as pointless after vertex 8 of `G112` (its result, UNSAT, is an instance of the
lemma). Redirected questions:

- P7: the 120 pairs of free vertices of `G112` (the 16 vertices outside the twelve disjoint
  copies of `F`): which are critical? If any is SAT the Petersen defect of `G112` is exactly 2.
  Committed expectation: some free-vertex pair is critical. Budget: 10 minutes per instance.
- P8: the normal-5 defect of `G52` by single-edge relaxation over all 78 edges (`normal5
  relaxed edge`): if any is SAT the normal-5 defect is exactly 1; if all are UNSAT with verified
  proofs the defect is at least 2. No committed expectation (the parity argument does not
  transfer). Budget: 30 minutes per instance.
