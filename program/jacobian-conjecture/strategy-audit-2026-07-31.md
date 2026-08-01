# Jacobian strategy audit after EXP-130

Date: 2026-07-31. This audit supersedes the route ranking in the 2026-07-30
audit. It does not change the scope of any accepted experiment.

## Current bottleneck

EXP-124--129 cover the complete rational graph on (AS\ne0). EXP-130 proves
that the reduced 90-dimensional algebra of

\[
V(R,S)\cap D(X),\qquad X=A^3,
\]

is covered uniformly in (Y=A^2C). Consequently the declared
four-parameter restriction is covered on the complete principal open
(A\ne0). The only remaining stratum of this restriction is (A=0).

This is meaningful progress on one restriction, not a proof of the complete
24-parameter core, the 51-parameter GGHV family, the ((72,108)) case, the
planar degree floor, or (JC(2)).

## What EXP-130 changes

The finite-algebra viewpoint is validated. Generic ambient Groebner
elimination reached its declared gate; factorwise subresultants, CRT fields,
module sections, and exact Bezout identities gave a faster and stronger
certificate. The successful object was not a list of algebraic points but the
zeroth Fitting/maximal-minor ideal after base change to a finite coordinate
algebra.

That lesson should be retained, but the same normalization cannot be extended
through (A=0): both (X=A^3) and (Y=A^2C) collapse there. The next
experiment must return to the original specialized 302-by-125 augmented
matrix before division by (A).

## Ranked routes

| Rank | Route | Proof value now | Gate and decision |
|---|---|---|---|
| P0 | Direct (A=0) matrix rank stratification in ((B,C)) | can close the last boundary of the four-parameter restriction | specialize the original matrix first; compute generic rank and determinantal pivots before any elimination |
| P0-control | Module/Fitting presentation over each residual boundary algebra | converts positive-dimensional rank defects into exact finite quotient tests, as in EXP-130 | use only after direct rank profiling identifies the residual ideals |
| P1 | Smith/Popov-style polynomial-matrix compression over (mathbb Q(B)) or (mathbb Q(C)) | exposes invariant factors and may avoid enumerating maximal minors | accept only with denominator and exceptional-fibre ledger plus direct rank controls |
| P1-control | Two-prime modular rank atlas followed by characteristic-zero SCC reconstruction | selects affordable minors without treating modular evidence as proof | reuse the EXP-129/130 selection pipeline if the generic boundary rank is 125 |
| P2-conditional | Boundary-divisor transport for intersection 21 | could connect the reduced system back to original-pair Newton data | reopen only after the four-parameter restriction closes or if (A=0) stalls |
| P3-hold | Lee--Li inner-polynomial restrictions or Jelonek component geometry | potentially strong global viewpoints | no proved applicability bridge to this reduced bracket-(x^2) matrix; do not base a conclusion on them |
| retired | more graph/base-locus sampling or a larger generic Groebner timeout | cannot change the now-closed (A\ne0) sector | do not run |

## Alternative views worth testing

### 1. Boundary module, not boundary points

Let (M_0(B,C)) be the exact (A=0) augmented matrix. The correct question is
whether its maximal-minor ideal is the unit ideal in (mathbb Q[B,C]), after
removing only structural columns already justified by EXP-111. A compact
presentation of its cokernel can expose the support of the rank-defect module
without computing all maximal minors. This is the positive-dimensional
analogue of EXP-130's finite-algebra/Fitting calculation.

### 2. Polynomial-matrix invariant factors

If one variable is treated as a coefficient-field parameter, fraction-free
row/column reduction can expose invariant factors whose numerators define all
exceptional fibres. This can be much cheaper than a bivariate determinantal
ideal. The danger is denominator loss; every denominator zero must be split
off and checked directly.

### 3. Local chart gluing

Rather than seek one global minor, construct a finite atlas. Start from a
generic full-rank pivot, restrict its zero divisor, and recurse on that
divisor. This is the same geometric logic that closed the rational graph, now
applied directly on the (A=0) plane. A single-minor failure is not a rank
failure.

### 4. Global literature routes remain conditional

The 2026 primary-source refresh found useful surrounding structure but no
theorem that bypasses the missing transport: GGHV supplies the reduced
((72,108)) system; Lee--Li concerns inner polynomials of original Keller
pairs; Jelonek concerns components of bounded-degree constant-Jacobian map
spaces. Until an exact morphism or invariant-transport theorem is proved,
those routes organize hypotheses but cannot certify this matrix family.

## EXP-131 decision tree

1. Hash-check the accepted EXP-111/121/123 source matrices and specialize the
   original 302-by-125 system at (A=0), without dividing by (A).
2. Compute exact generic rank over (mathbb Q(B,C)). If it is below 125,
   record a genuine whole-boundary rank defect; do not infer a Jacobian
   counterexample without the upstream necessity bridge.
3. If the generic rank is 125, select a sparse pivot at two admissible primes,
   reconstruct its characteristic-zero determinant, and factor its divisor.
4. Split every denominator, coordinate axis, and repeated factor into a direct
   specialization test. Never cancel a boundary factor silently.
5. Recurse with alternative row bases on each residual curve. When a residual
   is zero-dimensional, switch to the EXP-130 quotient-algebra unit-ideal
   method.
6. Independently verify closure through a module/Fitting or polynomial-matrix
   invariant-factor computation.
7. Only if all (A=0) strata are covered may the four-parameter restriction be
   declared complete. That statement still does not settle ((72,108)) or
   (JC(2)).

## Reprioritization

EXP-131 is the sole P0 research computation. Do not spend compute on the
closed graph or base locus. After EXP-131, either assemble the complete
four-parameter restriction or isolate the smallest exact residual rank
stratum. The independent ([125,150]) source-frontier work remains valuable
but secondary; broad Newton, properness, and component-geometry routes remain
on hold pending an applicability bridge.

## EXP-131 resolution and next redirect

EXP-131 followed the decision tree and closed the direct \(A=0\) plane with
two exact \(C\)-independent maximal minors. Their squarefree \(B\)-divisors
have an explicit Bezout identity equal to one. Together with EXP-118 and
EXP-123/129/130, the complete declared four-coefficient restriction is now
closed.

The P0 target therefore moves transversely into the 24-parameter cyclic core.
EXP-132 should add \((2,8)\) first: EXP-122 records a linear anchor factor and
a size-35 union SCC, the smallest unused linear candidate. The correct object
is the joint exceptional ideal of several lifted sections, with EXP-131's
two-minor Bezout atlas retained as a boundary regression gate. Lee--Li,
Jelonek, and intersection-21 transport remain conditional until an explicit
applicability bridge is proved.
