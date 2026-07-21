# EXP-027 - Verdict: CONFIRMED (2026-07-21). The gcd-12 certificate

Artifact: `artifacts/output-2026-07-21.txt`.

## Established results

1. **Validation [MV].** The exact code path reproduces EXP-026's (18, <= 27) certificate
   (gcd -144 a^2) before the new claim.
2. **THE CERTIFICATE [MV]: at (24, <= 36), h = x^5 y^7, NO Keller partner of degree <= 36
   exists for ANY a != 0** (1261 equations, 700 unknowns, 561 left-null vectors, one nonzero
   pairing, gcd = -80 a^2; 227 s). gcd(24, 36) = 12 is the second value outside the
   literature's coverage set {1, 8} u P u 2P; both uncovered composite gcds (9 and 12) now
   carry certified pure-slice exclusions.

## Scope, honestly

- Pure slice and windowed, as in EXP-026; and (24, 36) also sits inside Moh's degree-100
  verified range, so the new content is the explicit certificate, not the truth. The
  beyond-Moh design (JCB-030(d), gated on JCB-031's read of Moh's exact claim) is where the
  program can state something nobody has verified in any form.

## Consequences

- The certificate instrument now spans 25 to 700 completion unknowns with the SAME code
  path and single-pairing outcomes (one obstruction dominates every window tried); wiki 04
  gains the second certificate; JCB-030 continues with slice widening and window climbing.
