# EXP-002 - perfect matching covers of the counterexamples (Berge-Fulkerson, Berge, Fan-Raspaud)

Declared 2026-09-03 before experiment code was run. Phase PC-P2. Backlog PCB-003.

## Question

Do the three certified counterexamples `G112`, `H112`, `G52` (EXP-001 CONFIRMED) admit a
Berge-Fulkerson cover (six perfect matchings covering every edge exactly twice), a Berge cover by
five perfect matchings, a cover by four perfect matchings, and three perfect matchings with
empty intersection (Fan-Raspaud)?

## Motivation

The Petersen coloring conjecture implied the Berge-Fulkerson conjecture and hence the Berge
conjecture (perfect matching index at most 5) and the Fan-Raspaud conjecture (context dossier,
implication ladder). The first non-Petersen-colorable bridgeless cubic graphs are therefore the
sharpest known test cases for all three; no source reports these covers for them as of
2026-09-03 (context dossier section "what is not in the literature").

## Fixed objects

The three graphs of EXP-001 (same files and digests). Encodings from `pcclib.encoders`:
`berge_fulkerson`, `berge_cover(count=5)`, `berge_cover(count=4)`, `fan_raspaud`. Symmetry
breaking: the matchings containing edge 0 are fixed to indices 0 (and 1 for the double cover).
Witness checkers: `check_berge_fulkerson`, `check_berge_cover`, `check_fan_raspaud`, all reading
only the graph.

Controls: the Petersen graph (Berge-Fulkerson cover exists: its six perfect matchings each used
once cover every edge twice; perfect matching index 5; Fan-Raspaud holds), `K4` and the prism
(3-edge-colorable: perfect matching index 3, every cover exists), `J5` (snark: index at least 4;
Berge-Fulkerson expected to exist since the census found no Fulkerson counterexample through
order 36 [V via BGHM abstract]).

## Falsifiable predictions

- P1: every control returns the expected status: Petersen BF SAT, Berge-5 SAT, Berge-4 UNSAT
  (the Petersen graph has perfect matching index 5 [V, classical: every two perfect matchings of
  the Petersen graph share an edge, so four cannot cover]), Fan-Raspaud SAT; `K4` and prism all
  SAT including Berge-4 and Berge-3; `J5` BF SAT, Berge-4 status recorded.
- P2: each of `G112`, `H112`, `G52` has a Berge-Fulkerson cover, decoded and checker-validated.
- P3: consequently each has a Berge cover by five perfect matchings and satisfies Fan-Raspaud;
  both are also decided directly (their own SAT instances and witnesses).
- P4: the perfect matching index of each is exactly 4 or exactly 5, decided by the Berge-4
  instance: SAT with a validated witness gives 4; UNSAT with a verified DRAT proof gives 5 (index
  3 is impossible since the graphs are not 3-edge-colorable, which follows from EXP-001 because
  3-edge-colorable graphs are Petersen colorable [V, GJMMM introduction: "trivially true for
  3-edge-colorable"; Open Problem Garden]). Committed expectation: 4 for all three (no prior
  evidence; a guess to be tested).
- P5: corrupted witness controls: a Berge-Fulkerson witness with two matchings swapped is still
  accepted (the checker is order-blind), and one with a single edge moved is rejected.

## One-sidedness

P2 SAT is a positive certificate (an explicit cover). P2 UNSAT with a verified proof would be a
counterexample to the Berge-Fulkerson conjecture, a first-magnitude result that would then need
the full adversarial ladder before any claim (second encoding, second checker, hand-verified
structure). A TIMEOUT proves nothing.

## Premise dependencies

- EXP-001 CONFIRMED: the three graphs are genuine counterexamples (so the test is meaningful).
- Not 3-edge-colorable: derived from EXP-001 via the trivial direction of the conjecture.

## Invariant-first note

The Berge-Fulkerson instance on `G112` is itself the single deciding call; it runs first.

## Compute budget and kill criterion

CPU only. Wall cap 30 minutes per SAT call, 60 minutes per proof check, whole run under 3
hours. A capped instance is INCONCLUSIVE.

## Verdict rules

- CONFIRMED only if P1, P2, P3, P5 pass and P4 is decided (either value) for all three graphs.
- REFUTED if any target Berge-Fulkerson instance is UNSAT with a verified proof (escalates to a
  dedicated follow-up experiment before any claim).
- INCONCLUSIVE if any target hits its cap.
