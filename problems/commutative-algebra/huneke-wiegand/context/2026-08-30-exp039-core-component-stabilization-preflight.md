# EXP-039 preflight - component stabilization of the parity core

Date: 2026-08-30. Status: source-complete for the declared finite test.

## Question exposed by EXP-038

EXP-038 gives two exact out-of-sample passes for the corrected `t=2` parity-excess series, but it
does not exhibit the proposed degree-six relation.  For every tested `p>=5`, the kernel and the
connecting boundary have the same rank in characteristics two and odd; the entire defect occurs
in the combined signed presentation.  The next question is therefore structural:

> Does exact unit cancellation split the combined residual support into bounded, recurring
> characteristic-dependent blocks whose translations could carry a graded-module structure?

This is stronger than another coefficient computation and cheaper than integral Smith form of
the full matrix.

## Source and novelty check

- Bruns and Herzog, *Semigroup rings and simplicial complexes*, JPAA 122 (1997),
  <https://doi.org/10.1016/S0022-4049(97)00051-0>, identifies multigraded Betti numbers of affine
  semigroup rings with relative homology of squarefree divisor complexes and explicitly treats
  characteristic dependence.  It supplies the topology dictionary, not this parameterized
  family or its parity multiplicities.
- Autry et al., *Squarefree divisor complexes of certain numerical semigroup elements*,
  <https://arxiv.org/abs/1804.06632>, computes such complexes for selected numerical-semigroup
  families.  It supports studying the complexes directly but does not contain the present
  conductor-family targets.
- Church--Ellenberg--Farb--Nagpal, *FI-modules over Noetherian rings*,
  <https://arxiv.org/abs/1210.1854>, proves integral finite-generation machinery for compatible
  sequences.  Nagel, *Rationality of Equivariant Hilbert Series and Asymptotic Properties*,
  <https://arxiv.org/abs/2006.13083>, gives rational Hilbert-series consequences for finitely
  generated FI/OI modules.  Applicability here is only a research hypothesis: no FI/OI action or
  finite-generation theorem for these varying complexes is known.

No inspected source settles the component structure, the degree-six relation, or the exact
sequence `1,4,9,18,31,49,72,102,138`.  The proposed experiment is therefore not duplicating a
known result.

## Why components are the invariant-first test

Connected components of the bipartite row-column support give an exact block diagonalization up
to permutation.  Ranks and characteristic defects add across those blocks, independently of
pivot order.  If the proposed parity classes are genuinely independent translated local objects,
they should be visible at this coarsest level.  If the residual support is one giant component,
the component model is refuted immediately and the correct next invariant is a finer
Dulmage--Mendelsohn/matched-block or relative-homology decomposition.

## Declared resource gate

- CPU only; exact arithmetic over `GF(2)` and `GF(3)`.
- Regress `(4,2)` and `(5,2)` before accepting larger cells.
- Primary campaign: `p=4,...,9`, checkpointing one JSON row after every parameter.
- Budget: 1,800 seconds and 20 GB.  Stop cleanly at the last completed parameter if either limit
  is crossed; an early stop is **INCONCLUSIVE**, not evidence for stabilization.
- A positive recurring block requires a canonical-order `GF(5)` audit on its first and last
  observed instances.

## Manuscript and publication boundary

A connected-component table is method evidence, not a manuscript theorem.  Manuscript v0.24 and
Zenodo remain closed unless the experiment extracts an explicit all-parameter block/translation
law or a comparably strong structural theorem.
