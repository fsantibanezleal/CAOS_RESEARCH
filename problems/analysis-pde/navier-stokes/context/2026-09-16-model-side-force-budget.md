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
   **Partly answered 2026-09-17 by EXP-007**, for the dissipative term specifically: giving the wave an
   envelope costs the damping law a relative error of `3.6 alpha / (ell lambda)`, first order in the
   bandwidth ratio and depending on that ratio alone. At the construction's separations that is
   `lambda_{q-1}^(3 - Q_q)`, so localization does not obstruct the dissipative reduction and cannot set
   a threshold. What stays open is the INVISCID residual of a localized ansatz, which is items 2 and 3
   below.
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

## 4b. Where the missing piece actually lives, and what shape it has

Scoped on 2026-09-16 by reading the section map and the parameter section of the
Alpoge-Buckmaster paper, so that the open half of NS-016 is entered with its cost known rather than
discovered.

| what is needed | where it is | what form it takes |
|---|---|---|
| the localized profile and the exact datum | 4.1, 4.2 | an even cutoff and an oscillatory profile with a linear interval; a rotating base |
| the weighted derivative machinery | 5.1 to 5.3 | separated rates, weighted differentiation, coupled-equation bounds over a stage |
| summation over future stages | 5.4, 5.5 | geometric-sum bounds transferred to the coefficient fields |
| the corrections | 6.1 to 6.4 | two residual equations in material coordinates, a level-by-level recursion, `J_q = 2 k_q + 8` levels |
| the force estimates themselves | 7.1 | quantitative mixed-derivative estimates for one layer, conditional on explicit coefficient bounds |
| the parameter choice | 8.1 | one finite logarithmic threshold `y = log lambda_1` satisfying (8.1) to (8.6) |

**The shape matters for the estimate of effort.** Cordoba-Martinez-Zoroa-Zheng's Section 4.3 states its
force requirements as four exponent inequalities, which is why the reconstruction of their threshold
took a session. Alpoge-Buckmaster's Sections 5 to 8 are not written that way: they are weighted
mixed-derivative bounds with explicit constants and a common logarithmic threshold, and the exponent
content has to be extracted from them rather than read off. Their (8.1) fixes `log lambda_1` by a list
of finitely many scalar conditions (`y/log y >= 160 Q^2` among them), not by an optimization over
exponents.

So the open half of NS-016 is: extract the exponent content of 7.1 under the correction hierarchy of
6.2, in the Boussinesq variables, and only then optimize. That is a reading unit of the same size as
the round-1 deep-research pass, not a calculation that can be appended to this dossier. What can
already be said without it is in `2026-09-16-smoothness-versus-dissipation.md`: their own rule
`120 k <= Q` fixes the exchange rate between force regularity and frequency ratio, and that alone
decides the trade-off with dissipation.

## 5. What this changes in the record

- EXP-003's verdict stands as a statement about the model, and its scope is now sharper: the cap it
  measures is unreachable under the published force budget.
- Wiki page 4's landscape row for our cap keeps its meaning (necessary, not sufficient) and gains the
  reason it is loose.
- The bare threshold question remains not ours, as recorded at the Phase 0 gate.
