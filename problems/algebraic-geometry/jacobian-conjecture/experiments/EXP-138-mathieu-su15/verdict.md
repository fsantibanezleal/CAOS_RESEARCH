# EXP-138 verdict: CONFIRMED

Date: 2026-11-01. Hypothesis frozen at `1b08a923` before the code was written.

## Result

An independent sympy re-implementation of de Bondt's homogenization (arXiv:2610.24889, `anc/section2a.mac`
read as text only) turns Alpöge's map in de Bondt's volume-normalized form,
`F = (x1 - 3 x1^2 x2 - x1^3 x3, 3 v^2 x1 x3 + (9 v^2 - 6 v - 2) x2, v^3 x3 + (6 v^2 + 2 v) x2^2)`,
`v = 1 + 2 x1 x2`, into `G = x + H` on C^15 with every `H_i` homogeneous of degree 7, and exactly:

- `det J(F) = 1` and `F(0,1,-8) = F(-1,1,4) = (0,1,0)`;
- `(JH)^14 = 0`, so `JH` is nilpotent and `det J(G) = det(I + JH) = 1`;
- `G(0,1,-8,0,0,0,0,0,0,0,0,0,0,0,1) = G(-1,1,4,-4,-1,48,12,-36,-12,32,8,-40,-12,12,1)`.

With `h = -H`, `G = x - h` is a non-invertible Keller map with `h` homogeneous. By Zwart, Theorems 4.23
and 4.16 (arXiv:2511.16561v2, transcribed in EXP-136), the Mathieu conjecture for SU(N) implies that every
such map on C^N is invertible. Hence **the Mathieu conjecture is false for SU(N) for every N >= 15**
(adjoin identity coordinates for N > 15; the form `x - h` is kept). This lowers the threshold recorded by
EXP-136 from `N >= 24`. The witness is de Bondt's construction; the Mathieu consequence is not stated in
his paper.

## Prediction table

| prediction | outcome |
|---|---|
| P1 constant determinant and collision of `F` | PASS |
| P2 dimension 15, degree 7, homogeneous, `(JH)^14 = 0`, rational collision | PASS |
| P3 consequence through Zwart's chain | PASS (deductive, given P2) |
| P4 control: `F2 + x2^2` makes `det J` non-constant | PASS (fires) |

Artifacts: `artifacts/results.json` (all 15 components and both points), `artifacts/run-log.txt`; 7
seconds of CPU.

## Scope

SU(N) for `3 <= N <= 14` remains undecided by this route (the smallest homogeneous counterexample found
by de Bondt is in dimension 15; van Rijn's cubic homogeneous one is reported in dimension 19). SU(2) is
covered by Long (EXP-136 amendment). Zwart's text is expository; the implication is Mathieu's
(Theorems 5.3 and 5.4 of the 1997 paper, not located in an open copy, as EXP-136 records).
