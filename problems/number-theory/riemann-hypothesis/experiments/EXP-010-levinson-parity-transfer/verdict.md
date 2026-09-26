# EXP-010 verdict draft: localized Levinson detector and onset 0.534

Date: 2026-09-26. Declared at `2f7aaa6b` (baseline
`7a0711adb7e0f93b3a9429f6304f74f8951f8d69`) before any runner, proof or
output existed. Canonical execution from clean commit
`3dba086fed900d5a828bb78182fc68541b641d8a`; counting-lemma controls from clean
commit `770003367350b04be70e672d076ba0e5d3d99ecf`.

**Status: pending referee review.** Predictions A and B are proved in
[`mathematical-proof.md`](mathematical-proof.md), and that proof is under two
independent referee passes. Predictions C and D pass every frozen threshold
in exact and ball arithmetic, with an independent replay. Theorem D is relative to Wang's short-interval pair theorem
(arXiv:2609.07918v1, a recent unreviewed preprint) through the confirmed
EXP-006 product.

## Confirmed theorems

**A. Short-window mollified moment.** For `1/2<theta<1`, `0<nu<theta-1/2`,
fixed `R>0`, real `P` with `P(0)=0`, `P(1)=1`, real `Q` with `Q(0)=1`, and a
smooth weight equal to one on `(T,T+T^theta]` with derivative scale
`Delta=T^theta/log T`,

$$
\int w(t)\,|V\psi(\sigma_0+it)|^2dt=c(P,Q,R,\nu)\,\widehat w(0)+O(H/L).
$$

The proof reruns Young's Lemmas 4-7. The window length enters only through
the off-diagonal integration by parts (`nu<theta-1/2`), the reflected factor
`X_{alpha,beta,t}` (`theta<1`) and the contour shift (`nu<1/2`).

**B. Distinct sign changes.** If moreover `Q(x)+Q(1-x)=beta` is a nonzero
constant, then

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}\ge
\kappa=1-\frac1R\log c(P,Q,R,\nu),
$$

where `O` counts distinct sign changes of `Z`. The count sees odd order, not
simplicity, for `deg Q>=3`.

**D. Parity transfer.** For every fixed `theta` in `[0.534,1)`,

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}\ge
\max\Bigl\{0,c(\theta),\frac{c(\theta)+2\kappa}3,h(\theta;\kappa)\Bigr\}>0,
$$

with `h(theta;k)=(3+k-sqrt((1-k)(9-k-8c(theta))))/4` and any certified `kappa`
with `nu<theta-1/2`.

## Certified numbers

| `nu` | `kappa` lower | `kappa/nu` lower |
|---|---|---|
| 0.0199 | 0.0142729911882 | 0.717235 |
| 0.0299 | 0.0214483010716 | 0.717334 |
| 0.0339 | 0.0243176419798 | 0.717334 |
| 0.0349 | 0.0250349766522 | 0.717334 |
| 0.0399 | 0.0286216496468 | 0.717334 |
| 0.0458 | 0.0328539236725 | 0.717334 |
| 0.0499 | 0.0357949954879 | 0.717334 |
| 0.0999 | 0.0716640051800 | 0.717357 |

All eight pass `kappa>0.7170 nu`; `kappa(0.0339)>0.0243` and
`kappa(0.0349)>0.0250`, against `k_6(0.534)<0.00477` and `k_6(0.535)<0.00491`.
Every relative radius of `c` is below `1e-30`.

| `theta` | `nu` | `h(theta;kappa)` lower | frozen target |
|---|---|---|---|
| 0.534 | 0.0339 | 1.48069943748e-5 | 1.0e-5 |
| 0.535 | 0.0349 | 0.00152469402435 | 0.0015 |
| 0.54 | 0.0399 | 0.00902313762222 | 0.0090 |
| 0.5459 | 0.0458 | 0.0177638490344 | 0.0177 |
| 0.55 | 0.0499 | 0.0237708528879 | 0.0237 |
| 0.60 | 0.0999 | 0.0929528998664 | 0.0929 |

At `theta=0.5459` the ratio to the EXP-008 value `1.7764518e-5` exceeds
`999.962` (target 900). The Young anchor `c=2.35006777611844...` and Conrey's
`kappa>0.4088` are reproduced.

Scope of the gain: at every certified point with `theta<=0.55`, `c(theta)<0`
and `h` is the largest term. At `theta=0.60`, Wang's `c(0.60)=0.134554...`
exceeds `h`; the frozen target there holds but is not an improvement. With the
exploratory slope `0.7173`, `h` stays above `c` up to about `theta=0.567`.

## Required checks

| Check | Outcome |
|---|---|
| 1. Complete proofs of (A) and (B) referenced to source lemmas, audit and referee review | Proofs and internal audit written; referee passes in progress |
| 2. Exact admissibility of every frozen set | Passed in `fmpq` arithmetic |
| 3. Exact `c=A e^(2R)+B`, Arb enclosures, relative radius below `1e-30` | Passed |
| 4. Directed evaluation of `c(theta)`, `h_L` and the EXP-008 comparison | Passed |
| 5. Independent replay by validated quadrature and `mpmath.iv` | Passed; all enclosures overlap |
| 6. Young and Conrey anchors | Passed |
| 7. Numerical controls for (B) | Passed: nine checks, including tight double-zero cases and failure of the strict variant |
| 8. SHA-256 binding | Passed; see below |

The declaration cites "Young, Lemmas 1-6" for the approximate functional
equation, twisted and diagonal lemmas. In the rendered arXiv v1 these are
Lemmas 4-7 (Lemma 3 is the shifted-moment statement). The steps are the same;
only the numbering in the declaration is imprecise, and the proof cites the
rendered numbers.

## Evidence

| Artifact | SHA-256 |
|---|---|
| `artifacts/canonical/result.json` | `74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464` |
| `artifacts/canonical/execution-receipt.json` | `e0270d54d2003636648b0bd2981a5985fc941f3a36dc2b6ab10f2f26a632666e` |
| `artifacts/audit/audit.json` | `349f55bfaa92d9945b852aec92b1bdf113944d6c9e6dc7433f762390a97fe04e` |
| `artifacts/controls/controls.json` | `6ecab20fcd1c90632d2d4c20c9fe41ae51e40e05eee0e1540c82e9934aea375c` |
| `hypothesis.md` | `4d4a6051f155c99d296cfa43fed972c844c01cede93bef25b61fcfe6147514de` |
| `frozen-parameters.json` | `602ab84cb40c4ebc786d33fba1c0976e5fa8f9b4c072e20a65d09a2a24fa2e4d` |
| `run.py` | `b6ee96ce409150f56f9c34757354e1addb417d2fc1be7c7e281a2c97ee1a27df` |

The producer ran in 1.63 s of a 900 s budget, the audit in 14 s of 1800 s,
and the controls in 590 s of 1800 s, all on CPU.

Replay from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-010-levinson-parity-transfer/run.py --output-dir tmp/riemann-exp010-replay
python problems/number-theory/riemann-hypothesis/experiments/EXP-010-levinson-parity-transfer/audit.py --canonical tmp/riemann-exp010-replay/result.json --output-dir tmp/riemann-exp010-audit
python problems/number-theory/riemann-hypothesis/experiments/EXP-010-levinson-parity-transfer/controls.py --output-dir tmp/riemann-exp010-controls
python -m pytest -q tests/test_riemann_levinson_parity.py
```

## Manuscript decision and scope

Theorems A and B are standalone analytic results and change the method, not
only a constant, so they are written as a new manuscript,
`manuscripts/riemann-hypothesis/short-interval-levinson/`, which cites the
existing short-interval paper for the parity product.

The results are asymptotic, give no effective starting height, and do not
prove universal simplicity or the Riemann hypothesis. The bounded source
search found no prior short-window moment for general `Q` or sign-change
count for `deg Q>=3`; this is not a priority determination.
