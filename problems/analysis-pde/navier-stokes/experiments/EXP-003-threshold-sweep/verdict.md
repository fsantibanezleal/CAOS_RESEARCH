# EXP-003 verdict: CONFIRMED, and the headline claim is downgraded to a consistency relation

Date: 2026-09-12. Runner: `code/run_exp003.py`. Raw output: `result.json`. Hardware: RTX 4070 Laptop,
float64, 1,000,000 schedules evaluated in 1.46 s using 537 MB of VRAM.

## Question

Does the cascade model, with the time budget and the hold-interval damping put back in, predict the
published dissipation threshold of Cordoba, Martinez-Zoroa and Zheng?

Three hypotheses were committed in the runner docstring before the run.

## H1, the threshold formula: CONFIRMED

The model gives `alpha_c(p) = 1/(4p)` in the `(-Laplacian)^alpha` convention, with `p` the frequency
growth exponent in `lambda_q ~ A_q^p`. A numerical bisection cannot measure that directly, because a
supercritical schedule does not stall immediately: the growth rate stays positive until stage
`q* = log(1/nu) / (g (2 alpha p - 1/2))`, so a run truncated at `Q` stages reports a threshold too
high by `1 + 2 log(1/nu) / (g (Q-1))`.

Measured against that horizon-corrected prediction over `p` in [1.5, 12]:

| quantity | value |
|---|---|
| max relative error vs corrected prediction | 2.59e-06 |
| median relative error | 2.59e-06 |

And the gap to the asymptotic `1/(4p)` halves exactly as the horizon doubles, which is the predicted
`1/Q` scaling:

| stages | max gap to `1/(4p)` | ratio |
|---|---|---|
| 400 | 0.009618 | |
| 800 | 0.004803 | 2.00 |
| 1600 | 0.002400 | 2.00 |

An off-by-one was found and fixed here rather than shipped. The bound was first written with `Q`, the
number of stages, when the binding stage is the last one inspected, `Q-1`. With `Q` the
million-schedule ensemble showed 47 apparent violations and H1 carried a residual error of 2.56e-04;
with `Q-1` there are zero violations and the residual drops to 2.59e-06, a hundredfold improvement.
The tightest closing schedule in the ensemble sits 2.7e-06 below the bound, which is as sharp a
confirmation as this arithmetic admits.

## H2, which constraint binds: CONFIRMED, and it is a negative result

The whole point of the repair was that the first-pass estimate omitted the time budget and the
hold-interval damping, and both omissions were expected to push the threshold DOWN. They do not.

- **C3, the time budget, is not binding at all.** Stage times decay geometrically because
  `sigma_q ~ sqrt(A_q)` grows, so the total time converges for any positive `g`. The finite-time
  requirement costs nothing in exponent.
- **C4, layer survival under hold damping, gives the same exponent as C2.** Across 2,304 schedules on
  a `(p, alpha)` grid, the number where C4 fails while C2 still holds is **zero**. The reason is
  structural: the remaining time `R_q` shrinks like `1/sqrt(A_q)`, which is exactly the rate at which
  the growth rate rises, so `nu lambda_q^(2 alpha) R_q` and the growth condition read the same
  inequality `alpha p < 1/4`.

So dissipation acting during the holds does not rest, but it also does not bite harder. The
first-pass estimate's two known omissions turn out not to move the threshold. That is worth recording
precisely because it was expected to.

## H3, the calibration: CONFIRMED exactly, and it is weaker than it looks

Inverting `alpha_c = 1/(4p)` at the published threshold `alpha_0 = (22 - 8 sqrt 7)/9`:

    p = 1 / (2 alpha_0) = 9 / (2 (22 - 8 sqrt 7)) = 9 (22 + 8 sqrt 7) / 72
      = (22 + 8 sqrt 7) / 8 = 11/4 + sqrt 7 = 5.395751311064591

Agreement to 6.2e-15, that is to floating point. The algebra is exact, not numerical.

**What this is not.** It is not a derivation of the published threshold. Any threshold corresponds to
some `p`, so the relation on its own cannot be wrong. Two things keep it from being empty. First,
`alpha_c = 1/(4p)` was derived from two independent constraints that were not tuned to hit any
number, and the second of them was expected to give a different exponent and did not. Second, the `p`
it assigns is the clean algebraic number `11/4 + sqrt 7` rather than an arbitrary decimal, which is
what one expects if the published optimization is solving a quadratic naturally posed in the
frequency exponent.

**The claim is therefore stated as a consistency relation, not a result**: the published threshold is
exactly the statement that the frequency must grow like the `(11/4 + sqrt 7)` power of the background
gradient. Deriving `p = 11/4 + sqrt 7` from the construction's own localization and correction
requirements is the open target, and it is what would turn this into a theorem about the model.

## Ensemble: CONFIRMED

1,000,000 random schedules over `p` in [1.5, 12], `alpha` in [0.002, 0.302], `g` in [0.5, 2.0],
`nu` in [1e-14, 1e-4]. 174,600 close. Violations of the horizon-detectable bound: **0**. Wall time
1.46 s, peak VRAM 537 MB after chunking (the unchunked first attempt peaked at 7,936 MB, at the
card's limit).

## Verdict

**CONFIRMED** on all four checks. The threshold formula, the finite-horizon correction, the
non-bindingness of both repaired omissions, and the exact calibration all hold. The scientific
content is deliberately modest and is stated as such: a consistency relation between our reduced
bookkeeping and a published theorem, with the derivation of `p` left open.

Validity boundary: this is a statement about the exponent bookkeeping of an idealized geometric
schedule, not about Navier-Stokes and not about the full construction, whose localization envelopes,
higher-order corrections and steering geometry are absent from the model. EXP-002 licenses the
single-layer reduction against the PDE; nothing here has been checked against a genuine multi-layer
PDE simulation, and that gap is the first item of any continuation.
