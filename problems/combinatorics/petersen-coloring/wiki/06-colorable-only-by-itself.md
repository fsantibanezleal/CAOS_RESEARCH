# 06 - Which counterexamples are colorable only by themselves?

Sources: EXP-007 (hypothesis, addenda, verdict); `context/2026-09-18-v3-and-h3-dossier.md`;
`context/2026-09-18-hcoloring-reduction-lemmas.md`.

## The question

For cubic graphs $G$ and $H$ (parallel edges allowed in $H$, no loops), an $H$-coloring of $G$ is
a map $f : E(G) \to E(H)$ that is injective on every vertex star and sends every star of $G$ onto
a star of $H$: $f(\partial_G(v)) = \partial_H(\varphi(v))$ for a vertex map $\varphi$. A Petersen
coloring is a $P$-coloring. The relation "$H$ colors $G$" is transitive, so a graph that colors a
counterexample to the Petersen coloring conjecture is itself a counterexample.

Ma, Mattiolo, Steffen and Wolf (Combinatorica 45 (2025), Article 16) proved that there is a
unique inclusion-wise minimal set $\mathcal{H}_3$ of connected bridgeless cubic graphs coloring
every bridgeless cubic graph, and that $G \in \mathcal{H}_3$ if and only if no bridgeless cubic
graph of smaller order colors $G$. The conjecture was the statement $\mathcal{H}_3 = \{P\}$; after
the disproof $\mathcal{H}_3$ is infinite. Goedgebeur, Jooken, Macajova, Mattiolo, Mazzuoccolo and
Ulyanov (arXiv:2608.10028v3, Section 5.4) ask whether their 52-vertex counterexamples are
colorable only by themselves, and tie the question to whether they are smallest counterexamples.

Both outcomes are informative. A bridgeless cubic $H$ on fewer than 52 vertices coloring a
52-vertex counterexample would be a new counterexample below the known upper bound of the window
$[40, 52]$; the absence of any such $H$ places the graph in $\mathcal{H}_3$.

## Two lemmas that make the search finite and small

Let $n_x = |\varphi^{-1}(x)|$ be the fiber size of a target vertex $x$; $x$ is used if $n_x > 0$.

**Lemma A (fiber parity).** For every edge $e = xy$ of $H$, $f^{-1}(e)$ is a perfect matching of
the subgraph of $G$ induced on $\varphi^{-1}(x) \cup \varphi^{-1}(y)$. Hence $n_x + n_y$ is even
for every edge of $H$, and for connected $H$ all fiber sizes have the same parity.

*Proof.* A vertex $v$ meets an edge of image $e$ exactly when $e \in \partial_H(\varphi(v))$,
that is, when $\varphi(v) \in \{x, y\}$, and then it meets exactly one, because $f$ is injective
on $\partial_G(v)$. $\square$

So there are two modes: every fiber odd, and then $\varphi$ is onto; or every fiber even, and then
at most $n/2$ target vertices are used.

**Lemma B (at most one unused vertex).** If a connected bridgeless cubic multigraph $H$ colors a
connected cubic graph $G$ and the set $W$ of unused vertices is not empty, then some connected
bridgeless cubic multigraph $H'$ with $V(H') = U \cup W'$, $|W'| \le 1$, colors $G$ with the same
vertex map ($U$ the set of used vertices; $W'$ is empty when $|\partial_H(W)|$ is even).

*Proof sketch (full proof in the context note).* Identify $W$ to one vertex $w^*$ and delete
loops; the graph stays bridgeless. While $\deg w^* \ge 4$, the splitting lemma (Fleischner; in the
form of Kaiser, Kuzel, Li, Wang, Lemma 1) splits two edges $aw^*$, $bw^*$ off $w^*$ keeping the
graph bridgeless; $a \ne b$, since otherwise the third edge at the cubic vertex $a$ would be a
bridge; suppress the new vertex of degree 2. Stop at degree 3 (keep $w^*$) or 2 (suppress it).
Stars of used vertices are untouched up to merging pairs of edges with distinct far ends, so the
composed map is an $H'$-coloring; $H'$ is connected because the images of the edges of the
connected graph $G$ between distinct fibers were never touched. $\square$

**Corollary.** $G$ of order $n$ is colored by a connected bridgeless cubic multigraph of order
less than $n$ if and only if it is so colored, for some even $k < n$, in one of three modes: all
fibers odd and $\varphi$ onto; all fibers even and $\varphi$ onto ($k \le n/2$); all fibers even
with exactly one unused vertex ($k - 1 \le n/2$).

The effect on the computation is decisive. Without the lemmas, the unknown target has a free part
that the graph does not constrain; on `G52` the lazy cut loop learned more than 2,000 bridge cuts
per order in 35 minutes and decided nothing (attempt 1, preserved). With them, the first decided
orders needed no cut at all. The two encodings agree on all 21 control instances (`K4`, the prism,
the Petersen graph, the flower snarks `J3` and `J5`, every even order below their own).

## Encoding

One CNF per target order $k$: vertex-to-class variables, a slot bijection at every vertex, a
perfect matching on the $3k$ slots as the unknown edge set of $H$, consistency along every edge
of $G$, first-use numbering of classes and founder slot order as symmetry breaking, one parity
variable with an XOR chain per class (Lemma A), the unit clause "the last but one class is used"
(Lemma B). Connectedness and bridgelessness of $H$ are enforced lazily by sound cut clauses. A SAT
answer is re-verified from the definition by an independent checker and the decoded $H$ is tested
for Petersen colorability; an UNSAT answer is the final formula refuted by CaDiCaL with a DRAT
proof checked by drat-trim.

## Results

See the EXP-007 verdict; the table below is transcribed from it.

State on 2026-09-18 (the verdict is written when the last certification ends; the table is then
replaced by the verdict's):

| graph | target orders refuted with verified proofs | remaining |
|---|---|---|
| `G52` | 2, 4, and every even order from 30 to 50 | 26, 28: proofs complete, post-hoc check running; 6 to 24: reached or approaching the 6-hour limit |
| `G52b` | 44, 46, 48, 50 | 42: in-process UNSAT after 14,448 s, external proof being written; 40: long run; below 40 stopped undecided |
| `G68` | 64, 66 | 40 to 62 running |

Two forms of the statement (fixed in addendum 5 of the hypothesis before the mid-range orders
ended):

- **Unconditional.** For each listed order `k`, no loopless cubic graph on `k` vertices colors the
  graph with a vertex map of kind (O), (E0) or (E1). By the corollary above, the union of these
  statements over all even `k < n` is equivalent to "no connected bridgeless cubic graph of smaller
  order colors the graph".
- **Conditional on Observation 9 of arXiv:2608.10028v3** (every bridgeless cubic graph on at most
  38 vertices has a Petersen coloring). A graph that colors a counterexample is a counterexample,
  and a counterexample with parallel edges yields a smaller one (suppress the digon; the two edges
  of the 2-edge cut around it carry equal labels). So only target orders from 40 to 50 can occur,
  and they are all refuted for `G52`: **`G52` is colorable only by itself, that is, it belongs to
  $\mathcal{H}_3$.** The same conclusion for `G52b` needs its orders 40 and 42.

No decided instance needed a connectivity or bridge cut. For the same target order `G52b` is 10 to
25 times harder than `G52`.
