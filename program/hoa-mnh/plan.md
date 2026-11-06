# hoa-mnh: plan

Opened 2026-11-06. Scope: [scoping sheet](scoping-2026-11-06.md).

## Systematic spine

Exact census of MNH graphs by order, with every longest cycle and its residual, as far as exhaustive
generation reaches (order 11, then 12). Each order either finds a counterexample to Hoa's conjecture (and then
the least order is known) or raises the verified lower bound for the least order.

## Complementary lenses

1. Exhaustive enumeration (spine): geng over connected graphs, pruned by the degree-sum tightness every MNH
   graph satisfies, exact Hamiltonicity by subset dynamic programming.
2. Constructive gadgets: Zhan's route is K_1 join a maximal nontraceable graph built by Bullock et al. Theorem
   3.13 from three MNH gadgets; with the census, tabulate for each MNH graph X and vertex x the path deficiency
   between neighbours of x and the omitted set, and search gadget triples for counterexamples below 56.
3. Structure: toughness and minimum degree of the census graphs against Hoa's two theorems, to explain where
   counterexamples can and cannot occur.

## Invariant-first probe

Before any search: residual shape over all longest cycles (complete, component count, connectedness), toughness,
minimum degree; recorded per MNH graph in the census artifact.

## Adversarial validation

Known-answer gate: A185306 for n <= 10. Independent Hamiltonicity check (networkx-free brute force in a second
implementation) on every MNH graph found. Any counterexample is re-verified by a second implementation before a
claim.

## Exploration cadence

One bounded experiment per round; the census verdict decides whether the gadget lens runs next.

## First bounded experiment

EXP-001-mnh-census: orders 1-11 exhaustively (12 if the order-11 cost extrapolates to under 12 hours on 24 cores).
