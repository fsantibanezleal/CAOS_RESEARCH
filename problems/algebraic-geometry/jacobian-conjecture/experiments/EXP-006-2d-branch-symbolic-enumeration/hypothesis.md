# EXP-006 - Branch-symbolic enumeration of 2D equivariant Keller maps

- **Question.** EXP-005 reduced the Gm-equivariant Keller condition on C^2 to the univariate ODE
  b1 f g' - b2 f' g = const != 0 with b1 + b2 = 1 - a, but its injectivity scan was VACUOUS
  (0 instances). Does a proper enumeration (branch-symbolic solving, in-image targets) find real
  solution families, and is every one of them injective?
- **Motivation.** Conjecture "2D equivariant rigidity" (wiki 04): every Gm-equivariant Keller
  map of C^2 is invertible. A non-vacuous scan either supports it with real coverage or refutes
  JC(2) outright.
- **Fixes over EXP-005.** (1) Branches from solve() are kept SYMBOLIC; residuals are re-checked
  after every instantiation, and each discarded instance is counted with its reason (no silent
  dropping). (2) Fiber targets are taken IN THE IMAGE (target = F(x0, y0) for random rational
  (x0, y0) with x0 != 0), so empty fibers cannot masquerade as injectivity. (3) Multiple
  instantiation samples per branch.
- **Falsifiable predictions.**
  1. The enumeration over a in {1, 2, 3}, b1 in [-3, 3], deg f, deg g <= 3 finds a NONZERO
     number of polynomial Keller instances (the scan is no longer vacuous; hand analysis says
     e.g. linear diagonal maps must appear).
  2. Every instance has exactly ONE preimage over each tested in-image target (injective on the
     tested set). Analytic side-expectation (recorded, not assumed): the solution families are
     de Joncquieres-like / affine.
  3. No instance exhibits 2 or more preimages. (If one does, that is a counterexample to JC(2)
     and this program's biggest possible positive; we predict it does not happen.)
- **Method.** sympy over QQ. For each (a, b1, b2, df, dg): solve the coefficient system of
  b1 f g' - b2 f' g - c = 0 keeping c symbolic; per branch, instantiate free parameters over 3
  rational samples; filter by exact residual and polynomiality (counted); per instance, 3
  in-image targets; fiber count by lex Groebner (eliminant degree + zero-dimensionality check).
- **Success criterion.** Predictions 1 and 2 hold with instance count > 0 reported explicitly.
- **Failure criterion.** Scan vacuous again (design failure, documented), or a multi-point fiber
  (JC(2) refuted; escalate immediately).

Declared 2026-07-20 before the run.
