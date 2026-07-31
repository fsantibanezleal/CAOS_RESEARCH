# EXP-094: Verdict confirmed, the cited remark excludes none of the four candidates

## Result

The exact source-identity audit passed. C10, C11, C19, and C20 all fail the
predicates stated in GGV2 Remark 2.32.

| Configuration | Persisted source data | Required excluded data | Decision |
|---|---|---|---|
| C10 | \(A_0=(7,21)\), \(A'_0=(1,0)\) | \(A_0=(7,21)\), \(A'_0=(2,1)\) | no match |
| C11 | \(A_0=(7,21)\), \(A'_0=(1,0)\) | \(A_0=(7,21)\), \(A'_0=(2,1)\) | no match |
| C19 | \(B_1=A_0=(6,15)\) | \(B_1=(6,18+6k)\) | no match |
| C20 | \(B_1=A_0=(6,15)\) | \(B_1=(6,18+6k)\) | no match |

The previous strong-candidate classification conflated distinct source objects.
Sharing the main corner \(A_0\) does not satisfy an exclusion that also fixes
\(A'_0\), \(B_0\), or \(B_1\).

## Exact source derivation

1. The GGHV17 complete-chain proof identifies
   \(A_0=m^{-1}\operatorname{en}_{1,0}(P)\). GGV defines the same quantity as
   \(B_1\), so \(B_1=A_0\).
2. The GGHV17 family table gives \(A'_0=(1,0)\) for F9/C10 and F11/C11.
   GGV2 states that the discarded Heitmann families at \(A_0=(7,21)\) come
   from \(A'_0=(2,1)\). The endpoint mismatch is decisive.
3. The family table gives \(A_0=(6,15)\) for F7/C19 and F8/C20. Hence their
   \(B_1\) is \((6,15)\). GGV2's separate exclusion requires
   \(B_1=(6,18+6k)\), whose second coordinate is at least 18. The endpoint
   mismatch is decisive without knowing \(B_0\).

## Adversarial validation

The implementation was revised after its first run because the C19/C20
classifier initially short-circuited on an unknown \(B_0\). The corrected
implementation exposes the necessary \(B_1\) family predicate separately and
asserts that it fails.

Four controls passed:

1. \(A_0=(7,21)\), \(A'_0=(2,1)\) matches the Heitmann-family condition.
2. \(B_0=(6,15)\), \(B_1=(6,18)\) matches the GGV condition.
3. \(B_0=(6,15)\), \(B_1=(6,30)\) fails the nonmultiple-of-30 clause.
4. \(B_0=(8,28)\), \(B_1=(8,40)\) matches the known C13 exclusion from
   EXP-082.

The final artifact is
`artifacts/results.json`, SHA-256
`88D351CD23CC550932C481EDE4A208EDC7336D6897E1F90B27BEE314C642C0C2`.

## Verdict and scope

**CONFIRMED:** GGV2 Remark 2.32 does not exclude C10, C11, C19, or C20.
EXP-094 supersedes only the candidate classification in EXP-084/085. It does
not alter their primary-source transcriptions.

This result does not prove that any of the four configurations is realizable,
that any survives every other restriction, or that a planar counterexample
exists. It does not decide \((72,108)\) or raise the degree floor.

## Route decision

The cheap source lookup for these four configurations is complete and yielded
no exclusion. Repeated Heitmann-family matching is therefore retired for these
rows. The 16 unprinted \(A'_0\) values remain a separate exact chain-enumeration
task, but they are not a prerequisite for work on the \((72,108)\) target.

For the immediate target, the highest-value next experiment is the explicit
Makar-Limanov and Trakhtenberg applicability bridge through the GGHV
normalization. If that bridge fails, the certificate-module and localized-chart
analog becomes the leading constructive route.

## How could this be wrong?

- The conclusion depends on the persisted transcription of the GGHV17 family
  rows. Those rows were reread in the primary TeX source, but an independent
  implementation of the complete-chain enumeration has not reproduced the
  entire table.
- A different theorem may exclude one of the four configurations. This verdict
  concerns only the predicates in GGV2 Remark 2.32.
- The meanings of \(A_0\) and \(B_1\) are fixed by the cited source definitions.
  A different normalization would require an explicit transformation before
  comparison.

## Record-integrity note

EXP-085 has a verdict but no `hypothesis.md`. No retroactive hypothesis was
created. EXP-094 was declared and committed before execution so that this
correction has a complete experiment record.
