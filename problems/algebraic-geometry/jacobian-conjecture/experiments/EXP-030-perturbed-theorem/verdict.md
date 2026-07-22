# EXP-030 - Verdict: PARTIALLY REFUTED, THEN DECISIVE (2026-07-22). Injectivity fails; the theorem survives

Artifact: `artifacts/output-2026-07-22.txt`.

## What was refuted, honestly

Prediction 2 (injectivity of L_top on every class) is FALSE: on the classes of weight kv,
L_top has a 1-dimensional kernel, spanned (obviously in hindsight) by P_top^k, since
J(P_top, P_top^k) = 0. The proposed one-step downward induction breaks there. This is the
record working as designed: the naive proof died in public, and its corpse pointed at the
correct one (kernel absorption + annihilation: EXP-031).

## What was established

1. **Coupling structure [MV].** Every lower-weight monomial feeds the constant's row only
   from classes STRICTLY ABOVE the y-class; the shift formulas are exact.
2. **Empirics all hold [MV].** Perturbed full windows are inconsistent at every sample
   (tails of several shapes, including what EXP-031 later identified as danger weights);
   the quasi-triangular control x + (x+y)^2 stays consistent: the theorem's boundary is
   real (components with x-power/linear-base tops escape the hypothesis, as they must).
3. **The obstruction is b-free [MV].** Certificates over QQ(a, b) for safe tails: pairing
   gcds are pure a-powers.
4. **Beyond every floor, perturbed [MV].** The degree-135 instance with a degree-102
   lower-weight tail falls by the unchanged y-class chain.

## Consequences

- The refutation reshaped the proof into: absorption of kernel components as H(P_top) +
  the ANNIHILATION LEMMA for the induced sources. EXP-031 tests exactly that and closes it.
