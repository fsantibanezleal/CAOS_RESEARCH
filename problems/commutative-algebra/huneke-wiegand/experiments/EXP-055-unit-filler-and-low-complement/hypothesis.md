# EXP-055 hypothesis: uniform unit filler and low-complement source coordinates

Declared: 2026-09-04, before computation. Exact integers, CPU only.

## Question and frozen predictions

EXP-054 finds just one omitted row in each full boundary at `p=8,9,10`:

`M z_p = 2(b_A+b_B) + 2(-1)^p e_p`,

where `L_p=[1,p] union [3p,4p-2]`, `F_p=L_p minus {2,3p}`, and
`e_p=[K,F_p;13p]`. This finite residual suggests a uniform repair and a smaller proof language.

- P1: for every `p>=4`, `c_p=[K,F_p union {7p};6p]` has boundary `-e_p`.
  Thus the saved finite chains corrected by `2(-1)^p c_p` have exactly the desired full
  boundary. Verify the symbolic interval proof independently and test `p=4,...,100`.
- P2: retaining only the saved `S`-type source terms with high exterior set `{6p,10p}`
  still gives exactly `2(b_A+b_B)` on all `D` rows at `p=8,9,10`. Record its complete
  remaining `K` boundary rather than declaring it zero. This isolates a bounded-missing-set
  low Koszul problem without assuming that a row mask is a subcomplex.
- P3: the signed exterior-complement identity holds for all subsets of ordered universes
  of size at most eight, and the primary boundary/correction passes an independent checker.

The fixed-high slice is a decomposition by an invariant of the low differential, not a new
HNF basis. No bound on its support or number of semantic templates is predicted.

## Symbolic preflight and premises

EXP-036's exact coefficient module gives
`6p+[1,p] subset H_p` and `6p+[3p,4p-2] subset H_p`, so all low faces of `c_p` vanish.
Both `6p,7p` are in `H_p`, while `13p` is in degree two. The only surviving face is the
last exterior position `|F_p|=2p-3`, which has sign minus. This is an elementary family-specific
unit filler, not a new general Morse theorem.

EXP-054 owns the three finite residuals; EXP-053 owns the saved projected source coordinates;
EXP-052 owns the frozen target formulas. Its `p=11` source holdout remains unopened.
The complete Skoldberg paper https://arxiv.org/html/1311.5803v1 has been read, including the
chain-map and final homotopy-equivalence statements. No source settles the generic CAOS lift.

## Invariant first, PASS/FAIL meaning, and resource budget

The invariant-first calculation is a single column, not a new Smith computation. PASS on P1
establishes the stated uniform filler by the written proof and repairs the three known source
identities. It does NOT supply a generic formula for `z_p`, another torsion class, or an upper
bound. P2 PASS only validates a source slice and its remaining correction obligation finitely.
P1 FAIL would refute the proposed filler; P2 FAIL would refute the fixed-high decomposition as
implemented. P3 is a sign/provenance audit, not an all-parameter homology theorem.

Budget: 60 seconds, one CPU process, 1 GiB private memory; expected runtime under ten seconds.
Flush progress and checkpoint after each parameter block. Stop on a premise mismatch or exact
disagreement and preserve partial output. No HNF, complete-basis enumeration, or new parameter
source reconstruction. Tests and reruns use temporary output paths.

## Exploration and manuscript decision

New viewpoint: replace nearly full low exterior sets by their bounded-size missing sets with
the exact shuffle sign. Keep coefficient multiplication and high variables explicit. A later
experiment may seek signed subset-incidence recognition or a local dual relation in this model.
The elementary filler alone does not satisfy the stronger current manuscript-split gate.
