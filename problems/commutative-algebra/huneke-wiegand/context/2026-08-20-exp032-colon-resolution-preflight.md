# EXP-032 preflight - complete cubic-colon resolution

Date: 2026-08-20. Scope: HWB-035 and HWB-049.

## Question and claim boundary

Determine the complete ordinary graded minimal resolution of

```text
D_p=P_p/(Q_p:f_p)
```

for every integer `p>=4` and every field. EXP-030 identified this quotient as a canonical
idealization after killing `8p` linear variables, but extracted only the first two nonlinear
coefficients needed for `beta_(3,6)(C_p)`. A confirmation would determine the full colon-quotient
resolution. It would not determine the full resolution of `C_p`, because the unresolved
quadratic quotient `P_p/Q_p` remains in the cubic mapping cone.

## Invariant-first route

Put `c=2p-2` and `m=8p`. Over the polynomial ring in the `2p` low variables, EXP-030 gives

```text
E_p=V_p semidirect omega_(V_p),
H_(E_p)(z)=(1+cz+z^2)/(1-z)^2.
```

The ring is two-dimensional Gorenstein of codimension `c`, has no linear equations, and has
regularity two. Graded Gorenstein self-duality then permits only a linear strand and the final
socle shift. The Hilbert numerator predicts

```text
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1),  1<=a<=c-1,

B_(E_p)(x,z)=1+sum_a lambda_(c,a)x^a z^(a+1)+x^c z^(c+2).
```

The `m` killed variables form an independent Koszul factor, predicting

```text
B_(D_p)(x,z)=(1+xz)^m B_(E_p)(x,z).
```

This is a candidate complete resolution formula, not a result until the self-duality shifts,
Hilbert-numerator signs, positivity, endpoints, tensor factor, and independent checks pass.

## Frozen premises

| premise | SHA-256 | use |
|---|---|---|
| EXP-030 `proof.md` | `1822095a7d16207b7d04261b7a6645f7ca51b01f490ba9d212a84ab7ca5bc729` | canonical idealization, Gorenstein property, Hilbert series, and killed variables |
| EXP-030 `verdict.md` | `7f8d2fe3c61a0fc1f864452ca98d05d04e154496a2d45d2c8d8a7b32644de4d9` | confirmed scope and characteristic boundary |

Any mismatch stops the canonical run as `INCONCLUSIVE_PREMISE`.

## Required routes

1. Symbolic derivation: prove the low resolution shape from regularity, minimality, and Gorenstein
   self-duality, then extract the linear ranks coefficientwise from
   `(1+cz+z^2)(1-z)^c`.
2. Canonical campaign: verify positivity, self-duality, Hilbert reconstruction, projective
   dimension `10p-2`, regularity two, and the full Poincare polynomial for `p=4,...,300`.
3. Independent audit: reconstruct the coefficients from alternating Hilbert-numerator
   coefficients without importing the canonical rank formula, and convolve with the Koszul rows.
4. Adversarial controls: reject a wrong codimension, omitted top shift, wrong binomial sign, and a
   spurious second nonlinear strand.

## Manuscript decision

If confirmed, this is an adjacent strengthening of the canonical-idealization theorem and belongs
in the existing main manuscript as v0.19. A separate manuscript remains deferred because the
result is still a colon-quotient input, not the full presentation-ring resolution.
