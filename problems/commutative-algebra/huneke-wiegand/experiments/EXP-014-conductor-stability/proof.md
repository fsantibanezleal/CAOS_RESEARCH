# EXP-014 deductive proof

## General duality correction

Let `(R,m)` be a one-dimensional Gorenstein local ring and let `R subset E` be a finite birational
extension. Apply `Hom_R(-,R)` to

```text
0 -> R -> E -> E/R -> 0.
```

Because `E` is maximal Cohen-Macaulay over the one-dimensional Gorenstein ring,
`Ext^1_R(E,R)=0`. Also `Hom_R(E/R,R)=0` because `E/R` has finite length and `R` has depth one.
Therefore there is an exact sequence

```text
0 -> R:E -> R -> Ext^1_R(E/R,R) -> 0.
```

Local duality identifies `Ext^1_R(E/R,R)` with the Matlis dual of `E/R`, so

```text
length_R(R/(R:E))=length_R(E/R).
```

This is exactly Herzog-Kumashiro Proposition 3.1 Claim 1 after renaming their Gorenstein subring
`S` as `R` and their extension `R` as `E`. Thus EXP-013's equality of lengths is literature-derived
general structure. Its exact common ideal and the evaluated value `p+1` remain family-specific.

## Conductor nonstability by recognition

EXP-009 proves `R_p` is Gorenstein. EXP-011 proves `R_p subset E_p` is finite birational.
EXP-012 proves `type(E_p)=10p>1`, so `E_p` is not Gorenstein. Dey Corollary 3.7 states that for
such an extension over a one-dimensional Gorenstein base, `E_p` is Gorenstein if and only if its
conductor `R_p:E_p` is stable. Since EXP-013 identifies this conductor with `T_p`, `T_p` is not
stable for every `p>=4`.

## Direct family witness

The smallest value of `T_p` is `4s`. Its level-four residues are

```text
A_p=[0,p] union [3p,4p-2].
```

Both `1` and `p` belong to `A_p`, so

```text
8s+p+1=(4s+1)+(4s+p) lies in v(T_p^2).
```

However, membership in `v(t^(4s)T_p)` at level eight would require `p+1 in A_p`, which is false.
Hence `T_p^2 != t^(4s)T_p` for every `p>=4`. This direct witness is independent of the recognition
theorem.

## Finite defect bound

EXP-013 gives `[13s,infinity) subset v(T_p)`. Therefore
`[17s,infinity) subset v(t^(4s)T_p) subset v(T_p^2)`, so the quotient
`T_p^2/t^(4s)T_p` is decided completely below `17s`. The exact campaign therefore has a proved
finite tail and does not infer equality from a guessed cutoff.
