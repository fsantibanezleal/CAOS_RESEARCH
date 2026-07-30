# EXP-125 - Recursive cover of the EXP-124 factor curves

Declared 2026-07-30 before implementation or run.

## Question

On the EXP-123 graph and the EXP-124 residual divisor
\[
N(X,B)=F_3(X,B)F_6(X,B)F_7(X,B)=0,
\]
does the complete 302-row system retain augmented rank 125, and can an
alternative minor reduce the cheapest component \(F_3=0\) to finitely many
explicit \(B\)-values?

## Motivation

EXP-124 gives an exact dense-open graph cover
\[
\Delta_{\rm alt}=A^{90}N(A^3,B)
\]
and factors \(N\) into three plane factors of total degrees 3, 6, and 7.
All three are coprime to the EXP-123 polynomials \(R,S\). The constructible
atlas should therefore recurse on those factors rather than recompute a
generic determinant.

The degree-3 factor
\[
F_3=125B^3+300B^2+240B+16X+64
\]
is linear in \(X\). It admits the exact substitution
\[
X=-\frac{125B^3+300B^2+240B+64}{16}.
\]
This makes \(F_3\) the lowest-cost exact component. The higher factors are
included in modular reconnaissance so that the next priority can be based on
rank evidence rather than degree alone.

## Premise dependencies

1. [MV] EXP-123 gives
   \(\Delta_{\rm sh}=A^{87}(R(X,B)+YS(X,B))\) with
   \(\gcd(R,S)=1\).
2. [MV] EXP-124 gives a cross-prime alternative basis and
   \(\Delta_{\rm alt}=A^{90}N(X,B)\).
3. [MV] EXP-124 factors \(N\) exactly as a nonzero scalar times
   \(F_3F_6F_7\), and each factor is coprime to \(R,S\).
4. [D] On \(AS\ne0\), a point of a factor curve lifts to the graph through
   \(Y=-R/S\) and \(C=Y/A^2\).
5. [H] Specializing to a residual factor exposes another complete-row basis
   whose minor is generically nonzero there.

## Falsifiable predictions

1. For each \(F_i\), \(i=3,6,7\), at least four graph points over each of
   1009 and 1013 with \(AS\ne0\) have coefficient/augmented rank profile
   \(124/125\).
2. Each factor supplies at least one alternative 125-row basis distinct from
   both the shared EXP-121 basis and the EXP-124 basis.
3. The best \(F_3\)-selected basis appears over both primes and has largest
   exact cyclic block at most 60.
4. Its exact determinant restricts to a nonzero polynomial on the
   intersection of the graph with \(F_3=0\).
5. After exact denominator clearing, the \(F_3\) restriction is a
   nonconstant univariate polynomial in \(B\). A nonzero constant would be
   stronger and will be accepted as a complete \(F_3\) cover.

## Method

1. Load \(R,S,F_3,F_6,F_7\) from accepted EXP-123/124 artifacts.
2. Over each good prime, enumerate deterministic \((A,B)\) with \(A\ne0\),
   \(F_i(A^3,B)=0\), and \(S(A^3,B)\ne0\). Set
   \(Y=-R/S\), \(C=Y/A^2\), evaluate the complete matrix, and retain at least
   four points per factor.
3. Record coefficient/augmented ranks and deterministic independent row
   bases. Prefer a basis observed over both primes, then minimize changes
   from the EXP-124 basis.
4. For the selected \(F_3\) basis, find an exact rational anchor and compute
   the union-SCC decomposition for the \(A,B,C\) directions.
5. If the largest block is at most 60, reconstruct its exact determinant
   from every cyclic block under an isolated 300-second worker.
6. Reduce the determinant to invariant coordinates \(X=A^3,Y=A^2C\).
   Restrict first to the graph \(Y=-R/S\), clearing the exact power of \(S\),
   and then substitute the linear \(F_3\) formula for \(X\).
7. Persist the primitive univariate numerator in \(B\), its factorization,
   degree, rational roots, and gcds with the corresponding restrictions of
   \(R\) and \(S\).
8. Verify four direct exact determinant controls and modular evaluations on
   both the covered and residual parts whenever rational controls exist.

## What a PASS proves and what a FAIL proves

A PASS of prediction 4 proves that a dense open subset of the \(F_3\) graph
stratum is covered by the new minor. If prediction 5 also passes, only the
finite zero set of the univariate residual, together with intersections
where denominators vanish, remains on that component.

A nonzero constant closes \(F_3\) on \(AS\ne0\). A zero restriction refutes
the selected basis but not the factor-cover strategy. A sampled rank loss is
finite-field evidence only until reconstructed exactly. A budget stop is
inconclusive.

No outcome closes \(F_6\), \(F_7\), \(V(R,S)\), \(A=0\), the full
four-parameter restriction, the 24-parameter core, \((72,108)\), the degree
floor, or \(JC(2)\), unless those strata are separately and exactly covered.

## Adversarial controls

- Reproduce the EXP-124 factorization and gcd-one claims exactly.
- Require every sampled point to satisfy both its factor equation and the
  EXP-123 graph equation.
- Require a newly selected basis to differ from both existing bases.
- Select across both primes when available.
- Reconstruct the exact characteristic-zero determinant before quotient
  substitution.
- Clear graph and \(F_3\) denominators explicitly; do not infer a quotient
  claim from finite-field samples.
- Preserve refuted, null, and timeout outcomes.

## Compute budget and kill criterion

CPU only. Modular reconnaissance budget: 120 seconds. Exact worker budget:
300 seconds. Total hard gate: 450 seconds. Persist a checkpoint after each
factor/prime pair and before symbolic work. Stop inconclusively if any factor
cannot supply four points within the modular gate, if the \(F_3\) largest
cyclic block exceeds 60, or if the exact worker times out.

## Exploration moment

This experiment changes the recursive coordinate system from the ambient
four parameters to the normalization of a residual factor. The linear
\(F_3\) equation eliminates \(X\), while the graph eliminates \(Y\); the
remaining determinant question is univariate in \(B\). This is the sharpest
available dimension reduction. The higher factor curves will be prioritized
after their modular rank and basis diversity are measured.
