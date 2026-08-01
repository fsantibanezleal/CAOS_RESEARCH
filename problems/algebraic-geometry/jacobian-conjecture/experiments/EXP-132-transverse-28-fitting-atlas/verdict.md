# EXP-132 verdict - exact transverse atlas on the direct A=0 boundary

Status: **CONFIRMED COMPLETE EXACT FITTING ATLAS** for the declared
`A=0,d=1` five-coefficient boundary.

## Exact result

EXP-132 adds the `(2,8)` coefficient `T` to the direct specialized family

\[
M_0(B,C,T)=M_{\rm forced}+B M_{(0,5)}+C M_{(2,9)}+T M_{(2,8)}.
\]

Three exact 125-row sections of the original 302-by-125 augmented matrix have,
up to nonzero rational scalars, the determinants

\[
P(B)=(5B+4)^3(25B^2-20B+16)^3,
\]

\[
\begin{aligned}
Q(B,C,T)=B^{95}(&4785156250B^{12}+9765625B^{11}CT\\
&-1050000000B^9-10214400000B^6\\
&+1061683200B^3+5435817984),
\end{aligned}
\]

and

\[
R(B,C,T)=B^{105}C.
\]

The primary EXP-131 section is exactly independent of `T`. The second is
exactly affine in `T`, and its only new term is proportional to
`B^106*C*T`. The residual-selected third section has an acyclic normalized
dependency graph and reconstructs as the monomial `B^105*C`, independently
of `T`.

Consequently

\[
Q-9765625BT R=Q_0(B),
\]

where

\[
Q_0(B)=4785156250B^{107}-1050000000B^{104}
-10214400000B^{101}+1061683200B^{98}+5435817984B^{95}.
\]

The accepted artifact persists exact polynomials `u(B),v(B)` satisfying

\[
u(B)P(B)+v(B)\bigl(Q(B,C,T)-9765625BT R(B,C,T)\bigr)=1.
\]

Thus these three maximal minors generate the unit ideal in
`QQ[B,C,T]`. Equivalently, the zeroth Fitting support of the augmented
cokernel is empty on this boundary, and the full-column-rank polynomial
matrix is zero-right-prime there.

## Predictions

1. **Confirmed:** every `T=0` regression control reproduces EXP-131 exactly.
2. **Confirmed more strongly:** the two EXP-131 sections have exact `T` degrees
   zero and one, below the predicted degree-eight gate.
3. **Refuted:** three inherited sections do not survive. The EXP-123 shared
   basis and EXP-124 graph basis vanish identically after direct `A=0`
   specialization. New residual-selected bases were required.
4. **Confirmed more strongly:** the joint ideal is the unit ideal, rather than
   merely having residual dimension at most one.

## Controls and adversarial validation

- The original complete matrix is rebuilt from the bracket equations and the
  EXP-131 determinant formulas and Bezout identity are checked at `T=0`.
- Degree profiles agree at primes 1009 and 1153. The inherited bases that
  vanish are recorded with degree `-1`, not misclassified as constants.
- The first residual basis is stable on the linear and both quadratic fibres
  at both primes and is nonzero on 36 curve controls.
- At primes 109 and 127, all 18 split finite controls have augmented rank 125
  and choose the same final row basis.
- The final basis is reconstructed in characteristic zero from 106 singleton
  cyclic components. Three direct exact 125-by-125 determinants verify the
  block product.
- The normalized determinant scalars are checked to be nonzero constants, the
  `CT` elimination is expanded directly, and the final Bezout identity expands
  to exactly one.
- The accepted run completed in 116.18 seconds, within every declared gate.
- Accepted result SHA-256:
  `9465FD7E112733C0D21EB011A432898578D5ECB39FDDBE87E141C2ACE71AB0F4`.
- Exact worker SHA-256:
  `8215466DBE36C5CE36C3F929864BE8A8D940A436DA3AA709D289E82C68DC7891`.

Two deliberately stopped approaches are not used in the proof. Direct
three-variable expansion of the final determinant reached the five-minute
gate, and a generic expression-domain quadratic quotient also reached its
gate. Exact SCC decomposition exposed the acyclic block product and removed
both costs.

## Consequence and strict boundary

EXP-132 closes the complete `A=0,d=1` boundary of the declared
five-coefficient restriction

`{(0,1),(0,5),(1,0),(2,9),(2,8)}`.

It does **not** close the `A!=0,d=1` transverse lift or the `d=0` transverse
quotient. Therefore it does not yet close the complete five-coefficient
restriction. It also does not close the 24-parameter cyclic core, the full
51-parameter GGHV family, `(72,108)`, the planar degree floor, or JC(2).

## How could this be wrong?

The conclusion would fail if the original 302-row constructor, the removal of
the structural constant `Q` column, or the upstream interpretation of rank 125
were wrong. Those premises are independently persisted in EXP-111/112 and are
reconstructed here. Modular basis selection could choose misleading charts,
but every verdict-bearing determinant and the unit identity are reconstructed
over characteristic zero. Multiplying minors by nonzero rational scalars does
not change their ideal; all three scalars are explicitly checked to be
parameter-independent and nonzero.

## Next strongest path

1. Lift the accepted multi-section atlas through `(2,8)` on `A!=0,d=1`, using
   the finite graph/base-locus algebras rather than a fresh ambient Groebner
   elimination.
2. Re-audit `d=0` after adding `(2,8)`: EXP-118 closes only the old quotient,
   so the new direction must be checked against the explicit `P` kernel.
3. Treat the matrix as a module presentation and compute only the reduced
   maximal-minor/Fitting generators required on each residual algebra.
4. Use Smith/Popov invariant factors only if a positive-dimensional residual
   remains, and persist every denominator fibre. The 2026 structured Smith-form
   theorem is contextual support, not yet an applicability theorem for this
   family.
