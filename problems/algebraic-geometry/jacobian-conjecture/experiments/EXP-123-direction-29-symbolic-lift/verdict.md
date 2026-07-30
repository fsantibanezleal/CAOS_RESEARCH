# EXP-123 - Verdict: exact affine lift and rational exceptional graph

Verdict: **confirmed affine symbolic lift; literal gcd prediction refuted by
the known axis factor**.

## Result

The accepted exact run completed in 131.86 seconds, within the declared
six-minute gate. Both good-prime reconnaissance probes returned generic
\(C\)-degree one. The exact characteristic-zero determinant then confirmed
that result.

Let \(C=\varepsilon_{(2,9)}\), set
\[
X=A^3,\qquad Y=A^2C,
\]
and use the EXP-121 shared 125-row basis on \(d=1\). Its exact normalized
determinant is
\[
\boxed{
\Delta(A,B,C)=A^{87}\bigl(R(A^3,B)+A^2C\,S(A^3,B)\bigr).
}
\]

Here:

- \(R(X,B)\) is exactly the 23-term EXP-121 polynomial, with total
  \((X,B)\)-degree 18;
- \(S(X,B)\) has 18 monomials and total \((X,B)\)-degree 19;
- \(\gcd_{\mathbb Q[X,B]}(R,S)=1\).

The complete coefficient polynomials are persisted in
`artifacts/results.json`.

Predictions 1 through 3 passed. Prediction 4, as literally written over
\(\mathbb Q[A,B]\), was refuted:
\[
\gcd\bigl([C^0]\Delta,[C^1]\Delta\bigr)=A^{87}.
\]
This is not a new common component. It is the already visible \(A=0\) axis
factor of the EXP-121 chart. After removing it and passing to \(X=A^3\), the
primitive coefficient gcd is one.

## Geometry of the selected chart

On the principal open \(A\ne0\), the selected determinant vanishes exactly
when
\[
R(X,B)+Y S(X,B)=0.
\]
Therefore:

1. on \(S\ne0\), the exceptional set is the explicit rational graph
   \[
   Y=-\frac{R(X,B)}{S(X,B)};
   \]
2. on \(S=0\), a zero requires \(R=0\);
3. because \(R\) and \(S\) are coprime plane polynomials, the base locus
   \[
   V(R,S)\subset\mathbb A^2_{X,B}
   \]
   is zero-dimensional (possibly empty).

This converts a four-variable determinant problem into one rational graph and
one finite specialization stratum. It is a genuine higher-dimensional
constructible reduction, but not yet a cover.

## Exact checks

- The 302-by-125 system and EXP-121 anchor determinant were reconstructed.
- The \((0,1)/(0,5)/(2,9)\) union graph reproduced the EXP-122 largest SCC
  size 34.
- Two modular probes gave \(C\)-degree one:
  - \(p=1009\), \((A,B)=(2,3)\);
  - \(p=1013\), \((A,B)=(3,5)\).
- The exact \(C=0\) specialization reproduces the complete EXP-121
  determinant.
- At \((A,B)=(1,0)\), the exact polynomial is
  \(1+3C/544\), reproducing EXP-122.
- Four independent rational controls agree with direct exact 125-by-125
  determinant ratios:
  \[
  (A,B,C)=(1,0,1),(2,1,1),(1,1,-1),(0,1,2).
  \]
- The coefficient \(A\)-valuations are exactly 87 and 89. Each coefficient's
  remaining \(A\)-exponents occupy one residue class modulo three.
- Direct substitution reconstructs
  \(A^{87}(R(A^3,B)+A^2CS(A^3,B))\) exactly.

The accepted result artifact has SHA-256
`43C24C42F37F952AB09EAA834EC042DBA7B7E3E02C1AF1E52E13691C7E9D30EF`.

## Interrupted attempt

Attempt 001 completed both modular affine probes but was externally
terminated during the timeout-isolated symbolic worker because the shell
wrapper withheld progress output. All descendant processes were stopped, no
symbolic claim was produced, and the event is preserved under
`artifacts/attempts/`. The accepted retry used unchanged determinant code and
completed inside the original gate.

## What this proves

- The EXP-122 anchor-line linearity is not a specialization accident. It
  persists over the full symbolic \(A,B\) chart.
- The four-parameter selected determinant depends on the new coefficient only
  through \(Y=A^2C\), and only affinely.
- Away from \(A=0\), the selected exceptional locus is one rational graph
  with a finite base locus.
- The \((2,9)\) path is strictly more tractable than a generic
  24-variable determinant and remains the strongest continuation.

## What this does not prove

- The rational graph has not yet been covered by an alternative minor.
- The finite base locus \(V(R,S)\) has not yet been enumerated or covered.
- The \(A=0\) four-parameter boundary is not closed by this chart.
- No four-parameter restriction is yet excluded.
- The result does not close the 24-parameter core, full 51-parameter family,
  \((72,108)\), the planar degree floor, or \(JC(2)\).

## Adversarial validation

The symbolic determinant was computed from all 86 cyclic diagonal blocks:
one block of size 34 and 85 cyclic singleton blocks. It was not inferred from
the SCC support or from the modular probes. The four direct full-matrix
controls are independent of the blockwise symbolic expansion. The primitive
gcd was computed only after exact residue-class reduction to
\(\mathbb Q[X,B]\).

## How could this be wrong?

- This is one row basis. Other minors can have different invariant
  coordinates and exceptional sets.
- Coprimality proves that \(V(R,S)\) has no curve component; it does not prove
  that the base locus is empty.
- The rational graph statement is on \(A\ne0\). The \(A=0\) divisor must be
  handled by another chart or quotient.
- Completeness remains relative to the canonical EXP-071 coefficient pool.

## Strategy consequence

Declare EXP-124 to select alternative complete-row bases directly on the
rational graph
\[
Y=-R/S
\]
over finite fields, reconstruct their exact determinants in
\((X,B,Y)\), and restrict them to the graph. The first decision target is a
nonzero graph-restriction polynomial, not a full cover. If obtained, factor
its numerator and recurse only on those factors together with the finite base
locus \(R=S=0\).

Treat \(A=0\) separately. Do not mix the axis boundary into the generic graph
calculation, and do not recompute the already closed three-parameter \(T_B\)
restriction.
