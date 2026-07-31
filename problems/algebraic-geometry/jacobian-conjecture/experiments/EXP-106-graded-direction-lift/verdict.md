# EXP-106: The \(\mathbb Z/9\) grading extends to every nonconstant lower direction

## Verdict

**CONFIRMED, with the sparsity prediction refuted.**

The grading is not rare. All 23 remaining nonconstant directions in the
persisted 26-parameter lower family are compatible with both connected chart
gradings from EXP-105. The only nominal failure is \((0,0)\), whose bracket
direction is identically zero and therefore has no selected support.

For every nonconstant lower monomial \(x^p y^q\), the intrinsic variable
residue is

\[
w_{p,q}\equiv q-p+1\pmod9.
\]

The two existing curve directions pass independently, and an artificial
one-step exponent perturbation changes the residue as required.

The lowest-support new direction is \((0,7)\), with 94 selected entries across
the two charts and residue \(8\). Its selected direction ranks are 53 and 41
modulo \(998244353\).

Artifact SHA256:
`0CBD7E19C962829CE2C9C72AFBFB7578411AD14F189E574627619EF1907C3AB3`.

## Consequence

The hidden \(\mu_9\) symmetry is global on this lower-family matrix, not an
accident of the closed two-parameter slice. For the promoted coefficient
\(v=\varepsilon_{(0,7)}\), the invariant variable is \(y=v/u\). The two chart
determinants then have \(z=u^9\) width only 14, so a 16-by-64 bivariate NTT
grid is sufficient for a modular three-variable pilot.

Compatibility is a compute reduction, not a rank certificate. EXP-107 must
construct enough bivariate minors to decide their common zero locus.
