# Smoothness of the force and fractional dissipation pull against each other

Date: 2026-09-16. Backlog item NS-017, opened by NS-016. Code `nslib/ab_schedule.py` with 13 tests in
`code/tests/test_ab_schedule.py`.

Convention: `alpha` is OURS, `(-Laplacian)^alpha`, so classical viscosity is 1 and the published
hypodissipative threshold of Cordoba-Martinez-Zoroa-Zheng is `0.0463`.

**This dossier contains a prediction about work that has not been released.** It is written so that it
can be checked and, if wrong, seen to be wrong: the criterion is in Section 5.

> **Correction, 2026-09-17.** The rule `120 k <= Q` used below is a sufficient simplification
> in the published design, not a structural exchange rate. Transcribing the full force budget
> ([`2026-09-17-force-estimates-exponent-content.md`](2026-09-17-force-estimates-exponent-content.md)) shows that
> the ratio floor the estimates actually force is `Q >= 9d + 42`, from the derivative range of the
> coefficient bounds, and that the margin is capped near `1/2` by the remainder and near `1/4` by the
> leading phase means at the published target. The bound `1/480` below therefore holds for the
> design as published, but not for every retuning: at one derivative the most favourable reading of
> the architecture reaches `3.69e-03` (ours). The conclusion, that the design stays at least ten
> times below the proved threshold, is unchanged and now rests on the full budget. The text below is
> kept as written.

## 1. The question

Alpoge and Buckmaster prove blowup for 2D Boussinesq with a **smooth** force, inviscid. Cordoba,
Martinez-Zoroa and Zheng prove hypodissipative blowup with a **rough** force, `C^{1,eps}`. Alpoge and
Buckmaster state that they also have a hypodissipative result, not yet posted. What does our
dissipative extension of their own modulation system say about their published schedule, if
dissipation is switched on and nothing else is changed?

## 2. Their schedule, transcribed

From their Subsection 3.3, equations (3.7), (3.8) and (3.10), read in the primary source:

| object | value | where |
|---|---|---|
| frequency ratio | `lambda_q = lambda_{q-1}^(Q_q)`, `Q_q = Q* + q`, `Q* >= 200` | (3.7) |
| derivative order | `k_q = max{k : 120 k <= Q_q, ...}` | (3.8) |
| seed and gain | `Theta_seed = -lambda_q^(-k_q - 6)`, `L_q = (k_q + 5 + beta) log lambda_q`, `beta = 1/8` | (3.8) |
| the exact consequence they state | `|Theta_seed| e^(L_q) = lambda_q^(-7/8)` | (3.8) |
| insertion angle | `s_q = L_q sigma_{q-2} / sigma_{q-1}`, `Gamma_q = sigma_{q-1} sin s_q` | (3.10) |

Two facts follow immediately, and neither is a new claim about their work:

- A layer stops at temperature amplitude `lambda_q^(-7/8)`, so by the amplification identity
  `grad vartheta(0) = lambda Theta zeta` it deposits a gradient `A_{q+1} = lambda_q^(1/8)`. The
  exponent `1/8` is the **amplitude margin** `delta`.
- `120 k_q <= Q_q` ties the smoothness of the force to the frequency ratio: **each further derivative
  of the force costs another 120 in the ratio**, and a `C^infinity` force needs `k_q -> infinity`,
  which is why `Q_q = Q* + q` grows with the stage.

## 3. What dissipation would require

Our dissipative modulation system (derived in `modulation.py`, confirmed against the PDE by EXP-002 to
2.6e-04 absolute) damps a layer at `nu (lambda |zeta|)^(2 alpha)` while it grows at
`sqrt(A) sin(phi)`. Applying that to their stage `q`, whose background gradient is
`A_q = lambda_{q-1}^delta` and whose frequency is `lambda_q = lambda_{q-1}^(Q_q)`:

    growth needs   nu lambda_q^(2 alpha) < sqrt(A_q) sin s_q

which in exponents of `log lambda_{q-1}` is

    2 alpha Q_q < delta / 2 + (exponent of sin s_q).

With an insertion angle of order one, the most favourable case, this is

    alpha < delta / (4 Q_q) = 1 / (32 Q_q),

and with their own angle (3.10), which is itself a negative power of the frequency, a further factor
`Q_{q-1}` tighter:

    alpha < delta / (4 Q_q Q_{q-1}).

In our cascade notation this is nothing new: `lambda_q = A_q^p` with `p = Q_q / delta`, and the bound
is our own C2, `alpha p < 1/4`.

## 4. The consequence, and the numbers

**`Q_q = Q* + q` is unbounded, so no positive `alpha` satisfies the condition at every stage.** A
cascade with this schedule and any fixed dissipation runs a finite number of stages and stops, and a
finite cascade produces a finite gradient, not blowup.

| quantity | value with the published constants |
|---|---|
| largest `alpha` the FIRST stage can carry, favourable angle | `1.55e-04` |
| the same with their own insertion angle | `7.70e-07` |
| stages before stalling at `alpha = 1e-04` | 113 |
| frequency ratio compatible with `alpha = 0.0463` (the published threshold) | `0.675`, that is, less than 1 |
| derivatives of the force affordable there, by `120 k <= Q` | `0.006`, that is, none |

The last row is the structural statement in its sharpest form: **at the dissipation exponent where
hypodissipative blowup is already proved with a rough force, this schedule cannot control even one
derivative.**

The general trade-off is one line, `alpha < delta / (4 Q)`. Our own cap of `1/4` from EXP-003 is the
corner `delta -> 1`, `Q -> 1`; the published smooth-forcing design sits at `delta = 1/8`, `Q >= 200`,
seven orders of magnitude away, and both budgets were spent on the smoothness of the force.

## 4b. The converse bound: what one derivative costs

Read the same two relations the other way. Their rule is `120 k <= Q`, and the dissipation constraint
is `alpha < delta / (4 Q)`, so controlling `k` derivatives of the force costs

    alpha < delta / (480 k),

and even with the most generous amplitude margin the amplification identity allows, `delta -> 1`,

    k = 1  =>  alpha < 1/480 = 0.00208.

That is **22 times below the threshold already proved for a `C^{1,eps}` force** by
Cordoba-Martinez-Zoroa-Zheng (0.0463 in our convention), and 178 times below it at their own margin
`delta = 1/8`.

So the obstruction is not the published constants. `Q* >= 200` and `delta = 1/8` are design choices
that could be retuned; the exchange rate of 120 units of frequency ratio per derivative is what keeps
this correction scheme out of the regime that is already proved. A hypodissipative version has to
change the rate, which means changing the correction hierarchy itself, not the constants around it.

## 5. The prediction, and how it fails

**Prediction.** A hypodissipative version of the Alpoge-Buckmaster mechanism must do at least one of:

1. **bound the frequency ratio** `Q` (so `Q_q` does not grow with `q`), which by `120 k <= Q` bounds
   the derivatives controlled and therefore gives a force of FINITE regularity, not `C^infinity`;
2. **raise the amplitude margin** `delta` toward 1, that is, stop each layer much closer to
   `lambda^(-1)` than `lambda^(-7/8)`;
3. **change the growth mechanism**, for instance to vortex layers whose rate is the background
   gradient itself rather than its square root, which is what Cordoba-Martinez-Zoroa-Zheng use and is
   why their budget reads `a = alpha R` rather than our `alpha p < 1/4`.

and their threshold should scale like `delta / (4 Q)` with whatever pair they end up using.

**Falsification.** The prediction is wrong if their hypodissipative paper reaches a positive threshold
while keeping a stage-dependent, unbounded `Q_q`, an amplitude margin near `1/8`, and the same
square-root growth law. It is also wrong, in a more interesting way, if their dissipative analysis
does not damp a layer at `nu lambda^(2 alpha)`, which is the one piece of this that is ours rather
than theirs, and is the piece EXP-002 tested.

**Status: UNVERIFIED, and dated.** Recorded 2026-09-16. NS-010 in the backlog is the item that checks
it.

**Checks that the paper had not yet appeared**, so that the date on this prediction means something:

| checked | where | result |
|---|---|---|
| 2026-09-17 | arXiv listing for math.AP, and a search for the authors with the topic | no hypodissipative paper by these authors is posted |

Each further check goes in this table, and the day one of them finds the paper, the prediction is
settled here either way before anything else is written.

## 6. Caveats, plainly

- This is exponent bookkeeping applied stage by stage, in the same spirit as our EXP-003, not a proof
  that their construction fails under dissipation. Constants, logarithms and the correction hierarchy
  are ignored, and any of them could move a factor, though none of them can turn an unbounded `Q_q`
  into a bounded one.
- The dissipative damping term is ours. It follows from their own modulation system by adding
  `-nu(-Laplacian)^alpha` and using that the fractional Laplacian is diagonal on the phase, and it was
  checked against the nonlinear PDE, but they may treat dissipation differently.
- Their schedule is designed for an inviscid theorem. Nothing here says the design is bad; it says
  what it costs in a setting it was not built for.
