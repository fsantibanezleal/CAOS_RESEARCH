# EXP-005 verdict: the second-regime formula holds at the seven smallest open triples

Date: 2026-11-06. Status: **CONFIRMED [MV]** for the seven triples of the frozen table. The hypothesis was
committed before any computation; the method changed during the run (see Deviations).

## Result

Bougard-Joret Conjecture 1, second line, $f(n,\alpha,k)=t(n,\alpha)+\lceil k\alpha/2\rceil$ for $n>k\alpha$, is
proved in their paper only when $\lfloor n/\alpha\rfloor\ge\lceil k\alpha/2\rceil-\alpha+2$ ($\alpha\ge3$). At
every triple of the open window listed in the hypothesis, the exact value equals the formula:

| $(n,\alpha,k)$ | conjectured | exhaustive search: no graph with $\le E$ edges | value |
|---|---:|---|---:|
| (10,3,3) | 17 | $E=16$ (graphs with 15 and 16 edges searched: 21 and 362) | **17** (15 graphs at 17) |
| (11,3,3) | 20 | $E=19$ (17 to 19 edges: 55,812 graphs) | **20** (6 graphs at 20) |
| (13,4,3) | 21 | $E=20$ (1,999 graphs) | **21** (1 graph at 21) |
| (14,4,3) | 24 | $E=23$ (21 to 23 edges: 2,147,042 graphs) | **24** (1 graph at 24) |
| (15,4,3) | 27 | $E=26$ (23 to 26 edges: 904,211,641 graphs) | **27** (1 graph at 27) |
| (13,3,4) | 28 | $E=27$ (26 and 27 edges: 1,095,032 graphs) | **28** (1 graph at 28) |
| (14,3,4) | 32 | $E=31$ (28 to 31 edges: 5,268,961,461 graphs) | **32** (attained by the Bougard-Joret construction) |

"Graphs" are all non-isomorphic graphs on $n$ vertices with that many edges and minimum degree at least $k$ (a
necessary condition for $k$-connectivity), from nauty `geng`; each was tested exactly for independence number
$\alpha$ and connectivity at least $k$. Counts per edge value: `artifacts/enum.jsonl`.

This is evidence for the second line of the conjecture in the open window, not a proof of it: the window is
infinite and grows with $\alpha$ and $k$.

## Validation

- **Generator:** nauty 2.8.9 built from the official tarball (`geng`); connected-graph counts for $n=5,7,8$
  equal OEIS A001349 (21, 853, 11117).
- **Filter** (`filter.c`, exact bitset independence number; connectivity by deleting every vertex set of size
  $<k$): equals networkx on all 12,346 graphs on 8 vertices, for every $(\alpha,k)$ with $\alpha\le6$, $k\le5$
  (0 mismatches).
- **Known answers:** $f(7,3,4)=15$ (Das-Gupta's counterexample to the first line), $f(6,2,3)=9$, $f(6,2,4)=12$,
  and the second-regime value at the proved triple $f(12,3,3)=23$ (no graph with 18 to 22 edges; 2 graphs at 23)
  are all reproduced.
- **SAT route** (`run.py`): reproduced $(7,3,4)=15$ and found the conjectured graphs at (10,3,3) and (12,3,3); its
  lower side did not finish in the caps (`artifacts/results.jsonl`).

## Deviations from the hypothesis

The hypothesis froze a SAT search with lazy connectivity cuts. Its UNSAT side did not finish at $(10,3,3)$, $E=16$
(1 hour) nor at the $(12,3,3)$ gate, $E=22$ (30 minutes, two encodings). The result above comes from complete
enumeration (`run_enum.py`, `filter.c`), which decides the same question exactly and is gated by the same known
answers. The $E=32$ enumeration at (14,3,4) is not needed for the value (the construction attains it).

## Reproduction

In WSL with nauty built: `python3 run_enum.py <geng> <filter> n alpha k Emin Emax --jobs 28 --mod 896`;
`gcc -O2 -o filter filter.c`.
