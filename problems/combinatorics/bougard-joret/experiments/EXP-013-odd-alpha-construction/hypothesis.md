# EXP-013 preflight: extremal graphs without a clique partition for every odd alpha (k = 3)

Date: 2026-11-14. Status: frozen before any computation of this experiment. CPU only.

## Background

EXP-011 found, at the conjectured edge count c = t(n,alpha) + ceil(3 alpha/2) with k = 3, extremal graphs without a
partition into alpha cliques at (10,3,3), (11,3,3) and (16,5,3) to (19,5,3), and none at (20,5,3), (21,5,3), (22,5,3).
Conditional on Didin's Theorem 3, such graphs with p(G) >= 2 need alpha odd, s(G) = 1 and n <= 4 alpha - 1
(EXP-011 second addendum).

A descriptive analysis of the 32 graphs with s = 1 (probe scripts copied into this folder) shows one shape in all of them:
- alpha - 2 cliques of orders 3 and 4, plus one part X with independence number 2;
- X is one of two graphs, X6 (graph6 `ETxO`, 6 vertices, 8 edges) or X7 (graph6 `FQjRo`, 7 vertices, 11 edges),
  each the complement of a maximal triangle-free graph;
- exactly (3 alpha - 3)/2 edges join different parts, three from each part at three distinct vertices, so the
  quotient is a cubic multigraph on the alpha - 1 parts;
- X6 attaches at one triple of vertices up to automorphism, X7 at three.

X6 replaces two cliques K3 + K3 (6 edges) by 8 edges on the same 6 vertices, and X7 replaces K3 + K4 (9 edges) by 11 edges.
Either way it saves 2 of the ceil(3 alpha/2) = (3 alpha + 1)/2 edges between parts, so the total stays at c.

## Question

Does this shape give, for every odd alpha in {7, 9} and every n with 3 alpha < n <= 4 alpha - 1, a 3-connected graph
with n vertices, independence number alpha, c edges and clique cover number alpha + 1?

At (22,7,3), (23,7,3) and (24,7,3) such a graph is extremal unconditionally, because EXP-007 to EXP-010 proved
f = c there; at the other orders it is extremal if Didin's Theorem 9 holds.

## Method

`construct.py` (NetworkX 3.4.1, fixed seeds).
1. Take the balanced clique orders of T(n, alpha).
2. Replace two K3 by X6 when there are two K3, else a K3 and a K4 by X7; this needs a K3, which holds exactly when
   n <= 4 alpha - 1.
3. Choose a cubic multigraph on the alpha - 1 parts: the circular ladder, the Moebius ladder, then random cubic
   multigraphs, without loops.
4. Join the parts along it, each clique using three distinct vertices and X its recorded attaching triple.
5. Check each candidate exactly:
   - the edge count;
   - the independence number, as a maximum clique of the complement;
   - the vertex connectivity, by node_connectivity;
   - the clique cover number, by the exact alpha-colouring backtracking of EXP-011 `analyze.py` and the
     maximal-clique cover of `verify.py`, both run.
6. Keep the first candidate that passes per (n, alpha), and give up after 2,000 candidates.

## Predictions

- A passing graph exists for every (n, alpha) with alpha in {7, 9} and 3 alpha < n <= 4 alpha - 1 (MODERATE).
- No passing graph exists with this shape at n = 4 alpha, where every clique has order 4 and no X fits (HIGH; the
  shape needs a K3).

## Budget

At most 2 CPU-hours.
