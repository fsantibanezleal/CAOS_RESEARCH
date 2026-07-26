# EXP-098: Distinguish open chart covers from constructible certificate strata

## Question

Can localized left-syzygy certificates prove uniform inconsistency of a
polynomial family

\[
M(\varepsilon)q=b
\]

when no single global polynomial covector exists, and what exact form must such
a certificate cover take?

## Motivation

The strategy audit proposes replacing a single polynomial covector by a finite
chart cover. Before applying that route to the 51-parameter GGHV system, its
logical strength must be typed precisely.

If principal opens \(D(s_i)\) cover all of \(\operatorname{Spec}R\), and each
chart has a localized covector \(c_i\) satisfying

\[
c_i^TM=0,\qquad c_i^Tb=1,
\]

then denominators can be cleared. The resulting global syzygies pair with
powers of the \(s_i\). Since the \(D(s_i)\) cover, those powers generate the
unit ideal, and their linear combination is a single global polynomial
covector pairing to \(1\). A pure principal-open cover therefore does not
strictly generalize the global-covector target.

The potentially stronger mechanism is a constructible stratification. On a
closed rank-drop stratum, base change can create new syzygies that do not lift
to the parameter ring. Those specialization-only syzygies can certify the
residual stratum after generic open charts are removed.

## Falsifiable predictions

1. A finite principal-open cover by localized lifts collapses exactly to one
   global polynomial covector.
2. Over \(R=\mathbb{Q}[x,y]\), the family

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
   \end{pmatrix}
   \]

   is inconsistent at every geometric parameter point, but its global
   left-syzygy pairing ideal is only \((x)\), not the unit ideal.
3. The generic chart \(D(x)\) has a localized certificate pairing to \(1\).
   On the residual closed stratum \(V(x)\), the specialized syzygy \(e_3\)
   pairs to \(1\) and does not lift to a global syzygy over \(R\).
4. A recursive algorithm that alternates open certificates with specialization
   to the residual closed locus distinguishes the universally inconsistent
   control from both a globally certified control and a consistent control.

## Premise dependencies

- EXP-075 excludes global polynomial covectors only through parameter degree
  three. It does not exclude higher-degree covectors or constructible
  specialization certificates.
- EXP-097 closes direct resultant-degree transport but does not constrain the
  certificate module.
- The Stacks Project sections on finite presentations and Fitting ideals support
  the use of cokernel presentations, localization, base change, and
  determinantal rank strata. The collapse and the concrete control above are
  independently re-derived in this experiment.
- No claim is made that the toy presentation occurs inside the GGHV matrix.
  It tests the exact logical capability of the proposed method.

## What a PASS or FAIL proves

- A PASS proves that the strategy must use constructible rank strata, not a
  principal-open cover alone, if it is to be genuinely stronger than one global
  polynomial covector. It supplies an exact control and a recursive certificate
  contract for a later GGHV implementation.
- A FAIL of the universal inconsistency or non-lift claims refutes the proposed
  distinction and retires this formulation.
- Neither outcome excludes \((72,108)\), proves or disproves \(JC(2)\), or
  raises the planar degree floor.

## Method

Use exact SymPy polynomial arithmetic over \(\mathbb{Q}[x,y]\):

1. solve the global left-syzygy equations symbolically;
2. compute their pairing ideal with \(b\);
3. verify the \(D(x)\) localized certificate;
4. specialize modulo \((x)\), compute the enlarged kernel, and prove that
   \(e_3\) cannot lift;
5. verify universal inconsistency by the exhaustive dichotomy \(x=0\) or
   \(x\ne0\);
6. run globally certified and everywhere-consistent controls.

An independent direct equation check and a module-presentation check provide
the adversarial routes.

## Invariant-first note

The pairing ideal is the distinguishing invariant. Unit pairing means a global
certificate. A proper pairing ideal identifies the residual locus on which
kernel base change must be recomputed. No parameter sweep is needed.

## Compute budget and kill criterion

CPU only, exact arithmetic. Expected runtime below two seconds; budget 15
seconds. Stop on any failed identity or if the declared control matrix is not
universally inconsistent. A stopped or failed run establishes no claim about
the certificate route.

Declared 2026-07-26 before creating or running `run.py`.
