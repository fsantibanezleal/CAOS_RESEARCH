# 2. The two September 2026 constructions

Both extend the multiscale program of **Diego Cordoba and Luis Martinez-Zoroa**, who originated it and
to whom both groups assign the intellectual credit. Nothing in this problem is our mechanism, and that
attribution is a standing requirement on this page and the two that follow.

## The shared scheme

Tao's exposition of 2026-09-07 states the abstract strategy both constructions instantiate. For an
equation $N(u)=f$, take a low-frequency solution $N(u_{lo})=f_{lo}$ and add a high-frequency
correction so that

$$N(u_{lo}+u_{hi}) - N(u_{lo}) \approx 0,
\qquad\text{that is}\qquad N'(u_{lo})\,u_{hi}\approx 0 .$$

Design $u_{lo}$ so that this linearized evolution carries an exploitable instability, which takes
$u_{hi}$ from a small amplitude to a disruptive one. The two constructions differ in what supplies the
instability and in what the high-frequency part must cancel.

## Alpoge and Buckmaster: a layer cascade on a Rayleigh-Taylor background

Three papers, posted 2026-09-07, each with a Lean formalization at
[`fluid_lean`](https://github.com/tristanbuckmaster/fluid_lean): the incompressible porous medium
equation on $\mathbb{T}^2$ (with Coiculescu), the inviscid Boussinesq system on $\mathbb{R}^2$, and
the incompressible Euler equations on $\mathbb{R}^3$. All three are **forced** and all three are
inviscid or Darcy.

Their Boussinesq initial data are

$$\theta_{in}(x) = -\frac{A_0}{\lambda_0}\sin(\lambda_0 x_2)\,\chi_0(x), \qquad u_{in}=0,$$

so that $\partial_2\theta_{in}(0)=-A_0$: colder, heavier fluid above warmer, lighter fluid. That is a
smooth Rayleigh-Taylor-unstable stratification, and it is the instability the whole cascade feeds on.
An upward displacement carries warmer fluid into colder surroundings, and buoyancy reinforces the
displacement.

Localized oscillatory perturbations, which they call **layers**, are added one after another. Each new
layer grows through the instability created by the temperature gradient already present; its short
wavelength lets its gradient become large while its amplitude stays small; that larger gradient is the
background for the next layer, introduced at a still smaller scale. Infinitely many stages are
compressed into a finite time. The mechanics are in [page 3](03-the-modulation-system.md).

Their Theorem 1.1 delivers forces $f_{\theta}, f_u \in C_c^{\infty}$ supported in one fixed ball and
a time $T_*\in(0,\infty)$ with

$$\sup_{0\le t<T_*}\lVert\theta(t)\rVert_{\infty}<\infty, \qquad
  \lim_{t\uparrow T_*}\lVert\nabla\theta(t)\rVert_{\infty}=\infty, \qquad
  \limsup_{t\uparrow T_*}\lVert\omega(t)\rVert_{\infty}=\infty .$$

The last conclusion is a $\limsup$ rather than a limit, and the reason is structural: the vorticity
bound is evaluated only at the ends of steering intervals, when the newest amplitude has been returned
to zero and the older contributions share a sign. Between those times the contributions can cancel.

## OpenAI: a self-similar vortex core with oscillatory pulses

Announced 2026-09-08, with Lean certificates at
[`openai/NavierStokesAndEuler`](https://github.com/openai/NavierStokesAndEuler). Two results: forced
blowup for 3D Navier-Stokes for every $\nu>0$, claimed to establish Fefferman's (C) and (D); and
**unforced** blowup for 3D Euler from smooth compactly supported data.

The Navier-Stokes mechanism is different in kind. The singularity forms at the origin at $t=1$; write
$\tau=1-t$. In cylindrical coordinates the leading flow is axisymmetric: fluid spirals inward and
flows axially away on opposite sides of a dividing layer near $z=0$. Radial inflow carries angular
momentum to smaller radii, and since $r u_{\theta}$ is conserved for a parcel without torque, moving
inward increases $u_{\theta}$. Incompressibility prevents accumulation on the axis because the axial
outflow removes the incoming fluid, so the spin-up can continue.

The core is self-similar with **two different length scales**,

$$\ell_r \asymp \tau^{1/2}, \qquad \ell_z \asymp \tau^{1/2-h}, \qquad 0<h<\tfrac{1}{100},$$

so $\ell_r/\ell_z \asymp \tau^{h}\to 0$: an increasingly slender column, of volume of order
$\tau^{3/2-h}$. The velocity scales are

$$|u^{(0)}_{\theta}|,\,|u^{(0)}_z| \asymp \tau^{-1/2-h}, \qquad |u^{(0)}_r| = O(\tau^{-1/2}),$$

and the core kinetic energy is of order $\tau^{1/2-3h}\to 0$. That is how the energy constraint is
met: the speeds diverge on a region shrinking fast enough for the $L^2$ norm to stay bounded.

Viscosity is handled by an anisotropy in the Reynolds numbers,

$$\mathrm{Re}_{\theta} := \frac{|u_{\theta}|\ell_r}{\nu} \asymp \tau^{-h}\to\infty,
\qquad
\mathrm{Re}_r := \frac{|u_r|\ell_r}{\nu} = O(1).$$

The swirl outruns viscous diffusion while the radial motion stays in balance with it. This is how the
construction survives for every fixed $\nu>0$ instead of only in the inviscid limit, and it is the
single most important structural difference from the layer cascade.

The force is defined as the residual: for any incompressible pair one may set $f$ to whatever makes
the equation hold. The entire difficulty is that the individual terms diverge and the construction
must arrange enough cancellation that the sum and all its derivatives extend smoothly through $t=1$.
Joining the core to a smooth exterior leaves an unbounded residual in the annulus between them;
spatially oscillatory pulse rings are added whose nonlinear momentum fluxes cancel its singular part,
with further corrections removing what remains.

## Side by side

| | Alpoge-Buckmaster | OpenAI |
|---|---|---|
| instability source | Rayleigh-Taylor stratification | self-similar inward-spiralling vortex |
| background near the origin | affine in $x$, by construction | two-scale self-similar core |
| the small object | wave amplitudes $\Theta,\Omega$ at wavevector $\lambda\zeta$ | oscillatory pulse rings in the annulus |
| what the oscillation must do | grow, then return $\Omega$ to zero for the next layer | cancel the singular momentum residual of the core-to-exterior join |
| scale organization | discrete layers, infinitely many in finite time | continuous self-similar core plus corrections at every order |
| viscosity | absent | present, via $\mathrm{Re}_{\theta}\to\infty$ with $\mathrm{Re}_r=O(1)$ |
| forcing | required in all three results | required for Navier-Stokes; **not** for their Euler result |

The single technical step separating the two families is viscosity, and [page 4](04-dissipation-and-the-frequency-cap.md)
computes what that step costs.

## Sources

- L. Alpoge, T. Buckmaster, *Blowup for the Boussinesq equations with smooth forcing*, 2026-09-07.
- L. Alpoge, T. Buckmaster, *Blowup for the Euler equations with smooth forcing*, 2026-09-07.
- L. Alpoge, T. Buckmaster, M. P. Coiculescu, *Extending the Cordoba-Martinez-Zoroa IPM blow-up to
  uniformly space-time smooth forcing*, 2026-09-07.
- OpenAI, *Finite time blowup for Navier-Stokes*, and *Finite time blowup for the Euler equation*,
  2026-09-08.
- T. Tao, *Finite time blowup with smooth forcing term...*, What's new, 2026-09-07.
- D. Cordoba, L. Martinez-Zoroa, [arXiv:2410.22920](https://arxiv.org/abs/2410.22920).
- D. Cordoba, L. Martinez-Zoroa, F. Zheng, Arch. Ration. Mech. Anal. 250 (2026), article 38,
  [doi:10.1007/s00205-026-02198-0](https://doi.org/10.1007/s00205-026-02198-0).

All archived with hashes in [`references/`](../references/); read depth per source in
[`context/references.md`](../context/references.md).
