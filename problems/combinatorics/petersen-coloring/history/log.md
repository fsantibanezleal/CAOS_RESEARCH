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
