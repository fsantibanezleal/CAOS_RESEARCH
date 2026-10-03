# Uniform arithmetic collision and its phase scale

This proves an obstruction to one proof mechanism. It supplies no lower
bound for a signed mollifier sum or for a zero count.

For the declared family, expand

```text
h m-k n = h(kr+1)-k(hr+1) = h-k = 1.
```

Thus the twist is off diagonal. Also `h=M`, `k=M-1`,
`m<=Mr` because `r>=2`, and `n=Mr+1`.
Hence `mn<=Mr(Mr+1)<=2(Mr)^2=T/8`, with strict inequality since
`Mr>=4`. This gives the product-scale assertion for every declared case
and, in fact, for the whole integer family. The ratios are positive.

For `x>=0`, integration of `1/(1+t)` on `[0,x]` gives
`x/(1+x)<=log(1+x)<=x`. Since `hm/kn=1+1/(kn)`,

```text
H/(kn+1) <= H log(hm/kn) <= H/(kn).
```

The upper bound is exactly

```text
B^(d-a-b) / ((1-B^(-b))(1+B^(-a))).
```

The lower bound divided by the upper bound is `kn/(kn+1)`, tending to one.
Both bounds therefore have scale `B^(d-a-b)` with ratio tending to one.
Since `theta=d/(2a)` and `nu=b/(2a)`, the exponent is zero precisely at
`nu=theta-1/2`. Below that twist threshold the phase tends to infinity;
at it the phase stays bounded; above it the phase tends to zero.

The derivative scale `Delta=H/log T` used in EXP-010 is even smaller:
`Delta |log(hm/kn)| = H |log(hm/kn)|/log T`. At or beyond the threshold
it cannot tend to infinity. Increasing the number of integrations by
parts cannot turn this factor into a power saving for every twist.

The factors `16` in `T` only give fixed multiplicative factors in the
relations `H asymp T^theta`, `M asymp T^nu`. They do not alter the
exponent or the obstruction. A longer signed mollifier might still have
cancellation. In particular the power twists in this family may have
zero Mobius coefficients, so this is not evidence against its actual
moment asymptotic. That requires an estimate after summation.
