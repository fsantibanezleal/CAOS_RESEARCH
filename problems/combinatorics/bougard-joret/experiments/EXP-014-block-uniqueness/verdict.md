# EXP-014 verdict: CONFIRMED (P1, P2, P3); BJB-026 settled conditional on Didin's Theorem 3

Date: 2026-11-14. Hypothesis frozen in ed56cfa7 before any computation.

## Result

- [MV] `check_blocks.py` (NetworkX 3.4.1, `artifacts/run-output.txt`, `artifacts/check-blocks.json`):
  - the graph atlas has 34, 156 and 1,044 graphs on 5, 6 and 7 vertices, equal to OEIS A000088;
  - of the 1,234 graphs, 178 pass C1 (order and size), 3 pass C2 (connected, independence number 2, every edge
    critical) and C3 (clique cover number at least 3);
  - 39 pairs (X, A) pass C4 (degrees) and 18 pass C5 (every component of X - T meets A \ T for |T| <= 2);
  - the 18 form exactly four isomorphism classes of marked graphs: X6 with A in the orbit of {0, 1, 5} (2 subsets),
    and X7 with A in the orbits of {1, 2, 6} (4), {1, 2, 3} (4) and {0, 1, 2} (8);
  - independence and clique cover numbers by two methods each: 0 disagreements.
- P1 (no block on 5 vertices): holds. P2 (6 vertices: X6 at the orbit of {0, 1, 5}): holds. P3 (7 vertices: X7 at
  the three observed orbits): holds. No observed triple is missing.
- [D] `proof.md` turns this into a theorem, conditional on Didin's Theorem 3: every 3-connected extremal graph of
  case (a) of Proposition prop:where is a graph of Theorem thm:construction, with X in {X6, X7} at an observed triple,
  clique parts of orders 3 and 4 as in T(n, alpha) with two cliques removed, and the edges between parts a matching
  along a 3-edge-connected loopless cubic quotient. Conversely every such graph has the properties of
  thm:construction, and is extremal for n <= 24 (enumeration) and for every n if Didin's Theorem 9 holds.

## Reading

- The reduction needs Didin's Theorem 3 twice: once in prop:where, whose equalities give the three edges per part and
  G[V_i] = H[V_i], and once on the block X, where equality forces e(X) = t(|X| + 1, 2) - 1 and all clique orders into
  {3, 4}. All four structural claims the v0.03 note lists as open (clique orders, matching, block, attaching triples)
  therefore rest on it: given those equalities and the clique orders, the matching and the 3-edge-connected quotient
  follow from 3-connectivity.
- Correction (2026-11-14, while writing the note's section): the frozen hypothesis says that "three-connectivity
  adds, without Didin" the attachment facts. That overstates it: the three edges per part come from the equalities of
  prop:where(a), which use Didin's Theorem 3, and a part could be a single vertex until the clique orders (Didin again)
  are known. proof.md has the right order (Step 3 before Step 4) and its theorem is stated as conditional.
- With prop:where(b) and the complete enumeration of its six triples (EXP-011), BJB-026 is settled conditional on
  Didin's Theorem 3: the extremal graphs without a partition into alpha cliques are exactly the construction graphs and
  the 8 graphs at (10,3,3).
- Next: the result belongs in the next version of the second-regime note (v0.04), with the proof, after an independent
  review of `proof.md`.
