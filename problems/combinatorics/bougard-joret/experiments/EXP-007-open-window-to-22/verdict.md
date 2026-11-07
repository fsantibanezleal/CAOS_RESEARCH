# EXP-007 verdict: the second-regime formula holds at every open triple up to order 22

Date: 2026-11-07. Status: **CONFIRMED [MV]** (the prediction held at every triple; no cap was reached).
Hypothesis committed before computation (f85ce6b9).

## Result

All 28 open second-regime triples of order at most 22 not covered by EXP-005 and EXP-006 were computed exactly with
EXP-006's gated pipeline (independence-pruned `geng` and the early-stopping filter). At every one, no graph with
fewer edges than t(n, alpha) + ceil(k*alpha/2) has independence number alpha and connectivity at least k, so the
value equals the conjectured one. With EXP-005 (7 triples) and EXP-006 (4 triples): **the second line of
Bougard-Joret Conjecture 1 holds at all 39 triples of its open window with n <= 22.**

| triple | conjectured | edge counts | graphs searched below | attained at conjectured value (graphs) | value | status |
|---|---:|---|---:|---|---:|---|
| (17,3,5) | 48 | 43 to 47 | 2,120 | yes (3) | 48 | CONFIRMED |
| (18,3,5) | 53 | 45 to 52 | 6,568 | yes (2) | 53 | CONFIRMED |
| (18,4,4) | 40 | 36 to 39 | 4,086 | yes (4) | 40 | CONFIRMED |
| (18,5,3) | 32 | 27 to 31 | 71,021 | yes (35) | 32 | CONFIRMED |
| (19,3,5) | 59 | 51 to 58 | 17,920 | yes (4) | 59 | CONFIRMED |
| (19,4,4) | 44 | 38 to 43 | 24,673 | yes (2) | 44 | CONFIRMED |
| (19,5,3) | 35 | 29 to 34 | 149,597 | yes (18) | 35 | CONFIRMED |
| (19,3,6) | 60 | 57 to 59 | 83 | yes (1) | 60 | CONFIRMED |
| (19,6,3) | 30 | 29 to 29 | 295 | yes (2) | 30 | CONFIRMED |
| (20,3,5) | 65 | 57 to 64 | 21,372 | yes (4) | 65 | CONFIRMED |
| (20,4,4) | 48 | 40 to 47 | 41,808 | yes (2) | 48 | CONFIRMED |
| (20,5,3) | 38 | 30 to 37 | 132,654 | yes (5) | 38 | CONFIRMED |
| (20,3,6) | 66 | 60 to 65 | 4,046 | yes (1) | 66 | CONFIRMED |
| (20,6,3) | 33 | 30 to 32 | 23,316 | yes (5) | 33 | CONFIRMED |
| (21,4,4) | 53 | 45 to 52 | 141,850 | yes (2) | 53 | CONFIRMED |
| (21,5,3) | 42 | 34 to 41 | 471,911 | yes (17) | 42 | CONFIRMED |
| (21,3,6) | 72 | 63 to 71 | 29,091 | yes (1) | 72 | CONFIRMED |
| (21,6,3) | 36 | 32 to 35 | 303,615 | yes (5) | 36 | CONFIRMED |
| (21,4,5) | 55 | 53 to 54 | 420 | yes (1) | 55 | CONFIRMED |
| (21,5,4) | 44 | 42 to 43 | 1,298 | yes (7) | 44 | CONFIRMED |
| (22,4,4) | 58 | 50 to 57 | 222,379 | yes (4) | 58 | CONFIRMED |
| (22,5,3) | 46 | 38 to 45 | 874,494 | yes (31) | 46 | CONFIRMED |
| (22,3,6) | 79 | 70 to 78 | 83,931 | yes (1) | 79 | CONFIRMED |
| (22,6,3) | 39 | 33 to 38 | 1,365,978 | yes (5) | 39 | CONFIRMED |
| (22,4,5) | 60 | 55 to 59 | 47,945 | not run | 60 | CONFIRMED |
| (22,5,4) | 48 | 44 to 47 | 101,779 | not run | 48 | CONFIRMED |
| (22,3,7) | 81 | 77 to 80 | 782 | not run | 81 | CONFIRMED |
| (22,7,3) | 35 | 33 to 34 | 20,112 | not run | 35 | CONFIRMED |

Confirmed 28 of 28; open 0.

"Graphs searched below" counts the candidates the pruned generator produced at the edge counts below the conjectured
value. "Attained" counts the qualifying graphs at the conjectured value when that edge count was also enumerated (the
run script did so when the step below it took under ten minutes); otherwise the Bougard-Joret construction attains
the value.

## Validation

The pipeline's gates are EXP-006's (`../EXP-006-second-regime-beyond-15/artifacts/filter2-gates.txt` and
`alpha-prune-gates.txt`): the filter equals networkx on every graph of order 8, and the pruned generator reproduces
the qualifying counts of twelve known cases. No edge count reached the 2-hour cap; the slowest, (22,3,7) at E = 80,
took 1,331 s; the recorded edge-count runs total 5.5 hours of wall-clock time on 28 processes (attainment runs included).

## Scope

Finite and exact. The open window is infinite (for fixed alpha and k it is finite, but alpha and k are unbounded);
the general second line remains open.
