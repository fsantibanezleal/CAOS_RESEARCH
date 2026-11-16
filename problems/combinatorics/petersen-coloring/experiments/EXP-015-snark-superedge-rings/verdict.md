# EXP-015 verdict - CONFIRMED: every simple ring of two superedge blocks cut from the 91 cyclically 5-edge-connected snarks of order at most 28 (blocks of F), and every ring of three over F22, is Petersen colorable

Date: 2026-11-16 (run 2026-11-15 22:51 to 2026-11-16 04:15). Hypothesis frozen at `90040939` before any code ran; instrument
`run.py` (`gates`, `blocks`, `rings2`, `rings3`, `crosscheck`, `describe`, `zero`, `all`), tests `tests/test_petersen_exp015.py`.
Artifacts: `artifacts/results.json`, `blocks.json`, `data-manifest.json`, `run-log.txt`; packed sector matrices and the pair table
under `E:/_Datos/caos-research/petersen-coloring/EXP-015/` (`blocks.jsonl`, `blocktable.json`, `hits-F.npy`, `zero/`; SHA-256 in
`artifacts/data-manifest.json`, plus one SHA-256 per block). Environment: `requirements.txt`. The production command was
`run.py all`; it exited 0 with every block computed.

## Result

**Counts, nothing skipped.** F has 3,057 blocks (F26: 1,684 of the 16 snarks of order at most 26; F28d5: 1,373 blocks of the 75
snarks of order 28 at distance 5), all computed (kill criterion of 600 s never reached; slowest 215.5 s; mean 28.8 s at order 26,
33.4 s at order 28). They give 36,684 generator triples (block, orientation, junction) and 34,380 distinct generator matrices.
Aut-orbit counts of vertex pairs at distance at least 2 per graph and per distance are in `artifacts/results.json` under
`describe.graphs` (totals by order and distance, for example order 26: 412, 519, 529, 26 at distances 2, 3, 4, 5; order 28: 5,372,
7,154, 7,492, 1,373 and 3 at distance 6). F22 has 59 blocks (all computed), 708 triples, 591 distinct generators.

**R1 (rings of two, F).** All 591,009,390 unordered pairs of distinct generator matrices (a generator with itself included) were
tested; **0 have a zero trace**. Nonzero diagonal by sector (pairs): `0` 538,601,054; `E` 591,009,390 (every pair); `D3` 12,821,378;
`D2` 104,698,336; `T1` 59,144; `T2` 8,246,997. Non-simple rings: 1,836,486 of the 672,876,270 unordered pairs of generator triples
are not simple (a parallel edge through a vertex adjacent to both `u` and `w` of both blocks, counted analytically and checked
against `build_ring` on all 144 pairs of triples of the block of `P` in the unit test); they are excluded and none had a zero
trace anyway. Rings by order over triples (16 to 52) are in `results.json` (`R1.rings_of_two_by_order_over_triples`).

**R2 (rings of three, F22).** All 206,425,071 ordered triples of the 591 generators (68,808,751 cyclic classes) were tested;
**0 have a zero trace**. Every ring of three is simple (parallel edges need two ends of one side at one vertex).

**R3 (validation).** 500 random simple rings (seed 20261115: 300 of length 2 over F, 200 of length 3 over F22; 1 non-simple draw
skipped): the trace criterion (library product), the packed trace test and the bulk table (length 2), and CaDiCaL on the explicit
graph agree on 500 of 500. All 500 are colorable, so R3 checks the positive direction; the negative direction is checked by R4 and
the self-test below. The packed `uint64` AND test also agreed with the bulk matrix-product table on 200,000 random pairs of R1 and
with the library product on 200,000 random triples of R2 (0 mismatches).

**R4 (positive control, gate G2).** `G52`, cut edges 8, 26, 39, 40, 48, 59, all ten splits: zero diagonal in all six sectors and both
sides colorable (recomputed here, 26 to 42 s).

**Descriptive.** Sectors conducted by the 3,057 blocks: `{0,E,D3,D2}` 940, `{0,E,D3,D2,T2}` 1,002, `{0,E,D2}` 538, `{0,E,D2,T2}` 434,
`{0,E,D3,D2,T1,T2}` 67, and 8 smaller sets (every block conducts `0` and `E`; the full list is in `results.json`, `blocks`). Sample of
200 random rings of two (orders 42 to 52, seed 20261126): girth 3 in 2, 4 in 7, 5 in 191; exact cyclic edge connectivity 3 in 2,
4 in 10, at least 5 in 188 (exact search for a cycle-separating cut of at most four edges). So the colorable rings found are
mostly cyclically 5-edge-connected themselves, and none is a counterexample.

## Gates

- **G0 PASS.** SHA-256 of the six files match `SHA256SUMS`; 91 graphs in the listed counts (1, 1, 2, 2, 10, 75), each cubic, simple,
  girth at least 5, cyclically 5-edge-connected (exact), not 3-edge-colorable (SAT).
- **G1 PASS.** The block of `P` has 120, 296, 8 entries in `0`, `E`, `D2` and none elsewhere (EXP-014's `S`); 30 random blocks of F
  (seed 20261115, orders 24 to 28) recomputed with the second encoding and a second solver equal entry by entry.
  **Deviation:** the second solver is Glucose 4, not MiniSat 2.2 (see Limitations).
- **G2 PASS** (= R4).

| Prediction | Committed | Outcome | Evidence |
|---|---|---|---|
| R1 every simple ring of two generators of F is colorable | 0.75 | holds, 0 zero-trace pairs of 591,009,390; all 3,057 blocks computed | `results.json` R1 |
| R2 every simple ring of three generators of F22 is colorable | 0.85 | holds, 0 zero-trace cyclic triples of 68,808,751 | `results.json` R2 |
| R3 trace criterion and CaDiCaL agree on 500 random rings | validation | 500 of 500 | `results.json` R3 |
| R4 `G52` split gives a zero diagonal in six sectors, ten splits | control | yes | `results.json` G2 |

## Zero-trace rings

None, in R1 or R2. The `zero` procedure (rebuild the ring, CaDiCaL DRAT proof checked by drat-trim, second solver on the second
encoding, girth, exact cyclic connectivity) therefore ran on no ring. It was exercised on `G52` as a self-test: CaDiCaL UNSAT,
84,639,361-byte proof verified by drat-trim (commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` of
https://github.com/marijnheule/drat-trim, built in WSL), Glucose 4 on the second encoding also non-colorable, `G52` simple cubic of
girth 5, cyclic edge connectivity 4 (CNF SHA-256 `a0b5cf32...ccbd8d`, proof SHA-256 `297b5a74...ffe8e`).

## Adversarial validation record

- Packed trace test against `transfer.product` and `colorable_sectors`: unit test on all 78 pairs of the 12 generators of `P`, 60
  random pairs, a perturbed family with zero-trace pairs for the bulk path; 200,000 random pairs in the run (0 mismatches).
- Positive control: the criterion finds zero diagonals on `G52` (R4); the explicit solver confirms `G52` non-colorable with a
  checked proof (self-test).
- Second encoding and second solver on 30 random blocks (G1) and on the block of `P` (unit test).
- Accounting: 3,057 of 3,057 blocks, 34,380 generators, 591,009,390 pairs, 1,836,486 non-simple pairs of triples, 0 undecided.
- Matrix entries are models checked from the definition; a missing entry could only shrink a diagonal, so a nonzero diagonal
  proves colorability and the positive statements are sound (hypothesis, Soundness).

## How could this be wrong?

1. The float32 matrix product is exact for 0/1 entries up to 4,489 terms, and was checked against the integer path and the packed
   path on samples, not on all pairs; a bug in a rarely used branch (the chunk edges) would show as a spurious nonzero. The only
   dangerous direction is a spurious nonzero diagonal. Mitigation: the `hits-F.npy` table is kept and the 200,000-pair sample plus
   500 solver-checked rings found no mismatch.
2. The blocks come from one solver (CaDiCaL) for all 3,057 blocks; the second solver covered 30 of them plus `P`. A systematic
   defect in a block family not sampled could add missing or false entries; false entries cannot arise (each is a checked model),
   missing entries only reduce traces, so the claim stands.
3. Order 28 is restricted to distance 5 (F28d5) as frozen; rings with shorter blocks of order 28 were not examined, and orders 30 and
   above were out of scope. R1 is a statement about F, not about all cyclically 5-edge-connected snarks of order at most 28.
4. Orientation and junction coverage rest on the 12 generators; the unit test and R3 build the same rings through `build_ring`.
5. R3 contains only colorable rings, so it cannot detect a criterion that is too permissive; R4 and the `G52` self-test cover the
   non-colorable side for one graph.

## Consequence for PCC-F6 and Problem 11

No counterexample to the Petersen coloring conjecture arises from rings of two superedge blocks of F (orders 16 to 52) or of three
over F22 (orders 24 to 60); the transfer relation of these blocks always meets after some junction. This is evidence, not a proof:
it covers one family of superpositions. Next bounded actions: rings of three over larger families, blocks with a different split
of the six dangling ends (the 10 splits), and superedge blocks cut from order-30 snarks.

## Limitations

- **Second solver.** MiniSat 2.2 in python-sat 1.9.dev22 on this device exits with an access violation (exit code 3221225477) in
  `solve`: with assumptions as in EXP-014 (G1 failed 0 of 30, `run-log.txt` 22:57), and with the left triple fixed by unit clauses
  it still crashed on 28 of 30 blocks (23:04). Glucose 4 (a MiniSat derivative, code independent of CaDiCaL) was used instead
  (`EXP015_SECOND_SOLVER` selects another); the same encoding and the same G1 and zero-trace procedures. The hypothesis names MiniSat 2.2, so this
  is a deviation to be accepted or rerun on a device where `minisat22` is stable. The unit test of `second_encoding_matrices` uses
  the default solver.
- The data manifest lists the top-level files of the data root; the `zero/` folder (the `G52` CNF and DRAT proof) holds the hashes
  above and is not listed there.
- The blocks run took 2 h 8 min on a loaded machine; the final `all` run took 4 h 55 min (23:20 to 04:15).
