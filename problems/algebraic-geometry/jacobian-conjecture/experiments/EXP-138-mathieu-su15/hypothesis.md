# EXP-138 hypothesis: the Mathieu conjecture fails for SU(N) for every N >= 15

Date: 2026-11-01. Frozen before the construction is re-implemented or run.

## Source preflight

- de Bondt, "Alpöge's counterexample to the JC, Economic Stabilization, and Zhao's Vanishing
  Conjecture", arXiv:2610.24889v1 (2026-10-17). Section 3 and the ancillary file `anc/section2a.mac`
  (read as text, not executed) construct, from a volume-normalized form of Alpöge's map
  `F = (x1 - 3 x1^2 x2 - x1^3 x3, 3 v^2 x1 x3 + (9 v^2 - 6 v - 2) x2, v^3 x3 + (6 v^2 + 2 v) x2^2)`,
  `v = 1 + 2 x1 x2`, with collision points `(0,1,-8)` and `(-1,1,4)`, a unipotent homogeneous map of degree
  7 in dimension 15 (his table: `not HJC(15,7)`). The paper does not mention the Mathieu conjecture.
- Zwart, arXiv:2511.16561v2, Theorems 4.23 and 4.16 as transcribed in
  `experiments/EXP-136-cascade-dimension-audit/artifacts/sources.md`: the Mathieu conjecture for SU(N)
  implies Conjecture 4.3 on C^N, invertibility of every map `x - h` with `J = 1` and `h` homogeneous of any
  degree `d`. EXP-136 recorded the consequence "Mathieu false for SU(N), N >= 24" from the 24-variable
  cubic map of EXP-041.

## Predictions

- P1: `det J(F)` is a non-zero constant and `F(0,1,-8) = F(-1,1,4)`, in exact arithmetic.
- P2: an independent sympy re-implementation of the degree reduction and homogenization produces a map
  `G = x + H` on C^15 with every `H_i` homogeneous of degree 7 or zero, `det(I + s JH) = 1` identically in
  `s` (so `JH` is nilpotent and `J(G) = 1`), and two distinct rational points with the same image.
- P3: with P2, Zwart's chain gives that the Mathieu conjecture is false for SU(15), and for every
  `N >= 15` after adjoining identity coordinates (which keeps the form `x - h`, `h = -H`).
- P4 controls: changing one coefficient of `F` breaks the constant determinant or the collision, and the
  same change propagated through the construction breaks P2.

## What PASS and FAIL prove

PASS lowers the recorded Mathieu threshold from 24 to 15 with an exactly verified witness credited to de
Bondt's construction; the implication is Zwart's (expository source), with the fixed-dimension caveat of
EXP-136 not needed here because the map is already of the homogeneous form. FAIL locates a defect in the
witness or in our re-implementation and leaves N >= 24.

## Budget

Minutes of CPU, exact arithmetic only.

## Manuscript gate

PASS updates the cascade manuscript (`manuscripts/jacobian-conjecture/cascade`) status table: Mathieu
false for SU(N), N >= 15, and the dimension records of de Bondt for the vanishing conjectures.
