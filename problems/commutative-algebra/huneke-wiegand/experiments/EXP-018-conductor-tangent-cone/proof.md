# EXP-018 - symbolic proof

Fix `p>=4`, put `s=6p`, and write `D=[0,s-1]`, `D^-=[0,s-2]`, and

```text
H={2p-1,4p-1} union [4p+1,5p-2].
```

Retain the residue blocks `A,B,C` and put `U=A union B`. Directly from their definitions,

```text
D minus U = H,  |H|=p.
```

Let `x=t^(4s)`, `Q=xR`, `T=T_p`, and `G=gr_T(R)`.

## 1. The unique nonzero intersection defect

The EXP-013 ring and conductor profiles give

```text
v(Q)
 = {4s} union (8s+A) union (9s+D) union (10s+B) union (12s+C)
   union [13s,17s-2] union [17s,infinity),

v(xT)
 = (8s+A) union (9s+U) union (10s+B) union (12s+C)
   union [13s,17s-2] union [17s,infinity).
```

EXP-016 proves

```text
v(T^2)=(8s+C) union [9s,13s-2] union [13s,infinity).
```

Here `A subset C` and `C subset D^-`. Intersecting the displayed `Q` and `T^2` profiles therefore
gives

```text
v(Q intersect T^2)
 = (8s+A) union (9s+D) union (10s+B) union (12s+C)
   union [13s,infinity).
```

Comparison with `v(xT)` shows that the only difference is at level nine:

```text
v((Q intersect T^2)/(xT)) = 9s+(D minus U) = 9s+H.
```

Thus this quotient has length `|H|=p`. Equivalently, division by the nonzerodivisor `x` identifies
these classes with the kernel of multiplication by the initial form `x*` from degree zero to
degree one of `G`. Explicitly, the nonzero kernel classes are

```text
t^(5s+h)+T,  h in H.
```

## 2. Vanishing in every other degree

First, `Q subset T`, so `Q intersect T=Q=xR` and the degree-zero Valabrega--Valla quotient
vanishes.

EXP-017 gives

```text
v(T^3)=[12s,13s-2] union [13s,infinity),
v(T^4)=[16s,infinity),
v(T^5)=[20s,infinity).
```

The corresponding intersections and shifts are

```text
v(Q intersect T^3) = (12s+C) union [13s,infinity) = v(xT^2),
v(Q intersect T^4) = [16s,infinity) = v(xT^3),
v(Q intersect T^5) = [20s,infinity) = v(xT^4).
```

Finally EXP-017 proves `T^(n+1)=xT^n` for every `n>=4`. Since `xT^n subset xR=Q`, this equality
immediately implies

```text
Q intersect T^(n+1)=T^(n+1)=xT^n
```

for every such `n`. Hence the complete Valabrega--Valla module is concentrated at `n=1`, where
its length is `p`.

## 3. Depth of the tangent cone

The ring `R` is a one-dimensional Cohen--Macaulay local domain, `x` is regular, the residue field
is infinite, and `Q=(x)` is the minimal reduction of `T` from EXP-017. Thus `x` is a superficial
reduction element. The Valabrega--Valla criterion applies: the one-dimensional associated graded
ring `G` is Cohen--Macaulay exactly when

```text
Q intersect T^(n+1)=xT^n
```

for every `n>=0`. The length-`p` failure at `n=1` proves that `G` is not Cohen--Macaulay. Since
`dim(G)=1`, it follows that

```text
depth(G)=0.
```

This use of the criterion follows P. Valabrega and G. Valla, *Form rings and regular sequences*,
Nagoya Mathematical Journal 72 (1978), 93--101,
`https://doi.org/10.1017/S0027763000018225`.

## 4. Exact Hilbert series

Write

```text
a_n=length(T^(n+1)/xT^n).
```

EXP-017 proves

```text
(a_0,a_1,a_2,a_3,a_4,...)=(23p-1,14p,2p,1,0,...)
```

and `length(R/xR)=24p`. Since every `T^n` is a maximal Cohen--Macaulay rank-one module, its
quotient by the regular parameter `x` has length `24p`. The exact sequence

```text
0 -> T^(n+1)/xT^n -> T^n/xT^n -> T^n/T^(n+1) -> 0
```

therefore gives

```text
h_n=length(T^n/T^(n+1))=24p-a_n.
```

Consequently

```text
h_0=p+1,
h_1=10p,
h_2=22p,
h_3=24p-1,
h_n=24p for n>=4.
```

Multiplying `sum_(n>=0) h_n z^n` by `1-z` yields

```text
H_G(z)=((p+1)+(9p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

Every coefficient of the numerator is positive for `p>=4`, while `depth(G)=0`. Thus numerator
positivity does not detect this isolated intersection obstruction.

The proof uses the exact value blocks and the Valabrega--Valla criterion. The finite campaign is
supporting implementation evidence, not the infinite-family proof.
