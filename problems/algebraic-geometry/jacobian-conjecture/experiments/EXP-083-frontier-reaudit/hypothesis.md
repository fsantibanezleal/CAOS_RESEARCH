# EXP-083 - Re-audit the 24 [125,150] configs against the mined GGV2 remark + Heitmann

- **Question.** Which of the 24 [125,150] configurations are ALREADY excluded
  in the literature (so not open frontier), and which are genuinely open?
- **Motivation.** EXP-082 found C13 already discarded by GGV2 remark tex 1053
  (B0/B1 -> A0' forcing), which our dossier had not fully mined. The same
  remark and Heitmann Thm 2.24/2.25 + GGV5 Remark 7.9 exclude several A0'
  patterns: wp(n',n'-1) corners, the (7,21)/(10,25)/(14,35)/(6,15)/(9,21)
  families. Each of our 24 configs has a chain with an A0'; if that A0' is an
  excluded corner, the config is already done.
- **Predictions.** 1. [MV] For each of the 24 configs, compute the forced A0'
  from its chain data (where derivable by the EXP-077 method: shared-bottom-
  vertex d0, q1, shift) and test membership in the excluded family / named
  lists. 2. [D] Partition the 24 into ALREADY-EXCLUDED vs GENUINELY-OPEN vs
  DERIVATION-NEEDED (A0' not cleanly forcible without more source work).
- **Method.** Exact arithmetic per config; cite the exact excluding statement
  for each excluded one; honest DERIVATION NEEDED where the forcing is unclear.
- **Success.** A clean partition; the genuinely-open set is the real frontier.
- **Failure.** none (an audit).

Declared 2026-07-24 before the run.
