# 3. The modulation system

The exact reduction at the heart of the Alpoge-Buckmaster construction, transcribed from Subsection
1.2 and Lemma 3.1 of their Boussinesq paper. The mechanism is due to Cordoba and Martinez-Zoroa. Our
contribution on this page is limited to the verification: every claim below is checked numerically in
[`code/tests/test_modulation.py`](../code/tests/test_modulation.py) and against a full nonlinear PDE
simulation in [EXP-002](../experiments/EXP-002-reduction-control/verdict.md).

## Assumptions

- The forced inviscid Boussinesq system on $\mathbb{R}^2$, in vorticity form
  $\partial_t\omega + u\cdot\nabla\omega = \partial_1\theta + \operatorname{curl}f_u$, with
  $\omega=\partial_1u_2-\partial_2u_1$ and $u=\nabla^{\perp}\Delta^{-1}\omega$.
- $J(x_1,x_2)=(-x_2,x_1)$ and $\nabla^{\perp}=J\nabla$.
- The already-constructed fields are **affine near the origin**:
  $u_{old}(x,t)=D(t)x$ with $\operatorname{tr}D=0$, and $\theta_{old}(x,t)=G(t)\cdot x$. The
  corresponding $\omega_{old}$ is spatially constant.
- Cutoffs are ignored for the derivation; the localization that makes this legitimate is described at
  the end.

## The wave

Add a temperature wave and a vorticity wave sharing a single phase,

$$s=\lambda\,\zeta(t)\cdot x, \qquad \vartheta=\Theta(t)\sin s, \qquad \varpi=\Omega(t)\cos s,$$

with streamfunction and velocity

$$\psi=-\frac{\Omega}{\lambda^2|\zeta|^2}\cos s, \qquad
  v=\nabla^{\perp}\psi=\frac{\Omega}{\lambda|\zeta|^2}\,J\zeta\,\sin s,$$

which indeed satisfies $\Delta\psi=\varpi$. Here $\lambda$ is a fixed frequency parameter, $\zeta(t)$
a time-dependent direction, and $\Theta,\Omega$ signed real amplitudes.

## Why the ansatz is exact and not asymptotic

$v$ is parallel to $J\zeta$, hence perpendicular to $\zeta$, while $\nabla\vartheta$ and
$\nabla\varpi$ are both parallel to $\zeta$. Therefore

$$v\cdot\nabla\vartheta = v\cdot\nabla\varpi = 0,$$

and $v\cdot\nabla\omega_{old}=0$ because $\omega_{old}$ is constant. **The wave does not advect
itself.** No nonlinear correction term is needed, which is what separates this from a perturbative
expansion.

This is a geometric identity, so it is worth checking on actual fields rather than only on paper;
`test_self_advection_cancels_on_the_grid` evaluates $v\cdot\nabla\vartheta$ on a $256^2$ grid and finds
it at round-off relative to the size of its own terms.

## The amplitude equations

Subtracting the equations for the older fields and requiring the phase to be transported,

$$(\partial_t + Dx\cdot\nabla)s = \lambda(\dot\zeta + D^{T}\zeta)\cdot x = 0,$$

then matching the coefficients of $\sin s$ and $\cos s$ gives the closed system

$$\boxed{\;\dot\zeta=-D^{T}\zeta, \qquad
  \dot\Theta=-\frac{J\zeta\cdot G}{\lambda|\zeta|^2}\,\Omega, \qquad
  \dot\Omega=\lambda\,\zeta_1\,\Theta. \;}$$

Each equation records one effect: the older velocity turns and stretches the wavevector; the new
velocity moves the older temperature; the horizontal temperature derivative creates new vorticity. The
coefficient $\zeta_1$ is the *laboratory* component because the buoyancy direction $e_2$ is fixed and
does not rotate with the wave.

## Growth

Freeze $D=0$ and $G=-Ae_2$ with $A>0$, and write $\zeta=r\,e(\varphi)$ with
$e(\varphi)=(\sin\varphi,\cos\varphi)$. Since $J\zeta\cdot G=-Ar\sin\varphi$,

$$\frac{d}{dt}\begin{pmatrix}\Theta\\\Omega\end{pmatrix}
  =\begin{pmatrix}0 & \dfrac{A\sin\varphi}{\lambda r}\\[4pt] \lambda r\sin\varphi & 0\end{pmatrix}
   \begin{pmatrix}\Theta\\\Omega\end{pmatrix}.$$

The product of the off-diagonal entries is $A\sin^2\varphi$, so for $0<\varphi<\pi$ the eigenvalues
are

$$\pm\sqrt{A}\,\sin\varphi,$$

and on the growing eigenline $\Omega=(\lambda r/\sqrt{A})\,\Theta$ both amplitudes are multiplied by
$e^{\sqrt{A}\sin\varphi\,t}$.

> **A transcription warning, recorded because it nearly reached a dossier.** `pdftotext` floats the
> radical sign onto its own line, so $\sqrt{A}\sin\varphi$ and $\sqrt{A\sin\varphi}$ are
> indistinguishable in extracted text. They differ substantially: at $A=12.5$, $\varphi=0.37$ they are
> $1.28$ and $2.13$. The matrix settles it, and so does the eigenline the paper itself prints. Settle
> any transcribed formula by computing it.

## The amplification identity

At the origin,

$$\nabla\vartheta(0,t)=\lambda\,\Theta\,\zeta, \qquad
  Dv(0,t)=\Omega\,J e(\varphi)\otimes e(\varphi).$$

The first identity is the engine of the whole program: **a short wave carries a small temperature
amplitude and a large gradient**, the gradient picking up the factor $\lambda$. That is how each layer
can hand the next a larger background gradient while the temperature itself stays bounded, which is
required by the blowup statement ($\sup_t\lVert\theta\rVert_{\infty}<\infty$ while
$\lVert\nabla\theta\rVert_{\infty}\to\infty$).

The second identity is the problem: the accompanying shear has coefficient $\Omega$, and with
$\Theta<0$ the negative $\Omega$ would interfere with the growth of the next wave.

## Growth, steering, holding

The cycle that resolves it:

1. **Growth.** Amplitudes rise at $\sqrt{A}\sin\varphi$ along the growing eigenline.
2. **Steering.** Rotate $G$ and $\zeta$ *together*. A common rotation preserves $J\zeta\cdot G$ and
   $|\zeta|$, so it leaves the coupling in $\dot\Theta$ alone, but it can change the sign of the
   laboratory component $\zeta_1$ and hence of $\dot\Omega=\lambda\zeta_1\Theta$. With $\Theta<0$,
   briefly making $\zeta_1<0$ brings the negative vorticity amplitude back toward zero. The rotation
   is chosen to end with $\Omega=0$ and $\zeta_1=0$, retaining the temperature gain.
3. **Holding.** With $\zeta_1=0$ both amplitude derivatives vanish, and the interval this opens is
   where the next, finer wave grows on the enlarged gradient.

Infinitely many such cycles are fitted into a finite time, with the spatial scale decreasing at every
stage.

**A consequence that matters for the dissipative case:** holding intervals are quiescent only in the
inviscid system. With dissipation present, $\zeta_1=0$ still kills the coupling but the damping term
does not vanish, so the amplitudes decay throughout the hold. See
[page 4](04-dissipation-and-the-frequency-cap.md).

## From a wave to compact layers

For the real construction $\sin s$ is replaced by a smooth odd periodic profile $F(s)$ equal to $s$
near zero, with mean-zero primitive $P$ ($P'=F$). Then $\vartheta=\Theta F(s)$, $\varpi=\Omega F'(s)$,
$\psi=\Omega P(s)/(\lambda^2|\zeta|^2)$ satisfy the same cancellations and the same amplitude
equations, and the fields are exactly affine near the origin, so every finer layer sees precisely the
affine background assumed above. A transported envelope $g$ equal to one near the origin localizes
the temperature and streamfunction; corrections outside the central region cancel oscillatory
localization errors to successively higher order, with the correction order increasing with the layer
index so the force series converges with every mixed derivative.

Oddness pins the origin under the flow. Keeping the temperature gradients inside one acute cone stops
their gains from cancelling, which is what yields a full limit for $\lVert\nabla\theta\rVert_{\infty}$
rather than a $\limsup$.

## What we verified

[EXP-002](../experiments/EXP-002-reduction-control/verdict.md), against a GPU pseudo-spectral
simulation of the full nonlinear system:

- the predicted rate, to $4\times10^{-5}$ relative at the band peak and 0.6 percent median, at two
  angles;
- the predicted band structure, growth where the local $\cos$ is positive and no growth where it is
  negative;
- **frequency independence**, the load-bearing fact, to $2.7\times10^{-4}$ across $\lambda$ from 20 to
  160;
- three corrupted models all failing, once evaluated at a non-degenerate angle.

## Next

[4. Dissipation and the frequency cap](04-dissipation-and-the-frequency-cap.md).
