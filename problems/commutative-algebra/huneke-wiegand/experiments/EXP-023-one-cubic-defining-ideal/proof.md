# EXP-023 - exact one-cubic presentation

Fix an integer `p>=4`. Put `q=24p`, let `T_p` be the conductor ideal from EXP-013 through
EXP-021, and write

```text
C_p=F(T_p),
S_p=k[X_a : a in E_1],
J_p=ker(S_p -> C_p),
```

where `X_a` maps to the degree-one class of `t^(q+a)`. The cumulative offset bases of the
Artinian reduction of `C_p` are

```text
E_1 = G,
E_2 = [0,2p] union [3p,5p-2] union [6p,24p-1],
E_3 = [0,24p-1] minus {6p-1},
E_4 = E_5 = [0,24p-1].                              (1)
```

Here `G` is the union of the ten degree-one blocks encoded in `run.py`; it has cardinality
`10p` and contains `0,p,3p`. Formula (1) is obtained by cumulative union of the disjoint layers
proved in EXP-021. All intervals are integer intervals.

## Theorem

For every integer `p>=4`,

```text
J_p=((J_p)_2, F_p),   F_p=X_0^2 X_(3p)-X_p^3.         (2)
```

Consequently,

```text
beta_(1,2)=50p^2-17p,
beta_(1,3)=1,
beta_(1,j)=0 for j>=4,
mu(J_p)=50p^2-17p+1,
relation-type(C_p)=3.                                 (3)
```

The standard graded algebra `C_p` is Cohen--Macaulay but not Koszul.

The all-parameter connectivity step below is an exact machine-verified Presburger argument. The
finite campaigns support it but are not used to generalize from samples.

## 1. The degreewise state graph

EXP-022 proves the value-congruence description of `J_p`: a monomial is zero precisely when its
offset is absent from the relevant `E_d`, and two nonzero monomials have the same image precisely
when their offset sums agree.

Assume the complete kernel is already known through degree `d-1`, for `d` in `{3,4,5}`. The
degree-`d` quotient by all lower-degree equations is spanned by states

```text
(a,b),  a in E_1, b in E_(d-1),                        (4)
```

representing `X_a` times the unique surviving class of offset `b`. If

```text
r=t-a-c in E_(d-2),  t=a+b,                            (5)
```

then commutativity of the common product gives an edge

```text
(a,t-a) -- (c,t-c).
```

If `c` is in `E_1` and `r` is in `E_(d-2)` but `t-c` is absent from `E_(d-1)`, the same product
connects `(a,t-a)` to zero. These moves generate exactly the variable multiples of the complete
kernel below degree `d`: every such multiple is one of these equal-product or zero-product moves,
and every displayed move is such a multiple.

It follows that the degree-`d` quotient has one basis vector for each nonzero state component.
For a valid total `t in E_d`, its image in `(C_p)_d` is the one-dimensional offset-`t` class. For
an invalid total its image is zero. Therefore

```text
beta_(1,d)
 = number of nonzero state components - |E_d|.          (6)
```

This proves that connectivity is the exact minimal-equation question, not a heuristic proxy.

## 2. Degree three

Before adjoining a cubic, the exact connectivity profile is:

| total `t` | hub | maximum path length | conclusion |
|---|---:|---:|---|
| `[0,2p]` | `0` | 3 | one nonzero component |
| `[2p+1,3p-1]` | `t-2p` | 3 | one nonzero component |
| `3p` | separate analysis | 1 | exactly two components |
| `[3p+1,5p-2]` | `0` | 3 | one nonzero component |
| `[5p-1,6p-2]` | `t-(5p-2)` | 3 | one nonzero component |
| `[6p,24p-1]` | `0` | 3 | one nonzero component |

The only invalid total below the high tail is `6p-1`; its states reach zero in at most one move.
Every invalid total `24p<=t<=42p-2` also reaches zero in at most one move. The upper endpoint is
complete because `max(E_1)+max(E_2)=42p-2`.

At `t=3p`, the vertex condition from (1) gives exactly the three vertices `0,p,3p`. The edge
condition joins `0` to `3p`; the vertex `p` is isolated. The two resulting monomial components
are represented by

```text
X_0^2 X_(3p)  and  X_p^3.
```

Their difference is `F_p`. Thus (6) gives `beta_(1,3)=1`, and adjoining `F_p` joins the only two
exceptional components.

The table and the zero assertions were checked over all integers `p>=4`, not sampled values. Each
negated assertion is a quantifier-bearing Presburger formula using the interval predicates in
(1) and the ten affine blocks of `E_1`. `symbolic_certificate.py` covers the high regions by the
half-open affine cells `mp<=t<(m+1)p`, bisecting only when a solver query initially times out. All
133 terminal formulas are UNSAT; there are no SAT or unresolved leaves. This is the exact
all-parameter exclusion of an additional cubic component.

## 3. Degree four

Now `E_2` is the remainder basis and `E_3` is the preceding basis. Let

```text
H=[2p+1,3p-1] union [5p-1,6p-2]
```

be the complement of `E_2` inside `[0,6p-2]`.

For a valid total `t!=6p-1`, zero is a vertex. If a state `(a,t-a)` has `t-a in E_2`, it is
adjacent to zero. Otherwise `t-a in H`, and the state is adjacent to the vertex `p`. If
`t-p in E_2`, that vertex is adjacent to zero. If `t-p in H`, the intermediate vertex
`c=t-3p` lies respectively in `[1,p-1]` or `[3p,4p-2]`, both subsets of `E_1`, and gives a path
from `p` to zero. The apparent boundary `t=7p-1` cannot occur with both `t-a in H` and `a in E_1`.
Thus every valid state reaches zero in at most three edges.

At `t=6p-1`, zero is not a vertex. The vertices are exactly

```text
[1,p] union [3p,4p-2].
```

The first block is connected through `p`; every vertex in the second block has an edge to the
first block. Hence there is one component, with hub `p`. For `t>=24p`, the condition
`t-a in H` would force `a>18p-1=max(E_1)`, so every state has a direct zero edge.

These reductions are also encoded as exact Presburger negations in the certificate. Therefore
`beta_(1,4)=0`.

## 4. Degree five

Here the preceding basis is `E_4=[0,24p-1]`, while the remainder basis is
`E_3=[0,24p-1] minus {h}` with `h=6p-1`.

For a valid total `t` and state `(a,t-a)`, the direct edge to zero works unless `t-a=h`. In that
exceptional case use the generator `1`; if `a=1`, use `2` instead. The resulting neighboring state
has a direct edge to zero. Hence every valid state reaches zero in at most two moves. For an
invalid total `t>=24p`, the equality `t-a=h` is impossible because `a<=18p-1`, so the direct zero
edge always works. Thus `beta_(1,5)=0`.

## 5. Completeness above degree five

EXP-017 proves that `Q_p=(t^q)` is a minimal reduction of `T_p` with reduction number four.
EXP-021 proves that `C_p=F(T_p)` is Cohen--Macaulay. Abdolmaleki--Kumashiro, Theorem 2.8, then
constructs the complete defining ideal using equations only in degrees `2,...,r+1`, here through
degree five. Sections 2 through 4 therefore exhaust every possible higher minimal equation.

EXP-022 already gives

```text
beta_(1,2)=binom(10p+1,2)-22p=50p^2-17p.
```

Together with the degree-three through degree-five calculation and the source-backed degree bound,
this proves (2) and (3).

Finally, EXP-021 supplies Cohen--Macaulayness. A standard graded Koszul algebra has a quadratic
defining ideal, whereas `F_p` is a necessary minimal cubic. Hence `C_p` is not Koszul.

## 6. Independent exact evidence

The theorem was tested by two separately encoded finite routes:

- the state campaign passed every `p=4,...,23` with first Betti profile
  `(50p^2-17p,1,0,0)`;
- the audit rehashed all 20 rows and reconstructed `p=4,13,23` total by total without importing
  the campaign implementation.

The first attempted range, `p=4,...,24`, exceeded its declared five-minute budget only after
finishing the row at `p=24`. It remains preserved as `INCONCLUSIVE_BUDGET`; it is not treated as
a mathematical failure or silently relabeled as a pass.

The exact artifacts and their hashes are recorded in `verdict.md`.
