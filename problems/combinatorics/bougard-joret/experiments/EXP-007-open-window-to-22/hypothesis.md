# EXP-007 preflight: every open second-regime triple up to order 22

Date: 2026-11-07. Status: frozen before any computation. CPU only. Continues EXP-005 and EXP-006 (BJB-017).

## Question

Determine $f(n,\alpha,k)$ exactly at every triple of the open second-regime window of Bougard-Joret Conjecture 1
($\alpha\ge3$, $k\ge3$, $k\alpha<n\le22$, $n\ge2\alpha$, $n\ge\alpha+k$,
$\lfloor n/\alpha\rfloor\le\lceil k\alpha/2\rceil-\alpha+1$) not computed in EXP-005 or EXP-006: 28 triples.

| triple | $t(n,\alpha)$ | conjectured value | edge counts searched |
|---|---:|---:|---|
| (17,3,5) | 40 | 48 | 43 to 47 |
| (18,3,5) | 45 | 53 | 45 to 52 |
| (18,4,4) | 32 | 40 | 36 to 39 |
| (18,5,3) | 24 | 32 | 27 to 31 |
| (19,3,5) | 51 | 59 | 51 to 58 |
| (19,4,4) | 36 | 44 | 38 to 43 |
| (19,5,3) | 27 | 35 | 29 to 34 |
| (19,3,6) | 51 | 60 | 57 to 59 |
| (19,6,3) | 21 | 30 | 29 to 29 |
| (20,3,5) | 57 | 65 | 57 to 64 |
| (20,4,4) | 40 | 48 | 40 to 47 |
| (20,5,3) | 30 | 38 | 30 to 37 |
| (20,3,6) | 57 | 66 | 60 to 65 |
| (20,6,3) | 24 | 33 | 30 to 32 |
| (21,4,4) | 45 | 53 | 45 to 52 |
| (21,5,3) | 34 | 42 | 34 to 41 |
| (21,3,6) | 63 | 72 | 63 to 71 |
| (21,6,3) | 27 | 36 | 32 to 35 |
| (21,4,5) | 45 | 55 | 53 to 54 |
| (21,5,4) | 34 | 44 | 42 to 43 |
| (22,4,4) | 50 | 58 | 50 to 57 |
| (22,5,3) | 38 | 46 | 38 to 45 |
| (22,3,6) | 70 | 79 | 70 to 78 |
| (22,6,3) | 30 | 39 | 33 to 38 |
| (22,4,5) | 50 | 60 | 55 to 59 |
| (22,5,4) | 38 | 48 | 44 to 47 |
| (22,3,7) | 70 | 81 | 77 to 80 |
| (22,7,3) | 24 | 35 | 33 to 34 |

Edge counts below $t(n,\alpha)$ are skipped: by Turan's theorem on the complement, a graph on $n$ vertices with
independence number at most $\alpha$ has at least $t(n,\alpha)$ edges. Edge counts below $\lceil nk/2\rceil$ are
skipped (minimum degree $k$).

## Method

EXP-006's gated pipeline: `geng_a<alpha>` (geng with the independence-number PRUNE hook) `-q -d<k> n E:E r/mod`
piped into `filter2` (independence number exactly $\alpha$, connectivity at least $k$), every edge count from the
lower bound to the conjectured value minus one; the conjectured value itself is also enumerated when it costs less
than the step below it, to exhibit the extremal graphs.

## Prediction

The formula holds at every triple computed (MODERATE). Some triples may exceed the budget.

## Budget and stop condition

Triples are run in increasing order of $n$, then of $\lceil k\alpha/2\rceil$. At most 2 hours of 28 processes per
edge count and 12 hours in total; a triple that hits a cap is reported as open with its partial lower bound
(every edge count completed below it).
