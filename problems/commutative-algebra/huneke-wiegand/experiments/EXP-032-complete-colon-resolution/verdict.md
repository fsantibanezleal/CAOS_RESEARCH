# EXP-032 verdict - CONFIRMED

## Verdict

**CONFIRMED, with a precise scope correction.** For every integer `p>=4` and every field,
EXP-032 determines the complete ordinary graded Betti polynomial, hence every free-module rank
and shift, of the cubic-colon quotient

```text
D_p=P_p/(Q_p:f_p).
```

Put `c=2p-2`, `m=8p`, and

```text
lambda_(c,a)=c*binom(c,a)-binom(c,a+1)-binom(c,a-1).
```

Then

```text
B_(D_p)(x,z)
 =(1+xz)^m(1+sum_(a=1)^(c-1)lambda_(c,a)x^a z^(a+1)+x^c z^(c+2)).
```

The result does not give explicit differential matrices and therefore is not an explicit
resolution complex. It also does not give the full Betti table or minimal resolution of `C_p`.

## Consequences

- The low canonical idealization has only its linear strand and the terminal entry
  `beta_(c,c+2)=1`.
- Over `P_p`, the three nonzero rows are

  ```text
  beta_(i,i)   =binom(m,i),
  beta_(i,i+1) =sum_a lambda_(c,a)binom(m,i-a),
  beta_(i,i+2) =binom(m,i-c).
  ```

- `pd_(P_p)(D_p)=10p-2`, `reg_(P_p)(D_p)=2`, and the quotient is Gorenstein with final shift
  `10p`.
- Its total Betti rank is

  ```text
  2^(8p)((2p-4)2^(2p-2)+4).
  ```

- The first two low linear ranks recover the independent EXP-030 values
  `p(2p-3)` and `8p(p-1)(p-2)/3`.

## Why the theorem holds

EXP-030 identifies the low quotient as the canonical idealization of the `p`th Veronese ring.
It is two-dimensional Gorenstein with h-vector `(1,c,1)`, no linear equations, regularity two,
and a-invariant zero. Minimality and Gorenstein self-duality leave only a linear strand and the
single terminal socle entry. Coefficient extraction from

```text
(1+cz+z^2)(1-z)^c
```

then forces every linear rank. Tensoring with the minimal Koszul resolution on the `8p` disjoint
killed variables proves the full formula over `P_p`. These arguments commute with base change,
so there is no characteristic exception.

## Validation

- Canonical exact campaign: all 297 parameters `p=4,...,300`, with exact full row hashes and
  complete tables for `p=4,5,6`.
- Independent route: coefficient reconstruction without importing canonical code, matching every
  canonical row hash.
- Symbolic route: positivity factor, symmetry, first two ranks, rank sum, and endpoints, followed
  by exact arithmetic through `p=300`.
- Adversarial controls reject wrong codimension, omitted top shift, a reversed linear sign, and a
  spurious quadratic-row entry.

Aggregates:

```text
canonical    907438b249b98ca9ffef689b7edb9574cdb0044cc3dd4cb52de523129f7d37ee
independent  43635c8497dfe57904997326e983c7477e7320809cb2fee661c7933041f47b09
symbolic     f696390447a3ce20397d937aa73baebf23a3c5ae249d4ad1215ff48cb710a2ae
```

## Preserved failures

Two complete campaigns stopped at `p=230` and `p=223` under the declared 120-second budget and
remain `INCONCLUSIVE_BUDGET`. The successful recurrence implementation completed in 32.34 seconds.
The audit also caught a wrong post-Koszul Hilbert target and a `-0.0` canonical-serialization bug;
the symbolic layer rejected SymPy's incorrect generic-sum residual `c-1`. All final artifacts were
regenerated after correction.

## Research and publication decision

HWB-049 is complete for the graded Betti polynomial/free-module shape. The stronger task of
constructing differential matrices is separated from the proved claim. The result strengthens the
EXP-030 canonical-idealization theorem and satisfies the declared in-place manuscript v0.19 gate;
a separate paper is not yet justified. The strongest remaining path for `C_p` is to combine this
complete colon table with the cubic mapping cone and determine the comparison-map ranks against
the unresolved quadratic quotient `P_p/Q_p`.
