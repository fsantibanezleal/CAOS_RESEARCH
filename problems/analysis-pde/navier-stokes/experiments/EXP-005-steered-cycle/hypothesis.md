# EXP-005 hypothesis: the steered growth, steering and hold cycle, in the ODE and in the PDE

Committed 2026-09-14, before any code for this experiment has run.

## The gap this closes

EXP-004 Part A tried a dynamical two-layer run and was inconclusive by construction: it never
implemented the steering that returns a grown layer to a stationary holding state, so the second layer
grew on a background that was still shearing. EXP-004 Part B confirmed the handoff only on a frozen
surrogate. This experiment implements the steering itself, transcribed from the primary source, and
uses it to produce the frozen layer dynamically.

## What is transcribed (Alpoge-Buckmaster, Boussinesq paper, Subsections 3.3 and 3.6.2)

First-stage normalized model, their (3.25): for a trial pulse amplitude `mu`,

```
P_tautau = z(tau) P,    P(0) = P_tau(0) = 1,    tau_b = 1 + 1/Lambda
z(tau) = 1 - eta(tau)                      on [0, 1]
z(tau) = -mu Lambda h(Lambda (tau - 1))    on [1, tau_b]
```

with `eta` a smooth step and `h >= 0` a unit-mass profile on (0, 1), `H = max h`. Lemma 3.7 asserts,
under `c_p > 1`, `Lambda >= 2 c_p H`: `P > 0` for every trial; `1/(1+tau) <= v <= 1` on [0, 1] with
`v = P_tau/P`; `log 2 <= int_0^1 v <= 1`; the endpoint map `mu -> v(tau_b; mu)` is strictly decreasing,
positive at 0 and negative at `c_p`; its unique root satisfies `1/2 - 1/(4 Lambda) <= mu* <= 1`; and
`log 2 <= log P(tau_b) <= 1 + 1/Lambda` at the root.

Physical normalization, their Lemma 3.8: `Z = sin(s) z` is the laboratory phase component `zeta_1`,
the common rotation angle is `alpha = s - arcsin Z`, `Gamma = sigma sin s`, `a = sigma^2 sin(s)/lambda`,
`b = lambda Z`, `tau = Gamma (t - t_1)`, data on the growing eigenline `Omega = (lambda/sigma) Theta`,
`Theta < 0`. At the selected root, `zeta_1 = Omega = 0` at the end of steering and both stay zero.

## The PDE realization, and why it is exact

The construction's common rotation is a forced rigid rotation `D = alpha_dot J` of the whole
background, which cannot live on a torus. In 2D it does not need to: in the frame co-rotating with
angle `alpha`, the Coriolis and centrifugal accelerations are gradients and are absorbed by the
pressure, and the Euler acceleration only shifts the spatially uniform mean vorticity, which induces no
velocity on the torus. What remains is the Boussinesq system with a **rotating gravity direction**,
`g(t) = e(alpha(t)) = (sin alpha, cos alpha)` in co-rotating coordinates, buoyancy torque
`g_2 d_1 theta - g_1 d_2 theta`. The stratification and every wavevector are fixed in this frame, so
each wave stays an exact grid mode. For a wave at unit `zeta` this torque gives exactly
`b = lambda (zeta . (cos alpha, -sin alpha)) = lambda sin(s - alpha) = lambda Z`, the transcribed
coefficient. The base stratification `-(A/lambda_0) sin(lambda_0 x_2)` is no longer steady once
gravity tilts; its torque is cancelled by a low-frequency force, which is precisely the role the
forcing plays in the construction.

## A derived statement to be tested, not assumed

With equal dissipation `-nu (-Laplacian)^alpha` on both fields, the damping `d = nu lambda^(2 alpha)`
enters both amplitude equations identically, so `(Theta, Omega) = e^(-d t) (Theta~, Omega~)` with the
tilde pair solving the inviscid system. Consequences: the steering root `mu*` is **independent of the
dissipation**, the zero of `Omega` lands at the same time, and the hold decays at exactly `d`.

## Parameters

- Part A (ODE, paper-admissible): `c_p = 3`, `h = 2 sin^2(pi y)` so `H = 2`, `Lambda = 12 = 2 c_p H`,
  `eta` the standard C-infinity step. Also run at the PDE design `Lambda = 2.5`, which is outside the
  proof's sufficient condition; root existence there is reported, not assumed.
- Parts B and C (PDE): N = 512, `lambda_0 = 1`, `A = 4` so `sigma = 2`, wave `k = (4, 31)`, so
  `lambda = 31.26`, `sin s = 0.128`, `Gamma = 0.256`; `Lambda = 2.5`; growth length `L_growth = 6` plus
  the unit transition; seed `Theta = -1e-6` on the eigenline; hold of length `4/Gamma`; dt = 2e-3.
  Amplitudes read at the origin by demodulation (`Theta = -2 Im c_theta`, `Omega = 2 Re c_omega`).
  Part C: `alpha = 1/2`, `nu` set so `d = 0.2 Gamma`.
- Part D (PDE, two layers): N = 1024. Stage 1 as in B but seeded so the deposit `lambda_1 |Theta_1|`
  at the hold is about `A`. Then a layer-2 wave in the hold, laboratory angle `pi/6`, `|k_2|` near 256.

## Gates

**A. Transcription.** At `Lambda = 12` every assertion of Lemma 3.7 listed above holds on a fine grid
of the steering interval and on a 200-point `mu` grid in `[0, c_p]`. FAIL means the transcription is
wrong, and nothing downstream runs.

**B. Inviscid steered cycle in the PDE**, at the ODE-selected `mu*`:

- B1 `|Omega(t_b)| / max|Omega| < 2e-2` in the PDE, and the PDE `Theta(t_b)` within 2 percent of the ODE.
- B2 the endpoint map: PDE `Omega(t_b)/max|Omega|` at `mu` in {0, `mu*`, 2 `mu*`} within 0.02 absolute
  of the ODE values.
- B3 hold: over `4/Gamma` after `t_b`, `Theta` changes by less than 1 percent and
  `|Omega|/max|Omega|` stays below 3e-2.
- B4 numerical control: dt halved moves `Theta(t_b)` by less than 1e-3 relative.
- Negative controls, each must FAIL the zero-landing gate: `mu = 0` (steering without the pulse)
  must leave `|Omega(t_b)|/max|Omega| > 0.2`; fixed gravity (no steering at all) must leave `Omega`
  growing through `t_b`.

**C. Dissipative cycle**: the PDE `mu*` landing still satisfies B1 using the inviscid `mu*`; the
measured hold decay rate equals `d` within 2 percent; and `Theta(t) e^(d t)` matches the inviscid run
within 2 percent over the whole cycle.

**D. Dynamical handoff with steering**: a large-amplitude repeat of B (the Part D stage 1) must still
pass B1 at 5e-2, or D is rerun at a smaller deposit and that is recorded. Then, as in EXP-004, the
local rate field of layer 2 against the prediction from the TOTAL low-pass gradient (H1) and from the
base alone (H2): PASS if H1 correlation > 0.9 and H2 correlation is lower by more than 0.3 with a
larger RMSE. The slope is reported, not gated, because EXP-004 characterized a measurement-geometry
systematic in it.

## What each outcome would mean

A PASS of B to D replaces EXP-004's frozen surrogate with the construction's own mechanism: a layer
grown, steered to a stationary state by the transcribed control, and then serving as background for
the next. A FAIL of B with A passing would mean the reduction breaks during steering, where the
coefficients change fastest, which is the most informative failure available. A FAIL of C would refute
the damping factorization derived above. None of this bears on the viscous problem directly; it is a
check of the mechanism in the regime where the published results live.
