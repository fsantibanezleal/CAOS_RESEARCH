# EXP-011: a barrier for linear refinements of the Hilbert-parity product

Declared: 2026-09-28. Device: CPU. Baseline: branch `task/riemann-strategy-review`
after commit `ded5825`.

Status at declaration: the route preflights
([`context/2026-09-27-route-preflights.md`](../../context/2026-09-27-route-preflights.md),
section RH-034) found, in floating point, a counterexample to the linear
candidate `Q>=2N+3O-4S` for the Montgomery-Taylor window and periodic
configurations with `(Q-2N)/O` near 2.33. The configurations are frozen in
[`frozen-parameters.json`](frozen-parameters.json). No EXP-011 runner, audit,
or canonical artifact exists. This declaration is committed and pushed before
implementation and canonical computation.

## Question

EXP-006 proves `(Q-S)(N-O)>=2(N-S)^2` for every conjugation-invariant finite
multiset, with `Q=sum K(z-s)^2`, `K=(eta^2)^`. At `S=0` it reads
`Q/N>=2/(1-k)`, `k=O/N`, which is tight only for single points. A linear
refinement `Q>=2N+beta O-gamma S` with `beta>2` would lower the EXP-010 onset.
For the Montgomery-Taylor window used by Lamzouri, how large can `beta` be, and
what is the most such a refinement could give for the onset?

## Frozen definitions

`K(xi)=[sin((b-c)a)/(b-c)+sin((b+c)a)/(b+c)]/(2sin(ab)/b)`, `a=1/2`, `b=sqrt2`,
`c=2pi xi`, so `K(0)=1` and `K=(eta^2)^` with `eta^2` proportional to
`cos(sqrt2 u)` on `(-1/2,1/2)`. For a multiset with real points `x` of
multiplicity `m_x` and simple conjugate pairs `z, conj(z)`: `N` counts copies,
`S` simple real points, `O` distinct odd-multiplicity real points, and
`Q=sum_{z,s} m_z m_s K(z-s)^2`.

C1 and C2 are the configurations in the frozen file. For C2 (a finite lattice
of `2M+1` cells), translation invariance gives exactly
`Q=sum_{a,b in cell} m_a m_b sum_{|d|<=2M} (2M+1-|d|) K(x_a-x_b+ds)^2`.

## Predictions

A. Arb ball arithmetic certifies `Q(C1)-(2N+3O-4S)<-0.05` (`N=20`, `O=6`,
`S=0`). Hence `Q>=2N+3O-4S` is false for this window.

B. Arb certifies `(Q(C2)-2N)/O<2.365` (`O=10001`, `N=110011`, `S=0`). Hence no
inequality `Q>=2N+beta O-gamma S` with `beta>=2.365` (any `gamma`) holds for
this window.

C. With the EXP-010 detector (`nu=theta-1/2-10^(-4)`, certified `kappa>0.717 nu`
is not assumed; the onset uses the certified frozen constants of EXP-010 through
the same monotone relation), a valid refinement with `beta<2.365` gives
positivity only where `beta kappa>2-c(theta)-2`. Directed interval arithmetic
certifies that at `theta=0.5320` the needed `beta` exceeds 2.365, using the
EXP-010 value `kappa(0.0319)` recomputed by the EXP-010 exact routine. So no
linear refinement of this kind can move the onset below 0.5320.

D (control). The EXP-006 product holds on C1 and C2 with positive certified
slack, and the translation-invariant formula agrees with the direct double sum
on C2 truncated to `M=50`.

## What PASS and FAIL prove

PASS of A and B is a certified counterexample result for one fixed window. It
proves that the route "linear refinement of the product" is capped at an onset
of 0.5320 for this window (C), and it closes RH-034 as a theorem target. It
does not bound other windows, nonlinear refinements, or multi-point inputs
(RH-034's moment-LP form), and it changes no zero-counting theorem.

FAIL of A would mean the floating-point counterexample is an artifact; FAIL of
B would only weaken the cap. Either is recorded as `inconclusive` for that
prediction, with the frozen file unchanged.

## Transfer to smooth windows

Lamzouri uses smooth `eta_eps` in `C_c^inf((-1/2,1/2))` approaching the
Montgomery-Taylor optimum. C1 is a finite configuration with margin `0.05` on
differences of size at most about 6.1 and imaginary part at most 0.5, where
`K_eps->K` uniformly; the counterexample therefore persists for `eta_eps` close
enough to the limit. This is recorded as a remark, not certified.

## Compute budget and stop rules

CPU only, python-flint Arb at 128 bits, runner capped at 900 seconds. An
unresolved enclosure or a missed threshold gives `inconclusive` for that
prediction. The frozen file, configurations and thresholds do not change after
this declaration.
