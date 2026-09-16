# EXP-005 verdict: the steered cycle reproduces the PDE, and the background's own instability is the limit

Date: 2026-09-15. Hypothesis committed first at
[`hypothesis.md`](hypothesis.md) (commit `e636748`), before any code for this experiment ran.
Runner: [`code/run_exp005.py`](../../code/run_exp005.py); control law
[`code/nslib/steering.py`](../../code/nslib/steering.py); solver
[`code/nslib/corotating.py`](../../code/nslib/corotating.py); diagnostic
[`code/diagnose_hold.py`](../../code/diagnose_hold.py). Hardware: RTX 4070 Laptop, float64.

**Verdict: DECIDED IN PART.** Gate A passes. Gates B and C pass in full on the repaired
configuration, and the run at the parameters committed in the hypothesis is REFUTED, for a reason
that is a property of the mechanism rather than of the code. Gate D reproduces the handoff pattern
with a discriminating control, but not at the correlation the gate demanded, and the reason is
characterized rather than explained away.

## A. The transcription (PASS)

Every assertion of Alpoge-Buckmaster Lemma 3.7 holds numerically for the paper-admissible design
(`c_p = 3`, `h = 2 sin^2(pi y)` so `H = 2`, `Lambda = 12 = 2 c_p H`):

| assertion | result |
|---|---|
| `P > 0` for every trial pulse | holds, minimum 1.0 over 200 trials |
| `1/(1+tau) <= v <= 1` on the ramp | holds |
| `log 2 <= int_0^1 v <= 1` | 0.90048 |
| endpoint map strictly decreasing, positive at 0, negative at `c_p` | +0.6418 to -2.5018, monotone |
| their (3.28), `mu* in [1/2 - 1/(4 Lambda), 1]` | `mu* = 0.66321` |
| their (3.29), `log P(tau_b) in [log 2, 1 + 1/Lambda]` | 0.92839 |
| `v(tau_b; mu*) = 0` | 2.3e-17 |

The same checks run in repository CI in `tests/test_navier_stokes_steering.py`, which is why the
control law is kept free of torch.

## B. The steered cycle in the PDE

### B.1 At the committed parameters: REFUTED, and the cause is the mechanism

The committed configuration (`k = (4, 31)`, `sin s = 0.128`, `Lambda = 2.5`, 36.7 time units) fails
every gate: the measured amplitude grows by a factor 726 during the holding interval and changes
sign. Raw output preserved at
[`result-B-committed-parameters-REFUTED.json`](result-B-committed-parameters-REFUTED.json).

`diagnose_hold.py` separates instrument from physics by dumping the exact Fourier coefficient, three
demodulation radii, and the individual neighbour modes. The answer is physics:

| quantity | at `t_1` | at `t_b` | at the end |
|---|---|---|---|
| horizontal neighbour modes | 1.0e-07 | 8.5e-03 | 3.3e-02 |
| max abs theta (background is 4.0) | 4.00001 | 4.910 | 10.02 |

**The background this construction grows on is Rayleigh-Taylor unstable at rate `sqrt(A) = 2.0`,
while the steered layer grows at `sqrt(A) sin s = 0.256`.** Every mode at a more favourable angle
therefore gains `1/sin s` times as many e-folds as the layer does. Over the 37 time units the
committed schedule needs, that is about 72 e-folds from round-off, which is more than enough to take
the run over. The construction tolerates this because each layer is localized and the force controls
what happens outside; a plain periodic box has neither.

This is now a gate of its own (B5) rather than a possible silent contamination: `parasite_level`
measures the largest amplitude among modes `(k_1 + d, k_2)`, where the layer puts nothing and the
fast angles live, together with the excess of `max |theta|` over the background's own maximum.

### B.2 On the repaired schedule: PASS, every gate

Repair: raise the insertion angle so the layer grows at half the background's own rate
(`k = (15, 26)`, `sin s = 0.4997`, `Lambda = 1`, about 10 time units). Parasites then sit sixteen
orders below the wave. Two backgrounds were run, identical in everything else:

| | sine, `-(A/lam0) sin(lam0 x2)` | flattened, gradient affine to 4th order |
|---|---|---|
| vorticity landing, `abs(Omega(t_b))/peak` | 1.57e-02 | **3.67e-04** |
| steering gain against the ODE | 1.80e-02 | **3.06e-06** |
| absolute amplitude ratio to the ODE | 1.0315 | **1.0000** |
| hold: amplitude drift over `3/Gamma` | 14.7 % | **0.36 %** |
| hold: `abs(Omega)/peak` | 14.6 % | **0.34 %** |
| endpoint map, worst gap over the three trials | 0.196 | **4.7e-04** |
| dt halved, shift of the gain | 1.0e-03 | **8.7e-04** |
| parasites relative to the wave at `t_b` | 3.4e-16 | 1.0e-15 |
| gates passed | 4 of 7 | **7 of 7** |

Raw: [`result-B-sine.json`](result-B-sine.json), [`result-B-flattened.json`](result-B-flattened.json).

The two columns differ only in the curvature of the background over the layer's support, so that
curvature is the entire residual. This is not a tuning: the reduction assumes an AFFINE background,
which the construction arranges by localizing each layer where its background is affine; on a torus
the flattest available profile is the closest analogue, and the sine column is the price of not
having one.

**Negative controls, both required to fail, both do.** Without the pulse (`mu = 0`) the vorticity
amplitude is still at 0.99985 of its peak at `t_b`, against 1.0 in the ODE. With gravity frozen, so
no steering at all, it is at 1.0, still growing. The endpoint map is reproduced at all three trial
pulses to 4.7e-04, which is the sharp form of the claim: the PDE agrees with the ODE not only where
the control works but also where it is deliberately mis-set.

**A defect found and fixed rather than tolerated.** At the `2 mu*` trial the schedule asks for a
laboratory phase component of 1.07, which no unit vector has. The ODE was following that
unrealizable request while the PDE followed the physically clipped one, and the two disagreed for a
reason that had nothing to do with the physics under test. The clip is now applied in one place,
shared by both, and reported per trial (`schedule_clipped`).

## C. Dissipation factorizes (PASS)

Derived in `nslib.steering` before the run: with equal dissipation on both fields the damping
`d = nu lambda^(2 alpha)` enters both amplitude equations on the diagonal, so the whole cycle is the
inviscid cycle times `e^(-d t)`. Three consequences, all tested against the PDE at `alpha = 1/2` with
`d = 0.2 Gamma`:

| prediction | result |
|---|---|
| the INVISCID pulse amplitude still lands the vorticity at zero | landing 4.1e-04 |
| the holding interval decays at exactly `d` | measured 0.17479 against `d = 0.17311`, 0.97 % |
| `e^(d t)` times the viscous run reproduces the inviscid one | worst 0.24 % over the whole cycle |

Raw: [`result-C-dissipative.json`](result-C-dissipative.json). This is the statement that a
dissipative cascade may reuse the inviscid steering unchanged, and that a holding interval costs
exactly `exp(-nu lambda^(2 alpha) T)`, which is the assumption EXP-003's constraint C4 was built on.
