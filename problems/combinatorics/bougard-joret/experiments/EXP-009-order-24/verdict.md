# EXP-009 verdict: 4 of 6 CONFIRMED; (24,7,3) and (24,3,7) OPEN at the per-edge cap

Date: 2026-11-10. Hypothesis frozen at 153f1166 before any computation.

## Result [MV]

Same pipeline as EXP-008 (geng with the independence-number PRUNE hook, minimum degree k, the exact filter
`filter2`), 28 processes, every edge count from the lower bound to the conjectured value minus one.

| triple | conjectured | edge counts | graphs searched below | seconds | status |
|---|---:|---|---:|---:|---|
| (24,5,3) | 54 | 46 to 53 | 644,641 | 369 | CONFIRMED: f = 54 |
| (24,6,3) | 45 | 36 to 44 | 2,062,478 | 313 | CONFIRMED: f = 45 |
| (24,5,4) | 56 | 48 to 55 | 5,849,782 | 8,228 | CONFIRMED: f = 56 |
| (24,4,5) | 70 | 60 to 69 | 1,860,761 | 7,473 | CONFIRMED: f = 70 |
| (24,7,3) | 41 | 36 to 40 | 814,579 (36 to 39) | 2,282 + cap | OPEN: f >= 40 (E = 40 hit the 4-hour cap) |
| (24,3,7) | 95 | 84 to 94 | 138,923 (84 to 93) | 6,286 + cap | OPEN: f >= 94 (E = 94 hit the 4-hour cap) |

`artifacts/enum.jsonl` holds one record per completed edge count, `artifacts/summary.md` the table above,
`artifacts/run9-output.txt` the driver's lines (two caps, total 55,695 seconds of wall-clock time, inside the 24-hour
budget). No candidate graph was found at any completed edge count.

## Reading

- The second line of Bougard-Joret Conjecture 1 holds at 51 of the 53 open-window triples of order at most 24; the two
  open ones are each one edge count short of a decision: f(24,7,3) is 40 or 41 and f(24,3,7) is 94 or 95.
- The prediction (formula holds at every triple computed) holds at every triple whose search finished; the
  hypothesis named exactly these two triples as likely to hit a cap.
- Growth per edge count at the top of each search is a factor of 8 to 13 in graphs and in time ((24,5,4): 1,013 s at
  E = 54, 6,991 s at E = 55; (24,3,7): 1,050 s at E = 92, 4,608 s at E = 93), so the two capped edge counts need
  roughly 6 to 15 hours each on 28 processes (BJB-021).
