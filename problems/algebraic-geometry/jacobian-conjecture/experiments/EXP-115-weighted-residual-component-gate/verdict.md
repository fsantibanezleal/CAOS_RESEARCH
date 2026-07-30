# EXP-115 - Verdict: the weighted-open components transition, while the boundary exposes the \(P\)-kernel

Verdict: **mixed, exact component gate**. The weighted-open prediction is
confirmed. The proposed rank-125 boundary transition is refuted for a
structural reason.

## Result

The run completed in 2.7 seconds.

On \(d\ne0\), weighted normalization
\[
a=A u^7,\qquad b=B u^3,\qquad d=u^9
\]
reduces the selected factors to polynomials in \(A,B\). Writing \(X=A^3\),
\(G_{54}(A,B,1)\) is irreducible over both
\(\mathbb Q[X,B]\) and \(\mathbb Q[A,B]\).

The second factor splits:
\[
H_{63}(A,B,1)=L(A,B)Q(A,B),
\]
where
\[
L=16A^3+125B^3+300B^2+240B+64
\]
and
\[
\begin{aligned}
Q={}&256A^6-2000A^3B^3-4800A^3B^2+7680A^3B-1024A^3\\
&+15625B^6-37500B^5+60000B^4-56000B^3\\
&+38400B^2-15360B+4096.
\end{aligned}
\]
Both \(L\) and \(Q\) are irreducible over \(\mathbb Q[A,B]\).
Thus the weighted-open selected residual has three, not two, irreducible
components.

## Exact component non-containment on \(d\ne0\)

At the good prime \(p=1009\), the complete 302-by-125 augmented matrix has
rank 125 at isolated points on each component, with the other two factors
nonzero:

| component | \((A,B,d)\bmod1009\) | alternative determinant |
|---|---:|---:|
| \(G_{54}\) | \((64,4,1)\) | \(978\) |
| \(L\) | \((0,201,1)\) | \(768\) |
| \(Q\) | \((0,300,1)\) | \(676\) |

The selected pinned minor vanishes at all three points. The persisted row
bases define minors over \(\mathbb Q[A,B]\). If the corresponding
characteristic-zero component factor divided such a minor, its good-prime
reduction would vanish at the displayed point. The nonzero determinants
therefore prove that none of the three irreducible components is wholly
contained in the rank-deficient locus.

The \(L\)-component also has a characteristic-zero witness:
\[
(A,B,d)=(0,-4/5,1).
\]
At this point the selected minor is zero and a persisted alternative
125-row minor is exactly nonzero.

The row transitions are not small: the finite-field bases replace 68, 34,
and 34 pinned rows on \(G,L,Q\), respectively. Prediction 5 is refuted.
Alternative chart selection must use global row-basis search, not
single-row swaps.

## The \(d=0\) boundary

At \(d=0\), the selected residual has reduced component support
\[
A=0,\qquad B=0,\qquad
30720000A^3+48828125B^7=0.
\]
The last component contains the rational point
\[
(A,B)=(-9,12/5).
\]

The expected rank-125 alternative chart does not exist on this plane.
Instead, the complete augmented matrix has the exact polynomial right kernel
\[
K(A,B)
=
A\,y+B\,y^5+y^8(1-xy)^8.
\]
Coefficientwise over \(\mathbb Q[A,B]\),
\[
\mathcal A(A,B,d=0)K(A,B)=0.
\]
The kernel has zero coordinate on the appended target column.

This is not an accidental numerical dependency. On \(d=0\), the forced
\(x\)-term in \(P\) is cancelled, and
\[
P=A\,y+B\,y^5+y^8(1-xy)^8
\]
lies inside the retained \(Q\)-monomial space. The kernel is the tautological
bracket identity
\[
[P,P]=0.
\]

At exact rational representatives of all three boundary components, the
rank profile is
\[
\operatorname{rank}M=123,\qquad
\operatorname{rank}[M\mid b]=124.
\]
Thus each tested representative remains inconsistent even though every
125-column augmented minor vanishes.

## What this proves

- The weighted-open selected residual has three irreducible components.
- None of those three components is generically trapped in the
  rank-deficient locus; each admits an alternative full-rank chart.
- On \(d=0\), rank 125 is impossible for structural reasons because \(P\)
  itself enters the admissible \(Q\)-space.
- The correct boundary object is the quotient by the explicit
  one-dimensional \(P\)-kernel, followed by a 124-column augmented rank
  test.
- The three exact boundary controls have rank gap \(123/124\), so the
  inconsistency mechanism survives the quotient at those points.

## What this does not prove

- The proper closed intersections left on the \(G,L,Q\) components are not
  covered.
- The \(123/124\) rank gap is not yet proved uniformly over the whole
  \(d=0\) plane.
- Results on \(T_B\) do not close the 24-parameter core or the other
  27 parameters on alternative charts.
- The full \((72,108)\) family, the degree floor, and JC(2) remain open.

## Adversarial validation

- All three open-component witnesses annihilate exactly one declared factor
  modulo a good prime, keep the other factors nonzero, make the selected
  determinant zero, and make a persisted alternative determinant nonzero.
- \(G,L,Q\) were factored and checked for irreducibility over
  \(\mathbb Q[A,B]\).
- The \(L\)-component transition was independently lifted to an exact
  rational point.
- The boundary kernel identity was expanded in the six coefficients
  \(1,A,B,A^2,AB,B^2\); every 302-entry coefficient vector vanishes over
  \(\mathbb Q\).
- Exact nullspaces at representatives of \(A=0\), \(B=0\), and the nonlinear
  boundary component give the same \(123/124\) profile.

## How could this be wrong?

- A modular witness proves non-divisibility and generic component
  non-containment, not a complete characteristic-zero chart cover.
- The alternative minors can still vanish on proper subvarieties of their
  target components.
- The explicit \(P\)-kernel is derived in the three-parameter \(T_B\)
  restriction. Other active parameters may change whether \(P\) lies in the
  retained \(Q\)-space or introduce further kernel directions.

## Strategy consequence

EXP-116 should quotient the \(d=0\) plane by the explicit \(P\)-kernel:

1. remove a fixed nonzero kernel coordinate, preferably the \(y^8\) column;
2. search the complete 302-row system for 124-by-124 augmented minors;
3. prove a uniform nonzero-minor cover in \(A,B\), or compute the exact
   residual ideal where the rank gap may fail;
4. separately intersect the three \(d\ne0\) alternative minors with their
   target factors.

The quotient-boundary route is now first priority. A raw 125-minor search on
\(d=0\) is permanently retired.
