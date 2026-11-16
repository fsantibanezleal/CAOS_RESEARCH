# EXP-008 - Middle gadgets from the order-13 MNH graphs with a universal vertex (HMB-007, step 1)

Date: 2026-11-15. Frozen before any computation of this experiment. CPU only.

## Why

EXP-003 (with its order-12 addendum) showed that no gadget from an MNH graph of order at most 12 can be the middle of a
Zhan-type counterexample (every longest middle path omits a clique), so such a counterexample needs a middle gadget from
an MNH graph of order at least 13, and has order at least 32. EXP-004, EXP-006 and EXP-007 enumerated every MNH graph of
order 13 with a universal vertex: 286 graphs (`experiments/EXP-007-order-13-universal-last/artifacts/mnh-n13-caseA.txt`,
graph6 with annotations). Their gadgets are the first order-13 input to the mechanism. The MNH graphs of order 13 without
a universal vertex (case B, HMB-006) are not known and are outside this experiment.

## Mechanism

Exactly EXP-003's (`experiments/EXP-003-gadget-search/hypothesis.md`, sections "Mechanism" and "Question"): Bullock et al.
Theorem 3.13 with Zhan's Lemma 5; a gadget is (X, x) with G = X - x connected, not complete and N_X(x) != V(G); its
invariants are traceable, homogeneously traceable, the universal vertices of G[N] and traceability from each, d, and
whether some longest (p, q)-path (p != q in N) omits a non-clique set. The triple search admits a middle gadget with a
non-clique omitted set and two end gadgets with d at least the middle's, under conditions (iii) to (v).

## Questions and predictions

- **Q1.** Does any gadget (X, x) with X among the 286 graphs have a longest middle path omitting a non-clique set?
  Prediction: no (confidence MODERATE, 0.7): every such G contains the universal vertex of X (x is not universal, since
  N_X(x) != V(G)), which tends to keep omitted sets small and complete; EXP-003 found none up to order 12.
- **Q2.** If Q1 finds such middle gadgets: the triple search over end gadgets from the whole census (orders 4 to 12, the
  EXP-003 inputs) and the order-13 gadgets, with the least order 3 + sum |G_i| reached. Every candidate is built and
  verified directly as in EXP-003's "Validation" (K_1 join M non-Hamiltonian, every nonadjacent pair joined by a Hamilton
  path, the cycle length, no longer cycle, the residual not complete) before anything is claimed; a verified one is a
  counterexample to Hoa's conjecture of that order (below 56 if the order is below 56).

## Validation

- Gate 1: `gate_zhan.py` (Zhan's own gadget A_18, the known answer) passes with the same code.
- Gate 2: rerunning the gadget computation on the order-12 census reproduces `artifacts/gadgets-to12.json` of EXP-003
  (same gadget count, 2,796, and the same invariants).
- Every order-13 gadget's invariants by the two methods of EXP-003 (subset dynamic programming and backtracking), which
  must agree.
- Input check: the 286 graphs are decoded, of order 13, pairwise non-isomorphic, each with a universal vertex, and MNH
  (non-Hamiltonian, every non-edge closes a Hamilton cycle), rechecked here.

## Budget

Two hours of wall time, at most 4 processes.

## What follows

Q1 negative: the middle of a Zhan-type counterexample needs an order-13 MNH graph without a universal vertex (case B)
or order at least 14, and the next input is case B. Q1 positive and Q2 verified: a counterexample below order 56.
