# EXP-122 - Shared-basis core lift audit

Declared 2026-07-30 before implementation or run.

## Question

Does the 125-row basis selected independently on the finite \(L\) and \(Q\)
residual schemes in EXP-121 expose any direction in which the closed
three-parameter \(T_B\) restriction can plausibly lift to a
higher-dimensional constructible stratum?

This experiment is an exact activity and prioritization audit. It does not
claim that tangent activity, graph support, or an invertible anchor line alone
proves a higher-dimensional chart cover.

## Motivation and source-completeness

EXP-112 compressed the pinned chart to a 36-column cyclic block with 24 active
core directions. EXP-113 showed that \(T_B=\{(0,1),(0,5),(1,0)\}\) generates
that pinned core's connectivity. EXP-121 then found a different shared
125-row basis whose \(T_B\) graph has largest cyclic block 26 and whose exact
determinant closes the remaining finite \(L\) and \(Q\) residual schemes.

The complete primary-source pass for the GGHV family is already persisted in
the problem dossiers. A dated arXiv sweep on 2026-07-30 found no source that
settles the internal 24-direction activity of this repository-specific
augmented matrix. The current question is therefore decided from the exact
persisted matrix construction, not from an external claim.

## Premise dependencies

1. [MV] The complete augmented system is 302 by 125 after removing the
   structural constant \(Q\)-column. Supported by EXP-111 and EXP-112.
2. [MV] The pinned determinant has exactly 24 cyclic-core directions.
   Supported by EXP-112.
3. [MV] \(T_B=\{(0,1),(0,5),(1,0)\}\) is a deletion-minimal
   full-connectivity triple for the pinned 36-core. Supported by EXP-113.
4. [MV] EXP-121 selected the same 125-row basis independently on finite
   \(L\) and \(Q\) residual schemes, and this basis is invertible at the
   rational anchor \((A,B,d)=(1,0,1)\). Supported by EXP-121.
5. [H] Exact normalized tangent and mixed-cycle data at that anchor will
   distinguish promising lift directions from directions that should be
   deferred.

## Falsifiable predictions

1. Reconstructing the EXP-121 shared rows and rational anchor reproduces the
   exact nonzero determinant and the largest \(T_B\) cyclic block of size 26.
2. Among the 21 restored core directions outside \(T_B\), at least one is
   determinant-inert on its one-parameter anchor line:
   \[
   \det(M_\ast+tD_i)=\det(M_\ast).
   \]
3. At least one restored direction has support internal to the existing
   26-block, and at least one enlarges a cyclic component beyond size 26.
4. At least one restored direction has a nonzero exact first-order or
   pairwise mixed determinant coefficient with a \(T_B\) direction at the
   anchor.

Prediction 1 is a mandatory regression. Predictions 2 through 4 may be
refuted independently and will be reported without reinterpretation.

## Method

1. Rebuild the complete 302-by-125 affine-linear augmented system from the
   EXP-112/115 constructors, restoring all 24 directions identified by the
   exact EXP-112 cyclic core.
2. Load the shared row basis from the EXP-121 primary artifact and evaluate it
   at \(M_\ast=M(A=1,B=0,d=1)\).
3. Compute the exact normalized matrices
   \[
   K_i=M_\ast^{-1}D_i
   \]
   over \(\mathbb Q\).
4. Reproduce the \(T_B\) union graph and its size-26 largest cyclic component.
5. For every direction, persist:
   - exact nonzero count and rank;
   - exact trace, hence the first directional determinant derivative;
   - exact one-parameter characteristic factor
     \(\det(I+tK_i)\);
   - support internal to the \(T_B\) 26-block;
   - the largest SCC after adjoining the direction to \(T_B\);
   - exact pairwise mixed coefficients
     \[
     [es]\det(I+eK_i+sK_j)
     =\operatorname{tr}(K_i)\operatorname{tr}(K_j)
      -\operatorname{tr}(K_iK_j)
     \]
     for \(j\in T_B\).
6. Classify restored directions as anchor-line determinant-inert,
   active in the existing 26-block, SCC-increasing, or acyclic/off-block
   relative to the \(T_B\) graph. These labels are audit labels, not
   coverage theorems.
7. Independently validate every persisted one-parameter determinant factor at
   two nonzero rational parameter values by direct exact determinant ratios.

## What a PASS proves and what a FAIL proves

A PASS proves an exact, reproducible activity classification of the 24
cyclic-core directions on the EXP-121 shared basis at its rational anchor. It
identifies the smallest justified next symbolic neighborhood experiment.

A PASS does not prove that the complete \(T_B\) cover lifts, does not cover any
four-parameter restriction, and does not close the 24-parameter core, the
51-parameter family, \((72,108)\), the degree floor, or \(JC(2)\).

A FAIL of prediction 2 proves that no restored direction is free on its
one-parameter anchor line for this basis. A FAIL of prediction 3 proves that
the restored directions do not have the predicted mix of internal and
SCC-enlarging support. A FAIL of prediction 4 proves that all restored
directions first participate beyond the tested first and pairwise mixed
orders. None of these failures rules out a higher-dimensional cover using
other rows or higher-order interactions.

## Invariant-first note

The cheap invariants are the characteristic polynomial of each normalized
direction, the SCC size of its union with \(T_B\), and the trace pairings with
the three \(T_B\) matrices. They decide anchor-line determinant independence
and the earliest tested mixed participation without constructing a generic
24-variable determinant. A full 24-variable determinant or Groebner
calculation is explicitly outside this experiment.

## Adversarial controls

- Reproduce the EXP-121 exact anchor determinant and size-26 \(T_B\) SCC.
- Reproduce all 24 EXP-112 active direction labels exactly.
- Verify every one-parameter characteristic factor by direct determinant
  ratios at \(t=1\) and \(t=-1/2\) whenever the evaluated matrix is defined.
- Compute pairwise mixed coefficients from exact traces only and check
  symmetry under exchanging the two directions.
- Preserve null and refuted predictions as first-class results.

## Compute budget and kill criterion

CPU only, exact SymPy arithmetic over \(\mathbb Q\). Expected runtime is under
two minutes. The hard budget is five minutes. Progress must be flushed after
matrix construction and after every four directions. If the budget is hit,
the run is stopped and the completed per-direction records are preserved; the
verdict is inconclusive and the next round must replace characteristic
polynomials with blockwise or modular reconnaissance before retrying exact
work.

## Exploration moment

The new viewpoint is to treat the EXP-121 row basis as a local determinantal
representation and use its logarithmic determinant tensors
\(\operatorname{tr}(K_i)\) and
\(\operatorname{tr}(K_iK_j)\) as a sparse interaction oracle. This separates
directions that are graph-active but determinant-silent at low order from
directions that change a chart immediately. If all low-order tensors vanish,
the next path is higher-order trace words on the smallest SCC-increasing
direction, not a generic 24-variable expansion.
