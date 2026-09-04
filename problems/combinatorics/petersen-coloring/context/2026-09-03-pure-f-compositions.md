# Derivation note: compositions made only of copies of F are Petersen colorable (2026-09-03)

Status: `[D]` derived here, `[MV]` machine-witnessed by EXP-005 (classes `(5,0)` and `(6,0)`
exhausted by a single universal coloring in 15 and 27 iterations).

## Statement

Let `F` be the Petersen graph minus the endpoints of one edge, an 8-vertex 4-pole whose four
semi-edges sit at four distinct vertices of degree 2. Let `G` be any simple cubic graph obtained
from `k >= 1` disjoint copies of `F` by joining their `4k` semi-edges in pairs (no free
vertices). Then `G` has a Petersen coloring.

## Proof

Jooken's Lemma 2.1 (arXiv:2608.10028v2, `[V]`) lists the P-colorings of `F` by the distance in
the line graph `Q` of `P` between the two input labels; at distance 0 all four semi-edge labels
coincide. Concretely, there is a P-coloring `sigma_0` of `F` in which the four semi-edges all
carry the same edge `x` of `P` (EXP-005 exhibits one: the universal coloring recorded in
`E:/_Datos/caos-research/petersen-coloring/EXP-005/k5m0.jsonl`, whose 20 boundary labels are all
equal; its restriction to each copy is a valid P-coloring by the independent checker
`verify_witness_labels`, which tests membership in the exact P-coloring set `PCOL_F` of 315
boundary tuples). Color every copy of `F` in `G` by `sigma_0` with the same `x`. Every join
edge of `G` connects two semi-edges both labeled `x`, so it receives the well-defined label `x`.
At every vertex of `G` the star is a star of one copy of `F` under `sigma_0`, hence a star of
`P`. So the map is a Petersen coloring of `G`. QED.

## Consequences

- No counterexample to the Petersen coloring conjecture consists solely of copies of `F`; free
  vertices (or other gadgets) are necessary. The known counterexamples have 4 free vertices
  (`G52`) and 16 free vertices (both 112-vertex graphs), measured in EXP-005.
- The same argument applies to any gadget that admits a coloring with all boundary labels equal;
  so a counterexample must contain gadgets (here, free vertices, whose three labels must be
  distinct) that break label uniformity.
- For the composition search this means the classes `C(k, 0)` are trivial, and the difficulty
  is concentrated in how the free vertices are wired.
