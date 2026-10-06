# Second native input-audit declaration: Taylor remainders

Declared after preserving the inconclusive direct-interval pilot and before
implementing this variant. This is an additional input audit of EXP-023,
with the same frozen target, tables, pressure weights and worker runtime.

Let B=sum_j |c_j| and A=B/K(0). The Fourier integral over [-1/2,1/2]
gives |K^(r)(x)/K(0)| <= pi^r A for every real x and integer r>=0,
without assuming positivity of the window. The product rule gives
|w^(r)(x)| <= (2*pi)^r A^2, where w=(K/K(0))^2.
Use interval upper bounds for A and every constant.

At each rational cell midpoint evaluate K,K',K'',K''' using native 0F1.
In addition to the identities in native-table-audit-declaration.md, use

    sinc'''(z) = (z/5)*0F1(7/2;-z^2/4)
                 -(z^3/105)*0F1(9/2;-z^2/4).

It follows by differentiating the already declared second derivative.
Assemble w'=2*K*K'/K(0)^2 and
w'''=2*(3*K'*K''+K*K''')/K(0)^2.
For radius R, the entire closed cell has lower bounds

    w(mid) - |w'(mid)| R - (2*pi)^2 A^2 R^2/2,
    w''(mid) - |w'''(mid)| R - (2*pi)^4 A^2 R^2/2.

The first may be replaced by zero when negative because w>=0.
Every comparison uses stored binary64 values as exact dyadic rationals.
Bisect at most eight levels if a whole-cell comparison is unresolved.
Validate the third-derivative identity against its divided sine/cosine form
at nonzero rational points and its exact value zero at z=0. Wrong-lower-bound
controls must reject increased test values without altering the actual tables.

First run 512 cells with a thirty-second cooperative budget on one CPU.
Admit the complete 52,240-cell audit only if the pilot passes its complete
range and projects at most 600 seconds. A full run has that cooperative
budget and requires every cell in both tables. Partial output is inconclusive.
The trust base remains Python/FLINT/Arb. This audit neither replaces the
eight-dimensional cover nor proves RH, a simple-zero proportion, an
effective height, external peer review or worldwide novelty.
