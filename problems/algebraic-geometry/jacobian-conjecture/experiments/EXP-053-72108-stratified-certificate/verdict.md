# EXP-053 - Verdict: CONFIRMED; the stratified certificates land with a CONSTANT pairing (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## Findings

1. **[MV] The stratified certificates.** On the reduced (72, 108) system with the
   forced top edge y^8 (xy - t)^8 SYMBOLIC and three lower strata (bare; x y^4
   filler; y^3 + x^2 y^6 fillers), the H-restricted system (threshold i - j <= 2,
   289 rows) carries a cleared covector with c^T M = 0 identically in t and pairing
   THE CONSTANT 576: nonzero for EVERY t, and IDENTICAL across the sampled lower
   strata (55-92 s per stratum).
2. **[MV] Support economy.** The certificate is supported on FIVE rows only: the
   target row (2,0) and the short ray (9,16), (16,32), (17,33), (18,34): the
   obstruction is a compact structural object, the same anatomy as the Theorem-1
   chains, and a closed-form derivation looks within reach.
3. **[D] What remains for full closure of (72, 108).** (a) Determine which lower
   monomials enter the five support rows at all (if none for generic lower
   coefficients, the 576-certificate is UNIVERSAL on the stratum and the case
   closes); (b) the sweep over the remaining forced-structure parameters from the
   dossier (lambda1, alpha edges); (c) assemble with GGHV Prop 4.3 to state the
   floor-raise to 125. This is next round's first task, now concrete and small.

## How could this be wrong?

- Three lower strata sampled; universality rests on the support-entry analysis (a).
- The top-edge shape is the dossier's transcription (verified against the LaTeX
  sources; normalization caveats flagged there).
