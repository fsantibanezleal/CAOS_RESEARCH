# EXP-010: localized Levinson-Conrey sign changes and the parity onset

Declared: 2026-09-26. Device: CPU. Baseline: public `develop` commit
`7a0711adb7e0f93b3a9429f6304f74f8951f8d69` and release `v0.73.000`.

Status at declaration: the primary sources in the
[preflight dossier](../../context/2026-09-26-levinson-localization-preflight.md)
were read in full or in the cited sections. Exploratory, non-authoritative
scratch computations (a) reproduced the published Levinson-Conrey constants of
Young and Conrey, (b) checked the sign-change identity numerically at
`T=10^4,10^5,10^6`, and (c) selected the parameter sets in
[`frozen-parameters.json`](frozen-parameters.json), whose field
`exploratory_kappa_lower` records the scratch Arb values. No EXP-010 runner,
proof, audit, or canonical artifact exists. This declaration is committed and
pushed before implementation and canonical computation.

## Question

EXP-005 and EXP-008 feed the EXP-006 Hilbert-parity product with a localized
Selberg sign-change detector whose odd-support density is
`k_q(theta)=(theta-1/2)/(4eC_q)`, about `0.14(theta-1/2)`. Its onset is pinned
near Wang's pair-term root because that slope is small.

Can Levinson's method, with Conrey's general operator polynomial `Q` and a
mollifier of length `T^nu`, be localized to every interval `(T,T+T^theta]`,
`1/2<theta<1`, whenever `nu<theta-1/2`, as a lower bound for the number of
DISTINCT sign changes of Hardy's function? If so, does its explicit density
replace `k_q` in the unchanged EXP-006 product and move the simple-critical
short-interval onset from `(0.5458837,0.5458838)` to at most `0.534`?

## Frozen definitions

Let `L=log T`, `H=T^theta`, `y=T^nu`, and `sigma_0=1/2-R/L` with fixed `R>0`.
`P` is a real polynomial with `P(0)=0`, `P(1)=1`. `Q` is a real polynomial with
`Q(0)=1` and `Q(x)+Q(1-x)=1` identically. Put

$$
V(s)=Q\Bigl(-\frac1L\frac{d}{ds}\Bigr)\zeta(s),\qquad
\psi(s)=\sum_{h\le y}\frac{\mu(h)}{h^{s+1/2-\sigma_0}}
P\Bigl(\frac{\log(y/h)}{\log y}\Bigr),
$$

$$
c(P,Q,R,\nu)=1+\frac1\nu\int_0^1\!\!\int_0^1
\bigl(w(v)P'(u)+\nu w'(v)P(u)\bigr)^2\,du\,dv,\qquad w(v)=e^{Rv}Q(v),
$$

and `kappa(P,Q,R,nu)=1-R^{-1}log c(P,Q,R,nu)`. This is the Conrey 1989
Theorem 2 constant, in the form of Young (1.3) and CFKL (15)-(16), with the
mollifier exponent written `nu`. Let `O(T,H)` be the number of DISTINCT
`t in (T,T+H]` at which `Z(t)` changes sign. Each such point is a critical zero
of odd multiplicity, so `O(T,H)` is a lower bound for the EXP-006 odd-support
count.

## Prediction A: short-interval mollified moment

Fix `theta in (1/2,1)`, `nu in (0,theta-1/2)`, `R>0`, and polynomials `P`, `Q`
(for this prediction `Q` need only be a real polynomial). Put `Delta=H/L` and let
`w` be smooth with `0<=w<=1`, support in `[T-Delta,T+H+Delta]`, `w=1` on
`[T,T+H]`, and `w^(j)<<_j Delta^(-j)`. Then

$$
\int_{\mathbb R}w(t)\,|V\psi(\sigma_0+it)|^2\,dt
=c(P,Q,R,\nu)\,\widehat w(0)+O(H/L).
\tag{A}
$$

The proof must adapt Young, arXiv:1002.4403v1, Lemmas 1-6: the only permitted
changes are the smoothing scale `Delta=H/L` and the off-diagonal condition
`hk<=Delta^2T^(-1-epsilon)`, which holds for `h,k<=y` exactly because
`nu<theta-1/2`. Every other error must be shown to scale with `w-hat(0)`.

## Prediction B: distinct sign changes and the localized Levinson bound

Let `beta=Q(0)+Q(1)`, which is nonzero; every frozen `Q` has `beta=1` exactly.
With `omega=chi(1/2+it)^(-1/2)`, `E_beta=beta*zeta-V-chi(s)V(1-s)` and
`Vt=V+E_beta/2`, `omega E_beta` is real on the critical line and
`beta Z(t)=2Re(omega Vt)` holds exactly. Zeros of `Vt` on the line are charged
with full weight (detours pass west of them). The level-crossing count of a
continuous argument then gives

$$
O(T,H)\ge N(T,H)-2N_{Vt}(\sigma\ge\tfrac12;T,T+H)-O(L),
$$

where `N_Vt` counts zeros with multiplicity, including those on the line. The
exact expansion of `chi(s)V(1-s)` through `chi(s)chi(1-s)=1` writes `E_beta` as a
fixed combination of `L^(-j)zeta^(j)` with coefficients `O(1/L)`, so (A) applied
to monomials gives `int w|psi E_beta|^2=O(H/L^2)`. Littlewood's lemma on
`[sigma_0,sigma_1]x[T,T+H]`, Jensen's inequality and (A) then give, for every
fixed `theta`, `nu`, `P`, `Q`, `R` as above,

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}\ge\kappa(P,Q,R,\nu).
\tag{B}
$$

(B) counts distinct odd-order critical zeros. It is not a multiplicity-weighted
critical-mass count.

## Prediction C: certified detector constants

For each parameter set in `frozen-parameters.json` (degree-201 `Q` in the
Chebyshev family `Q(y)=1-y+sum x_j(T_(2j+1)(1-2y)-(1-2y))`, `x_j` rational over
`10^40`; `P(x)=S_13(rx)/S_13(r)` with `S_13` the degree-13 Taylor polynomial of
`sinh`; rational `R`, `r`, `nu`), exact rational arithmetic confirms the
constraints and Arb certifies

$$
\kappa>0.7170\,\nu
\qquad(\nu\in\{0.0199,0.0299,0.0339,0.0349,0.0399,0.0458,0.0499,0.0999\}).
\tag{C}
$$

In particular `kappa(0.0339)>0.0243` and `kappa(0.0349)>0.0250`, against the
EXP-008 Selberg densities `k_6(0.534)<0.00477` and `k_6(0.535)<0.00491`.

## Prediction D: earlier simple-critical onset

With Wang's pair term `c(theta)=2-theta/2-(1/sqrt2)cot(theta/sqrt2)` and
`k=kappa`, put

$$
h_L(\theta)=\frac{3+k-\sqrt{(1-k)(9-k-8c(\theta))}}4 .
$$

The EXP-006 product is independent of the odd-support detector, so (B) gives

$$
\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
\ge\max\Bigl\{0,c(\theta),\frac{c(\theta)+2k}3,h_L(\theta)\Bigr\}.
\tag{D}
$$

Directed interval arithmetic must prove, with `nu=theta-1/2-10^(-4)`:

- `h_L(0.534)>1.0e-5`; hence, because `c` increases with `theta` and the same
  `nu` stays admissible, every fixed `theta>=0.534` has a positive proportion of
  simple critical zeros in `(T,T+T^theta]`;
- `h_L(0.535)>0.0015`, `h_L(0.54)>0.0090`, `h_L(0.5459)>0.0177`,
  `h_L(0.55)>0.0237`, and `h_L(0.60)>0.0929`.

At `theta=0.5459` the bound must exceed the EXP-008 value `1.7764e-5` by a factor
above 900. The unconstrained numerical onset of the `0.7173 nu` curve, about
`0.53399`, is recorded only as context, not claimed.

## Required exact checks

1. Complete written proofs of (A) and (B), each step referenced to the source
   lemma it adapts, with an adversarial audit and an independent proof review.
2. Exact rational verification of `P(0)=0`, `P(1)=1`, `Q(0)=1`,
   `Q(x)+Q(1-x)=1` for every frozen set.
3. Exact reduction `c=A e^(2R)+B` with rational `A,B`; Arb enclosures of `c` and
   `kappa` with outward rounding and relative radius below `1e-30`.
4. Directed interval evaluation of `c(theta)`, `h_L`, and the EXP-008 comparison.
5. Independent replay: `c` by rigorous Arb double integration of the original
   integrand (not the moment reduction), and `c(theta)`, `h_L` by `mpmath.iv`
   at 100 digits; enclosures must overlap.
6. Reproduce the published anchors: Young `c=2.3500677...` (`P=x`, `Q=1-x`,
   `R=1.3`, `nu=1/2`) and Conrey's `0.4088...` (note added in proof).
7. Adversarial numerical controls for (B): the exact identity at several heights
   and degrees, and toy functions with planted double and triple critical zeros
   where the bound must hold, double zeros must not be counted, and the
   strict-inequality (`sigma>1/2`) variant must fail.
8. Bind sources, this declaration, the frozen file, runner, and outputs by
   SHA-256.

## Premise dependencies

| Premise | Status and support |
|---|---|
| EXP-006 product `(Q-S)(N-O)>=2(N-S)^2` with `O` the distinct odd-support count | Confirmed, EXP-006 verdict |
| Wang's short-interval pair term `c(theta)` for fixed `0<lambda<theta<1` | Attributed, arXiv:2609.07918v1; audited in `context/2026-09-12-wang-transfer-audit.md` and used by EXP-004 to EXP-009 |
| Young's approximate functional equation, twisted lemma, and main-term lemmas | Published, Arch. Math. 95 (2010); the short-interval adaptation is part of this experiment |
| Conrey 1989 Theorem 2 constant `c(P,Q,R,theta)` | Published; only the formula is used, re-derived symbolically in the preflight |
| Levinson counting with on-line zeros at weight one | Conrey 1989 eqs. (40)-(41); Conrey-Iwaniec-Soundararajan 2013 (A.16)-(A.18); the distinct sign-change sharpening is proved in this experiment |
| Littlewood's lemma, Jensen, Riemann-von Mangoldt, zero-free region and `1/zeta` bounds | Classical (Titchmarsh) |
| CFKL arXiv:2508.11108v1 | Motivation and `Q` family only; no CFKL theorem is a premise because `kappa` is certified directly |

The record's warning that critical-MASS inputs cannot feed the product (dossier
`2026-09-12-critical-mass-and-multiplicity-route.md`) is addressed by (B), which
counts distinct sign changes. The warning that high-degree `Q` loses the
simple-zero refinement is respected: (B) claims odd order only, and simplicity
comes solely from the EXP-006 product.

## What PASS and FAIL prove

PASS requires the complete proofs of (A) and (B) surviving adversarial review,
and certified (C) and (D). It proves that every fixed `theta>=0.534` has a
positive proportion of simple critical zeros in every sufficiently high interval
of length `T^theta`, together with the stated densities.

A failure of (A) blocks the localization at this mollifier range and is recorded
with its exact obstruction; (C) then remains only a certified constant. A failure
of (B), meaning the count cannot be separated from multiplicity, refutes the use
of Levinson's method in the parity product. Certified numbers with an incomplete
proof are supporting evidence only and do not authorize a theorem or manuscript
claim.

## Invariant-first note

The onset reduces to one scalar inequality, `k>1-2/A(theta)` with
`A=2-c`. At `theta=0.534` it needs `k>0.0242958`; the exploratory scratch value
of `kappa(0.0339)` is `0.0243176`. The qualitative invariant for (B) is whether
the detector counts distinct sign changes or multiplicity-weighted mass; the
preflight checked it on toy functions with planted double and triple zeros,
where the count is tight and double zeros are never counted.

## Compute budget and stop rules

CPU only. The canonical runner is capped at 900 seconds and the independent
audit at 1800 seconds, both flushing one line per parameter set. No GPU workload
is justified. A failed exact constraint, an unresolved enclosure, a missed
frozen threshold, or a failed independent overlap gives `inconclusive` for the
affected prediction. It does not permit changing the frozen file, targets, or
`nu` without a new committed declaration.

## Novelty and claim boundary

The Conrey constant, Young's method, CFKL's high-degree `Q`, Wang's pair term and
the EXP-006 product are prior results. The proposed contribution is the
localization of Levinson's method with general `Q` to every interval of length
`T^theta` for `nu<theta-1/2`, its use as a distinct sign-change count, the
combination with the Hilbert-parity product, the certified constants, and the
resulting onset. A bounded source search located Steuding's localization for
`Q(x)=1-x` (simple zeros for `H>=T^0.552`) and Conrey's Gaussian-window
proposition (effective only for `theta>6/7+nu/4`), but no localization with
general `Q` and no coupling of a Levinson count to a parity product. This is not
an exhaustive priority determination. The results are asymptotic, give no
effective starting height, rely on recent unreviewed preprints for the pair
term, and do not prove RH.
