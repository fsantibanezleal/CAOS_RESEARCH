# EXP-042 - Theorem 5 push: cleared all-parameter certificates for the staircase family

- **Question.** JCB-038 continuation. EXP-037's transport is generic (fraction-field
  steps). Upgrade to SOUND all-parameter certificates for the minimal staircase family
  P = x + a x^u y^v + b x^d, and measure window-robustness of the obstruction: the two
  ingredients of a THEOREM 5 (above-weight perturbations never rescue).
- **Motivation (derivation, declared).** EXP-024's discipline: a covector c with
  POLYNOMIAL entries satisfying c^T M = 0 as a polynomial identity in (a, b) gives a
  pairing f(a, b) = c^T rhs that evaluates soundly at EVERY parameter point; if f is a
  nonzero constant times a power of a alone, the window is empty for every a != 0 and
  EVERY b (with b = 0 being Theorem 1's case anyway). The annihilation lemma (EXP-036) is
  P-agnostic (pure Leibniz), so the window criterion (sources with in-window preimages
  pair to zero) should transfer verbatim to this family; if the pairing is also
  window-STABLE (same closed form at every N), the all-degree statement has the same
  shape as Theorems 1-3's closure.
- **Falsifiable predictions.**
  1. [MV] (Cleared certificates on the grid) For (u, v, d) on the EXP-037 grid at window
     N = 7: a cleared polynomial covector exists with c^T M = 0 identically and pairing
     f(a, b) = (nonzero rational) * a^i * b^j; when j = 0 the certificate excludes ALL b.
  2. [MV] (Window stability) For (u, v, d) = (2, 1, 2), the pairing at windows N = 5..9
     has the SAME closed form up to nonzero rational scale (the analog of the banded
     chain's window-independence).
  3. [MV] (Annihilation transfers) For this family, J(m, P^k) = -k L(P^{k-1} m) holds
     (it must: Leibniz) and the certificate pairing of a source vanishes exactly when
     the preimage P^{k-1} m fits the window (spot grid).
  4. [MV] (General above-weight tails) Sampled P = x + a x^u y^v + R with R a SUM of
     two or three above-weight monomials (numeric coefficients): windows empty; for one
     two-term R, a cleared 3-parameter certificate.
- **Method.** sympy over QQ(a, b) with cleared covectors (lcm of denominators, content
  removed, identity re-verified polynomially); windows 5..9; caps 570 s per part
  (degrade N before capping out; record any degradation).
- **Success criterion.** 1-3 verified (4 at least sampled): Theorem 5 gets its
  window-form statement (all parameters, certified windows) and the two closure
  ingredients are demonstrated; the remaining gap to all-degree is stated precisely.
- **Failure criterion.** No cleared certificate at some grid point (the transport
  degenerates somewhere: locate it); a pairing with mixed sign structure that vanishes
  on a nontrivial (a, b) locus (would mean a candidate completion locus: escalate).

Declared 2026-07-22 before the run.
