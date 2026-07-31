# Finite-scheme and cross-section lens - 2026-07-31

## Question

After EXP-125--127 reduce the three positive-dimensional graph components
to finite divisors, what is the strongest exact continuation: construct new
maximal minors, expand algebraic points, or reuse the existing sections in a
finite quotient algebra?

## Primary-source refresh

1. Guccione--Guccione--Valqui, *A system of polynomial equations related to
   the Jacobian Conjecture*, arXiv:1406.0886, Corollary 2.4, proves finiteness
   of the solution set of its associated system under the hypotheses of
   Theorem 2.3:
   <https://arxiv.org/abs/1406.0886>.
2. Guccione--Guccione--Horruitiner--Valqui, arXiv:2204.14178, combines the
   polynomial-system and Newton/intersection techniques and leaves the
   relevant \((72,108)\) case open:
   <https://arxiv.org/abs/2204.14178>.
3. Border-basis and quotient-algebra methods encode a zero-dimensional ideal
   by finite commuting multiplication matrices; see Kriegl, *Module Border
   Bases*, arXiv:1302.6383:
   <https://arxiv.org/abs/1302.6383>.
4. Braun--Pokutta, *Border bases and order ideals*, arXiv:0912.1502, records
   the term-order-independent finite quotient-algebra viewpoint:
   <https://arxiv.org/abs/0912.1502>.

The first source does not automatically identify its zero-dimensional system
with the present GGHV coefficient chart. That applicability bridge remains a
separate obligation. The reusable point is structural: once the local
experiment has independently proved finiteness, multiplication and unit
tests in its quotient algebra are the natural exact language.

## New view

Let the retained projected ledgers be
\[
 L_3=Q_9Q_{15},\qquad L_6=Q_{18}Q_{30},\qquad
 L_7=E_3E_9E_{18}.
\]
Instead of expanding their algebraic roots, work in
\[
 \mathcal A=\mathbb Q[B]/(L_3L_6L_7).
\]
If the seven irreducible factors are pairwise coprime, the Chinese remainder
theorem decomposes \(\mathcal A\) into seven exact number-algebra blocks.
A determinant section covers a block precisely when its restriction is a
unit there; equivalently, its multiplication matrix has nonzero determinant,
or its norm is coprime to the block polynomial.

This makes the existing two sections more valuable than a new random minor:

- \(h_{36}\), reconstructed in EXP-125 and reused in EXP-126, generated the
  finite divisors on \(F_3,F_6\) but has not been tested on the retained
  \(F_7\) blocks;
- \(h_7\), reconstructed in EXP-127, generated the finite divisor on
  \(F_7\) but has not been tested on the retained \(F_3,F_6\) blocks.

Their cross-restrictions can therefore close the ledger without any new
125-by-125 determinant.

## Ranked approaches

1. **P0 - cross-section unit tests in the finite quotient algebra.** Compute
   exact norms and gcds of \(h_7\) on \(F_3,F_6\), and of \(h_{36}\) on
   \(F_7\). This is the cheapest decision-bearing invariant.
2. **P1 - simultaneous minor selection in CRT blocks.** Only if a cross-gcd
   is nonconstant, select another persisted row basis directly on the
   surviving block algebra.
3. **P2 - finite base locus \(V(R,S)\).** Build its quotient algebra and test
   determinant units separately; do not contaminate the \(S\ne0\) chart.
4. **P3 - \(A=0\) boundary.** Reconstruct the specialized module and its
   structural kernels as an independent divisor experiment.
5. **P4 - original GGV zero-dimensional system.** Audit whether the present
   reduced chart maps into the 2014 system with all hypotheses preserved.
   This is conceptually strong but currently lacks the explicit bridge.

Generic Groebner elimination, algebraic-root expansion, modular-only point
coverage, and further coefficient slices remain demoted.

## Decision

Run EXP-128 as cross-section quotient-algebra closure. A unit gcd closes the
corresponding retained divisor exactly. A nonunit gcd becomes the next finite
block, with no negative inference beyond that block.
