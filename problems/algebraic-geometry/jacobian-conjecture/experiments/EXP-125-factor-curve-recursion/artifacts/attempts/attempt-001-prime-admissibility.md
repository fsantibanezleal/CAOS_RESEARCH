# Attempt 001 - inadmissible \(F_3\) prime

- Exit: assertion failure before any symbolic work.
- Elapsed: 69.4 seconds.
- Exact setup checks passed: the three EXP-124 factors and all six gcd-one
  claims with \(R,S\) were reproduced.
- Failed gate: `F3 supplies 4 points at p=1009`.
- Search performed: all \(1008^2\) pairs with \(A\ne0\).
- Cause: \(-1/16\) is not a cube modulo 1009, so
  \(F_3=(5B+4)^3+16A^3=0\) has no admissible nonzero-\(A\) points.

No rank or determinant claim was produced. See `../../redirect.md` for the
predeclared prime-admissibility correction used by the retry.
