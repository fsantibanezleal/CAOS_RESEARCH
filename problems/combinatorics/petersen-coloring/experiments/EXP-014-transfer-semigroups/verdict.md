# EXP-014 verdict - CONFIRMED: every ring of claws, of Petersen superedges, or of both is Petersen colorable (finite certificates); the transfer relation sees what charges cannot

Date: 2026-10-06. Hypothesis committed at `36731f89` before any code of the experiment ran;
addendum 1 (the zero-trace control) at `7d21ec5f` and addendum 2 (its cut sizes) at `76745fa8`,
each before the runs it governs. Runner `run.py` (`blocks`, `closure`, `closure --antichain`,
`crosscheck`), `run_g52_control.py`, `check_certificate.py`; library `code/pcclib/transfer.py`;
probes `code/probes/superedge_ring_connectivity.py`, `code/probes/superedge_ring_snarks.py`.
Artifacts under `artifacts/`; sector matrices and certificates under
`E:/_Datos/caos-research/petersen-coloring/EXP-014/`. Theory: `context/2026-10-06-charges.md`,
section 7.

## Result

**The blocks.** 81 blocks, each stored as six boolean sector matrices (sizes 60, 67, 48, 48, 30,
60); the slowest took 202 s. The nonempty sectors of every block equal the conducted orbits that
EXP-013 measured independently for the same 6-pole and split (for example all 14 shape-(a) blocks of
`J5`). The claw `Y` conducts `{0, E, D3, D2, T1}`; the Petersen superedge `S = P - u - w` conducts
`{0, E, D2}`, with 120, 296 and 8 entries in those sectors. Its sector-0 matrix has exactly two
entries in each row: a star at `u` extends in exactly two ways, the two automorphisms of `P` fixing
`u` and its three neighbors.

**The closures (exact, words of length at least 2).**

| family | generators | elements | longest new word | zero-trace elements | elements with a nonzero diagonal in sector |
|---|---|---|---|---|---|
| `F1 = {Y}` | 6 | 30 | 6 | 0 | `0`: 15, `E`: 18, `D3`: 7, `D2`: 9, `T1`: 13 |
| `F2 = {S}` | 6 | 19,005 | 12 | 0 | `0`: 11,230, `E`: 19,005, `D2`: 3 |
| `F3 = {Y, S}` | 12 | 116,463 | 13 | 0 | `0`: 64,854, `E`: 116,451, `D3`: 7, `D2`: 529, `T1`: 13 |
| `F4` (40 `Pb` blocks) | 336 | stopped at the cap of 200,000 at word length 3 | | 0 among those | |

**The closures kept as antichains under containment** (the declared method; a product containing
an active element is dropped):

| family | generators | certificate elements | longest new word | zero-trace elements | time |
|---|---|---|---|---|---|
| `F1` | 6 | 12 | 3 | 0 | under 1 s |
| `F2` | 6 | 276 | 5 | 0 | 5 s |
| `F3` | 12 | 2,454 | 6 | 0 | 349 s |
| `F4` | 336 | not reached: the one-hour limit ended the run inside the products of two generators | | none found | 3,600 s |
| `F5` | 684 | not reached, as for `F4` | | none found | 3,600 s |

**Checks** (`check_certificate.py`, `artifacts/certificate-check-antichain.json`, `artifacts/block-recheck.json`):

- certificates of `F1`, `F2`, `F3`: generators rebuilt from the stored block matrices and equal to the
  certificate's; every product of two generators contains a certificate element; every certificate
  element times every generator contains one; every certificate element has a nonzero diagonal. All
  three PASS, with integer matrix products (the runner uses float32 products).
- block matrices: `Y` and `S` recomputed by brute-force enumeration of maps, equal; 46 of the 81
  blocks (`Y`, `S`, 38 of the 40 `Pb`, 3 of the 4 `Da`, 3 of the 14 `Ja5`) recomputed with a second
  encoding (one variable per vertex image and bijection) and a second solver (MiniSat 2.2), all
  equal; the remaining 35 (2 `Pb`, 1 `Da`, 11 `Ja5`, all 21 `Ja7`) were not reached within the
  90-minute limit of that run. No block differed.

Theorems (computer-assisted; the certificates of `F1` to `F3` re-verified by `check_certificate.py`):

1. Every ring of at least two claws, with any junction permutations, is Petersen colorable. This
   contains every flower snark, `J_k = (Y id)^(k-1) (Y tau)`.
2. Every ring of at least two Petersen superedges `P - u - w`, glued connector to connector with any
   junction permutations and orientations, is Petersen colorable, and always has a coloring whose
   junction charges lie in the orbit `E` (all 19,005 elements have a nonzero `E` diagonal).
3. Every ring mixing claws and Petersen superedges in any order is Petersen colorable.

**Flower snarks carry the all-ones charge.** For `w_k = (Y id)^(k-1) (Y tau)` the sectors with a
nonzero diagonal are `T1` for every odd `k` and `E` for every even `k` (the sequence of products is
periodic from `k = 5` with period 2). `T1` is the class of the all-ones vector of `F_2^E(P)` (the
unique nonzero class fixed by `Aut(P)`); its 30 ordered triples are the orderings of the five triples
of pairwise antipodal edges (distance 3 in the line graph), which partition `E(P)`. Hence: **in
every Petersen coloring of a flower snark `J_k`, `k` odd, the three edges joining two consecutive
claws receive three pairwise antipodal edges of `P`.** The untwisted odd rings `(Y id)^k`
(3-edge-colorable) admit only the class `0` at their junctions.

**Which superedge rings are snarks, and how connected they are** (probes, descriptive). With the
same junction permutation at every junction, the ring of `t` superedges is a snark exactly for odd
`t` with the identity or one transposition (`t = 3, 5, 7` checked; girth 3 at `t = 3`, girth 5 for
`t = 5, 7`); every other uniform ring with `t` from 2 to 8 is 3-edge-colorable. The ring of five
superedges with the identity junction (40 vertices, a snark of girth 5) has no cycle-separating cut
with at most four edges (exhaustive search): it is a cyclically 5-edge-connected snark, so Theorem 2
covers graphs in the class of Problem 11 of arXiv:2608.10028v4. Rings of three and four superedges
with a non-identity junction are cyclically 5-edge-connected of girth 5 as well (3-edge-colorable).

**The zero-trace control (addendum 1, Q5).** `G52` has no 6-edge cut with both sides of at least
20 vertices in a randomized search; a 6-edge cut with sides of 18 and 34 vertices (cut edges 8, 26,
39, 40, 48, 59) gives two colorable 6-poles. For all ten splits of the six cut edges, the ring of
length 2 (which is `G52` again) has a zero diagonal in all six sectors, while the two sides share the
charge orbits `{0, E, D2}` in every split and also `D3` or `T2` in most. The non-colorability of the
counterexample is invisible to charges and fully visible to the transfer relation.

**Cross-check (Q4).** 203 rings (`J5`, `J7`, `J9` rebuilt from claw words and isomorphic to the
flower snarks; 200 random words of length 2 to 6 over all 81 blocks, orders 18 to 132): the sector
trace and CaDiCaL on the explicit graph agree in all 203 cases (all colorable).

## Predictions

| prediction | outcome |
|---|---|
| Q1 (claws, every flower snark) | PASS |
| Q2 (superedges) | PASS |
| Q3 (a zero-trace word over `F5`) | UNDECIDED as a closure (the `F5` and `F4` closures did not finish within their limits); no zero-trace element among the products computed, among the 116,463 elements of `F3`, or in the 200 random rings; the committed expectation (0.9 that none exists) is not contradicted |
| Q4 (random rings agree with the solver) | PASS, 203 of 203; only colorable rings occurred, so Q4 tested one direction |
| Q5 (addendum 1, `G52` split along a 6-edge cut has zero trace) | PASS, all ten splits |

## Consequence for PCC-F6

The success gate of the focus is met in its negative branch: Theorems 1 to 3 rule out the
ring-of-6-poles route for the claws, the Petersen superedge and their mixtures, and the route is
reduced to a precise, decidable question (a block family whose semigroup has a zero-trace element).
The control on `G52` shows that this question is not vacuous: the exact relation detects a
non-colorable gluing that charges cannot. Routed to `unbounded-defect` v0.02 (Section 6), published
2026-10-06, DOI `10.5281/zenodo.23196817`. Next bounded action: EXP-015 (6-poles cut from the
cyclically 5-edge-connected snarks of small order), declared before it runs.

## Limitations

- The theorems rest on computed sector matrices whose entries are checked maps; a missing entry
  could only make a diagonal smaller, so the positive statements are sound, but only `Y` and `S`
  were recomputed by three methods.
- The large families `F4` and `F5` are undecided as closures.
- The descriptive probes (superedge rings: snarks, girth, cyclic connectivity) were not declared
  predictions; they are measurements with exhaustive searches.
