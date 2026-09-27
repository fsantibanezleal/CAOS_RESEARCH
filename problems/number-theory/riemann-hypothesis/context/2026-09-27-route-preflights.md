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
