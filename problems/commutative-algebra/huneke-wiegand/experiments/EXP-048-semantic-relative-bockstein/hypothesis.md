# EXP-048 hypothesis - semantic relative Bockstein coordinates

Date: 2026-09-02. Status at declaration: **DECLARED, NOT RUN**. CPU-only exact integer and
binary arithmetic.

## Question and motivation

EXP-047 proves exact finite Smith forms for the three decisive row inclusions, but its transformed
Hermite kernel basis is arithmetic rather than semantic. Can the factor-two part of each relative
module be represented by normalized interval coordinates that persist under `p -> p+1`?

This is the smallest current test of HWB-074. It acts on the exact relative matrices already
computed, reconstructs their original added-row labels independently, and computes the relative
first Bockstein as a subspace of the mod-two cokernel. It does not compute another coefficient.

## Predictions fixed before computation

- **P1 (regression):** the relative Bockstein ranks are `2`, `2`, and `p-7` for `58->59`,
  `58->62`, and `56->58`, respectively, at every `p=8,...,11`.
- **P2 (stable completions):** after lexicographically ordering the normalized added-row
  coordinates and taking the canonical quotient-reduced row-echelon basis, each completion has a
  bounded-support two-vector Bockstein basis whose normalized support-template multiset is
  independent of `p`.
- **P3 (threshold family):** the `56->58` canonical basis consists of one translation family
  indexed by `1,...,p-7`, with no exceptional template whose number grows with `p`.

Here a normalized row coordinate records the missing elements of `L0=[1,p]`, the missing elements
of `L1=[3p,4p-2]` relative to both endpoints, the selected high-interval elements relative to both
endpoints, and the low-product row value relative to `p`. A template may contain one declared
integer translation index; all remaining fields must be constant.

## Method

1. Verify the frozen EXP-042 matrices and EXP-047 relative artifacts by SHA-256.
2. Independently reconstruct the full labelled `(p,2)` combined presentation and repeat the
   integral leaf/component extraction. Select the unique component with the frozen support hash.
3. Match every relative artifact row to its exact added-row label and verify its stored row hash.
4. For each relative integer matrix `R`, compute `ker(R mod 2)`. For every binary cycle `z`, form
   `(Rz)/2 mod 2`, reduce it modulo `im(R mod 2)`, and row-reduce the resulting classes in a fixed
   semantic row order.
5. Repeat with reversed relation-column traversal. Canonicalize both outputs in the same semantic
   coordinate order and require identical image-subspace certificates.
6. Emit every canonical representative and its normalized row coordinates. Classify P2 and P3 by
   the definitions above without discarding exceptions.

## One-sidedness

- A **PASS of P1** only reproduces the already proved finite torsion rank by a different invariant.
- A **PASS of P2 or P3** supplies a concrete finite semantic template and a candidate transition
  map for the next symbolic proof; it does not prove the formulas for all `p`.
- A **FAIL of P2** proves that the fixed canonical quotient section does not expose a stable bounded
  completion template. It does not rule out a different unimodular basis.
- A **FAIL of P3** rules out the proposed single translation-family description in this canonical
  section and redirects HWB-074 to dual parity characters or a relative Morse matching.

## Premise dependencies

- EXP-042 CONFIRMED FINITELY: the isolated matrices and their first-Bockstein ranks are frozen.
- EXP-043 CONFIRMED FINITELY: the tested rational-rank ceilings are exact.
- EXP-045 REFUTED with retained result: masks `59` and `62` are the stable minimal full carriers,
  with intersection `58` and threshold core `56`.
- EXP-047 CONFIRMED FINITELY: the three compact relative matrices have exact elementary
  factor-two torsion of ranks `2`, `2`, and `p-7`.
- **Hypothesis:** semantic normalization of the added rows is fine enough to reveal compatible
  representatives. No prior verdict establishes this.

## Invariant-first note

The first Bockstein is the cheapest invariant that separates free mod-two cokernel directions from
integral factor-two torsion. Rank, Smith factors, support connectivity, atom masks, and unit leaves
have already been exhausted by EXP-042--047. Computing a full transformed Smith form would be more
expensive and would obscure, rather than improve, the semantic test.

## Compute budget and stop conditions

- Smoke: `p=8`, at most 180 seconds and 8 GiB, with flushed reconstruction stages and an atomic
  checkpoint.
- Full range: `p=8,...,11`, at most 900 seconds and 12 GiB.
- Stop immediately on a premise-hash mismatch, a non-even lifted boundary, a row-label hash
  mismatch, a frozen support/rank mismatch, or disagreement between traversal audits.
- A budget stop is `INCONCLUSIVE_RESOURCE_BUDGET`; it does not support or refute P2/P3.

No manuscript or Zenodo update is authorized by declaration. The publication gate remains an
all-parameter normal form, compatible chain model, or comparably transferable theorem.
