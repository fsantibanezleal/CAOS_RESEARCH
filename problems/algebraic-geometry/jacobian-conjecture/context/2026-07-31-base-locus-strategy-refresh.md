# Jacobian strategy refresh: the base locus as a finite algebra

Date: 2026-07-31.

This refresh was completed after EXP-129 and before EXP-130. It asks whether
the finite base locus of the EXP-123 chart should be attacked by point
enumeration, ambient elimination, or a different exact object.

## Current exact input

EXP-123 gives

\[
\Delta=A^{87}\bigl(R(A^3,B)+A^2C S(A^3,B)\bigr),
\qquad \gcd(R,S)=1.
\]

The persisted polynomials have 23 and 18 monomials, with degrees 5 and 4 in
\(X=A^3\). EXP-129 closes the rational graph over \(AS\ne0\). The two
uncovered boundaries are the finite scheme \(V(R,S)\) and the separate
divisor \(A=0\).

## Fresh primary-source review

1. Guccione, Guccione, Horruitiner, and Valqui leave the \((72,108)\)
   frontier and construct the reduced polynomial systems used here:
   <https://arxiv.org/abs/2204.14178>.
2. Jelonek proves a component dichotomy in bounded-degree constant-Jacobian
   parameter spaces. It is valuable global structure, but no proved map
   identifies those components with the determinantal strata of this reduced
   bracket-\(x^2\) coefficient family:
   <https://arxiv.org/abs/2607.20597>.
3. Lee and Li constrain inner polynomials of an original planar Jacobian pair.
   EXP-095 through EXP-097 already show that the required transport to the
   final reduced coefficients is missing:
   <https://arxiv.org/abs/2408.01279>.
4. Sparse FGLM methods use multiplication matrices and CRT structure for
   zero-dimensional ideals. This is directly applicable after the base-locus
   ideal is certified zero-dimensional:
   <https://arxiv.org/abs/1304.1238>.
5. Module border bases characterize finite-codimension quotient modules by
   rewrite rules and commuting multiplication matrices. This supports treating
   the restricted row system over the finite coordinate algebra rather than
   evaluating it point by point:
   <https://arxiv.org/abs/1302.6383>.

No source in this pass proves or disproves JC(2), closes \((72,108)\), or
supersedes the exact GGHV matrix analysis.

## Alternative viewpoint

Let

\[
K=\bigl(\mathbb Q[X,B]/(R,S)\bigr)[X^{-1}].
\]

The saturation by \(X\) separates the principal-open base locus from the
\(A=0\) boundary. If \(K\) is finite-dimensional, every selected maximal
minor restricts to an element of one finite algebra. Multiplication by that
element gives a matrix on \(K\):

- a nonzero determinant means that the section is a unit on the whole scheme;
- several sections cover the scheme exactly when their generated ideal is the
  unit ideal in \(K\);
- CRT decomposition records repeated points, nilpotent structure, and local
  failures without choosing algebraic roots.

This is a Fitting-ideal test in a finite algebra, not a list of sampled points.
It combines the determinantal, quotient-algebra, and scheme-theoretic views.

## Ranked approaches for EXP-130

| Rank | Method | Proof value | Decision |
|---|---|---|---|
| P0 | Exact saturation plus finite quotient algebra | Separates \(A=0\), counts the scheme with multiplicity, and gives a canonical arena for chart certification | run first |
| P0 | Multi-section unit-ideal test in the quotient algebra | Can close the complete finite base locus without root solving | run after the quotient basis is certified |
| P1-control | Independent resultant/subresultant and multiplication-matrix checks | Detects projection or multiplicity mistakes | mandatory adversarial route |
| P2 | Algebraic-number point enumeration | Useful for diagnostics and row selection, but duplicates conjugate work | use only for reconnaissance |
| retired | Generic ambient Groebner sweep on the full parameter family | High cost and weaker scope than the finite algebra | do not run |

## Strategy decision

EXP-130 first computes and independently verifies the saturated base-locus
algebra. If it is empty, the principal-open base locus is closed immediately.
If it is nonempty, row bases are selected modularly and reconstructed exactly,
then their classes are tested for the unit ideal in the complete finite
algebra. The experiment stops before any unbounded ambient elimination.

