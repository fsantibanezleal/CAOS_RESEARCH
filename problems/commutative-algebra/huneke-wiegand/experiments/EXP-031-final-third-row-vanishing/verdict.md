# EXP-031 verdict - CONFIRMED

Date: 2026-08-20.

## Decision

**CONFIRMED.** For every integer `p>=4`, every field, and every multigraded offset `b`,

```text
beta_(3,(7,b))(C_p)=0.
```

The proof is integral. Zero-vertex matching leaves only residual-hole triangles, and a positive
low vertex gives each one a distinct same-offset tetrahedral filler whose reduced boundary has a
single unit entry. Therefore `beta_(3,7)=0` in every characteristic.

Together with EXP-027, EXP-029, and EXP-030, this completes the third homological row:

```text
beta_(3,4)=p(5p-1)(500p^2-440p+47)/2,
beta_(3,5)=4p(8p-1),
beta_(3,6)=8p(7p^2-12p+2)/3,
beta_(3,7)=0,
beta_(3,j)=0 otherwise,
beta_3=p(7500p^3-7988p^2+2025p-133)/6.
```

## Gate results

| gate | result |
|---|---|
| declaration before implementation | PASS; declaration `7a109ab` predates implementation `1802136` |
| premise hashes | PASS; EXP-024/027/030 proof and EXP-030 verdict match the frozen ledger |
| `p=4` smoke | PASS in 35.355 seconds; all 374 offsets have `H_2=0` over `GF(2)` and `GF(1000003)` |
| full exact profiles | PASS; all 374 offsets at `p=4` and all 470 offsets at `p=5` vanish |
| canonical unit fillers | PASS; every critical triangle for `p=4,...,12` has a distinct same-offset unit filler |
| independent audit | PASS; opposite filler order matches counts and offset ranges for `p=4,...,12` |
| arithmetic certificate | PASS; 297 parameter rows through `p=300` |
| integral proof | PASS; acyclic matching plus signed identity boundary block |
| characteristic independence | PASS; follows from unit integral cancellation, not finite-field extrapolation |
| adversarial controls | PASS; zero filler, wrong hole, three-candidate pool, full degree-three set, and reused same-offset filler are rejected |

The exact profile campaign completed in 126.893 seconds inside the 900-second budget. The
independent audit completed in 2.437 seconds.

## Artifact identities

- canonical aggregate: `d68afbb5c54ebb86abbf420c389e1cacf666071cb35f83e5d2b67eccbc354858`;
- independent-audit aggregate: `0be4b659126064328b5ef14a40e488a836f874d2eed9b048d4d3f19da971346e`;
- symbolic aggregate: `e4bf2e0ae303e905efc9f985b239d059a5255b02d2ddc1d37abab5cc5cb2fc1f`;
- `run.py`: `473651931e7055359024c369febbe156661946a953e4ba0ac97f8e6b12f8d926`;
- `audit.py`: `362d1c8478f13bfa7622fe42d4e608a4e2b4accfd8e01ae841bdb09d6c9de7f5`;
- `symbolic_certificate.py`: `5ffe99eed4a13438f25991609dd345b248d7eed7dda1b86f2762e7b2fe068296`;
- `results.json`: `1c6157e38fd3c265248961bfdef61a967918cd847def0962ca9438d4fb73bace`;
- `audit.json`: `bff18892e99bbf87d50b64d7d58ba6b85fc0a36b7f60248dea00765b05d71dd4`;
- `symbolic-certificate.json`: `af1fbc1da2adf643861da0bffcd26f0a9c1bb6fea4d1d63d5639a306d72e9e0d`.

## Corrected attempt

The first smoke implementation used the tetrahedron tuple as a global filler key. It reported a
collision between `(1,2,3)` at offset 29 and `(1,2,4)` at offset 30 because both use tetrahedron
`(1,2,3,4)`. Cells in different multigraded complexes are not duplicates. The attempt is preserved
as `attempt-1-global-filler-key.json` with status `INVALID_IMPLEMENTATION`; it carries no evidence
for or against the theorem. The corrected implementation keys by `(offset,tetrahedron)`.

## Scope and next action

This result completes the third homological row of the explicit conductor special-fiber family.
It does not determine the remaining higher rows, the full Betti table, the full minimal
resolution, or a classification of Huneke--Wiegand counterexamples.

HWB-045 is done. The row-completion theorem triggers an in-place v0.18 update of the existing main
manuscript and a Zenodo new-version gate under HWB-047. A separate manuscript remains deferred.
The next mathematical priority after publication is to combine complete rows with Gorenstein and
canonical-module duality to seek whole diagonal recurrences before any raw full-resolution sweep.
