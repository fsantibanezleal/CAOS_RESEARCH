# 05 - Experiments and results

One line per experiment; the folders hold the long form (hypothesis, runner, artifacts,
verdict). Verdicts are quoted verbatim from `verdict.md`, never upgraded.

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| [EXP-001](../experiments/EXP-001-ac-calibration/) ac-calibration | Does our exact AC builder reproduce the classical n = 3 classification and assemble the HM n = 4 system? | confirmed in part, REFUTED in part (P7 uniqueness), inconclusive at caps | Euler-Moulton counts exact (1 positive collinear solution per ordering, 4 mass samples); Lagrange point identical in symbolic masses; symbolic Euler eliminant (degree 54) persisted; n = 4 system profile baseline; equal-mass saturated ideal 0-dim (GB 37); THE REFUTATION: the bare AC distance system is dimension-blind, the regular tetrahedron (a = b = 1) coexists with the square (a^3 = (4 + sqrt(2))/8, minpoly 32x^6 - 32x^3 + 7) in the equal-mass rhombus stratum; planarity requires adjoining Cayley-Menger, after which the square is unique in the stratum |
| [EXP-002](../experiments/EXP-002-enriched-census/) enriched-census | Do the censuses on the ENRICHED system (F + G + e_IU, + e_CM for planarity) come out classical, and does enrichment remove the bare-system pathologies? | confirmed on every decided prediction; P2 inconclusive at caps (2 of 4 samples) | THE ENRICHMENT THEOREM-BY-MACHINE: F + G + e_IU is zero-dimensional DIRECTLY (0.7 s per sample, no saturation; the G-equations kill the EXP-001 line identically in symbolic masses); decided censuses perfectly classical (exactly 4 points: equilateral + 3 collinear); planar rhombus census = the square alone; U = M I exact everywhere; J baselines (square 1/16 + sqrt(2)/8, tetrahedron 3 sqrt(6)/32); engine limit measured: sympy census saturates on integer-separated masses (msolve queued, CCB-025) |

| [EXP-003](../experiments/EXP-003-jl25-prevariety-reproduction/) jl25-prevariety-reproduction | Does our wrapped gfan 0.7 reproduce the published Jensen-Leykin n = 5 generic-finiteness prevariety computations exactly? | CONFIRMED (all three predictions; exact reproduction) | Both published f-vectors matched digit-for-digit ((1506, 4744, 8586, 8787, 4652, 993) and (3586, 12012, 18531, 15625, 7072, 1357)); pointedness verified independently (85 unbounded directions, none with a positive coordinate); ~6 wall-minutes per valuation on 30 threads; the tropical lane (valuation search CCB-030, equation variants CCB-031, the n = 6 target) is OPEN on validated infrastructure |

## Instruments validated by EXP-001

- The exact AC system builder (F-equations, cleared forms over QQ[m][r]).
- The eliminant census (lex-Groebner univariate eliminants + CRootOf isolation + exact
  residual acceptance): the program's verdict-grade counting instrument. sympy's
  `solve_poly_system` was caught returning incomplete lists and is banned from
  verdict-bearing counts (see the adversarial record in the EXP-001 verdict).
- The saturation 0-dim certificate (product-Rabinowitsch + pure-power criterion),
  currently affordable at equal masses only; instrument upgrade queued (CCB-007).
