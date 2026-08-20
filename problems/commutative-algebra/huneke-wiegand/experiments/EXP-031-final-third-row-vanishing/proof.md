# EXP-031 proof - integral degree-seven contraction and the complete third row

## Theorem

For every integer `p>=4`, every field `k`, and every multigraded offset `b`,

```text
beta_(3,(7,b))(C_p)=0.
```

Consequently `beta_(3,7)(C_p)=0`. Together with EXP-027, EXP-029, EXP-030, regularity four, and
the minimum-shift bound, the complete third homological row is

```text
beta_(3,4)=p(5p-1)(500p^2-440p+47)/2,
beta_(3,5)=4p(8p-1),
beta_(3,6)=8p(7p^2-12p+2)/3,
beta_(3,7)=0,
beta_(3,j)=0 otherwise.
```

Its total rank is

```text
beta_3=p(7500p^3-7988p^2+2025p-133)/6.
```

## 1. Relative chain groups in total degree seven

Write `q=24p`, let `G_p=E_(p,1)` be the `10p` degree-one offsets, and fix a total offset `b`.
The relative-complex dictionary frozen in EXP-027 says that a squarefree cell `F` occurs in total
degree seven precisely when

```text
b-sum(F) is in E_(p,7-|F|).
```

The cumulative offset sets needed for first, second, and third chains are

```text
E_(p,5)=E_(p,4)=[0,q-1],
E_(p,3)=[0,q-1] minus {6p-1}.                         (1)
```

Put `h=6p-1`. Edges use `E_(p,5)`, triangles use `E_(p,4)`, and tetrahedra use `E_(p,3)`.
All cellular incidence coefficients are `+1` or `-1` over `Z`.

## 2. Distinguished-vertex matching

The offset `0` belongs to `G_p`. Use the following partial Boolean matching on the chain groups
through dimension three.

1. Match every edge `e` not containing `0` with the triangle `e union {0}`. The two cells have the
   same residual, and the first equality in (1) makes the match valid in both directions.
2. For a triangle `F` not containing `0`, match it with `F union {0}` whenever its residual is not
   `h`. The match is valid because the triangle residual belongs to the full set `E_(p,4)` and the
   tetrahedron residual belongs to `E_(p,3)` exactly when it is not `h`.

Every matched incidence is a unit. The matching is acyclic: every reversed matched arrow adds the
distinguished vertex `0`; after deleting any other vertex, the resulting face still contains `0`
and cannot be the lower cell of another matched arrow. In particular, every alternating path has
at most one reversed arrow in the relevant dimensions.

Every triangle containing `0` is the upper partner of its edge after deleting `0`. Every triangle
without `0` and residual different from `h` is the lower partner of its tetrahedron after adjoining
`0`. Hence the unmatched triangles are exactly

```text
F subset G_p minus {0},  |F|=3,  b-sum(F)=h.          (2)
```

## 3. A unit filler for every unmatched triangle

Since `p>=4`, the four offsets `1,2,3,4` all belong to `G_p`. For an unmatched triangle `F`, choose
the least

```text
x in {1,2,3,4} minus F.
```

Such an `x` exists because `F` has only three vertices. Put `T=F union {x}`. From (2),

```text
b-sum(T)=h-x.
```

Here `1<=x<=4`, so `0<=h-x<q` and `h-x!=h`. Equation (1) therefore shows that `T` is a
tetrahedron of the relative complex. It does not contain `0`, so it is unmatched by the partial
matching above.

For any vertex `y` of `T`, the residual of the triangle `T minus {y}` is

```text
b-sum(T minus {y})=h-x+y.                              (3)
```

This equals `h` if and only if `y=x`. Thus `F=T minus {x}` is the only unmatched triangle face of
`T`, and its direct boundary coefficient is `+1` or `-1`.

There is no hidden gradient contribution to another unmatched triangle. A noncritical face `G`
of `T` that does not contain `0` is paired upward with `G union {0}`. Every other triangle face of
that tetrahedron contains `0`, hence is paired downward with an edge and cannot be an unmatched
triangle of (2). Therefore the reduced boundary of `T` has exactly one entry in the unmatched
triangle rows, namely the unit entry on `F`.

At a fixed offset `b`, two different unmatched triangles cannot receive the same tetrahedron. If
one tetrahedron had two unmatched faces, equation (3) would require two distinct deleted vertices
to equal the single added vertex `x`. Reuse of the same tetrahedron tuple at a different offset is
irrelevant because it belongs to a different multigraded chain complex.

Consequently the reduced integral boundary from unmatched tetrahedra onto unmatched triangles
contains a signed identity block with one column for every unmatched triangle. It is surjective,
so integral `H_2` vanishes at every offset. Tensoring with any field proves the displayed
multigraded vanishing and characteristic independence.

## 4. Completion of the third homological row

EXP-027 proves the degree-four entry, EXP-029 proves the degree-five entry, and EXP-030 proves the
degree-six entry. The presentation has no linear equations, so the minimum shift in homological
degree three is four. EXP-024 proves regularity four, so no third syzygy can have internal degree
greater than seven. The theorem above kills the only remaining shift. This gives the complete row.

Adding the three nonzero total entries and simplifying gives

```text
beta_3=p(7500p^3-7988p^2+2025p-133)/6.
```

The formula is integral because it is the sum of the three already integral Betti formulas.

## 5. Validation and trust boundary

The canonical campaign checks the residual identities for all `p=4,...,300`, verifies explicit
unit fillers for every critical triangle at `p=4,...,12`, and computes the complete exact
degree-seven `H_2` profile at `p=4,5`. At `p=4`, all 374 offsets vanish over both `GF(2)` and
`GF(1000003)`; at `p=5`, all 470 offsets vanish over `GF(2)`. The independent implementation uses
the opposite filler order and matches critical counts, offset ranges, and unit-filler counts for
`p=4,...,12`. The arithmetic certificate checks the endpoint obligations through `p=300`.

The first smoke implementation incorrectly keyed fillers globally by tetrahedron tuple. It treated
the same tuple in two different offset complexes as a collision and stopped before rank
calculation. That attempt is preserved as `INVALID_IMPLEMENTATION` and is non-evidence. The
corrected route keys cells by `(offset,tetrahedron)`.

Finite ranks and arithmetic checks validate the implementations; they do not prove the theorem.
The all-parameter result rests on the integral acyclic matching and signed identity block in
Sections 2 and 3.
