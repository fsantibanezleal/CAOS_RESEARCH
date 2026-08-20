# EXP-029 proof - the colon-Koszul degree-five diagonal

## Theorem

Let `p>=4`, let `P_p=k[X_a:a in G_p]`, and let `C_p=P_p/J_p` be the conductor special fiber of
EXP-021. Over every field,

```text
beta_(3,5)(C_p)=binom(8p,2)=4p(8p-1).                         (1)
```

Put

```text
H_p={a in G_p:a>=6p}.
```

The complete offset-graded profile is

```text
beta_(3,(5,b))=#{ {a,c} subset H_p:a<c and a+c=b-3p }.        (2)
```

Its support is

```text
[15p+1,39p-3] minus {33p-1}.                                 (3)
```

The corresponding integral relative homology is free abelian. Together with EXP-028 and the
Hilbert numerator, the complete internal-degree-five diagonal is

```text
beta_(2,5)=p(2p-3),
beta_(3,5)=4p(8p-1),
beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3,
beta_(i,5)=0 for i outside {2,3,4}.                            (4)
```

## 1. The high cubic colon

EXP-023 and EXP-027 prove

```text
J_p=(Q_p,f_p),
f_p=X_0^2X_(3p)-X_p^3,
(Q_p:f_p)_1=span_k{X_a:a in H_p}.                             (5)
```

Using the eleven-block formula for `G_p`, the high set is

```text
H_p=
 [6p,8p-2] union [8p,10p-2] union {10p}
 union [11p-1,12p-1]
 union [13p+1,14p-2] union [14p,15p-1]
 union {16p} union [17p-1,18p-1].                             (6)
```

The disjoint block lengths sum to `8p`. The linear strand of `P_p/(Q_p:f_p)` is therefore the
Koszul strand on these `8p` coordinate variables. Its second wedges are indexed by unordered
distinct pairs `{a,c}` in `H_p`. After the cubic shift, their bidegrees are

```text
(5,3p+a+c).                                                   (7)
```

This identifies the candidate colon-Koszul classes and predicts (2). Completeness and
primitivity are proved next inside the integral relative complex, so no minimal mapping-cone
assumption is left implicit.

## 2. Integral relative chains in total degree five

EXP-025 gives, with `q=24p`,

```text
E_1=G_p,
E_2=[0,2p] union [3p,5p-2] union [6p,q-1],
E_3=[0,q-1] minus {6p-1},
E_4=[0,q-1].                                                  (8)
```

For offset `b`, the total-degree-five relative Koszul chain with a size-`s` vertex set `F` is
present exactly when

```text
b-sum(F) is in E_(5-s).                                      (9)
```

The signed differential deletes one vertex. In particular, `beta_(3,(5,b))` is the dimension of
the second homology, and only cells of sizes two, three, and four enter its kernel and image.

Order the vertices increasingly. Apply the EXP-028 lexicographic matching through size four:
at vertex `v`, pair each still-unmatched cell not containing `v` with its `v`-coface whenever
both occur, scanning first by size and then lexicographically. Every matched incidence is `+1`
or `-1`. The least toggled vertex increases along a reversed matched arrow, so the matching is
acyclic and every cancellation is valid over `Z`.

The following normal-form lemma is the family-wide interval calculation.

### Lemma 2.1 (degree-five normal form)

For every `p>=4` and offset `b`, the integral complex (9) is chain-homotopy equivalent, in the
dimensions bearing on second homology, to

```text
0 -> Z^(T_b) --(I,0)--> Z^(T_b) direct_sum Z^(K_b) -> 0,      (10)
```

plus contractible unit summands, where

```text
K_b={(p,a,c):a<c in H_p and a+c=b-3p}.                        (11)
```

Here `T_b` is a possibly empty set of transient critical triangles. The displayed identity
block is integral, and no boundary column has a component in the `K_b` block.

### Proof

Substitute (8) in (9). A vertex, edge, triangle, or tetrahedron occurs according as

```text
vertex {a}:          0<=b-a<=q-1,
edge {a,c}:          0<=b-a-c<=q-1 and b-a-c != 6p-1,
triangle {a,c,d}:    b-a-c-d in E_2,
tetrahedron F:       b-sum(F) in G_p.                         (12)
```

The first lexicographic pass cancels every triangle whose least admissible coface is present,
together with the lower-dimensional pairs created earlier in the scan. A critical triangle is
then tested against the least remaining tetrahedron in the same order. The three gaps in (8),

```text
[2p+1,3p-1], [5p-1,6p-1], and {6p-1},                        (13)
```

are the only reasons a proposed toggle can fail. Comparing their translated endpoints with the
blocks of `G_p` gives two cases.

1. If the triangle is not `(p,a,c)` with `a<c` in `H_p`, the first failed toggle from (13) is
   followed by an admissible vertex in the same block of `G_p`, or by the first vertex of the
   next block in (6). This gives a tetrahedron with incidence `+1` or `-1`. Ordering these
   transient triangles by the failed toggle, then lexicographically, makes their boundary
   submatrix upper triangular with unit diagonal. These are the `T_b` rows in (10).
2. For `(p,a,c)` with `a<c` in `H_p`, equation (12) gives the residual value `2p`, the right
   endpoint of the first component of `E_2`. Every possible earlier filler was already cancelled,
   and the next toggle crosses one of the gaps in (13). Hence the triangle survives. Conversely,
   the same endpoint comparison shows that no other triangle lacks the unit filler of case 1.

The least-toggle order also shows that a transient boundary may contain only its own row and rows
later in the order. It cannot contain a pair row from case 2. Clearing from first to last gives
the integral block `(I,0)` in (10). All other matched pairs are contractible unit summands. This
proves the lemma. `square`

Lemma 2.1 yields

```text
H_2(K_(5,b);Z)=Z^(K_b).                                      (14)
```

Thus (2) holds integrally. It also identifies the surviving basis with the second Koszul wedges
from (5)-(7), providing the mapping-cone cross-check without using it as an unproved minimality
shortcut. Base change in (14) proves characteristic independence.

## 3. Pair-sum support and total

Write the non-singleton blocks needed for coverage as

```text
A=[6p,8p-2],       B=[8p,10p-2],
D=[11p-1,12p-1],   E=[13p+1,14p-2],
F=[14p,15p-1],     G={16p},
K=[17p-1,18p-1].
```

Sums of two distinct elements from one interval and sums from two different intervals give the
following coverage. The labels name the two source blocks.

| pair | unshifted sum interval |
|---|---|
| `AA` | `[12p+1,16p-5]` |
| `AB` | `[14p,18p-4]` |
| `AD` | `[17p-1,20p-3]` |
| `BD` | `[19p-1,22p-3]` |
| `BE` | `[21p+1,24p-4]` |
| `AK` | `[23p-1,26p-3]` |
| `BK` | `[25p-1,28p-3]` |
| `DK` | `[28p-2,30p-2]` |
| `EK` | `[30p,32p-3]` |
| `FK` | `[31p-1,33p-2]` |
| `GK` | `[33p-1,34p-1]` |
| `KK` | `[34p-1,36p-3]` |

For `p>=4`, consecutive rows overlap or meet except between `DK` and `EK`, where the sole missing
integer is `30p-1`. That integer is not supplied by any omitted pair of blocks: a direct check of
the complementary ranges in (6) shows that `a+c=30p-1` would require one member in a gap of
`H_p`, or would violate `a<c`. Hence the pair-sum support is

```text
[12p+1,36p-3] minus {30p-1}.                                 (15)
```

Adding the cubic offset `3p` proves (3). There are `24p-4` supported offsets. Counting the basis
in (14) without grouping by sum gives

```text
beta_(3,5)=|K_b over all b|=binom(|H_p|,2)
          =binom(8p,2)=4p(8p-1),                              (16)
```

which proves (1).

Equivalently, if `A_p(t)=sum_(a in H_p)t^a`, the full multiplicity profile is the integer
coefficient formula

```text
beta_(3,(5,b))=[t^(b-3p)](A_p(t)^2-A_p(t^2))/2.               (17)
```

## 4. Completion of internal degree five

EXP-024 gives

```text
sum_(i,j)(-1)^i beta_(i,j)z^j
=(1-z)^(10p-1)(1+(10p-1)z+12pz^2+(2p-1)z^3+z^4).             (18)
```

There is no degree-five minimal equation. EXP-028 gives `beta_(2,5)=p(2p-3)`. Because there are
no linear equations, minimality forces `beta_(i,5)=0` for `i>=5`. Therefore only homological
degrees two, three, and four contribute to the coefficient of `z^5`:

```text
[z^5](18)=beta_(2,5)-beta_(3,5)+beta_(4,5).                   (19)
```

Substitute EXP-028 and (16), expand the left side, and solve for the last term. This gives

```text
beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3.                (20)
```

The numerator is divisible by three: checking `p` modulo three makes one of the displayed
factors or the final quadratic divisible by three. Equations (16), (19), and (20) prove (4).

## 5. Reproducible validation and trust boundary

The theorem is the integral normal form above. The computation validates its implementation and
boundary cases.

- The canonical campaign checks all pair profiles, endpoints, unique holes, totals, and Hilbert
  coefficient identities for `p=4,...,300`.
- Complete signed relative `H_2` profiles agree with (2) at `p=4,5,6`, with totals
  `496,780,1128`.
- The `p=4` complete profile agrees over `GF(2)` and `GF(1000003)`.
- An independent SymPy route reconstructs rational ranks immediately outside and at the left
  support endpoint: `H_2=0` at offset `60` and `H_2=1` at offset `61`.
- A separately encoded arithmetic/Z3 certificate checks the twelve support intervals, unique
  hole, support count, divisibility, and coefficient identity through `p=10000`.
- Frozen premise hashes stop the canonical runner if EXP-023 through EXP-028 drift.
- The first symbolic implementation exceeded its route budget because it materialized every
  support integer. It is preserved as non-evidence. Constant-memory endpoint merging then passed
  the unchanged obligations.

Canonical aggregates:

```text
campaign: 7564f15534e8a29f875a367d3a324b95041e8eef836d15deac3e35130e1ad37d
audit:    337854eef5d773c84cdd79c7734e63b295fa0337c5a1852e652559c334949b04
symbolic: 605733497d6fb0ead97bfd25e26daaa66d546c297751960e1c427f29ff69f279
```

Finite-field agreement alone would not prove (1)-(4). Characteristic independence comes from
the unit integral normal form (10), not from the sampled primes.

