# The Euler smooth-forcing construction: its growth class and its force budget

Date: 2026-09-18. Closes NS-019. Code `nslib/ab_euler_budget.py`, tests
`code/tests/test_ab_euler_budget.py` (7). Primary source: Alpoge-Buckmaster, *Blowup for the Euler
equations with smooth forcing*, Sections 2, 3, 5, 6 and 12 (pages 2 to 10, 15 to 27, 95 to 104), read
in the archived PDF `references/ab-euler.pdf` (sha256 `97ef408b...`).

Convention: `alpha` is OURS, `(-Laplacian)^alpha`; the proved rough-force threshold is `0.0463`.

## 1. The growth class, settled

The UNVERIFIED item of `2026-09-17-force-estimates-exponent-content.md` Section 5 is settled from the
source. In volume coordinates `y = (z, r^2/2)` the circulation `Gamma = r u^phi` plays the role of the
Boussinesq temperature, and the principal amplitude law (3.4) is

    d/dt (T, Omega^) = B (T, Omega^),   B = [[0, -d/(sigma kappa)], [sigma c zeta_1, 0]],

with `d = (J zeta) . grad Gamma_<` the background circulation gradient and `c = 2 W Gamma_<`, of
order one by (2.12). The growing eigenvalue is the square root of the product of the off-diagonal
entries, so it scales like `sqrt(|grad Gamma|)`: **the pendulum law, `gamma = 1/2`, in the blowup
variable `grad Gamma` of (1.3)**. Section 12 confirms it on the chosen sequence: the growth scale is
`sigma_i ~ N_i^(beta/2)` (p. 97) against a deposited gradient `N_i Y_i = N_i^beta`.

Consequence: the class ceiling of Theorem 3.1 that applies to this construction, and to any
dissipative version that keeps its swirl mechanism, is `alpha <= 1/4` (ours), `1/2` in `|grad|^alpha`,
not the `1/2` (ours) of vortex stretching.

## 2. The exponent content

Section 12 writes the force exponents explicitly, which the Boussinesq paper does not. With margin
`beta` (amplitude `N^(-(1-beta))`), `h = 1 - beta`, `Pi <= N^v`, `v = p/Q`, per-level parameter
`delta = Pi^d N^(-h)`, `h* = h - d v`, `J = 2k + 8`, `u >= k v`, their (12.15) reads

| contribution | exponent of `N_m` | their target |
|---|---|---|
| activation | `1 - e + 2u + v` | below `-6`, set by the seed exponent `e` |
| terminal remainders | `-(2h* - 1) k + beta - 9 h* + 2u + v` | below `-6` |
| phase means | `-2 h + 3u + 6v` | below `-3/2` |

with side conditions: the coefficient quotients (12.13), thirteen rows of the form
`Pi^(A - B d) N^(-n beta) <= 1`; the decay rows (12.7), among them `a - 5 beta/2 > 0` for the
localization `ell = N_{i-1}^(-a)` and the centre row `2 h* - beta/2 > 0`; `Pi >= ell^-1`, so `p >= a`;
and the derivative range `9k + 51 <= Q` (p. 101). Their constants (12.1)-(12.2) are `beta = 1/8`,
`d = 16`, `p = 8`, `q = 10`, `a = 4`, `e = 8`, `c_Q >= 2^18`, `q_0 >= 2^20`, `Q_i = q_0 + i`.

**Transcription check.** Their constants pass their own targets: activation `-7.00`, terminal
`-10.75`, means `-1.75`, `h* = 0.875 > 13/16`, every quotient row and the derivative range.

## 3. Dissipation

A layer grows only while `nu N_i^(2 alpha) < sigma_{i-1} sin s_i` with
`sigma_{i-1} ~ N_{i-1}^(beta/2)` and `N_i = N_{i-1}^Q`, so `alpha < beta / (4Q)` at an insertion
angle of order one: Theorem 3.1 with `p = Q/beta`, `gamma = 1/2`.

| reading | best `alpha` (ours) | theirs | below 0.0463 | at `k = 1` |
|---|---|---|---|---|
| as published (`Q >= 2^20 + 1`, and `Q_i` unbounded) | `2.98e-08` at the first stage, 0 asymptotically | `5.96e-08` | about `10^6` | |
| every free choice released (`tau -> 0`, least `d`, `Q >= 9k + 51`, `a > 5 beta/2`) | `3.64e-03` (k=0, Q=51, `beta = 0.742`) | `7.27e-03` | 12.7 | `3.12e-03` (Q=60) |
| localization at the previous wavelength (`a = 1`) | `3.77e-03` (k=0, Q=51) | `7.53e-03` | 12.3 | `3.22e-03` |

In the relaxed readings the binding constraint is the (12.7) centre row `2 h* > beta/2`, with the
least per-level power `d = 2` permitted by the quotient rows `Pi^(2-d)`. The ratio floor
`Q >= 9k + 51` is again the derivative range, the Euler counterpart of the Boussinesq `9d + 42`.

## 4. What it establishes

- **Both published smooth-forcing designs are pendulum-class**, so neither can be carried, by any
  retuning, past the class ceiling `1/4` (ours); and their own force estimates, with every free choice
  released, certify at most `2.2e-03` (Boussinesq) and `3.8e-03` (Euler), more than ten times below
  the threshold already proved with a rough force.
- **A sharper dated prediction for NS-010.** Alpoge and Buckmaster report a hypodissipative
  Navier-Stokes result built, per their Boussinesq paper's AI statement, after the Euler one. If it
  keeps the swirl (pendulum) mechanism and this estimate architecture, its exponent should not exceed
  about `7.5e-03` in the `|grad|^alpha` convention; a larger exponent means they changed the
  architecture, specifically the derivative range that forces `Q >= 9k + 51` or the centre-row
  structure, or the growth law. It cannot exceed `1/2` in that convention while the mechanism is a
  pendulum.

## 5. Scope and caveats

- As for the Boussinesq budget, these bound what the design's ESTIMATES certify, not the existence of
  solutions; constants and logarithms are not tracked; the favourable insertion angle is assumed.
- The damping of a localized swirl layer is taken to be `nu (N |zeta|)^(2 alpha)`, the leading
  symbol. EXP-002 verified that law against the nonlinear equations for Boussinesq, not for
  axisymmetric swirl; for a three-dimensional fractional Laplacian acting on `u^phi e_phi` the leading
  symbol is the same, but the lower-order geometric terms were not measured.
- The reading "every free choice released" keeps every structural inequality the paper's proof
  uses; it is not a claim that some other proof could not do better.
