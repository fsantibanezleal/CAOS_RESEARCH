# Complete proof: the adjacent exceptional strip

Date: 2026-09-04. Status: [D], elementary all-parameter derivation, with the independent adversarial audit recorded in verdict.md. Finite tests are supporting controls only.

## Theorem

For every integer $k\ge3$, $f(2k,k-1,k)=k^2$. Moreover, a graph is extremal for these parameters if and only if it admits the following construction. Let $T$ be a nonstar tree on $k+1$ vertices. Let $S$ be an independent set of size $k-1$, partitioned into sets $S_t$, $t\in V(T)$, with

$$|S_t|=\deg_T(t)-1.$$

Add all edges from $S_t$ to $V(T)\setminus\{t\}$, and retain the edges of $T$. Every extremal graph has this description relative to each maximum independent set $S$.

This is a surjective construction of unmarked isomorphism classes, not a claimed bijection. A graph may admit more than one choice of $S$.

## 1. Construction exists and is regular

The fiber sizes are nonnegative, and the handshaking identity for a tree gives

$$\sum_t(\deg_T(t)-1)=2k-(k+1)=k-1.$$

Thus a partition exists. Every vertex of $S$ has degree $k$. A vertex $t$ has degree

$$\deg_G(t)=\deg_T(t)+(k-1)-|S_t|=k.$$

Consequently the graph has $2k$ vertices and $k^2$ edges.

## 2. Independence number

A nonstar tree of order $k+1$ has independence number at most $k-1$. Indeed, an independent set of size $k$ would leave one vertex, and every edge would meet that vertex. Connectedness would then force a star. Also $\deg_T(t)\le k-1$ for every $t$.

An independent set inside $S$ has size at most $k-1$. One inside $T$ has the same bound. If it meets both parts, choose one of its vertices in $S$. That vertex has exactly one nonneighbor in $T$, so the independent set contains exactly one tree vertex $t$. Its other vertices belong to $S_t$, and its size is at most

$$1+|S_t|=\deg_T(t)\le k-1.$$

Since $S$ is independent of size $k-1$, $\alpha(G)=k-1$.

## 3. Connectivity, including the two-vertex residual case

Let $X\subseteq V(G)$ with $|X|<k$. Write $A=S\setminus X$ and $B=V(T)\setminus X$. As $|V(T)|=k+1$, $|B|\ge2$.

If $A$ is empty, deleting all $k-1$ vertices of $S$ uses the entire allowed budget. No tree vertex is deleted, so $G-X=T$ is connected.

Suppose $A\ne\varnothing$ and $|B|\ge3$. Every vertex of $A$ is adjacent to all but at most one member of $B$. Any two vertices of $A$ therefore share a neighbor in $B$. They lie in a common component $C$, which also contains every vertex of $B$ adjacent to any member of $A$. At most one vertex $t\in B$ can lie outside $C$: any such vertex must be the unique missed vertex of every member of $A$. Thus $A\subseteq S_t$.

If that $t$ is disconnected from $C$, every tree neighbor of $t$ must have been deleted, because all other surviving tree vertices belong to $C$. Also all vertices of $S\setminus A$ were deleted. The two disjoint sets give

$$|X|\ge(k-1-|A|)+\deg_T(t)
\ge(k-1-|S_t|)+\deg_T(t)=k,$$

a contradiction.

It remains to treat $|B|=2$, say $B=\{u,v\}$. Exactly $k-1$ tree vertices were deleted, so $X$ contains no vertex of $S$ and $A=S$. If some member of $S$ misses a tree vertex other than $u,v$, it is adjacent to both surviving tree vertices. Every other member of $S$ is adjacent to at least one of them, so $G-X$ is connected.

Otherwise all nonempty fibers are $S_u$ and $S_v$. Every other tree vertex has degree one. Because $T$ is nonstar, it has at least two nonleaf vertices; hence $u,v$ are exactly its nonleaf vertices. They are adjacent: an internal vertex of their unique path would be a third nonleaf vertex. The edge $uv$ survives and joins every vertex of $S$ to one connected component. This proves $k$-connectivity in all cases.

## 4. Optimality and necessity of the characterization

Every $k$-connected graph has minimum degree at least $k$, so on $2k$ vertices it has at least $k^2$ edges. The construction achieves this bound, proving the value of $f$.

Now let $G$ be extremal and let $S$ be any maximum independent set, of size $k-1$. Equality in the degree bound forces every degree to be $k$. Let $H=G-S$, of order $k+1$. It is connected because $k-1<k$. Each vertex of $S$ has all its neighbors in $H$, so it misses exactly one vertex of $H$. Denote the corresponding fibers by $S_t$.

There are $k(k-1)$ edges between $S$ and $H$, leaving

$$e(H)=k^2-k(k-1)=k.$$

A connected graph with $k+1$ vertices and $k$ edges is a tree. At each $t$,

$$k=\deg_H(t)+(k-1)-|S_t|,$$

which gives the required fiber sizes. If $H$ were a star, its $k$ leaves would be an independent set in $G$, a contradiction. Hence $H$ is a nonstar tree, completing the characterization.

## 5. Scope and relation to the preceding boundary

Das-Gupta's [Corollary 3.3](https://arxiv.org/html/2608.18828v1) gives the preceding value $f(2k-1,k-1,k)=k^2-1$ for $k\ge4$. The new strip has exactly one more edge, while the gap above $\lceil nk/2\rceil$ changes from $\lfloor k/2\rfloor-1$ to zero. Equality changes from full joins with trees on $k$ vertices to the missing-neighbor construction with nonstar trees on $k+1$ vertices.

The numerical $k=3$ case was already covered by the original $n=k\alpha$ boundary. The infinite numerical extension begins at $k=4$. The entire first interior shell $n=\alpha+k+1$, the corrected first regime, and the second regime are not proved here.
