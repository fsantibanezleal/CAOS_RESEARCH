# EXP-017 - The bilinear harness: exhaustive-in-Q JC(2) certificates at (2,3) and (3,3)

- **Question.** Complete what EXP-013's part 3 could not: exhaustive small-degree JC(2)
  certificates at degree pairs (2, 3) and (3, 3), past the sympy nonlinear-solve artifact.
- **Motivation.** JCB-021. The key structural fact: det J(P, Q) is BILINEAR in the coefficient
  vectors of P and Q. In the affine gauge (P = x + higher, Q = y + higher, det = 1), fixing
  P's coefficient vector A makes the Keller condition a LINEAR system in Q's coefficients B,
  which sympy solves completely and reliably. Sampling A over a structured grid (including all
  degenerate zero patterns) and solving exactly in B gives a certificate that is EXHAUSTIVE in
  B for every sampled A: strictly stronger than branch sampling, and immune to the (2, 3)
  artifact (the triangular witness must and will appear).
- **Falsifiable predictions.**
  1. [MV] (2, 3): for every A on the grid {-2, -1, 0, 1, 2, 1/2}^3, the linear system in B is
     solved COMPLETELY (consistent branches parametrized); the triangular witnesses
     (x, y + a x^2 + b x^3) appear; every clean Keller instance has in-image fiber size <= 1.
  2. [MV] (3, 3): same over a deterministic 60-vector A-sample (structured zero patterns plus
     mixed rationals); every clean Keller instance has in-image fiber size <= 1.
  3. (Scope, declared) The certificate is exhaustive in B per sampled A, not exhaustive in A;
     the A-space statement remains sampled and is recorded as such.
- **Method.** sympy over QQ: linear solve (solve on the B-unknowns) per A-sample; instantiation
  of free B-parameters over 2 shifts; exact fiber counts by lex Groebner at in-image targets;
  counters for consistency/degenerate/Keller filters (no silent drops).
- **Success criterion.** Predictions 1-2 hold with nonzero instance counts and zero multi-point
  fibers.
- **Failure criterion.** A multi-point fiber (a planar counterexample: escalate immediately),
  or vacuous scans (harness bug; diagnose before claiming anything).

Declared 2026-07-21 before the run.
