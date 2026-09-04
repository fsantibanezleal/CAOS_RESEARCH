# EXP-051 preflight - minimum-complexity unreduced Bockstein lifts

Date: 2026-09-03. Scope: HWB-076, stable completions `58->59` and `58->62`.

## Why this is the next action

EXP-050 proves that exact corrected representatives exist but refutes simple corrections to the
canonical EXP-048 chains. That complexity is not intrinsic: it is introduced by forcing an
integral torsion vector into a convenient mod-two quotient section.

Before quotient reduction, every binary cycle `z` already supplies an exact integral torsion
representative

```text
Rz=2b.
```

The cheapest new test is therefore to enumerate the deterministic binary kernel basis already
needed for the Bockstein, classify each nonzero quotient class, and retain the lowest-complexity
pair that spans the rank-two image. No integer optimization or new Smith computation is needed.

## Source, premise, and tooling check

The targeted source sweep for EXP-050 found no published cycle formulas for these CAOS blocks.
Stanley's Smith survey (<https://arxiv.org/abs/1602.00166>) supports the cokernel/lattice reading;
Kozlov (<https://arxiv.org/abs/cs/0504090>) and Jollenbeck-Welker
(<https://arxiv.org/abs/math/0501179>) support a later integral Morse compression. None selects
the required parameter-dependent cycles.

- EXP-047 supplies frozen exact relative matrices and complete finite `(Z/2)^2` types.
- EXP-048 supplies the semantic rank-two Bockstein quotient.
- EXP-049 supplies independent bounded duals.
- EXP-050 proves exact corrected existence but refutes its canonical section as a simple basis.

The runner uses only exact integer sums and binary elimination. A separate reverse/high-pivot
audit must independently find an exact spanning pair within the declared bounds.

## Invariant-first and budget

The decision invariant is the complexity of the divided boundary `b=Rz/2` before quotient
normalization. The lexicographic score is

```text
(support(b), max_abs(b), support(z), hash(z)).
```

- Full range `p=8,...,11`: at most 60 seconds and 4 GiB, checkpoint per inclusion.
- Stop on a frozen hash mismatch, odd boundary, quotient rank other than two, or exact identity
  failure.
- A resource stop is inconclusive.

## Exploration moment

This is a change from representative correction to cycle selection. If a small pair exists, its
boundary rows become the symbolic target and the large EXP-050 corrections are demoted as section
artifacts. If it does not, the primal route is demoted behind the support-four dual proof and the
relative-Morse upper bound.

No manuscript or Zenodo update is opened.
