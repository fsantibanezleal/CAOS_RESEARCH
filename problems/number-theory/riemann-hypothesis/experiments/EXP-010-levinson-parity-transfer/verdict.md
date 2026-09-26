# EXP-010 verdict: confirmed localized Levinson detector and onset 0.534

Date: 2026-09-26. Declared at `2f7aaa6b` (baseline
`7a0711adb7e0f93b3a9429f6304f74f8951f8d69`) before any runner, proof or
output existed. Canonical execution from clean commit
`3dba086fed900d5a828bb78182fc68541b641d8a`; counting-lemma controls from clean
commit `770003367350b04be70e672d076ba0e5d3d99ecf`.

**Verdict: confirmed, with one scope correction to Prediction A.**
Predictions A and B are proved in [`mathematical-proof.md`](mathematical-proof.md);
two independent referee passes found no fatal or major mathematical error.
Predictions C and D pass every frozen threshold in exact and ball arithmetic,
with an independent replay. Prediction A's parenthetical extension to an
arbitrary real `Q` is false as declared: the constant term is `Q(0)^2`, not
`1` (see below). Every polynomial used here has `Q(0)=1`, so no conclusion
changes. Theorem D is relative to Wang's short-interval pair theorem
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
`X_{alpha,beta,t}` and the support of the weight (`theta<1`), and the contour
shift (`nu<1/2`). For an arbitrary real `Q` the same proof gives the constant
`Q(0)^2+(1/nu) int int (w_R P'+nu w_R' P)^2`.

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
| 1. Complete proofs of (A) and (B) referenced to source lemmas, audit and referee review | Passed: internal audit and two independent referee passes (sound with minor fixes, all applied); see [`adversarial-audit.md`](adversarial-audit.md) and [`proof-review.json`](proof-review.json) |
| 2. Exact admissibility of every frozen set | Passed in `fmpq` arithmetic |
| 3. Exact `c=A e^(2R)+B`, Arb enclosures, relative radius below `1e-30` | Passed |
| 4. Directed evaluation of `c(theta)`, `h_L` and the EXP-008 comparison | Passed |
| 5. Independent replay by validated quadrature and `mpmath.iv` | Passed; all enclosures overlap |
| 6. Young and Conrey anchors | Passed |
| 7. Numerical controls for (B) | Passed: nine checks, including tight double-zero cases and failure of the strict variant |
| 8. SHA-256 binding | Passed; see below |

## Corrections to the declaration

The declaration is frozen; these corrections are recorded here and do not
change any frozen parameter, target or conclusion.

1. **Prediction A scope.** The declaration states (A) with the constant
   `c(P,Q,R,nu)`, whose first term is `1`, and adds that `Q` "need only be a
   real polynomial". The operator `Q(-L^-1 d/dalpha)Q(-L^-1 d/dbeta)` maps that
   term to `Q(0)^2`, so the extension is false when `Q(0)^2!=1` (for
   `P=0.7x+0.3x^2`, `Q=2-0.9x+0.4x^2`, `R=1.1`, `nu=0.2`: `61.0999...` against
   `58.0999...`). The proved general constant is `Q(0)^2+(1/nu)int int(...)^2`.
   (A) as used, with `Q(0)=1` for `1`, `1+x^j` and every frozen `Q`, is confirmed.
2. **Young numbering.** "Young, Lemmas 1-6" should read Theorem 2 and Lemmas
   3-7 of the rendered arXiv v1 (one counter for theorems and lemmas). The
   steps are the same; the proof cites the rendered numbers.
3. **Counting precedent.** The premise table cites Conrey-Iwaniec-Soundararajan
   (A.16)-(A.18) for the weight-one convention. CIS pass on-line zeros from the
   east side, which is weight zero. The precedent is Conrey 1989 eq. (32) with
   eqs. (40)-(41). The proof does not use CIS.

## Evidence

| Artifact | SHA-256 |
|---|---|
| `artifacts/canonical/result.json` | `74ed14a925bdd10f27d09d6fb23a8e43f9474f8e0e5280fceafac33e06f49464` |
| `artifacts/canonical/execution-receipt.json` | `e0270d54d2003636648b0bd2981a5985fc941f3a36dc2b6ab10f2f26a632666e` |
| `artifacts/audit/audit.json` | `b3a5fa0ae2ea54bcd1c4f323acfae3c81c87202780018ea8c29e798c674a4df1` |
| `mathematical-proof.md` (bound by the audit) | `d7fed000d944c4a57d83c9505e229ee3453829bb4632e6d1c01df2339502323e` |
| `artifacts/controls/controls.json` | `6ecab20fcd1c90632d2d4c20c9fe41ae51e40e05eee0e1540c82e9934aea375c` |
| `hypothesis.md` | `4d4a6051f155c99d296cfa43fed972c844c01cede93bef25b61fcfe6147514de` |
| `frozen-parameters.json` | `602ab84cb40c4ebc786d33fba1c0976e5fa8f9b4c072e20a65d09a2a24fa2e4d` |
| `run.py` | `b6ee96ce409150f56f9c34757354e1addb417d2fc1be7c7e281a2c97ee1a27df` |

The producer ran in 1.63 s of a 900 s budget, the audit in 14 s of 1800 s,
and the controls in 590 s of 1800 s, all on CPU. The audit was rerun after the
referee fixes so that it binds the final proof; its numbers are unchanged.

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
