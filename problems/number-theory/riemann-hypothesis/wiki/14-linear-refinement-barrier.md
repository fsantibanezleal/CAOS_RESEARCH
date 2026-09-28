# A barrier for linear refinements of the Hilbert-parity product

EXP-011 asks whether the EXP-006 product `(Q-S)(N-O)>=2(N-S)^2` can be
replaced by a linear inequality that is stronger near the onset. For the
Montgomery-Taylor window that Lamzouri's argument uses, the answer is no
beyond a small margin.

## Why a linear refinement was plausible

Lamzouri's arbitrary-parameter inequality gives one linear bound
`Q>=2tN-(2t-1)S-t^2 d` for each `t`, and EXP-006 combines the family with the
parity bound `2d<=N-O`. With no simple points and `k=O/N` the product reads
`Q/N>=2/(1-k)`, tight only for a single double or triple point. Separated
doubles and triples give the larger chord `Q/N>=2+3k`, which suggested
`Q>=2N+3O-4S`. A linear bound `Q>=2N+beta O` with any `beta>2` would lower the
EXP-010 onset.

## What fails

A real triple next to a near-real conjugate pair loses slack in proportion to
`|int u eta^2 sin(2pi x0 u)|^2/int u^2 eta^2` at a real zero `x0` of `K`. One
pair surrounded by several triples adds these losses. Six triples around one
pair already violate the chord:

$$
Q=57.941781999783\ldots<58=2N+3O-4S\qquad(N=20,\ O=6,\ S=0).
$$

Periodic lattices with several near-real pairs per triple push the excess
per triple further down. A certified 10001-cell lattice gives

$$
\frac{Q-2N}{O}=2.358863695426\ldots,
$$

so no inequality `Q>=2N+beta O-gamma S` with `beta>=2.365` holds for this
window. The infinite-lattice preflight suggests about `2.32`.

## Consequence

With the EXP-010 detectors, a valid linear refinement with `beta<2.365`
cannot reach `theta=0.532`; with the single-piece detector ceiling
`0.7173 nu` it could move the onset at most from 0.53396 to about 0.5324.
The finite-inequality route is closed. The remaining lever for the onset is
the admissible mollifier length, which EXP-012 pursues.

All numbers are Arb-certified at 128 bits except those marked as preflight or
ceiling values. See the
[verdict](../experiments/EXP-011-linear-refinement-barrier/verdict.md) and the
[route preflights](../context/2026-09-27-route-preflights.md).
