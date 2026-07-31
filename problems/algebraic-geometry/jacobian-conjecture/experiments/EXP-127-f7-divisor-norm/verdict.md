# EXP-127 - Verdict: \(F_7\) reduces to a degree-30 finite residual

Verdict: **exact \(F_7\) dense-open cover confirmed; effective residual
degree 30**.

## Result

The distinct EXP-125 \(F_7\) basis has exact anchor \((A,B,C)=(1,1,0)\).
Its union-SCC decomposition has one block of size 31 and 86 singleton
blocks, within the declared reconstruction budget. The complete normalized
determinant has \(A\)-valuation 89. Its invariant reduction has \(Y\)-degree
zero: this selected minor is already a section in \(X=A^3,B\), independent
of the graph coordinate \(Y=A^2C\).

Modulo the irreducible quadratic-in-\(X\) curve \(F_7(X,B)\), the section has
a nonzero primitive linear class
\[
h_7(X,B)=U(B)X+V(B).
\]
Its exact function-field norm has degree 58 and factors, up to a nonzero
rational scalar, as
\[
\mathcal N_7(B)=B^{16}E_3(B)E_9(B)E_{12}(B)E_{18}(B),
\]
where the four \(E_d\) are irreducible of the indicated degrees. The first is
\[
E_3(B)=375B^3+32.
\]
All factors and the complete \(U,V\) polynomials are persisted in
`artifacts/results.json`.

Same-point quotient arithmetic gives:

- on \(B=0\), the common affine root is \(X=0\), hence \(A=0\);
- on \(E_{12}=0\), the unique section root satisfies \(R=S=0\);
- on \(E_3,E_9,E_{18}\), the unique section root has \(X\ne0\) and
  \(S\ne0\).

Therefore, on the declared principal open \(AS\ne0\), the effective
\(F_7\) residual is exactly
\[
E_3(B)E_9(B)E_{18}(B)=0.
\]
It gives 30 normalized \(B\)-values over an algebraic closure. Each has a
unique \(X\), three nonzero cube roots \(A\), and then a unique
\(C=-R/(A^2S)\), for 90 lifted algebraic \((A,B,C)\) points.

## Exact checks

- The accepted EXP-125 result SHA-256 was verified before its \(F_7\) basis
  and modular samples were reused.
- \(F_7\) and its irreducibility over \(\mathbb Q[X,B]\) were reproduced.
- The exact anchor and all 87 SCC blocks were reconstructed.
- The isolated worker artifact has SHA-256
  `8711AD526482CD16316719A4F60783378748157460F56BCA41689726A891571A`.
- Four direct rational 125-by-125 determinants equal the reconstructed
  normalized determinant.
- Eight accepted modular \(F_7\) samples reproduce curve membership,
  graph membership, \(S\ne0\), and a nonzero selected minor.
- Polynomial division verifies \(H=QF_7+h_7\) exactly.
- The Sylvester resultant equals the leading coefficient of \(F_7\) times
  the determinant of multiplication by \(h_7\) in the quadratic quotient.
- Every irreducible norm factor was classified at the same algebraic point,
  rather than removed through projection-resultant overlap alone.
- Two accepted writes, reusing only the hash-verified exact worker on the
  second pass, produced identical result SHA-256
  `75C8385C175B99FE51B2D3481C8820C5D01D51EFABC4FC75CC5A48ABAFCF9AAE`.

## What this proves

- The selected exact maximal minor covers a dense open of the \(F_7\) graph
  component.
- Together with EXP-125/126, no positive-dimensional factor curve remains
  on the declared \(AS\ne0\) graph chart.
- The remaining graph targets are finite: 24 normalized values from \(F_3\),
  48 from \(F_6\), and 30 from \(F_7\), before overlaps or further charts.
- The divisor/norm viewpoint works for two distinct determinant bases and is
  now the preferred finite-residual ledger.

## What this does not prove

- None of the 102 normalized graph values (306 algebraic lifts before
  overlap analysis) is yet covered by another minor.
- The finite base locus \(V(R,S)\) and the \(A=0\) boundary remain open.
- The full four-parameter restriction, 24-parameter core, 51-parameter
  family, complete \((72,108)\) case, planar degree floor, and \(JC(2)\)
  remain open.

## Adversarial validation

The multiplicity \(B^{16}\) is not interpreted as 16 affine points. At
\(B=0\), the leading quadratic coefficient of \(F_7\) degenerates, so the
actual affine equations were reduced modulo \(B\); their common root is
\(X=0\), outside \(A\ne0\). The \(E_{12}\) factor is removed only after
direct quotient evaluation gives \(R=S=0\). The retained factors are
squarefree and have unique section roots with \(X,S\ne0\).

The first full run completed all mathematics but failed at final JSON
serialization because a SymPy multiplicity was not converted to a built-in
integer. That artifact-layer failure is preserved in
`artifacts/attempts/attempt-001-json-serialization.md`; no result from it was
accepted.

## Strategy consequence

The positive-dimensional phase of the rational graph atlas is complete.
The next strongest experiment should stop recomputing curve determinants
and instead cover the finite ledger by algebraic point charts:
\[
Q_9Q_{15}\quad(F_3),\qquad
Q_{18}Q_{30}\quad(F_6),\qquad
E_3E_9E_{18}\quad(F_7).
\]
Compute gcds and overlaps between these projected factors first. Then select
additional minors simultaneously on their quotient algebras, treating
\(V(R,S)\) and \(A=0\) as separate boundary experiments.
