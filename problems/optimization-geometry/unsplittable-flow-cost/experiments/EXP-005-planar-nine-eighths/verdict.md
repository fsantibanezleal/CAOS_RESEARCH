# EXP-005 verdict: CONFIRMED, the frontier constant is at least 9/8, also on planar instances

Run 2026-11-07 with the repository `.venv` (Python 3.13), exact rationals, no floats, no randomness, no network.
Hypothesis frozen at 50e402e9 before any computation. Artifacts: `artifacts/run-log.txt`,
`artifacts/grid-top.txt` (the 50 largest frontier values of the grid). Reproduce from the repository root:

```
.venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-005-planar-nine-eighths/run.py --jobs 4
```

## Result

- **P1 PASS [MV].** On M(3/4, 1/4, 1/2 + eps, 1/4, 1) with Muffatti's costs (each paid path of integral cost 1),
  the fractional cost is 2 - eps, and the least violation over all routings that cost no more is exactly
  9/8 - (3/4) eps, at eps = 1/10, 1/100 and 1/1000 (21/20, 447/400, 4497/4000).
- **P2 PASS [MV].** Each instance is acyclic, has a K4 subdivision on {s, u, v, w}, and is planar by our
  degree-based Kuratowski check, like Rybin's instance.
- **P3 PASS [MV].** The frontier value (the violation the best nonnegative pricing can force) equals the same
  9/8 - (3/4) eps on all three, witnessed by the cost vector (3/10, 2/5, 0, 3/10, 0, 0, 0, 0, 0): Muffatti's costs
  (1, 4/3, 1 on the three paid arcs) normalised to sum 1. On this family his pricing is optimal.
- **P4 (exploration) [MV on the grid].** Over 108,000 grid points (d1 = 1, b in k/8, d3 in k/4, fractions in k/16)
  the largest frontier value is 69/64 = 9/8 - 3/64, at b = 3/4, d3 = 1, (r1, q, r3) = (1/4, 9/16, 1/4): Muffatti's
  point with eps = 1/16, the closest the grid gets to his limit. No grid point exceeds 9/8. The next values (17/16 at
  q = 1/2 with r3 = 5/16, 135/128 at b = 5/8) lie below it. Wall time 380 s on 4 processes.

## What follows

1. **alpha* >= 9/8 and 9/8 <= alpha*_planar <= 2** (upper bound TVZ24). Since every member of the family
   forces 9/8 - (3/4) eps on a planar acyclic instance, no universal constant below 9/8 works. The bound is
   Muffatti's (GitHub `terrorproforma/maths`, `planar-cost-lower-bound`, commit dbf9d23, 2026-08-31); this
   experiment is our independent exact check, plus the finding that optimal pricing gives nothing more on the family.
   Our previous best, alpha* >= 16/15 from Rybin's instance itself (EXP-002, EXP-004), is superseded as a bound;
   alpha_inst = 16/15 for Rybin's instance stands.
2. **EXP-004's reading is withdrawn.** Its [D] sentence "pushing alpha* meaningfully above 1 will not come from
   tuning this family's parameters" is false: the same topology with demands (1, 3/4, 1) and fractions near
   (1/4, 1/2, 1/4) reaches 9/8. Its [MV] sweep stands; its integer box contained neither these demands with these
   splits nor fractions approaching q = 1/2 from above (the bound needs q > 1/2 strictly).
3. **Within the family, 9/8 looks like the ceiling** (Muffatti's symmetric analysis, and our grid with optimal
   pricing and asymmetric parameters). A larger forced violation needs another structure, which is where UFB-037
   and UFB-065 point.

## Deviation from the frozen plan

The first run computed P1 to P4 but crashed while writing `grid-top.txt` (the artifacts folder was created only at
the end). The fix creates it at start; the rerun reproduced P1 to P3 identically and completed P4. No method change.
