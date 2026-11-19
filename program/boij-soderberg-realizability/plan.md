# boij-soderberg-realizability: plan

Opened 2026-11-19. Scope: [scoping sheet](scoping-2026-11-19.md). Source: the
[2026-09-02 dossier](../../problems/combinatorics/petersen-coloring/context/scouting-2026-09/2026-09-02-dossier-boij-soderberg-realizability.md),
section 4.4 (stages) and section 5 (candidates A to G).

## Systematic spine

The realizability table of the 220 pure rays (0,d1,d2,d3) with d3 <= 12 over S = k[x,y,z]: for every ray the status of
the primitive point (realized with an explicit module and its field / obstructed with a named proof / open), the least
realizable multiple c_d or the interval [lower, upper] that brackets it, and the U(H) status on the 29 parity-passing
rays. Each round narrows the open set; the table is a result at every stage.

## Stages

0. Exact census: primitive points, U(H) parity and Hilbert functions, the construction multiples (Eisenbud-Schreyer any
   field; the two Eisenbud-Floystad-Weyman constructions in characteristic 0; classical complexes), every published
   obstruction applied at each multiple m, closure under scaling (realizations up, obstructions down) and duality.
1. Random search over GF(32003): generic level modules (randomSocleModule) and generic presentations (randomModule) at
   m = 1, 2, ... below the upper bound; each hit saved as an explicit module and re-verified in a fresh process, in
   Singular, and over QQ with lifted coefficients.
2. Structured search for the survivors with small beta_0: inverse systems with prescribed socle, monomial and toric
   candidates, linkage from Gorenstein and complete-intersection ideals.
3. Obstructions for the survivors: the linear-strand and maximal-minor obstruction of Erman 2009 Section 4 applied to
   pure rays, exhaustive linear presentations for beta_0 <= 3 with d1 = 1 (Eisenbud-Harris spaces of matrices), the
   structure of height 3 almost complete intersections.
4. U(H): the algebra as the cubic Artin-Schelter regular algebra k<x,y>/([x,[x,y]], [y,[x,y]]); minimal graded
   resolutions of quotients by left ideals and of small modules in Singular Plural and Macaulay2 AssociativeAlgebras;
   first the five S-obstructed parity-passing rays with d3 <= 9 ((0,1,3,4) is Erman-Sam's), then the rest.

## Complementary lenses

1. Census and closures (spine). 2. Module search. 3. Obstruction theory. 4. Noncommutative (U(H)). 5. Characteristic
dependence: hits re-run over GF(2), GF(3), GF(5); in characteristic 2 the elements x^2, y^2, z are central in U(H) and
U(H) is free of rank 4 over k[x^2, y^2, z], which carries S-realizations of (d, beta) to U(H)-realizations of (2d, beta)
[D, to be written up with proof in the experiment that uses it].

## Invariant-first probe

Before any search: the parity test (a ray property), the Hilbert function sign (a ray property), the obstruction lower
bound at each m and the construction upper bound decide every ray they reach; searches run only on rays these leave open.

## Adversarial validation

Known-answer gates: the Macaulay2 package tests (randomSocleModule on (0,1,3,4) and (0,2,3,6); randomModule on
(0,4,9,10) gives the Koszul table), the documentation hits on (0,2,3,7) and (0,2,3,9), the dossier's Appendix A columns.
A hit on a point a published obstruction excludes stops the run (a bug or a refutation of a published proof). Every
hit is re-verified by a second system and over QQ before it enters the table. Obstruction proofs are written out per
ray and checked by a reader other than the writer.

## Exploration cadence

One bounded experiment per round; the census decides the order of the search; the smallest-counterexample question
(candidate B) decides when U(H) (stage 4) starts.

## First bounded experiment

EXP-001-pure-ray-census: stages 0 and 1 on the 220 rays, and the machine check of the two d3 = 10 counterexamples.
Hypothesis frozen after the source-complete literature pass of 2026-11-19 (methodology 12, P1) and before any run.
