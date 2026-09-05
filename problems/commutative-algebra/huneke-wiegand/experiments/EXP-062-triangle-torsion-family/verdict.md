# EXP-062 verdict

Date: 2026-09-05. Status: **CONFIRMED: a quadratic family of independent two-torsion classes.**

The hypothesis was committed and pushed as `8daa0d4`. Computation began only
after EXP-061's complete original-sector audit passed. The source formulas
and first/middle/last sampling were fixed before the run.

## Exact all-parameter result

For every integer `p>=8` and every increasing nonnegative triple
`T=(i,j,k)` with sum `p-2`, the explicit original source `W_T` satisfies
`M W_T=2x_ij`. Its relative parity functional annihilates every original
K boundary and every connecting image of a complete D cycle. The family of
functionals pairs as the identity matrix with the chosen classes. Therefore

```text
(Z/2)^floor(((p-2)^2+3)/12) embeds in coker_Z(M_p).
```

This is quadratically unbounded integral two-torsion in the full explicit
presentation. The [proof](proof.md) establishes the entire relation lattice
among these classes as `2Z^{T_p}`; it does not merely find vectors with even
boundaries. A further, independently reviewed existence argument extends the
relative functionals over the D target and gives a retraction, so the detected
subgroup is a direct summand. No explicit all-parameter global D-row functional
or complete Smith form is computed or asserted.

The tracked eta is integrally congruent to the chosen class `x_02`, with an
explicit source for `eta-x_02`; it is not equal to that target vector. The
EXP-057 transfer also identifies the class of `b_A+b_B` up to sign.

## Predictions and proof basis

| Prediction | Verdict | Uniform justification |
|---|---|---|
| P1: full integer boundary `M W_T=2x_T` | PROVED for all `p>=8` and all T | Signed reflected intervals, all original faces, and the three-term triangle identity |
| P2: complete relative annihilation | PROVED for all `p>=8` and all T | Exhaustive K-source classification and complete generalized-potential/A-star arguments across every reachable high sector |
| P3: diagonal detection, independence, and count | PROVED for all `p>=8` | Unique edge completion, even relation lattice, and elementary six-step count recurrence |
| Splitting corollary | PROVED deductively | Well-defined functionals on `im(d_D)`, vector-space extension, and an identity retraction pairing |
| Full quotient or upper bound | NOT ESTABLISHED | No exhaustion of all cokernel classes or all torsion directions |

Independent paper review found no defect in the generic source signs, complete
relative argument, adjacency cancellations, `S=1,2` exceptional A rows,
count recurrence, or splitting deduction. The complete-kernel reconstruction's
first-low endpoint zero is not a restriction on the smallest second index in T.
The original family-to-presentation identification remains an imported premise.

## Finite campaign and adversarial evidence

The producer passes all 70 declared integer source identities, seven full
small-parameter pairing matrices, 93 exact count checks, and five original
eta-to-`x_02` source transfers. All source/functional mutation and duplicate/
mirrored-selection controls pass, including the ten-row adjacency case
`T=(1,2,3)` at `p=8`.

The 70 source checks comprise all 49 triangles at `p=8,...,14`, then the
first/middle/last lexicographic triangle at each of
`p=16,20,25,32,50,64,100`. The count formula is checked at `p=8,...,100`.
The five transfer identities are checked at `p=8,...,12`. Thus, for example,
the full family size at `p=100` is a proved count, while only three signed
sources there belong to the declared numerical stress campaign.

Both original differential encodings agree on each complete signed W boundary
and eta-transfer boundary. The functional-removal control includes an explicit
original K column whose pairing becomes one. Source coefficient/sign changes
have nonzero complete original unit-column residuals; permanent tests also
multiply actual altered sources. Duplicate and mirrored edge choices yield
singular pairing matrices, as independently checked.

Observed W support ranges from 38 to 13,594 and coefficient height is two
throughout the declared campaign. These source statistics are observations,
not an additional uniform counting claim. Functional support of ten to twelve
rows is proved by the formula
`12-1_{j=i+1}-1_{k=j+1}`.

## Independent complete original-sector audit

The auditor imports no producer mathematics. It reconstructs generic z
functionals, signed interval sources, all incident K sources, and all original
S columns in every reachable high sector. For all 27 triangles at
`p=8,...,12`, exact `F_2` row-span certificates verify the functional on
the complete D kernel, not merely on producer potential chains. It also
reconstructs and checks all 70 archived signed sources, all five transfer
sources, the small pairing matrices, controls, and the 93 count checks.

| Audit quantity | Count and interpretation |
|---|---:|
| Complete parity parameters | 5 |
| All triangles at those parameters | 27 |
| Distinct `(p,h)` high sectors | 65 |
| Distinct original S sources | 23,695 |
| Triangle-sector certificates | 364 |
| Source instances across those certificates | 151,319 |
| D-row instances across those certificates | 713,511 |
| D incidences across those certificates | 1,528,426 |
| Labelled D-row dual terms | 5,550 |

The instance totals repeat a physical sector when it is certified against
different triangle functionals; they are not counts of distinct original
matrices or columns. Every full D row is retained in each certificate.

All 39 combined permanent tests pass: 24 producer tests and 15 independent
audit tests. Focused Ruff checks pass. The complete independent audit also
replays byte-for-byte to temporary outputs. Producer and auditor finish within
their separate 120-second, 1-GiB, one-CPU caps. No dense global ambient matrix,
integer HNF/SNF, or old `p=11` HNF-source label is used. Tests use temporary
outputs, and no untouched-holdout claim is made.

## Certificate identity and source preservation

| File | SHA-256 |
|---|---|
| `run.py` | `019c34a9d1180b5cce3fc0d5bfb29db7ffd91c0b66d56eab9e042da7623f0d07` |
| `artifacts/results.json` | `09aef05e577e58b11c4ccc363ed47ccf1ed1598deb1b156a33bb3b6e49ae638d` |
| `artifacts/results-sources.json.gz` | `8475ffb305c1567eb68f99f675413be9f6afeb8bce5b0a9ce50b7a2484f7cb0d` |
| `audit.py` | `6c5b9a1183ed8b2838e5b356a9e2a3d0e1e6c39485984e47678ef88eac900136` |
| `artifacts/audit-results.json` | `854405294fab1d8881c76b58c30dc4120748e4f059ea8ae614e3b9619560a7ef` |

Producer internal hash:
`dbbf50d3e4d80cadb89cae79b5192e1879d283c8188b8280607afaf98dbb0f1a`.
Independent certificate internal hash:
`3f1c04eedfb392dd88d83ea243187c1a7cc3945ba367b879bee401f2af12b25e`.

Every tested W and transfer source retains its full signed original labels
in a lossless archive: 17,253,771 raw JSON bytes compress deterministically to
252,812 bytes, with zero gzip timestamp and empty embedded filename. Its raw
SHA-256 is
`af39d545d2f664dedbd0b90ac4b18c40ad88863b06d8c12a1f355f4a4e0472db`.
The auditor checks both archive representations and reconstructs every source
coefficient. Generated JSON is canonical LF text, so byte hashes remain valid
across the repository's line-ending normalization.

## Research and manuscript consequence

The single-class result of EXP-061 has generalized to an explicit, quadratically
growing family with a proved independence and splitting argument. This materially
strengthens the unpublished complementary manuscript and satisfies its uniform
parity/torsion theorem gate. The manuscript should present the exact original
model, full source witnesses, generic relative functionals, all-parameter count,
and the lower-bound nature of the result.

No full cokernel, quotient upper bound, isolated/relative-completion
identification, odd-torsion claim, or lower-strand recurrence follows from
this theorem. In particular, agreement with earlier isolated ranks 3,4,5,7
does not identify that smaller object with the full presentation. Scientific
novelty/dependency review, manuscript build/render QA, metadata, and fresh
public-download checks remain required. No new Zenodo publication is claimed
by this experiment verdict.
