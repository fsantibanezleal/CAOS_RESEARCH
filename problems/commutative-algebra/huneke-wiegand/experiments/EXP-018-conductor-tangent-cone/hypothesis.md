# EXP-018 - conductor tangent cone and Valabrega--Valla defect

Status: DECLARED before formal implementation or execution on 2026-08-12.

## Objects

For every integer `p>=4`, retain `s=6p`, the one-dimensional Gorenstein semigroup ring `R_p`, its
conductor ideal `T_p`, and the minimal reduction

```text
Q_p=t^(4s)R_p
```

from EXP-013--017. Put `G_p=gr_(T_p)(R_p)`.

## Falsifiable hypothesis

Let

```text
V_(p,n)=(Q_p intersect T_p^(n+1))/(Q_pT_p^n).
```

The complete Valabrega--Valla defect is predicted to be

```text
v(V_(p,0)) = empty,
v(V_(p,1)) = 9s+({2p-1,4p-1} union [4p+1,5p-2]),
v(V_(p,n)) = empty for every n>=2.
```

Thus `length(V_(p,1))=p`. The initial form of `t^(4s)` is a zero divisor on `G_p`, so the
one-dimensional tangent cone has depth zero and is not Cohen--Macaulay for every `p>=4`.

The exact graded Hilbert function and series are predicted to be

```text
h_0=p+1,
h_1=10p,
h_2=22p,
h_3=24p-1,
h_n=24p for n>=4,

H_(G_p)(z)
  = ((p+1)+(9p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

In particular every numerator coefficient is positive despite `depth(G_p)=0`.

## Required proof and evidence

1. Derive the exact intersection at `n=1` by intersecting the EXP-016 square with
   `v(Q_p)=4s+Gamma_p`, not merely by subtracting `Q_pT_p` from `T_p^2`.
2. Prove the intersections vanish at `n=0,2,3`; use EXP-017 stabilization to prove vanishing for
   every `n>=4`.
3. Apply the Valabrega--Valla criterion with its hypotheses stated explicitly to conclude
   `depth(G_p)=0` and non-Cohen--Macaulayness.
4. Derive the Hilbert function and rational series from exact finite-colength identities.
5. Run two exact implementations for every `p=4,...,300`, with a `p=4` smoke gate before the
   campaign artifact is created.
6. Run an independently written audit at `p=4,5,17,73,151,300` and rehash every campaign row.

## Adversarial controls

- delete `9s+(2p-1)` from the predicted defect;
- inject a false defect into degree two;
- replace the defect length `p` by `p-1`;
- force the false Cohen--Macaulay verdict;
- perturb one coefficient of the Hilbert numerator while preserving its value at `z=0`.

Every corruption must be rejected.

## Budget and verdict rule

- CPU only; exact integer/bitset arithmetic; no randomness;
- two minutes for the full campaign and one minute for the independent audit;
- `CONFIRMED` requires the symbolic proof, both complete exact routes, all controls, stable hashes,
  and the independent audit;
- a `p=4` mismatch preserves this declaration as `REFUTED` or triggers a separately numbered
  corrected hypothesis before any broad campaign.
