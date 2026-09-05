# 3. Missing-neighbor fibers

Let $T$ be a nonstar tree on $k+1$ vertices and $S$ an independent $(k-1)$-set. Partition $S$ into $S_t$ with $|S_t|=\deg_T(t)-1$. Join each $S_t$ to every tree vertex other than $t$. The identity

$$\sum_t(\deg_T(t)-1)=2k-(k+1)=k-1$$

makes the partition possible, and

$$\deg_G(t)=\deg_T(t)+k-1-|S_t|=k$$

makes the graph regular. A mixed independent set has at most $1+|S_t|=\deg_T(t)\le k-1$ vertices. A star would violate the required independence number.

![Missing-neighbor construction](assets/tree-strip.svg)

Connectivity has two cases. With at least three surviving tree vertices, the surviving independent-set vertices share a connected component and at most one tree vertex could be outside it. Isolating that vertex costs at least $k$ deletions. With exactly two surviving tree vertices, all independent-set vertices survive; if no vertex joins both, those tree vertices are the two internal vertices of a double star, whose edge reconnects them.

Conversely, degree-sum equality forces regularity. Deleting any maximum independent set leaves a connected $(k+1)$-vertex graph with $k$ edges, hence a tree. The fiber sizes follow from regularity. See the [full proof](../experiments/EXP-001-tree-strip/proof.md) for every quantifier and case.

## Extension beyond the tree strip

The full shell uses a residual graph on $k+1$ vertices and an independent set of size $\alpha$. Its constructions split into complement cycles ($\alpha=2$), the crown graph ($\alpha=k+1$), a residual matching ($\alpha=k$), the preserved tree strip ($\alpha=k-1$), and Harary graphs with a matching added in their complements for the remaining cases. Missing-neighbor fibers adjust degrees so the final edge count reaches the degree-sum bound, including odd parity.

The [EXP-002 proof](../experiments/EXP-002-next-shell/proof.md) supplies the matching bound, cyclic-gap connectivity argument, exact independence number, and deletion cases. Its $\alpha=2$ classification follows by forcing a 2-regular complement: triangles violate independence and 4-cycles violate connectivity; cycles of length at least five suffice. General residual graphs replace trees, so the original tree characterization is retained only on its own strip.
