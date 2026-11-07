# EXP-006 verdict: the second-regime formula holds at four more open triples, up to order 17

Date: 2026-11-07. Status: **CONFIRMED [MV]**. Hypothesis committed before computation (c04a8a8f); the method was
sped up during the run by two gated changes (below).

## Result

| $(n,\alpha,k)$ | conjectured $t(n,\alpha)+\lceil k\alpha/2\rceil$ | no qualifying graph with | qualifying graphs at the conjectured value | value |
|---|---:|---|---:|---:|
| (16,5,3) | 26 | 24, 25 edges | 18 | **26** |
| (17,5,3) | 29 | 26, 27, 28 edges | 34 | **29** |
| (17,4,4) | 36 | 34, 35 edges | 2 | **36** |
| (16,3,5) | 43 | 40, 41, 42 edges | 3 | **43** |

Together with EXP-005, the second line of Bougard-Joret Conjecture 1 holds at all eleven open triples computed
so far. A "qualifying graph" has $n$ vertices, independence number exactly $\alpha$ and connectivity at least $k$;
the extremal graphs at the conjectured value appear in the enumeration itself (`artifacts/enum.jsonl`).

## Method and its two gated changes

Complete enumeration as in EXP-005 (nauty `geng`, every graph with minimum degree at least $k$ and each edge count,
then an exact filter). Two changes, each gated before use (`artifacts/filter2-gates.txt`,
`artifacts/alpha-prune-gates.txt`):

1. `filter2.c`: the independence-number search stops once an independent set of size $\alpha+1$ is found (such a
   graph is rejected anyway). Gates: equal to networkx on all 12,346 graphs on 8 vertices for every
   $(\alpha,k)$, and kept counts equal to `filter.c` on four EXP-005 cases.
2. `prune_alpha.c`, a geng PRUNE hook: a partial graph with an independent set of size $\alpha+1$ is discarded
   with its whole subtree. Sound because geng only adds vertices, the partial graph is an induced subgraph of
   every completion, and an induced subgraph's independence number never exceeds the graph's. Gates: the kept
   counts of twelve known cases (from $f(7,3,4)=15$ through (17,5,3), $E=27$) are reproduced exactly.

Before the prune, (17,5,3) at $E=27$ took 1,040 s (35,329,226 graphs, none qualifying); with it, 0.4 s (482
graphs, none qualifying). The early unpruned records are kept in `artifacts/enum.jsonl` and agree.

## Reproduction

In WSL with nauty 2.8.9: build `geng_a<alpha>` with `prune_alpha.c` (`-DALPHA_BOUND=<alpha>`), `gcc -O2 -o filter2
filter2.c`, then `python3 run_enum.py geng_a<alpha> filter2 n alpha k Emin Emax --jobs 28 --mod 56`.
