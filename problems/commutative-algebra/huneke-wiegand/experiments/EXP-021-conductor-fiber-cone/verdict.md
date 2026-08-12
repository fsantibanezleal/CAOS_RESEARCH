# EXP-021 - verdict

Status: **CONFIRMED** on 2026-08-12.

## Theorem

For every integer `p>=4`, the conductor ideal `T_p` satisfies

```text
T_p^2=m_pT_p,
T_p^(n+1)=m_pT_p^n for every n>=1.
```

Consequently the natural tangent-cone map induces a graded-algebra isomorphism

```text
gr_(T_p)(R_p)/H^0 isomorphic to F(T_p).
```

The special fiber is a one-dimensional Cohen--Macaulay algebra and, over
`F_p=k[x_p]`, has decomposition

```text
F(T_p) isomorphic to F_p direct-sum F_p(-1)^(10p-1) direct-sum F_p(-2)^(12p)
  direct-sum F_p(-3)^(2p-1) direct-sum F_p(-4).
```

It has multiplicity `24p`, reduction number and regularity four, `a=3`, and Hilbert function

```text
1,10p,22p,24p-1,24p,24p,... .
```

Its Artinian reduction has h-vector `(1,10p-1,12p,2p-1,1)` and socle vector
`(0,0,10p,0,1)`. Hence the Cohen--Macaulay type is `10p+1`; the fiber cone is neither level nor
Gorenstein.

## Exact evidence

- The first formal campaign attempt passed through `p=225` but exceeded the declared 120-second
  budget. It is preserved as `INCONCLUSIVE`, not a mathematical failure.
- After an exact bitset optimization, the mandatory `p=4` smoke gate passed.
- Complete two-route campaign: `p=4,...,300`, 297 rows, PASS in 44.048252 seconds.
- Campaign aggregate:
  `3857877586143a3be5f14852feb12bd9efbfdf7c1cde458f30e8cd689155a95b`.
- Independent reconstructions: `p=4,5,17,73,151,300`, PASS in 14.324414 seconds.
- All 297 campaign rows independently rehashed.
- Independent audit aggregate:
  `1779407050b199039d3f6d808a720ea051a81ef11734fd1bccd1a76ec78c0a9c`.
- `results.json` SHA-256:
  `1fa45248cd8160af6539a26069e21d74023c39ebd18bff796660532766429e7c`.
- `audit.json` SHA-256:
  `d479ffa6be2db2a1e2b465603b65e53fe6e4135fe025e37f45d97abbfe5a2571`.
- `ruff` and Python byte-compilation checks: PASS.

## Adversarial controls

The campaign rejects a deleted value in `m_pT_p`, an injected positive-degree kernel, the false
count `mu(T_p^2)=22p-1`, deletion of a degree-two socle class, a false degree-three socle class,
and the Gorenstein/type-one mutation.

## How could this be wrong?

The infinite theorem depends on the already confirmed value-block and tangent-cone results in
EXP-009, EXP-013, and EXP-016--020. A symbolic error in one of those premises could propagate
despite finite agreement. The natural quotient statement also uses the full EXP-019 identification
`m_p/T_p=H^0`, not only equality of Hilbert series. The finite campaign validates two exact
implementations but does not replace the proof.

## Scope and next path

This theorem concerns the conductor ideals of the explicit EXP-009 family. It does not assert
that arbitrary conductor fiber cones, analytic-spread-one ideals, or Huneke--Wiegand
counterexamples have these properties. It is a material algebra theorem beyond v0.10 and triggers
the manuscript v0.11 gate. A defining-ideal calculation is now a justified separate research path,
not part of this verdict.
