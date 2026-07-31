# EXP-120 - Verdict: the third chart closes \(G\), but \(L\) and \(Q\) persist finitely

Verdict: **mixed, exact component closure and finite-residual reduction**.

## Result

EXP-115's independent \(G\)-basis reproduces its modular witness,
\[
\det \equiv 978 \pmod {1009},
\]
and is exactly invertible at the first deterministic rational control,
\[
(A,B,d)=(1,0,1).
\]
After normalization, the largest cyclic strongly connected block has size
25. Its determinant completed in 15.69 seconds; the complete final run
completed in 28.85 seconds.

The exact third determinant on \(d=1\) has total degree 108 and 21
monomials. It contains \(A^{90}\), and its remaining exponents are invariant
under \(X=A^3\). Up to a nonzero rational scalar, the full invariant is
\[
X^{30}L(X,B)Q(X,B)R(X,B),
\]
where
\[
L=125B^3+300B^2+240B+16X+64,
\]
\[
\begin{aligned}
Q={}&15625B^6-37500B^5+60000B^4-2000B^3X-56000B^3\\
&-4800B^2X+38400B^2+7680BX-15360B\\
&+256X^2-1024X+4096,
\end{aligned}
\]
and
\[
R=-156250B^7+15625B^6X+28000B^3X+3200B^2X^2+1024X.
\]
The exact scalar and complete expressions are persisted in
`artifacts/results.json`.

## Exact component ideals

Let \(\Delta_{\mathrm{sel}}\) be the EXP-114 selected determinant,
\(\Delta_{LQ}\) the EXP-119 alternative determinant, and
\(\Delta_G\) the third determinant above.

On the \(G\) component, factorwise exact Groebner calculations give
\[
(G,\Delta_{LQ},L)=(1),\quad
(G,\Delta_{LQ},X)=(1),\quad
(G,\Delta_{LQ},Q)=(1),\quad
(G,\Delta_{LQ},R)=(1).
\]
Because these are all the irreducible factors of \(\Delta_G\), they prove
\[
(G,\Delta_{LQ},\Delta_G)=(1).
\]
Thus the three charts cover the entire selected \(G\) curve component.

The other two component ideals are nonunit but zero-dimensional:

| component | exact status | elimination certificate |
|---|---|---|
| \(L\) | zero-dimensional, nonunit | lex basis of size 2; \(B\)-eliminant degree 108 and squarefree degree 73 |
| \(Q\) | zero-dimensional, nonunit | graded-lex basis of size 6; FGLM stopped at the declared 180-second gate |

The factorization of \(\Delta_G\) itself explains the outcome: it contains
both \(L\) and \(Q\), so this row basis vanishes identically on those two
components and cannot remove their common residuals.

## Prediction audit

1. First-nine rational anchor: **pass**; the first control works.
2. Largest cyclic block at most 60: **pass**; it is 25.
3. At most 500 monomials and invariant through \(X=A^3\): **pass**; 21
   monomials after the explicit \(A^{90}\) coordinate factor.
4. At least two unit component ideals: **fail**; only \(G\) is a unit.
5. Surviving residual squarefree degree at most 100: **partially
   evaluated**; \(L\) has squarefree degree 73, while the \(Q\) lex
   conversion reached its declared cost gate.

## Adversarial validation

- The \(p=1009\) witness from EXP-115 reproduces exactly.
- The rational anchor determinant is nonzero over \(\mathbb Q\).
- The SCC product matches five direct exact 125-by-125 determinants.
- The full determinant, including the \(A^{90}=X^{30}\) stratum, is used in
  every component ideal; no coordinate factor is silently cancelled.
- Each factorwise unit ideal on \(G\) has reduced basis `[1]`.
- The \(L\) lex basis and squarefree eliminant are persisted exactly.
- The \(Q\) claim stops at zero-dimensionality; no lex eliminant or point
  count is promoted.
- The final artifact SHA-256 is
  `752DB3AF4F5C1064468D8D349197EFB1E1D84E96CA29E4683FA8CBF5861142AD`.
- Failed, stopped, and corrected attempts are retained alongside the final
  run logs.

## What this proves

- The complete \(G\) component of the \(d\ne0\) selected residual is
  eliminated exactly by three maximal-minor charts.
- The remaining \(L\) and \(Q\) common residuals are zero-dimensional.
- The next chart search can be restricted to finite points on \(L\) and
  \(Q\), and must use row bases selected there rather than the current
  \(G\)-basis.

## What this does not prove

- The \(d\ne0\) chart is not covered because the \(L\) and \(Q\) finite
  residuals remain.
- The full three-parameter \(T_B\) restriction is therefore not closed,
  despite EXP-118 closing its \(d=0\) boundary.
- An eliminant degree is not a certified number of distinct affine points.
- The 24-parameter core, full 51-parameter family, the \((72,108)\) case,
  the planar degree floor, and JC(2) remain open.

## How could this be wrong?

The certificates are exact inside the persisted 302-row matrix model and
still depend on the upstream GGHV transcription and EXP-111 completeness
audit. Factorwise closure of \(G\) is valid because every factor of the
third determinant, including the coordinate factor, was included. The
nonunit \(L\) and \(Q\) results are deliberately weaker: they prove finite
common residuals, not their cardinality or that every projected root lifts
to an affine solution.

## Strategy consequence

The strongest next step is not another generic determinant. EXP-120 shows
that a basis selected on \(G\) necessarily carries the \(LQ\) factor in
this instance. EXP-121 should select new maximal-minor row bases directly
at deterministic algebraic or modular controls on the surviving \(L\) and
\(Q\) ideals, then test the resulting minors in those quotient rings. This
targets the actual obstruction and avoids recomputing already closed curve
components.
