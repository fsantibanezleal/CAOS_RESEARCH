# EXP-052 hypothesis - semantic formula for the two-column exact lift

Date: 2026-09-03. Status at declaration: **DECLARED, NOT RUN**. CPU-only exact reconstruction.

## Question

Can the exact two-column representatives exposed by EXP-051 be described by a parameterized
semantic row formula rather than elimination indices?

## Predictions fixed before computation

- **P1 (bounded vocabulary):** in each inclusion, the normalized training rows for the unique
  primary two-column witness use at most twelve coefficient-sensitive numeric skeletons across
  `p=8,9,10`.
- **P2 (formula extraction):** the complete training multisets admit a deterministic formula built
  from affine endpoint tokens and integer intervals, recorded in `candidate.md` and committed
  before any semantic reconstruction at `p=11`.
- **P3 (untouched holdout):** that frozen formula reproduces the complete coefficient-token
  multiset at `p=11` for both inclusions, while the stored two-column cycle continues to satisfy
  `Rz=2b` exactly and represents a nonzero quotient class.

## Method

1. Verify the frozen EXP-047, EXP-048, and EXP-051 hashes.
2. Reconstruct labelled components only for `p=8,9,10` and select the unique primary record with
   cycle support two.
3. Store exact labels, normalized tokens, coefficients, hashes, and direct matrix identities.
4. Infer a candidate formula from training only, implement it, and commit both before holdout.
5. Reconstruct `p=11`, compare multisets exactly, and repeat with a separate auditor.

## One-sidedness

- Passing P3 proves a finite out-of-sample semantic formula for one exact class in each stable
  completion. It does not prove the formula for every `p` or supply the second class.
- Failure identifies which semantic token family changes and demotes this HNF-section witness; it
  does not invalidate EXP-051's exact finite identities.
- Even a pass leaves the support-four dual lower bound and the free-complement upper bound as
  separate all-parameter obligations.

No manuscript or Zenodo update is authorized by declaration.
