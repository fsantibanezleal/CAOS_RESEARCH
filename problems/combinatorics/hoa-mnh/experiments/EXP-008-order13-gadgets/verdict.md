# EXP-008 verdict: no middle gadget from the order-13 MNH graphs with a universal vertex

Date: 2026-11-15. Status: **CONFIRMED [MV]** (the prediction held: Q1 is negative). Hypothesis committed before any
computation (915f6bee). CPU only, deterministic, no randomness.

## Result

Q1: every gadget (X, x) with X among the 286 order-13 MNH graphs with a universal vertex
(`EXP-007-order-13-universal-last/artifacts/mnh-n13-caseA.txt`) and x a vertex with G = X - x connected, not
complete, N_X(x) != V(G) (and |N| >= 2, as in EXP-003's code; this removes no gadget of the 286 graphs): **3,304 gadgets**, all of order 12, from all 286
graphs. All are traceable. **In none of them does any longest middle path omit a non-clique set** (the flag
`nonclique_omit` is false on all 3,304; `artifacts/gadgets-n13.json`). Q2 is therefore not triggered
(`artifacts/triples-n13.json`: `q1_positive` false), and no Zhan-type counterexample is claimed.

| Prediction | Outcome | Evidence |
|---|---|---|
| Q1: no order-13 gadget has a longest middle path omitting a non-clique set (confidence 0.7) | held | 3,304 gadgets, 0 with a non-clique omitted set (`artifacts/gadgets-n13.json`, `run-log.txt`) |
| Q2: triple search and direct verification, only if Q1 is positive | not triggered | `artifacts/triples-n13.json` |
| Gate 1: Zhan's A_18 passes with the same code | held | `artifacts/gates.json`: d = 2, non-clique omitted set, N(18) = {1, 8, 15} |
| Gate 2: the order-12 gadget artifact of EXP-003 is reproduced (2,796 gadgets, same invariants) | held | `artifacts/gates.json`: records identical to `gadgets-to12.json`, by plain backtracking and by the order-13 method |
| Two methods agree on every order-13 gadget | held, with a deviation from hypothesis.md:38 | DP vs transposition-table backtracking on all 3,304 (0 disagreements); EXP-003 plain backtracking on the 3,071 gadgets with at most 40 edges (0 mismatches, `triples-n13.json` `plain_cross_checked`); the 233 others lack the pre-registered plain check; an independent recomputation (CAOS_MANAGE `wip/caos-research/hoa-exp008-verify-2026-11-16.md`, D1) agrees on all 3,304 |
| Input check: 286 graphs, order 13, pairwise non-isomorphic, universal vertex each, MNH | held | `run-log.txt`, input check line |

The d distribution of the 3,304 order-13 gadgets (d = 12 minus the order of a longest (p, q)-path, p != q in N):

| d | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gadgets | 3031 | 173 | 51 | 15 | 8 | 12 | 5 | 4 | 3 | 2 |

273 gadgets have d >= 2, so d >= 2 is common, but the omitted set is a clique every time, exactly as for orders
4 to 12. 878 gadgets are homogeneously traceable; 878 are traceable from every universal vertex of G[N] (condition (v)).

A structural reading of the data [D, from the table above]: **every one of the 3,304 gadgets has a universal vertex
in G[N]** (the universal vertex of X is adjacent to x and to all of G). By condition (iii) of Bullock et al.
Theorem 3.13 at most one of the three gadgets of a glued graph may have a universal vertex in G[N], so an order-13
gadget from this input could fill at most one slot of a triple; the other two gadgets would come from graphs
without a universal vertex.

## Validation (adversarial record)

- **Gate 1** (`EXP-003/gate_zhan.py`, run unedited as a subprocess): on Zhan's A_18 the same code finds
  N(18) = {1, 8, 15}, B_17 homogeneously traceable, d = 2 and a non-clique omitted set, so the code does detect a
  valid middle gadget when one exists (a positive control for the negative result above).
- **Gate 2**: the gadget computation was rerun on the whole census (orders 4 to 12, EXP-001 and EXP-002 inputs):
  2,796 gadgets, records identical to `EXP-003/artifacts/gadgets-to12.json`, once with EXP-003's own two methods
  (subset dynamic programming and plain backtracking) and once with the order-13 method below; 0 disagreements in
  both.
- **Two methods at order 13, a deviation from the hypothesis (hypothesis.md:38) and from EXP-003.** Plain backtracking
  enumerates every simple path and does not finish on the dense order-13 gadgets (one dense gadget ran past two minutes
  without finishing, and a first full run was abandoned after about 30 minutes of 4 processes). Method 2 at order 13 is
  therefore backtracking over simple paths with a transposition table on (visited set, last vertex)
  (`bt_memo_invariants` in `run.py`), which returns the same quantities (traceable, homogeneously traceable, the start
  set, d, the non-clique flag). Its equivalence with plain backtracking is established on all 2,796 order-12
  gadgets (gate 2) and on the 3,071 of the 3,304 order-13 gadgets with at most 40 edges, run through EXP-003's plain
  `bt_invariants` as well: 0 mismatches. The remaining 233 denser order-13 gadgets are checked by dynamic
  programming against the transposition-table method only (0 disagreements); they have no plain-backtracking check; they include 38 of the 273 gadgets with d >= 2 and all 9 gadgets with d >= 8
  (omitted sets of 8 to 10 vertices).
- **Input check**: the 286 lines are 286 distinct graph6 strings, all decoded to order 13, pairwise non-isomorphic
  (Weisfeiler-Lehman hash filter with an exact networkx isomorphism test on every collision), each with a vertex of
  degree 12, and each MNH (non-Hamiltonian, every non-edge joined by a Hamilton path, by exact subset dynamic
  programming; independent of the EXP-001 to EXP-007 enumeration code).
- **Tests** (`tests/test_hoa_exp008.py`): loader, gadget enumeration against an independent networkx count of
  admissible x, the MNH recheck (positive, Hamiltonian negative, MNH minus an edge negative), the isomorphism filter,
  the verification helpers on C5 and the Petersen graph, DP/backtracking agreement, and memoized against plain
  backtracking on 24 census graphs.
- **Must-refute items**: DP and the transposition-table method agree on all 3,304 order-13 gadgets; DP and plain
  backtracking agree on the 3,071 with at most 40 edges (not refuted); gate 2 reproduces the order-12
  artifact exactly (not refuted); no counterexample was claimed, so none had to pass the direct checks.

## How could this be wrong?

- The result concerns this one mechanism (three gadgets glued through a 2-cut, then a universal vertex) and gadgets
  taken from the 286 graphs with a universal vertex only; it says nothing about MNH graphs of order 13 without a
  universal vertex (case B, HMB-006, unknown) nor about order at least 14.
- The 233 densest gadgets have no plain-backtracking check; their agreement rests on two separately written exact
  searches (dynamic programming and the transposition-table search) that share the gadget construction (decode, adj and
  N in gadgets_of), the complement step and gadgets.is_clique, so they could share a misreading of the definition of
  the omitted set. The independent check is the verification's recomputation (CAOS_MANAGE
  `wip/caos-research/hoa-exp008-verify-2026-11-16.md`, D1: a fixed-start bitmask dynamic program with its own decoding
  and its own clique test), which agrees on all 3,304 gadgets, the 233 included. Gate 1 exercises the DP on Zhan's
  known positive; the transposition-table method is checked on the same positive in
  `tests/test_hoa_exp008.py::test_transposition_table_method_finds_zhans_known_positive`.
- The flag is computed from the omitted sets of longest (p, q)-paths with p != q in N. A gadget with |N| < 2 is not a
  gadget here (EXP-003's code excludes it); such a gadget has no middle path at all.
- Q2 (the triple search with direct verification) was written but never exercised on a positive instance, because Q1
  is negative; its helpers are tested only on small known graphs.
- The mechanism rests on Bullock et al. Theorem 3.13 and Zhan's Lemma 5 as transcribed in EXP-003, not re-derived here.

## What follows

- **HMB-007 step 1**: no order-13 gadget from the universal-vertex graphs can be the middle of a Zhan-type
  counterexample. Together with EXP-003 and its order-12 addendum, a middle gadget must come from an MNH graph of
  order 13 without a universal vertex (case B) or from order at least 14. The order bound 32 of EXP-003's addendum
  is unchanged by this input (it concerns the least middle size, which this experiment does not improve).
- **HMB-006**: case B of order 13 is now the next input for the mechanism, as the hypothesis anticipated; a gadget
  from it needs no universal vertex of X, so its G[N] may or may not have one.
- Nothing here changes Hoa's conjecture: no counterexample is claimed.
