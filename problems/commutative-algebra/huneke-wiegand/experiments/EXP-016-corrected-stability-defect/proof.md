# EXP-016 symbolic proof

Fix `p>=4`, put `s=6p`, and write `D=[0,s-1]`, `D_minus=[0,s-2]`, and
`U=A union B`. EXP-013 gives the finite blocks of `v(T)` as

| level | residue set |
|---:|---|
| 4 | `A` |
| 5 | `U` |
| 6 | `B` |
| 8 | `C` |
| 9, 10, 11 | `D` |
| 12 | `D_minus` |

The tail begins at level 13.

## Residue identities

For residue sets `X,Y subset D`, let `L(X,Y)` contain the sums below `s`, and let `H(X,Y)`
contain the sums at least `s` after subtracting `s`. Decompose

```text
A=[0,p] union [3p,4p-2],
B=[p+1,2p-2] union [2p,3p-1] union {4p} union [5p-1,6p-1].
```

Using `[a,b]+[c,d]=[a+c,b+d]`, clipping at `s`, and translating the carry part by `-s`, direct
interval union gives the following identities. All endpoint orderings used here follow from
`p>=4`.

| product level | exact residue union |
|---:|---|
| 8 | `L(A,A)=C` |
| 9 | `H(A,A) union L(A,U)=D` |
| 10 | `H(A,U) union L(A,B) union L(U,U)=D` |
| 11 | `H(A,B) union H(U,U) union L(U,B)=D` |
| 12 | `H(U,B) union L(B,B) union L(A,C)=D_minus` |

These are equalities, not only coverage statements: the left sides list every pair of nonempty
`T` levels whose sum can land at the indicated level, including carries from the preceding level.
They prove

```text
v(T^2) intersect [8s,13s-1]
 = (8s+C) union [9s,13s-2].
```

In particular, `13s-1` is excluded. This is the endpoint missed by EXP-015.

## Tail

Since `4s in v(T)`, multiplication by `t^(4s)` shows

```text
[13s,17s-2] union [17s,infinity) subset v(T^2).
```

The only missing integer between those two intervals is filled by

```text
17s-1=(4s+1)+(13s-2),
```

and both summands lie in `v(T)`. Hence `[13s,infinity) subset v(T^2)`. No value below `8s`
can occur because the least value of `T` is `4s`. Combining this with the residue identities proves

```text
v(T^2)=(8s+C) union [9s,13s-2] union [13s,infinity).
```

## Exact quotient

Shifting the EXP-013 formula gives

```text
v(t^(4s)T)
 = (8s+A) union (9s+U) union (10s+B) union (12s+C)
   union [13s,17s-2] union [17s,infinity).
```

Subtracting this set from the square gives, level by level,

```text
C minus A = [p+1,2p] union [4p-1,5p-2],
D minus U = {2p-1,4p-1} union [4p+1,5p-2],
D minus B = [0,p] union {2p-1} union [3p,4p-1]
            union [4p+1,5p-2],
D minus empty = D,
D_minus minus C = [2p+1,3p-1] union [5p-1,s-2],
```

at levels 8, 9, 10, 11, and 12, plus the singleton `17s-1`. Their cardinalities are

```text
2p, p, 3p, 6p, 2p-1, 1.
```

Therefore

```text
length(T^2/t^(4s)T)=14p.
```

This also gives a direct stability obstruction. If `T^2=yT` for a regular `y in T`, comparison of
least valuations forces `v(y)=4s`, and then `v(yT)=4s+v(T)`. The displayed nonempty quotient makes
that impossible.
