# 07 - Defects are unbounded: abnormal edges and sublinear approximations

Sources: `context/2026-09-18-defect-unbounded.md`; `context/2026-09-03-defect-parity-lemma.md`;
EXP-006 (addendum 4), EXP-008, EXP-009, EXP-010 verdicts.

## Two ways to measure the distance from a Petersen coloring

- The **Petersen defect** $\mathrm{pd}(G)$: the least number of vertices at which a map
  $E(G) \to E(P)$ fails the star condition (introduced in EXP-004 and EXP-006).
- The **abnormal-edge number** $\mathrm{ab}(G)$: the least number of abnormal edges (neither poor
  nor rich) of a proper 5-edge-coloring. Mattiolo, Mazzuoccolo and Mkrtchyan (Bull. Inst. Combin.
  Appl. 92 (2021) 78-90, arXiv:2104.09241) proved that $\mathrm{ab}$ is never 1 and asked whether
  $\mathrm{ab} \le 2$ forces a normal 5-edge-coloring; the five known counterexamples have
  $\mathrm{ab} \le 2$ (arXiv:2608.10028v3), so the answer is no.

**Lemma 1 [D].** $\mathrm{pd}(G) \le \mathrm{ab}(G)$ for every cubic graph.

*Proof idea.* In the Kneser model of $P$ (vertices are 2-subsets of $\{1,\dots,5\}$, an edge
$\{A,B\}$ has the color outside $A \cup B$), a proper 5-edge-coloring assigns to each vertex the
2-set $A_v$ of its missing colors and to each edge $uv$, seen from $u$, the edge of $P$ at $A_u$
with the color of $uv$. The two views of a poor or rich edge agree; for an abnormal edge choose
one. Only the end not chosen of an abnormal edge can be bad.

With the parity theorem ($\mathrm{pd} \ne 1$, page 04) this gives $\mathrm{ab} \ge \mathrm{pd} \ge 2$
for every cubic graph without a Petersen coloring, and it reproves $\mathrm{ab} \ne 1$ in
general. Hence
$$\mathrm{pd} = \mathrm{ab} = 2 \quad \text{for } G_{112},\ H_{112},\ G_{52},\ G'_{52},\ G_{68}.$$
For $G_{52}$ the bound $\mathrm{ab} \ge 2$ was also confirmed by machine: 42 single-edge relaxations
refuted with checked proofs meet all 14 edge orbits of its automorphism group of order 6.

## Rings and frames

**Theorem 2 (rings) [D].** Open $t \ge 2$ cubic graphs without a Petersen coloring at one edge
each and join them cyclically through 2-edge cuts. Every map $E(R) \to E(P)$ has a bad vertex in
every block, so $\mathrm{ab}(R) \ge \mathrm{pd}(R) \ge t$; $R$ is bridgeless if the blocks are.

*Proof.* If a block has only good vertices, the sum over its vertices of the label vectors is a sum
of stars of $P$, hence a cut of $P$, and it equals the sum of the indicators of the labels of the
two edges leaving the block. A cut with at most two edges is empty in a 3-edge-connected graph, so
the two labels are equal and the opened edge can be restored with that label: a Petersen coloring
of the block.

**Theorem 3 (frames) [D].** Replace every vertex of a cubic graph $K$ on $t$ vertices by a
counterexample minus a vertex. Every map has a bad vertex in every block ($\mathrm{pd} \ge t$);
the result is 3-connected if $K$ and the blocks are. Here the three leaving labels sum to a cut of
odd weight, which must be a star because $P$ is bridgeless and cyclically 5-edge-connected.

The constructions are those of Mattiolo et al. (their Theorems 2 and 3), who conclude only that a
block without abnormal edges yields a coloring of the block's graph with at most 5, respectively
7, abnormal edges. The cut-space argument upgrades the conclusion to a genuine Petersen coloring.

## Consequence for the sublinear approximation conjecture

Their Conjecture 3 states that five statements are equivalent: (a) the Petersen coloring
conjecture; (b), (c), (d), (e): a sublinear function bounds $\mathrm{ab}$ on all bridgeless, all
2-connected, all 3-connected, all cyclically 4-edge-connected cubic graphs. They proved
(a) $\Leftrightarrow$ (b) and that a sublinear bound on the last three classes is equivalent to
$\mathrm{ab} \le 5, 7, 9$ respectively.

**Corollary 4 [D].** On 2-connected cubic graphs, and on 3-connected cubic graphs, a sublinear
bound on $\mathrm{ab}$ exists if and only if every graph of the class has a normal
5-edge-coloring. Since $G_{52}$ is 3-connected and has none, (c) and (d) are false:
$\mathrm{ab} \ge n/52$ on rings and $\mathrm{ab} \ge n/51$ on frames built from $G_{52}$.

So (a), (b), (c), (d) are all false, and the conjectured equivalence now amounts to the falsity of
(e): **is there a cyclically 4-edge-connected cubic graph with $\mathrm{ab} \ge 10$?** All five
known counterexamples are cyclically 4-edge-connected with $\mathrm{ab} = 2$.

**Proposition 5 (threshold) [D].** If one cyclically 4-edge-connected cubic graph $G^*$ has
$\mathrm{pd}(G^*) \ge 3$, then $\mathrm{pd}$ and $\mathrm{ab}$ are unbounded on that class and (e)
is false. Proof: let $e_1 = ab$, $e_2 = cd$ be the end-edges of a path of length three. A coloring
of the 4-pole $G^* - e_1 - e_2$ with all vertices good, extended by giving $e_1$ the pendant label
at $a$ and $e_2$ the pendant label at $c$, has at most the two bad vertices $b$ and $d$; so the
4-pole is not colorable, and every copy of it in the cyclic join of Mattiolo et al. (cyclically
4-edge-connected by their Proposition 2) contains a bad vertex. So on that class either
$\mathrm{pd} \le 2$ everywhere or $\mathrm{pd}$ is unbounded.

EXP-010 tested the natural route. The cyclic joining of copies of $G - e_1 - e_2$ (their Theorem 4)
forces a bad vertex per copy only if the 4-pole $G - e_1 - e_2$ has no Petersen coloring. For
$G_{52}$, $G'_{52}$ and $G_{68}$ every such 4-pole is colorable (482, 482 and 4,947 orbit
representatives), with
exactly the two boundary patterns the cut space allows: two crossed equal pairs (about 72 percent
of the witnesses found) or the four edges around one edge of $P$. A crossed pattern can be chained
around a ring with an even number of copies, because any two edges of $P$ can be swapped by an
automorphism (checked on the 120 automorphisms), so those cyclic joins are Petersen colorable. The 4-poles $G - \{u, v\}$ for an edge $uv$ are colorable as well: this is the
universal 2-criticality of page 04 read at adjacent pairs.

## Exact values on small instances (EXP-009)

| graph | order | connectivity | pd | ab |
|---|---|---|---|---|
| $R_2$ (two copies of $G_{52}$) | 104 | 2 | 2 | between 2 and 4 |
| $R_3$ | 156 | 2 | 3 | at least 3 |
| $R_4$ | 208 | 2 | 4 | at least 4 |
| $K_4[G_{52}]$ | 204 | 3 | 4 | at least 4 |

Every witness has exactly one bad vertex per block. Rings and the $K_4$ frame of the
Petersen-colorable snark $J_5$ are Petersen colorable (controls).

## Open

- Statement (e): a cyclically 4-edge-connected cubic graph with $\mathrm{ab} \ge 10$, or a proof
  that $\mathrm{ab} \le 9$ on that class.
- By Proposition 5, a cyclically 4-edge-connected cubic graph with Petersen defect at least 3
  would be enough. Ten dot products of $G_{52}$ with itself (102 vertices, new counterexamples with
  checked proofs) all have defect 2.
- Is $\mathrm{pd}$ bounded on cyclically 4-edge-connected cubic graphs? A superposition approach
  (superedges $G - \{u, v\}$ with $u, v$ far apart carry a nonzero class of
  $\mathbb{F}_2^{E(P)}$ modulo the cut space from one connector to the other) is recorded as
  research line PCR-7.
