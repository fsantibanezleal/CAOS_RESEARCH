# EXP-013 - conducted charge classes of 6-poles (first bounded action of focus PCC-F6)

Declared 2026-10-06 before any code of this experiment was run. Focus PCC-F6
(`program/petersen-coloring/research-governance.json`). Theory: `context/2026-10-06-charges.md`.

## Question

For 6-poles with their six dangling ends split into two connectors of three, which of the six
charge orbits `0, E, D3, D2, T1, T2` are conducted (realized as the common class of both connectors
by a map with every vertex good)? In particular: does any 6-pole cut from a cyclically
5-edge-connected cubic graph fail to conduct `0`, or conduct a small set?

## Fixed objects

Sources (cyclic edge connectivity measured exhaustively in this experiment):

- the Petersen graph `P`; the flower snarks `J5`, `J7`; the dodecahedron `GP(10, 2)`;
- the counterexample `G52` (cyclically 4-edge-connected; used for the charge spectrum of its
  critical pairs and as a positive control of the restoration lemma).

Shapes:

- (a) `H - u - w` for one representative of every `Aut(H)`-orbit of non-adjacent vertex pairs,
  connectors = the three ends at `u` and the three ends at `w`;
- (b) `H - e1 - e2 - e3` for one representative of every `Aut(H)`-orbit of triples of pairwise
  vertex-disjoint edges, all ten splits of the six ends into two triples (sources `P`, `J5`, the
  dodecahedron only; `J7` and `G52` too large for all triples in this experiment).

For each 6-pole, split and orbit: one formula (every vertex good, the first connector's class fixed
to the orbit's representative, by `Aut(P)`-invariance of conducted sets). SAT answers are checked
from the definition (all vertices good, both connectors in the target class); UNSAT answers carry
DRAT proofs checked by drat-trim.

## Falsifiable predictions

- P1 (controls): `0` is conducted by every shape-(a) 6-pole of a Petersen-colorable source
  (restriction of a coloring), and never by `G52 - u - w` (restoration lemma), on every pair
  examined.
- P2 (spectrum of `G52`): committed expectation, moderate confidence: every critical pair of `G52`
  can carry an `E` charge (orbit `E` conducted by every `G52 - u - w`); `T1` is conducted by none
  (it was never seen among the 1,326 stored witnesses).
- P3 (the question): committed expectation, low confidence (one third): some shape-(b) 6-pole of
  a cyclically 5-edge-connected source does not conduct `0` under some split.
- P4 (only if P3 holds): two 6-poles with disjoint conducted sets exist among the measured ones;
  their alternating ring `R_2` is then built and tested for cyclic 5-edge-connectivity (exhaustive
  search for cycle-separating cuts of size at most 4) and for Petersen colorability (checked
  proof). This would be a cyclically 5-edge-connected counterexample (Problem 11 of
  arXiv:2608.10028v4).

## One-sidedness

Conducted orbits are SAT witnesses; non-conducted orbits are verified refutations. If every
measured 6-pole of the cyclically 5-edge-connected sources conducts `0`, the route of section 5 of
the theory note needs other shapes or sources, and that is recorded as the outcome.

## Budget and stop rule

CPU only; 120 seconds per formula; 3 hours overall. Stop condition of PCC-F6 (first part): if every
measured 6-pole of a cyclically 5-edge-connected source conducts `0` and at least four of the six
orbits under every split, the focus is reviewed before a second experiment.

## Verdict rules

Each prediction PASS, REFUTED or UNDECIDED; the table of conducted sets is the output either way.
