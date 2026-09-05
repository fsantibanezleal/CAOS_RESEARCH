# Bougard-Joret and triangle-free extremal research

Updated: 2026-09-05, next-matching continuation.

[D] EXP-003 proves $T(d,d+1)=d^2+d+2$ for every integer $d\ge7$, where $T(d,m)$ is the maximum edge count of a triangle-free graph with maximum degree at most $d$ and matching number at most $m$. The same bound is sharp at fixed order $2d+3$. The new contribution is the uniform upper bound; the attaining construction is due to Banak, Ekim, and Taskin (BET). In particular, $T(13,14)=184$, closing the 184-to-185 interval in their Table 3.

| Result | Authority and scope |
|---|---|
| Next triangle-free matching level, all $d\ge7$ | [EXP-003 proof](experiments/EXP-003-triangle-free-next-matching/proof.md); solves this slice, not the full AEY conjecture |
| $d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2$ | EXP-003 secondary consequence; the exact endpoint remains undetermined |
| Full first interior shell $n=\alpha+k+1$ | [EXP-002 proof](experiments/EXP-002-next-shell/proof.md); preserved, including all alpha-two extremizers |
| Adjacent tree strip $f(2k,k-1,k)=k^2$ | [EXP-001 proof](experiments/EXP-001-tree-strip/proof.md); preserved with its complete nonstar-tree classification |

The [next-matching source review](context/2026-09-05-next-matching-review.md) extends the earlier portfolio refresh and identifies the known construction, finite overlaps, published conjecture, and access limits. The [exact certificate](experiments/EXP-003-triangle-free-next-matching/artifacts/certificate.json) and [independent audit](experiments/EXP-003-triangle-free-next-matching/artifacts/independent-audit.json) both pass. Their 48 graphs and finite five-type checks support the written proof; they do not establish its universal quantifier.

The separate next-matching manuscript v0.01 is [published at DOI 10.5281/zenodo.22343022](https://doi.org/10.5281/zenodo.22343022), with [concept DOI 10.5281/zenodo.22343021](https://doi.org/10.5281/zenodo.22343021). Its [publication receipt](../../../manuscripts/bougard-joret/next-matching/publication-verification.json) verifies all 352,871 bytes against a fresh unauthenticated download and confirms the latest version. All seven pages passed visual review, no final LaTeX warnings remain, and 101 tests passed. Scoped integration is complete through research PR #255 and private mirror PR #613. The first-shell manuscript remains frozen at [published v0.02](https://doi.org/10.5281/zenodo.22341644) in `manuscripts/bougard-joret/tree-strip/`.

Navigation: [wiki](wiki/README.md), [operational handoff](../../../program/bougard-joret/RESUME.md), [state](../../../program/bougard-joret/state.md), and [backlog](../../../program/bougard-joret/backlog.md). The general Bougard-Joret problem and the full triangle-free matching conjectures remain open.
