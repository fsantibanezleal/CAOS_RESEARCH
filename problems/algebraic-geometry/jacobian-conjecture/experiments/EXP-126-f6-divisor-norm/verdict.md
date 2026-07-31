# EXP-126 - Verdict: the \(F_6\) graph curve becomes a finite residual

Verdict: **exact \(F_6\) dense-open cover confirmed; effective residual
degree 48**.

## Result

The accepted run completed in 5.78 seconds. An invariant-first audit first
found that the cross-prime \(F_6\) basis persisted by EXP-125 is exactly the
same 125-row basis whose characteristic-zero determinant was reconstructed
there for \(F_3\). The EXP-125 result and worker hashes were verified before
reuse. The exact anchor, 32-vertex largest cyclic block, invariant reduction,
graph numerator, eight modular \(F_6\) samples, and four direct rational
determinants were independently reproduced.

Let \(H(X,B)\) be this section's exact numerator after restriction to the
EXP-123 graph \(Y=-R/S\). Reduction modulo the irreducible quadratic
\(F_6(X,B)\) gives a nonzero primitive class
\[
h_6(X,B)=U(B)X+V(B).
\]
Thus the selected minor does not vanish identically on \(F_6\).

The exact function-field norm
\[
\mathcal N_6(B)
 =\operatorname{Res}_X(F_6,h_6)
\]
has degree 74. Up to a nonzero rational scalar it factors as
\[
\mathcal N_6
 =D_2\,D_3^4\,D_6^2\,Q_{18}\,Q_{30},
\]
where all five displayed factors are irreducible and their subscripts are
their degrees. The three boundary factors are persisted explicitly in
`artifacts/results.json`; the first two are
\[
D_2=25B^2-20B+16,\qquad
D_3=125B^3-300B^2+64.
\]

Exact same-point classification gives:

- on \(D_2=0\), the unique section zero has \(X=0\) and \(S=0\);
- on \(D_3=0\), both \(U,V\) vanish and \(F_6\) has the double root
  \(X=75B^2/4-15B\), where \(R=S=0\);
- on \(D_6=0\), the unique section zero has
  \(X=-125B^3/16-75B^2/4-15B-4\), where \(R=S=0\);
- \(Q_{18}\) and \(Q_{30}\) meet neither \(S=0\) nor \(X=0\), and \(U\)
  is invertible modulo both.

Therefore, on the declared principal open \(AS\ne0\), the effective
\(F_6\) residual is exactly
\[
Q_{18}(B)Q_{30}(B)=0.
\]
It has 48 normalized \(B\)-values over an algebraic closure. Each determines
one \(X\)-value and three nonzero cube roots \(A\), then
\(C=-R/(A^2S)\), giving 144 lifted algebraic \((A,B,C)\) points.

## Exact checks

- The EXP-124 factorization and the gcd-one relations of all three factors
  with \(R,S\) were reproduced.
- The accepted EXP-125 result and symbolic-worker SHA-256 hashes matched the
  verdict exactly.
- The persisted \(F_6\) and \(F_3\) row lists were identical; the \(F_7\)
  list was different.
- \(F_6\) was reproduced as irreducible over \(\mathbb Q[X,B]\).
- The exact anchor and SCC sizes matched EXP-125.
- Four direct 125-by-125 rational determinants matched the reused
  characteristic-zero section.
- Eight accepted modular \(F_6\) points reproduced factor membership, graph
  membership, \(S\ne0\), rank profile \(124/125\), and a nonzero selected
  minor.
- Polynomial division exactly reconstructed
  \(H=QF_6+h_6\), with \(\deg_X h_6=1\).
- The Sylvester resultant norm agrees exactly with the determinant of
  multiplication by \(h_6\) in the quadratic quotient, after the expected
  leading-coefficient factor.
- Direct quotient-field evaluation confirms the \(D_2,D_3,D_6\) boundary
  roles and leaves only \(Q_{18},Q_{30}\) on \(AS\ne0\).

The accepted result artifact has SHA-256
`CF9A4F6284A79344C9361CABE97D34C8FD54654FEF907DA44BD68DD399AA20B1`.

## What this proves

- The selected exact maximal minor covers a dense open of the \(F_6\) graph
  curve.
- Its complete zero divisor projects to a degree-74 norm.
- Exact boundary classification removes the \(D_2,D_3,D_6\) factors from
  the declared principal open.
- The positive-dimensional \(F_6\) stratum is reduced to 48 normalized
  values, or 144 lifted algebraic points.
- The divisor/norm formulation is a viable reusable alternative to ambient
  Groebner elimination.

## What this does not prove

- The 144 lifted \(F_6\) points are not yet covered by another minor.
- The 72 lifted \(F_3\) points are not yet covered.
- The \(F_7\) graph curve is not yet covered exactly.
- The full finite base locus \(V(R,S)\) and \(A=0\) boundary are not covered.
- The full four-parameter restriction is not closed.
- The result does not close the 24-parameter core, the complete 51-parameter
  family, \((72,108)\), the planar degree floor, or \(JC(2)\).

## Adversarial validation

No characteristic-zero claim is inferred from modular rank. The reused
determinant is accepted only after row-list identity, source hashes, anchor,
SCC profile, invariant numerator, and four direct determinants all agree.
The norm is computed by two exact algorithms. Projection resultants are not
treated as same-point proofs: the degree-2, degree-3, and degree-6 factors
are classified by direct arithmetic in their quotient fields. The
degree-3 vertical-section case is handled at the double \(F_6\) root because
ordinary resultants vanish automatically when \(U=V=0\).

## How could this be wrong?

- Completeness remains relative to the canonical EXP-071 coefficient pool.
- The point count is over an algebraic closure.
- A different chart may remove some or all of the finite
  \(Q_{18}Q_{30}\) set, but that requires another exact determinant.
- The \(F_6\) calculation does not imply anything about \(F_7\) beyond the
  earlier modular reconnaissance.

## Strategy consequence

The divisor view passes its first nontrivial test. Apply it next to \(F_7\)
using the distinct persisted \(F_7\) basis. Because \(F_7\) has larger
\(X\)-degree, first compute the quotient remainder and norm without
expanding algebraic roots. If its exact cyclic block exceeds the declared
budget, select another persisted \(F_7\) basis or combine modular divisor
sections before attempting ambient elimination.

After \(F_7\), attack the finite \(F_3/F_6\) and base-locus schemes with
algebraic point charts, then treat \(A=0\) separately.
