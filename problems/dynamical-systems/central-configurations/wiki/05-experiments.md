# 05 - Experiments and results

One line per experiment; the folders hold the long form (hypothesis, runner, artifacts,
verdict). Verdicts are quoted verbatim from `verdict.md`, never upgraded.

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| [EXP-001](../experiments/EXP-001-ac-calibration/) ac-calibration | Does our exact AC builder reproduce the classical n = 3 classification and assemble the HM n = 4 system? | confirmed in part, REFUTED in part (P7 uniqueness), inconclusive at caps | Euler-Moulton counts exact (1 positive collinear solution per ordering, 4 mass samples); Lagrange point identical in symbolic masses; symbolic Euler eliminant (degree 54) persisted; n = 4 system profile baseline; equal-mass saturated ideal 0-dim (GB 37); THE REFUTATION: the bare AC distance system is dimension-blind, the regular tetrahedron (a = b = 1) coexists with the square (a^3 = (4 + sqrt(2))/8, minpoly 32x^6 - 32x^3 + 7) in the equal-mass rhombus stratum; planarity requires adjoining Cayley-Menger, after which the square is unique in the stratum |

## Instruments validated by EXP-001

- The exact AC system builder (F-equations, cleared forms over QQ[m][r]).
- The eliminant census (lex-Groebner univariate eliminants + CRootOf isolation + exact
  residual acceptance): the program's verdict-grade counting instrument. sympy's
  `solve_poly_system` was caught returning incomplete lists and is banned from
  verdict-bearing counts (see the adversarial record in the EXP-001 verdict).
- The saturation 0-dim certificate (product-Rabinowitsch + pure-power criterion),
  currently affordable at equal masses only; instrument upgrade queued (CCB-007).
