# Complete proof: the first interior shell

Date: 2026-09-05. Status: [D], complete elementary all-parameter derivation submitted for independent audit. The experiment verdict owns the subsequent audit and computational status. Finite checks are supporting evidence and are not premises of this proof.

The experiment preflight was committed as `d15f240` before the construction was implemented. This proof extends the adjacent strip proved in [EXP-001](../EXP-001-tree-strip/proof.md).

## 1. Definitions, theorem, and scope

All graphs are finite, simple, and undirected. Write $\alpha(G)$ for the independence number and $\kappa(G)$ for vertex connectivity. The quantity $f(n,a,k)$ is the minimum number of edges in a $k$-connected graph of order $n$ with independence number exactly $a$.

**Theorem 1 (the first interior shell).** For every integer $k\ge3$ and every integer $2\le a\le k+1$,

$$
f(a+k+1,a,k)=\left\lceil\frac{k(a+k+1)}2\right\rceil.
$$

The range $a\le k+1$ is exactly the admissibility condition $n\ge2a$ on the shell $n=a+k+1$. These parameters also satisfy $n\le ka$: the inequality is equivalent to $a(k-1)\ge k+1$, which follows from $a\ge2$ and $k\ge3$.

**Theorem 2 (all extremizers when $a=2$).** Let $k\ge3$ and $n=k+3$. A graph is extremal for $f(n,2,k)$ if and only if its complement is a disjoint union of cycles, each of length at least five, with total order $n$.

Theorem 1 proves this shell, not the whole revised first regime or the second regime of the Bougard-Joret problem. It includes previously known numerical cases, notably $a=k+1$, $(n,a,k)=(6,2,3)$, and the $a=k-1$ strip proved in EXP-001. Mathematical correctness and literature priority are separate questions; the dated source review bounds the novelty claim. No classification of all shell extremizers is asserted beyond Theorem 2 and the earlier tree-strip classification.

Every $k$-connected graph has minimum degree at least $k$. Thus the handshaking identity gives the universal lower bound

$$
e(G)\ge\left\lceil\frac{kn}{2}\right\rceil.
$$

It remains to attain this bound while proving the exact independence number and connectivity.

## 2. A matching lemma

**Lemma 3.** Every nonempty graph of minimum degree at least $b\ge0$ has a matching of size at least $\lceil b/2\rceil$.

**Proof.** Take a maximal matching $Q$. If there is an unmatched vertex $v$, all neighbors of $v$ are endpoints of edges in $Q$, by maximality. Therefore $2|Q|\ge\deg(v)\ge b$. If every vertex is matched, then $2|Q|$ is the graph order, which is at least $b+1$, and the claimed weaker bound again follows. A subset of a matching realizes any smaller prescribed nonnegative size. $\square$

## 3. Cycle powers and the Harary gap argument

Number the vertices of a cycle of order $m$ by $0,\ldots,m-1$ cyclically. Its $r$th power $C_m^r$ joins two vertices whenever their cyclic distance is at most $r$. We use only $r\ge1$ and $m\ge2r+4$, so this graph is $2r$-regular.

**Lemma 4 (cyclic gaps).** The graph $C_m^r$ is $2r$-connected. Moreover, the following graphs are $(2r+1)$-connected:

1. If $m=2q$, add to $C_m^r$ all antipodal edges $\{i,i+q\}$, $0\le i<q$.
2. If $m=2q+1$, add to $C_m^r$ the edges $\{i,i+q\}$, $0\le i\le q$.

The first augmented graph is $(2r+1)$-regular. The second has degree $2r+2$ at $q$ and degree $2r+1$ at every other vertex.

**Proof.** List the surviving vertices in cyclic order after a vertex deletion. Two consecutive surviving vertices are adjacent in $C_m^r$ if their intervening gap contains at most $r-1$ deleted vertices. If there are fewer than two gaps with at least $r$ deleted vertices, these consecutive-survivor edges form a spanning cycle or a spanning path of the surviving graph. Therefore disconnection requires at least two such gaps, hence at least $2r$ deleted vertices. This proves connectivity after fewer than $2r$ deletions. Since every degree is $2r$, the connectivity is exactly $2r$.

For either augmented graph, only deletion sets of size exactly $2r$ remain to be considered. Suppose its underlying cycle power is disconnected. The preceding count forces exactly two deleted blocks of length $r$, with no other deletions. The surviving vertices consequently form two nonempty consecutive arcs $A,B$. Choose $A$ to have the smaller length $p$. Rotate the cyclic coordinates for the following geometric argument so that

$$
A=\{0,\ldots,p-1\},\qquad
B=\{p+r,\ldots,m-r-1\}.
$$

If $m=2q$, then $p\le q-r$. For every $x\in A$, the antipode $x+q$ lies in $B$, because

$$
p+r\le q\le x+q\le q+p-1\le2q-r-1.
$$

Thus an added antipodal edge survives from $A$ to $B$.

If $m=2q+1$, then again $p\le q-r$. For every $x\in A$, both almost-antipodal vertices $x+q$ and $x+q+1$ lie in $B$, because their possible indices lie between $q$ and $q+p\le2q-r$. In the stated odd-order construction, every vertex is incident to at least one added edge to a vertex at cyclic distance $q$. This is an invariant property under rotation of the coordinates: each vertex has an added neighbor among its two almost-antipodal vertices. Consequently an added edge survives from $A$ to $B$ in this case too.

Each arc is internally connected by its ordinary cycle edges, so one crossing edge joins the entire surviving graph. This proves connectivity after every deletion of fewer than $2r+1$ vertices. In the even-order construction the antipodal edges form a perfect matching, giving degree $2r+1$ everywhere. In the odd-order construction, the endpoint lists $0,\ldots,q$ and $q,\ldots,2q$ overlap only at $q$, giving the asserted degrees. The minimum degree is $2r+1$ in both cases, so connectivity is exactly $2r+1$. $\square$

These are classical Harary constructions, credited to [Harary (1962)](https://doi.org/10.1073/pnas.48.7.1142). The complete argument above supplies every connectivity property used here; it does not rely on computational evidence or on an unverified assertion extracted from an inaccessible full text.

**Lemma 5 (independence of the cycle power).** If $r\ge1$ and $m>2r$, then

$$
\alpha(C_m^r)\le\left\lfloor\frac{m}{r+1}\right\rfloor.
$$

**Proof.** For an independent set of size at least two, the forward cyclic distances between consecutive members are all at least $r+1$. Their sum is $m$, so the size is at most $m/(r+1)$. A singleton satisfies the same bound because $m\ge r+1$. $\square$

## 4. An injective missing-neighbor construction

**Lemma 6 (lifting a residual graph).** Let $k\ge a\ge3$, let $d=k-a$, and let $H$ be a graph of order $k+1$. Choose a set $M\subseteq V(H)$ of size $a$. Suppose that

- $\alpha(H)\le a$;
- $\deg_H(t)\ge d+1$ for $t\in M$, and $\deg_H(t)\ge d$ for $t\notin M$;
- if $d\ge1$, then $H$ is $d$-connected.

Add an independent set $S$ of size $a$, assign its vertices bijectively to $M$, and join each $s\in S$ to every vertex of $H$ except its assigned vertex. Then the resulting graph $G$ has independence number exactly $a$ and connectivity exactly $k$.

**Proof: degrees and independence.** Every vertex of $S$ has degree $k$. Put $r_t=1$ if $t\in M$ and $r_t=0$ otherwise. Every residual vertex has degree

$$
\deg_G(t)=\deg_H(t)+a-r_t\ge k.
$$

An independent set contained in either part has size at most $a$. If it meets both parts, the presence of one $s\in S$ restricts it to at most one vertex $t$ of $H$. Since the assignment of missed vertices is injective, at most one vertex of $S$ can be included with that $t$. Such a mixed independent set has size at most two, hence at most $a$. The set $S$ witnesses $\alpha(G)=a$.

**Proof: connectivity.** Let $X\subseteq V(G)$ have $|X|<k$, and put

$$
A=S\setminus X,\qquad B=V(H)\setminus X.
$$

There are $k+1$ residual vertices, so $|B|\ge2$.

If $A=\varnothing$, then $a$ vertices have already been deleted. The case $d=0$ is impossible because $a=k>|X|$. If $d\ge1$, fewer than $k-a=d$ residual vertices were deleted, and the $d$-connectivity of $H$ implies that $G-X$ is connected.

Suppose next that $A\ne\varnothing$ and $|B|\ge3$. Each vertex of $A$ is adjacent to all but at most one member of $B$. Any two vertices of $A$ therefore share a neighbor in $B$, so all of $A$ lies in one component $C$. This component also contains every member of $B$ adjacent to any member of $A$. At most one residual vertex $t$ can lie outside $C$, because a fixed vertex of $A$ misses only one residual vertex. If such a $t$ exists, every member of $A$ misses $t$, so $|A|\le r_t$. If $t$ is disconnected from $C$, all its neighbors in $H$ were deleted. The disjoint deletions in the two parts then give

$$
|X|\ge a-|A|+\deg_H(t)
\ge a-r_t+\deg_H(t)
=\deg_G(t)\ge k,
$$

a contradiction.

Finally, if $|B|=2$, then exactly $k-1$ residual vertices were deleted. Since $|X|<k$, no vertex of $S$ was deleted. The $a\ge3$ vertices of $S$ miss distinct residual vertices, so at least one of them misses neither member of $B$ and is adjacent to both. Every other member of $S$ is adjacent to at least one member of $B$. Hence $G-X$ is connected in this final case as well.

This proves $\kappa(G)\ge k$. Since vertices of $S$ have degree exactly $k$, the opposite inequality holds, giving $\kappa(G)=k$. $\square$

## 5. The generic range: $a\ge3$ and $d=k-a\ge2$

Set

$$
m=k+1=a+d+1,\qquad n=a+m,\qquad
\varepsilon=kn\pmod2\in\{0,1\}.
$$

We construct a $d$-connected residual graph $H$ whose degrees are $d+1$ at exactly $a+\varepsilon$ distinct vertices and $d$ elsewhere. All constructions contain $C_m^r$ for $r=\lfloor d/2\rfloor\ge1$.

### 5.1. Even $d$

If $d=2r$, begin with the $d$-regular graph $C_m^r$. Its complement is $a$-regular, since $m-1-d=a$. Here $n=2a+d+1$ is odd, so $\varepsilon$ is the parity of $k$, equivalently the parity of $a$. Lemma 3 supplies a complement matching of size

$$
\frac{a+\varepsilon}{2}=\left\lceil\frac a2\right\rceil.
$$

Add these edges. Their distinct endpoints are exactly the $a+\varepsilon$ vertices whose degree becomes $d+1$. Connectivity is preserved by adding edges, so Lemma 4 shows that the resulting $H$ is $d$-connected.

### 5.2. Odd $d$ and even $m$

If $d=2r+1$ and $m$ is even, begin with $C_m^r$ plus the antipodal perfect matching. By Lemma 4 this is $d$-regular and $d$-connected. Here $a$ is even, $n=2a+d+1$ is even, and $\varepsilon=0$. The complement is $a$-regular, so Lemma 3 supplies a matching of size $a/2$. Adding it gives degree $d+1$ at exactly $a$ distinct vertices and degree $d$ elsewhere.

### 5.3. Odd $d$ and odd $m$

If $d=2r+1$ and $m=2q+1$ is odd, begin with the odd-order construction of Lemma 4. It is $d$-connected, with degree $d+1$ at $w=q$ and degree $d$ everywhere else. Here $a$ is odd, $n$ is even, and $\varepsilon=0$.

In the complement, every vertex other than $w$ has degree $a$, while $w$ has degree $a-1$. Deleting $w$ from that complement therefore leaves minimum degree at least $a-1$. Lemma 3 supplies a matching of size $(a-1)/2$ in the remaining graph. Add these edges to the residual graph. Their $a-1$ distinct endpoints exclude $w$, so the final $H$ has degree $d+1$ at exactly $a$ distinct vertices, including $w$, and degree $d$ elsewhere. Its $d$-connectivity is preserved.

### 5.4. Independence and lifting

In all three cases, $H$ contains $C_m^r$. Since $d\le2r+1$,

$$
m=a+d+1\le a+2r+2<(a+1)(r+1).
$$

The strict inequality holds because the difference between its right side and $a+2r+2$ is $r(a-1)-1\ge1$. Lemma 5 now gives

$$
\alpha(H)\le\left\lfloor\frac{m}{r+1}\right\rfloor\le a.
$$

Choose any $a$ of the $a+\varepsilon$ vertices of degree $d+1$ to form $M$ and apply Lemma 6. The resulting graph has order $n$, independence number $a$, and connectivity $k$.

Every vertex of $S$ has degree $k$. Each vertex of $M$ has degree $(d+1)+(a-1)=k$. Every residual vertex of degree $d$ has degree $d+a=k$. If $\varepsilon=1$, there is precisely one unselected residual vertex of degree $d+1$, and its degree in $G$ is $k+1$. Thus the degree sum is $kn+\varepsilon$, and

$$
e(G)=\frac{kn+\varepsilon}{2}=\left\lceil\frac{kn}{2}\right\rceil.
$$

This proves Theorem 1 throughout the generic range.

## 6. The boundary $a=k$: a residual matching

Here $k\ge3$, $m=k+1$, and $n=2k+1$. Let $H$ consist of a matching of size $\lceil k/2\rceil$ and its remaining isolated vertices. There are at least $k$ matching endpoints; choose $k$ distinct endpoints as $M$. Apply the same missing-neighbor construction with an independent set $S$ of size $k$.

The matching has

$$
\alpha(H)=k+1-\left\lceil\frac k2\right\rceil\le k.
$$

Every selected residual vertex has degree one in $H$, while the other residual vertices have nonnegative degree. Lemma 6 therefore applies with $a=k$ and $d=0$; its all-$S$-deleted case is impossible, so no connectivity of the residual matching is required. It proves $\alpha(G)=k$ and $\kappa(G)=k$.

If $k$ is even, the matching has $k$ endpoints and one isolated vertex. All endpoints are selected, and every vertex of $G$ has degree $k$. If $k$ is odd, the matching is perfect on $k+1$ vertices. Exactly one endpoint is unselected; it has degree $k+1$ in $G$, while every other vertex has degree $k$. These are precisely the two degree patterns required to give $e(G)=\lceil k(2k+1)/2\rceil$.

## 7. The boundary $a=k-1$: the nonstar path construction

The entire $a=k-1$ strip, including its full extremal characterization by nonstar trees, was proved in [EXP-001, Sections 1-4](../EXP-001-tree-strip/proof.md). For completeness, existence follows using the path $H=P_{k+1}$.

For $k\ge4$, choose as $M$ the $k-1$ internal vertices of this path and put $a=k-1$, $d=1$. The path is connected. Its selected vertices have degree two and its two unselected endpoints have degree one. Also,

$$
\alpha(P_{k+1})=\left\lceil\frac{k+1}{2}\right\rceil\le k-1.
$$

Lemma 6 applies and gives independence number $k-1$ and connectivity $k$. Every resulting degree is $k$, so on $n=2k$ vertices the graph has $k^2$ edges, attaining the lower bound.

The only case excluded from this invocation of Lemma 6 is $k=3$, $a=2$. It is covered directly by Section 9 below, as well as by the separate two-survivor argument in EXP-001.

## 8. The boundary $a=k+1$: the crown graph

Here $n=2a$ and $k=a-1$, with $a\ge4$. Take $K_{a,a}$ and remove a perfect matching. This graph is $k$-regular and has $ak=kn/2$ edges.

Either bipartition class is an independent set of size $a$. A mixed independent set contains at most one vertex from each class, since each vertex misses only its matched partner in the opposite class. Hence the independence number is exactly $a$.

After deleting fewer than $k=a-1$ vertices, at least two vertices remain in each class, and at least $a+2\ge6$ vertices remain in total. In particular, at least one surviving class has size at least three. Suppose it is $B$. Any two surviving vertices in the other class $A$ share a neighbor in $B$, because each misses at most one member of $B$. All of $A$ therefore lies in one component. Every vertex of $B$ has a neighbor in $A$, because $|A|\ge2$ and it misses at most one such vertex. The remainder is connected. This proves connectivity at least $k$, and $k$-regularity gives connectivity exactly $k$.

## 9. The boundary $a=2$ and its complete equality classification

Put $n=k+3\ge6$. Consider a graph $F$ that is a disjoint union of cycles, each of length at least five, with total order $n$, and let $G=\overline F$.

The graph $F$ is $2$-regular and triangle-free. Thus $G$ is $(n-3)$-regular, and

$$
\alpha(G)=\omega(F)=2,
$$

where $\omega$ denotes clique number. The equality is exact because $F$ has an edge. Also $n(n-3)$ is even, so

$$
e(G)=\frac{n(n-3)}2=\frac{nk}{2}=\left\lceil\frac{nk}{2}\right\rceil.
$$

To prove connectivity, suppose that deleting a set $X$ of fewer than $k=n-3$ vertices disconnects $G$. At least four vertices survive. Partition them into nonempty sets $U,V$ that are unions of distinct connected components of $G-X$. There are no $G$-edges between $U$ and $V$, so every possible edge between them belongs to $F$. Since every degree in $F$ is two, both $|U|$ and $|V|$ are at most two. As at least four vertices survive, both sizes are exactly two. The four cross edges form a $4$-cycle in $F$, and they exhaust the degrees of their four endpoints. Consequently this is an entire $4$-cycle component of $F$, contrary to its construction. This proves $\kappa(G)\ge k$; regularity gives equality.

Taking $F=C_n$ supplies an example for every $n\ge6$, proving the remaining case of Theorem 1.

For necessity in Theorem 2, let $G$ be any extremizer for these parameters. Equality in the edge bound and minimum degree at least $k$ force every degree to be exactly $k=n-3$. Hence its complement $F$ is $2$-regular, and therefore a disjoint union of cycles of length at least three. The equality $\alpha(G)=2$ rules out triangular components, since their three vertices would be independent in $G$.

If $F$ had a $4$-cycle component, delete every vertex outside that component. This deletes exactly $n-4=k-1$ vertices, while the remaining graph in $G$ is the complement of a $4$-cycle, namely two disjoint edges. That contradicts $k$-connectivity. All components of $F$ must therefore have length at least five. The preceding sufficiency proof applies to every such complement, completing the classification. $\square$

## 10. Exhaustion of the parameter range and evidence boundary

For $2\le a\le k+1$, either $a=2$, $a=k+1$, $a=k$, $a=k-1$, or $a\ge3$ and $k-a\ge2$. Sections 5-9 therefore cover every parameter in Theorem 1. In every case the constructed graph attains the universal edge lower bound and has the required exact independence number and connectivity.

The matching choices need not be unique. Their existence and every graph property used in this argument hold uniformly in the parameters. A deterministic implementation and its finite audits can corroborate the proof, but neither a numerical grid nor a successful program is used to infer an unrestricted theorem.

## References and attribution

- Bougard and Joret, *Turán's theorem and $k$-connected graphs*, Section 6: [author-hosted paper](https://gjoret.be/papers/turan.pdf). This is the original problem context, including known parameter ranges.
- Das-Gupta, 2026 preprint, Sections 3-4: [arXiv 2608.18828v1](https://arxiv.org/html/2608.18828v1). This is the recent correction/counterexample context, not a premise used to prove the construction here.
- F. Harary, *The Maximum Connectivity of a Graph*, Proceedings of the National Academy of Sciences **48** (1962), 1142-1146: [DOI 10.1073/pnas.48.7.1142](https://doi.org/10.1073/pnas.48.7.1142). Credit for the classical minimum-edge connected graph constructions; Lemma 4 gives a self-contained proof of the specific properties required here.
- [EXP-001 complete proof](../EXP-001-tree-strip/proof.md): the $a=k-1$ strip and its nonstar-tree classification.
