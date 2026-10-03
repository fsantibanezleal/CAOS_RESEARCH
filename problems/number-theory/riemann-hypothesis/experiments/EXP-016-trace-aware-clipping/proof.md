# Trace-aware clipped-block estimate and its exact consequence

## Zero-sum convexity

Write psi_tau(x)=x^2 for x<=tau and 2 tau x-tau^2 otherwise.
For tau>0 this is convex on the real line. Let x_1,...,x_m sum to zero,
and suppose x_1=s>=tau. The mean of the other displacements is
-s/(m-1)<=0, in the quadratic part of psi_tau. Scalar Jensen gives

    sum psi_tau(x_i) >= 2 tau s-tau^2+s^2/(m-1).

The right side is strictly increasing for s>=tau, since its derivative
is 2 tau+2s/(m-1)>0. Its value at s=tau is tau^2 m/(m-1).
This holds for all real zero-sum spectra, with no numerical sampling.

Equality requires s=tau and x_2=...=x_m=-tau/(m-1), by strict
convexity on the negative half-line. For 0<tau<=m-1 it is realized by
the PSD unit-diagonal equicorrelation matrix
U=(1-tau/(m-1))I+(tau/(m-1))J, where J has every entry one.
Its eigenvalues are 1+tau and 1-tau/(m-1), the latter m-1 times.
The displacement inequality is a standard zero-sum variance/Jensen
mechanism. No new universal matrix-method priority is claimed.

## The modified source dichotomy

Each source block U_B is a Gram matrix with unit diagonal and trace m.
If all its eigenvalue displacements are <=tau, the clipped defect
equals tr(U_B-I)^2, so the original local energy-plus-pressure estimate
applies unchanged. Otherwise the preceding estimate gives defect at
least tau^2 m/(m-1). Thus the same defect-plus-pressure conclusion
holds whenever delta(m-6)<=tau^2 m/(m-1). This is a weaker sufficient
condition than the original delta(m-6)<=tau^2. The pressure coefficient,
smoothing limit, pinching, mixed-multiplicity threshold and counting
residuals remain unchanged and attributed to the source.

Consequently q(m)=(1+H0-beta(m))/(2-a(m)) is still the bound, now under
the modified admissibility condition. The fixed rational choice in the
declaration passes all constraints at m=1311, and q(1311)>q(1310).
EXP-013's original-dichotomy optimum is not contradicted.

## Uniform cap in the modified scalar assembly

The off-line-pair residual still gives c<=2+sqrt(2-2a(m)) and tau<=c-1.
Therefore a necessary condition is

    D_new(m)=delta(m-6)(m-1)/m <= (1+sqrt(2-2a(m)))^2.

At m=1312, z=D_new-3+2a is positive and
z^2-4(2-2a)>0, as an exact rational substitution shows. This is
the strict reverse of the necessary condition, with squaring legal
because z>0. For m>=7, D_new'=delta(1-6/m^2)>0 and a'>0,
while the right side decreases. Thus every m>=1312 is excluded.
The q monotonicity already proved in EXP-013 makes m=1311 optimal
within this modified scalar-clipping assembly.

This does not optimize other convex spectral functions, local certificates,
windows or multiplicity-sensitive matrix witnesses. The zeta consequence
inherits the analytic and local inputs; no full external replay or new
simple-critical/short-window theorem follows.
