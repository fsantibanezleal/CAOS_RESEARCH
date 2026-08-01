# Attempt 002: subresultant coefficient extraction defect

The first factorwise CRT run reached the degree-3 linear specialized
subresultant, but its reconstructed \(X\)-class did not annihilate \(R\).

The defect was in coefficient extraction. `Poly.coeff_monomial(X)` returns
only the coefficient of the exact monomial \(X B^0\), not the complete
polynomial coefficient of \(X\) in \(\mathbb Q[B][X]\). The same mistake
affected the constant coefficient. The repair extracts the coefficient from
the expression as a polynomial in \(X\), then reduces the resulting
\(B\)-polynomial modulo the block factor.

No mathematical claim was persisted from the failed run. Direct substitution
into both \(R\) and \(S\) remains the acceptance gate.

