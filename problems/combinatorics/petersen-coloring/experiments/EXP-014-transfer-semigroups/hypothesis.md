# EXP-014 - transfer semigroups of 6-poles: every ring of a block family at once

Declared 2026-10-06 before any code of this experiment was run. Focus PCC-F6
(`program/petersen-coloring/research-governance.json`), second bounded action, opened by the
EXP-013 outcome. Theory: `context/2026-10-06-charges.md`, section "Transfer relations".

## Why this experiment

EXP-013 measured the conducted charge orbits of every 6-pole of `P`, `J5`, `J7` and the
dodecahedron (shapes a and b): all of them conduct the core `{0, E, D2}`. The charge obstruction of
EXP-012 (two blocks with disjoint conducted sets) therefore never fires on blocks cut from
Petersen-colorable graphs, and a ring of such blocks can only fail to be colorable through the
finer structure of its boundary labels. This experiment computes that finer structure exactly.

## The object

A 6-pole `M` with its six dangling ends split into an ordered left connector `L` and an ordered
right connector `R` has the transfer relation
`T_M = {(phi(L), phi(R)) : phi a map of M into E(P) with every vertex good}`, a subset of
`E(P)^3 x E(P)^3`. Joining the right connector of `M_i` to the left connector of `M_{i+1}` through a
junction permutation `pi_i` (end `j` of `R` to end `pi_i(j)` of `L`) and closing the cycle gives a
ring; it is Petersen colorable if and only if the boolean matrix product
`T_1 Pi_1 T_2 Pi_2 ... T_t Pi_t` has a nonzero diagonal entry.

Two reductions, both consequences of results already in the record:

1. Gauss law: the left and right labels of every good map have the same charge class, and a
   junction permutation preserves the class. So every transfer matrix is block diagonal over the 64
   classes, and so is every product.
2. `Aut(P)`-equivariance: the blocks over the classes of one orbit are conjugate, and conjugate
   blocks have the same trace. So a block family is fully described by six sector matrices, one per
   orbit `0, E, D3, D2, T1, T2`, of sizes 60, 67, 48, 48, 30, 60 (ordered label triples per class).

The ring is colorable if and only if some sector product has a nonzero diagonal. The set of all
sector products of a finite block family is a finite semigroup; computing its closure decides the
colorability of every ring of the family, of every length, at once.

## Soundness and certificate

Entries of the sector matrices are SAT witnesses checked from the definition (all vertices good);
missing entries are only under-approximations, so a positive trace computed from them is a proof.
The closure is kept as an antichain under inclusion (an element containing a stored one is
dropped: any zero-trace continuation of it is also one of the smaller element). The certificate of
"every ring of length at least 2 is colorable" is a set `C` of sector-matrix tuples such that

- every product of two generators contains an element of `C`;
- for every `c` in `C` and every generator `g`, `c g` contains an element of `C`;
- every element of `C` has a nonzero diagonal in some sector.

By induction on the word length every product of at least two generators then contains an element
of `C` and has a nonzero diagonal. `check_certificate.py` re-verifies the three conditions from the
stored generators and the stored `C`. A zero-trace word, if found, is rebuilt as a graph and decided
by an external solver with a DRAT proof checked by drat-trim before anything is claimed.

## Fixed objects (block families)

Each block enters in both orientations, each followed by each of the six junction permutations (12
generators per block, duplicates removed).

- `Y`: the claw (a center and three leaves, each leaf with one end in `L` and one in `R`). The
  rings of claws include every flower snark: `J_k = (Y id)^(k-1) (Y tau)` with `tau` a transposition.
- `S`: the Petersen superedge `P - u - w` (`u`, `w` at distance 2), `L` = the ends at `u`, `R` =
  the ends at `w` (the superedge `(P10)_{u,v}` of Sedlar and Skrekovski, arXiv:2305.05981).
- `Pb`: the four `Aut(P)`-orbits of `P - e1 - e2 - e3` (three pairwise disjoint edges), all ten
  splits each (40 blocks).
- `Ja5`, `Ja7`, `Da`: shape (a) of `J5` (14 blocks), `J7` (21 blocks), the dodecahedron (4 blocks),
  natural splits (the ends at `u` against the ends at `w`).

Families: `F1 = {Y}`, `F2 = {S}`, `F3 = {Y, S}`, `F4 = Pb`, `F5` = all 81 blocks.

## Falsifiable predictions

- Q1 (validation, high confidence): the closure of `F1` is reached and every element has a nonzero
  diagonal, so every ring of claws of length at least 2 is Petersen colorable; in particular every
  flower snark (agrees with Hagglund and Steffen, Ars Math. Contemp. 7 (2014) 161-173).
- Q2 (moderate confidence, 0.8): the same holds for `F2`: every ring of Petersen superedges is
  Petersen colorable.
- Q3 (the question; committed expectation 0.9 that it fails): some word of length at least 2 over
  `F5` has a zero diagonal in all six sectors (a non-colorable ring of blocks cut from cyclically
  5-edge-connected graphs). If it holds: the ring is built, its simplicity, girth and cyclic edge
  connectivity are measured (exhaustive search for cycle-separating cuts of at most four edges),
  and its non-colorability is certified by a checked proof. A cyclically 5-edge-connected one
  answers Problem 11 of arXiv:2608.10028v4; that follow-up is declared as EXP-015 before it runs.
- Q4 (consistency, high confidence): for 200 random words of length 2 to 6 over `F5`, the explicit
  ring graph's colorability decided by CaDiCaL (proof-checked when UNSAT) agrees with the trace
  answer in every case.

## One-sidedness

A reached closure with positive traces is a theorem for the family (with the certificate). A
closure stopped at the cap is UNDECIDED for that family, reported with the explored word length.

## Budget and stop rule

CPU only; at most 60 seconds per block for its sector matrices; closure cap 200,000 elements per
family; 3 hours overall. If Q3 fails with every closure reached, the ring-of-6-poles route over
blocks of Petersen-colorable cyclically 5-edge-connected graphs is closed for these families, and
PCC-F6 is reviewed against its stop conditions before any third experiment.

## Verdict rules

Each prediction PASS, REFUTED or UNDECIDED; the closure sizes, the sector-matrix densities and the
certificates are the output either way.
