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

## 2026-09-19 - statement (e) settled

- EXP-012: conduction lemma (a 4-pole whose vertices are all good carries the same cut-space class
  through both connectors; the class of a pair of labels is their line-graph distance); `A = G52 -
  {0,3} - {1,9}` conducts only distance 1, `B = G52 - {2,7}` only distance 0; their alternating rings
  are cyclically 4-edge-connected with defect at least `t`; `R_3` "at most 2 bad vertices" UNSAT
  with a verified proof. Statement (e) of the Mattiolo-Mazzuoccolo-Mkrtchyan conjecture is false,
  so their conjectured equivalence holds. unbounded-defect v0.01 published.
- EXP-007: `G52b` order 40 refuted by a portfolio (2.4 GB proof), orders 24 and 26 of `G52` checked
  post hoc after the WSL virtual machine stopped; both 52-vertex counterexamples are colorable only
  by themselves (given v3 Observation 9).

## 2026-10-06 - sync, governance, publications, new focus

- Synced with develop (333 commits, clean merge); the research worktree moved from `E:/_Temp` to
  `E:/_worktrees/CAOS_RESEARCH-petersen-coloring`; CAOS_MANAGE written from
  `E:/_worktrees/CAOS_MANAGE-petersen-coloring`.
- Literature refresh: arXiv:2608.10028v4 (2026-09-30) renumbers its statements (Observation 10,
  Problems 9 and 11) and still asks whether the 52-vertex counterexamples are colorable only by
  themselves; no work found on statement (e).
- Methodology 13 adopted: `research-governance.json`, `manuscript-map.md`, manuscript READMEs.
- Published: colorable-only-by-itself v0.01 (10.5281/zenodo.22859075); consequence-audit v0.06
  (10.5281/zenodo.23195171), which corrects v0.05's reading of the fifteen-graph criticality as
  evidence against the conjectured equivalence.
- Strategic review: F3, F4 closed; F5 gated; new active focus PCC-F6 (cut-space charges and
  cyclically 5-edge-connected graphs). Charge formulation written; coset structure of the cut code
  verified; EXP-013 declared and running.

## 2026-10-30 - portfolio review: external status

External status: disproved (Putman arXiv:2608.10012; Goedgebeur, Jooken, Máčajová, Mattiolo, Mazzuoccolo, Ulyanov arXiv:2608.10028, v4 2026-09-30) [V]. Nothing new on the conjecture since the last pass of 2026-10-06; adjacent only, Mkrtchyan arXiv:2610.35794 (2026-10-26) [V]. No new overlap with CAOS claims; OpenAI Math: none.
Plan change (assessment): unchanged; rank 1; PCC-F6 stays active. First bounded action: EXP-015 as ordered in `RESUME.md` section 5 (6-poles from the cyclically 5-edge-connected snarks of order at most 28, sector matrices, closures); close PCC-F6 if no zero-trace element exists.

Source: [portfolio review](../../../../program/portfolio-review-2026-10-30.md).

## 2026-11-14 - colorable-only-by-itself v0.02 published (10.5281/zenodo.24230853)

- Revision from the independent audit (CAOS_MANAGE wip/caos-research/msaudit-pc-2026-11-10.md, D1): the membership of
  both 52-vertex counterexamples in H_3 is stated as conditional on Observation 10 of arXiv:2608.10028v4, in the title
  as well ("The Two 52-Vertex Counterexamples to the Petersen Coloring Conjecture Are Colorable Only by Themselves If No Counterexample Has at Most 38 Vertices"); the formula and the certification pipeline as algorithms with proofs (symmetry breaking,
  implied attach clauses); tables of the refuted and undecided orders, the 21 controls, the ablation and the SHA-256
  values; 11,238 words, 15 equations, 7 figures, 9 tables, 25 references, 2 algorithms.
- Independent review (CAOS_MANAGE wip/caos-research/pc-cobi-v02-review-2026-11-14.md): CHANGES REQUIRED (title blocker,
  incomplete bibliography, Algorithm 2 placement, 14 minors), all fixed; re-check closed the rest. The planted SAT
  control at scale (audit plan item 6) is not done and is stated in the Limitations.
- Release: 39 gates passed; 33 pages, 700,579 bytes, SHA-256
  f7393db50890501728c04ba1fb57177a05f667b5dfd367bb23e43df3473f9c39; a fresh unauthenticated download equals the frozen
  file.

## 2026-11-15 - consequence-audit v0.07 published (10.5281/zenodo.24239715)

- Revision from the independent audit (CAOS_MANAGE `wip/caos-research/msaudit-pc-2026-11-10.md`, D2): encodings and
  certification as algorithms with formula sizes checked by `make_tables.py --check`, consolidated tables of the
  invariants, pair sweeps, rings and four-poles generated from the artifacts, a validation section, conditional
  statements marked (MMM Proposition 2 and Theorem 4), a proof of the 3-connectivity of frames, citations updated
  (arXiv:2608.10028 v4, Theorem 8 for the even orders), the rings of copies of G52 renamed C_t, and the title
  re-derived: "Exact Invariants of Five Counterexamples to the Petersen Coloring Conjecture: Covers, Flows, Defect Two
  and Unbounded Abnormal Edges". Independent review (CAOS_MANAGE `wip/caos-research/pc-consequence-audit-v07-review-2026-11-14.md`):
  CHANGES REQUIRED, re-check CHANGES REQUIRED (commit hashes), second fix pass verified.
- Record errata found by the review (the verdicts are not edited; the paper uses the artifact values): the GJMMMU author
  is Nikolay Ulyanov (corrected in `context/references.md`); EXP-008 `verdict.md` says "four instances" where its
  artifacts give five timeouts; EXP-010 `verdict.md` says "7 complete, 5 partial" where its artifacts give six and six;
  the hypothesis commits printed in the EXP-002, EXP-003 and EXP-004 verdicts (4ea64f5, e1e7a3b) do not exist in the
  repository; the commits that add those hypothesis files are 9821fbf4, ecd3bb3d and 571d9fe4.
- Release: 39 gates passed; 35 pages, 677,106 bytes, SHA-256
  12f8c16fbdd11b56bf43591d4984993d2fb4d882162a93c793a29f909a44f067.

## 2026-11-15 - unbounded-defect v0.03 published (10.5281/zenodo.24239832)

- Revision from the independent audit (CAOS_MANAGE `wip/caos-research/msaudit-pc-2026-11-10.md`, D3): Algorithms for
  the sector matrices, the exact and antichain closures with certificate and the certificate check, with costs; F1 to F5
  reported, F4 and F5 undecided; the 203-ring comparison stated as one-sided, with the block re-check status (46 of 81)
  and the G52 control; generated tables of the 1,890 six-pole splits, the G52 charge spectrum, the ring computations and
  the transmitted sets (546 of 949 decided); the transitivity proof for distances 0 to 3; the flower-snark corollary
  machine-verified for k = 5, 7, 9 with the periodicity beyond marked conjectural; superedge rings stated with the
  identity at every junction. Title: "Conduction of cut-space classes through multipoles: unbounded Petersen defect on cyclically 4-edge-connected cubic graphs and transfer semigroups of rings of 6-poles".
- Independent review (CAOS_MANAGE `wip/caos-research/pc-unbounded-defect-v03-review-2026-11-14.md`): CHANGES REQUIRED,
  re-check CHANGES REQUIRED (abstract scope), second fix pass applied as specified.
- Release: 39 gates passed; 35 pages, 805,518 bytes, SHA-256
  0eedaae3e928469738e585a97bf76e545ec07c3209fa67b6e5527febefa54417.

## 2026-11-16 - EXP-015: no zero-trace ring of superedge blocks from the cyclically 5-edge-connected snarks of order at most 28 (PCB-034)

- Hypothesis frozen 2026-11-15 (90040939) before any code: the six sector matrices of every superedge block G - u - w of F
  (every block of the 16 cyclically 5-edge-connected snarks of order at most 26, and the distance-5 blocks of the 75 of
  order 28; House of Graphs lists with SHA-256 sums), rings of two generators of F (R1) and cyclic rings of three over F22
  (R2) tested for a zero diagonal in all six sectors; R3 the trace against CaDiCaL on 500 random rings; R4 the G52 control.
- Result (verdict CONFIRMED): 3,057 blocks computed; 591,009,390 unordered pairs of distinct generators with 0 zero-trace
  (1,836,486 non-simple pairs excluded); 206,425,071 ordered triples over F22 (68,808,751 cyclic triples of distinct
  generators) with 0 zero-trace; R3 500 of 500; R4 holds. Every ring tested is Petersen colorable; no counterexample and no
  answer to Problem 11 of arXiv:2608.10028v4 is claimed. The E sector has a nonzero diagonal for every pair although the
  E matrices have an empty intersection and a full union over the blocks (open). Deviation: the second solver is Glucose 4
  (MiniSat 2.2 of python-sat 1.9.dev22 crashes on this device).
- Independent verification (CAOS_MANAGE `wip/caos-research/pc-exp015-verify-2026-11-16.md`): a SAT-free enumeration matched
  all 3,057 packed blocks entry by entry; own trace code found 0 zero traces on 2,000,000 R1 pairs, every pair with the
  order-10 block and 200,000 R2 triples; VERIFIED WITH CHANGES (six minor record fixes, applied in b6ddda57).
- Focus: by the rule of the 2026-10-06 review, PCC-F6 closes because EXP-015 found no zero-trace block; the closure and
  the next focus are decided at the strategic review (`research-governance.json`, PCC-F6 review note). Disposition:
  research record (a finite negative result; `unbounded-defect` takes a new version only for a correction, a ring of
  6-poles without a Petersen coloring, or the exact abnormal-edge numbers).

