# EXP-050 hypothesis - corrected Bockstein lifts with exact provenance

Date: 2026-09-03. Status at declaration: **DECLARED, NOT RUN**. CPU-only exact integer and binary
arithmetic.

## Question and motivation

Can the nonzero even corrections forced by EXP-049 be reconstructed exactly during Bockstein
quotient reduction, and do those corrections have a parameter-compatible semantic form?

For each canonical EXP-048 chain `a`, EXP-050 retains the integral vectors discarded by the
mod-two computation and seeks

```text
b=a+2c,       Ry=2b.
```

## Predictions fixed before computation

- **P1 (exact corrected representatives):** for both completions and every `p=8,...,11`, the
  provenance-preserving Bockstein basis has the same parity subspace as EXP-048 and supplies two
  exact identities `Ry=2b`, with integral nonzero correction `c=(b-a)/2`.
- **P2 (small corrections):** after the fixed semantic low-pivot reduction, every correction has
  coefficients in `{-1,0,1}` and support at most `4p`. This strong prediction is intended to fail
  if the canonical section remains arithmetically opaque.
- **P3 (stable correction complexity):** within each inclusion, the two sorted correction support
  sizes are integer-affine functions of `p` on the complete table, and their normalized row-atom
  histograms are independent of `p`.

## Method

1. Verify frozen EXP-047 through EXP-049 hashes.
2. Reconstruct the semantic added-row order and the four formula supports independently.
3. During mod-two kernel elimination, retain the exact binary source combination `z`.
4. During quotient reduction by an image vector represented by `w`, replace `(b,y)` by
   `(b-Rw,y-2w)`. During Bockstein row reduction, add both exact witnesses whenever parity vectors
   are xored.
5. Require the final parity basis to equal the frozen EXP-048 basis, compute `c=(b-a)/2`, and
   verify every exact multiplication directly from the sparse matrix.
6. Repeat with reversed relation traversal and high pivots as an independent audit of the same
   Bockstein subspace and exact-witness existence.

## One-sidedness

- A **PASS of P1** constructs exact corrected representatives on the tested range. It does not
  prove an all-parameter formula or the cokernel upper bound.
- A **FAIL of P1** exposes an implementation or premise contradiction and stops the round.
- A **PASS of P2/P3** supplies a concrete finite correction template for symbolic extraction.
- A **FAIL of P2/P3** proves only that this deterministic provenance section is not the desired
  simple basis. It redirects to bounded-support solving modulo four, guided by the duals.

## Premise dependencies

- EXP-047 CONFIRMED FINITELY: exact compact relative matrices and `(Z/2)^2` torsion.
- EXP-048 REFUTED with retained formulas: canonical `alpha/beta` parity supports.
- EXP-049 REFUTED with P3 retained: literal zero-one lifts fail and support-at-most-four parity
  duals certify finite independence.
- Hypothesis: the retained exact provenance has uniform semantic complexity.

## Invariant-first note

The exact identity `Ry=2b` plus parity `b mod 2=a` is the decisive invariant. It constructs the
needed object directly; another rank or Smith computation cannot expose the correction.

## Compute budget and stop conditions

- Smoke: `p=8`, 180 seconds, 8 GiB.
- Full: `p=8,...,11`, 900 seconds, 12 GiB, atomic checkpoint per inclusion.
- Stop on frozen hash mismatch, odd boundary, parity-subspace mismatch, exact multiplication
  failure, or primary/audit disagreement about rank.
- A resource stop is `INCONCLUSIVE_RESOURCE_BUDGET`.

No manuscript or Zenodo update is authorized by declaration.
