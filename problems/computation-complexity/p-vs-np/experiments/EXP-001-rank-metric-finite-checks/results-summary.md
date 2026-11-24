# EXP-001 results

Run: `python -I run.py 2 3 4` (CPython, standard library only), 2026-11-24. Log: `artifacts/run-output.txt`.

| mu | matrices by rank | p_mu/p_1 by rank of B | maximum | sum of rank times chi_B by rank of B |
|---|---|---|---|---|
| 2 | 1, 9, 6 | 3/2, 1/2 | 3/2 | -3, 1 |
| 3 | 1, 49, 294, 168 | 7/4, 35/36, 11/12 | 7/4 | -43, 5, -3 |
| 4 | 1, 225, 7350, 37800, 20160 | 15/8, 65/56, 395/392, 157/168 | 15/8 | -2619, 133, -27, 21 |

| mu | rank-one transversal to E11 (span) | rank-one summands of I (span) | invertible (span) | transversality graph |
|---|---|---|---|---|
| 2 | 4 (4 of 4) | 6 (4 of 4) | 6 (4 of 4) | 9 vertices, connected, has a triangle |
| 3 | 36 (9 of 9) | 28 (9 of 9) | 168 (9 of 9) | 49 vertices, connected, has a triangle |
| 4 | 196 (16 of 16) | 120 (16 of 16) | 20160 (16 of 16) | 225 vertices, connected, has a triangle |

mu = 2: six maximal cliques through 0, each of four vertices; 18 transversal pairs of rank-one matrices; 6 triples
that are pairwise transversal.
