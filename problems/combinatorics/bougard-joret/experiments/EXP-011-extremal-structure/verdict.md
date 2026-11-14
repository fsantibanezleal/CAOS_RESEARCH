# EXP-011 verdict: structural prediction REFUTED; recount and Didin-derived predictions CONFIRMED

Date: 2026-11-14. Hypothesis frozen at 47c86e8f; first addendum a480c533, written after phase 1 and before phase 2;
second addendum e552f1c6, written before any phase 2 structure analysis.

## Result [MV]

- **Recount gate.** Every extremal graph at c = t(n,alpha) + ceil(k alpha/2) was regenerated at the 35 triples:
  246 graphs, with the count equal to the earlier record at all 35 (`artifacts/collect.jsonl`; 0 mismatches). Phase 1
  covered 22 triples on 4 processes, phase 2a 8 triples on 4, and phase 2b 5 triples on 24. The outputs are in
  `artifacts/collect-phase*-output.txt`.
- **Independent recheck.** All 246 pass a NetworkX recheck of edges, independence number and connectivity
  (`analyze.py`, 0 failures). All have connectivity exactly k.
- **Clique partition.** 206 graphs split into alpha cliques, and every one of them has the Bougard-Joret structure:
  balanced cliques and exactly ceil(k alpha/2) edges between them. Lemma: at m = c a partition forces that structure.
  The other 40 have clique cover number alpha + 1. Two independent methods agree on all 246: the alpha-colouring
  backtracking (`analyze.py`) and the maximal-clique cover (`verify.py`).
- **Where.** The 40 lie at
  - (10,3,3): 12 of 15;
  - (11,3,3): 3 of 6;
  - (16,5,3): 5 of 18;
  - (17,5,3): 9 of 34;
  - (18,5,3): 8 of 35;
  - (19,5,3): 3 of 18.
  All have k = 3 and alpha odd.
- **Didin's core parameter** (`didin.py`; p(G) by exact partition search, checked against a brute force on 400 random
  graphs):
  - every graph satisfies m >= t(n+s, alpha) - s, none with equality;
  - every s lies in the set that his inequality chain allows;
  - s = 1 for 32 graphs, and s = 2 for 8 graphs at (10,3,3), which have a connected alpha-core.

## Predictions

| Prediction | Frozen at | Outcome |
|---|---|---|
| Gate: regenerated counts equal the records (HIGH) | 47c86e8f | CONFIRMED, 35 of 35 |
| Every extremal graph has a balanced alpha-clique partition with ceil(k alpha/2) edges between cliques (MODERATE) | 47c86e8f | REFUTED by phase 1: 40 graphs have none |
| Phase 2: graphs with a partition have the Bougard-Joret structure (HIGH) | a480c533 | CONFIRMED |
| Phase 2: no graph without a partition outside k = 3, alpha odd (MODERATE) | a480c533 | CONFIRMED |
| Phase 2: no graph without a partition has clique cover number above alpha + 1 (MODERATE) | a480c533 | CONFIRMED (none in phase 2; all 40 earlier have alpha + 1) |
| Every graph satisfies Didin's inequality with s computed exactly (HIGH) | e552f1c6 | CONFIRMED, 246 of 246 |
| Every s lies in the allowed set; every phase 2 graph has a partition (HIGH) | e552f1c6 | CONFIRMED, 0 violations; all 63 + 18 phase 2 graphs split |

## Reading

- The natural strengthening of Bougard-Joret's Proposition 8 to the conjectured value, that m <= c forces a partition
  into alpha cliques, is false at k = 3 with alpha odd. A proof of the second line must work below c, or without the
  partition.
- Conditional on Didin's Theorem 3, extremal graphs without a partition need either p >= 2, k = 3, alpha odd, s = 1
  and n <= 4 alpha - 1, or p = 1 at six small triples. The data match exactly: case (b) occurs only at (10,3,3).
- The 32 graphs with s = 1 all consist of alpha - 2 cliques and one of two blocks, X6 or X7, on a cubic quotient. This
  led to EXP-013, which builds such graphs for every odd alpha.
- The phase 2 schedule changed from "after EXP-010 on 28 processes" to phases 2a and 2b. 2a ran on 4 processes beside
  EXP-010 and 2b on 24 after it. This is recorded in the first addendum; the method is unchanged.

## How could this be wrong?

The counts come from the same pipeline as EXP-006 to EXP-010 (validated in EXP-012). The structural results come
from NetworkX code that shares nothing with it, and the clique-partition answer is confirmed by two independent
methods. p(G) is computed by a search checked against a brute force on small graphs. Didin's inequality is used only
as a stated theorem; the test here could have refuted it, and did not.
