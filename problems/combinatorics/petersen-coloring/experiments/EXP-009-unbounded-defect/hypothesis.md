# EXP-009 - exact Petersen defect and abnormal-edge number of rings and frames of counterexamples

Declared 2026-09-18 before any experiment code was run. Round 2. Backlog PCB-023.

## Question

`context/2026-09-18-defect-unbounded.md` proves `[D]` that a ring of `t` counterexamples joined
through 2-edge cuts, and a cubic frame on `t` vertices whose vertices are replaced by
counterexamples minus a vertex, have Petersen defect `pd >= t` and least number of abnormal edges
`ab >= pd` (Lemma 1: `pd <= ab`). Are the bounds attained on the smallest instances built from
`G52`, and do the machine checks agree with the theorems?

## Fixed objects

- `R_t`: ring of `t` copies of `G52`, each opened at edge index 0 of the sorted edge list,
  `t = 2, 3, 4` (104, 156, 208 vertices).
- `K_4[G52]`: the frame `K4` with each vertex replaced by `G52` minus vertex 0 (204 vertices).
- Controls: the same constructions on the Petersen-colorable flower snark `J5` (rings `t = 2, 3`
  and the `K4` frame).

## Falsifiable predictions

- P1 (controls). Rings and the `K4` frame of copies of `J5` are Petersen colorable (SAT at bound 0,
  checker defect 0). Reason: use one Petersen coloring of `J5` on every copy of a ring, so that all
  ring edges carry the label of the opened edge; for the frame, color `K4` by the three edges of
  one star `S` of `P`, and compose the coloring of each copy with an automorphism of `P` sending
  the star at the removed vertex onto `S` with the required bijection (the stabilizer of a vertex
  of `P` induces the full symmetric group on its three edges).
- P2 (structure). `R_t` is simple, cubic, bridgeless with edge connectivity 2; `K_4[G52]` is
  simple, cubic, with edge connectivity 3 (measured by `pcclib.invariants`).
- P3 (upper bounds, the content). Committed expectation: `pd(R_t) = t` for `t = 2, 3, 4` and
  `pd(K_4[G52]) = 4`: the cardinality-bounded Petersen encoding at bound `t` is SAT and the
  independent checker counts exactly `t` bad vertices, one in each copy. Moderate confidence (it
  rests on the universal 2-criticality of `G52`, which suggests that one bad vertex per copy plus
  the transmitted disagreement suffices). A SAT answer only at a larger bound refutes the
  expectation and is recorded.
- P4 (abnormal edges). `ab(R_t)` and `ab(K_4[G52])`: bound `t` SAT is the committed expectation
  (low confidence; `ab(G52) = 2` while a single copy opened at an edge may need one abnormal
  edge). The least satisfiable bound up to `2t` is reported with the checker count.
- P5 (consistency with the theorems). For `R_2`, twenty designated pair relaxations with both
  relaxed vertices in the same copy are UNSAT with verified proofs (Theorem 2 forces a bad vertex
  in the other copy). A SAT answer here would refute Theorem 2 or the encoder.

## One-sidedness

Lower bounds are theorems (`[D]`), not computations; P5 is an independent machine check of one
consequence. Upper bounds are explicit witnesses counted by `checkers.petersen_defect` and
`checkers.normal_defect` from the graph alone.

## Premise dependencies

EXP-001 (no Petersen coloring of `G52`), EXP-004 encoders with `defect_bound`, EXP-006 relaxed
encoders; the parity theorem.

## Invariant-first note

The lower bounds are the invariant; only attainment needs search.

## Compute budget and kill criterion

CPU only; 30 minutes per instance; 3 hours overall; an instance that times out is reported as
undecided and the least satisfiable bound is then an upper bound only.

## Verdict rules

CONFIRMED if P2 and P5 pass and P3 is decided for `R_2` and `R_3` at least; refuted expectations
are preserved with their values.

## Addendum 1 (2026-09-18 12:39), before the instances named here ran

The cardinality instance `pd(R_4) <= 4` hit the 30-minute limit on a saturated machine; bound 5
is SAT (checker defect 5, two bad vertices in one copy). To decide whether 4 is attained, a
witness search by designated relaxation is added: relax exactly one vertex in each copy (the
local indices of the bad vertices found for `R_3` and `R_4`, a few combinations), which is fast
when satisfiable. A SAT answer with checker defect 4 gives `pd(R_4) = 4`; UNSAT answers decide
nothing about `pd(R_4)`. Budget 10 minutes per combination, at most 12 combinations.
