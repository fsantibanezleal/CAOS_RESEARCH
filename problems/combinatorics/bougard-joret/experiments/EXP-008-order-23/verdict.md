# EXP-008 verdict: CONFIRMED, the second-regime value holds at all 8 open triples of order 23

Date: 2026-11-08. Hypothesis frozen at 19125234 before any computation. Status: **CONFIRMED [MV]**.

## Result

For each of the 8 open second-regime triples with n = 23, every candidate graph at every edge count from the lower
bound to the conjectured value minus one was enumerated (geng with the independence-number PRUNE hook, minimum
degree k, then the exact filter `filter2`), and none has independence number alpha and connectivity at least k. So
f(n, alpha, k) is at least the conjectured value t(n, alpha) + ceil(k alpha / 2), which the Bougard-Joret
construction attains:

| triple | f | edge counts searched | graphs searched below | seconds |
|---|---:|---|---:|---:|
| (23,7,3) | 38 | 35 to 37 | 1,456,747 | 6,526 |
| (23,5,3) | 50 | 42 to 49 | 954,295 | 200 |
| (23,4,4) | 63 | 55 to 62 | 190,804 | 342 |
| (23,6,3) | 42 | 35 to 41 | 2,519,045 | 241 |
| (23,3,6) | 86 | 77 to 85 | 100,793 | 1,306 |
| (23,4,5) | 65 | 58 to 64 | 610,557 | 7,350 |
| (23,5,4) | 52 | 46 to 51 | 1,410,017 | 5,162 |
| (23,3,7) | 88 | 81 to 87 | 62,230 | 13,918 |

In all, 7,304,488 candidate graphs in 35,045 seconds of wall-clock time on 28 processes (`artifacts/enum.jsonl`,
`artifacts/summary.md`, `artifacts/run8-output.txt`). No edge count reached its 3-hour cap (the largest, (23,3,7) at
E = 87, took 10,422 seconds), and the run ended well inside the 24-hour budget.

With EXP-005 to EXP-007, the second line of Bougard-Joret Conjecture 1 now holds at every one of the 47 open-window
triples of order at most 23. This is evidence in the smallest open cases, not a proof of the second line.

## Method notes

The pipeline is EXP-007's, unchanged (`run_enum.py` copied as is; the generators `geng_a<alpha>` and `filter2` were
gated in EXP-006). `run8.sh` reads the edge range of each triple from `triples.json` and applies the frozen caps.
