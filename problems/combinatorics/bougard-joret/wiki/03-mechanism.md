# 3. Missing-neighbor fibers

Let $T$ be a nonstar tree on $k+1$ vertices and $S$ an independent $(k-1)$-set. Partition $S$ into $S_t$ with $|S_t|=\deg_T(t)-1$. Join each $S_t$ to every tree vertex other than $t$. The identity

$$\sum_t(\deg_T(t)-1)=2k-(k+1)=k-1$$

makes the partition possible, and

$$\deg_G(t)=\deg_T(t)+k-1-|S_t|=k$$

makes the graph regular. A mixed independent set has at most $1+|S_t|=\deg_T(t)\le k-1$ vertices. A star would violate the required independence number.

![Missing-neighbor construction](assets/tree-strip.svg)

Connectivity has two cases. With at least three surviving tree vertices, the surviving independent-set vertices share a connected component and at most one tree vertex could be outside it. Isolating that vertex costs at least $k$ deletions. With exactly two surviving tree vertices, all independent-set vertices survive; if no vertex joins both, those tree vertices are the two internal vertices of a double star, whose edge reconnects them.

Conversely, degree-sum equality forces regularity. Deleting any maximum independent set leaves a connected $(k+1)$-vertex graph with $k$ edges, hence a tree. The fiber sizes follow from regularity. See the [full proof](../experiments/EXP-001-tree-strip/proof.md) for every quantifier and case.
