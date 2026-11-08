# EXP-008 preflight: every open second-regime triple of order 23 (BJB-018)

Date: 2026-11-07. Status: frozen before any computation. CPU only. Continues EXP-005 to EXP-007, which settled all
39 open triples with n <= 22 (note `second-regime` v0.01, 10.5281/zenodo.24044538).

## Question

Determine $f(n,\alpha,k)$ exactly at every triple of the open second-regime window of Bougard-Joret Conjecture 1
($\alpha\ge3$, $k\ge3$, $k\alpha<n$, $n\ge2\alpha$, $n\ge\alpha+k$,
$\lfloor n/\alpha\rfloor\le\lceil k\alpha/2\rceil-\alpha+1$) with $n = 23$: 8 triples.

| triple | $t(n,\alpha)$ | conjectured value | edge counts searched |
|---|---:|---:|---|
| (23,7,3) | 27 | 38 | 35 to 37 |
| (23,5,3) | 42 | 50 | 42 to 49 |
| (23,4,4) | 55 | 63 | 55 to 62 |
| (23,6,3) | 33 | 42 | 35 to 41 |
| (23,3,6) | 77 | 86 | 77 to 85 |
| (23,4,5) | 55 | 65 | 58 to 64 |
| (23,5,4) | 42 | 52 | 46 to 51 |
| (23,3,7) | 77 | 88 | 81 to 87 |

Edge counts below $t(n,\alpha)$ are skipped (Turan's theorem on the complement) and below $\lceil nk/2\rceil$
(minimum degree $k$).

## Method

EXP-007's pipeline unchanged: `geng_a<alpha>` (geng with the independence-number PRUNE hook, gated in EXP-006)
`-q -d<k> 23 E:E r/mod` piped into `filter2` (independence number exactly $\alpha$, connectivity at least $k$),
through `run_enum.py`, every edge count from the lower bound to the conjectured value minus one.

## Prediction

The formula holds at every triple computed (MODERATE). The largest-k triples may exceed the budget.

## Budget and stop condition

Triples run in the table's order (increasing width of the search, then $k$). At most 3 hours of up to 28 processes
per edge count and 24 hours in total; a triple that hits a cap is reported as open with its partial lower bound
(every edge count completed below it).
