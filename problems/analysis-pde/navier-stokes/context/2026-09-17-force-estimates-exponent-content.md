# The exponent content of the smooth-force estimates, and a correction to v0.04

Date: 2026-09-17. Closes the open half of NS-016. Code `nslib/ab_force_budget.py`, tests
`code/tests/test_ab_force_budget.py` (9). Primary source: Alpoge-Buckmaster, *Blowup for the
Boussinesq equations with smooth forcing*, Sections 5 to 8, pages 39 to 69, read in the archived PDF
(`references.md`).

Convention: `alpha` is OURS, `(-Laplacian)^alpha`. Theirs is twice ours. The proved rough-force
threshold is `0.0463` in ours.

## 1. What the estimates are

Theorem 7.3 bounds each layer's complete force pair in `C^k_{x,t}`, `k <= d = k_q`, by
`lambda^(-1/2)`, through (7.26): every contribution is at most a constant times `lambda^(-3/2)`,
and the common majorant `K(d) <= log lambda` absorbs the constants. Everything is a power of
`lambda = lambda_q`, with these inputs, all displayed in the paper:

| object | value | where |
|---|---|---|
| amplitude | `Y <= C_Y lambda^(-7/8)` | Def. 7.1(iii), (7.6) |
| coefficient scale | `Pi <= lambda^(5/Q)`, with `ell^-1 = lambda_{q-1}^3 <= Pi` | (7.4), Thm 8.2 |
| per-level parameter | `delta = Pi^5 lambda^(-7/8) <= lambda^(-7/8 + 25/Q)` | 7.1.1, p. 69 |
| correction levels | `J = 2d + 8`, remainder grades `J+1` to `2J+4` | (3.8), Prop. 6.1 |
| physical evaluation | `(lambda Pi^2)^r` oscillatory, `Pi^(2r)` phase independent | (7.19) |
| derivative range | coefficients needed through `r_* = 9d + 41 <= Q - 1` | (7.15), Thm 5.5 |
| why `Q - 1` | future-stage sums of Lemma 5.4 converge only for orders `n <= Q_q` | Lemma 5.4 proof |
| design rules | `Q >= 201`, `120 d <= Q` (sufficient for the range and for (7.25)) | (7.4) |

The eight contributions, at order `k`:

| contribution | size | note |
|---|---|---|
| activation, scalar and vorticity | `Pi lambda^(-d-6)`, `Pi lambda^(-d-5)`, times `(lambda Pi^2)^k` | the seed `lambda^(-d-6)` is chosen to pay for this |
| leading means `<S_1^theta>`, `<S_2^omega>` | `Pi Y^2`, `Pi^3 Y^2`, times `Pi^(2k)` | quadratic in `Y`, no `lambda^k` |
| higher means | `Y Pi^(2k-2) delta^3`, `lambda Y Pi^(2k-2) delta^4` | grades 3 and 4 onward, by the parity (7.16) |
| remainders | `(lambda Pi^2)^k lambda Y delta^(2d+9)` | first grade `J + 1` |

## 2. What v0.04 got wrong

Theorem 4.1 of v0.04 used one inequality, `J[(1 - delta) - 5/Q] >= k + 6`. Against the table:

1. The target `lambda^(-6)` is the **seed** rule, which bounds the activation contribution. The
   remainder's target is `lambda^(-3/2)`, and the remainder carries a prefactor `lambda Y`.
2. The per-level gain uses `Pi^5`, so the correction is `25/Q`, not `5/Q`.
3. The leading phase means are omitted. They are quadratic in the amplitude and cost only `Pi^2`
   per derivative, and at the published target they are the binding constraint.

The number it produced, `1.08e-03` in the `|grad|^alpha` convention (86 times below the proved
threshold), is therefore not a consequence of the paper's estimates. The direction of the conclusion
survives, as Section 3 shows, but the number and the reason are replaced.

## 3. The corrected budget

With margin `m` (amplitude `lambda^(-(1-m))`, theirs `1/8`), `pi = 5/Q`, target `lambda^(-tau)`,
worst order `k = d`, each constraint is linear in `m`:

    remainder              m <= [d + 9 - 2 d pi - 5 pi (2d + 9) - tau] / (2d + 10)
    leading means          m <= 1 - [pi (2d + 3) + tau] / 2
    higher means (vort.)   m <= [4 - tau - (2d - 2) pi - 20 pi] / 5
    higher means (scalar)  m <= [4 - tau - (2d - 2) pi - 15 pi] / 4
    level gain             m <  1 - 25/Q

and dissipation adds `alpha < m / (4Q)` (Theorem 3.1 with `p = Q/m`, `gamma = 1/2`, favourable
insertion angle).

**Transcription check.** Their own margin `1/8` passes their own constraints at their own ratio rule
for every `d` from 0 to 59, and the leading-means bound at their target is exactly their displayed
(7.25), `Pi^(2d+3) <= lambda^(1/4)`. The budget reproduces the paper before it is used against it.

Three readings, maximizing `alpha` over `d >= 0` and integer `Q` above the floor:

| reading | target | ratio floor | best `alpha` (ours) | theirs | below 0.0463 | at `d = 1` |
|---|---|---|---|---|---|---|
| published choices | `3/2` | `max(201, 120 d)` | `2.65e-04` (d=0, Q=201, leading means) | `5.29e-04` | 175 | `2.34e-04`, 198 |
| every free choice released | `0+` | `9d + 42` | `2.22e-03` (d=0, Q=45, remainder) | `4.44e-03` | 20.8 | `1.83e-03`, 25.4 |
| most favourable structure | `0+` | `9d + 42`, `Pi ~ lambda_{q-1}`, `delta = Pi^3 Y` | `4.48e-03` (d=0, Q=42) | `8.96e-03` | 10.3 | `3.69e-03`, 12.6 |

The third reading takes the localization at the previous wavelength, the least the nesting of Lemma
4.3 could allow, and the per-level parameter at the smallest power of `Pi` the scale table (7.14)
tolerates (`b1` needs `delta >= Pi^5 / lambda`, `b2` needs `delta >= Y Pi^3`). It is not a design
anyone has proposed; it bounds what retuning the constants of this architecture could achieve.

## 4. What it establishes

- **The design's estimates certify no dissipative version above `4.5e-03` (ours) in any reading, and
  none above `2.7e-04` at the published choices.** The gap to the proved rough-force threshold is at
  least a factor 10, and 175 as designed.
- **The exchange rate is the derivative range, not the rule `120 k <= Q`.** What forces the ratio up
  with the regularity is `Q >= 9d + 42`, from the coefficient orders the correction recursion
  consumes and the range over which the future-stage sums converge. The `120` is a convenience.
- **More regularity never helps.** In every reading the exponent is largest at the lowest order and
  falls monotonically, because the margin saturates at `1/2` (two correction levels per derivative)
  while the ratio floor grows linearly.
- **At the published target the binding constraint is the leading phase mean**, a nonoscillatory
  term quadratic in the amplitude. It caps the margin near `1/4` whatever the ratio.

## 5. Scope

- These are statements about what the design's ESTIMATES can certify: the constraints are the
  sufficient conditions its proof uses, not necessary conditions for any construction. A different
  correction scheme is not covered, and Theorem 3.1's class ceiling (`1/4` ours for pendulum growth)
  is the only bound here that is independent of the design.
- The favourable insertion angle is assumed. The published angle `s_q = L_q sigma_{q-2}/sigma_{q-1}`
  is a negative power of the frequency and tightens every row by a further factor.
- **Euler.** The Euler paper (Section 12) uses the same shape: amplitude `N^(-7/8)`, `J = 2k + 8`,
  `Q_i = q_0 + i` with `q_0 >= 220`, and `k <= Q / c_Q` with `c_Q >= 218`. Its growth rate is
  written `sigma_{i-1} sin s_i`, the same form as the Boussinesq `Gamma_q = sigma_{q-1} sin s_q`,
  where Theorem 3.2 fixes `sigma_q^2 = |G_{<q+1}|`, the pendulum law. Whether the Euler `sigma` is
  likewise the square root of the background gradient (as the Boussinesq analogy for axisymmetric
  swirl suggests, which would make `1/4` rather than `1/2` the class ceiling that applies) is
  UNVERIFIED. It belongs to the full extraction of that paper's budget, a separate reading unit
  (112 pages, a different continuation architecture) that is not claimed here.
