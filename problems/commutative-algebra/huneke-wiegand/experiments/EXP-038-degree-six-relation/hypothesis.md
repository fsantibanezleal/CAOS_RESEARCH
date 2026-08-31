# EXP-038 hypothesis - a first degree-six relation in the parity defect

Date: 2026-08-30. CPU only. Exact arithmetic over declared prime fields.

## Question

For the `t=2` excess

```text
e_p=dim_GF(2) A_(p,2)-dim_GF(3) A_(p,2),
```

does the corrected generating function

```text
sum_(p>=4) e_p x^(p-4)
  =(1+2x+x^2+x^3-x^6)/((1-x)^2(1-x^2)(1-x^3))?             (P1)
```

More strongly, is the `-x^6` term induced by a first homogeneous relation of degree six among
the lattice-indexed candidate parity classes, with no earlier relation?                  `(P2)`

## Falsifiable predictions

P1 reproduces the seven exact values through `p=10` and predicts

```text
e_11=102,  e_12=138.
```

The old, refuted series predicted `104` and `142`. Thus `(11,2)` separates the hypotheses.

P2 requires an explicit integral or mod-two relation certificate, including its signed support
and proof that it is the first correction. A numerical value of 102 cannot establish P2.

## Method and controls

1. Freeze the complete EXP-037 proof, verdict, engine, target, and audit hashes.
2. Reconstruct the corrected coefficients by two routes: generating-series convolution and a
   shifted denominator lattice count.
3. Reuse only the frozen exact basis/reduction engine; do not alter EXP-037 evidence.
4. Compute the complete `(11,2)` target over `GF(2)` and `GF(3)` under the declared resource cap.
5. On a pass, audit with canonical residual order and `GF(5)` before pursuing P2.
6. On a mismatch, refute P1 immediately and redirect to structural core invariants rather than
   adding another unconstrained interpolation.

## Scope

P1 is a finite-data hypothesis until an all-parameter derivation exists. Even a proof of P1 would
describe one multigraded family in the lower strand, not the full Betti table and not the general
Huneke-Wiegand conjecture.
