# EXP-002 - endomorphism overring and escape mechanism

Declared 2026-08-01 before EXP-002 code or computation. Phase HW-P2. Backlog HWB-002.

## Question

What is the exact finite birational overring `End_R(I)`, and does its value semigroup explain why
the rigid nonprincipal ideal escapes modern endomorphism-ring positive criteria?

Normalize `J=(1,t^14)R`. Its value set is `V=Gamma union (14+Gamma)`. A monomial `t^x`
belongs to `End_R(J)` exactly when `x+V` is contained in V; because V is generated over Gamma by
0 and 14, it suffices to test `x in V` and `x+14 in V`.

## Committed predictions

- P1: the stabilizer value semigroup is exactly
  `Lambda = Gamma union {101,107,181}`.
- P2: Lambda has Frobenius number 125, conductor 126 and genus 88.
- P3: Lambda is not symmetric and therefore its localized numerical-semigroup ring is not
  Gorenstein.
- P4: Lambda is closed under addition, contains Gamma, and stabilizes V in both generator tests;
  each of 101, 107 and 181 is necessary, while every other Gamma-gap fails stabilization.
- P5: two independent implementations agree: direct bounded set stabilization and an Apéry-vector
  membership route with a proved conductor tail.
- P6: replacing Lambda by Gamma fails because 101 stabilizes V but is not in Gamma; adding a false
  gap such as 103 fails the stabilizer test. These controls must be caught.

## Theorem consequences to audit, not assume

After P1-P6, check the exact hypotheses in Dey-Lyle (2025). For the commutative overring
`E=End_R(I)`, rigidity and nonprincipality should force the failure of their additional positive
hypotheses: E cannot be Gorenstein; I cannot be reflexive as an E-module; and the relevant
Ext/Tor vanishings cannot hold. Each implication must cite a precise theorem before entering the
verdict.

## Method and budget

- Route A: direct membership table through the candidate conductor and a proved tail.
- Route B: Dijkstra Apéry vectors modulo 56 for Gamma, V and the stabilizer.
- Enumerate all Gamma-gaps as adversarial nonmembers; no sampling.
- Exact integers only. Wall cap two minutes; expected runtime under one second.

CONFIRMED requires P1-P6. A mismatch between routes is REFUTED as an instrument and blocks all
theorem consequences.
