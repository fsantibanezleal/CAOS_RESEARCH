# EXP-013 - exact trace and conductor ideal

Declared: 2026-08-12, before implementation or execution. Phase HW-P5. Backlog HWB-014.

## Prediction

For every integer `p>=4`, put `s=6p`, retain the EXP-009 blocks `A_p,B_p,C_p`, and define

```text
Q_p=[p+1,2p-2] union {2p,4p},
H_p={2p-1,4p-1} union [4p+1,5p-2].
```

For `R_p=k[[Gamma_p]]`, `J_p=(1,t^s)`, and `E_p=End_(R_p)(J_p)=k[[Lambda_p]]`, predict

```text
tr_(R_p)(J_p) = R_p:E_p = tr_(R_p)(E_p) = T_p,
```

where

```text
v(T_p) = (4s+A_p)
         union (5s+(A_p union B_p))
         union (6s+B_p)
         union (8s+C_p)
         union [9s,infinity).
```

Consequently `length_(R_p)(R_p/T_p)=p+1`. The equality is compatible with the
Lindo-Maitra-Zhang reflexive-trace criterion; the exact formula and colength are the new claims.

## Method

1. Prove the formula symbolically from the exact EXP-009 and EXP-011 blocks.
2. Route A reconstructs `R_p:J_p`, multiplies by `J_p`, reconstructs `R_p:E_p`, and multiplies by
   `E_p`, using independent finite value-set arithmetic beyond every conductor bound.
3. Route B independently evaluates the three membership predicates value by value and compares
   them with the predicted blocks.
4. Check every `p=4,...,300` exactly and record deterministic row and campaign hashes.
5. Reject a deleted level-five trace value, an injected reflected obstruction, and a false trace
   equality control in which the overring block is deliberately altered.

## What PASS and FAIL prove

- Finite agreement through `p=300` supports but does not prove the all-`p` theorem. The symbolic
  block proof is load-bearing.
- Any membership or colength mismatch refutes the displayed formula at that parameter.
- A complete symbolic proof plus successful independent and adversarial checks confirms the theorem
  for every `p>=4`.

## Compute budget and kill criterion

CPU only, exact integer/set arithmetic, no randomness. Smoke budget: 10 seconds for `p=4,5`.
Full budget: two minutes for `p=4,...,300`. Abort on the first semantic mismatch or at two minutes;
a budget hit is `INCONCLUSIVE`, never supporting evidence.

## Scope boundary

EXP-013 computes trace and conductor ideals only for the explicit family. It neither proves a new
counterexample nor classifies arbitrary one-dimensional Gorenstein rings, rigid modules, or nearby
Kunz faces.
