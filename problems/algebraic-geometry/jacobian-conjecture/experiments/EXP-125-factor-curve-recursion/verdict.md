# EXP-125 - Verdict: the \(F_3\) graph curve becomes a finite residual

Verdict: **exact \(F_3\) dense-open cover confirmed; original prime
prediction refuted and corrected; \(F_6,F_7\) remain curves**.

## Result

After the prime-admissibility corrections documented in `redirect.md`, the
accepted run completed in 43.82 seconds. At each of the cube-locus-admissible
primes 739 and 811, all four sampled points on each of
\(F_3,F_6,F_7\) had coefficient/augmented rank profile \(124/125\). Every
factor supplied a new 125-row basis, distinct from both the shared EXP-121
basis and the EXP-124 basis, and each selected basis appeared over both
primes.

The exact reconstruction then targeted \(F_3\). Its selected basis has one
cyclic block of size 32 and 86 singleton blocks. In invariant coordinates,
its normalized determinant has \(A\)-valuation 89 and \(Y\)-degree one.
After restricting to the EXP-123 graph and then using
\[
F_3=(5B+4)^3+16X=0,
\]
the exact univariate quotient is nonzero and has degree 37.

Up to a nonzero rational scalar, it factors as
\[
U_3(B)=(5B+4)\,Q_6(B)^2\,Q_9(B)\,Q_{15}(B),
\]
where the subscripts give the exact irreducible degrees persisted in
`artifacts/results.json`.

The factor roles are exact:

- \(5B+4=0\) forces \(X=A^3=0\), hence lies outside \(A\ne0\);
- \(Q_6\) divides both \(R|_{F_3}\) and \(S|_{F_3}\), so it belongs to the
  finite EXP-123 base locus on this factor;
- \(Q_9\) and \(Q_{15}\) divide neither \(R|_{F_3}\) nor \(S|_{F_3}\).

Therefore, on the intended principal open \(AS\ne0\), the remaining
\(F_3\) residual is exactly
\[
Q_9(B)Q_{15}(B)=0.
\]
It has degree 24. Over an algebraic closure, this gives 24 normalized
\(B\)-values and three nonzero cube roots \(A\) for each, hence 72 lifted
\((A,B,C)\) points. This is a finite residual, not a remaining curve.

## Prime-admissibility refutations

The original named-prime prediction was false as written.

1. At 1009, \(-1/16\) is not a cube, so \(F_3\) has no point with
   \(A\ne0\).
2. At 1013 and 1019, \(F_3,F_7\) have points but \(F_6\) has none.
3. A first correction using arbitrary nonzero \(X\) incorrectly selected
   601 and 643; it failed to impose \(X=A^3\).
4. The final audit enumerated \(A\) directly. The first admissible primes
   were 739 and 811, followed by 919 and 1423.

These are arithmetic sample-availability failures, not matrix-rank losses.
All failed attempts and the corrected audit are persisted under
`artifacts/`.

## Exact checks

- The three EXP-124 factors and their gcd-one relations with \(R,S\) were
  reproduced.
- Twenty-four accepted graph/factor samples—four per factor and prime—passed
  the exact modular membership checks.
- Every accepted sample had rank profile \(124/125\).
- All three factors supplied cross-prime alternative bases.
- The vectorized row-basis backend reproduces the previously persisted scalar
  basis exactly.
- The exact \(F_3\) determinant used all 87 cyclic blocks.
- Four direct 125-by-125 rational determinant controls agree with the
  reconstructed determinant.
- The graph restriction, linear \(F_3\) substitution, degree-37
  factorization, restrictions of \(R,S\), and effective degree 24 were all
  computed exactly over \(\mathbb Q\).

The accepted result artifact has SHA-256
`2470AB06210C5E8CDE09FB3F1FFA227520D6C810FBF70A8E0713BBCDC240D803`.
The accepted worker artifact has SHA-256
`5133E1600F4AA484B91B96C8FBD85DF1A5BCC70670B12050F8303BA5EABA2375`.

## What this proves

- All three EXP-124 residual curves retain full augmented rank at the
  accepted finite-field samples and expose new cross-prime bases.
- The \(F_3\) graph component is covered away from a finite exact set.
- Its principal-open residual is controlled by two explicit irreducible
  univariate polynomials of degrees 9 and 15.
- Positive-dimensional graph residuals are now confined to \(F_6\) and
  \(F_7\), plus the separate \(A=0\) boundary.

## What this does not prove

- The 72 lifted \(F_3\) points are not yet covered by another minor.
- The \(Q_6\) base-locus points are not yet covered.
- The \(F_6\) and \(F_7\) graph curves are not yet covered exactly.
- The \(A=0\) boundary is not covered.
- The full four-parameter restriction is not closed.
- The result does not close the 24-parameter core, full 51-parameter family,
  \((72,108)\), the degree floor, or \(JC(2)\).

## Adversarial validation

No characteristic-zero claim was inferred from modular rank. The exact
\(F_3\) determinant was reconstructed independently, reduced through the
graph with denominator clearing, and then reduced by the exact linear
\(F_3\) equation. The factors removed from the \(AS\ne0\) residual were
removed only after exact divisibility tests against \(R|_{F_3}\),
\(S|_{F_3}\), and the \(X=0\) equation.

## How could this be wrong?

- Completeness remains relative to the canonical EXP-071 coefficient pool.
- Modular basis persistence on \(F_6,F_7\) is reconnaissance, not an exact
  cover.
- The count of 72 lifted points is over an algebraic closure and assumes the
  principal-open conditions already verified by the exact gcd tests.
- A different chart may merge or remove residual strata, but that cannot be
  claimed until its determinant is reconstructed.

## Strategy consequence

The next positive-dimensional target is \(F_6\), because a cross-prime basis
is already persisted and \(F_6\) is quadratic in \(X\). EXP-126 should
reconstruct that basis exactly, restrict to the graph, and reduce the graph
numerator modulo the quadratic \(F_6\) relation. A nonzero quotient-ring
class will cover a dense open of \(F_6\); its resultant or norm in \(B\)
will define the finite recursive residual.

After \(F_6\), apply the same quotient-ring method to \(F_7\). The finite
\(F_3\) set and \(Q_6\) base locus can then be attacked by direct algebraic
point charts. Keep \(A=0\) as a separate boundary experiment.
