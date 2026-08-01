# EXP-135 verdict - ambient transverse section inertness

Status: **PROVED IN CHARACTERISTIC ZERO**.

## Exact theorem

For the accepted EXP-124 normalized section, let

`H(A,B,C)=I+(A-1)K_(0,1)+B K_(0,5)+C K_(2,9)`

on its unique 33-by-33 cyclic core, and let `K_T=K_(2,8)`. Then

`det(H(A,B,C)+T K_T)=det(H(A,B,C))`

in `QQ[A,B,C,T]`. The other 86 singleton blocks are also exactly
`T`-independent, so the complete selected 125-by-125 determinant is unchanged
by the transverse direction `(2,8)`.

## Certificate

The transverse core has ranks `rank(K_T)=7`, `rank(K_T^2)=3`, and
`K_T^3=0`. Exact rank factorizations reduce the calculation to a 7-by-7
transfer; the `C` update has rank six and is handled by a Woodbury solve.

Separate determinant degree bounds are `(25,24,6,7)` in `(A,B,C,T)`. The
worker checks the full `26*25*7` tensor grid at each of 30 distinct primes.
At all 136,500 controls the base is invertible and the transfer squares to
zero, making the determinant pencil one as a polynomial in `T`.

After clearing the common denominator `5241600`, a row-l1 determinant bound
places every difference coefficient below an explicit 885-bit bound. The
prime product has 897 bits and exceeds twice that bound. Tensor interpolation
modulo every prime followed by this CRT height comparison therefore proves
that every characteristic-zero coefficient is zero.

Accepted artifact SHA-256:
`B426FE41C7DC835DAF8E6079DE50644EA6D7CE661EF71A93E9D4951F0AA2ED9A`.

## Consequence and strict scope

This is stronger than graph-only inertness: the EXP-124 section is inert on
the complete normalized `(A,B,C)` ambient chart. Its old divisor
`N=F_3F_6F_7` is therefore retained unchanged after adjoining `(2,8)`.

It is one section, not a transverse atlas. The two EXP-129 residual sections,
the EXP-130 finite-base section, and the transverse `d=0` quotient still have
to be lifted. EXP-135 does not close the complete five-coefficient
restriction, the 24-parameter core, `(72,108)`, the degree floor, or JC(2).
