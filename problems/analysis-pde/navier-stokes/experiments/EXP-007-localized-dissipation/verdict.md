# EXP-007 verdict: CONFIRMED, localization costs the dissipative reduction `3.6 alpha / (ell lambda)`

Date: 2026-09-17. Hypothesis committed first at [`hypothesis.md`](hypothesis.md). Runner
[`code/run_exp007.py`](../../code/run_exp007.py). Raw: [`result.json`](result.json). Hardware: RTX
4070 Laptop, float64, N = 4096, no time stepping.

> **Reproduction.** The exact settings are the `args` block of the result file, and
> `code/reproduce_all.py` rebuilds the command line from it. The command is
>
> ```
> python run_exp007.py --alpha 0.5 --mask-level 0.5 --n 4096
> ```

**Verdict: CONFIRMED, all three gates.** The dissipative reduction survives localization, and the
error it costs is now a measured formula rather than an assumption.

## The question

Our dissipative modulation system rests on the fractional Laplacian being diagonal on a plane wave.
The construction's layers are localized, with envelope radius `ell_q = lambda_{q-1}^(-3)`, and a
localized wave is a band of frequencies rather than one. Localization is exactly the object our
cascade model does not carry (NS-016), so the size of that error was unrecorded.

## Result

| gate | prediction | measured |
|---|---|---|
| H1, first order in the bandwidth ratio | slope `-1` in `log(ell lambda)` | **-0.9863** |
| H2, coefficient bounded over `alpha` in [0.05, 1] | order one | 0.180 to 3.606, and exactly linear in `alpha` |
| H3, control at `ell lambda ~ 1` | order one error | **1.90** |

**The error depends on the bandwidth ratio alone.** Cases that share `ell lambda` but split it
differently between frequency and envelope agree to four digits: `ell lambda = 102.4` gives
1.7182e-02, 1.7179e-02 and 1.7179e-02 at `lambda` = 64, 128 and 256. That is the structural claim, not
just a fitted slope.

**The coefficient is linear in the dissipation exponent**, which the hypothesis did not predict and the
measurement shows exactly: 0.180, 0.361, 0.901, 1.803, 3.606 at `alpha` = 0.05, 0.1, 0.25, 0.5, 1.0,
that is `3.606 alpha` to three digits. That is what the symbol expansion gives, since differentiating
`|xi|^(2 alpha)` brings down `2 alpha`, with the remaining factor `1.80` a shape constant of this
envelope. So

$$\boxed{\ \frac{\lVert(-\Delta)^{\alpha}(g\,e^{i\lambda\zeta\cdot x}) - (\lambda|\zeta|)^{2\alpha}g\,e^{i\lambda\zeta\cdot x}\rVert}{\lVert(\lambda|\zeta|)^{2\alpha}g\rVert}\ \approx\ \frac{3.6\,\alpha}{\ell\lambda}\ }$$

## What it means for the construction

At Alpoge-Buckmaster's own scales, `ell_q^(-1) = lambda_{q-1}^3` and `lambda_q = lambda_{q-1}^(Q_q)`
with `Q_q >= 201`, so `ell_q lambda_q = lambda_{q-1}^(Q_q - 3)` and the relative error is
`3.6 alpha lambda_{q-1}^(3 - Q_q)`: below any power this problem tracks. **Localization does not
obstruct the dissipative reduction at the separations the construction uses**, and it cannot be what
sets a hypodissipative threshold. The constraint that binds stays the one already on the record,
`alpha < delta / (4 Q)` (wiki page 8).

This also says what a hypodissipative construction must not do: shrink the separation between the
envelope and the wave. At `ell lambda` of order ten the damping law is already wrong by tens of
percent, and at order one it is wrong by 190 percent, which the control measures directly.

## Scope

- It is the DAMPING TERM that is checked here, not the whole force budget. The inviscid residual of a
  localized ansatz, the object Alpoge-Buckmaster's Sections 5 to 7 estimate and correct, is untouched
  by this experiment and remains the open half of NS-016.
- One envelope shape, a compactly supported C-infinity bump. The `1.80` is its shape constant; the
  `2 alpha` is not.
- Measured where the envelope exceeds half its maximum. In the tails both sides are near zero and
  their ratio is noise, which is how a measurement of nothing gets reported as a large error.
