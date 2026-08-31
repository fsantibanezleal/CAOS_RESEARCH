# EXP-043 preflight - Hadamard modular certificate for rational rank

Date: 2026-08-31. Exact finite certificate design; no matrix rank is evaluated before declaration.

## Target

EXP-042 proves that the first Bockstein of the isolated signed matrices has ranks `3,4,5,7`.
This counts elementary divisors of 2-adic valuation exactly one, but the complete 2-primary torsion
also requires the rational rank. The available equal `GF(3)` and `GF(5)` ranks are lower bounds for
`rank_Q`, not upper bounds.

## Determinant certificate

Let `M` have generic-rank candidate `r`, and let `d` be its maximum column degree. Every
`(r+1) x (r+1)` minor has absolute value at most

```text
d^((r+1)/2)
```

by Hadamard's inequality applied to its columns. If distinct primes `q_i` all give
`rank_GF(q_i)(M)<=r`, every such minor is divisible by `Q=product(q_i)`. The exact integer test

```text
Q^2 > 4*d^(r+1)
```

then forces every `(r+1)` minor to vanish. Since a rank-`r` minor is already nonzero modulo three,
this proves `rank_Q(M)=r`.

The certificate uses verified distinct primes below `2^64`, an exact prime product, and no floating
point comparison. Deterministic Miller--Rabin bases valid in the 64-bit range verify primality.

## Predicted conclusion

For `p=8,9,10,11`, every certificate prime is predicted to give the frozen `GF(3)` rank
`1002,1607,2450,3586`, respectively. A pass proves these are the rational ranks. Then

```text
rank_Q(M_p)-rank_GF(2)(M_p) = 3,4,5,7.
```

EXP-042's Bockstein has exactly the same rank, so every even nonzero Smith factor has valuation one
and the isolated cokernel's complete 2-primary torsion is

```text
(Z/2)^3, (Z/2)^4, (Z/2)^5, (Z/2)^7
```

at the four tested parameters.

## Boundary

This is a complete finite 2-primary statement if it passes. It is not a formula for all `p`, a
transition map, a recurrence proof, or the full lower strand. A manuscript or Zenodo update remains
closed unless the finite normal forms are upgraded to a uniform theorem or another independently
transferable result.
