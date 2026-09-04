# EXP-052 proof record - holdout-validated semantic exact-boundary formulas

Date: 2026-09-03. Status: **CONFIRMED FINITELY**. CPU-only exact reconstruction.

## Leakage-controlled construction

The training extractor reconstructed the labelled components only for `p=8,9,10`. For the unique
primary EXP-051 cycle supported on two relative columns, it stored the exact divided boundary and
normalized every nonzero row by missing low endpoints, selected high endpoints, coefficient kind,
and product coordinate.

The candidate was then written and committed at `b0b4ca9` before the `p=11` component was
semantically reconstructed. Its executable form is `candidate.py`; `candidate.md` records the
same formulas in mathematical notation. The training checker matched all six complete
coefficient-token multisets exactly.

## The two candidate families

Every row uses the fixed high variables `{6p,10p}`. In the `58->59` completion, write
`A(a,b;j)` for the `D:A` row missing `a,b` from `L0` and `3p,3p+j` from `L1`. Its six alternating
edge families contain exactly

```text
6p-30
```

distinct rows. In the `58->62` completion, write `B(a;j,w)` for the `D:B` row missing `a` from
`L0` and `3p,3p+j,w` from `L1`. Its four alternating triangular/interval families contain

```text
binom(p,2)-5
```

distinct rows. Coefficients in both formulas belong to `{+/-1,+/-2}`. The complete summation
rules, coefficient signs, and product coordinates are frozen in `candidate.md`.

## Declared predictions

P1 passes. The coefficient-sensitive numeric-skeleton vocabularies have sizes eight for
`58->59` and eleven for `58->62`, within the declared bound twelve.

P2 passes on training. The candidate reproduces every coefficient and normalized row token at
`p=8,9,10`, not only the support counts. The six observed/predicted multiset hashes agree.

P3 passes on the untouched holdout. Without changing the candidate, semantic reconstruction at
`p=11` gives exact matches on all 36 `58->59` rows and all 50 `58->62` rows. Direct integer
multiplication also rechecks `Rz=2b` for both two-column cycles, and independent binary reduction
shows that both `b mod 2` classes remain nonzero in the relative quotient.

## Independent audit

The separate auditor rebuilds the entire `p=11` labelled component again from the frozen chain
construction. It then reads each divided boundary directly from the EXP-047 integer matrix,
normalizes the reconstructed labels, compares the full multisets with the hash-locked candidate,
and independently verifies the nonzero quotient classes. All 31 checks pass.

The training artifact has SHA-256
`259ff476b7bb09c12566e4bd771da5c88af17f541cc5732db4dc7f2067e2ec70` and internal hash
`4aabacb66133ac97c7ebc7b12341d0f9fff9d7ef32a8b2c2ecd256e6a1392fa4`. The holdout artifact has
SHA-256 `0bb32fd050a8e9739ea866ffb6e75b612189899c84c350a1214b60ed78eebc8b` and internal hash
`516bbc925c8d17dd9fab021258a2082f5ff4e31df95e78507213478af452a503`. The audit certificate has
SHA-256 `ec48aa7cb63d5d445a4a9c6682b4ea3838748f0ace80e76dededc84e167f49f7` and internal hash
`519a34566e9177a7d8b34b14b0ba28cf5d926bc0b67eaaf7640ccd9c871bd0cc`.

## Mathematical boundary

This is stronger than an in-window curve fit: the full semantic formula was frozen before the
only untouched labelled case and survived it exactly. It is still not an all-parameter proof.
The two relative columns are coordinates in a parameter-dependent HNF kernel basis. A uniform
theorem must replace them by labelled source chains and verify the signed incidence identity for
arbitrary `p`.

The formula supplies one explicit nonzero exact class in each completion, not both independent
classes. EXP-049's bounded dual pair remains the best lower-bound mechanism for rank two. A
uniform free complement or relative-Morse matching remains necessary to exclude further torsion
and establish the upper bound.

## Consequence and strongest next action

The primal route is no longer an opaque Smith-coordinate search. It has a concrete target `b_p`
with bounded coefficients and explicit row families. The next experiment should construct a
labelled source chain `y_p` and prove `R_p y_p=2b_p` symbolically. Search should be constrained to
the small row formula, not the full quotient. In parallel, the fixed `58->62` parity duals should
be verified generically; after those lower-bound identities, effort moves to a parameterized free
complement for the upper bound.

No manuscript or Zenodo update is triggered because no all-parameter theorem has yet been proved.
