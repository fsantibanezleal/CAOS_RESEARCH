# EXP-126 - Determinantal divisor and norm on the \(F_6\) graph curve

Declared 2026-07-30 before implementation or run.

## Question

Does the cross-prime \(F_6\) row basis persisted by EXP-125 define a nonzero
maximal-minor section on the EXP-123 graph over the irreducible curve
\(F_6(X,B)=0\), and can its exact norm reduce the remaining \(F_6\) graph
stratum to a finite divisor?

## Motivation

EXP-124 leaves three factor curves on the rational graph. EXP-125 reduces
\(F_3\) to a finite residual and persists a new cross-prime basis for
\(F_6\). The factor
\[
\begin{aligned}
F_6={}&256X^2+(-2000B^3-4800B^2+7680B-1024)X\\
 &+15625B^6-37500B^5+60000B^4-56000B^3\\
 &+38400B^2-15360B+4096
\end{aligned}
\]
is quadratic in \(X\). Therefore the graph-restricted determinant has a
canonical quotient representative \(U(B)X+V(B)\), and its function-field
norm is a univariate polynomial in \(B\).

This experiment treats the selected maximal minor as a section on
\(C_6=\operatorname{Spec}\mathbb Q[X,B]/(F_6)\), rather than as another
ambient determinant.

## Premise dependencies

1. [MV] EXP-123 gives
   \(\Delta_{\rm sh}=A^{87}(R(X,B)+YS(X,B))\) with
   \(\gcd(R,S)=1\).
2. [MV] EXP-124 gives
   \(\Delta_{\rm alt}=A^{90}F_3F_6F_7\) up to a nonzero scalar, with
   each factor coprime to \(R,S\).
3. [MV] EXP-125 finds four \(F_6\) graph points over each of 739 and 811
   with rank profile \(124/125\), and persists a cross-prime row basis
   distinct from the earlier charts.
4. [D] On \(AS\ne0\), the graph equation gives \(Y=-R/S\); after clearing
   the exact power of \(S\), zeros of a determinant section are zeros of
   its graph numerator.
5. [D] If \(F_6\) is irreducible and the graph numerator has nonzero class
   modulo \(F_6\), its zero set on \(C_6\) is finite and projects into the
   zero set of the nonzero norm in \(B\).
6. [H] The persisted \(F_6\) basis has a characteristic-zero anchor and a
   largest cyclic block small enough for exact reconstruction.

## Falsifiable predictions

1. The selected basis has a rational characteristic-zero anchor and largest
   cyclic block at most 60.
2. Its exact normalized determinant passes four direct rational
   125-by-125 controls.
3. After invariant reduction and graph substitution, the exact graph
   numerator has nonzero remainder modulo \(F_6\).
4. The remainder has \(X\)-degree at most one and its exact norm in \(B\) is
   nonzero and nonconstant.
5. The Sylvester resultant and the determinant of multiplication by the
   remainder in the quadratic quotient agree up to the declared leading
   coefficient normalization.

## Method

1. Load the complete \(302\)-row system and the \(F_6\) row basis from the
   accepted EXP-125 artifact.
2. Reproduce the EXP-124 factorization, the exact \(F_6\) formula, and its
   gcd-one relations with \(R,S\).
3. Find a rational exact anchor using the declared deterministic control
   order. Normalize the three parameter-direction matrices and compute their
   union-SCC decomposition.
4. Persist the anchor and component sizes before symbolic reconstruction.
5. If the largest block is at most 60, reconstruct the determinant ratio
   from every cyclic block in an isolated worker.
6. Reduce to \(X=A^3,Y=A^2C\), substitute the graph
   \(Y=-R/S\) with exact denominator clearing, and divide the numerator by
   \(F_6\) in \(\mathbb Q(B)[X]\).
7. Clear rational constants from the remainder and write it primitively as
   \(U(B)X+V(B)\).
8. Compute
   \(\operatorname{Res}_X(F_6,U X+V)\), factor it over \(\mathbb Q[B]\),
   and independently compute the determinant of multiplication by
   \(UX+V\) in the basis \(1,X\) of the monic quadratic quotient.
9. Compute exact diagnostic resultants with \(S\), \(R\), \(X\), and the
   \(X\)-discriminant of \(F_6\). These diagnose candidate boundary
   projections only; no factor is removed from the effective residual
   without a same-point quotient-ideal test.
10. Re-evaluate the selected determinant directly at four rational control
    points and reproduce both accepted modular \(F_6\) sample sets.

## What a PASS proves and what a FAIL proves

A PASS of predictions 1 through 5 proves that the selected minor covers a
dense open of the \(F_6\) graph curve on \(AS\ne0\), leaving only a finite
divisor whose \(B\)-projection is contained in the exact norm roots.

A nonzero constant norm would close \(F_6\) on the declared principal open.
A nonconstant norm does not cover its roots; they remain finite algebraic
point targets. A zero quotient remainder refutes this basis on \(F_6\), not
the multi-minor atlas. A missing anchor, oversized cyclic block, or worker
timeout is inconclusive.

No outcome closes \(F_7\), the finite \(F_3\) set, \(V(R,S)\), \(A=0\), the
full four-parameter restriction, the 24-parameter core, the complete
51-parameter family, \((72,108)\), the degree floor, or \(JC(2)\).

## Adversarial controls

- Reproduce \(F_6\) and its irreducibility over \(\mathbb Q[X,B]\).
- Do not infer characteristic-zero coverage from finite-field ranks.
- Reconstruct the complete selected determinant from every SCC, including
  singleton factors.
- Verify the normalized determinant by four direct exact determinants.
- Verify quotient reduction by reconstructing
  \(H=QF_6+(UX+V)\).
- Compute the norm by two exact routes.
- Treat resultant gcds as projection diagnostics, not same-point proofs.
- Preserve null, refuted, timeout, and redirected outcomes.

## Invariant-first note

The cheap deciding invariants are:

1. the quotient remainder \(H\bmod F_6\), which immediately detects whether
   the selected chart vanishes identically;
2. the quadratic norm, which decides whether the residual is finite without
   a generic Groebner basis;
3. the discriminant, which isolates singular projection values.

These invariants decide the declared curve question before any ambient
elimination is justified.

## Compute budget and kill criterion

CPU only. Exact anchor and SCC budget: 60 seconds. Isolated symbolic worker:
300 seconds. Quotient and norm arithmetic: 90 seconds. Total hard gate:
480 seconds. Persist a checkpoint before the worker and flush stage output.

Stop inconclusively if no rational anchor is found in the declared controls,
if the largest cyclic block exceeds 60, if the worker exceeds 300 seconds,
or if total runtime exceeds 480 seconds. A nonzero but unexpectedly large
norm is still a valid finite-divisor result and will be persisted without
attempting algebraic root expansion.

## Exploration moment

The new viewpoint is the equivalence, on each residual curve, between:

- a maximal minor in the Fitting ideal;
- a regular section on the curve's principal open;
- a finite zero divisor;
- a univariate function-field norm.

Future charts can be combined by gcds of their divisor norms, so the atlas
accumulates a shrinking finite divisor ledger rather than unrelated
factorizations.

