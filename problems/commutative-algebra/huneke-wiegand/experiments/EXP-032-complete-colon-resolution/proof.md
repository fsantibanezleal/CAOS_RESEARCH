# EXP-032 proof - complete graded Betti polynomial of the cubic-colon quotient

## Theorem

Let `p>=4`. Retain the notation of EXP-030, and put

```text
D_p=P_p/(Q_p:f_p),
c=2p-2,
m=8p.
```

Over the polynomial ring in the `2p` low variables, define

```text
lambda_(c,a)
  =c*binom(c,a)-binom(c,a+1)-binom(c,a-1),    1<=a<=c-1.       (1)
```

Then, over every field, the complete ordinary graded Betti polynomial of the low canonical
idealization `E_p` and of `D_p` over `P_p` is

```text
B_(E_p)(x,z)
  =1+sum_(a=1)^(c-1) lambda_(c,a)x^a z^(a+1)+x^c z^(c+2),     (2)

B_(D_p)(x,z)=(1+xz)^m B_(E_p)(x,z).                           (3)
```

Equivalently, the only nonzero low Betti numbers are

```text
beta_(0,0)=1,
beta_(a,a+1)=lambda_(c,a)                    (1<=a<=c-1),
beta_(c,c+2)=1.                                              (4)
```

Over `P_p`, with the convention that an out-of-range binomial coefficient is zero,

```text
beta_(i,i)   =binom(m,i),
beta_(i,i+1) =sum_(a=1)^(c-1) lambda_(c,a)binom(m,i-a),
beta_(i,i+2) =binom(m,i-c),                                  (5)
```

and every other entry vanishes. In particular,

```text
pd_(P_p)(D_p)=10p-2,                 reg_(P_p)(D_p)=2,         (6)

sum_(i,j) beta_(i,j)(E_p)=(c-2)2^c+4,
sum_(i,j) beta_(i,j)(D_p)=2^m((c-2)2^c+4).                   (7)
```

The theorem determines every free-module rank and shift in the minimal resolution. It does not
construct the differential matrices, and it does not determine the full resolution of `C_p`.

## 1. Shape forced by the canonical idealization

EXP-030 proves, integrally and hence over every field, that after killing the `m=8p` high
variables the colon quotient is

```text
E_p=V_p semidirect omega_(V_p),
V_p=k[s,t]^(p),
H_(E_p)(z)=(1+cz+z^2)/(1-z)^2.                               (8)
```

This standard graded algebra is Cohen--Macaulay and Gorenstein of dimension two. It is presented
over a polynomial ring `S_p` on `2p=c+2` variables, has no linear equations, and has h-vector
`(1,c,1)`. Consequently,

```text
codim_(S_p)(E_p)=c,
reg(E_p)=2,
a(E_p)=deg(1+cz+z^2)-dim(E_p)=0.                              (9)
```

Let `F` be the minimal graded `S_p`-resolution. Since the defining ideal has no linear forms and
every differential of `F` has entries in the homogeneous maximal ideal,

```text
beta_(i,j)(E_p)=0 when i>0 and j<=i.                          (10)
```

Regularity two gives vanishing when `j-i>2`. Thus only the rows `j-i=1,2` can occur away from
`beta_(0,0)`.

Gorenstein duality, (9), and the `c+2` ambient variables give final shift

```text
(c+2)+a(E_p)=c+2
```

and the symmetry

```text
beta_(i,j)(E_p)=beta_(c-i,c+2-j)(E_p).                        (11)
```

The row `j-i=2` is dual under (11) to the diagonal row. Equation (10) says the latter contains
only `beta_(0,0)=1`. Therefore the former contains only

```text
beta_(c,c+2)=1.                                               (12)
```

Every remaining nonzero entry is on the linear strand `beta_(a,a+1)`, and (11) also predicts its
symmetry under `a -> c-a`.

## 2. Hilbert numerator and the exact linear strand

The alternating Betti numerator is

```text
(1-z)^(c+2)H_(E_p)(z)=(1+cz+z^2)(1-z)^c.                     (13)
```

For `1<=a<=c-1`, the coefficient of `z^(a+1)` in (13) is

```text
(-1)^(a+1)binom(c,a+1)
  +c(-1)^a binom(c,a)
  +(-1)^(a-1)binom(c,a-1)
=(-1)^a lambda_(c,a).                                        (14)
```

By the shape proved in Section 1, the only Betti contribution to this coefficient is
`(-1)^a beta_(a,a+1)`. Equations (1) and (4) follow. The apparently silent degrees one and `c+1`
cancel in (13), while its constant and degree-`c+2` coefficients give the two endpoints in (4).

The alternative factorization

```text
lambda_(c,a)
 =binom(c,a)*a(c-a)(c+2)/((a+1)(c-a+1))                      (15)
```

proves strict positivity for `1<=a<=c-1`; the original integral formula proves integrality.
It also makes the symmetry in (11) transparent. The first two entries recover the coefficients
already used in EXP-030:

```text
lambda_(c,1)=p(2p-3),
lambda_(c,2)=8p(p-1)(p-2)/3.                                 (16)
```

Finally, separating the endpoint terms in the binomial sums gives

```text
sum_(a=1)^(c-1) lambda_(c,a)
 =c(2^c-2)-(2^c-1-c)-(2^c-c-1)
 =(c-2)2^c+2.                                                (17)
```

Adding the two endpoint ranks proves the low formula in (7).

## 3. The high-variable Koszul factor

Write `P_p=S_p tensor_k T_p`, where `T_p` is the polynomial ring in the `m=8p` high variables.
The complete-colon theorem of EXP-030 gives

```text
D_p=E_p tensor_k T_p/(all high variables).                    (18)
```

Tensor the minimal `S_p`-resolution of `E_p` with the Koszul resolution of the residue field over
`T_p`. The variables are disjoint, so the tensor complex is exact. Every differential entry lies
in the homogeneous maximal ideal of `P_p`, so the tensor resolution is minimal. Its Betti
polynomial is the product of (2) with the Koszul polynomial `(1+xz)^m`. This proves (3) and the
three convolution rows in (5).

The top homological degree is `c+m=10p-2`; the highest offset is two. This proves (6). Evaluation
at `x=z=1` multiplies the low total rank by `2^m`, proving the second identity in (7). The formula
also exhibits the full Gorenstein symmetry with final shift `c+m+2=10p`.

## 4. Exact validation and corrections

The canonical route freezes and verifies the EXP-030 proof and verdict hashes before computing.
For every `p=4,...,300`, it checks positivity, low and full Hilbert reconstruction, Gorenstein
symmetry, the known first two coefficients, projective dimension, regularity, total ranks, and
four corrupted controls. Literal Koszul convolution is retained through `p=12`; larger rows use
the equivalent Vandermonde coefficient form. Exact complete tables are stored for `p=4,5,6`.

The independent route imports no canonical code. It reads the linear ranks directly from the
alternating coefficients of (13), reconstructs the full row after removing the diagonal and
quadratic-row contributions, and matches every stored canonical row hash. The symbolic route
checks (15)--(17), symmetry, endpoints, and the EXP-030 coefficients, followed by exact arithmetic
through `p=300`.

The aggregates are

```text
canonical    907438b249b98ca9ffef689b7edb9574cdb0044cc3dd4cb52de523129f7d37ee
independent  43635c8497dfe57904997326e983c7477e7320809cb2fee661c7933041f47b09
symbolic     f696390447a3ce20397d937aa73baebf23a3c5ae249d4ad1215ff48cb710a2ae
```

Three validation corrections are material:

1. The first smoke target incorrectly replaced the low h-vector coefficient `c` by the full
   ambient codimension after adjoining the killed variables. The tensor table rejected it.
2. Literal convolution and the first Vandermonde implementation reached only `p=230` and `p=223`
   within 120 seconds. Both `INCONCLUSIVE_BUDGET` artifacts are preserved. Precomputed binomial
   rows reduced the successful canonical run to 32.34 seconds.
3. The independent byte-level audit rejected canonical `-0.0` values caused by a negative Python
   exponent times a zero out-of-range coefficient. The canonical generator was made integer-only
   and rerun from scratch. A direct symbolic summation that returned a false residual `c-1` was
   likewise rejected in favor of the explicit binomial-theorem calculation in (17).

These corrections carry no theorem evidence; the three final PASS artifacts were generated only
after their causes were removed.

## 5. Evidence hashes and trust boundary

| file | SHA-256 |
|---|---|
| `run.py` | `274c40e9e3b1f5182a16de075bf540ece926d5433d04ef828cac631378e40a5c` |
| `audit.py` | `0f91ab102bde540efb347fc0c0492f79585e3f4f64db516686dc05fc5eadb209` |
| `symbolic_certificate.py` | `5f067ffff47b6ae08bf345f13887bb97fb11d42c96f2b44f374dba03f9c2efec` |
| `artifacts/results.json` | `81e70a5d86d7e0c2965d1c49699a511b601540e94f16456cc3a12dbdbcfa5ac2` |
| `artifacts/audit.json` | `77469a5ac1ff8a957b2f33bb8b23107bc82d71db84c000be41b6cf1440894900` |
| `artifacts/symbolic-certificate.json` | `ae3ced1a234517adafd171df18a6c7a9f127cbbff13c7ad74954b55ac39ff31c` |

The finite campaigns validate the formulas, endpoint logic, and independent implementations.
The all-parameter, all-field theorem rests on the EXP-030 canonical-idealization theorem, standard
graded Gorenstein self-duality, the Hilbert-numerator coefficient extraction, and the minimal
Koszul tensor argument. No solver or floating-point inference is used. A flaw in the EXP-030
identification would propagate here; that premise is frozen and explicitly hashed.
