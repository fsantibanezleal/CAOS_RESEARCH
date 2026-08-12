# EXP-013 exact trace and conductor proof

Fix `p>=4`, put `s=6p`, write `R=k[[Gamma]]`, and normalize the ideal as
`J=(1,t^s)`. Let `E=End_R(J)=k[[Lambda]]`. EXP-009 and EXP-011 give all value blocks used below.

## 1. The trace of J

Since `1` belongs to `J`,

```text
v(R:J)=W={n in Gamma : n+s in Gamma}.
```

Intersecting adjacent `Gamma` blocks gives

```text
W_4=A, W_5=B, W_6=W_7=empty, W_8=C,
W_9=W_10=[0,s-1], W_11=W_12=[0,s-2],
W_k=[0,s-1] for k>=13.
```

The set `W` is a `Gamma`-ideal. Since `v(J)=Gamma union (s+Gamma)`, multiplication therefore gives

```text
v(tr_R(J))=v(J(R:J))=W union (s+W).
```

Taking the union of adjacent displayed blocks yields

```text
T = (4s+A)
    union (5s+(A union B))
    union (6s+B)
    union (8s+C)
    union [9s,13s-2]
    union [13s,infinity).
```

The missing value `13s-1` is essential: it is the Frobenius gap of `Gamma`, so it cannot belong to
an `R`-ideal. This is the value that refuted the original smoke shorthand `[9s,infinity)`.

## 2. The conductor R:E

EXP-011 proves

```text
Lambda = Gamma union (7s+Q) union {13s-1},
Q=[p+1,2p-2] union {2p,4p}.
```

For `n in Gamma`, all translates by `Gamma` stay in `Gamma`; only the displayed new values need
checking. The translate `n+13s-1` lies in the conductor tail whenever `n>0`, while `n=0` fails.

If `n=4s+a` with `a in A`, then `n+7s+q=11s+a+q`. A carry can enter level 12, whose only missing
residue is `s-1`; failure would require `a+q=2s-1`. But
`a+q<=8p-2<12p-1=2s-1`, so every level-four value passes.

If `n=5s+r`, then `n+7s+q=12s+r+q`. It fails exactly when `r+q=s-1` for some `q in Q`. Thus the
excluded residues are the reflection

```text
H=(s-1)-Q={2p-1,4p-1} union [4p+1,5p-2].
```

Direct union of the EXP-009 blocks gives `[0,s-1] without H=A union B`. Finally, every positive
`Gamma` value at level at least six sends `7s+Q` and `13s-1` into the conductor tail. Consequently

```text
v(R:E)=T.
```

## 3. The trace of E and the balanced defect

The conductor `R:E` is an `E`-ideal and `1` belongs to `E`. Therefore

```text
tr_R(E)=E(R:E)=R:E=T=tr_R(J).
```

Relative to `Gamma`, `T` omits exactly

```text
{0} union (5s+H).
```

Since `|Q|=|H|=p`,

```text
length_R(R/T)=p+1.
```

EXP-011 also gives `Lambda minus Gamma=(7s+Q) union {13s-1}`, so

```text
length_R(E/R)=p+1=length_R(R/(R:E)).
```

This balanced conductor defect is a structural consequence of the explicit family, not merely a
finite observation.

## 4. Scope of the computation

The exact campaign and independent audit verify the block arithmetic and reject corruptions, but
the all-`p` result rests on the argument above. The proof concerns the explicit monomial family; it
does not classify trace ideals for arbitrary rigid modules or settle the remaining positive
Huneke-Wiegand variants.
