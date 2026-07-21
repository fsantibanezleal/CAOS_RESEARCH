# EXP-024 - Verdict: CONFIRMED (2026-07-21). A sound all-a certificate on the pure slice

Artifacts: `artifacts/output-{A,B}-2026-07-21.txt`.

## Established results

1. **Instrument refuted and rebuilt first.** The first attempt (fraction-field RREF of the
   augmented system) produced the obstruction row 0 = 1: NORMALIZED, hence sound only
   generically (the division by f(a) is invalid exactly where f vanishes). The pass was
   rejected and the instrument replaced by cleared left-null certificates: polynomial vectors
   c with c^T M = 0 as an identity, so f = c^T rhs evaluates soundly at EVERY parameter point.
2. **Pure-slice theorem [MV].** For P = x + a (xy)^2: eleven left-null vectors, one nonzero
   pairing, gcd = -8 a^2. Since -8 a^2 vanishes only at a = 0: for EVERY a != 0 there is NO
   Keller partner of degree <= 6. This upgrades EXP-023's generic-a inconsistency to all
   nonzero a, closing the exceptional-locus gap on this slice.
3. **Full-parameter certificate CAPPED [honest].** The 25 x 36 nullspace over the 8-parameter
   fraction field exceeded the 540 s cap with no partial output (EXP-020 precedent). The
   all-parameter statement rests, for now, on EXP-023's 25-sample scan plus this slice
   theorem; staged variants are queued (mixed numeric/symbolic slices, bilinear block
   elimination) in JCB-028.

## How could this be wrong?

- The certificate argument is one-directional by design: f(a0) != 0 proves inconsistency at
  a0; nothing here claims completeness of the certificate set (not needed: gcd is a pure
  a-power, so every a0 != 0 is covered by the single pairing).
- The theorem is the PURE slice only; lower-order P-coefficients could in principle open a
  consistent stratum that the 25 samples missed. That is exactly what the capped part B would
  decide.

## Consequences

- Wiki 04/05 and the manuscript gain the slice theorem; JCB-028 keeps the staged
  full-parameter certificate and the (4, <= 10) window as the next moves.
