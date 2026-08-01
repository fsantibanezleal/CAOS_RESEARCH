# EXP-131 verdict - the direct A=0 boundary is closed

Status: **CONFIRMED COMPLETE EXACT ATLAS**.

## Exact result

EXP-131 rebuilds the original reduced augmented system before any division by
\(A\) and specializes

\[
M_0(B,C)=M_{\mathrm{forced}}+B M_{(0,5)}+C M_{(2,9)}
\]

as a 302-by-125 matrix. Two row bases, selected stably at primes 1009 and
1153 and then reconstructed over \(\mathbb Q\), give exact determinants

\[
\Delta_1=\kappa_1(5B+4)^3(25B^2-20B+16)^3
\]

and

\[
\Delta_2=\kappa_2 B^{95}
(109375B^6-110592)
(21875B^6-4800B^3-24576),
\]

where \(\kappa_1,\kappa_2\in\mathbb Q^\times\). Both determinants have
degree zero in \(C\).

Writing

\[
f=(5B+4)(25B^2-20B+16)
\]

and

\[
h=B(109375B^6-110592)(21875B^6-4800B^3-24576),
\]

the persisted exact Bezout identity is

\[
\begin{aligned}
1={}&\left(
\frac{478515625}{17179869184}B^{12}
-\frac{2734375}{134217728}B^9
-\frac{205625}{4194304}B^6
+\frac{1025}{32768}B^3+\frac1{64}
\right)f\\
&-\frac{25B^2}{17179869184}h.
\end{aligned}
\]

Hence \((\Delta_1,\Delta_2)=(1)\) in \(\mathbb Q[B,C]\). At every point
of the \((B,C)\)-plane at least one augmented 125-minor is nonzero. Because
the coefficient matrix has only the 124 nonconstant \(Q\)-columns after the
structural constant column is removed, the augmented system is inconsistent
everywhere on this boundary.

## Controls

- Both modular selection primes give the same primary and alternative row
  bases.
- The linear residual fibre and both quadratic roots at the splitting primes
  retain augmented rank 125 at \(C=0,1,2,3,5\).
- Both determinant formulas were recomputed directly over characteristic zero
  and checked at four rational \((B,C)\) controls.
- The exact determinant factorizations, unit gcd, and Bezout identity are
  verified by `run.py`.
- Accepted artifact SHA-256:
  `9DBB699F56B43C518CEC08BBD9C667D2D92C22FD7C662C33CCCFF44AFD2A1CC1`.

## Consequence and strict boundary

EXP-131 closes \(A=0\) on the normalized \(d=1\) chart. EXP-118 already
closes \(d=0\), while EXP-123/129/130 close \(A\ne0,d=1\). Therefore the
complete declared four-coefficient restriction
\(\{(0,1),(0,5),(1,0),(2,9)\}\) is covered by exact augmented-minor atlases.

This is not a proof or disproof of JC(2). It does not close the 24-parameter
cyclic core, the full 51-parameter GGHV family, the complete \((72,108)\)
case, or the planar degree floor.

## Next strongest path

The next experiment should test a transverse fifth direction, beginning with
\((2,8)\): EXP-122 gives it a linear anchor factor and a size-35 union SCC,
the smallest linear candidate outside the closed restriction. The accepted
two-minor boundary atlas becomes a regression gate. A fifth-direction result
must recurse on the joint exceptional ideal of several sections; a single
minor cannot establish coverage.

