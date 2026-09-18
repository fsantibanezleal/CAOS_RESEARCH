# EXP-007 hypothesis: does localization break the dissipative reduction?

Committed 2026-09-17, before any code for this experiment has run.

## The gap this closes

Our dissipative modulation system (page 4 of the wiki) rests on one step: the fractional Laplacian is
diagonal on a plane wave, so `(-Laplacian)^alpha sin(lambda zeta . x) = (lambda |zeta|)^(2 alpha)
sin(lambda zeta . x)` exactly, and dissipation enters each amplitude equation as a single damping
term. EXP-002 confirmed the resulting system against the PDE.

**But the construction does not use plane waves.** Every layer is LOCALIZED: Alpoge-Buckmaster give it
an envelope of radius `ell_q = lambda_{q-1}^(-3)` (their (3.7)), and localization is exactly what our
cascade model does not represent (NS-016: "our model has plane waves, whose envelope is trivial, so
there is no `b` exponent to carry"). A localized wave is a band of frequencies, not one frequency, and
`(-Laplacian)^alpha` is not constant across a band. The residual is a force the construction would
have to absorb, and nothing in our record says how big it is.

## The prediction

For a symbol `|xi|^(2 alpha)` and a wave of frequency `lambda` modulated by an envelope of bandwidth
`ell^(-1)`, the standard symbol expansion gives

    (-Laplacian)^alpha [g(x) e^(i lambda zeta . x)]
        = (lambda |zeta|)^(2 alpha) g(x) e^(i lambda zeta . x) + E,

with the first correction carrying one derivative of the envelope:

    |E| / |(lambda |zeta|)^(2 alpha) g|  ~  C(alpha) / (ell lambda).

**H1. The relative error is first order in the bandwidth ratio.** Measured over a grid of `lambda` and
`ell`, `log(relative error)` against `log(ell lambda)` has slope `-1` to within 0.1.

**H2. The coefficient is bounded across the hypodissipative range.** `C(alpha)` stays of order one for
`alpha` in `[0.05, 1]`, so no exponent in the range that matters carries a hidden blow-up of the
correction.

**H3, the discriminating control.** With an envelope as wide as the wave itself, `ell lambda ~ 1`, the
relative error must be of order one. If it is small there too, the measurement is not sensitive to
localization at all and H1 proves nothing.

**H4, the consequence for the construction.** At their own scales, `ell_q^(-1) = lambda_{q-1}^3` and
`lambda_q = lambda_{q-1}^(Q_q)` with `Q_q >= 201`, so `ell_q lambda_q = lambda_{q-1}^(Q_q - 3)` and the
relative error is `lambda_{q-1}^(3 - Q_q)`: smaller than any power we track. PASS means the
dissipative reduction survives localization at the separations the construction uses, and the
constraint that binds stays the one we already have, `alpha < delta / (4 Q)`.

## Method

No time stepping is needed, which is why this is cheap. Build `g(x) sin(lambda zeta . x)` on the
torus with a smooth compactly supported envelope of radius `ell`, apply `(-Laplacian)^alpha`
spectrally in float64, and compare against `(lambda |zeta|)^(2 alpha) g(x) sin(lambda zeta . x)`
pointwise, measuring the relative error where the envelope is above half its maximum (so the
comparison is not dominated by the tails, where both sides are near zero and the ratio is noise).

Guards, from what has already bitten this problem: the wave plus its envelope bandwidth must fit
under the 2/3 dealiasing limit (EXP-005 part D), and the error must be measured where the envelope is
supported rather than everywhere (EXP-002's vacuous control).

## What each outcome means

A PASS closes the localization half of NS-016's question for the dissipative term specifically: the
envelope costs a relative error that vanishes like the inverse bandwidth ratio, so it cannot be what
sets a hypodissipative threshold. A FAIL, meaning an error that does not shrink like `1/(ell lambda)`,
would mean the dissipative extension we derived and EXP-002 confirmed does not survive the
localization the real construction needs, which would put a caveat on every dissipative statement in
this problem, including the NS-017 prediction.
