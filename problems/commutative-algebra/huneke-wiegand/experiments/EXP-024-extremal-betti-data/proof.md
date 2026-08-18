# EXP-024 - symbolic proof of the homological edge theorem

## Statement

Fix `p>=4`. Let `C_p=F(T_p)` be the conductor special fiber in the EXP-009 family and let

```text
P_p=k[X_a : a in E_(p,1)],
N=10p,
c=N-1=10p-1,
C_p=P_p/J_p.
```

Then the minimal graded `P_p`-resolution of `C_p` has:

```text
pd_(P_p)(C_p)=c,
reg_(P_p)(C_p)=4,
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(c,c+2)=10p,
beta_(c,c+4)=1,
beta_(c,j)=0 for j not in {c+2,c+4},
beta_(c-1,c+3)=8p.
```

Its alternating Betti polynomial is

```text
sum_(i,j) (-1)^i beta_(i,j) z^j
=(1-z)^c(1+(10p-1)z+12pz^2+(2p-1)z^3+z^4).
```

The canonical module has `10p` minimal generators in degree `-1` and one in degree `-3`.

This determines exact edges of the resolution, not its unresolved interior.

## 1. Confirmed premises

EXP-021 proves that `C_p` is a one-dimensional Cohen--Macaulay standard graded algebra and that
the image `x_p` of `X_0` is a regular linear parameter. Its Artinian reduction

```text
B_p=C_p/x_pC_p
```

has Hilbert vector

```text
h_p=(1,10p-1,12p,2p-1,1)
```

and socle vector `(0,0,10p,0,1)`. Equivalently,

```text
Hilb_(C_p)(z)=h_p(z)/(1-z).
```

EXP-023 proves the complete minimal first Betti row

```text
beta_(1,2)=50p^2-17p,
beta_(1,3)=1,
beta_(1,j)=0 for j>=4.
```

There are no linear equations. The experiment freezes and verifies the hashes of the EXP-021 and
EXP-023 campaign, audit, proof, and symbolic-certificate files before importing these premises.

## 2. Projective dimension and regularity

The polynomial ring `P_p` has depth `N`, while Cohen--Macaulayness and dimension one give
`depth_(P_p)(C_p)=1`. Hilbert's syzygy theorem gives finite projective dimension, so the
Auslander--Buchsbaum formula yields

```text
pd_(P_p)(C_p)=N-1=c.
```

For a Cohen--Macaulay standard graded algebra, regularity is the degree of its h-polynomial. Here
`deg h_p=4`, hence

```text
reg_(P_p)(C_p)=4.
```

This is also consistent with the exact EXP-021 decomposition over the one-variable Noether
normalization. Thus the v0.12 phrase asking for regularity over the full presentation ring was
stale: regularity four was already forced.

## 3. Alternating Betti polynomial

Let the minimal resolution have modules

```text
F_i = direct_sum_j P_p(-j)^(beta_(i,j)).
```

Taking Hilbert series in the resolution gives

```text
Hilb_(C_p)(z)
= [sum_(i,j)(-1)^i beta_(i,j)z^j]/(1-z)^N.
```

Since `Hilb_(C_p)(z)=h_p(z)/(1-z)` and `c=N-1`, multiplication by `(1-z)^N` proves

```text
sum_(i,j)(-1)^i beta_(i,j)z^j=(1-z)^c h_p(z).
```

The identity is an alternating constraint. It does not by itself separate consecutive Betti
contributions in the interior of the table.

## 4. Exact linear first syzygies

Because `J_p` has no linear equation, minimality forces every `i`th syzygy shift to be at least
`i+1`. Consequently only `beta_(1,3)` and `beta_(2,3)` contribute to the coefficient of `z^3`.
Writing `[z^3]` for coefficient extraction,

```text
beta_(2,3)-beta_(1,3)=[z^3](1-z)^c h_p(z).
```

Direct expansion gives

```text
[z^3](1-z)^c h_p(z)
=-binom(c,3)+c binom(c,2)-12pc+(2p-1).
```

Using `c=10p-1` and `beta_(1,3)=1` therefore yields

```text
beta_(2,3)=2p(500p^2-330p+31)/3.
```

The expression is integral for every integer `p`: modulo three,
`p(500p^2-330p+31)` is `p(2p^2+1)`, which vanishes for all three residue classes. The displayed
leading factor supplies the factor two.

There is an independent dimension derivation. In degree three, the map from the degree-three part
of the first free module onto `(J_p)_3` has domain dimension

```text
N beta_(1,2)+beta_(1,3).
```

Its kernel is the degree-three part of the second free module and has dimension `beta_(2,3)`.
Moreover,

```text
dim_k(P_p)_3=binom(N+2,3),
dim_k(C_p)_3=1+(10p-1)+12p+(2p-1)=24p-1.
```

Thus

```text
beta_(2,3)
=N(50p^2-17p)+1-[binom(N+2,3)-(24p-1)],
```

which simplifies to the same closed formula. This second route uses the complete EXP-023 first
Betti row rather than coefficient isolation.

## 5. The complete last row from the Artinian socle

Set `Q_p=P_p/(X_0)`, a polynomial ring in `c` variables. Since `X_0` is regular on both `P_p` and
`C_p`, tensoring the minimal `P_p`-resolution of `C_p` with `Q_p` is exact: the only possible
nonzero change-of-rings obstruction is

```text
Tor_1^(P_p)(C_p,Q_p)=(0:_(C_p) X_0)=0.
```

All differential entries remain in the homogeneous maximal ideal after reduction, so the reduced
resolution is minimal. Hence

```text
beta_(i,j)^(P_p)(C_p)=beta_(i,j)^(Q_p)(B_p).
```

The top Koszul complex of the `c` variables of `Q_p` identifies

```text
Tor_c^(Q_p)(B_p,k)_j = Soc(B_p)_(j-c).
```

The EXP-021 socle has dimension `10p` in degree two, dimension one in degree four, and zero in all
other degrees. Therefore the entire last row is exactly

```text
beta_(c,c+2)=10p,
beta_(c,c+4)=1,
beta_(c,j)=0 otherwise.
```

In particular, its total rank `10p+1` recovers the already proved Cohen--Macaulay type.

## 6. A penultimate extremal entry

Consider internal degree `c+3`. Since regularity is four, `beta_(i,c+3)=0` for `i<=c-2`.
The last-row calculation also gives `beta_(c,c+3)=0`, because the Artinian socle has no degree-
three part. The coefficient of `z^(c+3)` in the alternating Betti polynomial therefore has only
one contribution:

```text
[z^(c+3)](1-z)^c h_p(z)=(-1)^(c-1) beta_(c-1,c+3).
```

Only the degree-three and degree-four terms of `h_p` enter that coefficient, so

```text
[z^(c+3)](1-z)^c h_p(z)
=(-1)^c(2p-1)+(-1)^(c-1)c
=(-1)^(c-1)8p.
```

It follows that

```text
beta_(c-1,c+3)=8p.
```

## 7. Canonical-module generator degrees

Graded local duality presents the canonical module as

```text
omega_(C_p)=Ext^c_(P_p)(C_p,P_p(-N)).
```

Dualizing the minimal resolution, minimality places the image from the preceding dual module
inside the homogeneous maximal ideal times the last dual module. Thus its minimal generators are
read directly from the last free module. A last summand `P_p(-j)` contributes a canonical-module
generator of degree `N-j` because

```text
Hom_(P_p)(P_p(-j),P_p(-N))=P_p(j-N).
```

Since `c=N-1`, the `10p` summands with `j=c+2=N+1` give degree `-1`, and the one summand with
`j=c+4=N+3` gives degree `-3`. Hence

```text
mu_(degree -1)(omega_(C_p))=10p,
mu_(degree -3)(omega_(C_p))=1.
```

## 8. Computational audit and scope

The `p=4` smoke obtains `beta_(2,3)=17896`, last entries `(39,41,40)` and `(39,43,1)`, and
penultimate entry `(38,42,32)` by both encodings. The exact campaign passes all 297 parameters
`p=4,...,300`. A separate coefficient/dimension implementation rebuilds every row, reconstructs
the six selected EXP-021 socle cases, checks all twenty persisted EXP-023 first rows, and rejects
seven adversarial corruptions.

These computations audit algebra and premise transfer. The all-parameter theorem is carried by
Sections 2--7. The proof does not determine the remaining interior Betti numbers, produce a
Groebner basis, or remove the disclosed EXP-023 symbolic-certificate trust boundary.

## Sources checked

- Teresa Cortadellas and Santiago Zarzuela, *On the structure of the fiber cone of ideals with
  analytic spread one*, arXiv:math/0603042.
- Shiro Abdolmaleki and Shinya Kumashiro, *Defining ideals of the fiber cone with almost minimal
  multiplicity*, arXiv:2405.18041; International Journal of Algebra and Computation 34(7) (2024),
  DOI `10.1142/S0218196724500437`.
