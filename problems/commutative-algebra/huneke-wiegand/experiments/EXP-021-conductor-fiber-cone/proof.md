# EXP-021 - symbolic proof

Fix `p>=4`, put `s=6p`, `q=4s=24p`, and abbreviate

```text
R=R_p, m=m_p, T=T_p,
G=gr_T(R), C=F(T), x=(t^q)^*.
```

## 1. The exact square identity

The EXP-013 value blocks for `T`, together with the EXP-009 blocks for `m=Gamma_p-{0}`, give by
ordinary Minkowski addition

```text
v(mT)=(8s+C_p) union [9s,13s-2] union [13s,infinity).
```

Here `C_p=[0,2p] union [3p,5p-2]`. The finite block calculation begins with

```text
(4s+A_p)+(4s+A_p)=8s+(A_p+A_p),
A_p+A_p=C_p union [6p,8p-4],
```

where the last interval already lies at level at least `9s`; adding the remaining level-five,
level-six, and stable blocks fills every ring value from `9s` onward. The unique missing integer
`13s-1` remains missing because it is the Frobenius number of `Gamma_p`. No sum can occur below
`8s`. This is exactly the closed EXP-016 profile for `v(T^2)`. Since monomial ideals in `R_p` are
determined by their value sets,

```text
T^2=mT.                                                     (1)
```

Associativity and commutativity now give, for every `n>=1`,

```text
T^(n+1)=T^(n-1)T^2=T^(n-1)mT=mT^n.                         (2)
```

Thus this is not merely an eventual reduction identity: it holds for every positive degree of the
fiber filtration.

## 2. The natural quotient is an algebra isomorphism

There is a natural graded-algebra surjection

```text
pi:G=direct-sum T^n/T^(n+1) -> C=direct-sum T^n/mT^n
```

because `T^(n+1)` is contained in `mT^n`. In degree zero its kernel is

```text
ker(pi_0)=m/T.
```

EXP-019 proves that this is exactly `H^0(G)`, a `p`-dimensional vector space. In every degree
`n>=1`, Equation (2) gives

```text
ker(pi_n)=mT^n/T^(n+1)=0.
```

Therefore `ker(pi)=H^0(G)` as a homogeneous ideal, and the first main conclusion is the natural
graded-algebra isomorphism

```text
G/H^0(G) isomorphic to C.                                  (3)
```

This makes the Cohen--Macaulay quotient from EXP-019 canonical: it is the conductor special fiber.

## 3. Cohen--Macaulay and Hilbert anatomy

EXP-019 proves that `G/H^0(G)` is Cohen--Macaulay, while EXP-020 gives its complete module over
`F=k[x]`. Transporting both statements through (3) yields

```text
C isomorphic to F
  direct-sum F(-1)^(10p-1)
  direct-sum F(-2)^(12p)
  direct-sum F(-3)^(2p-1)
  direct-sum F(-4).
```

Consequently `C` is a one-dimensional Cohen--Macaulay standard graded algebra, free of rank
`24p` over `F`. Its Hilbert series and Hilbert function are

```text
H_C(z)=(1+(10p-1)z+12pz^2+(2p-1)z^3+z^4)/(1-z),
HF_C=(1,10p,22p,24p-1,24p,24p,...).
```

The largest free shift is four. Hence the reduction number and regularity are four, the
`a`-invariant is three, and the multiplicity is `24p`.

## 4. Artinian reduction and its socle

Since `C` is free over `F`, `x` is regular. Put `B=C/xC`. For `n>=1`, a monomial basis is obtained
from

```text
B_n=T^n/(mT^n+t^qT^(n-1)).
```

After subtracting `nq` from each value, the exact block calculation gives bases `D_n`:

```text
D_0={0},

D_1=[1,p] union [3p,4p-2] union [6p,8p-2] union [8p,10p-2]
    union {10p} union [11p-1,12p-1] union [13p+1,14p-2]
    union [14p,15p-1] union {16p} union [17p-1,18p-1],

D_2=[p+1,2p] union [4p-1,5p-2] union {8p-1,10p-1}
    union [10p+1,11p-2] union [12p,13p] union {14p-1}
    union [15p,16p-1] union [16p+1,17p-2] union [18p,24p-1],

D_3=[2p+1,3p-1] union [5p-1,6p-2],
D_4={6p-1},
D_n=empty for n>=5.
```

Their cardinalities are

```text
(1,10p-1,12p,2p-1,1),
```

which independently recovers the Hilbert numerator.

Multiplication in `B` is addition of offsets when the target offset remains in the displayed
basis, and zero otherwise. The degree-two nonsocle offsets are precisely

```text
[p+1,2p] union [4p-1,5p-2].
```

Indeed, an element of the first interval can be moved into `[2p+1,3p-1]` by an element of
`[1,p]` (use `p-1` at the right endpoint), while adding `p` moves the second interval into
`[5p-1,6p-2]`. Direct interval addition shows that every other `D_2` offset kills all of `D_1`.
No element of `D_3` is socle: for `d` in its first block,
`6p-1-d` lies in `[3p,4p-2]`, and for `d` in its second block it lies in `[1,p]`; in both cases
the product is the unique element of `D_4`. Every element of `D_1` has a nonzero product in
`D_2`, while `D_4` is socle because `D_5` is zero. Thus

```text
Soc(B)_2 = span of D_2 minus ([p+1,2p] union [4p-1,5p-2]),
dim Soc(B)_2=10p,
Soc(B)_4=B_4, dim Soc(B)_4=1,
Soc(B)_n=0 otherwise.
```

The Cohen--Macaulay type of `C` is therefore `10p+1`. The socle occupies two degrees, so `C` is
not level; in particular it is not Gorenstein.

## 5. Role of computation

The campaign reconstructs the value profiles, products, natural kernels, Artinian bases, and
socle directly for all `p=4,...,300`. A separately encoded audit begins from the closed power
profiles and rebuilds six selected parameters while rehashing every campaign row. These finite
checks validate the implementations and adversarial controls. Sections 1--4, based on the
confirmed EXP-009/013/016--020 premises, prove the statements for every `p>=4`.
