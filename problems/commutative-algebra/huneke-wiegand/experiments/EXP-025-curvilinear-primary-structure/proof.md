# EXP-025 - symbolic proof

Fix `p>=4`, put `q=24p`, and use the frozen EXP-021/023 notation

```text
C=C_p=P/J,
P=k[X_a : a in G],
X_a maps to the degree-one class with offset a,
G=E_1.
```

EXP-021 proves that `C` is a one-dimensional Cohen--Macaulay standard graded algebra, free of
rank `q` over `k[X_0]`. EXP-023 proves the value-congruence description: a degree-`n` monomial
maps to zero precisely when its total offset is absent from `E_n`, and two nonzero monomials have
the same class precisely when their offsets agree. Its cumulative bases are

```text
E_1=G,
E_2=[0,2p] union [3p,5p-2] union [6p,q-1],
E_3=[0,q-1] minus {6p-1},
E_n=[0,q-1] for n>=4.                                  (1)
```

The degree-one blocks also give `0,1 in G` and `max(G)=18p-1<q`.

## 1. Truncated monomial parametrization

Give every monomial `x y^a` standard degree one and form the graded subalgebra

```text
A=k[x y^a : a in G] inside k[x,y]/(y^q).
```

There is a graded surjection

```text
phi:P -> A,       X_a maps to x y^a.                    (2)
```

A degree-`n` monomial of `P` with total offset `b` maps under (2) to `x^n y^b`, which is zero
exactly for `b>=q`. Distinct surviving offsets give distinct monomials in the truncated polynomial
ring. On the other hand, EXP-023 says that the corresponding class in `C_n` is zero exactly when
`b` is absent from `E_n`, and otherwise depends only on `b`. The achieved surviving offsets are
therefore exactly `E_n` in both quotients. Degree by degree,

```text
ker(phi)_n=J_n.
```

Hence

```text
C isomorphic to k[x y^a : a in G] inside k[x,y]/(y^q). (3)
```

This proves P1. Formula (1) is the low-degree anatomy of (3), not a finite extrapolation.

## 2. Exact dehomogenization

For every positive `a in G`, compare the two degree-`a` monomials

```text
X_0^(a-1) X_a    and    X_1^a.
```

They have the same total offset `a<q`, so (3), or directly the EXP-023 congruence theorem, gives

```text
X_0^(a-1) X_a=X_1^a in C.                              (4)
```

After setting `X_0=1`, every generator becomes a power of `X_1`. Since `X_1^q=0`, Equation (4)
gives a surjection

```text
k[y]/(y^q) -> C/(X_0-1),       y maps to X_1.           (5)
```

EXP-021 gives a graded `k[X_0]`-module decomposition of `C` with total rank `q`. Tensoring it with
`k[X_0]/(X_0-1)` shows

```text
dim_k C/(X_0-1)=q.
```

The source of (5) also has dimension `q`, so (5) is an isomorphism. This proves P2.

## 3. Nilradical, sharp exponent, and primaryness

Let

```text
N=(X_a : a>0)C,          L=(X_a : a>0) in P.
```

The quotient `C/N` is `k[X_0]`, hence reduced. Every product of `q` generators of `N` has total
positive offset at least `q`, so (3) gives `N^q=0`. Thus `N` is exactly the nilradical and is the
unique minimal prime of `C`. Moreover,

```text
X_1^(q-1) maps to x^(q-1)y^(q-1),
```

which is nonzero. Therefore

```text
N^(q-1) != 0,       N^q=0,                              (6)
```

and the nilpotency index is sharply `q=24p`.

It remains important not to infer primaryness from the unique minimal prime alone. The
Cohen--Macaulay premise is load-bearing. A one-dimensional Cohen--Macaulay ring has no embedded
associated primes. Since `N` is the only minimal prime,

```text
Ass(C)={N}.
```

For a Noetherian ring, zero is primary exactly when its associated-prime set is the singleton
containing its radical. Hence zero is `N`-primary in `C`, and taking the inverse image in `P`
gives

```text
sqrt(J)=L,       J is L-primary.                        (7)
```

Equation (7) is the complete primary decomposition: it has one component. This proves P3 and P4.
The standard countercontrol `k[u,v]/(u^2,uv)` shows why uniqueness of the minimal prime without
the no-embedded-primes premise would not suffice.

## 4. Saturation and projective geometry

Let `P_+` be the irrelevant ideal. Since `C` is one-dimensional Cohen--Macaulay,

```text
H^0_(P_+)(C)=0.
```

The standard saturation identity `J^sat/J=H^0_(P_+)(C)` therefore gives `J^sat=J`. By (7), the
support of `Proj(C)` is the single coordinate point

```text
[1:0:...:0].
```

The chart `D_+(X_0)` contains the entire scheme. Its affine coordinate ring is the
dehomogenization in (5), namely `k[y]/(y^q)`. Consequently `Proj(C)` is a length-`q` curvilinear
fat point. Its maximal ideal is `(y)`, and

```text
dim_k (y)/(y^2)=1,
```

so the Zariski tangent space has dimension one. The Artinian local ring `k[y]/(y^q)` has socle
`k y^(q-1)` and is Gorenstein. Thus the projective scheme is locally Gorenstein.

EXP-021 proves, however, that the homogeneous coordinate ring `C` has Cohen--Macaulay type
`10p+1`, with socle in two degrees after regular reduction. Hence `C` is neither level nor
Gorenstein. This proves P5 and P6 and exhibits the strict distinction

```text
locally Gorenstein projective scheme != arithmetically Gorenstein embedding. (8)
```

## 5. Differential fingerprint and characteristic boundary

Put `B=C/(X_0-1)=k[y]/(y^q)`. The conormal sequence for `k[y] -> B` gives

```text
Omega^1_(B/k) isomorphic to B dy/(q y^(q-1)dy)
              isomorphic to (B/(q y^(q-1)))dy.          (9)
```

It follows that

```text
dim_k Omega^1_(B/k) = q-1,  if char(k) does not divide q,
dim_k Omega^1_(B/k) = q,    if char(k) divides q.       (10)
```

The module in (9) is cyclic, so every exterior power of degree at least two vanishes. Tensoring
with the residue field kills the relation coefficient and leaves the one-dimensional cotangent
space generated by `dy`, independently recovering the tangent dimension. This proves P7 without
silently imposing characteristic zero.

## 6. Role of computation and trust boundary

The campaign computes truncated sumsets from the degree-one blocks for every `p=4,...,300`, checks
the cumulative bases, disjoint layers, dehomogenization relations, sharp nilpotence, local versus
arithmetic type, characteristic split, and all declared corruptions. The audit does not import
the campaign: it starts from the disjoint EXP-021 layers, cumulatively rebuilds every row, rehashes
the campaign, and performs detailed selected-parameter reconstructions.

Those finite calculations validate the encodings and controls. Sections 1--5 prove the theorem
for every `p>=4` from the frozen EXP-021/023/024 premises. In particular, the EXP-023 exact
all-parameter value-congruence result retains its already disclosed solver/encoding boundary; the
present experiment does not create a separately checked proof object for that step.

