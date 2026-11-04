# EXP-004 preflight: the endpoint of the Bougard bracket (BJB-014)

Date: 2026-11-04. Status: frozen hypothesis before any computation. CPU only.

## Falsifiable target [C]

EXP-003 proved, for every integer d >= 7,

    d*d+4*d+1 <= f(2d+3, 2, d+2) <= d*d+4*d+2,

and left the endpoint open. Predict the UPPER endpoint:

    f(2d+3, 2, d+2) = d*d+4*d+2   for every integer d >= 7.

Equivalently (complements, as in EXP-003 Section 8): no triangle-free graph F on
2d+3 vertices with maximum degree at most d and exactly d*d+d+2 edges has a
(d+2)-connected complement. A complement fails (d+2)-connectivity exactly when F
contains a complete bipartite subgraph K_(U,W), U and W nonempty, on at least
d+2 vertices (delete the other at most d+1 vertices).

## Frozen symbolic route

Let F be such an extremal graph. It is nonbipartite (bipartite gives at most
d(d+1)), and with D = nd - 2e = d - 4, the deficit bound of EXP-003 Lemma 3
forces a shortest odd cycle C = c_0..c_4 of length five (length >= 7 gives
D >= 3d - 6). Every outside vertex has at most two C-neighbors. Let a be the
total shortfall of outside vertices below two C-neighbors and b the total
degree deficit of outside vertices. Then D = (d - 6 + a) + b, so a + b = 2.
Outside vertices with two C-neighbors fall into the five types V_i (neighbors
c_(i-1), c_(i+1)); let X be the at most two "defective" outside vertices.

Key observation: for an outside typed vertex v in V_i, N(v) lies in
V_(i-1) u V_(i+1) u X, while N(c_i) = V_(i-1) u V_(i+1) u (X n N(c_i)). If v has
degree d and no X-neighbor outside N(c_i), then {c_i, v} and N(v) span a K_(2,d)
on d+2 vertices. So in a counterexample every degree-d typed outside vertex
needs a "helper" in X not adjacent to c_i.

Cases to exclude:

1. X empty (a = 0, b = 2): at most two outside vertices lack degree d, but
   there are 2d - 2 outside vertices; some has no helper.
2. |X| = 1: the single helper would need about 2d - 4 > d neighbors.
3. |X| = 2 (a = 2, b = 0, every outside vertex has degree d, each defective
   vertex has exactly one C-neighbor c_p, c_q): split by q - p mod 5 in
   {0, +-1, +-2}. Each case is excluded by the type-size inequalities
   (n_(i-1) + n_(i+1) + eps_i <= d), the helper capacity d - 1 of each defective
   vertex, and the fact that a helper adjacent to two consecutive types forbids
   edges between its neighbors there (triangle-freeness). Case 0 forces the two
   defective vertices adjacent, a triangle with c_p; case +-1 leaves the middle
   type without enough helpers; case +-2 forces sizes (2, 1, 2, d-2, d-2) and
   then a vertex of degree at most 4.

The full proof is written in proof.md before the computation below is run.

## Finite corroboration (planned, not used to justify the universal claim)

1. Exhaustive at d = 7 (n = 17, e = 58) and, if feasible, d = 8 (n = 19,
   e = 74): an SMT search (z3) for a triangle-free graph with maximum degree
   at most d and at least d*d+d+2 edges whose complement is (d+2)-connected,
   with the five-cycle 0..4 fixed (justified by the shortest-odd-cycle lemma)
   and lazy cut constraints: each model found is checked by an exact vertex
   connectivity computation (networkx) on its complement, and the found cut's
   complete bipartite subgraph is forbidden. Expected result: UNSAT. A model
   that passes the connectivity check refutes the prediction.
2. The EXP-003 subdivided-crown complements remain the attaining graphs.

Prediction strength: HIGH for d >= 9, MODERATE at d = 7, 8, where slack in the
type-size inequalities is smallest.
