# program/ - the portfolio status board

The in-repo status section: which problems exist, in which lifecycle state (see
`methodology/01-lifecycle.md`), and where each problem's plan lives. Machine-readable mirror:
[`portfolio.yaml`](portfolio.yaml) (consumed by the data-pipeline to bake the web home page).

| Problem | Area | State | Feasibility | GPU | Plan |
|---|---|---|---|---|---|
| Jacobian conjecture | algebraic-geometry | exploring | A | yes | [jacobian-conjecture/plan.md](jacobian-conjecture/plan.md) |
| Central configurations (n-body) | dynamical-systems | exploring | A | yes | [central-configurations/plan.md](central-configurations/plan.md) |
| Unsplittable-flow cost | optimization-geometry | exploring | A | partial | [unsplittable-flow-cost/plan.md](unsplittable-flow-cost/plan.md) |
| Log-energy points on S^2 (Smale 7) | optimization-geometry | scoped | A | yes | (wave 2) |
| Shub-Smale tau conjecture | computation-complexity | exploring | A | yes | [tau-conjecture/plan.md](tau-conjecture/plan.md) |
| Riemann hypothesis | number-theory | scoped | A | yes | (wave 2) |
| Diophantine 2-variable decidability | computation-complexity | proposed | B+ | partial | |
| Hilbert 16th, part 2 | dynamical-systems | proposed | A- | yes | |
| Strongly polynomial LP | computation-complexity | proposed | B+ | partial | |
| Navier-Stokes regularity | analysis-pde | proposed | B | yes | |
| Yang-Mills mass gap | mathematical-physics | proposed | B | yes | |
| Birch and Swinnerton-Dyer | number-theory | proposed | B | marginal | |
| P vs NP | computation-complexity | proposed | C+ | partial | |
| Centralizer density (Smale 12) | dynamical-systems | proposed | C+ | no | |
| Hodge conjecture | algebraic-geometry | proposed | C+ | no | |
| Huneke-Wiegand counterexample extensions | commutative-algebra | exploring | A | no | [huneke-wiegand/plan.md](huneke-wiegand/plan.md) |

Portfolio selection is also informed by the finite-certificate and validation-loop criteria in
[`counterexample-radar.md`](counterexample-radar.md). Prestige is not a substitute for a tractable
falsification surface.

State transitions are logged in each problem's `state.md` and its `history/` log. Scoping
evidence: the 2026-07-20 scoping dossier (transcribed into `problems/.../context/` at open time).
