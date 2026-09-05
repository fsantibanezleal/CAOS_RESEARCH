# 1. Statement and history

For finite simple graphs, $f(n,\alpha,k)$ is the minimum edge count under order $n$, independence number exactly $\alpha$ and vertex connectivity at least $k$. For $n\ge2\alpha$, $n\ge\alpha+k$, $\alpha\ge2$, $k\ge3$, Bougard-Joret proposed a degree-sum formula in the regime $n\le k\alpha$ and a clique-union correction beyond it. See their [2008 primary paper](https://doi.org/10.1002/jgt.20289), Section 6.

Das-Gupta's [2026 preprint](https://arxiv.org/html/2608.18828v1) disproves the first formula and determines the boundary $n=\alpha+k$. That discovery remains theirs. EXP-001 studies one vertex above their exceptional family: $(2k,k-1,k)$.

EXP-002 extends the scope to the full first interior shell. For every $k\ge3$ and $2\le\alpha\le k+1$,

$$f(\alpha+k+1,\alpha,k)=\left\lceil\frac{k(\alpha+k+1)}2\right\rceil.$$

For $\alpha=2$, every extremal graph is the complement of a disjoint union of cycles of lengths at least five. The [EXP-002 proof](../experiments/EXP-002-next-shell/proof.md) owns the all-parameter statements; its [verdict](../experiments/EXP-002-next-shell/verdict.md) owns audit status. The general first and second regimes remain open.

## The triangle-free matching continuation

The complement viewpoint leads to a different extremal quantity: $T(d,m)$ is the maximum edge count in a triangle-free graph with maximum degree at most $d$ and matching number at most $m$. It is not the Bougard-Joret function $f(n,\alpha,k)$.

The [EXP-003 proof](../experiments/EXP-003-triangle-free-next-matching/proof.md) establishes, for every integer $d\ge7$,

$$T(d,d+1)=d^2+d+2.$$

This is the next-matching slice of the intermediate-range conjecture of Ahanjideh, Ekim, and Yildiz. The same expression is the sharp edge maximum for triangle-free graphs of order $2d+3$ and maximum degree at most $d$. Complementation supplies the separate consequence

$$d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2.$$

The exact Bougard-Joret endpoint and the full matching conjecture remain undetermined here. The [source review](../context/2026-09-05-next-matching-review.md) distinguishes the new upper-bound proof from the known BET construction and finite values.
