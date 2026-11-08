# EXP-005 verdict: STOPPED at the budget projection (gates at orders 10 and 11 pass; order 13 is out of reach)

Date: 2026-11-08. Hypothesis frozen at fe86a6f1.

## Result

- **Gate 1 and gate 2 PASS at orders 10 and 11 [MV]** (`artifacts/gates.txt`): GenHypohamiltonian 1.2.1 with the
  option `platypus` reproduces GNZ Table 1 (48 and 814 platypuses), and EXP-001's MNH filter on those lists gives
  exactly EXP-002's case-B counts (4 and 10). This confirms the route: case-B MNH graphs are the MNH graphs among
  the platypuses (GNZ Lemma 2), and the generator plus filter recover them.
- **Gate at order 12 not completed.** It ran as 8 parts (`mod <rest> 8`), two at a time. After 9.5 hours the two
  running parts had finished the stages of maximum degree up to 7 and were in the stage of maximum degree 8
  (cumulative CPU per part: 85 s through degree 4, 2,475 s through 5, 10,590 s through 6, 19,632 s through 7;
  `artifacts/order12-part0-stages.txt`). The generator warns that splitting with a small modulus produces many
  isomorphic copies, and each part had already written more graphs than one eighth of the 24,847 platypuses.
  The parts were then lost by an operator error: the parts' orchestrator was stopped so that the remaining six
  parts could run in parallel, and processes started through `wsl.exe` end with that session, so the two running
  parts ended too. No count was recorded at order 12.
- **Projection, order 13:** each order-12 part needs more than 5.5 CPU-hours before its last three degree stages,
  so all of order 12 is well above 100 CPU-hours, and the growth from order 11 (375 s in total) to 12 suggests a
  factor of several hundred; order 13 (not reported by GNZ) is then thousands of CPU-hours, beyond the 24-hour budget
  on 28 processes. Per the hypothesis, the experiment stops here.

## What follows for HMB-006

Case B at order 13 needs a generator restricted to the MNH conditions (maximum degree at most 9, 2-connected,
nonadjacent degree sums at most 12, non-Hamiltonian with every vertex-deleted subgraph traceable) rather than all
platypuses, or a run of hundreds of CPU-hours across several attended sessions. Case A is resumable (EXP-004).

## Operational note

A long WSL job must be started so that it survives the end of the launching `wsl.exe` (for example from a shell that
stays attached for the whole run), or its parts must be independent processes each with its own launcher.
