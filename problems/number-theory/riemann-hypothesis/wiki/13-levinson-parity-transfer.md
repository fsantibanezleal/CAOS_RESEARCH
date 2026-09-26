# Localized Levinson detector and the 0.534 onset

EXP-010 replaces the Selberg sign-change detector of EXP-005 and EXP-008 by
Levinson's, with Conrey's operator polynomial `Q` of any degree, on the
windows `(T,T+T^theta]`.

## Three results

**Short-window mollified moment (Theorem A).** For `1/2<theta<1`, a mollifier
of length `y=T^nu` with `nu<theta-1/2`, and a smooth weight equal to one on the
window with derivative scale `Delta=T^theta/log T`,

$$
\int w(t)\,|V\psi(\sigma_0+it)|^2dt=c(P,Q,R,\nu)\,\widehat w(0)+O(H/L),
$$

with Conrey's constant

$$
c(P,Q,R,\nu)=1+\frac1\nu\int_0^1\!\!\int_0^1
\bigl(w_R(v)P'(u)+\nu w_R'(v)P(u)\bigr)^2du\,dv,\qquad w_R=e^{Rv}Q(v).
$$

The proof is Young's short proof with three local changes: the off-diagonal
integration by parts (the only place where `nu<theta-1/2` is needed), the
reflected factor `X_{alpha,beta,t}` (the only use of `theta<1`), and the
contour shift (saving `T^(-delta(1-2nu))`).

**Distinct sign changes (Theorem B).** If `Q(0)=1` and `Q(x)+Q(1-x)=beta` is a
nonzero constant, then

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}\ge
\kappa=1-\frac1R\log c(P,Q,R,\nu),
$$

where `O` counts distinct sign changes of `Z`. The key facts are the exact
identity `beta Z=2Re(omega Vt)` with `Vt=V+E_beta/2`,
`E_beta=beta zeta-V-chi V(1-s)`, and a level-crossing count in which zeros of
`Vt` on the critical line carry full weight. For `deg Q>=3` the count does not
see simplicity; it sees odd order, which is what the parity product needs.

**Parity transfer (Theorem D).** Inserting `kappa` into the EXP-006 product
gives

$$
\liminf\frac{S}{N}\ge h(\theta;\kappa)=
\frac{3+\kappa-\sqrt{(1-\kappa)(9-\kappa-8c(\theta))}}4 .
$$

## Certified numbers

Degree-201 polynomials `Q` in a Chebyshev family and a truncated-`sinh` `P`
give `kappa>0.7170 nu` at eight frozen `nu` in `[0.0199,0.0999]`; the Selberg
slope is `1/(4eC_6)=0.140`. The exact form `c=A e^(2R)+B` with rational `A,B`
is certified in Arb and replayed by validated quadrature.

| `theta` | `nu` | `kappa>` | `h(theta;kappa)>` |
|---|---|---|---|
| 0.534 | 0.0339 | 0.0243176419 | 1.4806994e-5 |
| 0.535 | 0.0349 | 0.0250349766 | 0.0015246940 |
| 0.54 | 0.0399 | 0.0286216496 | 0.0090231376 |
| 0.5459 | 0.0458 | 0.0328539236 | 0.0177638490 |
| 0.55 | 0.0499 | 0.0357949954 | 0.0237708528 |

Every fixed `theta` in `[0.534,1)` therefore has a positive proportion of
simple critical zeros in `(T,T+T^theta]`. The previous onsets were `0.552`
(Steuding), `0.55019` (Wang) and `0.5458838` (EXP-008). At `theta=0.5459` the
bound is about 1000 times the EXP-008 value. Above about `theta=0.567`
Wang's `c(theta)` remains the largest term.

## Dependencies and limits

Theorems A and B use only Young's argument and classical tools. Theorem D uses
Wang's short-interval pair theorem (arXiv:2609.07918v1, recent and unreviewed)
through the EXP-006 product. The results are asymptotic, have no effective
starting height, and do not prove RH. The onset is limited by the mollifier
range; a Steuding-type range `nu<(3theta-1)/4` for general `Q` would make the
positivity condition hold for every `theta>1/2`.

- [Complete proof](../experiments/EXP-010-levinson-parity-transfer/mathematical-proof.md)
- [Adversarial audit](../experiments/EXP-010-levinson-parity-transfer/adversarial-audit.md)
- [Verdict](../experiments/EXP-010-levinson-parity-transfer/verdict.md)
- [Preflight dossier](../context/2026-09-26-levinson-localization-preflight.md)
