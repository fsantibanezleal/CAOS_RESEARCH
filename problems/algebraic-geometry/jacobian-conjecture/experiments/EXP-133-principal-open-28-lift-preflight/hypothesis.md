# EXP-133 hypothesis - principal-open `(2,8)` lift preflight

Declared: 2026-08-01

## Question

After adjoining `T = epsilon_(2,8)`, can the accepted `A != 0,d=1`
maximal-minor atlas from EXP-123/124/129/130 be lifted by treating `T` as a
univariate deformation over the already certified rational graph and finite
base algebras, rather than expanding a new determinant in `A,B,C,T`?

For a persisted 125-row section write

`M(A,B,C,T) = M(A,B,C,0) + T D_(2,8)`.

At every invertible control, normalize by `K=M(A,B,C,0)^(-1)D_(2,8)` and
factor `det(I+T K)` through the exact or modular strongly connected components
of `K`. Acyclic vertices contribute one. This is the first invariant and cost
gate before any quotient-algebra reconstruction.

## Primary-source and premise gate

- EXP-123/124/129/130 certify the complete `A != 0` sector only at `T=0`.
- EXP-132 closes only the direct `A=0,d=1` transverse boundary; it does not
  make the principal-open lift free.
- The polynomial-matrix Smith-form criteria of Lu--Ruan--Wang--Xiao
  (arXiv:2605.09286) motivate reduced determinantal divisors, but their
  structured highest-divisor hypothesis has not been proved for this matrix.
  The Fitting/SCC route is therefore the operative method; Smith/Popov form is
  conditional follow-up only if a positive-dimensional residual survives.

## Falsifiable predictions

1. At two independent primes, every persisted section has the same `T` degree
   on two generic rational-graph controls.
2. At least one accepted EXP-123/124/129/130 section is `T`-inert or affine on
   the generic graph.
3. For every tested section, the total cyclic support of the normalized
   `(2,8)` operator is at most 45 vertices; otherwise direct symbolic
   reconstruction is retired for that section.
4. The pair of graph-covering sections does not acquire a common nonconstant
   `T` factor at the sampled graph controls. A confirmed common factor would
   redirect immediately to modular residual row selection.

Prediction 1 is a stability check, not a proof of global degree. Predictions
2--4 decide the next exact worker.

## Controls

- Rebuild the original 302-by-125 augmented matrix and the `(2,8)` direction
  from the bracket equations.
- Load row bases only from accepted EXP-123, EXP-124, EXP-129, and EXP-130
  artifacts; record their source SHA-256 hashes.
- Generate controls on the exact EXP-123 graph
  `R(A^3,B)+A^2 C S(A^3,B)=0`, rejecting `A*S=0` modulo the test prime.
- Require the `T=0` selected matrices to have full rank 125.
- Repeat at primes 1009 and 1153 and at two graph controls per prime.

## Budget and kill criteria

- Preflight budget: 120 seconds; hard gate: 300 seconds.
- Never expand a generic four-variable 125-by-125 determinant.
- Work componentwise. Stop any component whose determinant sampling exceeds
  60 seconds and persist the component/profile that caused the stop.
- If cyclic support exceeds 45 on every persisted section, redirect to
  residual-specific row selection before exact reconstruction.

## What a pass or fail proves

A pass selects a bounded exact univariate-in-`T` worker on the already
certified graph/base algebras. It does not close the graph, base locus, or the
five-coefficient restriction. A fail is still informative: it retires blind
lifting of the existing atlas and selects new row bases directly on the
transverse residual.

No outcome here settles the transverse `d=0` quotient, the complete
five-coefficient restriction, the 24-parameter core, the 51-parameter family,
`(72,108)`, the planar floor, or JC(2).
