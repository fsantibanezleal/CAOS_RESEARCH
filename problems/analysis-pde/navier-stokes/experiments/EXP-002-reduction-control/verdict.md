# EXP-002 verdict: CONFIRMED

Date: 2026-09-12. Runner: `code/run_exp002.py`.

> **Reproduction, added 2026-09-17.** The exact settings of the run are the `args` block of
> the result file, not the defaults of the runner: `code/reproduce_all.py` rebuilds the
> command line from that block and diffs every numeric leaf of the rerun against the record.
> Verified on 2026-09-17, after the round-2 and round-3 refactors of `nslib`, with every
> result leaf identical. The command is
>
> ```
> python run_exp002.py --A0 4.0 --Theta0 1e-06 --dt 0.0005 --lam 40 --lam0 1 --mode all --n 768 --phi 1.5707963267948966 --t-end 0.6
> ```

Raw outputs: `result.json` (phi = pi/2),
`rate-phi-pi4.json` and `controls-phi-pi4.json` (phi = pi/4). Hardware: RTX 4070 Laptop, 8 GB,
float64, N = 768, dt = 5e-4, t_end = 0.6. Total wall time about 8 minutes.

## Question

Does the Alpoge-Buckmaster modulation system, and the dissipative extension derived in
[`../../context/2026-09-11-simplified-model-and-beyond.md`](../../context/2026-09-11-simplified-model-and-beyond.md),
predict the behaviour of the full nonlinear 2D Boussinesq equations?

The hypothesis and its three pass criteria were committed in the runner docstring before the run.

## Setup

The Alpoge-Buckmaster stratification with the cutoff dropped,
`theta_bg = -(A0/lam0) sin(lam0 x2)` with `omega = 0`, is an EXACT steady state of the unforced
system: `d_1 theta_bg = 0` kills the vorticity source and `u = 0` kills the advection. That is
verified as a unit test (`test_stratification_is_an_exact_steady_state`), and it is what makes the
control clean: any motion observed is the wave, not the background relaxing.

Its gradient is `G(x) = (0, -A0 cos(lam0 x2))`, so the LOCAL background gradient varies with height
and one run yields a curve of predictions indexed by `x2` rather than a single number.

## P1, the rate: PASS

Prediction `sigma(x2) = sqrt(A0 cos(lam0 x2)) sin(phi) - nu |k|^(2 alpha)`, checked where the
background is locally flattest (`cos >= 0.9`).

| configuration | measured | predicted | max rel err | median rel err |
|---|---|---|---|---|
| phi = pi/2, inviscid | 1.999828 | 2.000000 | 1.9e-02 | 4.7e-03 |
| phi = pi/4, inviscid | 1.414271 | 1.414214 | 2.5e-02 | 6.1e-03 |

At the band peak the agreement is 4e-05 relative. The max error sits at the edge of the acceptance
window, where the background gradient varies fastest and the local approximation is weakest, which is
the expected place for it to degrade.

## P2, the band structure: PASS

Where `cos(lam0 x2) < 0` the product of the off-diagonal coefficients changes sign, the eigenvalues
become imaginary and the wave must oscillate rather than grow. Measured over the run: the unstable
band amplified by a factor 3.32 while the stable band ended at 0.57 of its initial amplitude. The
predicted band structure is present.

Note on method: a log-slope fit is meaningless in the stable bands because the amplitude passes
through zero there. The first version of this experiment fitted one anyway and reported a spurious
rate of -0.81. The criterion was changed to an amplitude-ratio bound, which is the quantity the
prediction actually constrains.

## P3, frequency independence: PASS, and this is the load-bearing one

The inviscid growth rate carries no `lambda`: the `lambda` in the `Omega` equation cancels the
`1/lambda` in the `Theta` equation. Everything in the dissipative analysis rests on this, so it was
tested in the PDE and not only in the ODE.

| lambda | 20 | 40 | 80 | 160 |
|---|---|---|---|---|
| measured peak rate | 1.999417 | 1.999828 | 1.999931 | 1.999957 |

Relative spread across an eightfold range of frequency: **2.7e-04**. The residual drift is toward the
predicted 2.0 as `lambda` grows, which is the right direction: larger `lambda` means better scale
separation from the background, which is exactly the regime the reduction assumes.

## The dissipative extension: CONFIRMED quantitatively

This is the part that was derived here rather than transcribed, so it is the part that most needed
checking against the equation.

| alpha | nu | predicted damping `nu |k|^(2 alpha)` | measured rate | predicted rate | absolute error |
|---|---|---|---|---|---|
| 0.25 | 1e-5 | 0.00006 | 1.99976 | 1.99994 | 1.8e-04 |
| 0.25 | 1e-4 | 0.00063 | 1.99915 | 1.99937 | 2.2e-04 |
| 0.50 | 1e-5 | 0.00040 | 1.99942 | 1.99960 | 1.8e-04 |
| 0.50 | 1e-4 | 0.00400 | 1.99578 | 1.99600 | 2.2e-04 |
| 1.00 | 1e-5 | 0.01600 | 1.98382 | 1.98400 | 1.8e-04 |
| 1.00 | 1e-4 | 0.16000 | 1.83974 | 1.84000 | 2.6e-04 |

The largest case shifts the rate by 0.16 and the prediction tracks it to 2.6e-04 absolute. The
derived form `-nu (lambda |zeta|)^(2 alpha)` is correct in the full nonlinear equation across two
decades of viscosity and a fourfold range of dissipation order.

## Negative controls: all three discriminate, after a fix

Three deliberately corrupted models must fail the P1 criterion. At the first attempt they were run at
`phi = pi/2`, where `zeta_1 = sin(phi) = 1`, so dropping the `zeta_1` factor changes nothing and that
control reported the same error as the correct model. **The control was vacuous and the run did not
discriminate.** It was rerun at `phi = pi/4`, where `zeta_1 = 0.7071`:

| corrupted model | predicted | measured | rel err | verdict |
|---|---|---|---|---|
| correct | 1.41421 | 1.41427 | 4e-05 | tracks |
| drop the `zeta_1` factor | 2.00000 | 1.41427 | 0.310 | fails, as required |
| drop the inverse-norm scaling | 8.89921 | 1.41427 | 0.845 | fails, as required |
| flip the sign | 0.00000 | 1.41427 | enormous | fails, as required |

Recording the first attempt because it is the recurring lesson: a control evaluated at a degenerate
parameter cannot tell a right model from a wrong one, and it passes silently.

## Verdict

**CONFIRMED.** The reduced modulation system predicts the full nonlinear Boussinesq equations to
sub-percent accuracy in the regime it claims, its band structure is present, its frequency
independence holds across an eightfold range, and the dissipative extension derived in this problem
is quantitatively correct. The reduction is an instrument, not a picture, and statements built on it
are licensed within the stated regime.

Boundary of validity, stated so it is not exceeded later: scale separation `lambda / lam0 >= 20`,
small amplitudes (`Theta0 = 1e-6`), single layer, short horizon before nonlinear feedback matters.
Nothing here licenses a claim about many interacting layers, which is EXP-003's subject and is not
covered by this control.
