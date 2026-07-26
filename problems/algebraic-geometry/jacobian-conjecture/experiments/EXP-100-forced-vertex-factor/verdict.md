# EXP-100: Forced-axis factor suggested, residual strict flag refuted

## Result

The declared forced-projector and residual-flag prediction is **REFUTED**.

The exact normalized \((0,0)\) direction is zero, as required by the bracket
identity. The normalized forced \((1,0)\) direction has

\[
\operatorname{rank}B_x=32,\qquad \operatorname{tr}B_x=16,
\]

but it is not idempotent. It is therefore not the predicted rank-16 projector.

At the five exact values

\[
u\in\{-2,-1,1/2,1,3\},
\]

the axis determinant nevertheless equals

\[
\det A_0(1+u)^{16}.
\]

These checks suggest a characteristic-polynomial factor, but five evaluations
do not prove the polynomial identity. The factor must not be used until an
exact characteristic-polynomial or equivalent minimal-polynomial calculation
confirms it.

After removing \((0,0)\) and fixing \((1,0)\), the remaining 24 perturbations
still do not preserve a common strict flag. The shortest recorded cycle uses
the interior directions

\[
(1,7)\longrightarrow(0,1),
\]

and its labelled product has exact trace

\[
\operatorname{tr}(B_{(1,7)}B_{(0,1)})=\frac{13}{8}.
\]

All three normalized mixed determinant controls differ from the base
determinant. The artifact reproduced byte-for-byte with SHA-256
`A5D28B1BE4F64212BE1EEECDC5234C83EA1C2E65F5AFED1A4BADA4E21C0EBA5D`.

## Route decision

The common-flag route is closed for this selected minor, even after forced
vertex normalization. The first genuine interior interaction is now localized
to a two-parameter cycle. This is useful compression: rather than expand a
26-variable determinant, compute

\[
f(s,t)=\det\left(I+sB_{(0,1)}+tB_{(1,7)}\right)
\]

by a low-rank determinant reduction. Then:

1. factor \(f\);
2. identify its residual zero locus;
3. compute alternative augmented minors on that locus;
4. test whether their ideal with \(f\) is the unit ideal.

That is the first direct application of EXP-098's constructible
determinantal-strata contract to the actual GGHV matrix.

## Scope

- No simultaneous GGHV subfamily has been closed by EXP-100.
- The result replaces a 24-direction structural guess with one exact
  two-direction cycle.
- It does not exclude \((72,108)\) or decide \(JC(2)\).

## How could this be wrong?

- The union-support graph depends on the chosen base minor and basis. Another
  minor may admit a common flag.
- The nonzero product trace proves a genuine interaction for this
  normalization, but cancellations can still simplify the complete bivariate
  determinant.
- The suggested \((1+u)^{16}\) factor is not yet proved.
