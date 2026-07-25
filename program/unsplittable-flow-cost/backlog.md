# Unsplittable-flow cost conjecture - problem backlog

Ids are per problem (UFB-NNN). Phases per `plan.md` (UF-P0..UF-P5).

| id | title | phase | status | updated | notes |
|---|---|---|---|---|---|
| UFB-001 | EXP-001 calibration: the exact instance checker (feasibility, own path enumeration, all routings, congestion/cost decisions, per-arc violations, alpha_inst), validated on hand-built instances with known answers | UF-P0 | doing | 2026-07-24 | hypothesis before run; the toolchain shakedown; exact arithmetic only |
| UFB-002 | Direct read of DGG99 (Combinatorica 19(1) 1999, 10.1007/s004930050043): the theorem AND the augmentation / alternating-cycle proof technique | UF-P0 | todo | 2026-07-24 | paywalled; needed before any claim about why the argument is not cost-augmentable |
| UFB-003 | Direct read of Martens-Salazar-Skutella (ESA 2007): the equivalence of the cost form and the convex-combination form | UF-P1 | todo | 2026-07-24 | load-bearing for the corollary cascade; the easy direction is already re-derived by us |
| UFB-004 | EXP-002 adjudication: decide the 2026 claimed counterexample with our own checker; full C1-C9 battery and Q1-Q9 quantities | UF-P1 | todo | 2026-07-24 | declared before run; verdict honours the machine either way |
| UFB-005 | Direct reads of Sku02 and MS22 (the two proved special cases and the two conjectures) from primary sources | UF-P1 | todo | 2026-07-24 | currently [UNVERIFIED], reported via STVZ25 and MSW25 |
| UFB-010 | Separation LP instrument: re-derive the "exists a nonnegative cost vector making this instance a counterexample iff max delta > 0" reduction ourselves, and implement it in EXACT rational arithmetic (no float simplex) | UF-P2 | todo | 2026-07-24 | the engine that removes the cost vector from every search |
| UFB-011 | Canonical-form / isomorphism reduction for instance enumeration (digraph isomorphism plus demand-preserving terminal relabelling), with an exact completeness argument | UF-P2 | todo | 2026-07-24 | without this the exhaustion claim is not honest |
| UFB-012 | EXP-class: exhaustive small-instance search for minimality (smallest counterexample in vertices, arcs, terminals, d_max) | UF-P2 | todo | 2026-07-24 | novel target; needs UFB-010 and UFB-011 |
| UFB-020 | Odd-cycle conflict families: generalise the conflict triangle to longer odd cycles; can the flow structure realise the larger stable-set gap under the d_max budget? | UF-P3 | todo | 2026-07-24 | lens 2 and 4; the route to a larger forced alpha |
| UFB-021 | Clique conflict families: the extreme of the stable-set gap; almost certainly obstructed by flow structure, and the obstruction itself would be a theorem | UF-P3 | todo | 2026-07-24 | lens 4 |
| UFB-022 | Exact series-parallel recogniser and K4-subdivision detector, validated on known SP and non-SP digraphs | UF-P1/P3 | todo | 2026-07-24 | needed for consistency test C2 and the class-boundary statement |
| UFB-023 | Conflict-graph invariant instrument: build H, compute the fractional selection vector rho, test rho against stable-set (odd-cycle) inequalities; use as the cheap pre-filter before any LP | UF-P2/P3 | todo | 2026-07-24 | lens 4, invariant-first; the exploration-moment output of round 1 |
| UFB-024 | Verify or refute the proposer transcript's no-go claims (two-backbone prefix networks; three tracks cannot enforce a permutation; unequal demands indispensable; costs must be spread over the fractional support), one experiment per claim | UF-P2 | todo | 2026-07-24 | lens 6; they become search pruning rules only once verified |
| UFB-025 | Prove and machine-check the first minimality rung: no counterexample with at most 2 terminals (the conflict graph has no odd cycle) | UF-P2 | todo | 2026-07-24 | lens 8; cheap, and the base case of the minimality ladder |
| UFB-030 | The alpha frontier: compute alpha_inst for the certificate's parametric family symbolically, and find its supremum over valid parameters | UF-P3 | todo | 2026-07-24 | the quantitative frontier; the real open problem after a refutation |
| UFB-031 | The dual budget beta and the trade-off curve: at violation exactly d_max, the best achievable cost factor; parametric separation LP | UF-P3 | todo | 2026-07-24 | |
| UFB-040 | Conj 1.3 hunt (cost-free, two-sided, acyclic) with the same exhaustive engine; it survives a cost refutation and by STVZ25 Thm 1.6 implies a 2 d_max cost statement | UF-P4 | todo | 2026-07-24 | a counterexample here would be strictly bigger than the cost refutation |
| UFB-050 | Wiki 01-05 plus theme-aware SVGs (instance, conflict triangle, convex-hull separation, class boundary); web page gated on published state | UF-P5 | todo | 2026-07-24 | vertical, per unit, transcribed from verdicts |
| UFB-051 | Manuscript per methodology/09 once validated plus novel material exists; honest [MV]/[D]/[C] labelling; external framing gated on Felipe | UF-P5 | todo | 2026-07-24 | |
| UFB-060 | Standing literature re-search every round (this area is active; a preprint or an authors' response may appear at any time); read primary, never coverage | rolling | todo | 2026-07-24 | methodology/10 lens 11, methodology/11 item 1 |
