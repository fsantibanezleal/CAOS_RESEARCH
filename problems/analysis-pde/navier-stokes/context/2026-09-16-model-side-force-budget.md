# What our cascade model is still missing, and what the published budget already decides for it

Date: 2026-09-16. Backlog item NS-016, opened by the threshold reconstruction of
[`2026-09-14-threshold-reconstruction.md`](2026-09-14-threshold-reconstruction.md).

Code: `nslib/cascade.py` (super-geometric schedules) and `nslib/cmz_budget.py`
(`feasible_R_interval`), with tests in `code/tests/test_cascade.py`,
`code/tests/test_cmz_budget.py` and the exact pair in `tests/test_navier_stokes_threshold.py`.

Convention: `alpha` is OURS, `(-Laplacian)^alpha`, unless a line says otherwise. Theirs is twice ours.

## 1. The question

EXP-003 produced a cascade threshold `alpha_c = 1/(4p)` from four constraints: summable amplitudes,
growth positivity, a finite time budget, and layer survival. The published threshold is a factor 5.4
below our cap, and round 2 established why: the published constant is set by a force-regularity
constraint our model does not contain. This dossier asks what our model would need, and finds that one
piece of the answer is already decided.

## 2. Our model for a general schedule

Our model assumed a geometric background, `A_q = A_0 e^{gq}`. Write `u_q = log lambda_q` and allow any
schedule `u_{q+1} = R u_q`; `R = 1` is the geometric case and `R > 1` is super-geometric, which is what
every published construction uses (`M_{n+1} = M_n^R` in Cordoba-Martinez-Zoroa-Zheng,
`lambda_q = lambda_{q-1}^{Q_q}` with `Q_q >= 200` in Alpoge-Buckmaster). With `lambda_q = c A_q^p`, so
`log A_q = u_q / p` up to a constant, the amplification identity `A_{q+1} = lambda_q Theta_q` gives

    log Theta_q = u_q (R/p - 1).

So:

| constraint | geometric form | general form |
|---|---|---|
| C1 summable amplitudes | `p > 1` | **`R < p`** |
| C2 growth positivity | `alpha p < 1/4` | unchanged |
| C3 finite time budget | not binding | not binding, and less so |
| C4 layer survival | same as C2 | unchanged |

Only C1 moves, and the threshold `alpha_c = 1/(4p)` is untouched. `R` is not a free parameter beside
`p`: the same identity gives `R = p (1 + log Theta_q / u_q)`, so choosing how much amplitude each
stage spends IS choosing the schedule.

## 3. What the published budget already decides

The force budget is a quadratic in the frequency ratio: a positive margin needs
`7 alpha R^2 - (2 + 3 alpha) R + 2 < 0` (their convention), so the admissible ratios form an interval
that closes exactly at their threshold, with lower end above 1 at every positive alpha. Combining with
`p > R`:

    alpha_c <= 1 / (4 R_-(2 alpha)),   and no admissible R at all above the published threshold.

| `alpha` (ours) | admissible `R` | cap `1/(4 R_-)` |
|---|---|---|
| 0.01 | (1.045, 13.67) | 0.2392 |
| 0.02 | (1.105, 6.47) | 0.2263 |
| 0.0463 | (1.716, 1.80) | 0.1457 |
| 0.05 | none | none |
| 0.25 | none | none |

**Our cap of 1/4 is therefore never reached.** It was derived from the dissipation constraint alone,
and the schedule it would require is inadmissible for reasons that have nothing to do with
dissipation: above the published threshold there is no frequency ratio at all for which the force can
be controlled. The honest statement of our model's result is now:

> `alpha_c = 1/(4p)` is correct for the reduced model, and vacuous as a bound on the real problem,
> because the schedules that approach it are excluded by the force budget before the dissipation
> constraint ever binds.

## 4. What is still missing, precisely

To have a force budget of our own rather than importing theirs, our model needs three objects it does
not have:

1. **A localization scale.** Their `L_n` (constraints S, L, O) is the envelope wavenumber of layer `n`.
   Our model has plane waves, whose envelope is trivial, so there is no `b` exponent to carry.
2. **The residual of the ansatz.** The force is whatever the equation needs beyond the exact
   cancellation: in the Boussinesq setting that is the commutator of the envelope with the transport,
   plus the corrections that cancel oscillatory localization errors to successively higher order
   (Alpoge-Buckmaster's correction hierarchy, their `J_q = 2 k_q + 8` levels).
3. **A norm.** Their budget is summability in `L^1_t C^r_x` with `r < s`; ours would be the same, but
   the exponents differ because their layers are vortex layers with rate `A_{n-1}` while our waves are
   Boussinesq pendula with rate `sqrt(A)`. That difference is why their `D` reads `a = alpha R` and our
   C2 reads `alpha p < 1/4`; the two are not the same constraint written twice.

Item 2 is the real work, and it is a reading task on the primary sources before it is a calculation:
Alpoge-Buckmaster Sections 4 to 10 for the correction hierarchy, and their force estimates. It is
recorded as the open half of NS-016 rather than guessed at here.

## 5. What this changes in the record

- EXP-003's verdict stands as a statement about the model, and its scope is now sharper: the cap it
  measures is unreachable under the published force budget.
- Wiki page 4's landscape row for our cap keeps its meaning (necessary, not sufficient) and gains the
  reason it is loose.
- The bare threshold question remains not ours, as recorded at the Phase 0 gate.
