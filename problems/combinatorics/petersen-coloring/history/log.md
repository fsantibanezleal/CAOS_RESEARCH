# petersen-coloring: history log (append-only)

## 2026-09-03 - scouting, selection, and opening

- Scouted the September 2026 landscape of computer-found counterexamples (six primary-source
  dossiers under `program/scouting-2026-09/`); scored candidates on the counterexample radar.
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
