# EXP-125 prime-admissibility audit

## Exact \(F_3\) condition

Since
\[
F_3=(5B+4)^3+16A^3,
\]
a nonzero-\(A\) point requires \(-1/16\) to be a cube.

## Diagnostic sweeps

- \(p=1009\): \(-1/16\) is not a cube; no admissible \(F_3\) point.
- Every tested prime \(p\equiv2\pmod3\) from 911 through 1289 had at least
  four \(F_3\) and \(F_7\) points but no \(F_6\) point. This includes 1013
  and 1019.
- Candidate primes \(p\equiv1\pmod3\) were first filtered by the exact
  cubic-residue test for \(-1/16\), then exhaustively checked until four
  nonzero-\(X\), \(S\ne0\) points were found on each factor.

The first four fully admissible primes were:

| prime | \(F_3\) points | \(F_6\) points | \(F_7\) points |
|---:|---:|---:|---:|
| 601 | at least 4 | at least 4 | at least 4 |
| 643 | at least 4 | at least 4 | at least 4 |
| 691 | at least 4 | at least 4 | at least 4 |
| 727 | at least 4 | at least 4 | at least 4 |

EXP-125 selects 601 and 643, the first two in increasing order. Rank and
basis decisions remain part of the accepted run; this audit validates only
geometric sample availability.
