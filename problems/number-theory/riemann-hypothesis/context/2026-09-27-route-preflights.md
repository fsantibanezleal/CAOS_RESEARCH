# Route preflights after the 2026-09-27 strategic review

Date: 2026-09-27. Status: exploratory preflights under methodology 12 for the
routes ordered in the [plan](../../../../program/riemann-hypothesis/plan.md).
Every number below is a floating-point scratch value unless stated otherwise.
None is a certificate, and none changes a verdict. A route that produces a
claimable statement gets its own `EXP-NNN` declaration, certified runner,
audit and verdict. Scripts are in [`2026-09-27-preflights/`](2026-09-27-preflights/).

## RH-031: value of information for RH-027

Script: [`rh031_value_of_information.py`](2026-09-27-preflights/rh031_value_of_information.py).
It optimizes the Conrey constant `c(P,Q,R,nu)` over `R`, the optimal
sinh-type `P` for fixed `Q`, and the EXP-010 Chebyshev family for `Q`
(degree `2K+1`, `K` about `3/nu`, at most 150), then feeds `kappa` into the
EXP-006 root `h_L(theta)` with Wang's `c(theta)`, exactly as EXP-010 does.

Invariants (all reproduced):

| Check | Reference | Scratch value |
|---|---|---|
| EXP-010 range `nu=theta-1/2`, onset of the `0.7173 nu` curve | EXP-010 hypothesis: about `0.53399` | `0.53396` |
| Steuding-type range `nu=(3theta-1)/4`, `Q=1-x`, `P=x` | Steuding's simpler choice: `0.591` | `0.59034` |
| Same range, linear `Q=1-ay` with free `a`, `P=x` | Steuding's stronger choice: `0.552` | `0.55235` (`a=1.093`, `R=2.45`) |
| Optimal `kappa/nu` for small `nu` | Euler-Lagrange ceiling `0.7173` (2026-09-26 preflight) | `0.71733` at `nu` in `[0.034,0.10]` |

The linear-`Q` optimum has `beta=Q(0)+Q(1)=0.907`, not 1. Freeing `beta`
in the high-degree family returns `beta=1.000` at `nu=0.034,0.068,0.1`
(`1.0007` at `0.15`) with no gain in `kappa`, so EXP-010's frozen `beta=1`
loses nothing.

Optimized density (scratch; the smallest `nu` needs a degree above the cap):

| `nu` | 0.034 | 0.05 | 0.068 | 0.10 | 0.125 | 0.15 | 0.1875 | 0.25 | 0.375 |
|---|---|---|---|---|---|---|---|---|---|
| `kappa` | 0.02439 | 0.03587 | 0.04878 | 0.07174 | 0.08969 | 0.10769 | 0.13488 | 0.18103 | 0.27512 |
| `kappa/nu` | 0.71733 | 0.71733 | 0.71733 | 0.71736 | 0.71749 | 0.71790 | 0.71936 | 0.72411 | 0.73364 |

Onset of `h_L>0` by admissible range:

| Range for `nu` | Onset | `h_L(0.51)` | `h_L(0.52)` | `h_L(0.534)` | `h_L(0.55)` |
|---|---|---|---|---|---|
| `theta-1/2` (EXP-010, proved) | 0.53396 | negative | negative | 0.00006 | 0.0238 |
| `2theta-1` (Tang-type target A) | 0.52571 | negative | negative | 0.0166 | 0.0480 |
| `min{(3theta-1)/4,3/8}` (Steuding-type target B) | below 0.5005 | 0.0238 | 0.0380 | 0.0574 | 0.0787 |

Decision. Both targets are worth proving. Target A would move the onset from
`0.534` to about `0.526` and multiply the density at `0.534` by about 260.
Target B would give positivity for every `theta>1/2` (at `theta=0.505`,
`nu=0.129`, `kappa=0.092`, `h_L=0.0165`). Neither needs a degree of `Q` beyond
what EXP-010 already certifies: at the larger `nu` of target B, `K` near 20
suffices, and the value lies in the analytic range, not in the detector. The
stop condition "no partial extension moves the onset" is not met. RH-027 is
retained with target A first, because Tang's identity already evaluates the
off-diagonal for prime twists without shifts.

## RH-033: Wang's spectral term inside EXP-010

Source read in full: Wang arXiv:2609.24167v1, Proposition 2.1
(`lem:stability`) and Section 5. The added term is
`Delta_K(Z)=tr Psi(G_K)`, where `G_K=(K(x_j-x_l))` runs over the simple real
elements only and `Psi(t)=(t-1)^2` on `[0,2]`, `2t-3` beyond. It is estimated
from below by `a(n-2N/H)`, with `n` the number of simple critical zeros and
`a=2e(H)/3`. The assembly is `(1-a)n>=(2-C)N-2aN/H`, i.e.
`u_H=(C_0-2a_H/H)/(1-a_H)`.

Invariant reproduced: `a_0=4.9418e-7`, `delta_0=6.66625e-8`,
`C_0+delta_0=0.6725007703419` (floating point, matching the paper).

Findings:

1. `Psi` is the stability function of the ainta lineage, which EXP-002 and
   EXP-007 already credit as prior art; Wang's contribution is the three-point
   packing estimate of `tr Psi(G_K)`, which EXP-009 already sharpened
   (`R(alpha,beta)<=sqrt2`). The program therefore already owns the dominant
   version of this term globally.
2. In short intervals the gain is proportional to the simple count `n` and
   carries the penalty `-2aN/H`. At the onset the simple count is zero, so the
   term cannot lower any onset: for Wang's own curve it moves the root of
   `c(theta)` up by about `2a_0/H_0=2.7e-7` unless `H` is sent to infinity,
   where the gain vanishes. The same holds inside the EXP-006 product, whose
   onset is also the zero of the simple-count bound.
3. Away from the onset the relative density gain is of order `a_0`, about
   `5e-7`.

Decision: RH-033 is closed as `research-record`. No experiment is warranted;
the term neither moves the EXP-010 onset nor gives a gain worth a
declaration, and the global version is already dominated by EXP-009.

## RH-028: a second mollifier piece at short-window length

Script: [`rh028_two_piece.py`](2026-09-27-preflights/rh028_two_piece.py).
It evaluates the Bui-Conrey-Young main term `c=c1+2c12+c2`
(arXiv:1002.4127v1, Theorems 3-5; TeX source read in full) for
`psi=psi1+psi2`, where `psi2` is their `chi(s)`-type piece built from the
coefficients of `1/zeta^2` with `P2` vanishing to third order. `c12` and `c2`
are mixed derivatives at `x=y=0` of three- and four-fold integrals, taken by
central differences and Gauss-Legendre quadrature; `c` is quadratic in the
coefficients of `P2`, so the optimal `P2` is a linear solve.

Anchor at the published parameters (`theta1=4/7`, `theta2=1/2`, `R=1.28`):

- `c1` matches the exact EXP-010 routine: `c1=2.135890`, `kappa1=0.40712`.
- The optimal `P2` for the published `P1`, `Q`, `R` reproduces the published
  coefficients to about 2% (`0.02450,-0.00615,0.00585` against
  `0.02454,-0.00636,0.00603`), so the ratio of `c12` to `c2` is right.
- The resulting `kappa=0.40886` is below the published `0.4105`; the published
  value corresponds exactly to a second-piece contribution twice ours
  (`c1-2x0.004737` gives `kappa=0.41061`). Both integrals are stable to
  `1e-6` under refinement. Either the implementation misses a common factor
  two in `c12` and `c2`, or the published evaluation carries one. Both
  normalizations are reported below; the decision does not depend on it.

Short-window lengths (`theta1=nu`, `theta2=nu-1e-9`, RH-031 optimal `Q`, `P1`,
`R`; `P2` in `x^3..x^7`):

| `nu` | `R` | one-piece `kappa` | two-piece `kappa` | relative gain |
|---|---|---|---|---|
| 0.15 | 6.40 | 0.107686 | 0.107686 | `3.5e-10` absolute (about `3e-9` relative) |
| 0.068 | 14.18 | 0.048779 | 0.048779 | below `1e-9` |

At short length the second piece is negligible: `c12` is of order `1e-2`
against `c1` near 300 (the `e^(2R)` scale of the optimal `R`), and `c2` carries
a `1/theta2` weight. The doubled normalization changes nothing visible.

Limitation: this computes the Bui-Conrey-Young second piece, not Feng's
`mu*Lambda^(*k)` pieces. In Feng's main term the `k`-th piece enters with
factors of order `theta^(k-1)` [I, not re-derived here], so its relative gain
should also vanish as `nu->0`.

Decision: RH-028 is closed as `research-record` (gain far below the 1% bar).
Reopen only if a small-`theta` evaluation of Feng's formula shows a gain above
1% of `kappa`.
