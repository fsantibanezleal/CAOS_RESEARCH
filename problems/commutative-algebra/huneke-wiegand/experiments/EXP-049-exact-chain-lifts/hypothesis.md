# EXP-049 hypothesis - exact completion-chain lifts and parity duals

Date: 2026-09-02. Status at declaration: **DECLARED, NOT RUN**. CPU-only exact integer and binary
arithmetic.

## Question and motivation

Do the four explicit EXP-048 completion chains themselves represent exact order-two classes in the
relative integer cokernels, and can two independent dual parity characters certify their
nontriviality without a full Smith reduction?

This is the smallest decisive action under HWB-075. A Bockstein representative is only defined
modulo the relative image and may differ from a literal order-two chain by an even correction.
EXP-049 tests the stronger literal statement and reconstructs source-domain witnesses when it is
true.

## Predictions fixed before computation

- **P1 (exact chain lifts):** for every `p=8,...,11` and each of the two displayed chains in each
  stable completion, the exact lattice equation `R y=2a` has an integer solution. Direct
  multiplication must verify all sixteen equations.
- **P2 (source-domain realization):** mapping each `y` through the saturated integer kernel of the
  mask-58 source presentation gives an integer vector `x` satisfying `A x=0` and `B x=2a`
  exactly. The finite witness support is predicted to use only the four persistent source-column
  atoms already present in EXP-042, with no new semantic atom at larger `p`.
- **P3 (dual independence):** for each inclusion and parameter, there are two binary row
  functionals `ell_1,ell_2` with `ell_i R=0` and

  ```text
  ell_i(a_j)=1 if i=j, and 0 otherwise.
  ```

  The deterministic low-pivot and independent high-pivot solvers must agree on the four pairings
  and on annihilation, though their chosen functional supports need not agree.

P1 is the high-risk prediction. P2 and P3 are retained as explicit certificate obligations, not
inferred from the previously computed Smith diagonal.

## Method

1. Verify the pinned EXP-042, EXP-047, and EXP-048 inputs.
2. Rebuild each `alpha/beta` zero-one vector directly from its displayed semantic formula and
   require equality with the frozen EXP-048 representative.
3. Compute a transformed row Hermite form of `R^T`. Reduce `2a` against its nonzero rows. On exact
   division and zero remainder, map the HNF coordinates through the unimodular transform to obtain
   `y`, then verify `R y=2a` by sparse integer multiplication.
4. Recompute the saturated kernel of the mask-58 source matrix and form `x=yK`. Verify the source
   and added-row equations directly in the original signed matrix.
5. Solve `R^T ell=0` together with the two pairing equations over `F_2`, once with low pivots and
   once with high pivots. Verify every returned certificate against the raw sparse columns.
6. Store sparse witnesses, coefficient bounds, atom histograms, hashes, timings, and checkpoints.

## One-sidedness

- A **PASS of P1** proves only that the four displayed chains have order dividing two in every
  tested relative cokernel. Together with P3 it proves exact order two and independence on the
  tested range. It does not prove the formulas or the cokernel upper bound for every `p`.
- A **FAIL of P1** proves that at least one displayed Bockstein chain needs a nonzero even
  correction before it is an integral torsion representative. It redirects the proof target but
  does not remove the underlying `(Z/2)^2` found by EXP-047.
- A **PASS of P2** makes the finite witnesses explicit in the original source-domain coordinates.
  It does not by itself give an all-parameter formula.
- A **FAIL of P2** indicates a reconstruction or premise failure, because a valid `y` in the
  relative presentation must map through the saturated source kernel.
- A **PASS of P3** proves finite nontriviality and independence of the two named chains. A failure
  contradicts EXP-047/048 or the formula reconstruction and stops the run.

## Premise dependencies

- EXP-042 CONFIRMED FINITELY: exact signed isolated matrices.
- EXP-045 REFUTED with retained classification: stable carrier inclusions `58->59` and `58->62`.
- EXP-047 CONFIRMED FINITELY: exact relative modules with torsion `(Z/2)^2`.
- EXP-048 REFUTED with retained formulas: exact finite `alpha/beta` row supports and Bockstein rank
  two.
- **Hypothesis:** the literal zero-one chains have exact order two, rather than only representing
  the correct Bockstein cosets.

## Invariant-first note

Exact column-lattice membership of `2a` decides P1 directly. Another coefficient, field rank,
Bockstein rank, or full Smith form cannot answer this sharper question more cheaply.

## Compute budget and stop conditions

- Smoke: `p=8`, at most 300 seconds and 10 GiB.
- Full range: `p=8,...,11`, at most 2,400 seconds and 24 GiB, with an atomic checkpoint after each
  inclusion.
- Stop immediately on a premise hash mismatch, semantic support mismatch, failed exact division,
  exact multiplication mismatch, source-annihilation failure, or dual-audit disagreement.
- A budget stop yields `INCONCLUSIVE_RESOURCE_BUDGET` and no positive conclusion.

No manuscript or Zenodo update is authorized by declaration. The trigger remains a uniform
source-cycle/dual construction plus an all-parameter upper argument, or a comparably transferable
theorem.
