# EXP-013 verdict - every 6-pole of the Petersen graph, the flower snarks J5 and J7 and the dodecahedron conducts the core {0, E, D2}: the charge obstruction never separates them (P1, P2 PASS; P3 REFUTED)

Date: 2026-10-06. Hypothesis committed at `cb6a0929` before any run. Runner `run.py` (one formula per
6-pole, split and orbit; from 2026-10-06 16:10 every answer is also appended to
`E:/_Datos/caos-research/petersen-coloring/EXP-013/conduct-<source>-<shape>.partial.jsonl`, so a
stopped run resumes). Artifacts `artifacts/conduct-<source>-<shape>.json` and `run-*.log`; formulas
and proofs under `E:/_Datos/caos-research/petersen-coloring/EXP-013/`. Theory:
`context/2026-10-06-charges.md`, sections 3 to 6.

## Result

Conducted orbits (an orbit is conducted when some map with every vertex good puts a class of that
orbit on both connectors). SAT answers are checked from the definition; UNSAT answers carry DRAT
proofs accepted by drat-trim. No formula reached the 120-second cap on these sources.

| source | cyclic cut below 5 | shape | 6-poles (splits) | formulas | conducted sets that occur (count) |
|---|---|---|---|---|---|
| `P` | none | a | 1 | 6 | `{0, E, D2}` (1) |
| `P` | none | b | 4 (40) | 240 | `0 E D3 D2` (16), `0 E D3 D2 T2` (11), `0 E D3 D2 T1 T2` (5), `0 E D3 D2 T1` (4), `0 E D2 T2` (3), `0 E D2` (1) |
| dodecahedron `GP(10,2)` | none | a | 4 | 24 | `0 E D3 D2 T2` (2), `0 E D3 D2 T1` (2) |
| dodecahedron | none | b | 30 (300) | 1,800 | `0 E D3 D2 T2` (180), `0 E D3 D2` (68), `0 E D3 D2 T1 T2` (37), `0 E D3 D2 T1` (10), `0 E D2` (3), `0 E D2 T2` (2) |
| `J5` | none | a | 14 | 84 | `0 E D2` (6), `0 E D3 D2` (3), `0 E D2 T2` (3), `0 E D2 T1` (1), all six (1) |
| `J5` | none | b | 151 (1,510) | 9,060 | `0 E D3 D2 T2` (753), `0 E D3 D2` (523), `0 E D3 D2 T1 T2` (129), `0 E D3 D2 T1` (93), `0 E D2` (7), `0 E D2 T2` (4), `0 E D2 T1` (1) |
| `J7` | none | a | 21 | 126 | `0 E D2` (8), `0 E D3 D2` (5), `0 E D2 T2` (5), all six (2), `0 E D2 T1` (1) |

All 11,340 formulas on these four sources are decided: every SAT witness is accepted by the
checker and every UNSAT answer has a verified proof. **Every one of the 1,890 measured 6-pole
splits conducts `0`, `E` and `D2`.** The minimal conducted set that occurs is exactly the core
`{0, E, D2}`, attained by `P - u - w`.

`G52` (shape a, 212 6-poles up to its 6 automorphisms, 1,272 formulas, run 16:15 to 17:59, slowest
formula 106.6 s): all decided, every witness accepted, every refutation with a verified proof.

| conducted set | 6-poles `G52 - u - w` |
|---|---|
| `{E, D3, D2}` | 105 |
| `{E, D3, D2, T2}` | 47 |
| `{E, D2}` | 32 |
| `{E}` | 22 |
| `{E, D3}` | 5 |
| `{E, D2, T2}` | 1 |

`0` is conducted by none (212 refutations, as the restoration lemma requires), `E` by all, `T1` by
none. So every critical pair of `G52` can carry an `E` charge, 22 of the 212 pair orbits carry only
`E` charges, and no pair carries the all-ones class `T1`.

## Predictions

| prediction | outcome |
|---|---|
| P1 (controls: `0` conducted by every shape-(a) 6-pole of a colorable source; never by `G52 - u - w`) | PASS: all 40 shape-(a) 6-poles of the colorable sources conduct `0`; none of the 212 `G52 - u - w` does |
| P2 (`G52`: `E` conducted by every `G52 - u - w`, `T1` by none) | PASS on all 212 orbits of non-adjacent pairs |
| P3 (some shape-(b) 6-pole of a cyclically 5-edge-connected source fails to conduct `0`) | REFUTED: all 1,850 shape-(b) splits conduct `0` (and `E` and `D2`) |
| P4 (two 6-poles with disjoint conducted sets) | not reached (P3 refuted); impossible among these sources, since all conducted sets contain the core |

## Stop rule and consequence

The stop condition of the hypothesis asked whether every measured 6-pole of a cyclically
5-edge-connected source conducts `0` and at least four orbits under every split. The first part
holds; the second does not (the core has three orbits and occurs 25 times). What the data show is
stronger for the purpose of the route: all conducted sets contain the same three orbits, so no two of
these 6-poles are disjoint, and the ring theorem with 3-edge junctions cannot certify a
non-colorable ring built from them. A ring of such blocks can fail to be colorable only through
structure finer than charges. PCC-F6 was reviewed accordingly and its second bounded action,
EXP-014 (the exact transfer relations of the same blocks), was declared before any code ran.

## Adversarial validation record

- Conducted sets are `Aut(P)`-invariant, so one representative class per orbit decides the orbit;
  the representatives come from `pcclib/charges.py` (`orbit_table`, cross-checked against the coset
  table of `code/probes/cut_code_cosets.py`).
- The nonempty sectors of the exact transfer matrices computed in EXP-014 by a different method
  (projected model enumeration, no class constraint) coincide with these conducted sets for every
  block of `P`, `J5` (shape a), `J7` (shape a) and the dodecahedron (shape a) that both experiments
  contain.
- The cyclic edge connectivity of the sources is measured exhaustively in the runner (no
  cycle-separating cut with at most four edges).

## Limitations

Shape (b) was run for `P`, `J5` and the dodecahedron only, as declared. The 52-vertex counterexample
is not cyclically 5-edge-connected, so its 6-poles cannot give a cyclically 5-edge-connected ring;
it enters as a control and for the charge spectrum of its critical pairs.
