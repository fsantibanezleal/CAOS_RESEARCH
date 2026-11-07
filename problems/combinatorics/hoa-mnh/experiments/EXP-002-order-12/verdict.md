# EXP-002 verdict: no counterexample to Hoa's conjecture at order 12; A185306(12) = 151

Date: 2026-11-07. Status: **CONFIRMED [MV]** (the prediction of no counterexample held; the count prediction, 100
to 200, held). Hypothesis committed before the production run (1de9ac88).

## Result

Every maximal non-Hamiltonian graph of order 12, with every vertex set of every longest cycle:

| case | graphs generated | MNH graphs |
|---|---:|---:|
| A: a universal vertex, K_1 join H over every graph H on 11 vertices | 1,018,997,864 (= OEIS A000088(11)) | 114 |
| B: connected, maximum degree at most 8 (degree-sum-pruned generation) | 5,705,422,732 | 37 |
| **total** | | **151** |

Circumferences: 7 (1 graph), 8 (1), 9 (2), 10 (10), 11 (137). For all 151 graphs and every longest cycle, the
residual G - V(C) is a single complete graph.

1. **Hoa's conjecture holds for every MNH graph of order 12.** With EXP-001, it holds for every order up to 12, so
   the least counterexample order is in **[13, 56]**.
2. **A185306(12) = 151** (new term; with EXP-001, the sequence now reads ..., 18, 31, 67, 151 for n = 9..12).
3. No witness for Zhan's Questions 2 or 3 at order 12; f(12) = 1.

## Validation

- **Split gate:** the same split reproduces EXP-001 at orders 10 (27 + 4 = 31) and 11 (57 + 10 = 67).
- **Case A completeness:** the graphs read equal A000088(11) exactly.
- **Case B integrity:** the run was interrupted by a WSL restart and resumed by parts (a part is recorded only
  after its generator and filter finish); 16 randomly chosen parts were re-run from scratch and their counts
  compared with the stored records (`artifacts/recheck-caseB.txt`).
- **Independent re-check:** EXP-001's `verify.py` (plain backtracking, no shared code) confirms all 151 graphs:
  non-Hamiltonian, every nonadjacent pair joined by a Hamilton path, circumference, longest-cycle sets and residual
  flags (0 disagreements).
- **Prune soundness:** the degree-sum PRUNE hook reproduces 18, 31 and 67 at orders 9, 10 and 11 on its own.

## Reproduction

`join6.c` (case A), the EXP-001 `mnh.c` filter and `prune_degsum.c` hook; in WSL with nauty 2.8.9:
`geng -q 11 r/112 | join6 | mnh` and `geng_mnh -cq -D8 12 r/1120 | mnh`. All 151 graphs with their residual
flags: `artifacts/mnh-n12.txt`.
