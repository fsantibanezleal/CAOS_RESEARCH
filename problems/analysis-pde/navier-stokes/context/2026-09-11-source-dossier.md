# navier-stokes: opening source dossier

Date/access: 2026-09-11. Scope: the two September 2026 blowup claims (OpenAI; Alpoge-Buckmaster), the
Cordoba-Martinez-Zoroa program they both extend, and the official Clay problem statement they are
measured against. Every statement below is transcribed from the primary source named beside it, with
the read depth marked in [`references.md`](references.md). Nothing here is recalled from memory.

## 1. What the official problem actually asks

Fefferman's official description fixes the system

$$\partial_t u_i + \sum_{j=1}^{n} u_j \frac{\partial u_i}{\partial x_j}
  = \nu \Delta u_i - \frac{\partial p}{\partial x_i} + f_i, \qquad
  \operatorname{div} u = 0, \qquad u(x,0) = u^{\circ}(x),$$

and four side conditions: (4) rapid decay of every derivative of $u^{\circ}$, (5) rapid decay of every
mixed derivative of $f$ in $(1+|x|+t)$, (6) $p, u \in C^{\infty}(\mathbb{R}^n \times [0,\infty))$, and
(7) $\int_{\mathbb{R}^n} |u(x,t)|^2\,dx < C$ for all $t \ge 0$. The periodic variant replaces these
with (8), (9), (10), (11).

Fefferman then writes, verbatim: "To give reasonable leeway to solvers while retaining the heart of
the problem, we ask for a proof of one of the following four statements." The four are (A) and (B),
global existence and smoothness with $f \equiv 0$ on $\mathbb{R}^3$ and on $\mathbb{R}^3/\mathbb{Z}^3$;
and (C) and (D), breakdown:

> (C) Breakdown of Navier-Stokes solutions on $\mathbb{R}^3$. Take $\nu>0$ and $n=3$. Then there exist
> a smooth, divergence-free vector field $u^{\circ}(x)$ on $\mathbb{R}^3$ and a smooth $f(x,t)$ on
> $\mathbb{R}^3 \times [0,\infty)$, satisfying (4), (5), for which there exist no solutions $(p,u)$ of
> (1), (2), (3), (6), (7) on $\mathbb{R}^3 \times [0,\infty)$.

Two facts follow, and both matter for our scoping.

1. **(C) permits a forcing term.** The unforced hypothesis appears only in (A) and (B). A solver who
   exhibits a smooth rapidly decaying force and smooth data with no global smooth bounded-energy
   solution has proved one of the four statements Fefferman asks for. The "leeway" sentence is
   explicit and is part of the official text.
2. **(C) is nonetheless the weaker physical statement.** It does not show that the equations break
   down on their own; it shows they break down under an admissible external drive. Anyone reporting
   this result to a non-specialist and saying "the Navier-Stokes equations develop a singularity"
   without the word "forced" is overstating it. Our own writing must always carry the qualifier.

## 2. The OpenAI Navier-Stokes claim

Transcribed from the manuscript, Theorem 1.1:

> For every $\nu > 0$ there exist a force $f \in C_c^{\infty}(\mathbb{R}^3 \times (0,\infty); \mathbb{R}^3)$,
> a compact set $K \subset \mathbb{R}^3$, and smooth velocity and pressure fields $u, p$ on
> $\mathbb{R}^3 \times [0,1)$ satisfying
> $$\partial_t u + (u\cdot\nabla)u - \nu\Delta u + \nabla p = f, \quad \nabla\cdot u = 0, \quad u(\cdot,0)=0,$$
> such that $\operatorname{supp} u(\cdot,t) \cup \operatorname{supp} p(\cdot,t) \subset K$ for every
> $0 \le t < 1$,
> $$\sup_{0\le t<1} \lVert u(t)\rVert_{L^2(\mathbb{R}^3)} < \infty, \qquad
>   \limsup_{t\uparrow 1} \lVert u(t)\rVert_{L^{\infty}(\mathbb{R}^3)} = \infty.$$
> Consequently, there is no smooth solution $(u,P)$ on $\mathbb{R}^3 \times [0,\infty)$ with the same
> force and initial datum whose kinetic energy is uniformly bounded.

The paper then states: "This establishes alternative (C) in the Millennium problem statement for
Navier-Stokes as stated by Fefferman in [13]. Compact support also yields the corresponding
construction on $\mathbb{T}^3 = \mathbb{R}^3/\mathbb{Z}^3$, establishing alternative (D); see
Corollary 10.6."

**Hypothesis check against (C), done term by term.** Initial datum $u^{\circ} \equiv 0$ is smooth and
divergence free and satisfies (4) trivially. The force is $C^{\infty}$ and compactly supported in
space and time, so it vanishes for large $|x|+t$ and satisfies (5) trivially. The conclusion denies
existence of a global smooth solution with uniformly bounded kinetic energy, which is exactly the
denial of (1), (2), (3), (6), (7). The match is exact. The construction is therefore stronger than (C)
requires in two respects: the force is compactly supported rather than merely rapidly decaying, and
the initial velocity is zero rather than merely admissible.

**The mechanism**, transcribed from Section 2. The singularity forms at the spatial origin at $t=1$.
Write $\tau = 1-t$. In cylindrical coordinates about the vertical axis, the leading flow $u^{(0)}$ is
axisymmetric; fluid spirals inward toward the axis and flows axially away on opposite sides of a
dividing layer near $z=0$. The core evolves self-similarly with two different length scales,

$$\ell_r \asymp \tau^{1/2}, \qquad \ell_z \asymp \tau^{1/2-h}, \qquad 0 < h < 1/100,$$

so $\ell_r/\ell_z \asymp \tau^h \to 0$ and the core becomes an increasingly slender column of volume
of order $\tau^{3/2-h}$. The velocity scales are

$$|u^{(0)}_{\theta}|, |u^{(0)}_z| \asymp \tau^{-1/2-h}, \qquad |u^{(0)}_r| = O(\tau^{-1/2}),$$

and the core kinetic energy is of order $\tau^{1/2-3h}$, which tends to zero despite the unbounded
speeds. That is the whole trick of the energy constraint: the speeds diverge on a region that shrinks
fast enough for the $L^2$ norm to stay bounded.

The viscous term is handled by an anisotropy in the Reynolds numbers:

$$\mathrm{Re}_{\theta} := \frac{|u_{\theta}|\ell_r}{\nu} \asymp \tau^{-h} \to \infty, \qquad
  \mathrm{Re}_r := \frac{|u_r|\ell_r}{\nu} = O(1).$$

The angular Reynolds number diverges, so the swirl outruns viscous diffusion; the radial Reynolds
number stays bounded, so viscosity still competes with the radial inflow. This is how the construction
survives for every fixed $\nu > 0$ rather than only in the inviscid limit.

The force is defined as the residual: for any incompressible $(u,p)$ one may set $f$ to be whatever
makes (1.1) hold. The entire difficulty is that the individual terms diverge, and the construction
must arrange enough cancellation that the sum and all of its derivatives extend smoothly through
$t=1$. Joining the self-similar core to a smooth exterior leaves a residual in the intervening
annulus which is unbounded as $\tau \to 0$; spatially oscillatory pulses are added whose nonlinear
momentum fluxes cancel the singular part, and further corrections remove the remaining singular
errors.

## 3. The OpenAI Euler claim, which is the stronger mathematical statement

Transcribed from the companion manuscript, Theorem 1.1:

> There exists $u_0 \in C_{c}^{\infty,\sigma}(\mathbb{R}^3)$ such that $0 < T_*(u_0) < \infty$. Its
> smooth Euler solution satisfies
> $$\limsup_{t \uparrow T_*} \lVert \nabla u(t)\rVert_{L^{\infty}} = \infty, \qquad
>   \int_0^{T_*} \lVert \operatorname{curl} u(t)\rVert_{L^{\infty}}\,dt = \infty.$$

Here $C_c^{\infty,\sigma}(\mathbb{R}^3) = \{u_0 \in C_c^{\infty}(\mathbb{R}^3;\mathbb{R}^3) :
\nabla\cdot u_0 = 0\}$ and the equations are **unforced**: $\partial_t u + (u\cdot\nabla)u + \nabla p
= 0$. The announcement page confirms the reading: "The specific variant of the question that they
resolved was the unforced version, where no external force is applied to the fluid."

This is the claim with the larger mathematical consequence. Euler is not a Millennium problem, but
finite-time blowup for unforced 3D Euler from smooth compactly supported finite-energy data is the
question that Elgindi ($C^{1,\alpha}$, 2019), Elgindi-Ghoul-Masmoudi, Cordoba-Martinez-Zoroa-Zheng,
Elgindi-Pasqualotto, Chen-Shkoller, and Chen-Hou (smooth, with a boundary) have each addressed only
in a restricted regularity class or a restricted geometry. A smooth compactly supported unforced
example on all of $\mathbb{R}^3$ would close that line. Our scoping must treat this as the headline,
not the Navier-Stokes (C) statement.

## 4. The Alpoge-Buckmaster results and the mechanism in its simplest form

Three papers were posted on 2026-09-07, one day before the OpenAI announcement, each with a Lean
formalization at <https://github.com/tristanbuckmaster/fluid_lean>: IPM on $\mathbb{T}^2$ with a
uniformly space-time smooth force (with Coiculescu), 2D inviscid Boussinesq on $\mathbb{R}^2$ with
smooth compactly supported forces in both equations, and 3D incompressible Euler on $\mathbb{R}^3$
with a force smooth in space and time up to and including the blowup time. All three are **forced**.

The Boussinesq paper carries the mechanism in its most transparent form, and it is the object our own
work should start from. For the forced inviscid Boussinesq system

$$\partial_t \theta + u\cdot\nabla\theta = f_{\theta}, \qquad
  \partial_t u + u\cdot\nabla u + \nabla p = \theta e_2 + f_u, \qquad \operatorname{div} u = 0,$$

the initial data are $\theta_{in}(x) = -\frac{A_0}{\lambda_0}\sin(\lambda_0 x_2)\chi_0(x)$ and
$u_{in}=0$, so that $\partial_2\theta_{in}(0) = -A_0$: colder heavier fluid above warmer lighter
fluid, a smooth Rayleigh-Taylor-unstable stratification. Theorem 1.1 gives odd forces
$f_{\theta} \in C_c^{\infty}(\mathbb{R}^2\times\mathbb{R})$,
$f_u \in C_c^{\infty}(\mathbb{R}^2\times\mathbb{R};\mathbb{R}^2)$ and a time $T_* \in (0,\infty)$ with
a unique solution before $T_*$ such that

$$\sup_{0\le t<T_*}\lVert\theta(t)\rVert_{\infty}<\infty, \qquad
  \lim_{t\uparrow T_*}\lVert\nabla\theta(t)\rVert_{\infty}=\infty, \qquad
  \limsup_{t\uparrow T_*}\lVert\omega(t)\rVert_{\infty}=\infty.$$

**The exact wave and its modulation ODEs.** Suppose the fields already built have the local form
$u_{old}(x,t) = D(t)x$ with $\operatorname{tr}D = 0$, and $\theta_{old}(x,t) = G(t)\cdot x$. Add a
temperature wave and a vorticity wave sharing one phase,

$$s = \lambda\zeta(t)\cdot x, \qquad \vartheta = \Theta(t)\sin s, \qquad \varpi = \Omega(t)\cos s,$$

with streamfunction $\psi = -\frac{\Omega}{\lambda^2|\zeta|^2}\cos s$ and velocity
$v = \nabla^{\perp}\psi = \frac{\Omega}{\lambda|\zeta|^2}J\zeta \sin s$. Because $v \perp \zeta$ while
both wave gradients are parallel to $\zeta$, the wave does not advect itself:
$v\cdot\nabla\vartheta = v\cdot\nabla\varpi = 0$, and also $v\cdot\nabla\omega_{old}=0$. Requiring the
phase to be transported, $(\partial_t + Dx\cdot\nabla)s = \lambda(\dot\zeta + D^{T}\zeta)\cdot x = 0$,
and matching coefficients of $\sin s$ and $\cos s$ gives the closed system

$$\boxed{\;\dot\zeta = -D^{T}\zeta, \qquad
  \dot\Theta = -\frac{J\zeta\cdot G}{\lambda|\zeta|^2}\,\Omega, \qquad
  \dot\Omega = \lambda\zeta_1\Theta. \;}$$

Each equation records one physical effect: the older velocity turns and stretches the wavevector; the
new velocity moves the older temperature; the horizontal temperature derivative creates new vorticity.
The coefficient $\zeta_1$ is the laboratory component because the buoyancy direction $e_2$ is fixed.

**Why it grows.** Freeze $D=0$ and $G=-Ae_2$ with $A>0$, and write $\zeta = r\,e(\varphi)$ with
$e(\varphi) = (\sin\varphi,\cos\varphi)$. The amplitude pair obeys

$$\frac{d}{dt}\begin{pmatrix}\Theta\\ \Omega\end{pmatrix}
  = \begin{pmatrix} 0 & A\sin\varphi/(\lambda r) \\ \lambda r \sin\varphi & 0\end{pmatrix}
    \begin{pmatrix}\Theta\\ \Omega\end{pmatrix},$$

whose eigenvalues are $\pm\sqrt{A}\,\sin\varphi$ for $0<\varphi<\pi$; on the growing eigenline
$\Omega = (\lambda r/\sqrt{A})\,\Theta$ both amplitudes are multiplied by $e^{\sqrt{A}\,\sin\varphi\,t}$.

(Transcription check, done here rather than trusted: the extracted text floats the radical onto its own
line, so "$\pm\sqrt{A\sin\varphi}$" and "$\pm\sqrt{A}\sin\varphi$" are both readings of the glyphs. The
matrix decides it. The product of the off-diagonal entries is
$\frac{A\sin\varphi}{\lambda r}\cdot\lambda r\sin\varphi = A\sin^2\varphi$, so the eigenvalues are
$\pm\sqrt{A}\,\sin\varphi$, and the eigenvector for the positive one satisfies
$\lambda r \sin\varphi\,\Theta = \sqrt{A}\sin\varphi\,\Omega$, that is
$\Omega = (\lambda r/\sqrt{A})\Theta$, which is exactly the eigenline the paper prints. The second
reading is the correct one. The growth rate is therefore independent of the frequency $\lambda$, a fact
that carries the whole viscous analysis in
[`2026-09-11-simplified-model-and-beyond.md`](2026-09-11-simplified-model-and-beyond.md).)
At the origin $\nabla\vartheta(0,t) = \lambda\Theta\zeta$ and
$Dv(0,t) = \Omega\,Je(\varphi)\otimes e(\varphi)$. The first identity is the crux of the whole
program: a short wave can carry a **small** temperature amplitude and a **large** gradient, because
the gradient picks up the factor $\lambda$.

**Why it can be iterated.** The accompanying shear $\Omega$ would interfere with the next wave, so
growth is followed by a controlled rotation of $G$ and $\zeta$ together. A common rotation preserves
$J\zeta\cdot G$ and $|\zeta|$ but can flip the sign of the laboratory component $\zeta_1$, hence of
$\dot\Omega = \lambda\zeta_1\Theta$, without reversing the coupling in $\dot\Theta$. The rotation is
chosen to end with $\Omega = 0$ and $\zeta_1 = 0$, at which point both amplitude derivatives vanish
and a holding interval opens in which the next, finer wave can grow on the enlarged gradient. The
cycle is growth, steering, hold, repeat, with infinitely many stages compressed into a finite time and
the spatial scale decreasing at every stage.

For the real construction $\sin s$ is replaced by a smooth odd periodic profile $F(s)$ equal to $s$
near zero, with mean-zero primitive $P$; then $\vartheta = \Theta F(s)$, $\varpi = \Omega F'(s)$,
$\psi = \Omega P(s)/(\lambda^2|\zeta|^2)$ satisfy the same cancellation and the same amplitude
equations (their Lemma 3.1), and the fields are exactly affine near the origin, so each finer layer
sees precisely the affine background assumed above. Localization uses a transported envelope $g$ equal
to one near the origin; corrections outside the central region cancel oscillatory localization errors
to successively higher order, with the correction order increasing with the layer index so that the
force series converges with every mixed derivative.

Oddness pins the origin under the flow. The temperature gradients are kept inside one acute cone so
their gains cannot cancel, which gives a full limit for $\lVert\nabla\theta\rVert_{\infty}$; the
vorticity bound is evaluated only at the ends of steering intervals, when the newest amplitude is zero
and the older contributions share a sign, which is exactly why that conclusion is a $\limsup$ and not
a limit.

## 5. The two constructions compared

Tao's exposition gives the shared abstract scheme: for an equation $N(u)=f$, take a low-frequency
solution $N(u_{lo}) = f_{lo}$, add a high-frequency correction with
$N(u_{lo}+u_{hi}) - N(u_{lo}) \approx 0$, that is $N'(u_{lo})u_{hi}\approx 0$, and design $u_{lo}$ so
that this linearized evolution has an exploitable instability which takes $u_{hi}$ from small
amplitude to disruptive size. Both September 2026 constructions instantiate that scheme. They differ
in what supplies the instability and in what the high-frequency part has to cancel.

| | Alpoge-Buckmaster (Boussinesq, Euler, IPM) | OpenAI (Navier-Stokes, Euler) |
|---|---|---|
| instability source | Rayleigh-Taylor stratification; buoyancy amplifies a displacement | self-similar inward-spiralling vortex; angular momentum transport spins up the core |
| background | affine in $x$ near the origin, by construction | self-similar two-scale axisymmetric core, $\ell_r \asymp \tau^{1/2}$, $\ell_z \asymp \tau^{1/2-h}$ |
| the small object | wave amplitudes $\Theta,\Omega$ with wavevector $\lambda\zeta$ | oscillatory pulse rings in the annulus around the core |
| what the oscillation must do | grow, then return $\Omega$ to zero to prepare the next layer | cancel the singular part of the momentum residual left by the core-to-exterior join |
| scale organization | discrete layers, each finer than the last, infinitely many in finite time | continuous self-similar core plus corrections at every order |
| viscosity | absent (inviscid Boussinesq, Euler, IPM) | present and handled by the anisotropic Reynolds split $\mathrm{Re}_{\theta}\to\infty$, $\mathrm{Re}_r = O(1)$ |
| forcing | required in all three | required for Navier-Stokes; **not** required for their Euler result |

The single technical step that separates the two families is viscosity. Every published member of the
Cordoba-Martinez-Zoroa lineage is inviscid or Darcy. Tao's assessment on 2026-09-07 was that the
Alpoge-Buckmaster route has "a high likelihood of also extending to Navier-Stokes" but that "they do
not quite achieve these goals yet". Buckmaster's own statement says they believe they have blowup for
**hypo-dissipative** Navier-Stokes, unreleased because the Lean verification had not finished. The
anisotropic Reynolds split in the OpenAI paper is a concrete answer to the same obstruction, arrived
at by a different route.

## 6. Priority and credit, recorded as fact

Both parties agree on the intellectual lineage and it must be reproduced in anything we write.
Alpoge-Buckmaster: "The credit for the basic idea of this program goes to Diego Cordoba and Luis
Martinez-Zoroa, who for several years have been exploring the construction of forced blow ups." Their
Boussinesq paper repeats it: "We believe that the primary intellectual credit for the underlying
strategy belongs to them." Buckmaster adds that in his view Luis Martinez-Zoroa deserves a Fields
Medal.

Timeline, from the primary statements of both sides:

- Alpoge-Buckmaster obtained the Boussinesq and Euler results on 2026-08-15 and completed the Lean
  verification on 2026-08-22, after roughly a year of work.
- OpenAI states its effort began on 2026-09-01 after hearing a rumour, that the agents reached the
  Navier-Stokes resolution on 2026-09-05 (about 88 hours after launch, on the order of 10,000
  concurrent agents, roughly 2.7 million messages and 130 billion output tokens for that problem),
  and that Lean formalization took a further 17 hours. Their unforced Euler result came first, from
  nearly 100 agents over about 50 hours.
- Alpoge-Buckmaster posted on 2026-09-07; OpenAI announced on 2026-09-08.
- Buckmaster's statement records the content of two calls on 2026-09-06, including that he was told
  the model had been given only the problem statement and that this "turned out not to be true", two
  proposals about authorship that he declined, and a reply of "If you don't want me to be nice, then
  I don't have to be nice." He is explicit about the limits of his claim: "I have not seen OpenAI's
  proof. I do not know what their model did, or how. I do not know whether our data was used. I am
  not accusing anyone of anything."
- OpenAI updated the announcement page on 2026-09-10 stating that an investigation confirmed
  Buckmaster's Codex prompts "could not have influenced the system in any way, including through
  training", that they recognize priority of the Alpoge-Buckmaster forced Euler work, and that they do
  not intend to claim the Millennium Prize.

This dossier takes no position on the dispute. It records it because credit attribution is a gate in
`methodology/09-manuscripts-and-publication.md`, and because any manuscript we write in this area must
cite Cordoba and Martinez-Zoroa as the originators of the program, Alpoge-Buckmaster and OpenAI as the
September 2026 contributors, and must never present the layer or pulse mechanism as ours.

## 7. Verification status at the time of writing

Neither proof has been checked by the mathematical community. The Clay Mathematics Institute has not
commented. What does exist is machine verification, and it is of noticeably higher quality than the
usual claim of one; the audit is in
[`2026-09-11-lean-statement-audit.md`](2026-09-11-lean-statement-audit.md). The correct summary for
any of our surfaces is: the statements are faithful and the certificate is well engineered; nobody has
yet confirmed that the human-readable arguments support them, and independent replay of the Lean build
has not been done here.
