# EXP-123 - Symbolic \((2,9)\) lift of the shared chart

Declared 2026-07-30 before implementation or run.

## Question

On the normalized \(d=1\) four-parameter restriction
\[
\{(0,1),(0,5),(1,0),(2,9)\},
\]
is the EXP-121 shared-basis determinant affine in the new coefficient
\(C=\varepsilon_{(2,9)}\) over \(\mathbb Q[A,B]\)?

## Motivation

EXP-122 proves that no restored direction gives a free one-parameter lift.
It also isolates the eight directions \((2,j)\), \(2\leq j\leq9\), as a
coherent sparse class: each enlarges the fixed-\(d\) cyclic SCC but has a
linear determinant factor on the rational anchor line.

Direction \((2,9)\) is the strongest first target. On the EXP-121 basis it
has selected rank 53, normalized support 1319, and grows the cyclic block only
from 26 to 34. Its anchor-line factor is
\[
\det(I+C K_{(2,9)})=1+\frac{3}{544}C.
\]
It was determinant-inert on the pinned \(T_A\) chart in EXP-114, so it also
tests whether the observed chart complementarity can be exploited
constructibly.

## Premise dependencies

1. [MV] EXP-121 closes the complete three-parameter \(T_B\) restriction using
   a finite chart cover and provides the shared row basis used here.
2. [MV] EXP-122 reconstructs that basis at \((A,B,d)=(1,0,1)\), proves the
   \((2,9)\) union SCC has size 34, and gives the exact anchor-line factor
   \(1+3C/544\).
3. [MV] EXP-114 proves the pinned \(T_A\) determinant is independent of
   \((2,9)\). This is a comparison chart, not a coverage claim.
4. [H] The linearly active \((2,j)\) pattern persists over the symbolic
   \(A,B\) chart with low \(C\)-degree.

The primary-source status is unchanged from EXP-122. No external source
settles this internal determinant.

## Falsifiable predictions

1. The exact 34-block determinant at \(C=0\) reproduces the EXP-121
   shared-chart determinant up to the already persisted nonzero anchor scalar.
2. The exact determinant has degree one in \(C\).
3. The coefficient of \(C\) is nonzero and has a nonzero mixed \(A\) or \(B\)
   term, reproducing EXP-122's nonzero trace-pairing signal.
4. The coefficient of \(C\) and the \(C=0\) term have no common nonconstant
   factor in \(\mathbb Q[A,B]\).

## Method

1. Reconstruct the EXP-121 shared basis and exact normalized matrices at
   \((A,B,C,d)=(1,0,0,1)\).
2. Build the union graph of \((0,1),(0,5),(2,9)\), extract its 34-vertex cyclic
   block, and prove all remaining diagonal blocks contribute one.
3. Before a symbolic determinant, estimate the generic \(C\)-degree at
   deterministic \(A,B\) samples over two good primes. This is reconnaissance
   only and cannot support the verdict.
4. If both modular probes give degree at most four, compute
   \[
   \Delta(A,B,C)=
   \det\!\left(
   I+(A-1)K_{(0,1)}+B K_{(0,5)}+C K_{(2,9)}
   \right)
   \]
   exactly from the 34-block over \(\mathbb Q[A,B,C]\).
5. Verify:
   - \(\Delta(A,B,0)\) against the EXP-121 exact polynomial;
   - \(\Delta(1,0,C)=1+3C/544\);
   - the exact degree and monomial count in \(C\);
   - the gcd of \([C^0]\Delta\) and \([C^1]\Delta\) if the determinant is
     affine.
6. Independently evaluate the resulting polynomial against direct exact
   125-by-125 determinants at four rational \((A,B,C)\) controls.

## What a PASS proves and what a FAIL proves

A PASS of prediction 2 proves that this selected four-parameter chart has one
new affine exceptional graph over the \(A,B\)-plane, plus the coefficient-zero
stratum. Together with prediction 4, it proves that the two coefficient
polynomials share no divisorial component.

It does not prove a four-parameter chart cover. Alternative minors still have
to cover the affine exceptional graph and any coefficient-zero points.

A FAIL of prediction 2 proves that anchor-line linearity is a specialization
artifact. The next round must use the lowest exact \(C\)-coefficient
stratification rather than affine elimination. A budget stop is inconclusive
and triggers blockwise interpolation instead of a generic Groebner
calculation.

No outcome closes the 24-parameter core, the full 51-parameter family,
\((72,108)\), the planar degree floor, or \(JC(2)\).

## Invariant-first note

The generic modular \(C\)-degree and the exact 34-block are the cheap deciding
invariants. They test the affine premise before any ideal calculation. A
four-variable Groebner basis and the generic 24-variable determinant are
outside scope.

## Adversarial controls

- Reproduce the exact EXP-121 anchor determinant and \(C=0\) polynomial.
- Reproduce the EXP-122 size-34 union SCC and anchor-line factor.
- Use two modular degree probes before exact expansion.
- Check the exact result at four rational points through the original
  125-by-125 selected matrix.
- Persist a stopped symbolic attempt and declare the verdict inconclusive if
  the compute gate is reached.

## Compute budget and kill criterion

CPU only. The modular preflight budget is 30 seconds. The exact symbolic
determinant budget is five minutes, with flushed stage output. The total hard
gate is six minutes. If either modular probe has \(C\)-degree above four, or
if the exact determinant reaches five minutes without completion, stop and
persist the probe/checkpoint. No ideal computation is authorized after such a
stop.

## Exploration moment

EXP-122 suggests a chart atlas rather than a universal-basis strategy:
\((2,9)\) is invisible on the pinned \(T_A\) determinant but linearly visible
on the shared \(L/Q\) basis. EXP-123 tests the first transition function
between those behaviors. If affine, the next object is not a generic
four-variable zero set but one explicit rational exceptional graph; if
non-affine, its coefficient stratification provides the recursion tree.
