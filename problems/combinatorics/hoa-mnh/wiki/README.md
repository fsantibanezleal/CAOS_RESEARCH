# Hoa's conjecture on maximal non-Hamiltonian graphs

A graph is maximal non-Hamiltonian (MNH) if it has no Hamilton cycle but adding any missing edge creates one.
Hoa (1994) conjectured that removing the vertices of any longest cycle of an MNH graph leaves a complete graph.
Zhan (2026) disproved this for every order from 56 on, with residual two isolated vertices, and asked whether the
residual components must be complete (Question 2), whether a connected non-complete residual exists (Question 3)
and how many components a residual can have (Question 4).

Status of this program: opened 2026-11-06. Records: [RESUME](../../../../program/hoa-mnh/RESUME.md),
[plan](../../../../program/hoa-mnh/plan.md), [sources](../context/references.md). The first experiment is an exact
census of MNH graphs by order, with every longest cycle.

EXP-001 (2026-11-06): every MNH graph of order at most 11 is classified. Hoa's conjecture holds through order 11, so the least counterexample lies between 12 and 56 vertices. There are 67 MNH graphs on 11 vertices (a new term of OEIS A185306). Every longest cycle of every one of them leaves a single complete graph, so Zhan's Questions 2 and 3 have no small witness and his f(n) equals 1 up to n = 11. [Verdict](../experiments/EXP-001-mnh-census/verdict.md).

EXP-002 (2026-11-07) adds order 12: 151 MNH graphs, again with no counterexample, so the least counterexample has between 13 and 56 vertices. EXP-003 shows that none of the 2,796 small "gadgets" Zhan's construction would need works, so any counterexample of Zhan's type has at least 32 vertices. [EXP-002](../experiments/EXP-002-order-12/verdict.md), [EXP-003](../experiments/EXP-003-gadget-search/verdict.md).
