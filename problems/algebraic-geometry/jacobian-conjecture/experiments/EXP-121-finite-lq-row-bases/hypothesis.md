# EXP-121 - Row bases selected on the finite \(L/Q\) residual schemes

## Question

Can maximal-minor row bases selected directly on the finite common residuals
left by EXP-120 close the \(L\) and \(Q\) components of the weighted-open
\(T_B\) chart?

Let \(\Delta_{LQ}\) be EXP-119's first exact alternative determinant and let
\[
I_L=(L,\Delta_{LQ}),\qquad I_Q=(Q,\Delta_{LQ})
\subset\mathbb Q[X,B],
\quad X=A^3.
\]
EXP-120 proves both ideals are zero-dimensional and that its \(G\)-basis
determinant contains \(LQ\). That determinant therefore cannot shrink either
residual. This experiment selects new bases on \(V(I_L)\) and \(V(I_Q)\)
instead.

## Motivation

The unresolved target is no longer a plane curve. EXP-118 closes the complete
\(d=0\) quotient boundary, EXP-119 makes each weighted-open intersection
finite, and EXP-120 closes the entire \(G\) component. The remaining work is
the exact finite chart cover on \(L\) and \(Q\).

A row basis chosen at a full-rank residual point is guaranteed to define a
minor nonzero at that point. It is not guaranteed to cover the other
residual points. The correct experiment is therefore:

1. select candidate bases at residual points over independent good primes;
2. reconstruct each candidate determinant exactly over \(\mathbb Q[A,B]\);
3. test the enlarged ideals over \(\mathbb Q[X,B]\);
4. retain several charts if one chart does not generate the unit ideal.

The modular stage is basis selection only. A component is closed only by an
exact characteristic-zero unit ideal.

## Premise dependencies

- [MV] EXP-115 supplies the complete 302-by-125 augmented matrix and exact
  row-basis extraction machinery.
- [MV] EXP-119 supplies the exact factorization of \(\Delta_{LQ}\) through
  \(X=A^3\).
- [MV] EXP-120 proves \(I_L\) and \(I_Q\) are zero-dimensional; for \(L\), a
  lexicographic \(B\)-eliminant has degree 108 and squarefree degree 73.
- [D] If
  \[
  (F,\Delta_{LQ},\Delta_1,\ldots,\Delta_k)=(1)
  \]
  in \(\mathbb Q[X,B]\), then the corresponding principal-open charts cover
  the complete selected residual on \(F=0\).

## Predictions

1. [C] Each of \(I_L\) and \(I_Q\) has at least one full-rank affine residual
   point over one of the first four good primes
   \(1009,1013,1019,1031\).
2. [C] A row basis selected on each residual has at most ten row replacements
   relative to the pinned selected basis.
3. [C] Each selected basis has a deterministic rational normalization whose
   largest cyclic SCC is at most 60.
4. [C] The exact determinants descend to a monomial in \(A\) times a
   polynomial in \(X=A^3,B\), with at most 10,000 monomials.
5. [C] At least one of the two component ideals becomes the unit ideal after
   adding its first residual-selected determinant.
6. [C] Any surviving common residual has strictly smaller squarefree
   elimination degree than the EXP-120 \(L\) degree 73 or a strictly smaller
   graded basis certificate on \(Q\).

## Method

1. Reconstruct the complete 302-by-125 system and EXP-119's exact invariant
   determinant.
2. Over each declared good prime, enumerate affine points satisfying
   \(F=\Delta_{LQ}=0\), with \(F=L,Q\). Retain only points at which the
   complete augmented matrix has row rank 125.
3. Extract deterministic independent row bases at those points. Deduplicate
   bases and rank them by row replacements and modular residual coverage.
4. For the strongest basis on each component, find the first exact rational
   normalization from a declared small grid. Compute the dependency graph,
   enforce the SCC gate, and factor the exact block determinants on \(d=1\).
5. Validate each determinant against five direct exact 125-by-125
   evaluations and reconstruct its invariant form under \(X=A^3\), retaining
   every coordinate factor.
6. Compute exact Groebner bases for the cumulative ideals
   \[
   (L,\Delta_{LQ},\Delta_{L,1},\ldots),\qquad
   (Q,\Delta_{LQ},\Delta_{Q,1},\ldots).
   \]
   Stop selecting charts for a component as soon as its reduced basis is
   \([1]\).
7. If an ideal remains nonunit, persist its zero-dimensional basis and any
   completed lexicographic elimination certificate. Do not infer a point
   count from a resultant or an incomplete FGLM conversion.

## What PASS and mixed outcomes prove

A unit ideal on both \(L\) and \(Q\), combined with EXP-120's \(G\) closure
and EXP-118's boundary cover, closes the complete three-parameter \(T_B\)
restriction.

A unit ideal on only one component closes only that component. A nonunit
zero-dimensional result is still a strict finite-residual reduction, not a
closure claim.

Neither outcome closes the 24-parameter core, the 51-parameter family,
\((72,108)\), the planar degree floor, or \(JC(2)\).

## Adversarial validation

- Require residual equations and matrix rank to hold at every modular
  selection point.
- Reproduce every selected modular determinant independently.
- Use at least two good primes for modular coverage evidence when available.
- Treat modular coverage only as a selection heuristic.
- Compare each SCC product with five direct exact determinants.
- Preserve the complete \(A\)-coordinate monomial when descending to \(X\).
- Accept component closure only from an exact \(\mathbb Q[X,B]\) basis
  equal to `[1]`.
- Retain rejected bases, failed assertions, and budget-stopped algebra.

## Compute budget and kill criteria

CPU-only. The modular selection stage has a 180-second gate per prime. Each
exact determinant has a six-minute gate, with 240 seconds for its largest
block. Stop before a cyclic block larger than 60 or an expanded determinant
above 10,000 monomials. Each exact component-ideal calculation has a
240-second gate; the total experiment has a 1,200-second gate.

Declared 2026-07-30 before implementation or machine search.
