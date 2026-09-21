# Rank-six localization preflight

Date: 2026-09-20. Search cutoff: 2026-09-20 12:40 UTC.

## Primary-source observation

Pearce-Crump's arXiv:2609.15329v1 proves a vector-profile diagonal theorem for
every fixed finite rank. Its main theorem uses a fully printed rank-three
profile with

`C_3 = 0.6567752140190419405677628751089899133...`.

The same source states a certified ten-direction, six-square benchmark

`C_6 in 0.6566338678379319741683641732 +/- 5.63e-18`.

The source PDF and TeX archive are already pinned by the Riemann programme. The
local copies have SHA-256 values:

- PDF: `1476f60cf5f4a12239d0db3fdaaaf2b9d4de604c27f1a57b5a95f7b9f2a9f0be`.
- TeX archive: `24550f470d116b9a63148061e441d634a014d58dba1ce2dd6abe6edcfea061e4`.

The public source does not print the rank-six coefficient matrix. Its
existence and interval are therefore an attributed imported theorem, not a
locally reconstructed certificate. This limitation must appear in the verdict
and manuscript.

## Why the localization is rank-independent

The EXP-005 proof uses the detector rank only through a fixed finite sum of
analytic components. Pearce-Crump's coefficient-uniform horizontal estimate
applies componentwise, its vector-profile diagonal theorem packages the finite
sum into `C[q]`, and the arbitrary-subinterval rational-frequency estimate is
unchanged. With fixed rank and fixed profile, all finite constants are absorbed
before `T` tends to infinity. The local constraints

`u < (theta - 1/2)/2` and `u < 1/4`

are identical to EXP-005. Taking the height limit first, then the fixed-profile
regularization limit, gives the same local odd-support theorem with `C[q]` in
place of `C_3`.

## Online search

Exact searches for the printed rank-six constant, the phrase "stronger
rank-six benchmark", and public code for `C[q_6]` found no separate source or
coefficient release as of the cutoff. The arXiv primary source remains the only
located authority for the rank-six enclosure. This is bounded negative evidence,
not an exhaustive availability claim.

## Result-selection decision

The spectral-defect term of EXP-007 strictly improves the old positive curve
but cannot move its onset. Replacing `C_3` by the smaller source-certified
`C_6` strengthens the independent odd-support input and therefore moves the
Hilbert-parity onset itself. It is the more relevant next result. The manuscript
should remain one integrated paper because the new argument changes one
analytic input and all downstream formulas share the existing finite products.
A split becomes useful only if the six-square profile is independently rebuilt
or the rank-independent localization is expanded into a standalone analytic
study.
