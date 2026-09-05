# Bougard-Joret and the next triangle-free matching level

[D] EXP-003 proves $T(d,d+1)=d^2+d+2$ for every integer $d\ge7$, for triangle-free graphs with degree bound $d$ and matching budget $d+1$. The uniform upper bound is new in this research round; the attaining graph is the known BET construction. The theorem gives $T(13,14)=184$, resolving BET's 184-to-185 table interval. A secondary result bounds $f(2d+3,2,d+2)$ between $d^2+4d+1$ and $d^2+4d+2$; it does not determine which endpoint is attained.

[D] For every $k\ge3$ and $2\le\alpha\le k+1$, $f(\alpha+k+1,\alpha,k)=\lceil k(\alpha+k+1)/2\rceil$. For $\alpha=2$, all extremals are complements of disjoint cycles of lengths at least five. EXP-001's complete nonstar-tree characterization on $\alpha=k-1$ is preserved. The broader problem remains open; the shell contains explicitly identified prior cases.

1. [Statement and history](01-statement.md)
2. [Known results and scope](02-known-results.md)
3. [Construction and proof](03-mechanism.md)
4. [Exact experiments](04-experiments.md)
5. [Open questions](05-open-questions.md)

Current authority: [EXP-003 proof](../experiments/EXP-003-triangle-free-next-matching/proof.md), [certificate](../experiments/EXP-003-triangle-free-next-matching/artifacts/certificate.json), [independent audit](../experiments/EXP-003-triangle-free-next-matching/artifacts/independent-audit.json), and [next-matching source review](../context/2026-09-05-next-matching-review.md). The separate next-matching manuscript is [published v0.01](https://doi.org/10.5281/zenodo.22343022), concept DOI 10.5281/zenodo.22343021: seven pages, 352,871 public bytes verified, no final LaTeX warnings, and 101 tests passed. See the [publication receipt](../../../../manuscripts/bougard-joret/next-matching/publication-verification.json). Scoped integration is complete through research PR #255 and private mirror PR #613. The full AEY conjecture and general revised Bougard-Joret problem remain open.

Preserved authority: [EXP-002 proof](../experiments/EXP-002-next-shell/proof.md), [EXP-002 verdict](../experiments/EXP-002-next-shell/verdict.md), and [EXP-001 verdict](../experiments/EXP-001-tree-strip/verdict.md). [Earlier portfolio refresh](../context/2026-09-05-portfolio-refresh.md). The separate manuscript in `manuscripts/bougard-joret/tree-strip/` remains [published v0.02](https://doi.org/10.5281/zenodo.22341644), ten pages, with public bytes verified at publication. Its v0.01 DOI identifies the earlier strip result only.
