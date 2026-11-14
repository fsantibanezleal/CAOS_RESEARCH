# EXP-013 verdict: CONFIRMED, and proved for every odd alpha

Date: 2026-11-14. Hypothesis frozen at 15a64e33 before the construction ran.

## Result

- [MV] `construct.py`, every n with 3 alpha < n <= 4 alpha - 1 and alpha in {3, 5, 7, 9}, plus alpha = 11 beyond the
  frozen scope: 30 of 30 orders give a graph with
  - c = t(n,alpha) + (3 alpha + 1)/2 edges;
  - independence number alpha;
  - vertex connectivity 3;
  - clique cover number alpha + 1, confirmed by both partition methods.

  Each was found on the first or second candidate; `artifacts/construct.jsonl` has every graph in graph6, and
  `artifacts/run-output.txt` the run.
- At n = 4 alpha (5 orders) the shape does not exist: no clique of order 3 is left to merge, as predicted.
- At alpha = 5 the first quotient tried, a circular ladder on four parts, is not 3-edge-connected (it has a 2-edge
  cut); its graphs keep independence number 5 but are only 2-connected (checked on 20 random attachments per
  order; recorded on 2026-11-14 by `probe_ladder.py` in `artifacts/ladder.jsonl` and `artifacts/ladder-output.txt`:
  80 graphs, all with c edges and independence number 5, all with connectivity 2), and the second candidate, K4,
  passed.
- Every one of the 32 enumerated extremal graphs with s = 1 (EXP-011) is an instance of the construction:
  alpha - 2 cliques and X6 or X7 on a cubic quotient, which must be 3-edge-connected because the graph is
  3-connected.
- [D] `proof.md` proves the same for every odd alpha >= 3 and every n with 3 alpha < n <= 4 alpha - 1, given any
  3-edge-connected loopless cubic multigraph as quotient. The proof rests on six finite facts F1 to F6 about X6 and
  X7, verified exactly by `check_lemmas.py` (`artifacts/check-lemmas.txt`, 0 failures), and on Haxell's
  independent-transversal theorem.

## Reading

- Prediction 1 (a passing graph for every order at alpha = 7 and 9) holds, and holds for every odd alpha by the proof.
- Prediction 2 (no graph of this shape at n = 4 alpha) holds.
- Extremal unconditionally at (22,7,3), (23,7,3) and (24,7,3): their values are proved by enumeration (EXP-007 to
  EXP-010), and the constructed graphs attain them without a partition into alpha cliques.
- If Didin's Theorem 9 holds, the constructed graphs are extremal for every odd alpha >= 3 and 3 alpha < n <= 4 alpha - 1.
  Case (a) of the EXP-011 proposition is then realised everywhere it is allowed, and the bound n <= 4 alpha - 1 is sharp
  for the existence of such extremal graphs with p(G) >= 2.
- The building blocks X6 and X7 were found by a descriptive analysis of the EXP-011 graphs (probe scripts in this
  folder). They are the only two shapes among the 32 enumerated graphs with s = 1.

## How could this be wrong?

- The proof uses F1 to F6 as computed facts about two fixed graphs on 6 and 7 vertices; they are small enough to check
  by hand as well.
- Connectivity needs the quotient to be 3-edge-connected; the construction fails without it (the circular ladder on
  four parts), and the proof states the hypothesis.
- Extremality beyond order 24 rests on Didin's unrefereed Theorem 9.
