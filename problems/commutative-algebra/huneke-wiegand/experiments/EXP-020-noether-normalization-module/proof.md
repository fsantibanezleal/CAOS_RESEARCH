# EXP-020 - symbolic proof

Fix `p>=4`, put `s=6p`, and write

```text
G=gr_(T_p)(R_p),
F=k[x],  x=(t^(4s))^*.
```

The variable `x` has degree one. All module isomorphisms below are graded `F`-module
isomorphisms.

## 1. Finite module and complete torsion

EXP-017 proves that `t^(4s)R_p` is a reduction of `T_p` with reduction number four. Therefore
multiplication by `x` maps `G_n` onto `G_(n+1)` for every `n>=4`. It follows that `G` is a finite
graded module over the polynomial ring `F=k[x]`.

Because `G/xG` has finite length, the radical of `xG` is the homogeneous maximal ideal of `G`.
Every homogeneous annihilator in `k[x]` is a scalar multiple of a power of `x`. Consequently the
`F`-torsion submodule of `G` is exactly its zeroth local cohomology. EXP-019 proves

```text
tors_F(G)=H^0(G) isomorphic to k^p isomorphic to (F/(x))^p,
```

with every generator in degree zero. In particular, all torsion elementary divisors have exponent
one; there is no hidden `F/(x^c)` summand with `c>1`.

## 2. Free quotient and its shifts

Set `C=G/H^0(G)`. This is a finite torsion-free module over the principal ideal domain `F`, so it
is free. The graded form of the structure theorem gives

```text
C isomorphic to direct-sum_d F(-d)^(alpha_d)
```

for uniquely determined nonnegative integers `alpha_d`. EXP-019 gives its Hilbert series:

```text
H_C(z)=(1+(10p-1)z+12pz^2+(2p-1)z^3+z^4)/(1-z).
```

Since `H_(F(-d))(z)=z^d/(1-z)`, comparison of numerators yields

```text
alpha_0=1,
alpha_1=10p-1,
alpha_2=12p,
alpha_3=2p-1,
alpha_4=1,
alpha_d=0 otherwise.
```

The quotient `C` is free, hence projective, so the exact sequence

```text
0 -> H^0(G) -> G -> C -> 0
```

splits in the graded category after choosing homogeneous lifts of a free basis. Thus

```text
G isomorphic to
  (F/(x))^p
  direct-sum F
  direct-sum F(-1)^(10p-1)
  direct-sum F(-2)^(12p)
  direct-sum F(-3)^(2p-1)
  direct-sum F(-4).
```

This argument uses the general Noether-normalization module viewpoint developed by Cortadellas
Benitez and Zarzuela, but the family-specific decomposition follows directly from EXP-017--019.
No maximal-ideal-specific Apery formula is imported into the conductor filtration.

## 3. Minimal resolution and homological invariants

Resolve each copy of `F/(x)` by multiplication by `x` and leave the free summands unchanged. This
gives the minimal graded resolution

```text
0 -> F(-1)^p ->
     F^(p+1) direct-sum F(-1)^(10p-1) direct-sum F(-2)^(12p)
     direct-sum F(-3)^(2p-1) direct-sum F(-4)
   -> G -> 0.
```

The first map is diagonal multiplication by `x` into the `p` torsion generators. It is minimal
because all of its entries lie in `(x)`. Hence the only nonzero graded Betti numbers are

```text
beta_(0,0)=p+1,
beta_(0,1)=10p-1,
beta_(0,2)=12p,
beta_(0,3)=2p-1,
beta_(0,4)=1,
beta_(1,1)=p.
```

Since `p>0`, the torsion is nonzero and the projective dimension over `F` is exactly one. The
resolution gives

```text
reg_F(G)=max{j-i: beta_(i,j) is nonzero}=4.
```

Finite-length torsion has no first local cohomology, so `H^1(G)=H^1(C)`. The top degree of
`H^1(F(-d))` is `d-1`; the largest free shift is four. Therefore the top-local-cohomology
`a`-invariant is

```text
a(G)=end H^1(G)=3.
```

## 4. Minimal-reduction section and exact defect

Modulo `x`, every cyclic summand contributes one `k`-dimension. The free rank is

```text
1+(10p-1)+12p+(2p-1)+1=24p=e0(T_p),
```

and the torsion contributes `p=I(G)`. Hence

```text
length(G/xG)=25p=e0(T_p)+I(G).
```

The excess of the parameter section over multiplicity is therefore exactly the complete
Buchsbaum defect. Combining earlier exact formulas also gives, within this family,

```text
I(G)=e0(T_p)/24=e1(T_p)/39=length(R_p/T_p)-1=p.
```

## 5. Independent exact reconstruction

For each residue modulo `4s=24p`, let `w_(n,r)` be the least value of `T_p^n` in that residue.
Since `t^(4s)T_p^n` is contained in `T_p^(n+1)`, every step

```text
w_(n+1,r)-w_(n,r)
```

is either zero or `4s`. A run of `c` consecutive `4s` steps followed by a zero step gives
`F/(x^c)` generated at the run's starting degree; a final infinite run gives a free summand at
its starting degree. EXP-017 supplies the stable final run from degree four onward.

The exact campaign constructs the power profiles recursively and decomposes all `24p` columns.
The audit instead uses the closed EXP-017 formulas for `R_p,T_p,...,T_p^5`. Both recover exactly
the cyclic decomposition above. This finite reconstruction supports the implementation; Sections
1--4 are the proof for every `p>=4`.
