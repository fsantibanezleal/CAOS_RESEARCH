# Jacobian programme strategy audit: 2026-07-29

Scope: validate the complete active planar plan after EXP-110, reconcile every
route against primary evidence, and reprioritize toward the strongest
all-parameter path.

## Executive verdict

The planar Jacobian conjecture remains open. The repository has neither
validated nor invalidated it in dimension two. The immediate \((72,108)\)
GGHV branch also remains open.

EXP-111 corrects the proposed EXP-110 redirect:

- the constant \(Q\)-column is structurally zero because \([P,1]=0\), so
  \(\operatorname{rank}M\leq124\) identically;
- the exact pinned augmented minor from EXP-059 proves generic rank
  \(124/125\) for \(M/[M\mid b]\), hence inconsistency on a nonempty
  Zariski-open subset;
- this is not all-parameter closure because the exceptional augmented-minor
  locus remains;
- EXP-110 used 289 forced-only rows, while the complete row union inside the
  canonical EXP-071 pool has 302 rows;
- proving that all \(125\)-minors of \(M\) vanish is vacuous and is retired;
- EXP-109 and further coefficient-slice enumeration cannot terminate and are
  demoted.

The strongest route is now a graph-compressed augmented-minor attack on the
complete 302-row system. It first asks whether a choice of 125 independent
augmented rows makes every normalized perturbation jointly acyclic. A positive
answer gives a constant nonzero determinant and closes the reduced family
uniformly. A negative answer must still identify the smallest strongly
connected parameter core, reducing subsequent exact algebra to that core
instead of 51 variables.

## Evidence model after EXP-111

Write
\[
M(\varepsilon)q=b,
\qquad
\varepsilon=(\varepsilon_1,\ldots,\varepsilon_{51}).
\]
The constant coefficient of \(Q\) is pure gauge and has an identically zero
column. Remove it and append \(b\):
\[
A(\varepsilon)
=
[M_{\mathrm{nonconstant}}(\varepsilon)\mid b],
\]
an effective 302-by-125 affine-linear matrix.

The exact pinned determinant proves that some \(125\)-minor of \(A\) is a
nonzero polynomial. Thus \(A\) has rank 125 generically. The unresolved set is
\[
V(I_{125}(A)),
\]
the common zero locus of all augmented maximal minors. The reduced family is
excluded exactly when this locus is empty on every admissible GGHV branch.

The problem is therefore not generic rank. It is uniform nonvanishing of an
augmented determinantal ideal.

## Complete route adjudication

| Route | Decision | Evidence-backed value | Required next gate |
|---|---|---|---|
| Complete augmented-matrix graph compression | P0, pursue now | can give a uniform constant determinant, or reduce 51 parameters to a cyclic core | EXP-112 with modular search and exact verification |
| Constructible augmented-minor stratification | P0, retain in compressed form | exact framework for exceptional loci, validated on two- and three-coefficient slices by EXP-101 through EXP-108 | operate on the cyclic core from EXP-112, not the raw 51-variable family |
| EXP-109 and further slice lifts | demote to controls | validates chart machinery on bounded slices only | run only as a regression control for a core selected by EXP-112 |
| EXP-110 all maximal minors of \(M\) | retire as vacuous | structural zero constant column already proves the statement | preserve EXP-111 correction; no determinant work |
| Complete-row recovery | incorporate everywhere | 13 omitted equations from 14 directions may strengthen exceptional-stratum closure | use 302 rows in every new full-family experiment |
| Boundary-divisor reconstruction of intersection 21 | P1 conditional | could transport an original-pair invariant through the Laurent reduction | resume only if graph compression leaves a large core; write the complete divisor ledger first |
| Newton resolution | done at present scope | independently retains the first \(D=72\) branch | require a new restriction beyond the published retained branch |
| Lee-Li inner vertices and approximate roots | done at present scope | seven inner vertices, intersection 21, and the \(84+24\) partition are valid reconstruction filters | no direct coefficient equation without an exact transport map |
| Source frontier \([125,150]\) | P2 independent | 16 unprinted \(A'_0\) values remain useful for the wider floor | continue separately after the immediate \((72,108)\) core step |
| Staircase and window exclusions | retain as theorem infrastructure | exact on their declared strata, but not a complete mixed-staircase theorem | use only when an uncovered GGHV stratum matches the proved hypotheses |
| LND, fibres, Jelonek, and component geometry | hold | useful on original Keller pairs, not typed on \([P,Q]=x^2\) | require an explicit transport map |
| Flat connection and collision projection | retire as stated | no defined implication to the reduced problem | reopen only with typed objects and a falsifiable theorem |
| Degree-four or higher global covectors | hold | EXP-075 excludes polynomial covectors through degree three only | require a necessity or compression theorem before large compute |
| Dimension at least three counterexample record | rolling maintenance | exact false-side record is already established | no current compute |
| Manuscript and Zenodo | no trigger yet | EXP-111 corrects an unpublished branch record and does not add a closed mathematical block | update after an adjudicated all-parameter or new structural result |

## P0 route: acyclic or small-core augmented chart

At the pinned point select 125 rows for which \(A_0\) is invertible. For each
parameter direction form
\[
N_i=A_0^{-1}A_i.
\]
If a simultaneous row and column ordering makes every \(N_i\) strictly upper
triangular, then
\[
\det A(\varepsilon)
=
\det A_0\det\!\left(I+\sum_i\varepsilon_iN_i\right)
=
\det A_0\ne0
\]
for all parameters. This would exclude the entire reduced family in one exact
chart.

EXP-099 refuted a common strict flag for one historical 289-row basis. It did
not search the 13 recovered rows or alternative bases. Therefore the full-row
basis-selection question is genuinely open.

If no common acyclic basis exists, compute the strongly connected components
of the union dependency graph. Directions outside cyclic diagonal blocks are
uniformly eliminable. The determinant depends only on the cyclic core after
block triangularization. EXP-101 through EXP-108 show that the first observed
cycle, generated by \((0,1)\) and \((1,7)\), is tractable by exact graded
charts. The measurable success criterion is therefore either:

1. an acyclic basis and an exact constant determinant; or
2. a certified reduction from 51 parameters to a strictly smaller cyclic core
   with the row basis and block decomposition persisted.

## EXP-112 decision protocol

1. Build the complete 302-by-125 augmented coefficient matrices.
2. Reproduce the pinned rank and the historical EXP-099 basis as controls.
3. Search deterministic modular row bases, including pivots that prioritize
   the 13 recovered rows.
4. For each basis, form the normalized direction matrices and the union
   dependency graph.
5. Rank candidates by largest strongly connected component, number of cyclic
   parameters, and exact-verification cost.
6. If an acyclic candidate appears, verify \(A_0^{-1}A_i\) exactly over
   \(\mathbb Q\) and persist the constant-determinant proof.
7. Otherwise persist the best block decomposition and declare a follow-up
   experiment only on its cyclic core.

The modular stage is candidate generation only. No mathematical conclusion
depends on it until the selected structure is reconstructed exactly.

## Conditional second route: boundary ledger

EXP-097 correctly blocks direct use of
\(\deg_x\operatorname{Res}_y(P,Q)=21\) on the final Laurent coefficients.
The invariant can be reopened only by tracking:

1. the initial coordinate swap and which eliminant is selected;
2. every Laurent localization and its lost \(x=0\) divisor;
3. common translations, which preserve the resultant;
4. the final inversion, which reflects exponent intervals;
5. the absolute boundary order needed to recover degree 21.

This is mathematically stronger than another coefficient slice but costs more
than EXP-112. It becomes P0 only if the cyclic core remains too large for exact
determinantal work.

## Fresh primary-source sweep

The 2026-07-29 sweep found no primary source that closes \((72,108)\):

- Shaska's 2026 graded classification is already reconciled with EXP-010. It
  concerns equivariant Keller maps and does not exclude the non-equivariant
  GGHV reduced family.
- Braun, Gwozdziewicz, Fernandes, and Orefice-Okamoto's 2026 result concerns
  the real Jacobian conjecture when one component has degree 6. It does not
  apply to the complex degree-\((72,108)\) case.
- The GGHV 2022 paper remains the primary statement leaving
  \((72,108)\) open.
- Lee-Li's 2024 inner-polynomial region and the older GGHV
  approximate-root formulas remain restrictions, not exclusions of this
  branch.

Primary links:

- https://arxiv.org/abs/2607.20210
- https://arxiv.org/abs/2605.12302
- https://arxiv.org/abs/2204.14178
- https://arxiv.org/abs/2408.01279
- https://arxiv.org/abs/1708.09367

## Stop and go rules

- Do not claim JC(2), the \((72,108)\) case, or the degree floor is decided
  until every exceptional augmented-minor stratum is closed.
- Do not use rank \(124\) as evidence of a nontrivial covector. It is forced by
  the constant \(Q\)-column.
- Do not use a 289-row full-family matrix. The canonical complete union has 302
  rows.
- Do not enumerate further coefficient slices as the main route.
- Do not run a 51-variable Groebner basis or determinant expansion before the
  graph-compression gate.
- A modular graph candidate becomes a claim only after exact rational
  reconstruction.
- Publish a new manuscript or Zenodo version only after the corrected passages
  are traced to verdicts and a substantive block is adjudicated.

## Exploration moment

The new viewpoint is to read the augmented determinant through the dependency
graph of normalized parameter operators. A common acyclic graph gives a
one-chart uniform proof. Failure still has positive value because strongly
connected components isolate the only parameters capable of changing the
determinant. This converts the previous all-or-nothing common-flag test into a
compression instrument and directly reuses the small cyclic structures already
solved by EXP-101 through EXP-108.
