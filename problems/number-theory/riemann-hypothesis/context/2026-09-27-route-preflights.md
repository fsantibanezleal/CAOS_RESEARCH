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

## RH-035: the route below `theta=1/2` is closed

Below `theta=1/2` every detector the program uses is unavailable: the
localized Selberg density `k_q=(theta-1/2)/(4eC_q)` is negative, and the
localized Levinson range `nu<theta-1/2` is empty. The only odd-order input is
Karatsuba's theorem (`H=T^(27/82+eps)`, Math. USSR-Izv. 24 (1985), main
theorem p. 524, read in the 2026-09-12 dossier), whose density `a_eps` is
positive but not explicit.

Wang's pair term `c(theta)` holds for every `0<theta<1`, so the EXP-006
product still applies. The odd-support density it needs is `1-2/A(theta)`,
`A=2-c(theta)` (scratch values):

| `theta` | `c(theta)` | needed `k` (EXP-006 product) | needed `k` (RH-034 linear candidate, if proved) |
|---|---|---|---|
| 0.3303 | -1.1377 | 0.3626 | 0.3792 |
| 0.40 | -0.6330 | 0.2404 | 0.2110 |
| 0.45 | -0.3717 | 0.1567 | 0.1239 |
| 0.48 | -0.2427 | 0.1082 | 0.0809 |
| 0.50 | -0.1660 | 0.0766 | 0.0553 |

The best explicit Selberg-method proportion is Pearce-Crump's global 7%
(arXiv:2609.15329v1, read in full for EXP-008); localized constants are
smaller, and Karatsuba's are not explicit. An odd-order critical density of
8% to 36% in intervals shorter than `T^(1/2)` is far beyond any located
method. The 2026-09-27 report's crude conversion
`simple>=(c-(Q-1)/6)N` gives the same order (17% to 19%) and is superseded
here by the product, which is the program's sharp finite inequality.

Decision: RH-035 is closed as `research-record`. Reopen only if an explicit
odd-order critical proportion above the tabulated threshold appears for some
`theta<1/2`.

## RH-032: Cohn-Elkies kernels are outside the unconditional framework

Lamzouri's Proposition 2.1 (arXiv:2609.02882v2, read in full) needs
`K=(eta^2)^` with `eta` real, even, in `L^2`, and `supp eta` in
`(-lambda,lambda)`. The zero sum enters only as `Q=sum K(z-s)^2=||F||^2`,
a Hilbert-space norm (EXP-006 proof, eq. (3)), and it is evaluated through
BGSTB Lemma 5, which needs a test function supported in `[-1,1]`. The
positivity used is that of a norm, not a sign of the pair-correlation
function `F(alpha)`.

A Cohn-Elkies relaxation uses test functions `r>=0` whose Fourier transform
is not compactly supported and is nonpositive outside the support, and it
drops the tail using `F(alpha)>=0` there. Unconditionally two facts block it:

1. Off-line zeros make `z-s` complex, `F` has no sign, and Lamzouri shows no
   nonconstant entire kernel has `Re K>=0` on all of `C`; this is exactly why
   his proof avoids pointwise positivity.
2. No unconditional asymptotic exists for the pair sum with test functions of
   unbounded Fourier support; that is Montgomery's conjecture.

The admissible class `eta^2*eta^2` is contained in the Montgomery-Taylor class
`g*g~`, and its optimum is the Montgomery-Taylor constant, which is why the
2026 unconditional constants coincide with the RH bandlimited ones. Under RH
the Cohn-Elkies improvement is prior art (Chirre-Goncalves-de Laat 0.6792).

Decision: RH-032 is closed with the obstruction recorded; focus `RH-F5` is
closed. Reopen only with a Hilbert-space (norm-type) representation of a
sign-constrained tail.

## RH-027: reduction of the Tang-type target

Target A asks for the EXP-010 moment (A),

$$
\int w(t)\,|V\psi(\sigma_0+it)|^2\,dt=c(P,Q,R,\nu)\,\widehat w(0)+O(H/L),
$$

for `nu` beyond `theta-1/2`. Expanding `|psi|^2` reduces it to twisted
moments `int w(t)(h/k)^(it) zeta(sigma_0+alpha+it)zeta(sigma_0+beta-it) dt`
with `(h,k)=1`, `h,k<=y=T^nu`, and shifts `|alpha|,|beta|<<1/L`, summed with
weights `mu(h)mu(k)P[h]P[k]/sqrt(hk)` (derivatives of `Q` come from the
shifts).

What Tang supplies (arXiv:2608.14852v1, Theorem 1, read in full): for distinct
odd primes `p,q`, no shifts, a Gaussian window of width `H=T^delta`, the
twisted moment equals the diagonal main term, plus a dual moment
`sum_{chi mod p} chi(q) int G_{T,H}(1/2+it)(...)|L(1/2+it,chi)|^2 dt` over an
effective `t`-range of length `T/H`, plus `O((T/H)(pqT)^eps((p/q)^(1/2)+(q/p)^(1/2)))`.

What target A needs beyond Tang:

1. General coprime `h,k` in place of primes (Khan's global formula already
   covers general coprime twists; the short-window version must be redone).
2. Shifts `alpha,beta`, uniformly in `|alpha|,|beta|<<1/L`.
3. The summed dual moments, with weights `a_h a_k/sqrt(hk)`, shown to be
   `o(H)`, or evaluated if they carry a main term.

Heuristic ranges [I]:

- Error term alone: with mollifier weights the summed Tang error is
  `(T/H)M^(1+eps)`, so `nu<2theta-1`.
- Dual moments bounded trivially: per pair about `sqrt(h)(T/H)log T`
  (orthogonality over characters mod `h` on a range of length `T/H`), summed
  to `(T/H)M^(3/2)`, so `nu<(2/3)(2theta-1)` (target A'). A large-sieve
  saving in the sum over moduli, using the character sums
  `sum_k a_k chi(k)/sqrt(k)`, is what would push this toward `2theta-1`.

Value (RH-031 machinery, scratch):

| Range | Onset | `h_L(0.534)` |
|---|---|---|
| `theta-1/2` (proved, EXP-010) | 0.53396 | 0.00006 |
| `(2/3)(2theta-1)` (target A', trivial dual bound) | 0.53067 | 0.00558 |
| `2theta-1` (target A) | 0.52571 | 0.0166 |

Decision. Target A' is the next analytic declaration candidate: it is the
smallest statement with a clear value (onset about `0.5307`, density at `0.534`
about 90 times EXP-010's), and every ingredient is a known technique
(Khan-Tang reciprocity, shifts, trivial large sieve). It is not declared
today: EXP-011 is declared only with a written proof plan whose steps are
referenced to Tang's and Khan's lemmas, per methodology 02 and 12. Target B
(Steuding-type) stays behind it: it needs an Atkinson-Motohashi evaluation of
the off-diagonal uniform in shifts and in general `Q`, a much larger project.

## RH-036: bounded replay of Zhu's window infimum

Script: [`rh036_weil_window_upper.py`](2026-09-27-preflights/rh036_weil_window_upper.py).
It evaluates Zhu's geometric-side Weil form (arXiv:2608.24827v2, eqs. (2)-(3)
and the exact time-domain archimedean term of Lemma 2.5, read in full) on the
span of the first `N` even Legendre modes of `L^2[-0.8,0.8]`: the pole term
`2F(i/2)^2`, the archimedean integral, and the prime powers `n=2,3,4` (the only
ones with `log n<1.6`). The autocorrelations are exact rational polynomials;
the transcendental parts are evaluated with mpmath at 80 digits. The minimum
eigenvalue is a variational upper bound for `lambda*(0.8)`. This is a
multiprecision replay, not an interval certificate, and it replays only the
upper-bound half; the lower-bound certificate (200 Legendre modes, a
frequency cutoff `T=200`) is not replayed.

| `N` even modes | `lambda_min` | second eigenvalue |
|---|---|---|
| 8 | `3.24e-11` | `4.08e-7` |
| 14 | `2.87e-15` | `3.23e-10` |
| 20 | `2.047e-17` | `1.03e-11` |
| 24 | `1.746e-17` | `9.59e-12` |

Zhu's certified window is `8.9e-18<=lambda*(0.8)<=2.27e-17`. The `N=20` and
`N=24` values lie inside it, still decreasing toward the certified floor, and slightly below his upper bound, consistent with his remark
that the sine basis behind that upper bound loses a little through the
boundary condition `f(+-L)=0`. The spectral gap to the second eigenvalue
(about six orders) is consistent with his simple, even ground state.

Landau-Widom question. The replay confirms the scale of the window's lower
spectral edge but gives no map from window positivity to a zero-proportion
functional: the program's detectors use pair-correlation sums with support
`lambda<theta`, not Weil positivity on a window. No barrier statement for
Gram-type detectors follows.

Decision: RH-036 is closed as `research-record` (independent upper-bound
replay consistent with Zhu; no proportion channel).

## RH-034: a linear Hilbert-parity inequality beyond the EXP-006 product

Scripts: [`rh034_linear_inequality_search.py`](2026-09-27-preflights/rh034_linear_inequality_search.py),
[`rh034_stress.py`](2026-09-27-preflights/rh034_stress.py),
[`rh034_window_control.py`](2026-09-27-preflights/rh034_window_control.py).

Where the product loses. EXP-006 proves `(Q-S)(N-O)>=2(N-S)^2` from Lamzouri's
arbitrary-parameter inequality `Q>=2tN-(2t-1)S-t^2 d` (one linear inequality
per `t`, EXP-006 proof eq. (5)) and the parity bound `2d<=N-O`. The product is
the envelope of that family. With `S=0` and `k=O/N` it gives
`Q/N>=2/(1-k)`, tight only for a single double or triple point. For separated
real clusters without simple points the true minimum is the chord
`Q/N>=2+3k` (doubles and triples), strictly larger for `0<k<1/3`. The loss is
the Cauchy-Schwarz step `sum alpha_j^2>=(sum alpha_j)^2/d` over the first
Gram-Schmidt range.

Candidate. For every conjugation-invariant finite multiset,

$$
Q\ge2N+3O-4S. \tag{L}
$$

It is tight for single points of multiplicity one, two and three, for widely
spaced simple points, and for doubles and triples at real zeros of `K`. It is
strictly stronger than every member of Lamzouri's family for `0<k<1/3`, so it
cannot follow from EXP-006's inputs alone.

Tests (floating point):

1. Exhaustive small types (up to three real points of multiplicity 1-3 and
   two conjugate pairs), `cos^2` window: minimum slack `0` (reached only in
   degenerate limits where off-line pairs collapse onto the line).
2. Random stress, 601 trials over `cos^2`, `tent^2` and truncated Gaussian
   windows, up to four real clusters of multiplicity 1-4 and three pairs of
   multiplicity 1-2: minimum slack `0` to machine precision.
3. Random stress, 201 trials with the Montgomery-Taylor window used by
   Lamzouri (`eta^2` proportional to `cos(sqrt2 u)` on `(-1/2,1/2)`): minimum
   slack `0` to machine precision.
4. Local analysis and control. For a real triple and a conjugate pair near a
   real zero `x0` of `K`, `Q-13=4pi^2 y^2(8mu2-12|int u eta^2 e^(-2pi i x0 u)|^2)+O(y^3)`,
   so (L) fails for small `y` exactly when the ratio
   `|int u eta^2 e^(-2pi i x0 u)|^2/mu2` exceeds `2/3`. Montgomery-Taylor
   window: ratios `0.252, 0.058, 0.025` at the first three zeros, slack
   positive. Edge-concentrated control window (`eta^2` proportional to `u^8`):
   ratios `0.969, 0.826`, and (L) fails with `Q-13=-0.246`. The tests
   therefore detect violations when they exist.

Conclusion. (L) is false for general admissible windows and survives every
test for the Montgomery-Taylor window. Any proof must use window-specific
information, at least the local condition above, beyond Lamzouri's argument.

Value (scratch; `s>=(2+3k-A)/4` with `A=2-c(theta)`):

| Mollifier range | Onset with the product | Onset with (L) | density at 0.534 with (L) |
|---|---|---|---|
| `theta-1/2` (proved) | 0.53396 | 0.52964 | 0.0058 (product: 0.00006) |
| `(2/3)(2theta-1)` (target A') | 0.53067 | 0.52617 | 0.0119 |
| `2theta-1` (target A) | 0.52571 | 0.52124 | 0.0241 |

Decision. (L) for the Montgomery-Taylor window, and for the smooth
approximants `eta_eps` of Lamzouri's kernel-construction lemma, is the second declaration
candidate beside RH-027 target A'. It is a finite statement, so a proof or a
counterexample is decisive. The first bounded action is a proof attempt that
refines the first Gram-Schmidt range per cluster; the local ratio condition
shows which property of the window the proof must use.
