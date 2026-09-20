# EXP-008 verdict: confirmed rank-six local transfer

Date: 2026-09-20. The declaration was committed at `2297d2fc` before the
EXP-008 runner and authoritative computation. The canonical certificate ran
from clean commit `5f4885c70188a7126f0b47ea954e589a7583b358`.

**Verdict: confirmed relative to the attributed rank-six source input.** The
localization and downstream exact consequences pass internal adversarial
review. Pearce-Crump's six-square coefficient matrix is not printed, so this is
not an independent reconstruction of the imported `C_6` certificate. It does
not establish external acceptance, an effective starting height, or RH.

## Confirmed local theorem

[D] For every fixed finite-rank admissible vector profile `q` covered by
Pearce-Crump's vector-profile theorem, with diagonal constant `C[q]`, and every
fixed `1/2<theta<1`,

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{\theta-1/2}{4eC[q]}.
\tag{1}
$$

The proof extends EXP-005 componentwise. Fixed finite rank changes constants,
not the short-interval exponent. Applying (1) to Pearce-Crump's stated
six-square profile gives

$$
k_6(\theta)=\frac{\theta-1/2}{4eC_6},
$$

where

$$
C_6\in0.6566338678379319741683641732\pm5.63\cdot10^{-18}.
$$

## Confirmed earlier onset

[D] Combining (1) with the EXP-006 finite Hilbert-parity product gives

$$
\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),\frac{c(\theta)+2k_6(\theta)}3,h_6(\theta)\right\},
\tag{2}
$$

where

$$
h_6(\theta)=\frac{3+k_6(\theta)-
\sqrt{(1-k_6(\theta))(9-k_6(\theta)-8c(\theta))}}4.
$$

[MV] Directed exact arithmetic proves the unique positivity onset satisfies

$$
\boxed{0.5458837<\theta_6<0.5458838.}
\tag{3}
$$

For comparison, the rank-three onset is certified in
`(0.5458846,0.5458847)`. Thus the new input moves the onset earlier. At the
separating exponent `theta=0.545884`, the previous term is negative while

$$
\boxed{h_6(0.545884)>
2.5541123454645702\mathbin{\cdot}10^{-7}.}
\tag{4}
$$

At `theta=0.5459`,

$$
\boxed{h_6(0.5459)>
0.0000177645181613023236390595079,}
\tag{5}
$$

and its improvement over the rank-three term exceeds

$$
9.2635430617773560\mathbin{\cdot}10^{-7}.
\tag{6}
$$

This is about a 5.5 percent relative increase at the frozen point and is the
material headline improvement of EXP-008.

## Optimized spectral companion

[D+MV] Reusing EXP-007 with `R=(11/5)/h_6` proves a strict full-curve spectral
correction. At `theta=0.5459`,

$$
H_6-h_6>
1.7766622541125682\mathbin{\cdot}10^{-68}.
\tag{7}
$$

This is more than one hundred times the published EXP-007 lower gain at the
same point. It remains too small to affect the displayed decimal in (5). Its
role is structural; the onset shift comes from the stronger independent
odd-support input.

## Evidence and replay

The canonical result is
[`artifacts/canonical/result.json`](artifacts/canonical/result.json), schema
`riemann-exp008-results-v1`, SHA-256
`56db06037e0b36ed519919c352fb0a5419e2b6ba29629d65948f399c1d3bf4ba`.
It records PASS from a clean commit in 64.406 seconds.

The runner validates pinned source hashes, directed rational intervals for both
rank-three and rank-six curves, disjoint fine onset brackets, the optimized
spectral reserve, and overlap with an independent 100-decimal `mpmath.iv`
implementation.

Replay from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-008-rank-six-local-transfer/run.py --output-dir tmp/riemann-exp008-replay --budget-seconds 120
python -m pytest -q tests/test_riemann_rank_six_local.py
```

## Manuscript decision

Integrate EXP-008 into manuscript v0.07. A split would duplicate the EXP-005
local rectangle and EXP-006/007 finite transfers. A separate paper becomes
appropriate if the rank-six coefficient matrix is released and independently
reconstructed, or if the rank-independent localization is developed for a
broader optimized profile family.

## Scope

The result is asymptotic and uses recent attributed preprints. It does not give
an effective height, a global best proportion, universal simplicity, or a proof
of the Riemann hypothesis.
