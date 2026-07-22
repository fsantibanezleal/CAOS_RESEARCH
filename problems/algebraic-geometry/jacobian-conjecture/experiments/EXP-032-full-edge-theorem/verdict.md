# EXP-032 - Verdict: CONFIRMED (2026-07-22). THEOREM 3: every x-anchored edge falls

Artifact: `artifacts/output-2026-07-22.txt`. (One instrument bug caught mid-run and fixed:
the kernel scan first used the old (2, -1) weights for the u = 3 edge, whose classes live at
(2, -2); the corrected scan confirmed the prediction. Recorded, not hidden.)

## THE THEOREM (leading form unconditional; tails inherit one [D] step)

**Theorem 3.** Let z = x^k y^m (k, m >= 1) and E = x phi(z) with phi(0) != 0 and
deg phi = g >= 1 (the general weighted-homogeneous edge anchored at the vertex x, carrying
up to g + 1 monomials). Then E is never the leading form of a Keller component; and
P = E + R, for any polynomial R of strictly lower weight (degree >= 2), is never a Keller
component, at any partner degree.

Proof of the leading-form statement, in one line after the structure: on the y-class ray
g_s = x^{ks} y^{ms+1}, the operator is MULTIPLICATION,
J(E, g_s) = [(ms+1) phi(z) + k z phi'(z)] z^s [MV, symbolic coefficients], so the class
equation asks for a polynomial f with m z phi f' + (phi + k z phi') f = 1; the top
coefficient of the left side at degree D + g is (mD + kg + 1) phi_g c_D with every factor
nonzero: induction kills f, contradicting the constant. The with-tails statement uses the
Theorem-2 machinery: kernels on the kv-classes are exactly the powers E^j [MV], absorption,
and the annihilation step (inherits the [D] closed-form gap of EXP-031, with the same
verified instances pattern).

## Machine verification

1. [MV] The multiplication formula, exact, all k, m, g <= 3 with SYMBOLIC phi coefficients.
2. [MV] The univariate kill: truncated class systems inconsistent over QQ(coefficients)
   in 12 configurations; every certificate a pure power of the TOP coefficient (constants
   when the system is inconsistent independently of the lower edge coefficients).
3. [MV] Full completion windows empty for binomial AND trinomial edges, including
   perfect-square and perfect-cube phi: factorization does not rescue.
4. [MV] The QQ(a, b) certificate for the binomial edge is 60 a^3: b-free: completion is
   impossible unless the edge itself degenerates (a = 0).
5. [MV] Kernels = powers of the full edge; tails never rescue at the probes; the
   quasi-triangular control stays consistent: the x-anchored boundary is exactly right.

## What this subsumes and what remains

- Subsumes the weight-class theorem (phi = 1 + a z^g with one term) and every leading form
  of Theorem 2. The program's exclusion now reads: NO Keller component has a Newton top
  edge anchored at the linear vertex x with interior direction (k, m >= 1), regardless of
  the edge's coefficient pattern.
- Remaining open territory, honestly mapped: components must have tops of quasi-triangular
  type (pure powers of y or of a linear form after the gauge, the edges NOT anchored at x
  with both exponents positive) or leading structure outside this normalization. The
  frontier question is now sharp: classify completions whose top edge is y-anchored
  (JCB-035), where genuine components (quasi-triangular and their conjugates) live; JC(2)
  is the statement that nothing else lives there.
- The [D] gap (annihilation in closed form) now covers Theorems 2 and 3 uniformly; one
  derivation closes both (JCB-033).
