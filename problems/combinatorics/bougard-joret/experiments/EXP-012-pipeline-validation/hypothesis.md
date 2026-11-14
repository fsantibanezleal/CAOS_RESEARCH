# EXP-012 preflight: validation of the search pipeline at the production parameters

Date: 2026-11-11. Status: frozen before any computation. CPU only.

## Question

EXP-005 to EXP-010 decide the second line of the Bougard-Joret conjecture with three components:
- nauty's `geng` (2.8.9), with minimum degree k and a fixed edge count, split into `res/mod` parts;
- the PRUNE hook `prune_alpha` (EXP-006), compiled into `geng_a<A>`;
- the exact filter `filter2` (EXP-006): independence number exactly alpha, vertex connectivity at least k.

The filter was cross-checked only on the 12,346 graphs of order 8 with alpha <= 6 and k <= 5
(`EXP-006.../artifacts/filter2-gates.txt`). The prune was checked end to end on 12 small cases
(`alpha-prune-gates.txt`). Production used orders up to 24, k up to 7 and alpha up to 7. An independent audit
(2026-11-10) asked for validation at those parameters.

Question: do the three components, as built and run in production, compute exactly what the method assumes, on
inputs at the production orders and parameters?

## Method

All ground truth comes from networkx 3.4.1 on Windows, which shares no code with the C programs:
- the independence number as the maximum clique of the complement (`max_weight_clique`, unit weights);
- the vertex connectivity (`node_connectivity`).

The C programs run in WSL (Ubuntu 24.04, gcc 13.3.0).

- **Gate F, provenance.** Rebuild `filter2` from `EXP-006.../filter2.c` with `gcc -O3`, and `geng_a3` to `geng_a7`
  from nauty 2.8.9's `geng.c` and `EXP-006.../prune_alpha.c` with the build line in that file's header. Compare the
  SHA-256 of each rebuilt binary with the production binary. When a hash differs, run Gates A to D on both binaries.
- **Gate A, filter on constructed graphs with known answers.** Families at orders 10 to 24 that spread the
  independence number over 2 to 8 and the connectivity over 1 to 9:
  - Harary graphs H(k, n);
  - circulants with random connection sets;
  - random d-regular graphs (d = 3 to 9);
  - complements of sparse random graphs;
  - unions of alpha cliques joined by random cross edges;
  - the EXP-011 extremal graphs.

  Each graph is decided by `filter2` at every (a, k) with a in {alpha-1, alpha, alpha+1} and k in
  {kappa-1, kappa, kappa+1}, with 1 <= k <= 9. Expected: kept exactly when a = alpha and kappa >= k. At least 3,000
  graphs and 20,000 decisions; fixed seeds.
- **Gate B, filter on production streams.** For every production triple with k >= 6 or alpha = 7, take
  `geng_a<alpha> -q -d<k> n E:E res/mod` at E in {c-1, c, c+1}, on slices of at most about 3,000 graphs:
  (19,3,6), (20,3,6), (21,3,6), (22,3,6), (22,3,7), (23,3,6), (23,3,7), (22,7,3), (23,7,3), (24,7,3), (24,3,7).
  Compare the set `filter2` keeps on each slice with the set networkx says qualifies.
- **Gate C, the prune hook on its own.** A harness calls `prune_alpha(g, n, n)` for each graph on standard input,
  compiled at ALPHA_BOUND = 2 to 8. Inputs: the Gate A graphs, and random graphs of orders 8 to 24 with densities
  chosen to put the independence number near the bound. Expected: the hook returns 1 exactly when the independence
  number exceeds the bound.
- **Gate D, the res/mod partition under the prune.** For (17,5,3) at E = 29, (19,3,6) at E = 60 and (20,4,4) at
  E = 48, compare the sorted output of `geng_a<alpha>` over one part (mod 1) with the union of its 56 parts
  (mod 56). Expected: identical multisets.
- **Gate E, the generator's completeness at production orders.** Compare `geng` counts with OEIS values read on
  oeis.org during the run:
  - connected graphs of order 9 and 10 (A001349);
  - connected cubic graphs of orders 16 to 22 (A002851), with `-c -d3 -D3`;
  - connected 4-regular graphs of orders 12 to 15 (A006820), with `-c -d4 -D4`.

## Predictions

- Gate F: every rebuilt binary is byte-identical to the production binary (MODERATE; the build may embed paths).
- Gates A to E: zero disagreements (HIGH).

## Budget

At most 6 CPU-hours. Gates B and E run on at most 4 processes beside EXP-010; networkx runs on at most 4 processes.
