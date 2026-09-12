# EXP-002: strict short-interval stability gain

Declared: 2026-09-12, before computation. Device: CPU. Symbolic proof and certified example.

## Question and falsifiable prediction

For every fixed exponent $\theta$ with $c(\theta)>0$, can a finite stability defect improve
Wang's simple-critical proportion $c(\theta)$ by some positive amount? The proposed theorem
uses a finite Hilbert operator, the stability-enhanced rank-trace inequality, and the fact that
the optimized cosine kernel cannot vanish simultaneously at two nonnegative gaps and their sum.
A numerical illustration will target $\theta=3/4$ using only rational/certified constants.

## Source-complete premises

Inspect Wang arXiv:2609.07918v1 through its final optimization and references, Lamzouri v2's
finite Hilbert proof, and ainta's complete stability proof and pinching argument before running.
Wang's fixed-support pair-correlation result for $0<\lambda<\theta<1$ is an imported analytic
premise. Its hypotheses, weight removal, and order of limits must be preserved. The finite
stability lemma must be re-derived independently. No claim from an unreviewed higher-moment
repository is an input. EXP-001 owns the baseline constant brackets.

## Method and invariant first

Write $\Psi(t)=(t-1)^2$ on $[0,2]$ and $\Psi(t)=2t-3$ above 2. Derive
$S\ge2N-Q+\operatorname{tr}\Psi(G)$ for the simple-atom Gram matrix. Prove the kernel's
zero-addition obstruction algebraically, then obtain a positive minimum of the three-point
energy on a compact gap triangle. Derive a rigorous disjoint-block or shifted-block count.
Handle $\lambda\uparrow\theta$ by continuity after the large-height limit, never by applying
a theorem outside its support range. Independently inspect all constants and counting factors.

For a concrete example, use outward-rounded interval evaluation and exhaustive subdivision
or an independent analytic lower bound. Search parameters may be chosen within this declared
family; a certificate must cover the full compact domain, not samples. Preserve its domain,
threshold, exact parameters, node count, unresolved-cell count, and arithmetic implementation.

## PASS and FAIL

PASS requires a complete written proof with explicit dependence on imported theorems, an
independent adversarial audit, a valid concrete interval certificate, and a scoped novelty
search. A numerical PASS alone certifies only the finite inequality. Any missing analytic
transfer, incorrect counting factor, or counterexample blocks the claimed zeta extension.
The intended theorem improves a short-interval bound; it does not assert a global record,
prove RH, or improve the exponent where a positive bound first becomes available.

## Budget, checkpoints, and kill criterion

Initial arithmetic and invariant checks: under one minute. Interval illustration: ten-minute
budget, flushed progress and resumable pending-box checkpoint first smoke-tested on a tiny
domain. Maximum 2 million cells. Any unresolved cell, invalid enclosure, timeout, or nonzero
imaginary residue causes a non-confirmed verdict. No GPU is justified by this two-variable
certification task. The mathematical proof and novelty audit, not runtime, decide acceptance.
