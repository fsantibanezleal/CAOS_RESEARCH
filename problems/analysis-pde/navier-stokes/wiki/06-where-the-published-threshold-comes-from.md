# 6. Where the published threshold comes from

The hypodissipative threshold that bounds this whole program is
$\alpha_0=(22-8\sqrt7)/9=0.09267$, proved by Cordoba, Martinez-Zoroa and Zheng
([ARMA 250 (2026) article 38](https://doi.org/10.1007/s00205-026-02198-0),
[arXiv:2407.06776](https://arxiv.org/abs/2407.06776)): for every dissipation exponent below it, forced
finite-time blowup, with a force in $L^1_tC^{1,\epsilon}_x\cap L^\infty_tL^2_x$.

Their own introduction gives a back-of-the-envelope number, $5-2\sqrt6=0.10102$, and says plainly that
the real calculation has other error sources. This page reconstructs the real one. Everything below is
their construction and their exponents; what is added here is which constraint sets the constant and
why the heuristic misses it. Full derivation, with the sections read:
[`context/2026-09-14-threshold-reconstruction.md`](../context/2026-09-14-threshold-reconstruction.md).

**Convention.** This page uses THEIR $|\nabla|^\alpha$, so classical viscosity is $\alpha=2$ and
$\alpha_0$ is twice the value in [page 4](04-dissipation-and-the-frequency-cap.md)'s convention.

## Everything is a power of one base

The vorticity is an infinite sum of vortex layers, each far more concentrated than the last, and every
quantity is $N$ raised to a power that grows like $R^n$:

| quantity | form |
|---|---|
| frequency of layer $n$ | $M_n=N^{R^n}$, so $M_{n+1}=M_n^R$ |
| amplitude | $A_n=N^{aR^n}$ |
| localization scale | $L_n=N^{bR^n}$ |
| force regularity headroom | $s>0$, the Holder margin of the force |

So the whole design is four numbers $(R,a,b,s)$, and the theorem exists exactly when a positive $s$
can be found.

## Four constraints, and the one that binds

Section 4.3 of the paper estimates the force each layer needs. Written as exponent inequalities:

| | source | constraint |
|---|---|---|
| **D** dissipation | 4.3.5 | $a=\alpha R$ |
| **S** self-interaction | 4.3.2 | $2a-\dfrac{a}{R}+b+s-1\le0$ |
| **L** localization | 4.3.3 | $b\ge a+\dfrac1R+s$ |
| **O** outer velocity on the inner layer | 4.3.4 | $a+\dfrac2R+s+1-3b\le0$ |

**D** says the layer must outrun its own dissipation, and it is saturated at every $\alpha$: that
equality is the same statement as the frequency cap of [page 4](04-dissipation-and-the-frequency-cap.md).
**S** saturated then fixes $b=1+\alpha-2\alpha R-s$, and substituting into **O** leaves a single
inequality in $(\alpha,R,s)$:

$$\boxed{\;4s<2+3\alpha-7\alpha R-\frac2R\;}$$

Maximizing the right-hand side over the frequency ratio gives $7\alpha=2/R^2$, that is

$$\alpha R^2=\frac27,\qquad R=\sqrt{\frac{2}{7\alpha}},$$

**exactly the ratio the paper chooses**, and at that optimum $7\alpha R+2/R=2\sqrt{14\alpha}$, so

$$s(\alpha)=\frac{2+3\alpha-2\sqrt{14\alpha}}{4},$$

which is the paper's formula for $s$. Then $s>0$ is $9\alpha^2-44\alpha+4>0$, whose smaller root is

$$\alpha_0=\frac{22-8\sqrt7}{9}.$$

No coefficient anywhere in that chain is fitted; each comes from a displayed exponent in Section 4.3.

## The heuristic differs by one swap

At the published point the localization constraint **L** is NOT active. Its margin is

$$b-\Big(a+\frac1R+s\Big)=\frac12\Big(\sqrt{\frac{2\alpha}{7}}-\alpha\Big)=0.0350\ \text{at }\alpha_0,$$

positive for all $\alpha<2/7$. The introduction's heuristic keeps **D**, **S** and **L** and does not
contain **O** at all. Saturating **L** instead and optimizing the same way gives

$$2s\le1+\alpha-3\alpha R-\frac1R,\qquad \alpha R^2=\frac13,\qquad
s(\alpha)=\frac{1+\alpha}{2}-\sqrt{3\alpha},\qquad \alpha<5-2\sqrt6 .$$

**The entire gap between $0.1010$ and $0.0927$ is which constraint binds.** The heuristic's binder is
slack in the proof; the proof's binder is absent from the heuristic. That also says what would have to
change for the threshold to move: a better treatment of the outer layers' velocity acting on the inner
layer, nothing else.

## What else the same inequality says: the frequencies must grow super-geometrically

The budget above is a quadratic in the frequency ratio. A positive force margin needs

$$7\alpha R^{2}-(2+3\alpha)R+2<0,$$

so the admissible ratios form an interval $(R_-,R_+)$ with

$$R_\pm=\frac{(2+3\alpha)\pm\sqrt{9\alpha^{2}-44\alpha+4}}{14\alpha}.$$

The discriminant is **exactly** the polynomial whose root is $\alpha_0$. So the interval of admissible
frequency ratios closes to a single point precisely at the published threshold, and that point is the
paper's own $R=\sqrt{2/(7\alpha)}$:

| $\alpha$ | admissible $R$ | the paper's choice |
|---|---|---|
| $0.001$ | $(1.002,\ 285.1)$ | $16.90$ |
| $0.01$ | $(1.021,\ 27.98)$ | $5.345$ |
| $0.05$ | $(1.143,\ 5.000)$ | $2.390$ |
| $\alpha_0=0.09267$ | $\{1.7559\}$ | $1.7559$ |
| $0.10$ | empty | none |

**The lower end is above 1 at every positive $\alpha$.** A cascade whose frequencies grow
geometrically, so that $\log M_n$ is linear in $n$, is the case $R=1$, and there the margin is exactly
$-\alpha$: negative for every viscosity. Read off the constraints directly, $R=1$ forces
$b\ge a+1+s$ from localization and $b\le1-a-s$ from self-interaction, so $\alpha+s\le0$.

**The construction does not merely prefer super-geometric frequency growth, it requires it**, and
requires more of it as the dissipation rises, until at $\alpha_0$ only one ratio is left. That is a
statement about our own cascade model too: its schedule is geometric, so a rigorous version of it
would have to move to $M_{n+1}=M_n^{R}$ before a force budget could close.

Checked in exact arithmetic in CI (the discriminant identity and the $R=1$ exclusion) and numerically
in [`code/tests/test_cmz_budget.py`](../code/tests/test_cmz_budget.py).

## Two things this does not say

It is exponent bookkeeping, with $\delta\to0$, logarithms dropped and constants ignored. It reproduces
the authors' own stated choices of $R$, $s$, $b$ and their own slackness remark, which is good evidence
that the transcription is right, but it is not a re-proof of their theorem. And the authors evidently
know which estimate binds, since they chose $R$ and $s$ accordingly; what is made explicit here is the
optimization and the heuristic-versus-proof swap.

## The round-1 claim this replaces

[EXP-003](../experiments/EXP-003-threshold-sweep/verdict.md) inverted our own cascade relation
$\alpha_c=1/(4p)$ at the published threshold and found $p=11/4+\sqrt7$ exactly, and two reasons were
given for that being informative. **Both are withdrawn.** The relation IS constraint **D** saturated,
and the construction saturates **D** at every $\alpha$, so $2p=1/\alpha$ holds identically along the
family; evaluating it at $\alpha_0$ says nothing about $\alpha_0$. And the clean algebraic form is
automatic: $\alpha_0\in\mathbb{Q}(\sqrt7)$, inverses stay there, and the result is tidy only because
the norm of $22-8\sqrt7$ is $36$.

Verified in exact arithmetic in CI (`tests/test_navier_stokes_threshold.py`) and numerically in
[`code/tests/test_cmz_budget.py`](../code/tests/test_cmz_budget.py): at five values of $\alpha$ the
paper's $R$ is the strict maximizer of the **O** budget, and at the published point **D**, **S** and
**O** bind while **L** holds.

## Next

[7. Steering and the holding interval](07-steering-and-the-holding-interval.md).
