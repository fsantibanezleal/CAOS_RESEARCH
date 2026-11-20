# Hoa's conjecture on maximal non-Hamiltonian graphs: result and manuscript map

Updated 2026-11-19. This map separates mathematical evidence, strategic value, manuscript coverage and external novelty
(methodology 13). Experiment verdicts remain the authority for every count and bound.

## Status boundary

Hoa's conjecture (posed as a question by Vu Dinh Hoa, Problem 266, Discrete Math. 164 (1997); called a conjecture by Zhan)
is already false: X. Zhan (arXiv:2608.00957v3, 2026-08-14) gives counterexamples of every order n >= 56, with residual 2K_1,
toughness 1 and circumference n - 2, and poses Questions 2 to 4. Priority belongs to Zhan. Hoa proved the conjecture for
toughness below 1 and for minimum degree at least n/3 (as reported by Zhan). The CAOS program contributes exact census
counts, the verification of the conjecture on bounded orders, and bounds on where a counterexample of Zhan's type can
occur; it does not claim the disproof and has found no counterexample below 56.

Internal exact validation does not establish peer review or worldwide novelty. The searches of 2026-11-06 (arXiv, newest
first, no follow-up to Zhan) and the portfolio review of 2026-11-19 (nothing new) are recorded in
`problems/combinatorics/hoa-mnh/context/references.md`; no negative search is a novelty proof. Moulton's 2014 list (MNH
graphs to order 20) was not located and Hoa 2005 was not obtained, so the new OEIS terms below are unconfirmed against them.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Census of MNH graphs to order 12 with every longest cycle: A185306(11) = 67, A185306(12) = 151 (new terms; 31 at order 10 reproduced) | EXP-001, EXP-002 | confirmed, with independent re-checks (0 disagreements) | extends a sequence stuck at order 10 since 2013 | none yet (HM-F2); research record |
| Hoa's conjecture holds for every MNH graph of order at most 12, so the least counterexample order is in [13, 56] | EXP-001, EXP-002 | confirmed on the computed range | raises the lower bound on the least counterexample order | none yet (HM-F2); research record |
| Zhan's Questions 2 and 3 have no witness through order 12; f(n) = 1 for 4 <= n <= 12 | EXP-001, EXP-002 | decided on the range | answers Zhan's questions on bounded orders | none yet (HM-F2); research record |
| Gadget bounds: no Zhan-type middle gadget from the 2,796 gadgets of order at most 12; any three-gadget counterexample has order at least 32 | EXP-003 | confirmed; the bound concerns this mechanism only (other shapes are bounded by the census, order at least 13) | locates where a counterexample below 56 can occur | none yet (HM-F2); research record |
| Order 13, case A (a universal vertex): exactly 286 MNH graphs, all satisfying Hoa's conjecture (1,100,439,010 graphs read, 2,000 parts) | EXP-004, EXP-006, EXP-007 | complete after two partial runs (17.6 percent, 82.7 percent), independently verified | order 13 settled for Hoa except case B | none yet; research record |
| Order 13, platypus route for case B | EXP-005 | stopped at the budget projection (gates at orders 10 and 11 pass) | negative result on this route | research record |
| No middle gadget among the 3,304 gadgets of the 286 order-13 graphs | EXP-008 | confirmed, independently verified | a Zhan-type middle needs order-13 case B or order at least 14 | none yet; research record |
| Order 13, case B (maximum degree at most 9) | none | open: needs an MNH-restricted generator (HMB-006) | decides order 13 and the next input of the gadget mechanism | open obligation |

## Manuscripts

None. No manuscript of this problem exists (`manuscripts/hoa-mnh/` is absent and the global manuscript index lists none);
whether the census results justify one is the proposed focus HM-F2, to be decided at the next review. `manuscripts` is an
empty list in `research-governance.json`.

## Focus record

- Closed: HM-F0, the exact census of MNH graphs with every longest cycle to order 12 (EXP-001, EXP-002; success gate met
  2026-11-07).
- Current: **HM-F1**, the least order of a counterexample to Hoa's conjecture: order 13 and counterexamples of Zhan's type
  below 56 (EXP-003 to EXP-008); next bounded action the order-13 case of maximum degree at most 9 (portfolio review of
  2026-11-19, rank 6, decision 5).
- Proposed: HM-F2, a manuscript for the census results (the new terms at orders 11 and 12, Hoa's conjecture through order
  12, the gadget bounds), to be decided at the next review.

## Open obligations

- HMB-006: order 13 case B (maximum degree at most 9) needs an MNH-restricted generator; the sizing probe estimates about
  10^12 graphs and 30 to 65 hours on 30 cores (an estimate, not a measurement).
- HMB-007: the direct construction search for Zhan-type counterexamples of order 32 to 55 continues with order-13 case B or
  order at least 14.
- HMB-003: obtain Hoa 2005 (World Scientific, pp. 67-70) before any write-up.
- HMB-004: ask for or locate Moulton's 2014 list.
