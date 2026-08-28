# EXP-034 proof - a surviving lower-strand Betti class

## Theorem

Let `p>=4`, let `P_p=k[X_g:g in G_p]`, and retain the EXP-033 exact sequence

```text
0 -> K_p -> A_p -> D_p -> 0,
A_p=P_p/Q_p,
D_p=P_p/(Q_p:f_p).
```

Give every variable the bigrade

```text
deg(X_g)=(1,g)
```

and write `beta_(i,(j,b))` for the corresponding standard-degree/offset Betti number. Put

```text
b_p=8p-1,
F_p={1,...,p},
tau_p=b_p+sum_(g=1)^p g=8p-1+p(p+1)/2.                       (1)
```

Then, over every field,

```text
beta_(p,(p+2,tau_p))^(P_p)(K_p)=1,
beta_(p,(p+2,tau_p))^(P_p)(A_p)=1,
beta_(p,(p+2,tau_p))^(P_p)(C_p)=1.                           (2)
```

In particular,

```text
beta_(p,p+2)(A_p)>=1,
beta_(p,p+2)(C_p)>=binom(8p,p-1)+1.                           (3)
```

This is one exact class in the previously unresolved regularity-two strand. It does not determine
either complete lower strand.

## 1. Regular reduction and the two-layer module

EXP-033 proves that `X_0` is regular on `K_p`. It is also regular on `D_p`: under the EXP-030
idealization

```text
D_p isomorphic to R_p semidirect omega_(R_p),
R_p=k[s,t]^(p),
```

the variable `X_0` acts by `s^p`, which is regular both on the domain `R_p` and on its torsion-free
canonical module. The exact sequence then makes `X_0` regular on `A_p` as well. Reduction modulo
`X_0` therefore preserves the sequence and the minimal Betti numbers. Put

```text
S_p=P_p/(X_0),
M_p=K_p/X_0K_p.
```

The EXP-033 offset bases of `K_p` are the high generator offsets in degree one and the stable
interval `[6p,24p-1]` in every degree at least two. Hence

```text
(M_p)_1=span{u_h:h in H_p},
H_p={g in G_p:g>=6p},                  |H_p|=8p,

(M_p)_2=span{v_b:b in B_p},
B_p=[6p,24p-1] minus H_p,              |B_p|=10p,

(M_p)_d=0                              for d>=3.              (4)
```

Multiplication is

```text
X_g u_h = v_(g+h)  if g+h in B_p,
X_g u_h = 0        otherwise.                                (5)
```

Indeed, a product in the stable interval represents its offset basis element. If its offset lies
in `H_p`, it is `X_0u_(g+h)` and vanishes in the reduction; if it lies in `B_p`, it is the stated
degree-two basis element. Products outside the stable interval vanish. Equation (4) also makes
the full degree-two layer socle.

## 2. The incidence maps compute both Betti strands of the kernel

Let `V_p` have basis `e_g`, indexed by `G_p minus {0}`. In standard internal degree `i+1`, the
Koszul complex of `M_p` has only two nonzero terms:

```text
delta_i: exterior^i(V_p) tensor (M_p)_1
         -> exterior^(i-1)(V_p) tensor (M_p)_2,               (6)

delta_i(e_F tensor u_h)
 =sum_(g in F, h+g in B_p)
    (-1)^pos e_(F minus {g}) tensor v_(h+g).                  (7)
```

There is no incoming term on the left because `(M_p)_0=0`, and no outgoing term on the right
because `(M_p)_2` is socle. Therefore

```text
beta_(i,i+1)(K_p)=dim ker(delta_i),
beta_(i-1,i+1)(K_p)=dim coker(delta_i),                       (8)
```

with the same formulas in every offset. This is the promised exact reduction of the full
resolution of `K_p` to two-layer incidence ranks.

## 3. The first missing generator gives a rank-one cokernel

The smallest element of `B_p` is

```text
b_p=8p-1.                                                     (9)
```

The positive degree-one offsets have smallest `p` elements `1,...,p`. Thus the smallest total
offset in the codomain of `delta_(p+1)` is `tau_p`, and the corresponding component is
one-dimensional with basis

```text
e_(F_p) tensor v_(b_p).                                      (10)
```

Its possible incoming variables form

```text
R_(b_p)={g in G_p minus {0}:b_p-g in H_p}.                   (11)
```

For `1<=g<=p`, the complementary offset lies in `[7p-1,8p-2]`, a subinterval of the first high
block. For `3p<=g<=4p-2`, it is at most `5p-1`, below every high offset. For `g>=6p`, it is at
most `2p-1`, again below every high offset. These cases exhaust `G_p minus {0}`, so

```text
R_(b_p)=F_p.                                                  (12)
```

An incoming term to (10) would require a domain exterior set `F_p union {g}` with
`g in R_(b_p) minus F_p`. This set is empty. Consequently the single row in this multidegree is
zero, integrally, and

```text
beta_(p,(p+2,tau_p))(K_p)=1.                                 (13)
```

The class is primitive over `Z`, so (13) is characteristic-independent.

## 4. The connecting map cannot hit the distinguished coordinate

Reduce the exact sequence modulo `X_0` and consider the connecting map

```text
Tor_(p+1)^(S_p)(D_p/X_0D_p,k)_(p+2,tau_p)
  -> Tor_p^(S_p)(M_p,k)_(p+2,tau_p).                         (14)
```

The degree-one basis of `D_p/X_0D_p` has low offsets

```text
L'_p=[1,p] union [3p,4p-2].                                  (15)
```

To contribute to (10), a lifted Koszul differential must remove a high exterior variable `h`
and multiply it by a low coefficient `X_l` with `h+l=b_p`. By (12), the only possibilities are

```text
l=1,...,p,       h_l=b_p-l in [7p-1,8p-2].                  (16)
```

After fixing the high exterior factor `e_(h_l)`, the selected low chain is

```text
e_(F_p) tensor X_l                                             (17)
```

at low total offset

```text
sigma_l=sum(F_p)+l.                                           (18)
```

It is the only low chain in that multidegree. If a size-`p` exterior set contains a variable from
the second block in (15), its exterior sum is at least

```text
3p+1+...+(p-1)=sum(F_p)+2p,
```

and adding a positive coefficient exceeds `sigma_l` because `l<=p`. If the coefficient itself
lies in the second block, the same conclusion follows from `3p>l`. Thus every exterior variable
lies in `[1,p]`; size `p` forces `F_p`, and (18) forces the coefficient to be `l`.

This unique chain is not a cycle. Its Koszul boundary term obtained by removing `p` is

```text
(-1)^(p-1)e_({1,...,p-1}) tensor X_pX_l.                     (19)
```

In `D_p/X_0D_p`, the ring-summand degree-two offsets are `[p+1,2p]`. Since
`p+l` lies in this interval, (19) is a nonzero unit coordinate. The high variables annihilate
`D_p`, so its Koszul complex splits by high exterior set. Chains with two or more high exterior
variables cannot leave the high-free exterior `F_p` after one differential, and low-low
multiplication agrees in the two quotients. Therefore every cycle in the source of (14) has zero
coefficient on every chain (17). The connecting map is zero on the unique target component (10).

## 5. Exact survival in `A_p` and `C_p`

EXP-032 gives the row-two strand of `D_p` by tensoring the low terminal class at homological
degree `c=2p-2` with the high-variable Koszul complex. Since `p<c`,

```text
Tor_p^(P_p)(D_p,k)_(p+2)=0.                                  (20)
```

Equations (13), (14), and (20), together with the long exact Tor sequence, prove the middle
equality in (2), including exact multiplicity one.

The EXP-033 cubic cone is multigraded and minimal; the cubic has offset `3p`. A possible extra
summand at the last component in (2) would come from the diagonal group

```text
Tor_(p-1)(D_p,k)_(p-1,tau_p-3p).
```

That diagonal is the Koszul wedge on `p-1` high linear generators. Its smallest shifted offset is

```text
3p+sum_(h=6p)^(7p-2) h.
```

Subtracting `tau_p` gives

```text
(p-2)(6p-1)>0.                                                (21)
```

Hence no shifted diagonal class occurs at `tau_p`, and the final equality in (2) follows.

Finally, summing offsets gives the first inequality in (3). The minimal cubic cone contributes
the full shifted diagonal rank `binom(8p,p-1)` to `beta_(p,p+2)(C_p)`, while the surviving class
adds at least one more, proving the second inequality.

## 6. Reproducible validation and trust boundary

- The canonical exact campaign verifies the frozen premise hashes, all basis counts, (9)--(13),
  the row-two boundary, and the shifted-diagonal exclusion for all 297 values `p=4,...,300`.
- Literal boundary matrices through `p=8` have a one-rank drop when the selected source column is
  removed over both `GF(2)` and `GF(1000003)`.
- The independent route rebuilds the Artinian fiber bases from numerical-semigroup ideal powers
  for `p=4,...,25`, matching the canonical high and kernel hashes. It enumerates every rational
  source through `p=9`; each declared low multidegree has one source chain and boundary rank one.
- Eight Z3 interval negations are UNSAT. A separate coefficient implementation checks 299 rows
  through `p=300` plus `p=500,1000`; SymPy gives the exact gap (21).
- Filled-gap, deleted-variable, wrong-target, wrong-exterior, wrong-shift, and partition mutations
  are rejected.

Aggregates:

```text
canonical       65ef176dcd9f5bd5467c09e763fdb20c67798de9743443ce5d0e34958c1645ce
finite ranks    31d70c09d251bb6009b610be05c33a42ccd50e417b84aff2c0db561018e6acc5
independent     31479abd3c7247fe0ba464eefe06e437a595812c3d6055d0de8d0ced25d12794
symbolic        b3f461298706a394cc0f1a296557e10f52435f78d2f1039452fb726871b79a4d
```

The finite campaigns validate implementations. The regular reduction, one-dimensional target,
representation-set exclusion, unique source, unit boundary, and Tor exact-sequence argument prove
the theorem for every `p>=4` and every field.

