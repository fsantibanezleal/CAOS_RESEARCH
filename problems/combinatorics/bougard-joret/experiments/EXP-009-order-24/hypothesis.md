# EXP-009 preflight: every open second-regime triple of order 24 (BJB-019)

Date: 2026-11-09. Status: frozen before any computation. CPU only. Continues EXP-005 to EXP-008, which settled all
47 open triples with n <= 23 (note `second-regime` v0.02, 10.5281/zenodo.24059677).

## Question

Determine $f(n,\alpha,k)$ exactly at every triple of the open second-regime window of Bougard-Joret Conjecture 1
with $n = 24$: 6 triples.

| triple | $t(n,\alpha)$ | conjectured value | edge counts searched |
|---|---:|---:|---|
| (24,5,3) | 46 | 54 | 46 to 53 |
| (24,6,3) | 36 | 45 | 36 to 44 |
| (24,5,4) | 46 | 56 | 48 to 55 |
| (24,4,5) | 60 | 70 | 60 to 69 |
| (24,7,3) | 30 | 41 | 36 to 40 |
| (24,3,7) | 84 | 95 | 84 to 94 |

Edge counts below $t(n,\alpha)$ (Turan's theorem on the complement) and below $\lceil nk/2\rceil$ (minimum degree
$k$) are skipped.

## Method

EXP-008's pipeline unchanged (`run_enum.py`, the generators `geng_a<alpha>` gated in EXP-006, the filter `filter2`),
driven by `run9.sh` with the caps below.

## Prediction

The formula holds at every triple computed (MODERATE). The triples with $\alpha = 7$ or $k = 7$ may hit a cap: at
order 23 their top edge counts took 5,905 s and 10,422 s, and costs grow by roughly an order of magnitude per edge
count.

## Budget and stop condition

Triples run in the table's order. At most 4 hours of 28 processes per edge count and 24 hours in total; a triple
that hits a cap is reported as open with its partial lower bound (every edge count completed below it).
