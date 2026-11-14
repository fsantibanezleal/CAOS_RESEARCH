# EXP-010 verdict: CONFIRMED; f(24,7,3) = 41 and f(24,3,7) = 95

Date: 2026-11-14 (runs finished 2026-11-11). Hypothesis frozen at 084e0874 before any computation.

## Result [MV]

EXP-009's pipeline unchanged (`run_enum.py`, `geng_a7` and `geng_a3` with the independence-number PRUNE hook,
minimum degree k, the exact filter `filter2`), one edge count per triple, 56 disjoint parts, 14 processes per triple,
both triples at the same time.

| triple | edge count | graphs generated | kept | seconds | conclusion |
|---|---:|---:|---:|---:|---|
| (24,7,3) | 40 | 23,556,793 | 0 | 42,833.6 | f(24,7,3) = 41, the conjectured value |
| (24,3,7) | 94 | 569,264 | 0 | 38,875.3 | f(24,3,7) = 95, the conjectured value |

With EXP-009's completed edge counts below each (36 to 39 and 84 to 93, no graph kept), no qualifying graph exists
below the conjectured value at either triple, and the Bougard-Joret construction attains it.

`artifacts/enum.jsonl` holds the two records and `artifacts/run-24-*-output.txt` the driver's output (exit 0 for
both). Both runs stayed inside the 20-hour cap.

## Reading

- The prediction holds: no graph at either edge count.
- With EXP-005 to EXP-009, the second line of Bougard-Joret Conjecture 1 holds at all 53 open-window triples with
  n <= 24 (alpha >= 3, k >= 3, outside the range Bougard and Joret's Proposition 8 settles).
- Didin (Zenodo 10.5281/zenodo.22831382, preprint under review) claims the lower bound of the second line for all
  n > k alpha; this enumeration is an independent exhaustive check of that claim on the 53 triples, not a proof of
  it.
- Cost: on 14 processes each, 11.9 and 10.8 hours. The pruned output at (24,7,3), E = 40 is about 30 times that at E = 39
  (790,718 graphs), the largest single edge count of the programme.

## How could this be wrong?

The search rests on geng's completeness with the PRUNE hook and the res/mod split, and on the filter; EXP-012
validates each at the production parameters (provenance, filter at k = 6, 7 and alpha = 7, the hook, the split, the
generator's counts). A defect there would affect every experiment from EXP-006 on alike.
