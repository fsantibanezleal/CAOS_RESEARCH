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

## D. The dynamical handoff, with steering (DECIDED IN PART)

This is the run [EXP-004](../EXP-004-multilayer-handoff/verdict.md) Part A could not do. There, layer 1
was grown and layer 2 injected while layer 1 was still shearing, and the result was inconclusive by
construction; Part B had to replace the grown layer with a frozen sinusoid. Here layer 1 is grown,
**steered to rest by the transcribed control**, and then serves as the background for layer 2.

**Stage 1, at the amplitude that matters.** Seeded so that its deposit is comparable with the base
gradient, layer 1 reaches `lambda_1 |Theta_1| = 3.69`, that is `0.92` of the background it grew on,
and the steering still works at that amplitude: landing `3.8e-04`, steering gain to `3.2e-05` of the
ODE, hold drift `0.91` percent, parasites `1.2e-14` of the wave. The cycle is not a small-amplitude
phenomenon.

**Stage 2, the local rate field.** Layer 2 is injected into the holding interval and its local growth
rate measured by demodulation, then compared with the rate predicted from the TOTAL low-pass gradient
(H1) and from the base alone (H2, the discriminating control):

| configuration | H1 correlation | H2 control | H1 RMSE | H2 RMSE |
|---|---|---|---|---|
| `lam2 = 192`, window `1.5 lam1` | 0.676 | 0.360 | 0.404 | 0.507 |
| `lam2 = 192`, window `3 lam1` | 0.755 | 0.335 | 0.348 | 0.485 |
| `lam2 = 192`, window `4.5 lam1` | 0.327 | 0.667 | 0.369 | 0.288 |
| **`lam2 = 360`, window `3 lam1`** | **0.808** | **0.392** | **0.287** | **0.432** |

**The pattern is confirmed and the control discriminates**, by 0.42 in correlation and with a
40 percent worse RMSE, which is gate D2. **Gate D1, correlation above 0.9, is NOT met**, and that is
reported as not met rather than softened.

What limits it is measurement, and the sweep shows it rather than asserting it. The rate field is read
through a demodulation window that must resolve an envelope varying on layer 1's own scale while
excluding layer 1's harmonics, so there is an interior optimum: too narrow and the structure under
test is smoothed away, too wide and the base-only prediction fits better than the true one, which is
what the 4.5 row is. At the optimum, raising the scale separation from 6 to 12 moves the correlation
from 0.755 to 0.808, the same direction EXP-004 reached 0.999 in at separation 12 on a frozen,
purely vertical background with no steering history. The residual slope, 1.26, is the same
measurement-geometry systematic EXP-004 characterized at 1.36.

**A trap found here and now guarded.** At `lam2 = 320` with `N = 1024` the wave sits at 0.94 of the
2/3 dealiasing limit and passes a naive check, but its demodulation WINDOW reaches past the limit, so
half the envelope is annihilated every step. The only symptom is systematically low rates and a
correlation falling from 0.68 to 0.42. The guard now counts the window, not just the wave.

## What EXP-005 establishes, and what it does not

**Establishes.**

1. The steering control, transcribed from the source, does what its lemma says, and a PDE realization
   of it reproduces the reduced model to `3e-06` in the gain and `4e-04` in the landing, with the
   endpoint map reproduced at a deliberately mis-set pulse as well as at the selected one.
2. A holding interval under dissipation costs exactly `exp(-nu lambda^(2 alpha) T)`, and the selected
   pulse does not depend on the viscosity. EXP-003's constraint C4 rested on the first of those.
3. A steered layer at 0.92 of the background gradient serves as the background for the next layer, and
   that layer responds to the TOTAL accumulated gradient rather than to the base alone.

**Does not establish.**

- Anything about many layers: two is not a cascade, and the time-compression that makes infinitely
  many stages fit in finite time is untouched here.
- Anything at the correlation the D gate asked for. 0.808 is not 0.9.
- Anything about the viscous problem. This is a 2D Boussinesq model system, and the whole cycle lives
  at the hypodissipative end.

**And it adds one caveat the exponent bookkeeping cannot see.** The cascade runs against a faster
instability of its own background, by exactly the factor `1/sin s` in the exponent. The committed
first run was destroyed by it, and no amount of numerical care would have saved that configuration:
what saves the real construction is localization and forcing, not speed.
