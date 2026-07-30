# EXP-124 - Alternative chart on the EXP-123 rational graph

Declared 2026-07-30 before implementation or run.

## Question

On the principal open \(A S(A^3,B)\ne0\), does the complete 302-row system
contain an alternative 125-row minor that is nonzero generically on the
EXP-123 exceptional graph
\[
Y=-\frac{R(X,B)}{S(X,B)},\qquad X=A^3,\quad Y=A^2C?
\]

## Motivation and source-completeness

EXP-123 proves that the shared chart is
\[
\Delta_{\rm sh}=A^{87}(R(X,B)+Y S(X,B)),
\qquad \gcd(R,S)=1.
\]
It therefore reduces the selected exceptional locus, away from \(A=0\), to
one rational graph and the finite base locus \(V(R,S)\). The next
constructible step is an alternative minor selected on that graph, not a
generic four-variable determinant.

The complete GGHV source pass remains current. A fresh arXiv primary-source
sweep on 2026-07-30 found no paper deciding this internal augmented-matrix
graph. No external claim supports the verdict.

## Premise dependencies

1. [MV] EXP-111/112 give the complete 302-by-125 augmented system and exact
   coefficient pool.
2. [MV] EXP-121 gives the shared row basis and exact 23-term \(R(X,B)\).
3. [MV] EXP-123 gives the 18-term \(S(X,B)\), proves
   \(\gcd(R,S)=1\), and verifies the exact affine formula above.
4. [D] On \(A S\ne0\), setting
   \(C=-R(A^3,B)/(A^2S(A^3,B))\) parametrizes the selected chart's rational
   exceptional graph.
5. [H] The complete row pool supplies an alternative basis whose determinant
   does not vanish identically on this graph.

## Falsifiable predictions

1. At two good primes, deterministic graph points with \(A S\ne0\) have
   coefficient/augmented rank profile \(124/125\).
2. At least one graph-selected row basis differs from the EXP-121 shared
   basis and is full rank at graph points over both primes.
3. The best deterministic basis has largest cyclic block at most 60 for the
   \(A,B,C\) directions.
4. Its exact determinant restricts to a nonzero numerator on
   \(Y=-R/S\).
5. The restricted numerator is not a nonzero constant. A constant would be
   stronger and will be accepted as an immediate graph cover, but it is not
   predicted.

## Method

1. Load \(R,S\) from the EXP-123 primary artifact and reduce them modulo the
   good primes 1009 and 1013.
2. Enumerate deterministic nonzero \(A\) and \(B\), retain \(S(A^3,B)\ne0\),
   set \(Y=-R/S\), and recover \(C=Y/A^2\).
3. Evaluate the complete 302-by-125 matrix, record the coefficient/augmented
   rank profile, and extract deterministic independent row bases.
4. Score distinct bases by replacements from the shared basis and by the
   exact union-SCC size after a rational anchor is found. Retain the smallest
   cyclic candidate that appears over both primes when possible.
5. If the largest cyclic block is at most 60, compute the selected determinant
   exactly from all cyclic diagonal blocks in \(A,B,C\), under a
   timeout-isolated five-minute worker.
6. Verify the full determinant at four rational controls and reduce its
   monomials to invariant coordinates \(X=A^3\), \(Y=A^2C\) whenever one
   residue class exists.
7. If
   \[
   \Delta_{\rm alt}=A^v T(X,B,Y),
   \]
   let \(m=\deg_Y T\) and compute the exact graph numerator
   \[
   N(X,B)=S(X,B)^m T\!\left(X,B,-R(X,B)/S(X,B)\right).
   \]
   Persist its factorization, gcds with \(R,S\), degrees, and monomial count.
8. If symbolic reconstruction hits its gate, preserve the modular basis and
   checkpoint with an inconclusive verdict. Do not substitute a modular
   nonzero value for an exact graph claim.

## What a PASS proves and what a FAIL proves

A PASS of prediction 4 proves that the new minor is generically nonzero on
the rational graph. Its nonvanishing principal open removes a dense part of
that graph; the exact factors of \(N\), together with \(V(R,S)\), become the
only graph residuals for the next recursion.

It does not prove a complete graph cover unless \(N\) is a nonzero constant.
It does not address \(A=0\).

A FAIL of prediction 1 proves that the complete augmented system loses rank
on the sampled graph points, but only modulo the tested primes. A FAIL of
prediction 4 proves that the selected alternative basis is useless on the
whole graph; another basis or a specialization-only syzygy is required. A
budget stop is inconclusive.

No outcome closes the four-parameter restriction, the 24-parameter core, the
full 51-parameter family, \((72,108)\), the degree floor, or \(JC(2)\), unless
all residual strata are separately and exactly covered.

## Invariant-first note

The first gate is rank 125 at graph points. The second is exact SCC size.
These cheap invariants decide whether symbolic reconstruction is justified.
The graph substitution is performed only after exact characteristic-zero
reconstruction. No generic four-variable Groebner calculation is authorized.

## Adversarial controls

- Reproduce the EXP-123 \(R,S\), their gcd one, and the shared determinant's
  vanishing at every sampled graph point.
- Require the alternative basis to differ from the shared basis.
- Cross-check the selected basis at both good primes.
- Verify the exact determinant by direct 125-by-125 rational evaluations.
- Verify graph substitution both by denominator clearing and by exact
  evaluation at rational graph points whenever available.
- Preserve null, refuted, and stopped outcomes.

## Compute budget and kill criterion

CPU only. Modular selection budget: 60 seconds. Exact symbolic worker budget:
300 seconds. Total hard gate: 390 seconds. Checkpoints are written after each
prime and before the worker. If no cross-prime basis appears, use the best
single-prime candidate but label the selection evidence accordingly. If the
largest cyclic block exceeds 60 or the worker times out, stop with an
inconclusive verdict and retain the selected basis for a blockwise
interpolation round.

## Exploration moment

The constructible atlas is now treated as a graph-cover problem. Rather than
adding parameters to every existing chart, EXP-124 selects equations after
specializing to the graph where the current chart fails. This directly
implements the specialization-only syzygy mechanism identified in EXP-098.
If the graph numerator factors sparsely, those factors define the recursive
strata; if it is dense, the next invariant is its Newton polygon rather than
a raw Groebner basis.
