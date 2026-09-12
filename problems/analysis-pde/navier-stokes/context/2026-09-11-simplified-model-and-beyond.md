# Can we build a simplified model with the same behaviour, and can we go beyond it?

Date: 2026-09-11. This answers the three questions put to the session: whether a simplified version of
the September 2026 blowup can be built, how deep the argument and the scenario really go, and whether
there is anything beyond the current findings that is ours to take. It is written from the dossiers in
this folder, not from memory.

## 1. The uncomfortable first answer: the simplified version already exists, in print

The natural instinct is to reduce the blowup to a small model and integrate it. That model is
Subsection 1.2 and Lemma 3.1 of the Alpoge-Buckmaster Boussinesq paper. It is four real unknowns,

$$\dot\zeta = -D^{T}\zeta, \qquad
  \dot\Theta = -\frac{J\zeta\cdot G}{\lambda|\zeta|^2}\,\Omega, \qquad
  \dot\Omega = \lambda\zeta_1\Theta,$$

and it is *exact*, not asymptotic: where the envelope $g$ equals one and the profile $F(s)$ equals $s$,
the wave solves the equations with no nonlinear correction at all. Writing this system down and
integrating it is **reproduction**. Our own counterexample radar rules say it in two lines: "Reproduce
a public candidate independently before extending it" and "Credit discovery priority explicitly;
replication is not rediscovery." The bougard-joret ledger rejected exactly this move a week ago, in
its own words: repackaging a local reconstruction of a published mechanism as a discovery of the
session would be false.

So the reproduction is worth doing, and it is worth doing well, but it is a **control**, not a result.
It earns its place by being the instrument that the rest of the work is measured with, and by being
the thing that catches us if our understanding of the mechanism is wrong.

That settles the first question honestly: yes, we can build a simplified version with the same
behaviour, in an afternoon, and it is not a contribution.

The real question is the second one.

## 2. Where the two constructions are actually separated: viscosity

Every result in the Cordoba-Martinez-Zoroa lineage is inviscid or Darcy. IPM is a zeroth-order Darcy
law, Boussinesq is taken inviscid, Euler is inviscid by definition. Alpoge and Buckmaster state they
believe they also have blowup for **hypo-dissipative** Navier-Stokes and have not released it. Tao's
assessment is that the route has a high likelihood of extending to Navier-Stokes but does not get
there yet. OpenAI, reaching for Navier-Stokes itself, did not use a layer cascade at all: they used a
self-similar vortex core with an anisotropic Reynolds split, $\mathrm{Re}_{\theta}\asymp\tau^{-h}
\to\infty$ and $\mathrm{Re}_r = O(1)$.

Three independent facts pointing at one obstruction. It is worth computing what the obstruction
actually is, because the modulation system makes it a two-line calculation and neither paper we have
read states it in this form.

### 2.1 The dissipative modulation system

Add dissipation to both Boussinesq equations, with a fractional Laplacian of order $\alpha\in(0,1]$ so
that the classical viscous case is $\alpha=1$:

$$\partial_t\theta + u\cdot\nabla\theta = -\nu(-\Delta)^{\alpha}\theta + f_{\theta}, \qquad
  \partial_t\omega + u\cdot\nabla\omega = \partial_1\theta - \nu(-\Delta)^{\alpha}\omega + \operatorname{curl} f_u.$$

The ansatz is unchanged: $\vartheta=\Theta(t)\sin s$, $\varpi=\Omega(t)\cos s$, $s=\lambda\zeta(t)\cdot x$.
The two cancellations that make the ansatz exact are purely geometric, $v\perp\zeta$ while
$\nabla\vartheta\parallel\zeta$, so $v\cdot\nabla\vartheta=v\cdot\nabla\varpi=0$ survives dissipation
untouched, and so does the phase-transport condition $\dot\zeta=-D^{T}\zeta$. The fractional Laplacian
is diagonal on the phase, $(-\Delta)^{\alpha}\sin s = (\lambda|\zeta|)^{2\alpha}\sin s$. So the
dissipative system is the inviscid one with one damping term per amplitude:

$$\boxed{\;\dot\Theta = -\frac{J\zeta\cdot G}{\lambda|\zeta|^2}\,\Omega - \nu(\lambda|\zeta|)^{2\alpha}\Theta,
  \qquad
  \dot\Omega = \lambda\zeta_1\Theta - \nu(\lambda|\zeta|)^{2\alpha}\Omega. \;}$$

In the frozen configuration used in the paper ($D=0$, $G=-Ae_2$, $\zeta=r\,e(\varphi)$) the matrix is
the inviscid one minus $\nu(\lambda r)^{2\alpha}I$, so its eigenvalues are

$$-\nu(\lambda r)^{2\alpha} \pm \sqrt{A}\,\sin\varphi .$$

### 2.2 The one fact that decides everything

**The inviscid growth rate $\sqrt{A}\,\sin\varphi$ does not depend on $\lambda$, while the damping
$\nu(\lambda r)^{2\alpha}$ grows in $\lambda$ without limit.**

This is the whole obstruction in one sentence, and it is visible only once the eigenvalue is read
correctly. The growth rate is $\sqrt{A}\sin\varphi$, not $\sqrt{A\sin\varphi}$, and in neither reading
does it carry a $\lambda$: the $\lambda$ in the $\dot\Omega$ coefficient cancels against the
$1/\lambda$ in the $\dot\Theta$ coefficient. Amplification is set by the background gradient alone.
Frequency buys gradient, not growth. Dissipation charges for frequency, quadratically or worse.

The cascade therefore runs into a cap. Growth at stage $q$ requires

$$\nu(\lambda_q r)^{2\alpha} < \sqrt{A_q}\,\sin\varphi
  \qquad\Longrightarrow\qquad
  \lambda_q \;\lesssim\; \Big(\frac{\sqrt{A_q}}{\nu}\Big)^{1/(2\alpha)} \;\asymp\; A_q^{1/(4\alpha)}\,\nu^{-1/(2\alpha)} .$$

### 2.3 What the cascade needs, against what it is allowed

The mechanism amplifies because a short wave carries a small amplitude and a large gradient:
$\nabla\vartheta(0,t)=\lambda\Theta\zeta$. The background gradient handed to the next stage is
therefore of size $A_{q+1}\asymp\lambda_q\Theta_q$. Meanwhile the blowup statement itself demands
$\sup_t\lVert\theta(t)\rVert_{\infty}<\infty$ while $\lVert\nabla\theta(t)\rVert_{\infty}\to\infty$, so
the amplitudes must stay summable, $\sum_q\Theta_q<\infty$. Combining the requirement with the cap,

$$A_{q+1} \;\asymp\; \lambda_q\Theta_q \;\lesssim\; \Theta_q\,A_q^{1/(4\alpha)}\,\nu^{-1/(2\alpha)} .$$

Write $a_q=\log A_q$. The recursion is

$$a_{q+1} \;\lesssim\; \underbrace{\frac{1}{4\alpha}}_{\text{coefficient}}\,a_q
  \;\underbrace{-\;\frac{\log\nu}{2\alpha}-\log r}_{\text{constant}}
  \;+\;\underbrace{\log\Theta_q}_{\text{drift}} .$$

The homogeneous coefficient is $1/(4\alpha)$, which crosses $1$ exactly at $\alpha=1/4$: the map is an
expansion below that value and a contraction above it.

**This is where the first draft of this dossier overreached, and the smoke test caught it.** Reading
the coefficient crossing as a clean critical exponent $\alpha_c=1/4$ ignores the other two terms, and
they are not small. The constant $-\log\nu/(2\alpha)$ is large and positive for small viscosity, and
the drift $\log\Theta_q$ is negative and grows with $q$ at a rate that depends on how the summable
budget is spent. `code/modulation_smoke.py` integrates the recursion over 4,000 stages for two legal
budgets ($\Theta_q=2^{-q}$ and $\Theta_q=(q+1)^{-2}$) and four viscosities, and the outcome is:

| $\alpha$ | escapes in how many of the 8 parameter settings |
|---|---|
| 0.20 | 8 of 8 |
| 0.24 | 4 of 8 (only the favourable viscosities and the gentler budget) |
| 0.26 | 0 of 8 |
| 0.30 | 0 of 8 |
| 0.50 | 0 of 8 |

So the defensible statement is weaker than a critical exponent and stronger where it counts:

> **$\alpha = 1/4$ is an upper bound for the cascade threshold in this ansatz, not an achieved
> threshold.** No escape was observed at any $\alpha>1/4$ in any parameter setting tried. Below $1/4$
> escape is not automatic: the constant and the drift can still kill it, as they do at $\alpha=0.24$
> for the harsher budget. The true threshold is at most $1/4$ and depends on $\nu$ and on how the
> amplitude budget is spent.

A second caveat, carried deliberately in the code docstring: **this recursion has no time axis.**
Finite-time blowup also needs $\sum_q T_q<\infty$ with $T_q$ the stage growth time, and that
constraint is entirely absent above. Escape of $a_q$ is therefore *necessary but not sufficient*. Any
claim about a threshold has to model the time budget too, and that is the first thing the real sweep
must add.

What survives all of this untouched is the part that matters for reading the published record:
classical viscosity is $\alpha=1$, four times the upper bound, and the failure there is not marginal.
The cap $\lambda\lesssim A^{1/4}$ sits far below the requirement $\lambda\asymp A$, in every parameter
setting tried, by orders of magnitude. The naive layer cascade does not reach classical Navier-Stokes,
and no tuning of $\nu$ or of the amplitude budget brings it close.

### 2.4 Why this is worth taking seriously: it explains the published record

A scaling heuristic is worth what it predicts about facts it did not use. This one was derived from
Subsection 1.2 of a single paper, and it accounts for the rest of the landscape:

- **Every published result in the program is at or below the threshold.** IPM is Darcy, a zeroth-order
  multiplier, $\alpha=0$. Inviscid Boussinesq and inviscid Euler, $\alpha=0$. All strictly below
  $1/4$, all succeed.
- **Alpoge and Buckmaster claim hypo-dissipative Navier-Stokes and not Navier-Stokes.** Hypo-dissipative
  means exactly $\alpha<1$. The bound sharpens it to a number they should be at or under, and gives us
  a falsifiable comparison the day their paper appears.
- **Tao says the route should extend, but has not.** Consistent with an obstruction that is a finite
  quantitative gap, not a structural impossibility.
- **OpenAI did not use a cascade for Navier-Stokes.** They used a self-similar core in which the
  amplification itself diverges like $\tau^{-1/2-h}$ rather than being handed from layer to layer at a
  fixed background, and they kept $\mathrm{Re}_r=O(1)$, that is, they arranged for viscosity to stay in
  balance with the radial inflow instead of trying to outrun it. In the language above, they escaped
  the cap by refusing the trade that creates it.

That is four independent facts explained by one mechanism. It is the reason this line is worth machine
time rather than a paragraph.

### 2.5 What would refute it

Stated plainly so that a later result can kill it cleanly. The bound is refuted if any of the
following holds: the Alpoge-Buckmaster hypo-dissipative paper closes the cascade for some
$\alpha\ge 1/4$; a sweep of the dissipative modulation system exhibits sustained growth of $A_q$ at
$\alpha>1/4$ under a summable amplitude budget and a convergent time budget; or the steering and
holding intervals, which the calculation above ignores entirely, are shown to change the coefficient
rather than the constant.

The third is the most likely and is the first thing to test. Holding intervals are periods in which
$\dot\Theta=\dot\Omega=0$ in the inviscid system, arranged by steering $\zeta_1$ to zero so the next
layer can grow undisturbed. In the dissipative system those same intervals are **not** quiescent: with
$\zeta_1=0$ the coupling vanishes but the damping $-\nu(\lambda|\zeta|)^{2\alpha}$ does not, so both
amplitudes decay throughout the hold. Dissipation does not wait while the construction waits. That
consideration pushes the real threshold **down**, not up, and it is the single largest missing piece
in the estimate above.

The honest summary of this subsection: the derivation in 2.1 is exact and verified, the cap in 2.2 is
immediate, and the threshold in 2.3 is an upper bound with two known omissions (no time budget, no
hold-time damping), both of which move it in the same direction.

## 3. What is actually ours to take

Ranked by whether it is a contribution or a service, and by whether we can finish it.

**A. Independent statement audit of the two certificates.** Done for Navier-Stokes (C) and (D) in
[`2026-09-11-lean-statement-audit.md`](2026-09-11-lean-statement-audit.md): faithful, with the
third-party DeepMind reference statement as the strongest fact in the repository. Not done for the
unforced Euler certificate, which has no external reference statement and therefore needs it more.
This is service work of real value to a community that currently has opinions and no audits, it is
finishable in days, and it is honest about being an audit rather than a theorem.

**B. Independent replay of the Lean builds.** Mechanical, expensive, and the only verification anyone
can do today. Cheapest real check available. Budgeted as EXP-001.

**C. Reproduction of the inviscid modulation system with a positive control against the PDE.** The
control, per Section 1. Its value is not the ODE; it is the comparison nobody publishes: does the
reduced modulation system actually track a direct 2D Boussinesq simulation through a growth, steering
and holding cycle, and where does it stop tracking? A reduced model that is never checked against the
equation it reduces is a picture, not an instrument.

**D. The dissipative threshold.** The one place a genuinely new statement might sit. Target: locate the
cascade threshold for the layer ansatz with the two omissions repaired, that is, with an explicit time
budget $\sum_q T_q<\infty$ and with damping charged during the holding intervals. The upper bound
$1/4$ is the starting hypothesis, not the answer; the sweep exists to find where the real transition
sits and how it depends on $\nu$ and on the amplitude budget. This is the "go beyond" answer, and it is
deliberately small: not the Clay problem, not even Navier-Stokes, but a quantitative statement about
the exact mechanism both September 2026 papers are built on.

**E. A model equation carrying the threshold.** The tradition is respectable and well defined:
Constantin-Lax-Majda, De Gregorio, Cordoba-Cordoba-Fontelos, and Tao's averaged Navier-Stokes are all
simplified systems built to isolate one mechanism, and the last of these is a landmark precisely
because the simplification was chosen to carry the obstruction rather than to avoid it. The slot here
is a dissipative layer-cascade model in which the transition at $\alpha_c$ can be proved by hand. This
is the most ambitious item and the only one that would be a paper on its own. It is downstream of D
and should not be started before D produces a number.

## 4. Honest novelty assessment

Required by the radar rules before any of this gets machine time.

- The inviscid modulation system: **not novel**, it is Subsection 1.2 and Lemma 3.1 of a public paper.
- The dissipative modulation system of Subsection 2.1: an elementary extension of a public ansatz. Any
  competent reader of that paper would write the same three lines. It is not a contribution by itself.
- The $\alpha\le 1/4$ upper bound: **novelty UNVERIFIED, and quite possibly already known.** The
  unreleased Alpoge-Buckmaster hypo-dissipative paper is the obvious place it would appear, and they
  have had it since before 2026-09-07. We have read Section 1 of one of their three papers; Sections 3
  to 10 have not been read and may contain the dissipative analysis outright. The correct posture is to
  derive and test it as our own, record the date, and compare the moment their paper appears, expecting
  to be second. Note also that the bound as it stands is not yet a result: it has two known omissions
  (Subsection 2.5) and it was already weakened once by our own smoke test inside this session.
- The PDE-versus-reduced-model control of item C: not novel as an idea, and not claimed as one.

Nothing above should be described to anyone as our discovery of a blowup mechanism. The mechanism
belongs to Cordoba and Martinez-Zoroa, it was pushed to smooth forcing by Alpoge and Buckmaster, and a
different mechanism for the viscous case was produced by OpenAI.

## 5. What the GPU is actually for

The RTX 4070 on this machine has 8 GB and compute capability 8.9. Three of the four candidate tasks do
not need it and saying so is part of the preflight.

| task | GPU appropriate | why |
|---|---|---|
| integrating one modulation trajectory | no | four ODEs; microseconds on a CPU |
| **ensemble sweep over $(\alpha,\nu,\lambda_q,\varphi_q,\Theta_q)$ schedules** | **yes** | embarrassingly parallel, $10^5$ to $10^7$ independent trajectories, batched as tensors; this is the experiment that locates $\alpha_c$ |
| **direct 2D Boussinesq pseudo-spectral run** | **yes** | the control in item C; resolving a cascade of layers needs large grids and many steps, and FFT-heavy time stepping is what the hardware is for |
| Lean build replay | no | CPU and memory bound, not a GPU workload |
| self-similar profile solve for the OpenAI core | later | needs Section 4 of their paper, which has not been read |

8 GB is the binding constraint on the second one and sets the achievable resolution; that is a sizing
question for the plan, not a blocker. Nothing here needs a cluster, and nothing here needs more than
one heavy job at a time, which our own record insists on.

## 6. The scenario, evaluated

Asked directly whether this changes what the problem is worth to us: it does, but not in the direction
of attacking the Clay problem.

The portfolio row for `navier-stokes` was scored feasibility B, a verification or visualization
surface rather than a real experimental one, and reviewed twice on 2026-09-05 with the verdict that
numerical regularity cannot replace the required existence or breakdown argument. That verdict is
still correct for the Clay problem and nothing here changes it. We are not going to prove or disprove
global regularity.

What changed is that a concrete, finite, checkable surface appeared where there was none: an exact
four-dimensional reduction of a real blowup mechanism, published eleven days ago, extensible to
dissipation in three lines, with a quantitative threshold that explains four independent published
facts and that a consumer GPU can locate in an afternoon of compute. That is a class A surface for a
restricted question sitting underneath a class B problem, which is exactly the shape the radar was
written to find.

The scoping recommendation is therefore to keep the portfolio row honest about the Clay problem and to
open the work on the reduced mechanism, with the threshold as the single target and the audit and
reproduction as the controls around it.
