# EXP-049 - Verdict: CONFIRMED; THEOREM 6 (the universal tower) stands (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## THEOREM 6 (the universal tower, [MV/D])

Let P = x + R (R without constant or linear part) whose total-degree top form T = P_D is
NOT a proper power. If the completion window is inconsistent with a certificate at any
single N >= deg P - 1, then it is inconsistent at EVERY window: P is not a Keller
component at any partner degree. Proof: the EXP-046 tower argument with T the FULL top
form: (i) degree bookkeeping (P-agnostic); (ii) ker J(T, .) on degree-M forms is zero
unless deg T | M and then exactly the span of T^{M/deg T} (dependence of binary forms;
machine-verified for a primitive monomial, a binomial, and a dense cubic at four
degrees each); (iii) THE UNIVERSAL REDUCTION: T = P - lower by definition, so
T^k - P^k has degree <= k deg P - 1: every resonance reduces in-window mod ker L
(verified on three multi-term shapes; rank tests place L(T^k) in the old-column space);
(iv) the extension (EXP-046). Proper-power tops are the stated exception: they need the
EXP-048 half-plane construction.

## The harvest [MV]

One cleared window certificate each (monomial pairings), hence ALL-DEGREE exclusions by
Theorem 6:
- x + a x^2 y + b x^3 (two-edge staircase; pairing -4620 a^7 b, all a, b != 0; b = 0 is
  Theorem 1);
- x + a x^2 y + b x^2 + c x^3 y^2 (THREE-term staircase; pairing -4620 c^4);
- x + a x^3 y + b x^2 (pairing -630 a^4);
- x + a x^2 y + b x^4 y^3 (pairing -168 b^3).
Multi-edge staircases now fall at all degrees from single window certificates: route M2's
induction is no longer needed shape by shape; only a BASE certificate per shape.

## What this changes

- The program's per-shape cost of an all-degree exclusion drops to one cleared window
  solve (seconds). Theorem 5 is the special case of Theorem 6 + the EXP-042 grid
  certificates. The staircase program's remaining structural gap is exactly the
  proper-power-top case (half-plane construction, EXP-048), which is also what the
  B = 16 frontier shapes need.

## How could this be wrong?

- The kernel classification uses the standard dependence fact for binary forms
  (machine-checked at tested degrees); the extension step is EXP-046's, verified there.
- Harvest pairings with a parameter factor (e.g. -4620 a^7 b) exclude the open locus of
  that parameter; the vanishing locus falls back to the earlier theorems (stated).
