# EXP-023 - Verdict: CONFIRMED (2026-07-21). The (4,6) window is empty on the sampled slice

Artifact: `artifacts/output-2026-07-21.txt`. First run had no positive controls (an
all-inconsistent scan is exactly the vacuity trap of EXP-005/012); part C was added and the
whole suite rerun before any conclusion was drawn.

## Established results

1. **The (4, <= 6) completion window is EMPTY on the primitive slice [MV].** All 25 samples
   of P = x + P2 + P3 + a h^2 (h = xy generic-a and numeric; h = x^2 + gamma y^2 for gamma in
   {1, -1, 0}; pure, single-coefficient, and dense patterns; a != 0) admit NO Keller
   completion Q of degree <= 6 at all: the complete linear system is inconsistent every time.
   Zero primitive realizations; the divisibility prediction holds.
2. **The scan is not vacuous [MV].** Positive controls: the harness FINDS the completions of
   the quasi-triangular x + (x+y)^4 (consistent, generic degree 4, empty degree-6 region,
   exactly as the closed theory predicts) and the detector FIRES on the genuine degree-6
   realization above x + (x+y)^2 (top proportional to ((x+y)^2)^3). Both paths of the
   instrument are exercised.
3. **One descent step extends the exclusion to (4, <= 8) [D].** A degree-7 partner is
   impossible outright (top-dependence over the rank-2 base forces even partner degree), and
   a degree-8 partner has top proportional to (a h^2)^2, so one subtraction Q - c P^2 lands
   it inside the empty window. On the sampled slice there is no Keller partner of degree
   <= 8 whatsoever.

## Scope, honestly

- The exclusion is SAMPLED (25 structured points, declared), not a variety-level elimination;
  and the window is degree <= 6 (+8 by the reduction), not all degrees. The residual ladder
  is (4, 4k+2) for k >= 2: partner degree 10, 14, ... where the top is b h^{2k+1} and no
  P-power subtraction exists.
- [C, UNVERIFIED from primary sources] The literature already excludes small gcd for Keller
  pairs: gcd(deg P, deg Q) = 1 (Magnus 1955) and gcd = prime (Appelgate-Onishi 1985; Nagata),
  as cited in van den Essen's monograph. Our (4,6) emptiness (gcd 2) independently replicates
  a slice of that with a different instrument, which is a validation of the machine, not a
  new theorem. The genuinely open territory is composite gcd >= 4, first at bidegrees like
  (8, 12). Primary-source fetch of Magnus/Appelgate-Onishi is queued (JCB-029) before any of
  this is stated unhedged in the manuscript or wiki.

## Consequences

- JCB-027 closes as first contact: the primitive stratum resists at its smallest bidegrees
  for structural reasons the machine sees directly (inconsistency, not merely
  non-invertibility).
- Next (JCB-028): the (4, 10) window (25 -> 33 unknowns, still linear per sample) and a
  variety-level (not sampled) inconsistency certificate at (4, 6): eliminate the P-parameters
  too and show 1 lies in the ideal. Then the composite-gcd ladder (8, 12) with staged
  elimination.
