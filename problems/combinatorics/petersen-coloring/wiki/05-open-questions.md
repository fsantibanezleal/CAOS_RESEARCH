# 05 - Open questions and our nulls

Sources: GJMMM Section 5; EXP-005 and EXP-006 verdicts; `program/petersen-coloring/research-lines-2026-09-03.md`.

## Open in the literature (as of 2026-09-03)

1. The smallest counterexample: order in $[38, 52]$ (GJMMM Problem 7). Not attacked head-on
   here; see the composition classes below.
2. Cyclically 5-edge-connected counterexamples (GJMMM Problem 5): open.
3. Normal 6-edge-colorings of every bridgeless cubic graph (GJMMM Conjecture 6, attributed to
   Samal): open in general; true on the three counterexamples (EXP-004).
4. Whether the Berge-Fulkerson, Berge, Fan-Raspaud and 5-cycle double cover conjectures hold in
   general: open; all true on the three counterexamples (EXP-002, EXP-003).

## Our exact results that sharpen the picture

- Every counterexample has Petersen defect at least 2 (parity theorem, `[D]`), and the three
  known ones have defect exactly 2 (EXP-006 `[MV]`); for all three, every pair of vertices is
  critical (universal 2-criticality), a property without a proof yet.
- No counterexample consists only of copies of the pole $F$ (Proposition, `[D]`, `[MV]`).
- Perfect matching index 4 on all three; oddness 4 on the 112-vertex graphs versus 2 on the
  52-vertex graph (EXP-002, EXP-003).

## Our nulls and budget stops (honest record)

- Composition classes $\mathcal C(k, m)$ (k copies of $F$, m free vertices) below 52 vertices:
  $(5,0)$ and $(6,0)$ exhausted (universal coloring); $(3,2)$ control, $(5,2)$ and $(6,2)$ did not
  converge under counterexample-guided search within budget (EXP-005): the outer loop needs symmetry
  breaking or a QBF formulation (research line PCR-4b, PCR-4c). No claim is made for the
  unexhausted classes.
- Normal-5 defect: at least 1 on all three (EXP-001); the cardinality-encoded bound-1 instances
  hit the 30-minute cap (EXP-004); the designated-edge sweep of the 52-vertex graph is the exact
  route (EXP-006 addendum 2).
- The 68-vertex counterexample announced on X was not retrievable and is not covered.

## Declared next lines

PCR-1 (perfect matching index along the infinite families), PCR-2 (oddness along the families),
PCR-3 (critical-pair structure), PCR-4b/4c (convergent composition search), PCR-5 (cyclic
5-connectivity via rigid 5-poles).
