# Fixed-input parameter improvement and ceiling

All source constants are those frozen in the declaration. The source's
mixed-Gram inequality and analytic/local inputs are attributed to
arXiv:2609.33043v1. This note verifies their parameter assembly, not the
full interval certificate or an independent zero-counting theorem.

## Compatibility of the matrix certificate

Let `U` be Hermitian with unit diagonal, `1<=D_ii<=2`,
`G=D^(1/2) U D^(1/2)`, and let `C` clip the eigenvalues of `U-I` from above
at `tau`. Set `M=D^(-1/2) C D^(-1/2)` and `B=2D+2M`.
Since `C<=tau I`,
`B<=2(D+tau D^(-1))<=2c I` when
`c>=max(1+tau,2+tau/2)`; the scalar function `x+tau/x` is convex on `[1,2]`.
In an eigenbasis of `G`, completing squares gives
`tr phi_c(G)>=tr BG-tr B^2/4` for all `B<=2c I`.
Using the unit diagonal of `U`, expansion subtracts `tr D^2` and leaves
`2tr C(U-I)-tr M^2`. Since `D_ii>=1`,
`tr M^2=sum_ij |C_ij|^2/(D_ii D_jj)<=tr C^2`.
The remaining spectral sum is `tr Psi_tau(U)`. This re-derivation checks
the clipping threshold and shows why the multiplicity endpoints cannot
simply be ignored during parameter tuning.

## The fixed counting assembly

For a block of `m` points, the imported local inequality and the source's
pinching argument yield a defect at least
`a l-beta W-o(N)`, provided `delta(m-6)<=tau^2`, with
`a=delta(1-6/m)` and `beta=6p(1-6/m)`. The high-multiplicity and off-line
pair residuals are `rh=6c-7-c^2` and `rk=4c-2-c^2`.
When `rh>=a` and `rk>=2a`, they may both be discarded, producing
`(2-a) N_d >= (1+H0-beta) N-o(N)`.
This is the count of distinct zeros in the strip, not of distinct zeros
on the line. Its analytic and certificate dependencies remain those of
the source.

## Feasible improvement

Substitute `m=1310`, `tau=2411/1000`, `c=3411/1000`.
The canonical result records every rational slack. In particular
`tau^2-delta(m-6)=3601/1000000`,
`c-(1+tau)=0`, and the high and off-line residuals remain strictly positive
after subtracting `a` and `2a`. The resulting `q(m)` is strictly larger
than the source's exact fraction at `m=1298`.

## Uniform cap, not a census

The off-line-pair requirement is
`(c-2)^2<=2-2a`. Since admissibility gives `c>=2`, it implies
`c<=2+sqrt(2-2a)` and `tau<=c-1<=1+sqrt(2-2a)`.
Consequently a necessary condition is

```text
D(m):=delta(m-6) <= (1+sqrt(2-2a(m)))^2.
```

At `m=1311`, put `z=D(m)-3+2a(m)`.
The exact certificate has `z>0` and `z^2>4(2-2a(m))`, the strict reverse
of the necessary condition after squaring with the correct sign.
For larger `m`, `D(m)` increases, while `a(m)` increases and the
right-hand side decreases. Thus every integer `m>=1311` is excluded.
The high-multiplicity constraint is unnecessary for this exclusion;
dropping a constraint makes the necessary-condition argument stronger.

Finally write `t=1-6/m`. Then
`q=(1+H0-6pt)/(2-delta t)`, whose derivative in `t` has the sign of
`delta(1+H0)-12p`. That exact rational is positive. Therefore the
feasible `m=1310` maximizes `q` among all integer blocks in this fixed-input
scalar-clipping proof. This says nothing about new windows, different
block estimates, multiplicity-sensitive clipping or a new analytic input.
