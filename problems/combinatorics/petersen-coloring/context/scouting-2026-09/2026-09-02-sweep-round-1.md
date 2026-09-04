# New-problem scouting, round 1 (2026-09-02)

Purpose: find the next problem to open in CAOS_RESEARCH, scored with
`program/counterexample-radar.md`. Every row below is a lead, not a verdict. Claims carry the
local marks `[V]` verified against a primary source read in this sweep, `[MV]` machine-verifiable
in principle, `[U]` unverified (search-engine summary only).

## Landscape (September 2026)

- AI-assisted counterexamples are now routine: an index at `https://aimath.robertj1.com/` lists
  506 AI-linked claims through 2026-08-21 (116 disproofs) `[U]`. Xena blog 2026-07-20
  ("Human mathematicians are being outcounterexampled") lists the unit-distance disproof, the
  order-4 group-scheme counterexample, and the Jacobian counterexample `[V]`.
- The radar consequence: replication alone is worthless; the value is in certified minimality,
  families, mechanism, and surviving variants, exactly the Huneke-Wiegand pattern.
- Problems already owned by other sessions (excluded): Jacobian and every Jacobian-adjacent
  item (Gaussian moments, vanishing conjecture, Mathieu), Huneke-Wiegand and rigid ideals in
  dimension-one Gorenstein domains, central configurations, tau conjecture, unsplittable flow.

## Leads

| id | lead | primary source | status of source read | first radar impression |
|---|---|---|---|---|
| L1 | Han's conjecture disproved (finite-dim C-algebra, gldim infinite, HH_n=0 for n>=1); Kong, Liu, Shen; GPT-assisted | arXiv:2608.00177 (2026-07-31) | abstract + HTML summary `[V]` | construction is derived (tilting bundle on 10-point blowup, dual numbers, folded complexes), NO explicit presentation, NO dimension given. Extension: explicit small quiver algebra. Certificate: HH of a finite-dim algebra is computable but needs all n>=1; hard. |
| L2 | Localization problem for AB rings answered negatively; Lyle, Nasseh; Claude Opus 5 assisted | arXiv:2609.00754 (2026-09-01) | abstract + HTML summary `[V]`; dimension reported inconsistently (1 vs 11) `[U]` -> must read the PDF | Gorenstein ring S[[t]]/I over k[[x1..x5]], embedding dimension 6, quadratic relations, localization at (x1..x5) is a Jorgensen-Sega ring. Extension: minimal embedding dimension, other parameters alpha, characteristic. Certificate: Ext computations over artinian Gorenstein rings (Macaulay2). |
| L3 | Bougard-Joret conjecture on the minimum number of edges of k-connected graphs with independence number alpha, disproved; Das, Gupta | arXiv:2608.18828 (2026-08-19) | abstract `[V]` | boundary case n=alpha+k fully determined, smallest failure (7,3,4). OPEN: the corrected value of f(n,alpha,k) for the rest of the regime n<=k*alpha. Finite exact surface (geng + SAT/ILP with certificates). |
| L4 | Hoa's 1994 conjecture on maximal non-Hamiltonian graphs disproved for every order n>=56; Zhan | arXiv:2608.00957 (2026-08-02, v2 08-14) | abstract `[V]` | OPEN by construction: the smallest order of a counterexample (somewhere in 7..55), and the problems the paper poses. Exact surface: MNH graph enumeration + longest-cycle certificates. Enumeration to order 55 is out of reach; a structural route is needed. |
| L5 | Rethlas resolves Erman-Sam Questions 6.1 and 6.2 (Boij-Soderberg realizability of integral points on pure rays) by counterexamples | arXiv:2605.25259 (2026-05-24) | HTML summary `[V]` | OPEN: which integral points on codimension-3 pure rays are realizable over S=k[x,y,z]. Exact surface (Macaulay2 constructions, Betti tables). Heavy algebra; novelty window good. |
| L6 | Sra, "GPT, the Counterexample Machine": 16 counterexamples with explicit open follow-ups | arXiv:2608.29595 (2026-08-30) | HTML summary `[V]` | follow-ups: quantum coupon collection positivity for n<=5 in all d (claimed proved), sharp constants; matrix inequalities. Mostly analysis/matrix; finite exact certificates exist but extension value unclear. |
| L7 | aimath index July-Aug 2026 disproofs with computational certificates: Carlson depth conjecture (GAP/Singular), Dere real-form conjecture (dim 10 Lie algebras), Babai Cayley graphs, purely-prime ideals, HRT conjecture | index `[U]` | none read | each needs a primary read; minimality/family questions likely open. |
| L8 | Numerical semigroups: Wilf verified to genus 100 (Delgado et al. 2023), Bras-Amoros counting through g=77 (2025) | arXiv:2310.07742, OEIS A007323 | summaries `[U]` | mature, heavy compute, low novelty per CPU-hour. Deprioritized. |
| L9 | FrontierMath Open Problems (about 50 verifiable open problems; 3 solved by AI) | epoch.ai/frontiermath/open-problems | index `[U]` | verifiable-by-program by design; needs a read of the list for a finite-certificate item not already saturated. |

## Next step

Deep dossiers on L2, L3, L4, L5, L7 (and L1 for feasibility) written to this folder, then a
radar score table and the pick.
