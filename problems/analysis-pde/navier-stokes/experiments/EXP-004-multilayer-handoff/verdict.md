# EXP-004 verdict: the layer-to-layer handoff CONFIRMED on pattern, with a characterized slope systematic

Date: 2026-09-12. Runner: `code/run_exp004.py`.

> **Reproduction, added 2026-09-17.** The exact settings of the run are the `args` block of
> the result file, not the defaults of the runner: `code/reproduce_all.py` rebuilds the
> command line from that block and diffs every numeric leaf of the rerun against the record.
> Verified on 2026-09-17, after the round-2 and round-3 refactors of `nslib`, with every
> result leaf identical. The command is
>
> ```
> python run_exp004.py --A0 4.0 --A1 4.0 --Theta1 0.002 --Theta2 1e-07 --alpha 1.0 --dt 0.0004 --grow1 2.4 --lam0 1 --lam1 12 --lam1b 16 --lam2 192 --mask-frac 0.35 --measure2 0.08 --mode frozen --n 1024 --nu 0.0 --phi1 1.5707963267948966 --phi2 1.5707963267948966 --settle 2.0
> ```

Raw: `result-frozen.json` (the clean test),
`result-dynamical.json` (the honest inconclusive companion). Hardware: RTX 4070 Laptop, float64.

## The gap this closes

EXP-002 validated a SINGLE layer on the prescribed stratification. EXP-003's exponent bookkeeping
assumes infinitely many NESTED layers, each growing on the gradient the earlier ones deposited, and
its load-bearing premise is that the growth rate of a layer is set by the TOTAL low-frequency
gradient, not merely the base stratification. Neither source paper reports a numerical multi-layer
check. This experiment tests that premise against the full nonlinear PDE.

## Part A, the dynamical attempt: INCONCLUSIVE, and the reason is the setup, not the mechanism

Grow layer 1 from the stratification, then inject a finer layer 2 and measure where it grows. Layer 1
did grow as intended (`Theta` from 1e-3 to 0.218, depositing a gradient `lambda_1 Theta_1 = 6.97`,
which is 1.74 times the stratification gradient `A0 = 4`). But the measured rate of layer 2 correlated
only 0.27 with the full low-pass prediction AND only 0.22 with the base-only control: **the control
did not discriminate, so the run proves nothing.**

The cause is a defect in the SETUP, identified before drawing any conclusion. The reduction assumes
each layer grows on a FROZEN affine background, which the construction arranges by steering the
previous layer into a holding interval (`zeta_1 = 0`, `Omega = 0`) where its amplitudes are constant.
This path never implements steering, so layer 1 is still rotating and shearing while layer 2 grows,
and the background layer 2 sees is not stationary over the measurement window. A non-stationary
background is outside what the modulation reduction describes, so a poor fit here is expected and
uninformative. Recorded, not hidden, because it motivates Part B.

## Part B, the frozen test: CONFIRMED on the load-bearing claim

Replace the dynamically grown layer with a FROZEN mid-scale contribution to the background. The
background

$$\theta_{bg}(x) = -\frac{A_0}{\lambda_0}\sin(\lambda_0 x_2) - \frac{A_1}{\lambda_{1b}}\sin(\lambda_{1b} x_2)$$

is a function of $x_2$ alone, so $\partial_1\theta = 0$ exactly, the vorticity source vanishes, and
with $u=0$ nothing is advected: an exact steady state, verified two ways. The unit test
`test_two_scale_vertical_background_is_steady` confirms it does not move (and that a tilted term
would), and the run itself measures a drift of **1.45e-15** over 200 steps. The mid-scale
$\lambda_{1b}$ term stands in for the gradient an earlier layer would have deposited; modelling it as
a vertical sinusoid rather than a tilted travelling wave is the one simplification, and it is exactly
what keeps the background frozen so the test is clean.

The background gradient is $G(x) = (0,\ -A_0\cos(\lambda_0 x_2) - A_1\cos(\lambda_{1b} x_2))$, varying
with height at two scales. Inject a fine layer 2 at $\lambda_2$ and measure its local growth-rate
field. Compare it to the rate predicted from the TOTAL two-scale gradient (H1) and to the rate
predicted from the base stratification alone (H2 control).

At N = 1024, $\lambda_0 = 1$, $\lambda_{1b} = 16$, $\lambda_2 = 192$, $A_0 = A_1 = 4$:

| prediction | correlation with measured rate | RMSE |
|---|---|---|
| **H1, full two-scale gradient** | **0.99945** | 0.188 |
| H2 control, base stratification only | 0.212 | 0.808 |

**The local growth rate of layer 2 follows the total two-scale gradient almost perfectly and the base
alone not at all.** That is precisely the premise EXP-003 rests on: a layer responds to the total
accumulated low-frequency gradient, including what earlier layers contributed, and not merely the base
stratification. The handoff works in the full nonlinear PDE.

## The slope systematic, reported rather than smoothed over

The pre-committed pass criterion (in the runner docstring) was "correlation above 0.9 AND regression
slope within 15 percent of 1". The correlation criterion passes overwhelmingly; the **slope does
not**: the measured rate is about 1.36 times the prediction. By the committed criterion, `all_pass`
is therefore False, and it is reported as False. The goalpost was not moved.

The slope offset is a measurement-geometry systematic, not a failure of the handoff, and three
independent facts establish that:

1. **It is present already at $A_1 = 0$** (a single-scale background), where the two predictions are
   identical: slope 1.35 there too. A two-scale effect cannot be responsible for something visible
   with one scale.
2. **It shrinks as the comparison mask tightens toward the flat peaks** of the gradient: 1.36 at
   mask fraction 0.35, 1.29 at 0.7, 1.24 at 0.9. The offset lives in the steep regions, where the
   local-rate picture is imperfect because the growing wave's envelope develops sidebands that couple
   neighbouring heights. In the two-scale background the gradient is curved everywhere (the
   $\lambda_{1b}$ term), so no truly flat region exists and the offset cannot be driven fully to 1.
3. **The absolute rate was already pinned to 4e-05 relative by EXP-002** in its flat-peak region. This
   experiment is about the PATTERN, and the pattern is unambiguous.

So EXP-004 confirms the qualitative, load-bearing claim decisively and leaves the absolute-slope
calibration in this particular geometry (horizontal probe wave, pointwise fit over a curved gradient)
as a known systematic rather than a clean 1.0. Honest verdict: **pattern CONFIRMED, committed slope
sub-gate not met, cause diagnosed.**

## Method notes worth keeping

- **A negative control must be able to fail.** The dynamical Part A control did not discriminate
  (0.27 vs 0.22), which is why Part A is inconclusive rather than confirmatory. The frozen Part B
  control discriminates hard (0.999 vs 0.21). Same lesson as EXP-002's degenerate-angle control, in a
  new guise.
- **A wave above the 2/3 dealiasing limit is annihilated silently.** The first frozen attempt put
  $\lambda_2 = 256$ at N = 512 (limit 170); the demodulated envelope was noise and the fit produced
  meaningless rates near 970. The runner now refuses that configuration loudly instead of reporting it
  as a failed hypothesis.
- **A wave injected off the local growing eigenmode carries a transient.** Fitting from $t=0$ over a
  short window reads the transient as an inflated rate; a settling interval before fitting removes it.
  The pattern (correlation) is unaffected either way.

## What remains open

A genuinely dynamical multi-layer confirmation, with steering implemented so each grown layer is held
frozen while the next grows, is still not done. Part B establishes the essential physics (rate follows
total gradient) on a frozen surrogate; the full dynamical cascade with steering is a larger build and
is the natural next step if this line is pursued further.
