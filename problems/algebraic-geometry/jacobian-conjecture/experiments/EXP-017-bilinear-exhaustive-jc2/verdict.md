# EXP-017 - Verdict: CONFIRMED (2026-07-21)

Artifacts: `artifacts/output-{23,33}-2026-07-21.txt`.

## Established results

1. **The bilinear harness works and is the right tool.** det J(P, Q) is bilinear in the
   coefficient vectors, so in the affine gauge the Keller condition is a LINEAR system in Q's
   coefficients for each fixed P: sympy solves it completely and reliably, ending the EXP-013
   nonlinear-solve artifact. The triangular witnesses (x, y + a x^2 + b x^3) that refuted the
   old solver appear exactly where they must (the A = 0 samples), validating the harness
   against the recorded failure.
2. **(2, 3) certificate [MV].** Over the full grid {-2, -1, 0, 1, 2, 1/2}^3 of P-coefficient
   vectors (216 samples): 16 admit Keller completions (200 provably inconsistent linear
   systems); all 32 clean instances have in-image fiber size <= 1.
3. **(3, 3) certificate [MV].** Over 45 structured + mixed deterministic A-vectors: 5 admit
   completions; all 10 clean instances injective.

## Scope (declared)

Exhaustive in Q per sampled P; sampled (not exhaustive) in P. The full-A statement would need
the consistency variety of the linear system (rank conditions on M(A)), which is the natural
next stage of this harness (the conditions are minors of a small matrix: computable).

## Adversarial validation record

- The harness was validated against a KNOWN failure (the EXP-013 artifact) by requiring the
  triangular witnesses to reappear; counters make every filter visible (no silent drops).
- Fiber counts are exact lex-Groebner eliminant degrees at in-image targets.

## Consequences

- JC(2) now carries our own mechanical certificates at (2, 2) exhaustive, (2, 3) and (3, 3)
  exhaustive-in-Q over structured P-grids: the harness scales (the linear solve is cheap), so
  wider degree pairs and the rank-conditions completion are a mechanical continuation
  (JCB-021 stays open for the full-A stage and higher degrees).
