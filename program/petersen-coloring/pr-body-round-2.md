# petersen-coloring round 2: five graphs, H-colorings by an unknown target, unbounded defects

Problem-scoped change (`problems/combinatorics/petersen-coloring/`, `program/petersen-coloring/`,
`manuscripts/petersen-coloring/`, the problem's page and its citations). No version bump, no bake,
no tag: the release step stays with the serialized release owner.

## What this round adds

- **Literature.** arXiv:2608.10028v3 (2026-09-11), Ma-Mattiolo-Steffen-Wolf (Combinatorica 2025) and
  Mattiolo-Mazzuoccolo-Mkrtchyan (2021) read and recorded
  (`context/2026-09-18-v3-and-h3-dossier.md`). v3 overlaps round 1 on several invariants; the
  record and the manuscript say so and cite it.
- **Two new graphs** from House of Graphs (57278: second 52-vertex counterexample; 57280: 68-vertex
  counterexample), certified with our own encoders before use (four checked DRAT proofs).
- **EXP-008 CONFIRMED.** Both graphs have the invariants of `G52` (perfect matching index 4,
  oddness 2, resistance 2, 5-CDC, 5-flow, no 4-flow, normal chromatic index 6, Petersen defect 2),
  and every vertex pair is critical (1,326 and 2,278): universal 2-criticality on all five known
  counterexamples.
- **EXP-007 (open, certification running).** "Is a 52-vertex counterexample colored by a smaller
  bridgeless cubic graph?" (question of v3, Section 5.4). Attempt 1 did not converge (2,000 lazy
  cuts per order, no decision; preserved). Two lemmas proved in
  `context/2026-09-18-hcoloring-reduction-lemmas.md` (all fibers of the vertex map have the same
  parity; unused target vertices reduce to at most one, by the splitting lemma) remove the
  unconstrained part of the target; the reduced and unreduced encodings agree on 21 controls; every
  decided order is a zero-cut refutation with a drat-trim-verified proof. `G52`: orders 2, 4, 30 to
  50 refuted, which with the lower bound 40 of v3 puts `G52` in `H_3`. `G52b`: 44 to 50 refuted;
  `G68`: 64, 66. Both forms of the statement (unconditional list; conditional membership) were fixed
  in an addendum before the mid-range orders ended. An incident (orphaned attempt-1 driver) is
  recorded; no result file was affected.
- **Theory** (`context/2026-09-18-defect-unbounded.md`): `pd <= ab`; rings of `t` counterexamples
  and cubic frames need one bad vertex per block; hence no sublinear bound on abnormal edges for
  2-connected or 3-connected cubic graphs, so statements (a) to (d) of Conjecture 3 of Mattiolo et
  al. are false and the conjecture reduces to its cyclically 4-edge-connected statement; threshold
  proposition (one such graph with Petersen defect at least 3 would settle it). The constructions
  are theirs; the cut-space conclusion is new. **EXP-009 CONFIRMED**: defect equals the number of
  blocks on `R_2`, `R_3`, `R_4`, `K_4[G52]`.
- **EXP-010 (budget ends 18:30 on 2026-09-18).** All 4-poles `G - e1 - e2` of `G52`, `G52b`, `G68`
  are colorable; ten dot products of `G52` with itself are new 102-vertex counterexamples with
  defect 2; boundary distance sets.
- **Manuscript.** `consequence-audit` v0.04 published: DOI 10.5281/zenodo.22836612 (five graphs,
  Section 5.3). A second manuscript (`colorable-only-by-itself`) is drafted and waits for the last
  certificates.
- **Web page.** Two new tabs (colorable only by itself; large defects), five-graph table, EN/ES;
  visual gate 32 of 32.
- Wiki pages 03 to 07, research lines with the round's exploration moment (PCR-7 to PCR-10),
  RESUME rewritten, state, backlog, history log.

## Checks run locally

`check_template_residue`, `check_content_standards`, `check_research_structure`,
`check_manuscript_voice manuscripts`: OK. `pytest` of the problem library: green. Frontend
`npm ci` and `npm run build`: OK. Visual gate: PASS.
