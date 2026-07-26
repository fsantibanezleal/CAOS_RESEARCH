# EXP-101: First explicit GGHV minor transition

## Result

The experiment is **CONFIRMED** with one cost-prediction refutation.

The combined perturbation rank is \(97\), not at most \(48\). Despite that
failed estimate, the exact reduced determinant completed inside the declared
five-minute budget. The low-rank factorization and direct 125 by 125 determinant
checks agree.

## Forced-axis factor

The exact characteristic polynomial of the normalized forced \((1,0)\)
direction is

\[
\chi_{B_x}(\lambda)=\lambda^{109}(\lambda-1)^{16}.
\]

Therefore

\[
\det(I+uB_x)=(1+u)^{16}.
\]

This proves the factor suggested but not established by EXP-100. The matrix is
not a projector because it has nontrivial nilpotent structure in its
zero-eigenspace, which explains rank \(32\) together with trace \(16\).

Its only determinant zero is \(u=-1\), where the forced \(x\)-vertex
coefficient vanishes and the declared GGHV stratum is left.

## Exact first minor stratum

For

\[
s=\varepsilon_{(0,1)},\qquad
t=\varepsilon_{(1,7)},
\]

the selected augmented minor satisfies

\[
\frac{\det A(s,t)}{\det A_0}
=
\frac{(st-8)^6
\left(
32768s^9-(st-8)^7
\right)}{549755813888}.
\]

Equivalently,

\[
\frac{\det A(s,t)}{\det A_0}
=
\frac{(st-8)^6
\left(
2^{15}s^9-(st-8)^7
\right)}{2^{39}}.
\]

This factorization is exact. Three independent direct determinants agree with
the reduced formula.

The trace checks also agree:

\[
\operatorname{tr}B_s=0,\qquad
\operatorname{tr}B_t=0,\qquad
\operatorname{tr}(B_sB_t)=\frac{13}{8}.
\]

Hence the \(st\) coefficient is

\[
-\frac{13}{8},
\]

matching the determinant polynomial.

## First chart transition

The bounded rational search found

\[
(s,t)=(-8,-1),
\qquad st=8.
\]

At this point the first minor vanishes, but exact full ranks are

\[
\operatorname{rank}M=124,\qquad
\operatorname{rank}[M\mid b]=125.
\]

The fiber remains inconsistent. Row and column pivot extraction produced an
explicit alternative 125 by 125 augmented minor containing the right-hand-side
column and nonzero at this point.

The Gröbner basis of the first and alternative minor ideal reduces to the
single residual factor

\[
g(s,t)=
s^9-\frac{s^7t^7}{32768}
+\frac{7s^6t^6}{4096}
-\frac{21s^5t^5}{512}
+\frac{35s^4t^4}{64}
-\frac{35s^3t^3}{8}
+21s^2t^2
-56st+64.
\]

Multiplying by \(2^{15}\) gives the simpler form

\[
2^{15}g(s,t)=2^{15}s^9-(st-8)^7.
\]

Thus the first two minors cover the full component \(st=8\). Their remaining
common zero locus is the rational curve

\[
2^{15}s^9=(st-8)^7.
\]

Because \(\gcd(7,9)=1\), it has the rational parametrization

\[
s=8u^7,\qquad
st-8=64u^9,\qquad
t=\frac{8u^9+1}{u^7},
\quad u\ne0.
\]

The point \(u=1\) gives \((s,t)=(8,9)\), where both existing minors vanish.
This is the next exact closed stratum for a third chart.

## Adversarial validation

- The 97-dimensional Sylvester reduction reconstructed both normalized
  perturbations exactly.
- Linear and mixed coefficients agree with independent trace identities.
- Three direct 125 by 125 determinants agree with the reduced polynomial.
- At the first-minor zero, full bracket and augmented ranks were recomputed
  directly.
- The alternative minor includes the right-hand-side column and is explicitly
  nonzero at the transition point.

## Route decision

The constructible determinantal-strata method has now moved from a control to
the actual GGHV matrix:

1. chart 1 covers the complement of its factored zero locus;
2. chart 2 removes the complete \(st=8\) component;
3. the only residual on this slice is the parametrized curve above;
4. compute chart 3 at \(u=1\), pull its determinant back to the \(u\)-line, and
   decide the remaining finite residual.

This is an exact two-parameter slice result, not yet the full 51-parameter
coverage.

## Scope and non-claims

- The two-parameter slice is not yet completely excluded because the residual
  curve remains.
- No conclusion covers the other 49 parameters or the other forced branches.
- The complete \((72,108)\) case and \(JC(2)\) remain open.

## How could this be wrong?

- The parametrization excludes \(u=0\); however \(s=0\) does not lie on the
  residual curve because then its equation reads \(0=(-8)^7\).
- The alternative minor polynomial is tied to the selected rows and columns,
  but its nonzero value and the computed ideal are exact.
- Completing this slice requires checking every residual point of the third
  chart pullback, not sampling values of \(u\).
