# hoa-mnh: RESUME (session handoff)

Updated 2026-11-06 (opened). First read for any session, per methodology 07. Derived view: experiment verdicts win.

## 1. State in one screen

Maximal non-Hamiltonian (MNH): G is not Hamiltonian and G + e is Hamiltonian for every nonedge e. Hoa's
conjecture (1994): for every MNH graph G and every longest cycle C, G - V(C) is complete. Zhan
(arXiv:2608.00957v3) disproves it at every order n >= 56 (residual 2K_1, toughness 1, circumference n - 2) and
asks Questions 2-4; nobody has followed up [V, 2026-11-06]. The least counterexample order lies in [8, 56] (our
atlas check covers n <= 7). Hoa proved the conjecture for toughness < 1 and for delta >= n/3 [V via Zhan].

EXP-001/EXP-002 (2026-11-06/07): every MNH graph of order <= 12 classified with every longest cycle. Hoa's
conjecture holds through order 12, so the least counterexample order is in [13, 56]; A185306(11) = 67 and
A185306(12) = 151 (new terms); no witness for Zhan's Questions 2-3; f(n) = 1 for 4 <= n <= 12. EXP-003: no
Zhan-type counterexample from gadgets of order <= 12; any Zhan-type counterexample has order >= 32.

## 2. The objects table

| Object | Definition / authority |
|---|---|
| MNH graph | non-Hamiltonian; every nonedge creates a Hamilton cycle; equivalently every nonadjacent pair is joined by a Hamilton path |
| residual | G - V(C) for a longest cycle C (Hoa's "restgraph") |
| Hoa's conjecture | every residual of every MNH graph is complete; false for n >= 56 (Zhan) |
| Zhan's Q2, Q3, Q4 | every residual component complete?; a connected non-complete residual?; f(n) = max number of residual components |
| degree-sum tightness | in an MNH graph every nonadjacent pair has d(u) + d(v) <= n - 1 (Bondy-Chvatal closure) |
| A185306 | number of MNH graphs on n vertices: 0, 1, 1, 1, 3, 3, 7, 9, 18, 31 (n = 1..10); 67 at n = 11 (EXP-001); 151 at n = 12 (EXP-002) |
| dossier | [2026-09-02 dossier](../../problems/combinatorics/petersen-coloring/context/scouting-2026-09/2026-09-02-dossier-hoa-mnh.md) |

## 3. Experiment index

| Experiment | Question | Verdict | Load-bearing result |
|---|---|---|---|
| EXP-001-mnh-census | MNH graphs and every longest-cycle residual to order 11-12 | CONFIRMED to order 11 | Hoa holds for n <= 11; A185306(11) = 67; no Q2/Q3 witness; f(n) = 1 for 4 <= n <= 11 |
| EXP-002-order-12 | Order 12 by the maximum-degree split | CONFIRMED | A185306(12) = 151; Hoa holds at order 12; n_0 in [13, 56] |
| EXP-003-gadget-search | Zhan-type counterexamples from census gadgets | CONFIRMED (none) | 2,796 gadgets of order <= 12, all with clique omitted sets; any Zhan-type counterexample has order >= 32 |

## 4. In flight

EXP-001, EXP-002 and EXP-003 complete (2026-11-07). Nothing running.

## 5. Next actions

1. HMB-006: order 13 needs a structured generator (case A: all graphs on 12 vertices, 1.65 x 10^11, feasible in
   hours; case B, maximum degree <= 9, is the expensive part).
2. HMB-007: a direct construction search for Zhan-type counterexamples between 32 and 55 vertices (a middle
   gadget from an MNH graph of order >= 13 with a non-clique omitted set).
3. HMB-003: Hoa 2005 (World Scientific) still to obtain before any write-up.

## 6. Where everything lives

- Records: `program/hoa-mnh/`; problem tree: `problems/combinatorics/hoa-mnh/`.
- Sources: data root `caos-research/hoa-mnh/sources/` (manifest with SHA-256 in `context/references.md`).
- Generator: nauty geng 2.8.9 built in WSL (`~/caos-nauty/nauty2_8_9/geng`), from the official tarball.

## 7. Gotchas

- A185306 counts K_2 as MNH and K_1 as Hamiltonian; the counts include the connectivity-1 MNH graphs (two cliques
  sharing a vertex), so a biconnected-only generation would undercount.
- Hamiltonicity tests must be exact; no heuristic search may conclude non-Hamiltonicity.
