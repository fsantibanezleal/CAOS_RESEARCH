# 08 - Six-poles, charges and transfer semigroups

Sources: `context/2026-10-06-charges.md` (sections 1 to 7); EXP-013 and EXP-014 hypotheses, addenda
and verdicts. Published in *unbounded-defect* v0.02, Section 6, DOI
[`10.5281/zenodo.23196817`](https://doi.org/10.5281/zenodo.23196817).

## Why 6-poles

Every known counterexample to the Petersen coloring conjecture has 4-edge cuts around copies of the
Petersen 4-pole, and Problem 11 of arXiv:2608.10028v4 asks for a cyclically 5-edge-connected one. A
ring of blocks joined by 2-edge connectors has 4-edge cuts between arcs; a ring of 6-poles joined by
3-edge connectors has 6-edge cuts between arcs, so it can be cyclically 5-edge-connected. The ring
theorem of page 07 holds verbatim for such rings: two 6-poles with disjoint conducted sets would give
cyclically 5-edge-connected graphs of unbounded defect.

## The 64 classes

The charge of a vertex is the class of the sum of its three labels in
$Q = \mathbb{F}_2^{E(P)}/\mathrm{Cut}(P)$; the vertex is good when the class is 0 and the labels are
distinct. The cut space is a binary $[15, 9, 3]$ code, so $|Q| = 64$, in six orbits under
$\mathrm{Aut}(P)$:

| orbit | classes | least weight | elements of least weight |
|---|---|---|---|
| `0` | 1 | 0 | the cut space (the ten stars) |
| `E` | 15 | 1 | one edge; also two edges at distance 1 |
| `D3` | 15 | 2 | two edges at distance 3 |
| `D2` | 30 | 2 | two edges at distance 2 (two such pairs per class) |
| `T1` | 1 | 3 | the five antipodal triples (the class of the all-ones vector) |
| `T2` | 2 | 3 | triples of pairwise distance-2 edges (ten per class) |

The five antipodal triples (three pairwise distance-3 edges) partition $E(P)$: removing the twelve
edges at the four 2-subsets that contain a fixed element leaves one of them.

## EXP-013: the core

Over 1,890 splits of 6-poles of `P`, `J5`, `J7` and the dodecahedron (shapes `H - u - w` and
`H - e1 - e2 - e3`), 11,340 formulas, all decided, every conducted set contains `0`, `E`, `D2`, and
`{0, E, D2}` itself is conducted by `P - u - w`. So charges never separate two of these blocks.

## EXP-014: the exact transfer relation

A block (6-pole with ordered connectors `L`, `R`) has the transfer relation
$T_M = \{(\sigma(L), \sigma(R))\}$. A ring is colorable iff the boolean product
$T_1 \Pi_1 \cdots T_t \Pi_t$ has a nonzero diagonal entry. By the Gauss law the relation is block
diagonal over the 64 classes, and by $\mathrm{Aut}(P)$-equivariance one class per orbit suffices:
six **sector matrices** of orders 60, 67, 48, 48, 30, 60. The products of a finite block family form
a finite semigroup; closing it decides every ring of the family, of every length, and the closed set
(kept minimal under containment) is a certificate checkable by products alone.

| family | generators | exact closure | antichain certificate | zero-trace elements |
|---|---|---|---|---|
| claw `Y` | 6 | 30 | 12 | 0 |
| Petersen superedge `S = P - u - w` | 6 | 19,005 | 276 | 0 |
| `Y` and `S` | 12 | 116,463 | 2,454 | 0 |

**Theorem.** Every ring of at least two blocks, each a claw or a Petersen superedge in either
orientation, joined through arbitrary bijections, is Petersen colorable. A ring of superedges always
has a coloring with all junction classes in the orbit `E`.

**Flower snarks.** $J_k = (Y\,\mathrm{id})^{k-1}(Y\,\tau)$. For odd $k$ only the sector `T1` has a
nonzero diagonal (for even $k$ only `E`; periodic from $k = 5$). So **every Petersen coloring of
$J_k$, $k$ odd, maps the three edges between consecutive claws onto an antipodal triple of $P$.**

**Superedge rings.** With the identity at every junction, $S^t$ ($t \ge 3$) is 3-edge-colorable iff
$t$ is even (3-edge-coloring transfer matrix, period 2), and for $t \ge 5$ it has girth 5 and is
cyclically 5-edge-connected (exhaustive search on $S^5$ plus the run argument of page 07's
cyclic-connectivity lemma). So the odd $S^t$, $t \ge 5$, are cyclically 5-edge-connected snarks of
girth 5 on $8t$ vertices, all Petersen colorable by the theorem.

**The classes are not enough.** `G52` split along a 6-edge cut (sides of 18 and 34 vertices) gives
two colorable 6-poles whose conducted sets share `0`, `E`, `D2` in all ten splits; their ring of
length 2 is `G52`, and the sector product has a zero diagonal in all six sectors.

**Validation.** Block matrices of `Y` and `S` recomputed by brute-force enumeration of maps, and 46
of the 81 blocks (including `Y` and `S`) by a second encoding with a second solver, all equal (the
other 35 were not reached within the run's limit); 203 rings decided both by traces and by CaDiCaL on
the graph, all agreeing; the three certificates re-verified by a separate program with integer
matrix products.

**`G52` pairs (EXP-013).** Of the 212 orbits of non-adjacent pairs of `G52`, none conducts `0` (the
restoration lemma), all conduct `E`, none conducts `T1`; 22 conduct only `E`.

## Open

- Which 6-poles without small internal cuts have a transfer semigroup with a zero-trace element? A
  ring of 6-poles without a Petersen coloring needs one (next bounded action of PCC-F6, EXP-015).
- The large families of EXP-014 (`F4`: the forty `P - e1 - e2 - e3` blocks, 336 generators; `F5`: all
  81 blocks, 684 generators) did not close within their one-hour limits; no zero-trace element
  appeared among the products computed.
