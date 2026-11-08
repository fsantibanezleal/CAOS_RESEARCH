# EXP-004 preflight: order 13, the maximal non-Hamiltonian graphs with a universal vertex (HMB-006, case A)

Date: 2026-11-07. Status: frozen before any production computation. CPU only.

## Question

Which maximal non-Hamiltonian (MNH) graphs of order 13 have a vertex of degree 12, and does Hoa's conjecture
(every longest cycle C leaves G - V(C) complete) hold for them? This is case A of the maximum-degree split used at
order 12 (EXP-002; Goedgebeur-Neyt-Zamfirescu Corollary 12: an MNH graph has Delta = n - 1 or Delta <= n - 4).
Case B (Delta <= 9) is sized at about 10^12 graphs and is not part of this experiment.

## Method

Case A graphs are G = K_1 join H with H on 12 vertices. A pruned generator lists H: geng with a PRUNE hook that
discards a partial graph with a nonadjacent pair of degree sum above maxn - 2. Soundness [D]: in an MNH graph every
nonadjacent pair has degree sum at most n - 1 (Bondy-Chvatal: otherwise adding the edge would not change
Hamiltonicity); in G = K_1 join H, deg_G = deg_H + 1 on H, so deg_H(u) + deg_H(v) <= n - 3 = 12 - 2; geng only adds
vertices, edges among existing vertices never change and degrees only grow, so a violating pair stays violating.
Each H goes through `join6` (adds the universal vertex) and EXP-001's `mnh` filter (exact Hamiltonicity tests,
every longest-cycle vertex set, residual completeness), split into disjoint res/mod parts.

## Gates (before production)

1. The pruned generator plus join6 plus mnh reproduces the case-A counts of EXP-002's split at orders 10, 11 and 12:
   27, 57 and 114.
2. EXP-001's independent `verify.py` re-checks every order-13 graph found (non-Hamiltonian, every nonadjacent pair
   joined by a Hamilton path, residual flags).

## Predictions

- The number of order-13 MNH graphs with a universal vertex lies between 180 and 320 (the case-A counts double
  roughly per order: 27, 57, 114) (MODERATE).
- None is a counterexample to Hoa's conjecture (HIGH).

## Budget

At most 6 hours on up to 6 processes (shared with JCB-103's runs).
