# EXP-052 preflight - semantic formula for the two-column exact lift

Date: 2026-09-03. Scope: HWB-076, stable completions `58->59` and `58->62`.

## Decision question

EXP-051 finds one primary representative supported on exactly two relative kernel columns for
every completion and every `p=8,...,11`. Its divided boundary has height at most two, but raw row
and column indices are not parameter coordinates. The next decision is whether the exact boundary
has a semantic interval formula that predicts an untouched parameter.

## Leakage barrier

The training extractor may reconstruct semantic row labels only for `p=8,9,10`. It writes those
labels and normalized endpoint tokens to a training artifact. A human-readable `candidate.md` and
a deterministic formula generator must then be committed before the holdout command is allowed to
reconstruct any `p=11` label. The already stored EXP-051 support sizes and raw row indices are not
treated as semantic holdout data.

## Premises and invariant

- EXP-047 supplies the frozen exact relative matrices.
- EXP-048 supplies independently reconstructed row labels and endpoint normalization.
- EXP-051 supplies exact two-column cycles `Rz=2b` and quotient-rank-two context.

The invariant is the multiset of pairs `(coefficient, normalized semantic row token)` in the
two-column divided boundary. Exact row labels are retained as an audit surface, not used as the
cross-parameter comparison key.

## Validation and budget

- Training: `p=8,...,10`, at most 300 seconds and 8 GiB, checkpoint per parameter.
- Freeze: candidate formula and generator committed before holdout.
- Holdout: `p=11` only, at most 180 seconds and 8 GiB.
- Stop on source-hash, row-hash, exact-identity, uniqueness, or budget failure.
- A separate auditor must reconstruct the holdout multiset directly from the frozen matrix.

No manuscript or Zenodo gate is open at declaration.
