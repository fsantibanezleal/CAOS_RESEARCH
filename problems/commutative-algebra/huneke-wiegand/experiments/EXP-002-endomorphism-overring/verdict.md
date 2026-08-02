# EXP-002 verdict - CONFIRMED

Run date: 2026-08-01. Phase HW-P2. Backlog HWB-002.

## Exact computation

For `J=(1,t^14)R`, let `V=Gamma union (14+Gamma)`. Both the direct bounded-membership
route and the independent Apéry/Dijkstra route return

```text
v(End_R(J)) = Lambda = Gamma union {101,107,181}.
F(Lambda)=125, conductor(Lambda)=126, genus(Lambda)=88.
```

All predeclared predictions P1-P6 pass. Lambda is additively closed and nonsymmetric. Its
pseudo-Frobenius set has 24 elements, so the localized numerical-semigroup ring
`E=End_R(I)` has Cohen-Macaulay type 24 and is not Gorenstein.

The exact minimal generating set of Lambda adds only 101 and 107 to the displayed minimal
generators of Gamma. The third new value 181 is not a new minimal generator: for example,
`181=80+101`. Thus the predeclared word "necessary" in P4 is interpreted set-theoretically
(all three values are required for the exact difference `Lambda minus Gamma`), not as a claim
that all three are irreducible generators.

## Theorem dependency map

Write `E=End_R(I)`. Here `R` is a one-dimensional Gorenstein local domain, `I` is a faithful
torsion-free two-generated positive-grade ideal, `Ext^1_R(I,I)=0` by EXP-001, and `E` is
commutative. The exact computation gives `E != R`.

Using Dey--Lyle, *Centers of Endomorphism Rings and Reflexivity*, arXiv:2510.02210v2:

| conclusion for the candidate | precise route |
|---|---|
| `Ext^1_E(I,I)=0` | Proposition 4.1(2): rigidity over `R` descends to the center; here `Z(E)=E` |
| `I` is not reflexive as an `E`-module | contrapositive of Theorem 4.4(1), since reflexivity would force `Z(E)=R` |
| `Ext^2_E(I,I) != 0` | contrapositive of Theorem 4.4(2), since its vanishing would force `Z(E)=R` |
| `Ext^1_E(I,E) != 0` | contrapositive of Theorem 4.2, since vanishing together with rigidity would make `I` principal |
| `Tor^R_1(I,E) != 0` | contrapositive of Theorem 4.3, since `I` is two-generated and vanishing would force `E=R` |

This identifies the escape mechanism: the rigid ideal remains rigid after passage to its
endomorphism overring, but it loses reflexivity there; the adjacent Ext/Tor obstructions are
forced to be nonzero. The computation explains why the sufficient criteria do not prove
principality without contradicting them.

## Controls and scope

- DP and Apéry membership routes agree exactly.
- Gamma alone is rejected because 101 stabilizes `V` but is absent from Gamma.
- The false gap 103 is rejected.
- All other 88 old Gamma gaps below the old conductor fail stabilization.

This is a structural analysis of Son Pham's public candidate. Discovery priority remains Son
Pham's. It is not a minimality theorem, an infinite family, or a peer-reviewed result. Publication
novelty remains gated on comparison with the candidate's authors and the literature.
