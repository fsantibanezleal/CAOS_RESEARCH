# EXP-027 - The gcd-12 certificate: (24, <= 36)

- **Question.** JCB-030(a). Certify the second uncovered composite gcd: for h = x^5 y^7
  (deg 12 base), does P = x + a h^2 admit NO Keller partner of degree <= 36 for ANY a != 0?
- **Motivation.** EXP-026's probe showed the numeric window empty in 9.4 s at 700 unknowns;
  the (18,27) numeric-to-symbolic scaling (3 s to 82 s) predicts the symbolic run lands
  inside the 570 s cap. gcd(24, 36) = 12 is outside the coverage set {1, 8} u P u 2P.
- **Falsifiable predictions.**
  1. [MV] (Validation) The code path reproduces EXP-026's (18, <= 27) certificate gcd
     (-144 a^2) before the new claim.
  2. [MV] (The certificate) At (24, <= 36), h = x^5 y^7, a symbolic: pairings exist with gcd
     a pure a-power: no partner of degree <= 36 for any a != 0. Cap-out documented if hit.
  3. (Escalation) A consistent point goes to the checker; everything stops.
- **Method.** The EXP-024/025/026 certificate instrument, unchanged; cap 570 s.
- **Success criterion.** 1 exact; 2 certified or honestly capped.
- **Failure criterion.** Escalation fires, or validation fails (fix first).

Declared 2026-07-21 before the run.
