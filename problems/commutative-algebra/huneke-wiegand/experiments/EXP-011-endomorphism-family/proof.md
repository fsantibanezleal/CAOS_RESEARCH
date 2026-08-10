# EXP-011 parametric endomorphism-overring proof

## Theorem

For every integer `p>=4`, put `s=6p` and let `Gamma_p`, `R_p`, and
`J_p=(1,t^s)R_p` be the EXP-009 family. Define

```text
Q_p = [p+1,2p-2] union {2p,4p}.
```

Then the value semigroup of `E_p=End_(R_p)(J_p)` is

```text
Lambda_p = Gamma_p union (7s+Q_p) union {13s-1}.
```

It has

```text
multiplicity       = 4s  = 24p,
Frobenius number   = 9s-1 = 54p-1,
conductor          = 9s  = 54p,
genus              = 38p-1,
embedding dimension = 12p.
```

In particular `Lambda_p` is nonsymmetric, so the localized semigroup ring `E_p` is not
Gorenstein. Moreover, the EXP-002 endomorphism escape is uniform across the family:

```text
Ext^1_(E_p)(J_p,J_p) = 0,
J_p is not reflexive as an E_p-module,
Ext^1_(E_p)(J_p,E_p) != 0,
Ext^2_(E_p)(J_p,J_p) != 0,
Tor^R_p_1(J_p,E_p) != 0.
```

## 1. Adjacent value-set blocks

Let `G_k` be the residue set of `Gamma_p` at level `ks`. EXP-009 gives

```text
G_0={0}, G_1=G_2=G_3=empty,
G_4=A, G_5=[0,s-1], G_6=B, G_7=empty, G_8=C,
G_9=G_10=G_11=[0,s-1], G_12=[0,s-2],
G_k=[0,s-1] for k>=13.
```

The value set of `J_p` is `V_p=Gamma_p union (s+Gamma_p)`. Its level-`k` residue set is therefore
`V_k=G_k union G_(k-1)`, where `G_(-1)` is empty. Hence

```text
V_0={0}, V_1={0}, V_2=V_3=empty,
V_4=A, V_5=V_6=[0,s-1], V_7=B, V_8=C,
V_k=[0,s-1] for k>=9.
```

An exponent `n=ks+r` belongs to `Lambda_p` exactly when multiplication by `t^n` preserves both
generators of `J_p`. Equivalently, `n` and `n+s` both belong to `V_p`. Thus the level-`k` residue
set of `Lambda_p` is

```text
L_k = V_k intersect V_(k+1).
```

All intersections reproduce the corresponding `Gamma_p` block except level 7 and the terminal
gap. At level 7,

```text
B intersect C
  = ([p+1,2p] minus {2p-1}) union {4p}
  = [p+1,2p-2] union {2p,4p}
  = Q_p.
```

Every level from 9 onward is full. Relative to `Gamma_p`, this fills `7s+Q_p` and the single old
Frobenius value `13s-1`, proving the displayed formula.

## 2. Numerical invariants

The first positive value remains `4s`, so the multiplicity is `4s=24p`. The level-8 block is
`C=[0,2p] union [3p,5p-2]`, which omits residue `s-1=6p-1`. Level 9 and every later level are
full. Therefore the largest gap is `9s-1=54p-1` and the conductor is `9s=54p`.

The gaps are counted by levels:

```text
below level 4: 4s-1 = 24p-1,
level 4:       s-|A| = 4p,
level 5:       0,
level 6:       s-|B| = 3p,
level 7:       s-|Q_p| = 5p,
level 8:       s-|C| = 2p.
```

Here `|A|=2p`, `|B|=3p`, `|Q_p|=p`, and `|C|=4p`. The total genus is consequently
`38p-1`. A symmetric numerical semigroup with Frobenius `54p-1` would have genus `27p`; the
difference is `11p-1>0`. Thus `Lambda_p` is nonsymmetric for every `p>=4`.

## 3. Minimal generators

EXP-009 proves that `Gamma_p` has exactly `11p` minimal generators in levels 4, 5, and 6. Every
new value `7s+q`, with `q` in `Q_p`, lies below twice the multiplicity `8s`, so it cannot be a sum
of two positive elements. These `p` values are therefore new minimal generators.

The remaining extra value is not minimal. For any `q` in `Q_p`, the level-5 block contains
`5s+(s-1-q)`, and

```text
(7s+q) + (5s+(s-1-q)) = 13s-1.
```

The old generators generate all of `Gamma_p`, and the displayed equality generates the only
other added value. Hence there are no further minimal generators, and the embedding dimension is
`11p+p=12p`.

## 4. Uniform endomorphism escape

By EXP-009, `R_p` is a one-dimensional Gorenstein local domain and `J_p` is faithful,
torsion-free, two-generated, nonprincipal, and rigid. The ring `E_p=End_(R_p)(J_p)` is commutative,
and the nonempty set `7s+Q_p` proves `E_p` is strictly larger than `R_p`.

The current primary source, Dey-Lyle arXiv:2510.02210v2, then applies exactly as in EXP-002:

1. Proposition 4.1(2) makes rigidity descend to the center, which here is `E_p`.
2. The contrapositive of Theorem 4.4(1) shows that `J_p` is not reflexive over `E_p`, since
   reflexivity would force `E_p=R_p`.
3. The contrapositive of Theorem 4.4(2) forces `Ext^2_(E_p)(J_p,J_p)` to be nonzero.
4. The contrapositive of Theorem 4.2 forces `Ext^1_(E_p)(J_p,E_p)` to be nonzero because `J_p` is
   nonprincipal.
5. The contrapositive of Theorem 4.3 forces `Tor^R_p_1(J_p,E_p)` to be nonzero because `J_p` is
   two-generated and `E_p` is strictly larger than `R_p`.

This proves the uniform statements.

## 5. Computational support

The proof is independent of the finite campaign. The exact implementation checked all
`p=4,...,300` by two routes: direct adjacent-block intersection and additive generation from the
predicted minimal generators. A separate implementation rehashed all 297 rows and reconstructed
the semantic value sets at `p=4,5,17,73,151,300`. Deleting a required `Q_p` member and omitting the
terminal singleton were both rejected.
