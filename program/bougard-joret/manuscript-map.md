# Bougard-Joret: result and manuscript map

Updated 2026-11-16. This map separates mathematical evidence, strategic value, manuscript coverage and external novelty (methodology 13). Experiment verdicts remain the authority for proofs and exact checks. It is the first governance record of the programme: the focuses before BJ-F3 are reconstructed from the records (`program/bougard-joret/plan.md`, `RESUME.md`, `backlog.md`, `state.md`, `problems/combinatorics/bougard-joret/history/log.md`, the experiment verdicts and the manuscript metadata), not declared at their admission.

## Status boundary

Bougard and Joret's Conjecture 1 (J. Graph Theory 58 (2008), Section 6) gives a two-line formula for f(n, alpha, k), the minimum number of edges of a k-connected graph of order n and independence number alpha.

- The first line, ceil(n k / 2) in the regime n <= k alpha, is false: Das and Gupta (arXiv:2608.18828v1, 2026-08-19) determine f at n = alpha + k and the smallest counterexample is (7, 3, 4). The discovery is theirs.
- The second line, f = t(n, alpha) + ceil(k alpha / 2) for n > k alpha, has its upper bound from the Bougard-Joret clique construction. Didin (Zenodo 10.5281/zenodo.22831382, preprint of 2026-09-18, submitted to J. Graph Theory and under review) claims the lower bound for every n > k alpha (his Theorem 9). The programme read the statements and did not audit the proof (`context/references.md`).
- Bougard and Joret hold their proved ranges (k at most 2, n = k alpha, the large-order range, alpha = 2 with n >= 2k, and the second line when floor(n / alpha) >= ceil(k alpha / 2) - alpha + 2, their Proposition 8).
- The general first regime (a corrected formula for n <= k alpha) is open.

The CAOS programme does not claim the disproof of the first line and does not claim a proof of the second. It determines the function on the first interior shell n = alpha + k + 1, proves one level of a triangle-free matching conjecture and the exact value f(2d + 3, 2, d + 2) from it, and checks the second line exhaustively at 53 triples with the extremal structure.

Internal exact validation and Zenodo persistence do not establish peer review or worldwide novelty. The searches recorded in `context/references.md` and `history/log.md` (2026-09-05, 2026-10-30, 2026-11-07, 2026-11-11) found no overlap with the results below beyond what is stated in the table, with every statement marked [U] as to exhaustive priority; specialist confirmation is still required. Nothing here is expert or peer reviewed except through the programme's own independent reviews recorded in the history log.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Adjacent tree strip: f(2k, k-1, k) = k^2 for every k >= 3, all extremal graphs on a nonstar tree with fibers | EXP-001 | proved [D] (uniform proof, adversarial audit, 86 nonstar tree controls, order-six census) | first exact value above Das and Gupta's boundary | `tree-strip` |
| Full first interior shell: f(alpha + k + 1, alpha, k) = ceil(k (alpha + k + 1) / 2) for k >= 3, 2 <= alpha <= k + 1; alpha = 2 extremizers are the complements of disjoint cycles of length at least five | EXP-002 | proved [D]; 75 constructions, 45 direct checks and the order-six census pass [MV]; other extremizers not classified | the shell value; the alpha = 2 structure | `tree-strip` |
| Next matching level: T(d, d + 1) = d^2 + d + 2 for every d >= 7, T(13, 14) = 184 | EXP-003 | proved [D] (uniform upper bound; the attaining graph is Banak, Ekim and Taskin's); 48 graphs and 287,564 five-type candidates [MV] | one level of the Ahanjideh-Ekim-Yildiz conjecture; the full conjecture is open | `next-matching` |
| Exact Bougard-Joret value f(2d + 3, 2, d + 2) = d^2 + 4d + 2 for every d >= 7 | EXP-004 | proved [D], independent audit PASS; configuration-split satisfiability at d = 7 (8 of 8) and d = 8 (7 of 8, the eighth excluded by an identity); the global search planned in the hypothesis did not finish | the first line fails by floor(d / 2) - 1 at these parameters | `next-matching` |
| Second line at the open window to order 22: 39 triples equal t(n, alpha) + ceil(k alpha / 2) | EXP-005, EXP-006, EXP-007 | exact enumeration with an independence-pruned generator and an exact filter [MV]; finite only | independent check of Didin's claimed lower bound | `second-regime` |
| Second line at orders 23 and 24: 14 more triples, the order-24 closure at (24, 7, 3) = 41 and (24, 3, 7) = 95 | EXP-008, EXP-009, EXP-010 | exact enumeration [MV]; 53 of 53 open-window triples with n <= 24 hold; seven pairs (alpha, k) settled for every n | as above; closes the window for those pairs | `second-regime` |
| Extremal graphs at 35 triples: 246 graphs, 206 with the Bougard-Joret structure, 40 with no partition into alpha cliques (clique cover number alpha + 1; all at k = 3, alpha odd) | EXP-011 | measured [MV], rechecked by independent implementations; the frozen prediction that every extremal graph splits into alpha cliques is refuted | a proof of the second line through a clique partition cannot reach the conjectured size | `second-regime` |
| Pipeline validation at the production parameters (Gates A to F, 0 disagreements) | EXP-012 | confirmed [MV]; 19 of the 33 Gate B slices are empty (stated in the verdict and the paper) | the soundness of the search behind EXP-005 to EXP-011 | research record, reported in `second-regime` |
| Odd-alpha construction: blocks X6 and X7 on a 3-edge-connected cubic quotient give extremal graphs without a clique partition for every odd alpha and 3 alpha < n <= 4 alpha - 1 | EXP-013 | proved [D] with finite checks; extremal at (22..24, 7, 3), and everywhere if Didin's Theorem 9 holds | explicit graphs outside the Bougard-Joret structure | `second-regime` |
| Block characterisation: for alpha >= 3, the extremal graphs without a clique partition are exactly the X6/X7 construction graphs and the 8 graphs at (10, 3, 3) | EXP-014 | proved [D], conditional on Didin's Theorem 3; exhaustive check over all graphs on 5 to 7 vertices | closes the structure question BJB-026 under that premise | `second-regime` |

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `tree-strip` | v0.05 | [10.5281/zenodo.24232301](https://doi.org/10.5281/zenodo.24232301) | [10.5281/zenodo.22315251](https://doi.org/10.5281/zenodo.22315251) | what is f(n, alpha, k) on the first interior shell n = alpha + k + 1, and who are the extremal graphs at alpha = 2 and alpha = k - 1 |
| `next-matching` | v0.05 | [10.5281/zenodo.24232146](https://doi.org/10.5281/zenodo.24232146) | [10.5281/zenodo.22343021](https://doi.org/10.5281/zenodo.22343021) | what is the maximum size of a triangle-free graph with bounded degree and matching number d + 1, and what exact Bougard-Joret value follows |
| `second-regime` | v0.04 | [10.5281/zenodo.24231735](https://doi.org/10.5281/zenodo.24231735) | [10.5281/zenodo.24044537](https://doi.org/10.5281/zenodo.24044537) | does the second line hold at the small open orders, and which graphs attain it |

Split decision (recorded from the programme's own practice, 2026-11-16): the three papers have different central questions and proof toolkits (a degree-sum and cyclic-gap argument for the shell; shortest odd cycles, five-type equality exclusion and the Tutte-Berge formula for the matching level; exhaustive enumeration with a validated pipeline and a block reduction for the second regime), so they stay separate. `tree-strip` v0.02 absorbed the shell; `next-matching` was created as its own paper on 2026-09-05 (plan-2026-09-05-triangle-free.md, step 3) and `second-regime` as its own note on 2026-11-07. Published versions are immutable; no merge of the papers is proposed. UNVERIFIED: this split decision was not stated as such in the records; it is the reading of the plans and the three metadata files, for Felipe to confirm at the review.

## Focus record

- Closed: BJ-F1 (tree strip and the first interior shell, EXP-001 and EXP-002, success gate met 2026-09-05); BJ-F2 (the next matching level and the exact value at (2d + 3, 2, d + 2), EXP-003 and EXP-004, met 2026-11-04). Both are reconstructed from the records.
- Current: **BJ-F3**, the second regime n > k alpha at small orders with the extremal structure (EXP-005 to EXP-014; status active-success-gate-met). Its success gate is met (53 of 53 triples to order 24, 246 extremal graphs, the odd-alpha construction, the conditional characterisation; second-regime v0.04, 2026-11-14), and it stays current until the strategic review with Felipe chooses the next focus (methodology 13: the changed target is shown to him first).
- Proposed, shown to Felipe before any work, in the order given by the coordinating session from the open backlog rows:
  1. BJ-F4 (BJB-015): extend the triangle-free matching upper bound beyond the solved level m = d + 1.
  2. BJ-F5 (BJB-009): classify the first-shell extremizers beyond alpha = 2 and the tree strip.
  3. BJ-F6 (BJB-006): when different maximum independent sets give different tree representations.
  The stop conditions and first bounded actions of the three proposed focuses are the drafter's proposals under methodology 13 and `wiki/05-open-questions.md`, not decisions of the records; they are marked as such in the governance record and are for Felipe's review. Which matching level BJ-F4 targets first is not in the records.
- Deferred in the records and not proposed here: BJB-010 (second-shell search, superseded by EXP-003), BJB-007 (the unsplittable-flow reconciliation, owned by another programme).

## Open obligations

- `tree-strip`: the classification of the shell extremizers beyond alpha = 2 and alpha = k - 1 (BJ-F5) and the count of unmarked isomorphism classes (BJ-F6) are open; the paper does not claim them.
- `next-matching`: the full Ahanjideh-Ekim-Yildiz conjecture and the other matching levels (BJ-F4) are open; no claim beyond m = d + 1.
- `second-regime`: the second line is not proved here; the lower bound for every n > k alpha rests on Didin's claimed proof, whose correctness is not audited by this programme, and the characterisation of the extremal graphs without a clique partition is conditional on his Theorem 3. The two statements v0.01 and v0.02 made about the line being open outside the proved range were corrected in v0.03.
- The general first regime n <= k alpha (a corrected formula) is open and has no focus.
- Global record: each manuscript's README has been drafted to carry the current-version line and version DOI the governance checker reads; the next-matching `metadata.md` still shows v0.04 as current and is stale against v0.05 (`zenodo.json`, `publication-gate.json`, `main.tex`).
