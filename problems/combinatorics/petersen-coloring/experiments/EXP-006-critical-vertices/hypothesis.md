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
