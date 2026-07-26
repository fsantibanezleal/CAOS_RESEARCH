# EXP-098: Constructible certificate strata are strictly stronger

## Result

The prediction is **CONFIRMED**, with one correction to the prior strategy
wording.

A principal-open cover by localized global syzygies is not a more general
certificate than one global polynomial covector. If

\[
c_i^TM=0,\qquad c_i^Tb=1
\]

over \(R_{s_i}\), clear denominators to obtain global syzygies \(d_i\) with
\(d_i^Tb=s_i^{N_i}\). If the \(D(s_i)\) cover \(\operatorname{Spec}R\), then
the powers \(s_i^{N_i}\) generate the unit ideal. A polynomial linear
combination of the \(d_i\) is one global syzygy pairing to \(1\).

The genuinely stronger object is a **constructible rank stratification**:
generic open certificates followed by new syzygies computed after quotienting
by the residual closed-stratum ideal. Kernel formation need not commute with
that non-flat specialization.

## Exact separating control

Over \(R=\mathbb{Q}[x,y]\), set

\[
M=
\begin{pmatrix}
-y&0\\
x&0\\
0&x
\end{pmatrix},
\qquad
b=
\begin{pmatrix}
1\\0\\1
\end{pmatrix}.
\]

The system is inconsistent at every geometric parameter point:

- on \(V(x)\), the third equation is \(0=1\);
- on \(D(x)\), the second equation forces \(q_1=0\), contradicting
  \(-yq_1=1\).

An independent Gröbner calculation gives the unit basis \([1]\) for the total
solution ideal in \(\mathbb{Q}[x,y,q_1,q_2]\).

Every global left syzygy has the form

\[
c=h(x,y)(x,y,0)^T.
\]

Its pairing with \(b\) is \(xh\), so the global pairing ideal is the proper
ideal \((x)\). There is no global polynomial covector pairing to \(1\).

The constructible certificate has two pieces:

\[
D(x):\quad c_{\mathrm{gen}}=(1,y/x,0)^T,
\]

and

\[
V(x):\quad c_{\mathrm{sp}}=e_3.
\]

Both pair to \(1\) on their declared strata. The specialized syzygy \(e_3\)
cannot lift: globally, the second column of \(M\) imposes \(xc_3=0\), hence
\(c_3=0\) in the domain \(R\).

Equivalently,

\[
\operatorname{coker}M\cong (x,y)\oplus R/(x),
\]

and the class of \(b\) is \((x,1\bmod x)\). Its first component detects the
generic chart, while the torsion component detects the closed stratum but has
no map to the torsion-free ring \(R\).

## Adversarial validation

- Exact Gröbner elimination and the direct \(x=0\)/\(x\ne0\) dichotomy agree.
- The global syzygy equations and the cokernel presentation independently give
  pairing ideal \((x)\).
- A globally certified inconsistent control was detected immediately.
- An everywhere-consistent control retained its explicit solution and produced
  no nonzero pairing.
- The artifact reproduced byte-for-byte with SHA-256
  `9F885708784011A44259B26107367B3491CE1072CEAB19BF1BA2735CB1574671`.

The finite-presentation and base-change framing is consistent with the Stacks
Project sections on
[modules of finite presentation](https://stacks.math.columbia.edu/tag/01BM)
and [Fitting ideals](https://stacks.math.columbia.edu/tag/0C3C), including
the compatibility of Fitting ideals with base change. The separating example
and collapse lemma are proved directly here and do not depend on an imported
claim.

## Route decision

Replace the former target

> finite principal-open cover by localized certificates

with the recursive contract:

1. on the current stratum \(A=R/J\), compute left syzygies of \(M_A\);
2. form their pairing ideal \(I_J\);
3. certify the open complement of \(V(I_J)\) using its pairing generators;
4. replace \(J\) by \(\sqrt{J+I_J}\) and recompute syzygies after
   specialization;
5. stop successfully when the residual closed locus is empty;
6. stop unresolved when the ideal chain stabilizes with zero pairing.

This is strictly stronger than a global polynomial covector because new
specialization-only syzygies can appear on the residual closed strata.
Determinantal/Fitting rank strata provide an equivalent implementation surface
that may be cheaper than a full syzygy module.

The next GGHV experiment should first test a cheaper structural gate on the
already selected augmented minor: after base elimination, do all parameter
perturbation matrices preserve a common strict flag? If yes, the determinant
is identically constant without multivariate expansion. If not, use its
nonconstant pairing factors as the first residual closed strata.

## Scope and non-claims

- This result corrects and strengthens the certificate strategy.
- It does not yet apply the recursion to all 51 GGHV parameters.
- It does not exclude \((72,108)\), raise the degree floor, or decide \(JC(2)\).
- EXP-075 still excludes only global polynomial covectors of degree at most
  three. EXP-098 shows why specialization certificates remain logically open.

## How could this be wrong?

- A concrete implementation may fail to compute the required radicals or
  specialized syzygies at GGHV scale. That is a cost limitation, not a defect
  in the certificate contract.
- Scheme-theoretic multiplicities may require primary rather than radical
  strata for some lifting arguments. Pointwise exclusion only needs the
  radical cover, while a stronger scheme-level statement would retain those
  multiplicities.
- The selected GGHV matrix may have no useful low-complexity stratification.
  EXP-098 proves capability of the method, not tractability of that instance.
