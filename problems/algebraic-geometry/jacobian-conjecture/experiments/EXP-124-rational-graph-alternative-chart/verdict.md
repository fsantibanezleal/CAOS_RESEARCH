# EXP-124 - Verdict: dense-open alternative cover of the rational graph

Verdict: **all five predictions confirmed; three residual factor curves
remain**.

## Result

The accepted exact run completed in 32.86 seconds, within the declared
390-second gate. At each of the good primes 1009 and 1013, all 20 sampled
points on the EXP-123 graph had coefficient/augmented rank profile \(124/125\).
The same deterministic alternative 125-row basis was selected over both
primes. It differs from the shared EXP-121 basis by one row.

For that basis, the exact normalized determinant has the form
\[
\Delta_{\mathrm{alt}}(A,B,C)=A^{90}N(A^3,B).
\]
In particular, it is independent of \(C\), so its restriction to
\(Y=-R/S\) introduces no denominator. The polynomial \(N(X,B)\) has 21
monomials, total degree 16, and factors over \(\mathbb Q\) as
\[
N=\frac1{272629760}F_3F_6F_7,
\]
where
\[
F_3=125B^3+300B^2+240B+16X+64,
\]
\[
\begin{aligned}
F_6={}&15625B^6-37500B^5+60000B^4-2000B^3X-56000B^3\\
&-4800B^2X+38400B^2+7680BX-15360B\\
&+256X^2-1024X+4096,
\end{aligned}
\]
and
\[
F_7=-156250B^7+15625B^6X+28000B^3X
3200B^2X^2+1024X.
\]
These are the three factors returned by exact factorization; their displayed
subscripts record total degree.

Moreover,
\[
\gcd(N,R)=\gcd(N,S)=1.
\]
Thus, on \(AS\ne0\), the alternative chart covers the dense graph open
\(N\ne0\). Its only remaining graph strata lie over the three factor curves
\(F_3=0\), \(F_6=0\), and \(F_7=0\). The finite base locus \(R=S=0\) and the
axis \(A=0\) remain separate.

## Exact checks

- The EXP-123 primitive identity \(\gcd(R,S)=1\) was reproduced.
- Forty deterministic finite-field graph points reproduced the shared
  determinant's vanishing.
- Every sampled point had rank profile \(124/125\), and the same alternative
  basis was full rank over both primes.
- The selected exact union graph has 87 cyclic components: one component of
  size 31 and 86 singleton components.
- Exact characteristic-zero reconstruction used every cyclic block.
- The determinant occupies one invariant \(A\)-residue class, with valuation
  90, and reconstructs exactly from \(X=A^3\).
- Direct 125-by-125 determinant evaluations agree at
  \((A,B,C)=(1,0,0),(1,0,1),(2,1,1),(-1,1,1)\).
- Exact factorization gives the three factors above, and exact gcd
  computations with both \(R\) and \(S\) give one.

The accepted result artifact has SHA-256
`3AE5A2DA83FA99EDFDAF06486B0AB65150D506D1378B2372710915713066D113`.
The isolated worker artifact has SHA-256
`A8EA36295D6A504D06787007472E53101BB9E135DFD24B68642FF9F545DDFDA1`.

## Interrupted launch records

An initial foreground launch was terminated by a short command-wrapper
timeout during modular output. A subsequent detached launch completed the
modular selection and exact SCC gate, but its process tree was terminated
when the launcher exited. Neither interruption reached or contradicted the
symbolic determinant result. The detached launch output is retained under
`artifacts/attempts/`; the accepted run used unchanged mathematical code and
completed within the original gate.

## What this proves

- The EXP-123 rational graph is not an irreducible obstruction for the
  complete row pool.
- One alternative minor covers a dense open subset of that graph exactly.
- The residual graph recursion is reduced to three explicit plane factor
  curves, together with the already separate finite base locus.
- Basis selection after specialization is effective here: a one-row basis
  replacement reduces the active exact block from size 34 to size 31.

## What this does not prove

- The three residual factor curves are not yet covered.
- The finite base locus \(V(R,S)\) is not yet enumerated or covered.
- The \(A=0\) boundary is not covered.
- The full four-parameter restriction is not closed.
- The result does not close the 24-parameter core, full 51-parameter family,
  \((72,108)\), the degree floor, or \(JC(2)\).

## Adversarial validation

The graph numerator was not inferred from modular samples. It was obtained
from an exact characteristic-zero determinant, reconstructed in invariant
coordinates, and checked against four direct full determinants. Since the
alternative determinant has \(Y\)-degree zero, no cancellation with a power
of \(S\) is hidden in the graph substitution. Exact gcd-one checks rule out
shared curve components with \(R\) or \(S\), but do not rule out finite
intersections.

## How could this be wrong?

- Completeness remains relative to the canonical EXP-071 coefficient pool.
- The selected minor covers only its principal open; other minors are needed
  on all three factor curves.
- Factor-curve points must still satisfy \(X=A^3\) over the working field.
  Modular reconnaissance alone cannot prove a characteristic-zero cover.
- The graph analysis assumes \(AS\ne0\); the excluded divisors require their
  own exact charts.

## Strategy consequence

The strongest next step is a recursive factor-stratum cover. EXP-125 should
sample each of \(F_3,F_6,F_7\) together with the graph equation, select
alternative row bases over both good primes, and reconstruct exact
restrictions in the corresponding quotient rings. The linear-in-\(X\)
factor \(F_3\) is the cheapest exact first target. The \(A=0\) boundary and
finite base locus remain parallel fallback paths; neither should be mixed
into the generic factor calculation.
