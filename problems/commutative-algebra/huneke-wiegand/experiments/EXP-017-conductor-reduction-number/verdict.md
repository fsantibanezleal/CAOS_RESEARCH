# EXP-017 verdict - CONFIRMED

Date: 2026-08-12.

The declared hypothesis is confirmed for every integer `p>=4`.

## Theorem-level result

For `Q_p=t^(4s)R_p`, the conductor has exact reduction number four:

```text
T_p^5=Q_pT_p^4,
T_p^(n+1)=Q_pT_p^n for all n>=4,
```

and none of the preceding three reduction equalities holds. The complete quotient-length profile
is

```text
length(T_p/Q_p)                 = 23p-1,
length(T_p^2/Q_pT_p)            = 14p,
length(T_p^3/Q_pT_p^2)          = 2p,
length(T_p^4/Q_pT_p^3)          = 1,
length(T_p^(n+1)/Q_pT_p^n)      = 0 for n>=4.
```

The exact power formulas are

```text
v(T_p^3)=[12s,13s-2] union [13s,infinity),
v(T_p^4)=[16s,infinity),
v(T_p^5)=[20s,infinity).
```

Consequently the Hilbert-Samuel function is `length(R_p/T_p^n)=24pn-39p` for every `n>=4`, with
`e_0(T_p)=24p` and `e_1(T_p)=39p`.

## Evidence

- The symbolic block proof is `proof.md` and is load-bearing.
- The `p=4` smoke gate passed before the full campaign artifact was written.
- Two exact representations in `run.py` agree with every predicted set and length for all 297
  parameters `p=4,...,300`.
- Campaign aggregate:
  `e9c3c887648f08cf67c614b381f00c8c6520dcd1bb89f8cdece62293bfd06030`.
- An independently written tail-set auditor rehashes all campaign rows and reconstructs
  `p=4,5,17,73,151,300`.
- Audit aggregate:
  `0f6ed70676ffb8972b8b167ad52c4f9d2851f69c3b1d96f4023e5e3d5825c781`.
- `results.json` SHA-256:
  `52bcdedce9039f72af705453917856354d48a77303dffeb237737111f57c7c7e`.
- `audit.json` SHA-256:
  `4a6ae8125bf00c965501792ec39d7375cb3f803023d13f34c17430427d1bb1a5`.
- Deleted-terminal, false-stabilization, altered-interval, and perturbed-length controls are
  rejected.

## Boundary

This is an exact theorem for the explicit conductor family `T_p`. It does not claim reduction
number four for arbitrary conductors, trace ideals, finite birational extensions, or Gorenstein
numerical semigroup rings. The Hilbert data are derived from the block proof, not inferred from a
finite sweep.

