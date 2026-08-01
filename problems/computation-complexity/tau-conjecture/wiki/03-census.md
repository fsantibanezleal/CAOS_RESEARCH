# 03: The census: $z_{\max}(\tau)$, exactly

Transcribed 2026-08-01 from EXP-001/002/003 verdicts. The census is the
program's spine (approaches evaluation, route A6): decide the bottom of
the conjecture's ladder exactly, and extract the extremal mechanisms.

## Definitions

Model: constant-free SLPs, inputs $\{-1, 1, x\}$ (equivalent to free
constants $-1, 0, 1$), gates $+, -, \times$, length = gate count.
$$z_{\max}(\tau) := \max\{\, z(f) : f \ne 0,\ \tau(f) \le \tau \,\},$$
$z(f)$ = distinct integer roots. The conjecture says $z_{\max}(\tau) \le
(1+\tau)^\kappa$; it fails for $\kappa < 1$, so the census watches whether
the measured growth stays near-linear.

## The table (all values decision-complete, exact arithmetic)

| $\tau$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $z_{\max}$ | 1 | 2 | 3 | 3 | 4 | 5 |
| reached-set states | 9 | 98 | 1,462 | 29,506 | 778,087 | not stored (last-gate scan) |
| new polynomials | 9 | 34 | 177 | 1,249 | 11,377 | 134,494 |

Milestones: minimal $\tau$ for 3 distinct integer roots = 3 ($x^3 - x$);
for 4 roots = 5 (EXP-002); for 5 roots = 6 (EXP-003:
$\mp x(x^2-1)(x^2-4)$, the depth-5 DOS record times the input $x$, which
adjoins the root 0 for one gate). Records track $z = \tau - 1$ from
$\tau = 3$ on; whether that law continues at depth 7 is the standing
question (blocked on canonicalization: the depth-6 frontier is not
stored).

## Method and its anchor

BFS over reached-set states (the future of a program depends only on the
SET of computed values), normalized (no duplicate values, no computed 0,
no computed copy of an input; each reduction proved WLOG for optimal
programs). The enumerator's integer restriction reproduces Markstroem's
published census (arXiv:1306.3091v4, Figure 1) exactly, depths 1-7: 14 of
14 anchor values. The LAST-GATE LEMMA (EXP-003) buys one depth past any
exhausted frontier without storing the next frontier: every $\tau = d+1$
polynomial is one gate over a depth-$d$ state.

## Record gallery (mechanisms)

- $\tau = 3$: the four sign/scale variants of $x^3 - x = x(x-1)(x+1)$:
  consecutive triples centered at 0.
- $\tau = 4$: shifted triples ($-x(x+1)(x+2)$: translation of the root
  block costs exactly one gate) and multiplicity-padded quartics.
- $\tau = 5$: ten records, all difference-of-squares splittings on the
  Chebyshev-conjugate map $C(x) = x^2 - 2$:
  $x^2 - C(x)^2 = -(x-1)(x+1)(x-2)(x+2)$,
  $1 - ((x+1)^2 + x)^2 = -x(x+1)(x+2)(x+3)$,
  $((x-1)^2 - x)^2 - 1 = x(x-1)(x-2)(x-3)$ and variants: root sets
  $\{\pm1, \pm2\}$ and four consecutive integers.
- All depth-5 records have 2-adic valuation spectrum $\{0, 1\}$ on
  nonzero roots: at the bottom of the ladder, roots pile into few
  valuation classes (the pressure sits on Rojas' digit-conjecture side,
  not the valuation-spectrum side).

## The tower obstruction (why the depth-5 mechanism saturates)

The records' inner map $C(x) = x^2-2$ is the doubling map; iterating it is
exactly the factory that makes the REAL analogue of the conjecture false
($C^k(x) - x$ has $2^k$ real roots at $\tau \le 2k+2$). Over $\mathbb{Z}$
it produces almost nothing: $C^k(x) - x$ has exactly 2 integer roots for
every $k$ (the fixed points $2, -1$; integer orbits with $|x| \ge 3$
escape), and the difference-of-squares tower
$G_k = C^{k-1}(x)^2 - C^k(x)^2$ stalls at the root set
$\{0, \pm 1, \pm 2\}$ (5 roots) for every $k \ge 2$, because the integer
preimage tree of $C$ stabilizes. Proofs: context note
`2026-08-01-chebyshev-tower-derivation.md`; machine checks in
`code/tclib/test_tclib.py`.

## Reading the data (two-sided, honest)

Growth $1, 2, 3, 3, 4, \dots$ tracks $z \approx \tau - 1$: fully
consistent with the linear-rate world in which the conjecture (even with
$\kappa = 1$) lives comfortably. No finite census can decide the
conjecture; what it can do is kill or exhibit MECHANISMS. So far every
mechanism found (shifted blocks, DOS splittings, towers) is provably
linear-rate or saturating; the geometric-progression family remains the
best known factory, and it is linear.
