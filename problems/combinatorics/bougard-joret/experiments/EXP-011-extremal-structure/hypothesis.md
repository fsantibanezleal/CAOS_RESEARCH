# EXP-011 preflight: the structure of the extremal graphs at the conjectured value

Date: 2026-11-11. Status: frozen before any computation. CPU only.

## Question

At 35 open-window triples, EXP-005 to EXP-007 also enumerated the conjectured edge count c = t(n,alpha) +
ceil(k alpha/2) and found 1 to 35 qualifying graphs (k-connected, independence number exactly alpha, c edges); the
records keep only five examples each. Is every one of these extremal graphs a Bougard-Joret graph, that is: does its
vertex set split into alpha cliques of the balanced sizes of the Turan graph T(n, alpha), with exactly
ceil(k alpha/2) edges between the cliques?

This matters for the method of a general proof: Bougard and Joret's argument (their Proposition 8) works by forcing
such a clique partition; an extremal graph without one would show that a proof of the second line must handle graphs
with no clique partition.

## Method

1. **Regenerate every extremal graph** at E = c for the 35 triples (list below), with the pipeline of EXP-006 to
   EXP-009 (`geng_a<alpha> -q -d<k> n c:c res/mod` and `filter2 alpha k --print`), all qualifying graph6 lines kept
   (`collect.py`). The number per triple must equal the count recorded in the earlier enumeration (gate).
2. **Recheck each graph independently** (`analyze.py`, networkx, no shared code with the C filter): the independence
   number by an exact maximum clique of the complement, the vertex connectivity by networkx, the edge count.
3. **Clique partition:** decide exactly whether V(G) splits into alpha cliques (a proper alpha-colouring of the
   complement, by backtracking), and if so record the clique sizes, the edges inside the cliques and between them,
   and the number of edges leaving each clique.

Triples (from the earlier records, with the recorded number of extremal graphs): (10,3,3) 15, (11,3,3) 6, (12,3,3) 2,
(13,3,4) 1, (13,4,3) 1, (14,4,3) 1, (15,4,3) 1, (16,3,5) 3, (16,5,3) 18, (17,3,5) 3, (17,4,4) 2, (17,5,3) 34,
(18,3,5) 2, (18,4,4) 4, (18,5,3) 35, (19,3,5) 4, (19,3,6) 1, (19,4,4) 2, (19,5,3) 18, (19,6,3) 2, (20,3,5) 4,
(20,3,6) 1, (20,4,4) 2, (20,5,3) 5, (20,6,3) 5, (21,3,6) 1, (21,4,4) 2, (21,4,5) 1, (21,5,3) 17, (21,5,4) 7,
(21,6,3) 5, (22,3,6) 1, (22,4,4) 4, (22,5,3) 31, (22,6,3) 5. (12,3,3) lies in the proved range and is a control.

## Predictions

- Gate: the regenerated counts equal the recorded ones (HIGH).
- Every extremal graph has a partition into alpha cliques of the balanced Turan sizes, with exactly ceil(k alpha/2)
  edges between cliques (MODERATE).

## Budget

Phase 1 (the triples whose earlier enumeration at c took at most 60 seconds on 28 processes) on 4 processes while
EXP-010 runs; phase 2 (the rest) on 28 processes after EXP-010 ends. At most 24 hours in all.

## Addendum before phase 2 (2026-11-11), written after the phase 1 results and before any phase 2 run

Phase 1 (22 triples, 165 extremal graphs, every count equal to the recorded one) refuted the structural prediction:
40 extremal graphs have no partition into alpha cliques (clique cover number alpha + 1, confirmed by a second,
independent method, `verify.py`, a cover by maximal cliques). All of them lie at k = 3 with alpha odd: (10,3,3) 12 of
15, (11,3,3) 3 of 6, (16,5,3) 5 of 18, (17,5,3) 9 of 34, (18,5,3) 8 of 35, (19,5,3) 3 of 18; (20,5,3) has none of 5.
Every graph that has a partition into alpha cliques has the full Bougard-Joret structure (125 of 125).

Predictions for phase 2, frozen now (the 13 remaining triples, same pipeline, plus `verify.py`):

- Gate: the regenerated counts equal the recorded ones (HIGH).
- Every extremal graph with a partition into alpha cliques has the full Bougard-Joret structure (HIGH).
- Extremal graphs without a partition into alpha cliques occur only at triples with k = 3 and alpha odd; among the
  phase 2 triples that is (21,5,3) and (22,5,3), and none occurs at (15,4,3), (20,3,6), (20,6,3), (21,3,6), (21,4,4),
  (21,4,5), (21,5,4), (21,6,3), (22,3,6), (22,4,4), (22,6,3) (MODERATE).
- Every extremal graph without a partition into alpha cliques has clique cover number exactly alpha + 1 (MODERATE).

Phase 2 scheduling: the seven triples whose earlier enumeration at c took at most 600 seconds on 28 processes, and
(15,4,3), run now on 4 processes beside EXP-010; the five others after EXP-010 ends.
