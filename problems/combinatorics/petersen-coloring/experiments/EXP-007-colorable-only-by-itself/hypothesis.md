# EXP-007 - is the 52-vertex counterexample colorable only by itself? (and a quotient route to smaller counterexamples)

Declared 2026-09-18 before experiment code was run. Round 2. Backlog PCB-017.

## Question

For graphs `G`, `H`, an `H`-coloring of `G` is a map `f : E(G) -> E(H)` with adjacent edges
receiving distinct images and `f(d_G(v)) = d_H(u)` for some vertex `u` of `H`, for every vertex
`v` of `G` (Ma, Mattiolo, Steffen, Wolf, Combinatorica 45 (2025), Article 16, arXiv:2305.08619,
Section 1 `[V]`; graphs may have parallel edges but no loops `[V, their Section 2]`). `H_3` is
the unique inclusion-wise minimal set of connected bridgeless cubic graphs coloring every
connected bridgeless cubic graph, and by their Theorem 3.7 `[V]` the following are equivalent
for a connected bridgeless cubic `G`: `G` is in `H_3`; the only connected bridgeless cubic graph
coloring `G` is `G` itself; `G` cannot be colored by a bridgeless cubic graph of smaller order.

Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo, Ulyanov (arXiv:2608.10028v3, 2026-09-11,
Section 5.4 `[V]`) ask whether their 52-vertex counterexamples are colorable only by
themselves, and note that the question is tied to whether they are smallest counterexamples.
Decide it for `G52`: for each even `k < 52`, is there a connected bridgeless cubic multigraph
`H` on `k` vertices with an `H`-coloring of `G52`?

## Why both outcomes matter

- If some `H` exists, then `H` has no Petersen coloring either (the relation "colors" is
  transitive, so `P` coloring `H` would give `P` coloring `G52`): `H` is a counterexample to the
  Petersen coloring conjecture on fewer than 52 vertices, improving the upper bound of the open
  window `[40, 52]` of v3 Problem 8. It would be certified independently by the EXP-001 route.
- If no `H` exists for any even `k < 52`, then `G52` belongs to `H_3`: it is colorable only by
  itself. This answers the v3 Section 5.4 question for this graph with checkable certificates.

## Method

One CNF per target order `k`, with the target multigraph unknown:

- target structure: each target vertex `i < k` has three slots; a perfect matching `p` on the
  `3k` slots with no pair inside one vertex (no loops; parallel edges allowed) is the edge set
  of a cubic multigraph `H`;
- the map: `x(v,i)` (vertex `v` of `G` is sent to `i`), and at every `v` a bijection `z` between
  its three incident edges and the three slots of its image, so the star of `v` maps onto the
  star of `i` with distinct images;
- consistency along each edge `uv` of `G`: the slot used at `u` and the slot used at `v` are the
  same slot or are matched by `p` (the same edge of `H` seen from either end);
- symmetry breaking: target vertices are numbered in order of first use (vertex 0 of `G` goes
  to 0; class `i+1` is first used only after class `i`), and the founder of each class fixes the
  slot order; unused target vertices are allowed (colorings need not be surjective) and sit at
  the end;
- connectedness and bridgelessness of `H` are enforced lazily: a model whose `H` is
  disconnected or has a bridge yields the sound clause "some further slot pair crosses the
  offending side", and the solve repeats.

A SAT answer is decoded and re-verified by an independent checker (`H` cubic, loopless,
connected, bridgeless; `f` an `H`-coloring from the definition), and `H` is then refuted for
Petersen colorability by the EXP-001 encoding with a checked proof (it must be a
counterexample). An UNSAT answer carries a DRAT proof checked by drat-trim; the lazily learned
clauses are logged with the cut that justifies each.

## Fixed objects

`G52` (`data/gjmmm-52.edgelist`). Controls: the Petersen graph with every even `k < 10` (must
be UNSAT: by Kardos, Macajova, Zerafa as cited in v3 Section 5.4 `[U, cited through v3]` the
Petersen graph is colored only by itself or by graphs with a bridge); the flower snark `J5`
with `k = 10` (must be SAT, since `J5` has a Petersen coloring, and the decoded `H` must pass the
checker); `K4` with `k = 2` (SAT: the three parallel edges; every 3-edge-colorable graph is
colored by it).

## Falsifiable predictions

- P1: controls behave as stated.
- P2 (the question): committed expectation, moderate confidence: every even `k` from 2 to 50 is
  UNSAT for `G52`, so `G52` is in `H_3`. A SAT instance REFUTES the expectation and produces a
  new smallest known counterexample.
- P3: for every SAT instance (controls included) the independent checker accepts the decoded
  pair `(H, f)`; for every UNSAT instance drat-trim verifies the proof.

## One-sidedness

UNSAT for all `k` with verified proofs is a theorem about `G52` (membership in `H_3`),
unconditional on any census. SAT is a positive certificate. TIMEOUT decides nothing for that
`k`; the verdict then reports exactly which orders are decided.

## Premise dependencies

- Theorem 3.7 of Ma-Mattiolo-Steffen-Wolf `[V]` (read in the arXiv version).
- EXP-001 CONFIRMED (`G52` has no Petersen coloring), used only to interpret a SAT outcome.
- The v3 lower bound 40 is NOT used: all even orders from 2 are tested here.

## Invariant-first note

A covering-type count already excludes foldings without identified adjacent vertices (they
would be coverings, forcing `k` to divide 52 with quotient at least 2, so `k <= 26`), but
identified adjacent vertices are allowed in `H`-colorings, so no single invariant decides the
question.

## Compute budget and kill criterion

CPU only, one process per `k` in parallel (at most 12 at a time). Wall cap 6 hours per `k`;
whole experiment 24 hours. Each instance logs flushed progress and writes its result JSON on
completion; undecided orders are listed.

## Verdict rules

- CONFIRMED (of P2) if P1 and P3 pass and every even `k` from 2 to 50 is UNSAT with a verified
  proof.
- REFUTED (of P2) if some `k` is SAT with a checker-accepted `(H, f)` and `H` is refuted for
  Petersen colorability with a verified proof: a new counterexample on `k` vertices.
- INCONCLUSIVE for the orders that hit the cap.
