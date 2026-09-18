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

## Round 2 update (2026-09-18)

Sources: `context/2026-09-18-v3-and-h3-dossier.md`, `context/2026-09-18-defect-unbounded.md`,
EXP-007 to EXP-010.

Literature. arXiv:2608.10028v3 (2026-09-11) raises the lower bound of item 1 to 40 (window
$[40, 52]$), adds a second 52-vertex counterexample and counterexamples of every even order at
least 60, and reports for five graphs several invariants that round 1 had computed for three
(Berge-Fulkerson covers, perfect matching index at most 4, 5-cycle double covers, strong normal
6-edge-colorings, colorings with two abnormal edges). The 68-vertex graph is now retrievable
(House of Graphs 57280) and is covered by EXP-008.

New exact results (pages 06 and 07):

- Fiber parity and the unused-vertex reduction for $H$-colorings with an unknown target (Lemmas A
  and B), and the certified list of target orders that do not color the 52-vertex
  counterexamples (EXP-007).
- $\mathrm{pd} \le \mathrm{ab}$; $\mathrm{pd} = \mathrm{ab} = 2$ on all five counterexamples; rings and
  frames with $\mathrm{pd} \ge t$; no sublinear bound on $\mathrm{ab}$ for 2-connected or
  3-connected cubic graphs (statements (c), (d) of Conjecture 3 of Mattiolo, Mazzuoccolo and
  Mkrtchyan are false); the threshold proposition: one cyclically 4-edge-connected cubic graph with
  $\mathrm{pd} \ge 3$ would refute statement (e).

New open questions:

5. Is there a cyclically 4-edge-connected cubic graph with Petersen defect at least 3
   (equivalently, by the threshold proposition and Theorem 4 of Mattiolo et al., would Conjecture 3
   of their paper hold in full)? Every 4-pole $G - e_1 - e_2$ of the two 52-vertex graphs is
   colorable, and adjacent boundary labels are always available at the ends of a deleted edge
   (EXP-010), so the known counterexamples give no such graph by cyclic joining.
6. Is every vertex pair of every counterexample critical? True for all five known graphs.
7. Are the 68-vertex and the 112-vertex counterexamples colorable only by themselves?

The item "the 68-vertex counterexample was not retrievable" of the round-1 list is closed.
