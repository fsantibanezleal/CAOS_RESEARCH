# EXP-015 - Rings of superedges cut from the cyclically 5-edge-connected snarks of order at most 28

Declared 2026-11-15 before any code of this experiment was run. Focus PCC-F6
(`program/petersen-coloring/research-governance.json`), the next bounded action named by EXP-014 (PCB-034). Theory:
`context/2026-10-06-charges.md`, sections 5 and 7. Toward Problem 11 of arXiv:2608.10028v4 (does a cyclically
5-edge-connected counterexample to the Petersen coloring conjecture exist?), still open at this date (web search
2026-11-15; the smallest counterexample order is reported between 38 and 52).

## Why this experiment

EXP-014 decided every ring of claws and of Petersen superedges (all colorable) and showed on `G52` that the transfer
relation detects a non-colorable gluing that charges cannot. Its large block families did not close. Superedges cut from
cyclically 5-edge-connected snarks are the natural next family: a ring of them is the classical superposition shape, its
order is the sum of the block orders, and two blocks from snarks of order at most 28 give rings of order 16 to 52, which
covers the open range of the smallest counterexample. Every block is cut from a Petersen-colorable graph, so each
conducts the core sectors; a non-colorable ring can only come from the finer structure the transfer relation sees.

Sizing (probe of 2026-11-15, evidence only, script outside the repository): one block's sector matrices take 0.3 s
(`P`) to 38 s (order 28) on one core with python-sat 1.9.dev22 (CaDiCaL 1.5.3); the snarks of orders 20, 22, 24, 26
have 14, 22 + 22, 70 + 69 and 1,486 Aut-orbits of vertex pairs at distance at least 2 (1,684 blocks with `P`); an order-28
snark has about 336, of which about 20 at distance 5.

## Inputs

- House of Graphs lists of cyclically 5-edge-connected snarks (girth at least 5), files
  `https://houseofgraphs.org/data/snarks/cyc5/Generated_graphs.<n>.05.sn.cyc5.g6` for n = 10, 20, 22, 24, 26, 28,
  downloaded 2026-11-15 to the data root `caos-research/petersen-coloring/sources/hog-snarks-cyc5/` with SHA-256 sums
  (`SHA256SUMS`): 1, 1, 2, 2, 10 and 75 graphs (91 in all; the lists have no file for orders 12 to 18: no snark has
  order 12 to 16, and the two of order 18, the Blanusa snarks, are cyclically 4-edge-connected).
  Lists from G. Brinkmann, J. Goedgebeur, J. Hagglund, K. Markstrom, Generation and properties of snarks, J. Combin.
  Theory Ser. B 103 (2013) 468-488.
- `G52` (`data/gjmmm-52.edgelist`) for the positive control of EXP-014 addendum 1.

## The object

For a snark `G` and vertices `u`, `w` at distance at least 2, the **superedge block** `B(G; u, w) = G - u - w` has
`L` = the three dangling ends at the former neighbors of `u` (ordered by the neighbor's index) and `R` = those of `w`;
it enters in both orientations, each followed by each of the six junction permutations (12 generators per block,
duplicates removed). Block pairs `(u, w)` are taken up to `Aut(G)` (one representative per orbit of unordered pairs).
Sector matrices, rings, products and the trace criterion are those of EXP-014 (`code/pcclib/transfer.py`): a ring is
Petersen colorable if and only if some sector of its product has a nonzero diagonal.

Families:
- `F26`: every block of the 16 snarks of order at most 26 (1,684 blocks);
- `F28d5`: the blocks of the 75 snarks of order 28 with `u`, `w` at distance 5;
- `F22`: the blocks of the snarks of order at most 22 (59 blocks);
- `F = F26` union `F28d5`.

## Falsifiable predictions

- **R1 (the question; committed expectation 0.75 that it holds).** Every simple ring of two generators of `F` is
  Petersen colorable (every product of two generators has a nonzero diagonal in some sector). Decided exhaustively:
  all unordered pairs of generators, a block with itself included.
- **R2 (committed expectation 0.85).** Every simple ring of three generators of `F22` is Petersen colorable.
- **R3 (validation).** For 500 random simple rings (seed 20261115: 300 of length 2 over `F`, 200 of length 3 over
  `F22`) the trace criterion and CaDiCaL on the explicit graph agree.
- **R4 (positive control).** The `G52` split of EXP-014 addendum 1 (cut edges 8, 26, 39, 40, 48, 59) gives a zero
  diagonal in all six sectors for all ten splits, recomputed here.

Descriptive measurements (not predictions): the sectors each block conducts; the number of rings of each order; girth
and cyclic edge connectivity of a sample of 200 rings of length 2 (exact search for a cycle-separating cut of at most
four edges).

## If a zero-trace ring is found

It is rebuilt as a graph (`transfer.build_ring`), checked simple and cubic, and its non-colorability decided by CaDiCaL
on the explicit Petersen-coloring formula with a DRAT proof checked by drat-trim, and by a second solver on a second
encoding (one variable per vertex image and bijection, MiniSat 2.2, as in EXP-014). Then its girth, cyclic edge
connectivity (exact) and order are computed. Before anything is claimed, the coordinating session re-runs the solver
check. Outcomes: a counterexample to the Petersen coloring conjecture of that order (new if below 52); if it is
cyclically 5-edge-connected, an answer to Problem 11. Every zero-trace ring found is reported, not only the first.

## Gates (before production)

- G0. Inputs: the SHA-256 sums match; every graph is cubic, simple, of girth at least 5, cyclically 5-edge-connected
  (exact search) and not 3-edge-colorable (SAT); the counts per order are as listed.
- G1. Block matrices: `P`'s block equals EXP-014's `S` (120, 296, 8 entries in `0`, `E`, `D2`); 30 random blocks of `F`
  recomputed with the second encoding and MiniSat 2.2 are equal entry by entry.
- G2. R4 passes before the ring search starts (the criterion detects a known non-colorable gluing).

## Soundness

Entries of the sector matrices are models checked from the definition (every vertex good); a missing entry could only
shrink a diagonal, so a nonzero diagonal is a proof of colorability and the positive statements R1 and R2 are sound.
A zero diagonal is a candidate only until the solver checks above confirm it.

## Budget and kill criterion

At most 12 parallel processes and 10 hours of wall time in all (blocks about 6 hours, ring searches about 2 hours). A
block that takes more than 10 minutes is recorded as not computed and its rings as undecided; R1 then holds only for
the computed blocks, and the verdict says so.

## Premise dependencies

- EXP-014 (CONFIRMED): the transfer relation, Propositions 7.1 and 7.2 and the trace criterion, the code
  (`code/pcclib/transfer.py`) and the `G52` control.
- EXP-013 (CONFIRMED): the conducted core `{0, E, D2}` of blocks cut from Petersen-colorable graphs.

## Invariant-first note

The deciding invariant of a ring of two blocks is whether the two transfer relations, as unions of `Aut(P)`-orbits of
label pairs in each sector, meet after the junctions; the charge sectors alone never separate them (EXP-013).
