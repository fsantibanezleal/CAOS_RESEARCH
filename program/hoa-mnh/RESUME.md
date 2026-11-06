# hoa-mnh: RESUME (session handoff)

Updated 2026-11-06 (opened). First read for any session, per methodology 07. Derived view: experiment verdicts win.

## 1. State in one screen

Maximal non-Hamiltonian (MNH): G is not Hamiltonian and G + e is Hamiltonian for every nonedge e. Hoa's
conjecture (1994): for every MNH graph G and every longest cycle C, G - V(C) is complete. Zhan
(arXiv:2608.00957v3) disproves it at every order n >= 56 (residual 2K_1, toughness 1, circumference n - 2) and
asks Questions 2-4; nobody has followed up [V, 2026-11-06]. The least counterexample order lies in [8, 56] (our
atlas check covers n <= 7). Hoa proved the conjecture for toughness < 1 and for delta >= n/3 [V via Zhan].

EXP-001 (2026-11-06): every MNH graph of order <= 11 classified with every longest cycle. Hoa's conjecture holds
through order 11, so the least counterexample order is in [12, 56]; A185306(11) = 67 (new term); no witness for
Zhan's Questions 2-3 and f(n) = 1 for 4 <= n <= 11.

## 2. The objects table

| Object | Definition / authority |
|---|---|
| MNH graph | non-Hamiltonian; every nonedge creates a Hamilton cycle; equivalently every nonadjacent pair is joined by a Hamilton path |
| residual | G - V(C) for a longest cycle C (Hoa's "restgraph") |
| Hoa's conjecture | every residual of every MNH graph is complete; false for n >= 56 (Zhan) |
| Zhan's Q2, Q3, Q4 | every residual component complete?; a connected non-complete residual?; f(n) = max number of residual components |
| degree-sum tightness | in an MNH graph every nonadjacent pair has d(u) + d(v) <= n - 1 (Bondy-Chvatal closure) |
| A185306 | number of MNH graphs on n vertices: 0, 1, 1, 1, 3, 3, 7, 9, 18, 31 (n = 1..10); 67 at n = 11 (EXP-001) |
| dossier | [2026-09-02 dossier](../../problems/combinatorics/petersen-coloring/context/scouting-2026-09/2026-09-02-dossier-hoa-mnh.md) |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-mnh-census | MNH graphs and every longest-cycle residual to order 11-12 | CONFIRMED to order 11 | Hoa holds for n <= 11 (n_0 in [12, 56]); A185306(11) = 67; no Q2/Q3 witness; f(n) = 1 for 4 <= n <= 11 |

## 4. In flight

EXP-001 complete 2026-11-06 (verdict CONFIRMED to order 11). Order 12 not run (about 29 hours by plain generation, over the stop condition); next: HMB-005 (faster order-12 route) and HMB-002 (gadget search).

## 5. Next actions

1. HMB-005: order 12 by the universal-vertex split (K_1 join a maximal nontraceable graph on 11 vertices) plus
   maximum degree <= n - 4 for the rest; each part must reproduce the plain counts at orders 10 and 11 first.
2. HMB-002: gadget search (lens 2) on the classified MNH graphs for counterexamples below 56.
3. HMB-003: read Problem 266 and Hoa 2005 before any write-up.

## 6. Where everything lives

- Records: `program/hoa-mnh/`; problem tree: `problems/combinatorics/hoa-mnh/`.
- Sources: data root `caos-research/hoa-mnh/sources/` (manifest with SHA-256 in `context/references.md`).
- Generator: nauty geng 2.8.9 built in WSL (`~/caos-nauty/nauty2_8_9/geng`), from the official tarball.

## 7. Gotchas

- A185306 counts K_2 as MNH and K_1 as Hamiltonian; the counts include the connectivity-1 MNH graphs (two cliques
  sharing a vertex), so a biconnected-only generation would undercount.
- Hamiltonicity tests must be exact; no heuristic search may conclude non-Hamiltonicity.
