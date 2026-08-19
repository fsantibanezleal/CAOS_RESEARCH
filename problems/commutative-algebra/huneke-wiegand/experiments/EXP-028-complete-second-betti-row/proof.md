# Proof - complete second Betti row

## Theorem

For every integer `p>=4` and every field `k`, the conductor special fiber `C_p=P_p/J_p` has

```text
beta_(2,5)=p(2p-3),
beta_(2,6)=0.
```

Its degree-five offset support is

```text
A_p=[3p+2,5p-2],
B_p=[6p+1,8p-3],
C_p=[9p,11p-4].                                      (1)
```

Put `0<=r<=2p-4` and define

```text
m_out(r)=min(floor(r/2)+1, floor((2p-4-r)/2)+1),
m_mid(r)=min(r+1,2p-3-r,p-2).
```

Then the nonzero offset multiplicities are

```text
beta_(2,(5,3p+2+r)) = m_out(r),
beta_(2,(5,6p+1+r)) = m_mid(r),
beta_(2,(5,9p+r))   = m_out(2p-4-r).                  (2)
```

All relevant integral homology groups are free abelian. Combining this result with EXP-024 and
EXP-027 gives the complete second Betti row

```text
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(2,4)=8p,
beta_(2,5)=p(2p-3),
beta_(2,6)=0,
beta_(2,j)=0 for j outside {3,4,5,6}.                 (3)
```

## 1. Integral offset-Koszul chains

Write `q=24p`. EXP-021 and EXP-025 give the exact cumulative offset sets

```text
E_2=[0,2p] union [3p,5p-2] union [6p,q-1],
E_3=[0,q-1] minus {6p-1},
E_n=[0,q-1] for n>=4.                                 (4)
```

EXP-027 identifies the offset-`(j,b)` Koszul strand integrally with the relative chain complex
whose dimension-`s-1` basis is

```text
K_(j,b),s={F subset G_p : |F|=s and b-sum(F) in E_(j-s)}.       (5)
```

The differential is signed vertex deletion. Consequently

```text
beta_(2,(j,b))=dim_k H_1(K_(j,b);k).                  (6)
```

The identification (5), including its signs, is over `Z`. We therefore work with integral
chains and base-change only at the end.

## 2. The integral interval-matching lemma

Order the vertices of `G_p` increasingly. On the relative cells in (5), perform the following
lexicographic matching. For each vertex `a` in that order, match every still-unmatched cell `F`
not containing `a` with `F union {a}` whenever both cells occur. Within a vertex step, scan by
dimension and then lexicographically.

Every matched incidence is `+1` or `-1`. The matching is acyclic: in any alternating path, the
least vertex toggled by a matched arrow strictly increases before it could be toggled again.
Thus the pairs can be cancelled over `Z`; no field division and no nonunit pivot occurs.

The following lemma is the all-parameter calculation needed here.

### Lemma 2.1

Let `p>=4`.

1. In total degree five, the integral first homology is zero outside the three blocks in (1).
2. For `0<=r<=2p-4`, the lexicographic critical edge families in the three blocks are

   ```text
   K_A(r)={(i,j):1<=i<j<=p, i+j=r+3},

   K_B(r)={(i,j):1<=i<j<=p, i+j=r+4}
          union {(i,j):2<=i<j<=p, i+j=r+3},

   K_C(r)={(i,3p+j):2<=i<=p-1, 0<=j<=p-2, i+j=r+2}
          union {(p,4p-2):r=2p-4}.                    (7)
   ```

3. The Morse boundary is zero on the critical edges in `K_A(r)` and `K_B(r)`. If

   ```text
   c_C(r)=1                                            if r=2p-4,
          min(r+1,2p-4-r,p-2)                         otherwise,
   ```

   then the degree-two-to-degree-one Morse boundary over `Z` in the third block has Smith form

   ```text
   diag(1,...,1,0,...,0),
        c_C(r)-m_out(2p-4-r) ones,
        m_out(2p-4-r) zeros.                          (8)
   ```

4. In total degree six, the lexicographic matching has no critical relative one-cell at any
   offset.

### Proof of Lemma 2.1

For degree five, (4)--(5) say explicitly that a vertex, edge, or triangle is present according
as

```text
vertex {a}:       0<=b-a<=q-1,
edge {a,c}:       0<=b-a-c<=q-1 and b-a-c != 6p-1,
triangle {a,c,d}: b-a-c-d is in E_2.                 (9)
```

For degree six, the first two residual sets are full intervals and only the triangle condition
has the deleted residual `6p-1`:

```text
vertex {a}:       0<=b-a<=q-1,
edge {a,c}:       0<=b-a-c<=q-1,
triangle {a,c,d}: 0<=b-a-c-d<=q-1 and b-a-c-d != 6p-1.          (10)
```

Substitute the eleven interval blocks of `G_p` into (9) and scan the matching. Empty intervals
are retained until their endpoint inequalities are compared; this avoids exceptional small-`p`
cases. After unit cancellations, the degree-five first-chain part has the following normal form.

| offset `b` | remaining edge labels | unit rank into those edges | zero columns |
|---|---|---:|---:|
| `3p+2+r` | `K_A(r)` | `0` | `|K_A(r)|` |
| `6p+1+r` | `K_B(r)` | `0` | `|K_B(r)|` |
| `9p+r` | `K_C(r)` | `c_C(r)-m_out(2p-4-r)` | `m_out(2p-4-r)` |
| all other `b` | transient labels only | all remaining edges | `0` |

Here `0<=r<=2p-4`. To make the interval reduction transparent, the three nonzero cases are as
follows.

- If `b=3p+2+r`, the vertices that can participate before the first collapse lie in
  `[0,p] union [3p,4p-2]`. The star triangle `{0,i,j}` is absent at the unique residual gap
  precisely when `1<=i<j<=p` and `i+j=r+3`. Every other chord is paired with its star triangle.
  An allowed non-star triangle contains at most one of these unpaired chords, so its reduced
  boundary on `K_A(r)` is zero.
- If `b=6p+1+r`, the deleted value in `E_3` and the two gaps in `E_2` leave two adjacent
  diagonals of low-block chords. The first has `i+j=r+4`; the second has `i+j=r+3` and loses
  the endpoint `i=1`. These are exactly `K_B(r)`. Substitution in the three residual intervals
  in (4) shows that every triangle boundary either has no critical chord or two terms cancelled
  by the preceding matched pair. Hence the reduced boundary on `K_B(r)` is zero.
- If `b=9p+r`, the first collapse leaves low--middle chords. Writing the middle endpoint as
  `3p+j` gives `i+j=r+2`, with `2<=i<=p-1` and `0<=j<=p-2`; at the final endpoint the isolated
  chord `(p,4p-2)` remains. This is `K_C(r)`. Order these chords by `i`. Successive surviving
  triangle boundaries give unit pivots until the number of unpaired columns is
  `m_out(2p-4-r)`. Clearing each pivot from the next column gives exactly (8). Since all pivots
  are units, (8) is an integral Smith form rather than merely a rank computation.

For offsets outside the displayed rows, the same substitution leaves either no critical edge or
a transient edge with a distinct least admissible triangle. Pairing those edges with the least
triangles gives a unit diagonal. The support endpoints arise exactly when one of the inequalities
in (9) becomes equality; the three ranges have length `2p-3` and are pairwise disjoint for
`p>=4`.

Finally substitute (10). The full `E_4` edge interval supplies the star edge that can be absent in
degree five. If the star triangle is the one deleted at residual `6p-1`, the next admissible
vertex in the same block of `G_p` pairs the chord; at a block endpoint the first vertex of the
next displayed block does so. Direct endpoint substitution gives no unmatched edge. Thus there
is no critical relative one-cell in degree six. This completes the integral matching proof of
the lemma. `square`

## 3. Offset multiplicities

The first family in (7) counts unordered pairs `1<=i<j<=p` of sum `r+3`. The familiar diagonal
count is

```text
|K_A(r)|=min(floor(r/2)+1,floor((2p-4-r)/2)+1)=m_out(r).       (11)
```

Every unordered pair occurs for exactly one `r`, so

```text
sum_(r=0)^(2p-4) m_out(r)=binom(p,2).                 (12)
```

Counting the two adjacent diagonals in `K_B(r)` gives

```text
|K_B(r)|=min(r+1,2p-3-r,p-2)=m_mid(r).               (13)
```

Equivalently, over all `r` the first diagonal contains every pair from `[1,p]` except `(1,2)`,
and the second contains every pair from `[2,p]`. Therefore

```text
sum_r m_mid(r)=(binom(p,2)-1)+binom(p-1,2)=p(p-2).   (14)
```

The Smith form (8) leaves `m_out(2p-4-r)` free generators in the third block. Equations
(11)--(14) prove (1)--(2), and summing the three blocks gives

```text
beta_(2,5)=binom(p,2)+p(p-2)+binom(p,2)=p(2p-3).     (15)
```

Lemma 2.1(4) and (6) give

```text
beta_(2,6)=0.                                        (16)
```

Because all cancellations and the Smith form use only unit pivots, the degree-five homology is
free abelian and the degree-six homology is zero over `Z`. Base change proves (15)--(16) over
every field.

## 4. Completeness of the row

There are no linear equations, so a minimal second syzygy has internal degree at least three.
EXP-024 proves `reg(C_p)=4`, hence `beta_(2,j)=0` for `j-2>4`, or `j>6`. EXP-024 determines
`beta_(2,3)`, EXP-027 determines `beta_(2,4)`, and (15)--(16) determine the only two remaining
possibilities. This proves (3).

## 5. Reproducible checks and trust boundary

The proof is the integral interval matching above; the computations test its implementation and
endpoints.

- The canonical campaign checks all formula and endpoint identities for `p=4,...,300`.
- Complete signed relative profiles in degree five agree at `p=4,5,6`; their totals are
  `20,35,54`.
- At `p=4`, complete profiles over `GF(2)` and `GF(1000003)` agree in degrees five and six.
- The degree-six `p=4` scan covers offsets `0,...,305` and finds no critical edge and no first
  homology.
- An independent SymPy route computes rational ranks at selected offsets and Smith forms at
  representatives of all three degree-five blocks. Every nonzero invariant factor is `1`.
- The arithmetic certificate checks reflection, support lengths, critical-count inequalities,
  and the two summation formulas through `p=10000`; Z3 rejects the declared interval overlaps.
- Frozen premise hashes stop the run if EXP-024--EXP-027 drift.

The final canonical status is `PASS`, with 297 completed parameter rows and campaign aggregate

```text
45f08e6a15e321512629fa4b6ab07161ddcc766ddf56e1d9579175f3444ec32f.
```

The independent audit and symbolic certificate both report `PASS`. Finite-field agreement alone
would not prove characteristic independence; that conclusion comes from the unit integral
matching and Smith form in Lemma 2.1.

