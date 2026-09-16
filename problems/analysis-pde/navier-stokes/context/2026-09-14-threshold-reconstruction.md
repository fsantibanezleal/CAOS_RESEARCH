# Where the published threshold (22 - 8 sqrt 7)/9 comes from

Date: 2026-09-14. Source, read in the primary: D. Cordoba, L. Martinez-Zoroa, F. Zheng, *Finite time
blow-up for the hypodissipative Navier Stokes equations with a force in L1_t C^{1,eps}_x and
L^inf_t L^2_x*, Arch. Ration. Mech. Anal. 250 (2026) article 38,
[doi:10.1007/s00205-026-02198-0](https://doi.org/10.1007/s00205-026-02198-0),
[arXiv:2407.06776v2](https://arxiv.org/abs/2407.06776), archived in [`../references/`](../references/).
Sections read: 1.2.1 to 1.2.4, all of Section 4 including the force estimates 4.3.1 to 4.3.5 and the
proof of Theorem 1 in 4.4.

Code and tests: [`../code/nslib/cmz_budget.py`](../code/nslib/cmz_budget.py),
[`../code/tests/test_cmz_budget.py`](../code/tests/test_cmz_budget.py) (30 numeric tests), and the
exact-arithmetic repository test `tests/test_navier_stokes_threshold.py` (sympy, runs in CI).

The construction and every constant are the authors'. What this dossier adds is an explicit account of
which of their constraints sets the constant, derived from their own exponents with no fitted
coefficients, and a correction to our round-1 reading of it.

Convention throughout: THEIR dissipation `|grad|^alpha`, so classical viscosity is their `alpha = 2`.

## 1. The construction's parameters, as exponents

The vorticity is an infinite sum of vortex layers `omega_n`, each much more concentrated than the last.
Everything is a power of a large base `N`, raised to `R^n`:

| quantity | form | meaning |
|---|---|---|
| frequency of layer n | `M_n = N^(R^n)` | super-geometric: `M_{n+1} = M_n^R` |
| amplitude | `A_n = N^(a R^n)` | the stretching felt by layer n is `A_{n-1} = N^((a/R) R^n)` |
| localization | `L_n = N^(b R^n)` | support size of layer n |
| force margin | `s` | Holder exponent headroom of the force, must be `> 0` |

Section 4 fixes (transcribed, and each re-checked symbolically, see Section 5 below):

$$R = \sqrt{\frac{2}{7\alpha}}, \qquad a = \sqrt{\frac{2\alpha}{7}}, \qquad
s = \frac{3\alpha + 2 - 2\sqrt{14\alpha}}{4}, \qquad b = 1 + \alpha - s - 2\sqrt{\frac{2\alpha}{7}}.$$

The paper notes that `8 sqrt 7 = sqrt 448 > sqrt 441 = 21`, so `alpha_0 < 1/9`, and that `R > sqrt 2`
and `s > 0` on the admissible range.

## 2. The four exponent constraints

Reading Section 4.3, each force contribution must be summable over `n` in `L^1_t C^r_x` with `r < s`.
At the level of exponents (with `delta -> 0` and logarithmic factors dropped) that gives:

| label | source | constraint |
|---|---|---|
| **D** dissipation | 4.3.5, and the equality choice in 1.2.4 | `a = alpha R` |
| **S** self-interaction | 4.3.2: `(N^(2 sqrt(2alpha/7) - alpha + r - 1) L)^(R^n)` | `2a - a/R + b + s - 1 <= 0` |
| **L** localization | 4.3.3: needs `L > A N^(1/R + s)` | `b >= a + 1/R + s` |
| **O** outer velocity on inner layer | 4.3.4: `N^(8 sqrt(2alpha/7) + r + 1) L^(-3)` | `a + 2/R + s + 1 - 3b <= 0` |

For **O**, the paper's `8 sqrt(2 alpha/7)` is `a + 2/R` at their parameters, because
`1/R = (7/2) a`; the general form is what enters the derivation.

## 3. The derivation

Saturate **D** and **S**. **S** then fixes `b = 1 + a/R - 2a - s = 1 + alpha - 2 alpha R - s`.
Substituting into **O**:

$$4s < 2 + 3\alpha - 7\alpha R - \frac{2}{R}.$$

The right-hand side is maximized over the frequency ratio where `7 alpha = 2/R^2`, that is

$$\alpha R^2 = \frac{2}{7}, \qquad R = \sqrt{\frac{2}{7\alpha}},$$

**which is exactly the value the paper chooses**. At that optimum `7 alpha R + 2/R = 2 sqrt(14 alpha)`, so

$$s(\alpha) = \frac{2 + 3\alpha - 2\sqrt{14\alpha}}{4},$$

the paper's formula, and `s(alpha) > 0` is equivalent to `9 alpha^2 - 44 alpha + 4 > 0`, whose smaller
root is `(44 - sqrt 1792)/18 = (44 - 16 sqrt 7)/18`:

$$\boxed{\;\alpha_0 = \frac{22 - 8\sqrt 7}{9} = 0.0926655\ldots\;}$$

No coefficient in this chain was fitted. Each comes from a displayed exponent in Section 4.3.

## 4. Which constraint does NOT bind, and why the heuristic overshoots

At the published point the localization constraint **L** holds with a margin

$$b - \Big(a + \frac1R + s\Big) = \frac{1}{2}\Big(\sqrt{\frac{2\alpha}{7}} - \alpha\Big),$$

positive for `alpha < 2/7`, and equal to `0.0350` at `alpha_0`. The paper records the same fact in its
own words ("after substituting s and rearranging, this is equivalent to `sqrt(2 alpha/7) > alpha`").

The heuristic of Section 1.2.4 keeps **D**, **S** and **L** and does not contain **O**. Saturating
**L** instead of **O**:

$$2s \le 1 + \alpha - 3\alpha R - \frac1R, \qquad \alpha R^2 = \frac13,
\qquad s(\alpha) = \frac{1+\alpha}{2} - \sqrt{3\alpha}, \qquad \alpha < 5 - 2\sqrt6 = 0.10102\ldots$$

which is exactly the paper's back-of-envelope formula; we derive it here as an optimum rather than
take it as stated.

**So the whole gap between the heuristic threshold `0.1010` and the proved threshold `0.0927` is a
swap of the binding constraint.** The heuristic's binder, localization, is slack in the proof. The
proof's binder, the action of the outer layers' velocity on the inner layer (4.3.4), is absent from
the heuristic. The paper itself flags the heuristic as "only a back-of-the-envelope calculation: in
reality there are other sources of error"; this identifies which source it is, and shows that it is
the only one that moves the constant.

## 4b. A consequence: the admissible frequency ratios, and why geometric cascades are excluded

The same budget is a quadratic in `R`. A positive margin needs `7 alpha R^2 - (2 + 3 alpha) R + 2 < 0`,
so the admissible ratios form an interval whose endpoints are

    R_pm = [ (2 + 3 alpha) +/- sqrt(9 alpha^2 - 44 alpha + 4) ] / (14 alpha),

and the discriminant is EXACTLY the polynomial whose root is `alpha_0`. Three consequences, all
checked (`feasible_R_interval`, `geometric_cascade_margin`, and the exact sympy pair in
`tests/test_navier_stokes_threshold.py`):

1. The interval closes to a single point precisely at `alpha_0`, and that point is the paper's own
   `R = sqrt(2/(7 alpha))`. Above `alpha_0` it is empty, which is the theorem's boundary seen from a
   different direction.
2. `R_- > 1` for every `alpha > 0`, approaching 1 only as `alpha -> 0`: at `alpha = 0.001` the
   interval is `(1.002, 285.1)`, at `alpha = 0.05` it is `(1.143, 5.000)`.
3. At `R = 1`, the geometric cascade, the margin is exactly `-alpha`. Independently of the optimum,
   `R = 1` forces `b >= a + 1 + s` (localization) against `b <= 1 - a - s` (self-interaction), hence
   `alpha + s <= 0`.

So super-geometric frequency growth is not a convenience of the construction, it is forced, and the
amount forced rises with the dissipation. Our own cascade model uses a geometric schedule, which is
why it can carry the dissipation constraint but not a force budget: item NS-016.

## 5. Verification

- Exact (sympy), in CI: `tests/test_navier_stokes_threshold.py`. Derives the **O** budget from **D**
  and **S**, finds the optimum `alpha R^2 = 2/7`, recovers `s(alpha)` and `(22 - 8 sqrt 7)/9`; derives
  the **L** budget and recovers `1/3`, `(1+alpha)/2 - sqrt(3 alpha)` and `5 - 2 sqrt 6`; proves the
  localization slack closed form and its positivity at `alpha_0`.
- Numeric, problem suite: `code/tests/test_cmz_budget.py`. At five values of alpha, the paper's `R` is
  the strict maximizer of the **O** budget; at the published point **D**, **S**, **O** bind and **L**
  holds.
- The paper's own statements used as independent checks of the transcription: the `L` exponent equals
  `(2+alpha)/4 + (3/2) sqrt(2 alpha/7)` as printed; its check `L > A N^(1/R+s)` reduces to
  `sqrt(2 alpha/7) > alpha` as printed; its 4.3.4 exponent `2 sqrt(14 alpha) - 2 - 3 alpha + r + 3s`
  follows from the substitution as printed.

## 6. What this corrects in our round-1 record

EXP-003 inverted our cascade relation `alpha_c = 1/(4p)` at the published threshold and obtained
`p = 11/4 + sqrt 7`, then argued the calibration was not empty for two reasons. **Both are withdrawn.**

1. *"The relation came from constraints not tuned to hit a number."* The relation is the dissipation
   constraint **D** saturated, which is the paper's constraint 1 of Section 1.2.4. The construction
   saturates it at **every** alpha, so along the whole published family
   `ln M_n = (1/alpha) ln A_{n-1}`, i.e. `2p = 1/alpha` identically. The identity holds at `alpha_0`
   because it holds everywhere, and it carries no information about where `alpha_0` sits.
2. *"The p it assigns is a clean algebraic number."* That is automatic arithmetic. `alpha_0` lies in
   `Q(sqrt 7)`, the inverse of any element of `Q(sqrt 7)` lies in `Q(sqrt 7)`, and the inverse is
   especially tidy here only because the norm of `22 - 8 sqrt 7` is `36`, a perfect square.

The honest state after this round: our frequency cap reproduces the construction's dissipation
constraint (a consistency check that does hold), but the published threshold is set by **O**, a
force-regularity constraint that our reduced cascade model does not contain. The genuine account of the
constant is Section 3 above, not the round-1 calibration.

## 7. What remains honest caveats

- This is exponent bookkeeping: `delta -> 0`, logarithms dropped, constants in the `<~` ignored. It
  reproduces the paper's stated choices exactly, which is strong evidence the transcription is right,
  but it is not a re-proof of the theorem.
- The authors plainly know which estimate binds; they chose `R` and `s` accordingly. The contribution
  here is making the optimization and the heuristic-versus-proof binding swap explicit and checkable,
  not discovering the constant.
- The same accounting applied to the smooth-forcing upgrade (the unreleased Alpoge-Buckmaster
  hypodissipative paper) would show whether smooth forcing moves the binding constraint. That is the
  natural question for NS-010 when that paper appears.
