# EXP-006 preflight: the second regime beyond order 15 (BJB-017)

Date: 2026-11-07. Status: frozen before any computation. CPU only. Continues EXP-005.

## Question

The open second-regime window of Bougard-Joret Conjecture 1 ($\alpha\ge3$, $k\alpha<n$,
$\lfloor n/\alpha\rfloor\le\lceil k\alpha/2\rceil-\alpha+1$; EXP-005 hypothesis) continues past the seven triples
of EXP-005. In order of expected cost, determine $f(n,\alpha,k)$ exactly at

| $(n,\alpha,k)$ | conjectured $t(n,\alpha)+\lceil k\alpha/2\rceil$ | degree bound $\lceil nk/2\rceil$ |
|---|---:|---:|
| (16,5,3) | 18+8 = 26 | 24 |
| (17,5,3) | 21+8 = 29 | 26 |
| (17,4,4) | 28+8 = 36 | 34 |
| (16,3,5) | 35+8 = 43 | 40 |

($t(16,5)=6+3+3+3+3$, $t(17,5)=6+6+3+3+3$, $t(17,4)=10+6+6+6$, $t(16,3)=15+10+10$.)

## Method

As EXP-005 (complete enumeration): `geng -q -d<k> <n> <E>:<E> <res>/<mod>` for every $E$ from the degree bound to
the conjectured value minus one, piped into the exact `filter.c` (independence number exactly $\alpha$,
connectivity at least $k$). No graph below the conjectured value proves the lower bound; the Bougard-Joret
construction attains the conjectured value.

## Gates

The EXP-005 gates stand (filter equal to networkx on all 12,346 graphs on 8 vertices; known values reproduced).
Before each triple, the number of graphs at its smallest edge count is checked against a direct count by a second
run with a different `mod`.

## Prediction

The formula holds at every triple computed. Confidence MODERATE.

## Budget and stop condition

At most 12 hours of 28 processes in total. A triple whose next edge count extrapolates (from the growth of the
previous counts) past the remaining budget is stopped and reported as open with its partial lower bound.
