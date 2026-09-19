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
