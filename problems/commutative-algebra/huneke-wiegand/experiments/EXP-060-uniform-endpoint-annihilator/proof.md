# EXP-060 proof: a uniform original source for twice the endpoint residual

Date: 2026-09-05. Scope: every integer `p>=8`, in the original integral
presentation `M` of EXP-036. This is a symbolic source identity. The independent
finite audit and its resource outcomes are recorded separately; they are not the
reason an all-parameter conclusion follows.

## 1. Statement, grading, and orientation

Put `L=[1,p] union [3p,4p-2]`, `h=8p-2`, and
`tau=sum(L)+10p-2=4p^2+6p-1`. The source exterior degree is `2p-2`; the
target exterior degree is `2p-3`. An S source has a low coefficient, and a K
source has a high coefficient. The original exterior differential removes an
element at zero-based increasing position `i` with sign `(-1)^i`.

First-low variables are indexed by `p-r`, `0<=r<=p-1`, and second-low
variables by `3p+u`, `0<=u<=p-2`. For an integral potential collection `f`
with `f_u(r)=0` for `r<=u`, define the source `P(f)` exactly as in the
committed hypothesis. Writing `R=u+v` and `F=f_u-f_v`, its two families are:

| Family | Omitted low variables | Coefficient offset | Normalized coefficient | Admissibility |
|---|---|---|---|---|
| alpha | `p-r,p-s,3p+u`, `r<s` | `p+u-r-s` | `alpha_u(r,s)=f_u(s)-f_u(r)` | `u<=r+s<=p+u-1` |
| beta | `p-r,3p+u,3p+v`, `u<v` | `3p+R-r` | `beta_r=F(r)-F(R+1)` if `R<=p-2`, otherwise `F(r)` | `max(0,R-p+2)<=r<=min(p-1,R)` |

Every exterior is the indicated low complement union `{6p,h}`. The actual
source coefficients are respectively `(-1)^(p+r+s+u) alpha_u(r,s)` and
`(-1)^(p+r+u+v) beta_r`. These signs come from complementing the increasing
low exterior and then putting the omitted first-low variables into increasing
endpoint order, as in EXP-059. Changing the value of the last high variable
does not change this ordering sign. The coefficient offset is the sum of the
three omitted low variables minus `4p`, so every label has total offset `tau`.
The admissibility bounds place the coefficient in `[1,p]` or `[3p,4p-2]`,
respectively. No inadmissible source label is used.

Define the signed K target basis element

```text
e(r;u,v) = (-1)^(p+r+u+v)
           [K,(L minus {p-r,3p+u,3p+v}) union {6p};
              11p-2+u+v-r],                 u<v.
```

It is used only when its coefficient is an original degree-two offset. Write
`x_uv=e(u+v;u,v)` when `u+v<=p-1`; its coefficient is `11p-2`. For oriented
notation put `y_uv=x_uv` if `u<v`, `y_uv=-x_vu` if `u>v`, and `y_uu=0`.
All instances below are admissible. This distinction is important:
`x_01=e(1;0,1)`, not `e(2;0,1)`.

The source asserted in the hypothesis is

```text
V_p=P(F_2+2F_1-4delta_03-4delta_02)+4Q_3-4Q_2,
Q_a=[K,(L minus {p-a,3p}) union {6p};8p-2-a],  a=2,3.
```

Each `Q_a` is a positive unit source. Its coefficient is in
`[6p,8p-2]`, its exterior has cardinality `2p-2`, and its total offset is
`sum(L)+2p+a+(8p-2-a)=tau`.

## 2. The complete D boundary of P(f) vanishes

Only two kinds of nonzero low multiplication occur: first-low times first-low
gives an A row, and mixed first/second-low multiplication gives a B row.
Second-low times second-low vanishes. Thus every D face of the displayed
sources occurs in one of the following equations, up to a common unit sign:

```text
alpha_u(r,s)-alpha_u(r,t)+alpha_u(s,t)=0,
    r<s<t,  u<=r+s+t<=p+u-1;

alpha_u(r,s)-alpha_v(r,s)+beta_r(u,v)-beta_s(u,v)=0,
    r<s, u<v, max(0,u+v-p+2)<=r+s<=u+v+1.
```

An inadmissible source coefficient is zero. In an A equation, a pair below
its lower admissibility bound has both potentials zero, while no pair can
exceed the equation's upper bound. Substitution of `f_u(s)-f_u(r)` therefore
telescopes, including truncated pairs.

For a B equation the alpha terms can also be replaced by their potential
differences: its upper bound `r+s<=u+v+1<=p+u-1` prevents upper truncation,
and a pair below a lower bound has both corresponding potential values zero.
The equation becomes

```text
beta_r-F(r)=beta_s-F(s).
```

If `R<=p-2`, the beta interval is `0,...,R`; its formula extends to `R+1`
as zero, because `F(R+1)-F(R+1)=0`. No endpoint in a B equation exceeds
`R+1`. The last display thus holds even at the absent endpoint `R+1`.
If `R>=p-1`, put `a=R-p+2`. Then `1<=a<=u`, and both potentials vanish
below `a`. The formula `beta_r=F(r)` consequently extends by zero to the
absent lower indices as well. This proves every B equation.

Hence `d_D P(f)=0` integrally for the potentials under consideration. This
argument proves a source construction, not an exhaustion or basis theorem
for the entire fixed-high sector.

## 3. Every K face of P(f)

The low exterior has cardinality `2p-4`, so removal of `6p` has positive
sign and removal of `h` has negative sign. All `6p` faces vanish:

```text
6p+[1,p] is contained in [6p,8p-2],
6p+[3p,4p-2] is contained in [8p,10p-2].
```

Both containing intervals are part of the original high set `H`, hence are
zero in the relevant degree-two quotient. The complete other-high face table
is particularly small:

| Source coefficient | Product with `h=8p-2` | Surviving case |
|---|---|---|
| alpha: `c` in `[1,p]` | `8p-2+c` | only `c=1`, giving C0 offset `8p-1` |
| beta: `3p+t`, `0<=t<=p-2` | `11p-2+t` | only `t=0`, giving C2 offset `11p-2` |

For alpha, `c>=2` lies in `[8p,10p-2]`. For beta, `t>=1` lies in
`[11p-1,12p-1]`. These are high intervals. Thus there are no other original
K rows, and no projection or discarded residual is involved.

The C0 row for an alpha coefficient can occur only when
`r+s=p+u-1`; its coefficient is the negative of the actual alpha source
coefficient. The C2 row for a beta coefficient occurs only at `r=R`, with
normalized coefficient

```text
F(R+1)-F(R),  if R<=p-2;
-F(p-1),     if R=p-1.
```

There is no diagonal C2 face if `R>p-1`. This includes the upper endpoint
which an unrestricted difference formula would otherwise miss.

## 4. Reflection-symmetric intervals give exact twice-edge boundaries

Fix three distinct indices `i,a,b` with `a<b` and
`i+a+b=p-2`. Let `T_i(a,b)` be the potential having only

```text
f_i(r)=1 for i+a+1<=r<=i+b.
```

The interval lies strictly inside `i<r<p-1`, so it satisfies the required
vanishing and contributes no top-endpoint term. Its endpoints sum to
`p+i-1`, so it is invariant under `r -> p+i-1-r`. Every possible C0 pair
has exactly this endpoint sum. Consequently `f_i(s)-f_i(r)=0` on all C0
pairs, including pairs outside the interval.

For C2, write `g(t)=f_i(i+t)`. By Section 3 the contribution is the oriented
edge sum with coefficient `g(v+1)-g(v)`. An interval indicator has precisely
two jumps: `+1` at `v=a` and `-1` at `v=b`. Therefore the full original
identity, not merely a quotient relation, is

```text
M P(T_i(a,b))=y_ia-y_ib.
```

This is an interval telescoping identity. A pair of reflected unit potentials
would instead give a relation among discrete differences and would not suffice
for the conclusion above.

For `j=1,2` put `k=p-2-j`. Since `p>=8`, one has `0<j<k<=p-2`, and

```text
F_j=T_0(j,k)-T_j(0,k)-T_k(0,j).
```

This is exactly the three-interval definition in the hypothesis. Applying the
preceding identity gives, with every sign shown,

```text
M P(F_j)
 = (x_0j-x_0k) - (-x_0j-x_jk) - (-x_0k+x_jk)
 = 2x_0j.
```

The auxiliary edge `x_jk` has `j+k=p-2`, so it is within, rather than
beyond, the diagonal domain. All three C0 contributions vanish individually.
There are no repeated indices or `r=0` interval endpoints, including at `p=8`.

## 5. The two exact short kernel-domain corrections

For `a=2,3`, put `delta_0a(0,a)=1` and all other potential values zero.
Section 3 gives the diagonal C2 boundary of `P(delta_0a)` as

```text
x_0,a-1 - x_0a.
```

Its only C0 pair is `(a,p-1-a)`. The endpoints are distinct and increasing
because `p-1-a>a` for these values and `p>=8`. The normalized alpha value
is `-1`, its source orientation sign is `(-1)^(2p-1)=-1`, and removal of
`h` contributes a final negative sign. The actual C0 coefficient is therefore
`-1` in both cases.

Now take the positive unit `Q_a` defined in Section 1. All of its faces are:

| Removed exterior variable | Surviving original face | Coefficient |
|---|---|---|
| first-low variable `a+1` | the same C0 row as `P(delta_0a)` | actual sign `(-1)^a` |
| second-low variable `3p+v`, `1<=v<=a` | `e(a;0,v)` | normalized coefficient `(-1)^a` |
| any other low variable | none: product lies in `H` | zero |
| high variable `6p` | none: product `14p-2-a` lies in `H` | zero |

For the first row, the omitted first-low variable is `p-a>a+1`, so `a+1`
has zero-based exterior position `a`. Its product is `8p-1`; every other
first-low product lies in one of the adjacent high intervals. For a second-low
face, the product is `11p-2-a+v`, which belongs to C2 precisely for
`1<=v<=a`. The exterior sign is `(-1)^(p+v-2)`; dividing by the signed
row convention `(-1)^(p+a+v)` gives `(-1)^a`. Finally, `14p-4` and
`14p-5` both lie in `[13p+1,14p-2]` when `p>=8`. Thus no high-free row or
unit filler is hidden in the calculation.

It follows that `J_a=P(delta_0a)+(-1)^a Q_a` cancels C0 exactly and has

```text
M J_a = x_0,a-1 + sum_{v=1}^{a-1} e(a;0,v).
```

In particular, with the names used in the declaration,

```text
B=J_3=P(delta_03)-Q_3,
M B=e(3;0,1)+x_02+e(3;0,2);

D=J_2=P(delta_02)+Q_2,
M D=x_01+e(2;0,1).
```

## 6. Exact vector identity for eta and its annihilator

Translating EXP-057's four raw rows into the signed target convention gives

```text
eta=-2e(3;0,2)-x_02-2e(2;0,1)-2e(3;0,1).
```

Substitution of the two identities in Section 5 yields the exact equality of
original target vectors

```text
eta=x_02+2x_01-2 M B-2 M D.
```

Combining it with `M P(F_j)=2x_0j` proves

```text
2eta = M(P(F_2)+2P(F_1)-4B-4D)
     = M(P(F_2+2F_1-4delta_03-4delta_02)+4Q_3-4Q_2)
     = M V_p.
```

All identities are over the integers and all boundary rows are included. The
`delta_02/Q_2` correction cannot be omitted. More precisely, omitting it from
the final formula gives `V_omit=V_p+4D`, with the nonzero exact residual

```text
M V_omit-2eta=4(x_01+e(2;0,1)).
```

The literal earliest paper proposal also used the opposite `F_1` coefficient:
`V_early=P(F_2-2F_1-4delta_03)+4Q_3=V_omit-4P(F_1)`. Its different
nonzero residual is

```text
M V_early-2eta=4(e(2;0,1)-x_01).
```

The two rows are distinct, so both failures hold uniformly for `p>=8`. These
are pre-declaration paper errors, not repairs made after an experimental failure.

EXP-057 established `M(s+q)=b_A+b_B+eta`. Consequently the explicit original
source `2s+2q-V_p` also satisfies

```text
M(2s+2q-V_p)=2(b_A+b_B).
```

## 7. What is proved, and what remains separate

Subject to the stated original presentation, the signed derivation proves for
every `p>=8` that the classes of `eta` and `b_A+b_B` in its full integral
cokernel have order dividing two. The construction passes from a fixed-high
potential sector through original K-source corrections to the previously
persisted endpoint target; it is not only a projected D-boundary calculation.

After base change to any commutative coefficient ring in which two is a unit,
the tracked class vanishes explicitly: `eta=M(V_p/2)`. The same statement for
`b_A+b_B` follows from the final identity of Section 6. This is a statement
about these particular classes, not about the whole connecting quotient.

It does not show that either class is nonzero, that its order is exactly two,
that another independent class exists, or that these classes exhaust the
quotient. Nor does it resolve the surviving Huneke-Wiegand research target or
any Jacobian-conjecture question. A class that vanishes is compatible with every
identity proved here.

The independent audit must still check the committed formulas against all
original faces at its declared finite parameters and reject the specified
mutations. Such checks challenge implementation and sign errors; they do not
replace the interval, truncation, and source proofs above. Source-model accuracy
and independent review of this derivation remain explicit scientific premises.
