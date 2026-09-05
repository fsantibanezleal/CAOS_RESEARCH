# Complete proof: the next triangle-free matching level

Date: 2026-09-05. Status: [D], complete all-parameter derivation submitted for independent audit. The experiment verdict owns the subsequent validation status. Preflight was committed and pushed as `f3fdda6` before implementation and computation. EXP-001 and EXP-002 are unchanged.

## 1. Definitions, result, and attribution

All graphs are finite, simple, and undirected. Write $e(F)$, $\Delta(F)$, and $\nu(F)$ for edge count, maximum degree, and maximum matching size. Define

$$
T(d,m)=\max\{e(F):F\text{ is triangle-free},\ \Delta(F)\le d,\ \nu(F)\le m\}.
$$

Isolated vertices are permitted and do not affect this maximum.

**Theorem 1 (fixed order).** For every integer $d\ge7$,

$$
\max\{e(F): |V(F)|=2d+3,\ F\text{ triangle-free},\ \Delta(F)\le d\}
=d^2+d+2.
$$

**Theorem 2 (next matching level).** For every integer $d\ge7$,

$$
T(d,d+1)=d^2+d+2.
$$

This settles the $m=d+1$ values in the conjectured intermediate range of Ahanjideh, Ekim, and Yildiz (AEY), Conjecture 6.1. It does not settle their entire conjecture. The attaining graph is the known $t=1$ construction of Banak, Ekim, and Taskin (BET), Proposition 4.1. The contribution proved here is a uniform upper bound.

BET's author-manuscript Table 3 already certifies this next-level value for $d=7,\ldots,12$. At $(d,m)=(13,14)$ it records lower bound 184 and upper bound 185. Theorem 2 proves **184**, not 185:

$$
T(13,14)=13^2+13+2=184.
$$

The primary sources and access distinctions are listed in Section 11. Bounded literature searches do not guarantee exhaustive bibliographic priority.

## 2. A shortest-odd-cycle degree bound

**Lemma 3.** Let $F$ be a triangle-free graph on $n$ vertices, and let $C$ be a shortest odd cycle in $F$, of length $\ell$. Then $\ell\ge5$, the cycle has no chord, every vertex outside $C$ has at most two neighbors on $C$, and

$$
\sum_{v\in V(C)}\deg_F(v)\le2n.
$$

**Proof.** Triangle-freeness gives $\ell\ge5$. A chord would split the odd cycle into two cycles of opposite parity; the odd one would be shorter. Thus $C$ is chordless.

Suppose that a vertex $x$ outside $C$ has at least three neighbors on it. List all its neighbors in their cyclic order on $C$. The lengths of the intervening arcs sum to the odd integer $\ell$, so at least one arc has odd length. Every arc has length at least two, since consecutive cycle vertices adjacent to $x$ would form a triangle. There are at least two other arcs, whose combined length is at least four. Hence the chosen odd arc has length at most $\ell-4$. Together with the two edges from its endpoints to $x$, it gives an odd cycle of length at most $\ell-2$, a contradiction.

The chordless cycle contributes $2\ell$ to the sum of its vertex degrees. The $n-\ell$ outside vertices contribute at most two edges each to that sum. Therefore

$$
\sum_{v\in V(C)}\deg_F(v)
\le2\ell+2(n-\ell)=2n.
$$

$\square$

If additionally $\Delta(F)\le d$, put

$$
D(F)=\sum_{v\in V(F)}(d-\deg_F(v))=nd-2e(F).
$$

Each summand is nonnegative. Lemma 3 therefore gives, for any nonbipartite $F$,

$$
D(F)\ge\sum_{v\in V(C)}(d-\deg_F(v))
\ge\ell d-2n\ge5d-2n. \tag{1}
$$

This is an elementary degree-deficit bound. No minimum-degree stability theorem is needed for the proof below.

## 3. Excluding the sole remaining fixed-order equality case

Let $F$ be triangle-free, have $n=2d+3$ vertices, and satisfy $\Delta(F)\le d$, with $d\ge7$.

If $F$ is bipartite, choose a bipartition whose smaller side has at most $d+1$ vertices. Summing degrees over that side gives

$$
e(F)\le d(d+1).
$$

If $F$ is nonbipartite, (1) gives $D(F)\ge d-6$, hence

$$
e(F)\le\frac{(2d+3)d-(d-6)}2=d^2+d+3. \tag{2}
$$

Suppose for contradiction that equality holds in (2). Then $D(F)=d-6$. Every inequality in (1) is an equality. It follows that:

1. A shortest odd cycle $C$ has length five.
2. Every vertex outside $C$ has degree exactly $d$.
3. Every vertex outside $C$ has exactly two neighbors on $C$.

Number $C$ cyclically by $c_0,\ldots,c_4$, with all subscripts in this section read modulo five. Its two neighbors at any outside vertex must be a nonadjacent pair on $C$. Every such pair is uniquely of the form $\{c_{i-1},c_{i+1}\}$. Define the type $V_i$ to contain $c_i$ together with all outside vertices having precisely that pair of cycle neighbors. Put $n_i=|V_i|$. Thus

$$
n_i\ge1,\qquad \sum_{i=0}^4n_i=2d+3. \tag{3}
$$

Each $V_i$ is independent: any two of its members share a cycle neighbor. There are no edges between $V_i$ and $V_{i+2}$, for the same reason. Thus every edge of $F$ joins consecutive types. In other words, $F$ is a subgraph of a blowup of the five-cycle; completeness between consecutive types has not been assumed.

The representative $c_i$ is adjacent to every member of $V_{i-1}\cup V_{i+1}$, directly from the type definition, and to no other type. Consequently

$$
b_i:=n_{i-1}+n_{i+1}=\deg_F(c_i)\le d. \tag{4}
$$

If $n_i\ge2$, the type contains an outside vertex. That vertex has degree $d$, while all its possible neighbors lie in the two adjacent types, of total size $b_i\le d$. Hence

$$
n_i\ge2\quad\Longrightarrow\quad b_i=d. \tag{5}
$$

The following elementary contradiction excludes (3)-(5).

**Lemma 4 (five-type equality obstruction).** For $d>6$, no positive integers $n_0,\ldots,n_4$ satisfy (3), (4), and (5).

**Proof.** If all five types have size at least two, (5) gives $b_i=d$ for every $i$. Summing and using (3),

$$
5d=\sum_i b_i=2\sum_i n_i=4d+6,
$$

so $d=6$, a contradiction. Therefore some type is a singleton; rotate indices so that $n_0=1$.

First suppose $n_1,n_4\ge2$. Applying (5) at these two types yields $n_2=n_3=d-1$. The total in (3) then forces $n_1+n_4=4$, so both are two. But

$$
b_2=n_1+n_3=2+(d-1)=d+1,
$$

contradicting (4).

Thus a type adjacent to $V_0$ is also a singleton. Reflect indices if necessary so that $n_0=n_1=1$. If $n_2,n_4\ge2$, (5) gives $n_3=d-1$. Equation (3) then gives $n_2+n_4=d+2$, contrary to $b_3\le d$.

Otherwise one of $n_2,n_4$ is also one. After reflecting and relabeling the consecutive singleton pair if needed, there are three consecutive singleton types, which we may call $n_0=n_1=n_2=1$. Equation (3) gives $n_3+n_4=2d$. But (4) at types 0 and 2 gives $n_4\le d-1$ and $n_3\le d-1$, a final contradiction. $\square$

Therefore equality in (2) is impossible. Since the edge count is an integer,

$$
e(F)\le d^2+d+2. \tag{6}
$$

No parity assumption was used. Equivalently, $D(F)$ has the parity of $d$; eliminating $D(F)=d-6$ improves its lower bound to $d-4$ for both odd and even $d$.

## 4. Attainment: the known BET construction

Put $p=d+1$. On bipartition classes $A=\{A_0,\ldots,A_{p-1}\}$ and $B=\{B_0,\ldots,B_{p-1}\}$, take the crown graph $K_{p,p}$ minus the matching $\{A_iB_i:0\le i<p\}$. Delete the two further edges $A_0B_1,A_1B_0$. Add a vertex $v$ adjacent exactly to $A_0,A_1,B_0,B_1$. Denote the result by $Q_d$.

This is BET's $t=1$ construction in Proposition 4.1, expressed using a crown graph. It is credited as prior work, although this representation was also independently derived during the present exploration.

The graph $Q_d-v$ is bipartite. The four neighbors of $v$ are independent because every edge between $\{A_0,A_1\}$ and $\{B_0,B_1\}$ is absent. Thus $Q_d$ is triangle-free. Every old vertex has degree $d$ and $v$ has degree four. For $d\ge7$, the maximum degree is exactly $d$, and

$$
|V(Q_d)|=2d+3,\qquad
e(Q_d)=d(d+1)-2+4=d^2+d+2. \tag{7}
$$

The edges $A_iB_{i+2\bmod p}$ form a perfect matching on the $2p$ old vertices. They avoid both the removed diagonal and the two further removed edges, since $p\ge8$. Thus $\nu(Q_d)\ge d+1$, while its order gives the reverse inequality. Consequently $\nu(Q_d)=d+1$.

Equations (6) and (7) prove Theorem 1 and provide the lower bound in Theorem 2.

## 5. A smaller odd-order bound

**Lemma 5.** If $J$ is triangle-free, has order $2d+1$, and satisfies $\Delta(J)\le d$, then

$$
e(J)\le d^2+1.
$$

**Proof.** If $J$ is bipartite, the smaller bipartition class has at most $d$ vertices, so $e(J)\le d^2$. Otherwise (1), now with $n=2d+1$, gives $D(J)\ge d-2$. Hence

$$
e(J)\le\frac{(2d+1)d-(d-2)}2=d^2+1.
$$

$\square$

This lemma is used only for $d\ge7$ here. The upper bound is also attained more generally by subdividing one edge of $K_{d,d}$ when $d\ge2$.

## 6. Arbitrary-order upper bound via Tutte-Berge

We use the classical **Tutte-Berge formula** in its standard form. For a finite graph $F$, let $o(F-S)$ be the number of odd-order components of $F-S$. Then

$$
\nu(F)=\min_{S\subseteq V(F)}
\frac{|V(F)|+|S|-o(F-S)}2. \tag{8}
$$

In particular, there exists a set $S$ attaining this minimum. If $C$ ranges over all components of $F-S$ and $t_C=\lfloor|V(C)|/2\rfloor$, (8) becomes the exact accounting identity

$$
\nu(F)=|S|+\sum_C t_C. \tag{9}
$$

Let now $F$ be any triangle-free graph of arbitrary order with $\Delta(F)\le d$ and $\nu(F)\le d+1$. Choose $S$ as in (9). The total number of edges incident to $S$ is at most

$$
\sum_{v\in S}\deg_F(v)\le d|S|.
$$

Edges within $S$ are counted twice in this degree sum, so using it as an upper bound is valid. The remaining edges lie within the components $C$.

- If $C$ has even order $2t_C$, the degree bound gives $e(C)\le dt_C$.
- If $C$ has odd order $2t_C+1$ and $t_C\le d-1$, Mantel's theorem gives
  $$e(C)\le\left\lfloor\frac{(2t_C+1)^2}{4}\right\rfloor=t_C(t_C+1)\le dt_C.$$
- If $C$ has odd order and $t_C=d$, Lemma 5 gives $e(C)\le dt_C+1$.
- If $C$ has odd order and $t_C=d+1$, Theorem 1 gives $e(C)\le dt_C+2$.

Identity (9) shows that no $t_C$ exceeds $d+1$. It also shows that there cannot be two components with $t_C\ge d$, since $2d>d+1$. Thus the total surplus over $d\sum_C t_C$ in all component bounds is at most two. Combining with the incident-edge bound and (9),

$$
e(F)\le d|S|+d\sum_Ct_C+2
=d\nu(F)+2
\le d(d+1)+2.
$$

The graph $Q_d$ attains the final value by Section 4. This proves Theorem 2 for every integer $d\ge7$. $\square$

This route uses the standard Tutte-Berge and Mantel theorems, not a supposition that an arbitrary graph already has an extremal component structure.

## 7. Alternative upper bound through the published AEY reduction

For an independently auditable route, discard isolated vertices and choose an edge-extremizer maximizing its number of $d$-star components. AEY Corollary 3.5 then makes every component either a $d$-star, or factor-critical with matching size $t\ge d$ and order $2t+1$. This follows there from Lemmas 2.4 and 3.2. The statement concerns the selected extremizer, not every graph.

At budget $d+1$, at most one nonstar component occurs. If absent, the edge count is at most $d(d+1)$. If its matching size is $d$, Lemma 5 (also AEY Theorem 3.4) bounds its edges by $d^2+1$, with at most one additional star, giving at most $d^2+d+1$. If its matching size is $d+1$, its order is $2d+3$ and Theorem 1 gives $d^2+d+2$. These alternatives reproduce the upper bound of Theorem 2.

The direct proof in Section 6 remains valid independently of this reduction.

## 8. A Bougard-Joret consequence with an explicit one-edge uncertainty

For a graph $G$, let $f(n,a,k)$ retain its Bougard-Joret meaning: the minimum number of edges in a $k$-connected graph of order $n$ and independence number exactly $a$. This is different from the triangle-free matching quantity $T(d,m)$.

**Theorem 6.** For every integer $d\ge7$,

$$
d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2. \tag{10}
$$

The exact choice between these two consecutive integers is not proved here.

**Lower bound.** If $G$ has order $n=2d+3$, independence number two, and connectivity at least $k=d+2$, then its complement $F$ is triangle-free and

$$
\Delta(F)\le(n-1)-k=d.
$$

Theorem 1 therefore gives

$$
e(G)=\binom{2d+3}{2}-e(F)
\ge(2d+3)(d+1)-(d^2+d+2)
=d^2+4d+1.
$$

**Upper-bound construction.** Start with the crown graph $R_d=K_{d+1,d+1}$ minus its diagonal matching. Subdivide a single existing edge $ab$: delete $ab$, introduce $w$, and add $aw,wb$. Let $P_d$ be the resulting graph and let $G_d=\overline{P_d}$.

The graph $P_d-w$ is bipartite, and the two neighbors of $w$ are nonadjacent, so $P_d$ is triangle-free. It has an edge, hence $\alpha(G_d)=\omega(P_d)=2$. Its old vertices have degree $d$ and $w$ has degree two. Its edge count is

$$
e(P_d)=d(d+1)+1,
$$

and therefore

$$
e(G_d)=d^2+4d+2. \tag{11}
$$

To prove $(d+2)$-connectivity of $G_d$, suppose that fewer than $d+2$ deleted vertices leave it disconnected. At least $d+2$ vertices survive. Partition its surviving components into nonempty sets $U,V$ with no cross edges of $G_d$. Then all cross pairs belong to $P_d$: it contains a complete bipartite subgraph with sides $U,V$ on at least $d+2$ vertices.

If this subgraph excludes $w$, it lies in a subgraph of the original crown. Each of its sides lies in one of the two original bipartition classes. Their sets of matched indices must be disjoint, because all diagonal edges of the crown are absent. Its total order is thus at most $d+1$, a contradiction.

If it includes $w$, assume $w\in U$. The opposite side is contained in $\{a,b\}$. If $|V|=1$, its total order is at most $\Delta(P_d)+1=d+1$. If $V=\{a,b\}$, no old vertex can join $w$ in $U$: the vertices $a,b$ lie in opposite original bipartition classes, and an old vertex cannot be adjacent to both in the bipartite graph $P_d-w$. The total order is then only three. Both possibilities contradict the required $d+2$ survivors.

Thus $G_d$ is $(d+2)$-connected. Its old vertices have degree exactly $d+2$, so its connectivity is exactly $d+2$. Equation (11) proves the upper bound in (10). $\square$

These parameters lie strictly inside the original proposed first regime: $2d+3>2+(d+2)$ and $2d+3<2(d+2)$. Moreover,

$$
(d^2+4d+1)-\left\lceil\frac{(2d+3)(d+2)}2\right\rceil
=\left\lfloor\frac d2\right\rfloor-2.
$$

This is positive for every $d\ge7$ and grows without bound. Thus (10) supplies an infinite strict-interior discrepancy from the degree-sum prediction, while retaining a one-edge uncertainty about the exact Bougard-Joret value. For instance, $97\le f(19,2,10)\le98$, whereas the degree-sum prediction is 95.

## 9. Why the known triangle-free maximizer cannot be complemented directly

The graph $\overline{Q_d}$ has the edge count in the lower endpoint of (10), but it fails the required connectivity. Indeed,

$$
N_{Q_d}(A_0)=N_{Q_d}(A_1)
=\{v,B_2,\ldots,B_d\},
$$

a set of size $d$. The resulting $K_{2,d}$ occupies $d+2$ vertices. Deleting the other $d+1$ vertices leaves no complement edges between its two sides. This is a cut of size $d+1$, smaller than the required $d+2$.

In fact,

$$
\kappa(\overline{Q_d})=d+1. \tag{12}
$$

For the lower bound in (12), a cut of size at most $d$ would leave at least $d+3$ vertices and hence a complete bipartite subgraph of $Q_d$ on that many vertices. If it excludes $v$, the crown argument bounds its order by $d+1$. If it includes $v$ in one side, the other side lies in $\{A_0,A_1,B_0,B_1\}$. When that other side uses both original bipartition classes, no old vertex can join $v$ in its side, so the total order is at most five. When it uses only one original class, it has size at most two; the side containing $v$ has size at most $d$, by the degree bound at an opposite vertex. The total order is at most $d+2$. All cases contradict $d+3$ surviving vertices. This proves (12).

The rejected shortcut is recorded because optimality for bounded-degree triangle-free graphs alone does not imply the connectivity needed by their complements.

## 10. Scope, small-degree boundary, and evidence independence

Theorems 1 and 2 hold for all integer degrees $d\ge7$, including odd degrees. The range is essential for the stated formula: at $d=6$, the balanced blowup of $C_5$ with five parts of size three has order 15, degree six, and 45 edges, exceeding $6^2+6+2=44$. Its order also bounds its matching number by seven, so it disproves extension of the same formula to $T(6,7)$.

Theorems 1 and 2 do not classify every extremal graph. They do not settle the remaining intermediate matching levels or the full conjecture of AEY. Theorem 6 does not choose the exact endpoint of the Bougard-Joret bracket. The earlier shell and tree-strip theorems remain separate results with their original scope.

The predeclared finite checks test the known attaining graphs, the subdivided-crown complements, the rejected cuts, parity, and the five-type constraints for specified degrees. Those computations can detect implementation errors and corroborate the derivation. They are not used to justify any universal quantifier above. No computational PASS is asserted by this proof document; the experiment verdict and certificates own that evidence.

## 11. Primary sources and standard-theorem references

- M. Ahanjideh, T. Ekim, and M. A. Yildiz, *Maximum size of a triangle-free graph with bounded maximum degree and matching number*, Journal of Combinatorial Optimization **47** (2024), article 57. [DOI 10.1007/s10878-024-01123-z](https://doi.org/10.1007/s10878-024-01123-z); [final published PDF](https://pure.uva.nl/ws/files/225491323/Maximum_size_of_a_triangle-free_graph.pdf). Definition 2.3, Lemma 2.4, Theorem 3.4, Corollary 3.5, and Conjecture 6.1 were checked in that version.
- Banak, Ekim, and Taskin, *Constructing extremal triangle-free graphs using integer programming*, Discrete Optimization (2023). [DOI 10.1016/j.disopt.2023.100802](https://doi.org/10.1016/j.disopt.2023.100802); [author manuscript](https://arxiv.org/html/2304.01729). Proposition 4.1 supplies the attaining family and Table 3 supplies the cited finite bounds. The final publisher full PDF was not obtained during this refresh; the content check used the author manuscript.
- C. Berge, *Sur le couplage maximum d'un graphe*, Comptes Rendus de l'Academie des Sciences **247** (1958), 258-259. The standard formula used in (8) is also explicitly restated as Theorem 2.1 in the primary research article [*A note on maximum size of a graph without isolated vertices under the given matching number*](https://www.sciencedirect.com/science/article/abs/pii/S0096300323004642). The original 1958 full text was not obtained here.
- Mantel's theorem is used in its classical form $e(H)\le\lfloor |V(H)|^2/4\rfloor$ for triangle-free graphs. It is a standard external theorem; the proof of the new fixed-order bound is Sections 2-4 above.
- The Bougard-Joret notation and prior counterexample context are recorded in the problem's [September 5 source refresh](../../context/2026-09-05-portfolio-refresh.md) and the earlier experiments. The secondary translation here is proved directly in Sections 8-9.
