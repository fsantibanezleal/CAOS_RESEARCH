# EXP-056 hypothesis: uniform low-source identity

Declared: 2026-09-04, before new parameter evaluation. Exact integers, CPU only.

## Frozen formula and predictions

Let `L_p=[1,p] union [3p,4p-2]` and

`T_p(a,j;c)=[S,(L_p minus {a,3p,3p+j}) union {6p,10p};c]`, with `c=a+j-2`.

The half of the fixed-high EXP-055 source has the following candidate formula:

$$s_p=\sum_{a=1}^{p-4}(-1)^{a+1}T_p(a,2;a)
+(-1)^{p+1}T_p(p-3,2;p-3)
+2(-1)^{p+1}T_p(p-2,1;p-3)
+2(-1)^pT_p(p-3,1;p-4).$$

- P1: for every `p>=8`, the `D` part of `M_p s_p` equals the frozen EXP-052
  `b_p^A+b_p^B` formula. Prove this by collecting each row coefficient, not by extrapolation.
- P2: the full boundary is `M_p s_p=b_p^A+b_p^B+gamma_p`, where `gamma_p` is the negative
  of the same weighted terms with source replaced by
  `[K,(L_p minus {a,3p,3p+j}) union {6p};10p+c]`.
- P3: recover exactly half the saved fixed-high sources at `p=8,9,10`, test the formulas at
  `p=8,...,100`, and pass independent arithmetic plus deliberate sign-corruption controls.

The new parameters are a stress test of a written identity, not an untouched HNF-source holdout.
The original `p=11` source data remain unopened.

## Premises and source-complete preflight

EXP-055 owns the fixed-high extraction; EXP-052 owns the target candidate formula; EXP-036/037
own the coefficient module and original differential. EXP-054 refutes a naive source lift but
does not contradict this separate `D` identity. No generic HNF source formula is assumed.

The relevant source sections and final chain-map proof in
https://arxiv.org/html/1311.5803v1 were read in this round. The identity here is rederived from
the explicit coefficient module. Standard Koszul insertion/deletion gives a proof language,
not a theorem about the CAOS parity quotient imported from the literature.

## Invariant-first proof outline

For an A row with missing low indices `a<b`, the coefficient is
`(-1)^b w_j(a)+(-1)^(a-1)w_j(b)` if `a+b+j-2>p`, and zero otherwise. Interior terms cancel.
For B rows, use the single deleted second-low index and threshold `v+c>=4p-1`.
The high `6p` face vanishes; the last `10p` face has sign minus. These local identities
decide the full formula without matrix ranks.

## PASS/FAIL meaning, resources, and publication

PASS with the symbolic proof establishes a uniform source identity and the integral cokernel
relation `[b_A+b_B]=-[gamma_p]`. It does not establish that this class is nonzero, killed by
two for every `p`, or the whole parity quotient. FAIL refutes the proposed formula and keeps
only the finite EXP-055 extraction. A finite sweep alone cannot confirm P1.

Budget: 60 seconds, one CPU process, 1 GiB private memory. Checkpoint and flush after each
parameter; stop on a premise mismatch, independent disagreement, or budget exhaustion. No HNF
or full original basis enumeration. Persist compact parameter hashes and counts, not repeated
large row sets. Tests use temporary files.

Exploration: move the all-parameter target to the explicit `p-1`-row K-side chain `gamma_p`,
using bounded missing-set coordinates and keeping the exact primal, dual and upper-bound gates
separate. Reassess manuscript novelty honestly; a uniform differential identity alone does not
resolve the connecting-parity problem or automatically meet the stronger publication trigger.
