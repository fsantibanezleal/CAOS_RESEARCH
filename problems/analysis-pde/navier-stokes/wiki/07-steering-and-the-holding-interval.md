# 7. Steering, and what a holding interval costs

[Page 3](03-the-modulation-system.md) described the cycle in words: grow, steer, hold, repeat. This
page is the cycle as an implementable control, transcribed from Alpoge-Buckmaster Subsections 3.3 and
3.6.2, and run against the full nonlinear PDE in
[EXP-005](../experiments/EXP-005-steered-cycle/verdict.md).

The mechanism belongs to Cordoba and Martinez-Zoroa, and this control to Alpoge and Buckmaster.
What is ours is the numerical realization, its controls, and the two quantitative statements at the
end of the page.

## Why a grown layer cannot simply be left alone

A layer that has finished growing leaves two things behind. One is wanted: a temperature gradient
$\nabla\vartheta(0)=\lambda\Theta\zeta$, large because of the factor $\lambda$, which is what the next
layer grows on. The other is not: a shear $Dv(0)=\Omega\,Je(\varphi)\otimes e(\varphi)$, whose
coefficient is the vorticity amplitude $\Omega$, and which would keep deforming the next layer instead
of letting it sit on a frozen background.

So the vorticity amplitude has to be returned to zero while the temperature gain is kept. That is what
steering does.

## The control

Rotate the background gradient $G$ and the phase direction $\zeta$ **together**. A common rotation
leaves $J\zeta\cdot G$ and $|\zeta|$ alone, so the coefficient in $\dot\Theta$ does not move, but it
does move the **laboratory** component $\zeta_1$, which is what multiplies $\Theta$ in
$\dot\Omega=\lambda\zeta_1\Theta$. With $\Theta<0$, making $\zeta_1$ briefly negative drives $\Omega$
back up toward zero.

In normalized time $\tau=\Gamma(t-t_1)$, with a smooth step $\eta$ and a unit-mass profile $h$ on
$(0,1)$, their (3.25) is

$$P_{\tau\tau}=z(\tau)P,\qquad P(0)=P_\tau(0)=1,\qquad
z(\tau)=\begin{cases}1-\eta(\tau), & 0\le\tau\le1\\[2pt]
-\mu\Lambda h(\Lambda(\tau-1)), & 1\le\tau\le\tau_b=1+\Lambda^{-1}\end{cases}$$

a smooth ramp of the phase component to zero, then a short negative pulse. The pulse amplitude $\mu$
is not free: it is **selected** so that $v=P_\tau/P$ vanishes at $\tau_b$, which is exactly
$\Omega(t_b)=0$. Their Lemma 3.7 proves the endpoint map $\mu\mapsto v(\tau_b;\mu)$ is strictly
decreasing with a unique root in $[\tfrac12-\tfrac1{4\Lambda},1]$, and that the temperature gain
across steering satisfies $\log2\le\log P(\tau_b)\le1+\Lambda^{-1}$: the vorticity goes back, the
temperature does not.

Every one of those assertions is checked numerically, in repository CI, by
`tests/test_navier_stokes_steering.py`. At the paper's own design constants the selected root is
$\mu^\ast=0.66321$ and the gain is $e^{0.92839}$.

## Putting it in a periodic box: turn gravity, not the fluid

The construction rotates the whole background, which a torus does not allow. In two dimensions it does
not have to. In the frame co-rotating with $\alpha(t)$ the Coriolis and centrifugal accelerations are
gradients and disappear into the pressure, and the Euler acceleration only shifts the spatially uniform
mean vorticity, which induces no velocity on a torus. What is left is Boussinesq with a **rotating
gravity direction** $g(t)=e(\alpha(t))$, in which every wavevector stays an exact grid mode. The
buoyancy torque then gives a wave at unit $\zeta$ exactly

$$b=\lambda\,\zeta\cdot(\cos\alpha,-\sin\alpha)=\lambda\sin(s-\alpha)=\lambda Z,$$

the transcribed coefficient. The base stratification is no longer steady once gravity tilts, and a
low-frequency force holds it: that is not a cheat, since the theorem being modelled is a forced one,
and holding the prescribed background is exactly what its force does.

## What the PDE says

On a background flattened so that its gradient is affine to fourth order at the origin, the full cycle
matches the transcribed ODE:

| | measured |
|---|---|
| vorticity landing, $\lvert\Omega(t_b)\rvert/\max\lvert\Omega\rvert$ | $3.67\times10^{-4}$ |
| steering gain against the ODE | $3.06\times10^{-6}$ |
| hold: amplitude drift over three growth times | $0.36\%$ |
| endpoint map at $\mu\in\{0,\mu^\ast,2\mu^\ast\}$, worst gap | $4.7\times10^{-4}$ |

with both negative controls failing as they must: without the pulse the vorticity is still at $0.99985$
of its peak, and with gravity frozen it never turns at all.

## Two things this experiment adds

**1. A holding interval costs exactly $e^{-\nu\lambda^{2\alpha}T}$, and the steering does not change
with viscosity.** With equal dissipation on both fields the damping enters both amplitude equations on
the diagonal, so the whole cycle factorizes as $e^{-dt}$ times the inviscid cycle, $d=\nu\lambda^{2\alpha}$.
Consequences, all three confirmed against the PDE: the **inviscid** pulse amplitude still lands the
vorticity at zero (measured $4.1\times10^{-4}$), the hold decays at exactly $d$ (measured to $0.97\%$),
and rescaling the viscous run by $e^{dt}$ reproduces the inviscid one to $0.24\%$. This is the
assumption constraint C4 of [page 4](04-dissipation-and-the-frequency-cap.md) was built on, now
measured rather than assumed.

**2. The layer is slower than the background it grows on, by exactly $\sin s$.** The background is
Rayleigh-Taylor unstable at rate $\sqrt A$; the steered layer grows at $\sqrt A\sin s$. So every mode
at a more favourable angle gains $1/\sin s$ times as many e-folds as the layer does, and a schedule
long enough to complete a small-angle cycle is long enough for round-off to take the box over. At the
insertion angle of the first run, $\sin s=0.128$ over 37 time units, that is about 72 e-folds, and the
run was indeed destroyed by its own background: $\max\lvert\theta\rvert$ went from $4.0$ to $10.0$ and
the measured amplitude "grew" by a factor 726 in the holding interval.

The construction is not vulnerable to this, because each layer is localized where it matters and the
force controls what happens elsewhere. But it says something about the mechanism that is easy to miss
in the exponent bookkeeping: **the cascade is always running against a faster instability of its own
background, and what keeps it alive is localization, not speed.**

## Next

Back to the [index](README.md).
