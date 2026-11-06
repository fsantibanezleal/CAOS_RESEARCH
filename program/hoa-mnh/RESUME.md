# hoa-mnh: RESUME (session handoff)

Updated 2026-11-06 (opened). First read for any session, per methodology 07. Derived view: experiment verdicts win.

## 1. State in one screen

Maximal non-Hamiltonian (MNH): G is not Hamiltonian and G + e is Hamiltonian for every nonedge e. Hoa's
conjecture (1994): for every MNH graph G and every longest cycle C, G - V(C) is complete. Zhan
(arXiv:2608.00957v3) disproves it at every order n >= 56 (residual 2K_1, toughness 1, circumference n - 2) and
asks Questions 2-4; nobody has followed up [V, 2026-11-06]. The least counterexample order lies in [8, 56] (our
atlas check covers n <= 7). Hoa proved the conjecture for toughness < 1 and for delta >= n/3 [V via Zhan].

First round: EXP-001, the exact classification of MNH graphs to order 11 (12 if the cost allows) with every
longest cycle, deciding Hoa's conjecture and Zhan's Questions 2-4 below those orders and extending OEIS A185306.

## 2. The objects table

| Object | Definition / authority |
|---|---|
| MNH graph | non-Hamiltonian; every nonedge creates a Hamilton cycle; equivalently every nonadjacent pair is joined by a Hamilton path |
| residual | G - V(C) for a longest cycle C (Hoa's "restgraph") |
| Hoa's conjecture | every residual of every MNH graph is complete; false for n >= 56 (Zhan) |
| Zhan's Q2, Q3, Q4 | every residual component complete?; a connected non-complete residual?; f(n) = max number of residual components |
| degree-sum tightness | in an MNH graph every nonadjacent pair has d(u) + d(v) <= n - 1 (Bondy-Chvatal closure) |
| A185306 | number of MNH graphs on n vertices: 0, 1, 1, 1, 3, 3, 7, 9, 18, 31 (n = 1..10) |
| dossier | [2026-09-02 dossier](../../problems/combinatorics/petersen-coloring/context/scouting-2026-09/2026-09-02-dossier-hoa-mnh.md) |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-mnh-census | MNH graphs and every longest-cycle residual to order 11-12 | in preparation | - |

## 4. In flight

Opened 2026-11-06 on branch `work/hoa-mnh/open`. EXP-001 hypothesis to be frozen before any run.

## 5. Next actions

1. Freeze EXP-001's hypothesis; build the exact filter; gate against A185306 for n <= 10.
2. Run n = 11, then n = 12; enumerate every longest cycle of every MNH graph.
3. Gadget search (lens 2) on the classified MNH graphs for counterexamples below 56.

## 6. Where everything lives

- Records: `program/hoa-mnh/`; problem tree: `problems/combinatorics/hoa-mnh/`.
- Sources: data root `caos-research/hoa-mnh/sources/` (manifest with SHA-256 in `context/references.md`).
- Generator: nauty geng 2.8.9 built in WSL (`~/caos-nauty/nauty2_8_9/geng`), from the official tarball.

## 7. Gotchas

- A185306 counts K_2 as MNH and K_1 as Hamiltonian; the counts include the connectivity-1 MNH graphs (two cliques
  sharing a vertex), so a biconnected-only generation would undercount.
- Hamiltonicity tests must be exact; no heuristic search may conclude non-Hamiltonicity.
