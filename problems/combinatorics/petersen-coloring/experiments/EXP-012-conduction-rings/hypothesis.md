# EXP-012 - conduction of cut-space classes by 4-poles, and rings of Petersen defect at least t

Declared 2026-09-19 before any code of this experiment was run. Round 2. Backlog PCB-029.
Research line PCR-7 (statement (e) of Mattiolo, Mazzuoccolo, Mkrtchyan).

## Theory (derived, `[D]`, recorded in `context/2026-09-19-conduction.md`)

For a pair of labels `(x, y)` of edges of `P`, the class of `1_x + 1_y` modulo the cut space of `P`
is determined by the distance `d(x, y)` in the line graph of `P`, `d` in `{0, 1, 2, 3}`: `d = 0`
gives the zero class; `d = 1` gives the class of the third edge at the common vertex; two pairs
at different distances never have the same class (a cut of weight at most 4 is empty, a star or
the four edges around an edge of `P`).

Conduction lemma. Let `M` be a 4-pole whose dangling ends are paired into connectors `{p, q}` and
`{r, s}`. In a map with every vertex of `M` good, `1_s(p) + 1_s(q) + 1_s(r) + 1_s(s)` lies in the cut
space (it is the sum of the stars of the vertices of `M`), so the two connectors carry the same
class, hence the same distance. Let `D(M)` be the set of distances realized at `{p, q}` over all
such maps (the conducted set).

Ring theorem. Let `A` and `B` be 4-poles with paired connectors and `D(A)` disjoint from `D(B)`.
In the cubic graph `R_t(A, B)` made of `t` copies of `A` and `t` copies of `B` alternating around a
cycle, each connector of a block joined by two edges to a connector of the next block, every map
into `E(P)` has at most `t` blocks without bad vertices: two consecutive good blocks would share a
connector whose distance lies in `D(A)` and in `D(B)`. Hence `pd(R_t) >= t` and, by Lemma 1 of
`context/2026-09-18-defect-unbounded.md`, `ab(R_t) >= t`.

If `A` and `B` are cyclically 4-edge-connected 4-poles and `R_3` is cyclically 4-edge-connected, then
`R_3` is a cyclically 4-edge-connected cubic graph with Petersen defect at least 3, and by
Theorem 6 (with Proposition 2 of Mattiolo et al.) statement (e) is false and their Conjecture 3
holds.

## Inputs already certified

EXP-010 (addenda 3, 4): for 282 edge pairs `(e0, e)` of `G52` the distance set at the ends of `e0`
in the 4-pole `G52 - e0 - e` is `{1}`, the distances 2 and 3 refuted with verified proofs; distance
0 is impossible because it would restore a Petersen coloring of `G52` (EXP-001). So for these
4-poles, with connectors `{a, b}` (ends of `e0`) and `{c, d}` (ends of `e`), `D(A) = {1}`.

## Question

Is there a cyclically 4-edge-connected 4-pole `B` with a pairing such that `D(B)` avoids 1?

## Candidates (fixed now)

1. `W = P - {u, v}` (`u`, `v` adjacent), three pairings: `{u1, u2} | {v1, v2}` (the two ends at
   `u` against the two at `v`), and the two crossed pairings.
2. `P - e1 - e2` for `e1`, `e2` at distance 2 and at distance 3 in the line graph, three pairings.
3. `G52 - {u, v}` for one representative of every edge orbit of `G52`, three pairings.
4. The 36-vertex 4-pole `L` of Putman's construction, extracted from `G112` as a vertex set with a
   4-edge boundary containing four copies of `F` and one claw, three pairings (only if its
   extraction is unambiguous).

## Falsifiable predictions

- P1 (control): the conducted sets of the `G52 - e0 - e` 4-poles used as `A` are `{1}`
  (re-derived here with the new encoder for the first five such pairs).
- P2: committed expectation, moderate confidence: some candidate has a pairing with `D` avoiding
  1. The basis is Jooken's description of `L` (outputs equal at input distance 0, copied at
  distance 1, swapped at distance 2 or 3): with each connector made of one input and the output
  on the same side, a copy or an equality gives distance 0 and a swap gives the input distance 2
  or 3, never 1. For `W` alone the "starred" replacement at input distance 2 may produce 1; no
  direction is committed for `W`.
- P3 (only if P2 holds): the ring `R_1(A, B)` has no Petersen coloring (checked proof) and
  `R_3(A, B)` is cyclically 4-edge-connected (exhaustive search for cycle-separating cuts of size at
  most 3, plus an explicit 4-cut). With the ring theorem this gives `pd(R_3) >= 3`, and the
  cardinality instance "at most 2 bad vertices" of `R_3` is expected UNSAT (checked by solver as a
  consistency check, 2-hour limit; a timeout decides nothing).

## One-sidedness

`D(B)` avoiding 1 is an UNSAT statement with a verified proof for each pairing; membership of a
distance in `D` is a SAT witness checked from the definition. The ring theorem is a proof; the
cyclic connectivity of `R_3` is an exhaustive computation.

## Premise dependencies

EXP-001 (`G52` is a counterexample), EXP-010 (distance sets), Theorem 6 and Proposition 5 of the
context note, Proposition 2 of Mattiolo et al. (only for the step from one graph to statement (e)).

## Budget

CPU only; 10 minutes per SAT instance; 4 hours overall (not counting the optional consistency
check of P3).

## Verdict rules

CONFIRMED if P1, P2, P3 pass (then statement (e) is false under the stated premises); REFUTED (of
P2) if every candidate conducts 1 under every pairing; the table of conducted sets is the output
either way.

## Addendum 1 (2026-09-19 12:20), before any result of candidate family 3 was read

A short argument settles part of P2 in advance `[D]`. Let `G` have no Petersen coloring, `uv` an
edge, `B = G - {u, v}`, with connectors `{u1, u2}` (the ends of `uu1`, `uu2`) and `{v1, v2}` (the
u|v pairing). If a map with every vertex of `B` good had distance 1 at `{u1, u2}`, the two labels
would share a vertex `x` of `P` with third edge `z`; by Lemma 3 the other connector also has
distance 1, with third edge `z'` at its common vertex, and the equal classes give `z = z'`
(distinct edges have distinct classes). Labelling `uv` by `z` would then make `u` and `v` good: a
Petersen coloring of `G`. So `1` is not in `D(G - {u, v})` under the u|v pairing.

Together with `D(G52 - e0 - e) = {1}` for the 282 edge pairs of EXP-010, Theorem 4 of the context
note applies with `A = G52 - e0 - e` and `B = G52 - {u, v}`, joined connector `{c, d}` of `A` to
connector `{u1, u2}` of `B` and connector `{v1, v2}` of `B` to connector `{a, b}` of the next `A`:
`pd(R_t(A, B)) >= t` for every `t`, provided `D(B)` is not empty (every adjacent pair of `G52` is
critical, EXP-006 and EXP-011, so `B` has a Petersen coloring). What remains to be tested is P3:
`R_1` non-colorable, `R_2`, `R_3` cyclically 4-edge-connected, and the consistency check that
`R_3` has no map with at most two bad vertices. The pair used: the first `(e0, e)` with distance
set `{1}` in EXP-010 order, and `uv` the first edge of `G52` disjoint from `e0`, `e` and from their
neighbourhoods (so that the blocks are cut from `G52` independently of each other; any choice is
allowed by the theorem).

## Addendum 2 (2026-09-19 12:35), before the runs named here

Outcome so far (read before this addendum): `D(A) = {1}`, `D(B) = {0}` with checked proofs; `R_1`
non-colorable; `R_1`, `R_2` without cycle-separating cuts below 4; `pd(R_2) = 2` with the two bad
vertices in the two `B`-blocks. The solver consistency check "at most 2 bad vertices" on `R_3`
(cardinality encoding, 2-hour limit) is running and may time out.

Additional checks, cheaper and fixed now:
- P4 (upper bound): `R_3` has a map with exactly three bad vertices (cardinality bound 3, 1-hour
  limit; SAT expected, the checker must count 3 bad vertices in three different blocks, and by
  the ring theorem these blocks are pairwise non-consecutive).
- P5 (sampled lower bound): ten designated pairs of vertices of `R_3`, drawn with a fixed seed
  (`random.Random(12)`), five inside a single block and five in two different blocks: relaxing the
  star condition at exactly these two vertices is UNSAT with a verified proof in every case (the
  ring theorem says every map has bad vertices in at least three blocks).
- P6 (independent cut check): the exhaustive routine of EXP-001 (all edge sets of size at most
  three) finds no cycle-separating cut in `R_1` and `R_2`, as the bridge search did.

## Addendum 3 (2026-09-19 12:52): tooling only

The cardinality solves for `R_3` (bounds 2 and 3) are slow (more than 20 minutes each so far).
The ten P5 pairs are therefore run in parallel by `run_r3_pairs.py`, with the same seed and the
same selection code as `run_r3_checks.py`; results in `artifacts/r3-pairs.json`. A note on P4
added before its result: with exactly one bad vertex per bad block the bad blocks must be the three
`B`-blocks, since an `A`-block with one bad vertex between two good `B`-blocks would have both
connectors at distance 0, forcing the class of its bad vertex to be zero, which a bad vertex never
has.

## Addendum 4 (2026-10-06), before the runs named here

Open obligation of `unbounded-defect` v0.01: the upper bound `pd(R_3) <= 3` (P4 timed out with the
cardinality encoding). Witness search by designated relaxation, as for `R_4` in EXP-009: relax the
star condition at exactly one vertex in each of the three `B`-blocks of `R_3`, at the local index of
the bad vertex of the `B`-block witness of `R_2` (and, if that fails, the next three `B`-block
vertices in order of local index). A SAT answer whose checker defect is 3 gives `pd(R_3) = 3`;
UNSAT answers decide nothing about `pd(R_3)`. Budget 30 minutes per combination, at most four
combinations. Runner `run_r3_upper.py`, result `artifacts/r3-upper.json`.
