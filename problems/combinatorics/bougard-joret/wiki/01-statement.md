# 1. Statement and history

For finite simple graphs, $f(n,\alpha,k)$ is the minimum edge count under order $n$, independence number exactly $\alpha$ and vertex connectivity at least $k$. For $n\ge2\alpha$, $n\ge\alpha+k$, $\alpha\ge2$, $k\ge3$, Bougard-Joret proposed a degree-sum formula in the regime $n\le k\alpha$ and a clique-union correction beyond it. See their [2008 primary paper](https://doi.org/10.1002/jgt.20289), Section 6.

Das-Gupta's [2026 preprint](https://arxiv.org/html/2608.18828v1) disproves the first formula and determines the boundary $n=\alpha+k$. That discovery remains theirs. EXP-001 studies one vertex above their exceptional family: $(2k,k-1,k)$.

EXP-002 extends the scope to the full first interior shell. For every $k\ge3$ and $2\le\alpha\le k+1$,

$$f(\alpha+k+1,\alpha,k)=\left\lceil\frac{k(\alpha+k+1)}2\right\rceil.$$

For $\alpha=2$, every extremal graph is the complement of a disjoint union of cycles of lengths at least five. The [EXP-002 proof](../experiments/EXP-002-next-shell/proof.md) owns the all-parameter statements; its [verdict](../experiments/EXP-002-next-shell/verdict.md) owns audit status. The general first and second regimes remain open.
