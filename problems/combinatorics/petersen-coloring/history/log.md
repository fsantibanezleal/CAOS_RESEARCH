# petersen-coloring: history log (append-only)

## 2026-09-03 - scouting, selection, and opening

- Scouted the September 2026 landscape of computer-found counterexamples (six primary-source
  dossiers under `problems/combinatorics/petersen-coloring/context/scouting-2026-09/`); scored candidates on the counterexample radar.
- Selected the 2026 disproof of Jaeger's Petersen coloring conjecture: Putman's two 112-vertex
  graphs (Zenodo 21845291, arXiv:2608.10012), Jooken's human-checkable proof (arXiv:2608.10028),
  and the 52-vertex graph plus infinite families of Goedgebeur, Jooken, Macajova, Mattiolo and
  Mazzuoccolo (Zenodo 21933786). Discovery priority recorded for all of them.
- Chose the consequence audit (Berge-Fulkerson, Berge, Fan-Raspaud, 5-cycle double cover,
  nowhere-zero 5-flow, normal 6, defects) as the CAOS contribution; minimality kept bounded to a
  declared gadget grammar.
- Downloaded and hash-verified the public artifacts to `E:/_Datos/caos-research/petersen-coloring/`;
  transcribed the three graphs into `data/` with SHA-256 digests (Putman's compact-JSON digest
  convention reproduced exactly).
- Wrote `pcclib` (graphs, invariants, CNF builder, encoders, checkers, WSL solver runner) with
  tests. Declared EXP-001 before running anything.

## 2026-09-03 - EXP-001 to EXP-003

- EXP-001 CONFIRMED: our edge-image Petersen encoding and side-presence normal encoding refute
  `G112`, `H112`, `G52` with drat-trim-verified proofs (normal-5 proofs 0.2 to 0.9 GB, 15 to 20
  minutes each; Petersen proofs seconds to a minute); five colorable controls accepted; Putman's
  four public proofs verified with our checker; cyclic edge connectivity 4 certified by exhaustive
  small-cut search plus explicit 4-cuts. Session restart interrupted the background run after it
  had finished; the log and manifest were intact.
- EXP-002 CONFIRMED: Berge-Fulkerson covers, Berge-5 covers and Fan-Raspaud triples on all
  three; perfect matching index exactly 4 (the committed guess). Attempt 1 failed only on a
  mis-coded corrupted-witness control (the control could re-add the edge it removed); preserved
  as `run-attempt1-control-bug.log`; targets unchanged in attempt 2.
- EXP-003 CONFIRMED: 5-cycle double covers, nowhere-zero 5-flows, no 4-flows; oddness 4 and
  resistance 3 for both 112-vertex graphs, oddness 2 and resistance 2 for `G52`; the committed
  oddness-2 expectation refuted on the 112-vertex graphs. Oddness encoded exactly via the
  2-coloring lemma.
- Declared EXP-004 (normal 6, strong normal 6, exact normal-5 defect, exact P-defect).
- Context dossier and references written from the primary texts (Putman, Jooken, GJMMM read in
  full); wiki 01, 03, 04 transcribed.

## 2026-09-03 - EXP-004 to EXP-006, the parity theorem, manuscript and web page

- EXP-004: normal and strong normal 6-edge-colorings on all three graphs (normal chromatic index
  exactly 6); cardinality-encoded defect ladders stalled at bound 1 under the 30-minute cap,
  except `G52` whose P-defect came out exactly 2 by that route (bound 1 UNSAT in 532 s, bound 2
  SAT).
- EXP-005 declared and run on the classes of `k` copies of `F` plus `m` free vertices: `(5,0)`
  and `(6,0)` exhausted in seconds by a universal coloring, which became the pure-F proposition
  (context note); the 26-vertex control `(3,2)` did not converge in 15 minutes (1,059
  iterations, 29,052 clauses), and `(5,2)`/`(6,2)` ran under 2-hour budgets. Convergence
  measured, refinement recorded (research lines PCR-4b/4c).
- EXP-006 declared: designated relaxation. All 52 single-vertex relaxations of `G52` UNSAT
  (verified); the pattern was proved for every cubic graph (parity theorem: bad-set label vectors
  sum into the cut space of `P`; odd cuts of size 1 or 3 are stars), so the 112-vertex single
  sweep was stopped after one vertex. All 1,326 pairs of `G52` critical (defect exactly 2 at
  every pair); all 120 free-vertex pairs of `G112` and of `H112` critical (defect exactly 2).
  Full pair sweeps of the 112-vertex graphs and the edge-relaxation sweep of `G52` (normal-5
  defect) launched.
- Manuscript v0.01 drafted from the verdicts (7 pages), Zenodo DOI reserved
  (10.5281/zenodo.22285165, concept 10.5281/zenodo.22285164), header printed; web problem page
  built and gated (24 screenshots, light/dark, EN/ES, all tabs, no overflow); wiki 01-05 written.
- Incidents: a shell heredoc split a Python string literal and mangled LaTeX (fixed through the
  file tools); an orphaned solver process of the stopped single sweep was killed by hand.

## 2026-09-03 - publication

- EXP-006 closed: all 6,216 pairs of `G112` and of `H112` critical (universal 2-criticality on
  all three graphs); verdict written. EXP-005 `(5,2)` stopped at its 2-hour budget (1,992
  iterations, 80,832 clauses, no counterexample); `(6,2)` running.
- Manuscript v0.01 frozen (7 pages, 351,989 bytes, SHA-256 `40b476f6...`), attached to the
  reserved Zenodo draft and PUBLISHED: DOI 10.5281/zenodo.22285165, concept
  10.5281/zenodo.22285164. Public download verified against the committed PDF.
- EXP-005 closed INCONCLUSIVE on its question: `(6,2)` also budget-stopped (1,498 iterations,
  75,286 clauses, no counterexample); verdict written.

## 2026-09-18 - round 2

- Literature: arXiv:2608.10028v3 (2026-09-11) and Ma-Mattiolo-Steffen-Wolf read in full
  (`context/2026-09-18-v3-and-h3-dossier.md`); v3 overlaps round 1 on several invariants, raises
  the lower bound to 40, and asks whether the 52-vertex graphs are colorable only by themselves.
- EXP-007 declared and run. Attempt 1 (unknown target with a free part, lazy connectivity and
  bridge cuts) learned about 2,000 cuts per order in 35 minutes and decided nothing. Lemmas A
  (fiber parity) and B (at most one unused target vertex, splitting lemma) were proved
  (`context/2026-09-18-hcoloring-reduction-lemmas.md`), the reduced encoding agreed with the
  unreduced one on 21 controls, and every decided order became a zero-cut refutation. `G52`:
  orders 2, 4, 30 to 50 refuted with verified proofs by the evening.
- House of Graphs became reachable: `G52b` (57278) and `G68` (57280) added to `data/` and certified
  (four checked proofs). EXP-008: both match `G52` on every invariant; all 1,326 and 2,278 vertex
  pairs critical.
- `G52` has 6 automorphisms and 14 edge orbits; the 42 edge relaxations already refuted meet every
  orbit (EXP-006 addendum 4). Later the same day the lower bound turned out to be Proposition 3 of
  Mattiolo, Mazzuoccolo, Mkrtchyan (2021); recorded as such.
- Theory: `pd <= ab`; ring and frame theorems (one bad vertex per block); Corollary: statements
  (c), (d) of the sublinear approximation conjecture of Mattiolo et al. are false; threshold
  proposition (`pd >= 3` on one cyclically 4-edge-connected graph refutes (e))
  (`context/2026-09-18-defect-unbounded.md`). The ring and frame constructions were found in their
  2021 paper AFTER the theorems were written; the record states that the constructions are theirs
  and the cut-space conclusion is ours. EXP-009: defect equals the number of blocks on `R_2`,
  `R_3`, `R_4`, `K_4[G52]`.
- EXP-010: all 4-poles `G - e1 - e2` of `G52`, `G52b`, `G68` colorable; ten dot products of `G52`
  with itself are new 102-vertex counterexamples with defect 2; distance sets always contain 1.
  A symmetry-breaking conflict in the distance-set runner was caught before any result was read.
- Incident: the driver of EXP-007 attempt 1 survived the stop command and ran old code for four
  hours next to the rerun (shared log files, a third of the machine). No result file affected;
  recorded in the EXP-007 hypothesis.
- A wording error of our own was caught before publication: "4-poles can be chained around a
  ring" holds for rings of even length only; corrected in the manuscript, wiki, context note and
  page.
- Audit manuscript v0.04 PUBLISHED (10.5281/zenodo.22836612): five graphs, Section 5.3 on
  abnormal edges, unbounded defects and the sublinear approximation consequence. (v0.03 of the
  same record was another session's author-name release of the same day.)
