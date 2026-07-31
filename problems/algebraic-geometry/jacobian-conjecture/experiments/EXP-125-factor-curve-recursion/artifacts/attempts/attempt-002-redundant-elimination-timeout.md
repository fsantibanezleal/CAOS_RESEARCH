# Attempt 002 - modular implementation timeout

- Exit: modular reconnaissance timeout at the declared 120-second gate.
- Symbolic work: not started.
- Completed stratum: \(F_3\) at \(p=1013\).
- Evidence: four exact graph/residual samples, all with rank profile
  \(124/125\), and one new one-row-replacement basis.
- Pairs scanned: 3341.
- Cause: each sample redundantly computed two selected determinants and two
  independent-row eliminations.

The retry retains the four-point rank requirement. It uses the exact graph
and factor equations for membership, performs one independent-row
elimination to choose a basis, and tests that basis at subsequent samples.
Full augmented rank 125 forces coefficient rank 124 because the coefficient
matrix has exactly 124 columns.
