# Attempt 005 - affine-\(X\) audit did not enforce \(X=A^3\)

- Exit: assertion failure at `F6 supplies 4 points at p=601`.
- Elapsed: 2.3 seconds.
- \(F_3/p=601\): four graph/residual points, all rank \(124/125\), with a
  new alternative basis.
- \(F_6/p=601\): no sampled point with \(X=A^3\).
- Symbolic work: not started.

The preceding prime audit had found arbitrary nonzero \(X\)-points on
\(F_6\), but had not required \(X\) to lie in the cube image. The corrected
audit enumerates the actual list \(A^3\), including its multiplicities, and
also checks \(S\ne0\).
