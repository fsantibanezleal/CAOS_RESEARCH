# EXP-003 verdict: no Zhan-type counterexample from gadgets of order at most 11

Date: 2026-11-06. Status: **CONFIRMED [MV]** (the prediction held). Hypothesis committed before computation
(c25531a4).

## Result

Every gadget (X, x) with X an MNH graph of order 4 to 11 (the complete EXP-001 census) and x a vertex with
G = X - x connected, not complete and N(x) != V(G): **1,158 gadgets**. All are traceable. Their middle
deficiencies d (|G| minus the order of a longest path of G between two distinct neighbours of x) are

| d | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gadgets | 920 | 131 | 47 | 25 | 19 | 9 | 5 | 2 |

**In every one of the 1,158 gadgets, every longest middle path omits a clique.** By the mechanism in the
hypothesis (Bullock et al. Theorem 3.13 with Zhan's Lemma 5), the residual of a longest cycle of K_1 join M is
the omitted set of a middle gadget, so no triple of these gadgets gives a counterexample to Hoa's conjecture,
whatever the order. A Zhan-type counterexample needs a middle gadget from an MNH graph of order at least 12.

391 of the gadgets also satisfy condition (v) (traceable from every universal vertex of G[N]); this does not
affect the conclusion, since no gadget at all can serve as the middle.

## Validation

- **Two methods:** every invariant was computed by subset dynamic programming and, independently, by plain
  backtracking; they agree on all 1,158 gadgets.
- **Known-answer gate** (`gate_zhan.py`): on Zhan's own gadget (A_18 with vertex 18, order 18, outside the
  census) the same code finds N(18) = {1, 8, 15}, B_17 homogeneously traceable, d = 2 and a non-clique omitted
  set ({16, 17}, nonadjacent), exactly as Zhan's Lemmas 2 and 6 state. The code detects a valid middle gadget
  when one exists.

## Scope

The conclusion concerns this one mechanism (three-gadget gluing through a 2-cut, then a universal vertex). It
says nothing about counterexamples of other shapes; EXP-001 and EXP-002 cover all shapes up to their orders.
When the order-12 census (EXP-002) is complete, its gadgets are the next input.
