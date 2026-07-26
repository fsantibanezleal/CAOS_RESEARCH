# EXP-104: Exact valuation by determinant interpolation

## Question

Are the 81 missing low coefficients in EXP-103's first chart exactly zero over
\(\mathbb Z\), so that its normalized determinant can participate in a
characteristic-zero gcd-one certificate?

## Exact interpolation target

For EXP-102's row chart, assignment gives

\[
1547\le \operatorname{ord}_u f,\qquad \deg f\le1646.
\]

Therefore

\[
g(u)=f(u)/u^{1547}
\]

is an integer polynomial of degree at most \(99\). Its values at 100 distinct
nonzero integers determine it exactly.

## Method

1. Reconstruct the same integer polynomial matrix and EXP-102 row chart used
   by EXP-103.
2. For \(k=1,\ldots,100\), compute the 125-by-125 determinant over
   \(\mathbb Z\) and divide by \(k^{1547}\).
3. Interpolate \(g\in\mathbb Q[u]\) exactly and require all coefficients to be
   integers.
4. Verify the interpolation independently at \(u=101\) and \(u=-1\).
5. Decide whether coefficients \(0,\ldots,80\) vanish and coefficient \(81\)
   is nonzero. If so, \(\operatorname{ord}_u f=1628\) exactly.
6. Recompute the EXP-102 and endpoint-safe EXP-103 \(u=2\) minors modulo
   \(998244353\). Normalize them only by their now-proved exact valuations and
   require gcd \(1\).
7. Repeat the modular gcd at \(1004535809\) as an implementation control.

## Proof criterion

If the interpolation proves exact support \([1628,1646]\), both selected
integer minors have constant and leading coefficients nonzero modulo the first
prime after their exact monomial valuations are removed. A nonconstant common
divisor over \(\mathbb Q[u]\) would therefore reduce to a nonconstant common
divisor modulo that prime. A modular gcd of \(1\) proves the exact gcd is \(1\).

Consequently the augmented matrix has rank \(125\) for every \(u\ne0\) on the
residual curve. Together with EXP-101's first two charts, this closes the
declared two-parameter coefficient slice.

This does not cover the other 49 GGHV coefficients and does not decide
\(JC(2)\).

## Falsifiers and controls

- Any nonintegral interpolated coefficient indicates a scaling error.
- A nonzero coefficient below degree 81 refutes the observed valuation.
- Failure at \(u=101\) or \(u=-1\) invalidates the interpolation.
- A nonconstant modular gcd leaves an explicit residual factor.
- Exact determinant timings are emitted every ten nodes; abort at five
  minutes before interpolation.

Declared 2026-07-26 before creating or running `run.py`.
