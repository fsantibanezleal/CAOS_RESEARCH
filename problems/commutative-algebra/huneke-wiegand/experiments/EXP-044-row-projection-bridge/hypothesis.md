# EXP-044 hypothesis - row-projection localization of the signed bridge

Date: 2026-08-31. CPU only. Exact integer and finite-field arithmetic.

## Question

EXP-042 found that the same intrinsic Bockstein classes have `D:B` representatives under one
pivot convention and `K:C0` representatives under the opposite convention. EXP-044 tests whether
these two row atoms form a necessary and sufficient two-sided torsion bridge, or whether they are
only basis-dependent shadows of a larger signed relation.

For each frozen isolated matrix at `p=8,9,10,11`, form exact row projections that:

1. delete `D:B`;
2. delete `K:C0`;
3. delete both atoms;
4. retain only the union `D:B union K:C0`.

Zero columns remain part of each projected presentation. Every projection is evaluated by exact
`GF(2)`, `GF(3)`, and `GF(5)` ranks and by forward and reverse first-Bockstein reductions.

## Predictions

### P1. Each side is necessary

Deleting either `D:B` or `K:C0` eliminates the full first Bockstein at every tested parameter.
The predicted projected Bockstein ranks are all zero. A surviving class refutes the claim that the
torsion requires the proposed two-sided bridge.

### P2. The union is sufficient

Retaining only `D:B union K:C0` preserves the full Bockstein ranks

```text
p=8,9,10,11 -> 3,4,5,7.
```

Failure means that additional row atoms participate essentially and the bridge must be enlarged
before an integral normal form is attempted.

### P3. Projection and field-rank agreement

For every projection, forward and reverse Bockstein ranks agree. Whenever the projected odd-field
ranks agree, their common rank minus the `GF(2)` rank equals the Bockstein rank. This is a finite
consistency check, not a rational-rank certificate for the projected matrices.

## Audit and claim boundary

The runner must verify the exact EXP-042 script, result, and matrix hashes before computation. An
independent auditor must reload the frozen matrices, rebuild every projection, recompute all
finite-field ranks with the opposite pivot convention, and recompute the first Bockstein without
calling the runner's projection routine.

The `p=8` smoke is capped at 300 seconds and 8 GB. The full campaign is capped at 1,200 seconds
and 16 GB. A resource stop is inconclusive. A pass would identify a finite bridge candidate only;
it would not construct a unimodular matching, an OI/FI map, an all-parameter theorem, or the full
lower strand. No manuscript or Zenodo gate opens from row projections alone.
