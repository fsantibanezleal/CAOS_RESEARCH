# EXP-033 proof - the cubic mapping cone is minimal

## Theorem

Let `p>=4`, let `P_p=k[X_a:a in G_p]`, and retain

```text
A_p=P_p/Q_p,
C_p=P_p/(Q_p,f_p),
D_p=P_p/(Q_p:f_p),
f_p=X_0^2X_(3p)-X_p^3.
```

Put

```text
c=2p-2,       m=8p,       N=10p,
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1).
```

Over every field,

```text
depth(A_p)=1,
pd_(P_p)(A_p)=N-1,
reg_(P_p)(A_p)=2.                                           (1)
```

The mapping cone of

```text
0 -> D_p(-3) --f_p--> A_p -> C_p -> 0                       (2)
```

is therefore minimal, and the complete ordinary graded Betti polynomials satisfy

```text
B_(C_p)(x,z)=B_(A_p)(x,z)+x z^3 B_(D_p)(x,z).               (3)
```

In particular, the two highest regularity strands of `C_p` are

```text
beta_(i,i+3)(C_p)
  =sum_(a=1)^(c-1) lambda_(c,a) binom(m,i-1-a),              (4)

beta_(i,i+4)(C_p)=binom(m,i-1-c),                            (5)
```

where out-of-range binomial coefficients are zero. The first strand in (4) is positive exactly
for `2<=i<=N-2`, and the second is positive exactly for

```text
2p-1=c+1 <= i <= c+m+1=N-1.                                 (6)
```

Their total ranks are

```text
sum_i beta_(i,i+3)=2^m((c-2)2^c+2),
sum_i beta_(i,i+4)=2^m.                                     (7)
```

Equation (3) removes every comparison-rank ambiguity from the cubic mapping cone. It does not
determine the two lower strands of `A_p`, so the complete Betti table of `C_p` remains open.

## 1. A colon intersection and pullback

Write

```text
L_p=Q_p:f_p.
```

EXP-030 proves both

```text
L_p=Q_p+(X_h:h in G_p and h>=6p)                             (8)
```

and that the image of `f_p` is a nonzerodivisor on `P_p/L_p=D_p`.

We first prove

```text
Q_p=(Q_p,f_p) intersect L_p.                                 (9)
```

The forward inclusion is immediate. Conversely, take `g` in the right side and write
`g=q+a f_p` with `q in Q_p`. Since `q` and `g` belong to `L_p`, so does `a f_p`. Regularity of
`f_p` modulo `L_p` gives `a in L_p=Q_p:f_p`, and hence `a f_p in Q_p`. Thus `g in Q_p`, proving
(9). This is the load-bearing use of the EXP-030 nonzerodivisor theorem; the analogous
intersection is false for an arbitrary ideal and element.

Put

```text
T_p=P_p/(L_p,f_p)=D_p/f_pD_p.
```

The standard intersection sequence from (9) is

```text
0 -> A_p -> C_p direct-sum D_p -> T_p -> 0,                  (10)
```

where the last map is the difference of the two quotient maps. Projecting the pullback onto
`D_p` gives

```text
0 -> K_p -> A_p -> D_p -> 0,                                (11)
K_p=ker(C_p -> T_p).
```

Indeed, the kernel before identifying it with a submodule of `C_p` is `L_p/Q_p`. Its map to
`C_p` is injective by (9), and its image is `(L_p+(Q_p,f_p))/(Q_p,f_p)`, which is exactly the
kernel defining `K_p`.

## 2. The high-variable kernel has regularity two

EXP-032 gives

```text
H_(D_p)(z)=(1+(2p-2)z+z^2)/(1-z)^2.                          (12)
```

Since `f_p` is `D_p`-regular of degree three,

```text
H_(T_p)(z)
 =(1-z^3)H_(D_p)(z)
 =(1+(2p-1)z+2p z^2+(2p-1)z^3+z^4)/(1-z).                  (13)
```

EXP-024 gives

```text
H_(C_p)(z)
 =(1+(10p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).                (14)
```

The exact quotient `C_p -> T_p` and (13)--(14) yield

```text
H_(K_p)(z)=(8p z+10p z^2)/(1-z).                            (15)
```

EXP-026 proves that `X_0` is regular on `C_p`: no leading generator in its flat grevlex
degeneration is divisible by `X_0`. It is therefore regular on the submodule `K_p`. Equation
(15) shows that `K_p` is nonzero of dimension one, so this regular element proves that `K_p` is
Cohen--Macaulay.

Taking the quotient by `X_0`,

```text
H_(K_p/X_0K_p)(z)=8p z+10p z^2.                             (16)
```

For a regular linear form on a Cohen--Macaulay graded module, regularity is unchanged by this
Artinian reduction. The last nonzero degree in (16) is two. Hence

```text
reg_(P_p)(K_p)=2.                                            (17)
```

The finite structural audit sees the same module directly. In degree one its offset basis is the
`8p` high variables. In every degree at least two its basis is the stable interval
`[6p,24p-1]`, of size `18p`; multiplication by `X_0` preserves each offset and is injective. This
enumeration checks (15)--(17) but is not needed for the all-parameter proof.

## 3. Depth and regularity of the quadratic quotient

The quotient `D_p` is two-dimensional Cohen--Macaulay of regularity two by EXP-030/032, while
`K_p` has depth one by Section 2. The depth lemma applied to (11), with
`depth(K_p)<depth(D_p)`, gives

```text
depth(A_p)=1.                                                (18)
```

The regularity inequality in the same exact sequence and (17) give

```text
reg(A_p)<=max(reg(K_p),reg(D_p))=2.                          (19)
```

The equality in (1), rather than just the upper bound, is also forced. From (11), (12), and (15),

```text
H_(A_p)(z)
 =[1+(N-2)z+(2p+1)z^2-Nz^3]/(1-z)^2.                       (20)
```

Auslander--Buchsbaum and (18) give `pd_(P_p)(A_p)=N-1`. Multiplying (20) by `(1-z)^N`, the
coefficient of `z^(N+1)` is `-N`, because `N=10p` is even. Under the bounds `pd=N-1` and
`reg<=2`, the only Betti number that can contribute there is

```text
(-1)^(N-1) beta_(N-1,N+1)(A_p).
```

Therefore

```text
beta_(N-1,N+1)(A_p)=N,                                      (21)
```

and `reg(A_p)=2`. This proves all of (1).

## 4. The grading gap makes the cone minimal

Let `F_D` and `F_A` be minimal graded resolutions. EXP-032 says that every summand of
`(F_D)_i` has shift `i`, `i+1`, or `i+2`. After the degree-three shift in (2), every source
summand in a lifted comparison map `F_D(-3) -> F_A` has shift at least `i+3` in homological
degree `i`.

Equation (1) says that every target summand in `(F_A)_i` has shift at most `i+2`. Thus each
homogeneous entry of the comparison map has strictly positive degree. There is no scalar entry,
so the cone has no cancellation and is minimal. In homological degree `i` its modules are

```text
(F_C)_i=(F_A)_i direct-sum (F_D)_(i-1)(-3).                  (22)
```

This proves (3), and it also proves directly that every map in (3) on `Tor(-,k)` is zero.

The `A_p` summand in (22) has regularity at most two. Hence the regularity-three and
regularity-four strands of `C_p` come entirely from, respectively, the linear and terminal rows
of `D_p`. Substitution of the EXP-032 formulas gives (4) and (5). Positivity of every
`lambda_(c,a)` and of the binomial coefficients gives the support in (6). Summing the convolution
and using

```text
sum_(a=1)^(c-1) lambda_(c,a)=(c-2)2^c+2
```

gives (7).

As consistency checks, (4) recovers

```text
beta_(2,5)=p(2p-3),
beta_(3,6)=8p(7p^2-12p+2)/3,
```

while (5) gives `beta_(3,7)=0`, `beta_(N-2,N+2)=8p`, and
`beta_(N-1,N+3)=1`, exactly the independently proved EXP-024 and EXP-028--031 anchors.

## 5. Reproducible validation

The deductive proof above carries the theorem. Exact computation validates every arithmetic
identity, premise boundary, and implementation.

- Canonical route: all 297 values `p=4,...,300` pass in 15.159 seconds. It checks the five Hilbert
  numerators, exact-sequence identity, depth/projective-dimension consequences, terminal
  coefficient, complete formulas (4)--(5), all overlapping prior anchors, and six adversarial
  mutations. Complete strands are stored for `p=4,5,6`.
- Independent route: all 297 coefficient arrays are reconstructed from the alternating Hilbert
  numerator without importing canonical functions. Every array hash and total agrees.
- Structural route: the eleven-block generator set, high-variable kernel, stable interval, and
  `X_0` action pass independently at `p=4,...,25,50,100,300`.
- Symbolic route: the section, kernel, and quadratic-quotient Hilbert identities, both known
  low-rank identities, the degree-six formula, and all endpoint identities simplify to zero.

Canonical aggregates:

```text
canonical    67bff9217c89f212916220e858ef5168abe2d64cdbd789488e0ce5f49204092a
independent  6593291efaf092333bc42972c2f05712a151efb46f3f52ed9d28afd329585a4c
symbolic     58ab24887c79c3c075fdefea1f38ff2e1c1ef539490f7f52359149ed2bb1a4c8
```

Three exact but incomplete implementations are preserved as `INCONCLUSIVE_BUDGET` non-evidence.
They stopped at `p=102`, `p=209`, and `p=267`. Each optimization retained the already generated
row hashes. The final implementation replaces repeated large-binomial evaluation with an exact
recurrence and closes the unchanged campaign.

## Evidence hashes and trust boundary

| file | SHA-256 |
|---|---|
| `run.py` | `5ea4a6068aac1d22d814362b8db8ad22a39145c72d104072fb80106f418e01db` |
| `audit.py` | `f6f00f16b997e72d7fbdfc3b329faccc8e67350b7c2b0854332241faea4842eb` |
| `symbolic_certificate.py` | `0da790c2e52d1cd8542922c5a4e9badfaf628f6b4ed5909a7acded355650c820` |
| `artifacts/results.json` | `2b6d450b42c0e98ba1272b513b969ce81608205830f6f59216fa58dea6e85eb5` |
| `artifacts/audit.json` | `c4f338787b8ec08d5b1d49024bed2516e8cc9115af77d796aed7e602b2553cd8` |
| `artifacts/symbolic-certificate.json` | `459a822ecfee028627aa1c8806eff486fc0ac0b82b4e80be538ed477f55ba037` |

The all-parameter result depends on the frozen EXP-023/024/026/030/032 theorems. Within that
boundary, Sections 1--4 use only ideal arithmetic, a regular element, the depth and regularity
lemmas, Auslander--Buchsbaum, and graded minimality. No solver, floating-point inference, or
finite extrapolation enters the proof.
