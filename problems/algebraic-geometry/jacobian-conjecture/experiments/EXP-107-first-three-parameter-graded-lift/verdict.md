# EXP-107: The first three-parameter lift leaves a finite residual fiber

## Verdict

**CONFIRMED as a finite-residual modular pilot; the proposed two-chart cover is
refuted.**

For the promoted coefficient \(v=\varepsilon_{(0,7)}\), use

\[
z=u^9,\qquad y=v/u.
\]

Both 125-by-125 determinant polynomials were reconstructed over
\(\mathbb F_{998244353}[z,y]\) on independent 16-by-64 NTT grids and checked
by direct off-grid determinant evaluations. Their \(y=0\) restrictions recover
the exact EXP-105 boundary polynomials.

The endpoint-safe chart is stronger than expected: it is entirely independent
of \(y\) and remains

\[
G(z)=(8z+1)^{14}
\]

up to its already recorded nonzero integer content. The other chart has 45
terms, bidegree \((14,12)\), and specializes to \(z^{12}F(z)\) at \(y=0\).

The two bivariate polynomials have gcd one but do not generate the unit ideal.
Their lexicographic Gröbner basis is zero-dimensional. On the only possible
support \(z=-1/8\), the first polynomial becomes a squarefree degree-12
polynomial \(Q(y)\). Modulo the pilot prime its factor degrees are
\(1,1,10\).

Artifact SHA256:
`40583A2BB6343A63C4570C6C97E11A3D663F38AA34E1788BACFA23E4110EB7CA`.

## Consequence

The old two charts fail only at twelve reduced geometric points in the pilot
fiber, not along a positive-dimensional component. This is a precise chart
selection problem: EXP-108 must construct a third maximal minor whose
restriction at \(z=-1/8\) is coprime to \(Q(y)\).

This modular result neither proves consistency of the three-parameter slice
nor proves or disproves JC(2). A successful third chart must be repeated and
lifted before any characteristic-zero slice-coverage claim.
