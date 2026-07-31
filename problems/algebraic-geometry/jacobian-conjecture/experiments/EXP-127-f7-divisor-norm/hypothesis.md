# EXP-127 - Determinantal divisor and norm on the \(F_7\) graph curve

Declared 2026-07-30 before implementation or run.

## Question

Does the distinct cross-prime \(F_7\) row basis persisted by EXP-125 define a
nonzero maximal-minor section on the EXP-123 graph over
\[
F_7(X,B)=-156250B^7+15625B^6X+28000B^3X
          +3200B^2X^2+1024X=0,
\]
and can its quotient-ring norm reduce the remaining positive-dimensional
graph stratum to a finite divisor?

## Why this is the strongest next path

EXP-126 confirms that maximal minors treated as curve sections convert a
positive-dimensional residual component into a finite divisor without a
generic ambient Groebner basis. \(F_7\) is the only positive-dimensional
component left on the declared \(AS\ne0\) graph. Although its total degree is
seven, it is only quadratic in \(X\), so every section again has a canonical
linear representative \(U(B)X+V(B)\) and a univariate quadratic norm.

The persisted \(F_7\) basis differs from both the \(F_3\) and \(F_6\) bases.
Its characteristic-zero determinant must therefore be reconstructed rather
than reused.

## Dependencies

1. [MV] EXP-123 gives the shared graph equation
   \(R(X,B)+YS(X,B)=0\), with \(\gcd(R,S)=1\).
2. [MV] EXP-124 leaves exactly \(F_3F_6F_7=0\) after the alternative chart.
3. [MV] EXP-125 persists one \(F_7\) basis across primes 739 and 811, with
   four accepted graph samples at each prime and rank profile \(124/125\).
4. [MV] EXP-126 validates the quotient-section/norm workflow on \(F_6\).
5. [H] The distinct \(F_7\) basis admits a rational exact anchor whose largest
   union-SCC block is small enough for exact reconstruction.

## Falsifiable predictions

1. A rational anchor exists in the deterministic control list and the largest
   exact cyclic block is at most 60.
2. The reconstructed normalized determinant passes four direct 125-by-125
   rational determinant controls.
3. After invariant reduction and graph substitution, its remainder modulo
   \(F_7\) is nonzero and has \(X\)-degree at most one.
4. The exact norm in \(B\) is nonzero; hence the selected minor covers a
   dense open of the \(F_7\) graph curve.
5. A Sylvester resultant and quotient multiplication matrix give the same
   norm up to the declared leading-coefficient normalization.

## Method

1. Hash-verify the accepted EXP-123 through EXP-125 source artifacts and
   reload the exact 302-by-125 system.
2. Reproduce \(F_7\), its irreducibility over \(\mathbb Q[X,B]\), and its
   gcd-one relations with \(R,S\).
3. Reproduce all eight accepted modular \(F_7\) samples and the selected
   nonzero minor.
4. Find the first nonzero rational anchor in the established deterministic
   control order; persist its determinant and union-SCC profile.
5. Reconstruct every SCC determinant in an isolated worker only if the
   largest block is at most 60.
6. Reproduce the invariant expression in \(X=A^3,Y=A^2C\), restrict to
   \(Y=-R/S\), and divide exactly by \(F_7\) over \(\mathbb Q(B)[X]\).
7. Primitive-normalize the remainder \(U(B)X+V(B)\); compute and factor its
   norm in \(\mathbb Q[B]\) by both exact routes.
8. Classify norm factors against \(A=0\), \(S=0\), and \(R=S=0\) by
   same-point quotient arithmetic before removing any boundary factor.

## Interpretation

A PASS proves only a dense-open cover of the \(F_7\) graph component and
leaves any norm roots as finite algebraic point targets. A zero remainder
refutes this basis but not the multi-minor atlas. A missing anchor, block over
60, or worker timeout is an inconclusive computational redirect.

No result here closes the finite \(F_3/F_6\) residuals, \(V(R,S)\), \(A=0\),
the complete four-parameter restriction, the 24- or 51-parameter families,
\((72,108)\), the degree floor, or \(JC(2)\).

## Adversarial controls

- No characteristic-zero claim follows from modular rank alone.
- Reconstruct all SCC factors, including singletons.
- Compare against four direct exact determinants.
- Verify \(H=QF_7+(UX+V)\) exactly.
- Compute the norm through two independent exact representations.
- Treat ordinary resultants only as projection diagnostics; use quotient
  arithmetic for same-point boundary classification.
- Persist null, refuted, timeout, and redirected outcomes.

## Compute budget and kill criterion

CPU only. Exact anchor/SCC gate: 60 seconds. Isolated determinant worker:
360 seconds. Quotient/norm gate: 120 seconds. Total gate: 540 seconds.

Stop inconclusively if no declared rational anchor is nonzero, the largest
block exceeds 60, the worker exceeds 360 seconds, or the total gate is
exceeded. Do not expand algebraic roots and do not launch a generic Groebner
basis.
