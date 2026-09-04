# EXP-005 - counterexamples below 52 vertices built from disjoint copies of the Petersen 4-pole

Declared 2026-09-03 before experiment code was run. Phase PC-P6. Backlog PCB-009 (rescoped).

## Question

Let `F` be the 8-vertex 4-pole obtained from the Petersen graph by deleting the endpoints of one
edge. Every known counterexample to the Petersen coloring conjecture contains `F` as a
submultipole (GJMMM Section 5 `[V]`), and the retrievable ones decompose as `k` disjoint copies
of `F` plus `m` further vertices with `8k + m = n`: `G52` has `n = 52`, so `(k, m) = (6, 4)` if it
contains six disjoint copies (to be measured here). Define the class `C(k, m)` of simple cubic
bridgeless graphs whose vertex set is `k` disjoint copies of `F` (with their internal edges)
plus `m` free vertices, with the `4k + 3m` semi-edges joined by a perfect matching. Does any
graph in `C(k, m)` with `38 <= 8k + m <= 50` fail to have a Petersen coloring?

## Method (exact, counterexample-guided)

The class is finite. A join formula `J(k, m)` has one variable per admissible pair of semi-edges
(exactly one join per semi-edge; no loop at a free vertex; no double edge between two free
vertices, nor between two semi-edge owners already adjacent inside a copy of `F`). The search
alternates:

1. solve `J` for a matching `M` (CaDiCaL); `J` UNSAT means the class is exhausted;
2. build the graph `G_M`; if it is disconnected or has a bridge, add the sound clause "some join
   leaves the offending side other than the bridge" and continue;
3. decide Petersen colorability of `G_M` with `pcclib.encoders.petersen_coloring` (EXP-001
   route); if UNSAT with a verified DRAT proof, `G_M` is a counterexample: record it, also refute
   it with the normal-5 encoding, and continue with a clause excluding this exact matching;
4. if SAT with coloring `lambda`, every matching whose joined pairs all carry equal labels under
   `lambda` is colorable by the same coloring (each copy of `F` and each free-vertex star keeps a
   valid star map regardless of what it is joined to), so the clause "some joined pair has
   unequal labels" is sound; add it, plus the same clause for the colorings obtained by applying
   one automorphism of `F` to one copy or one permutation of the three labels at one free vertex
   (each is again a valid coloring of the same gadgets), and continue.

Every learned clause is logged with the witness (coloring or cut) that justifies it, so the
final "class exhausted" claim is auditable: an auditor re-verifies each witness on its gadgets,
then re-checks the final UNSAT of `J` plus all learned clauses (DRAT proof kept).

## Fixed objects

`F` from `pcclib.graphs.petersen_minus_adjacent_pair`; encodings from `pcclib.encoders`;
checkers from `pcclib.checkers`; the search in `pcclib.compose`. Classes are run in this order
with the budget below: `(5,0)`, `(5,2)`, `(5,4)`, `(6,0)`, `(6,2)`, `(5,6)`, `(5,8)`, `(5,10)`,
`(4,6)`, `(4,8)`, `(4,10)`, `(4,12)`, `(4,14)`, `(4,16)`, `(4,18)`.

Controls: `(4,4)` (36 vertices; must exhaust with no counterexample, consistent with the census
`[V]`), `(2,0)`, `(3,2)` (small, must exhaust quickly), and the positive control `(6,4)` (must
find a counterexample if `G52` lies in `C(6,4)`, which the run measures first by counting the
disjoint copies of `F` in `G52`).

## Falsifiable predictions

- P1: `(2,0)`, `(3,2)`, `(4,4)` exhaust with no counterexample, `(4,4)` within budget.
- P2: `G52` contains six disjoint copies of `F` (measured by exhaustive induced-subgraph search
  with boundary 4); then `(6,4)` finds a counterexample within budget, and the first one found
  is refuted with a verified proof by both encodings.
- P3 (the question): committed expectation, low confidence: no class with `8k + m <= 50` in the
  list contains a counterexample, each exhausting within budget. A found counterexample below
  52 vertices REFUTES this expectation and is the headline result (new smallest known
  counterexample, subject to the full adversarial ladder before any claim).
- P4: every learned clause's witness re-verifies on its gadgets under an independent checker
  that reads only the gadget graphs and the labeling.

## One-sidedness

"Class exhausted" is a theorem about `C(k, m)` only. It says nothing about counterexamples that
contain fewer copies of `F`, or none. A found counterexample is a positive certificate.

## Premise dependencies

- EXP-001 CONFIRMED (the Petersen encoding refutes and accepts correctly).
- The soundness of the coloring clause is derived above (star maps are local); it is exercised
  by the `(4,4)` control, which must not exclude a colorable... it must terminate with UNSAT,
  and by P4.

## Invariant-first note

No single invariant decides colorability of a composition; the P-coloring sets of the gadgets
are the invariant that the CEGAR loop exploits.

## Compute budget and kill criterion

CPU only. Per class: 2 hours wall or 20,000 iterations, whichever first; a class stopped at
budget is INCONCLUSIVE with its iteration count and the number of learned clauses recorded.
Whole experiment: 24 hours. Checkpoint: the learned clauses and witnesses are appended to a
JSONL file per class after every iteration, so a stopped class resumes.

## Verdict rules

- CONFIRMED if P1, P2, P4 pass and every listed class is decided (exhausted or a counterexample
  found), whatever P3's outcome.
- REFUTED (of P3, reported as the headline) if a counterexample below 52 vertices is found and
  survives both encodings.
- INCONCLUSIVE if any listed class hits its budget; partial classes are reported as such.
