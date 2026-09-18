# EXP-017b - The loci bounds in the s-variable model (the Dias-Pan-faithful reformulation)

Declared: 2026-08-02, BEFORE any run. Successor to EXP-017 per its verdict:
the premature elimination of the inverse-cube differences inflated the
minors to degree near 100; Dias-Pan kept those quantities as ring variables
and their analogous subideal bases completed in minutes. This experiment
adopts their variable model exactly.

## The ring and ideal

Variables: the nine quotient distances + heights (h1, e12, f) + ONE
s-variable per distinct unordered pair of distance names appearing as an
inverse-cube difference in the reduced block (enumerated mechanically from
the block structure; expected around 21, giving a ring of about 34
variables, the Dias-Pan C^32 scale) + t.

Ideal SH_s: the EXP-017 shape quadrics + E1 + gauge r12 = 1 + the defining
relations s_{ab} * a^3 * b^3 - (b^3 - a^3) = 0 for each s-variable over its
pair (a, b) (sparse, degree 7) + the saturation t * (product of the nine
distances) * f - 1. Each matrix entry is now a sum of terms
(sign) * s_{ab} * Delta with Delta quadratic in (wA, wB, h1, e12, f):
BILINEAR entries, no clearing, 4x4 minors of degree about 12 instead of
100.

## Predictions

- P0a (smoke): dim(SH_s gauged) = 4, two-way agreement (the s's are
  function-field elements of the distances, so the dimension must not move).
- P0b (smoke): the s-model matrix, evaluated at W1 with the exact s-values
  computed from the distances, agrees entrywise with EXP-016's
  coordinate-built matrix. Any mismatch stops everything.
- P1..P4 (the four loci bounds): dim(SH_s + all 4x4 minors) <= 3;
  + all 3x3 <= 2; + all 2x2 <= 1; + all entries <= 0. Full Singular std at
  600 s caps; per-minor pgb fallback at 120 s where the full basis walls;
  two-way agreement wherever complete. The reformulation gain is measured
  against EXP-017's all-caps baseline.
- Declared outcome classes per rung: BOUND MET / BOUND NOT MET (that k then
  needs the sign-analysis lemma, declared separately) / INCONCLUSIVE-CAP.

## Preflight (methodology/12)

- Source-complete: everything is our own verified construction plus the
  Dias-Pan model read in full; no [U] premise.
- Smoke: P0a + P0b before any minor is trusted.
- One-sidedness: BOUND NOT MET is a real declared outcome; caps honest.
- Invariant-first: per-rung dimensions, minor degrees, wall times, and the
  gain factor vs EXP-017.
- Budget and kill: 4 x 600 s full attempts + up to (15 + 80 + 90 + 24) x
  120 s fallbacks; no extensions; rungs independent.

## Consequence ladder

- ALL FOUR LAND: the Lemma 7.3 chain closes dim(Omega_stratum) <= 4 =
  generic finiteness for the k = 2, p = 2 stratum off equal heights. STOP:
  the exact statement wording goes to Felipe FIRST, before any record
  beyond the verdict.
- Some rung BOUND NOT MET: the sign-analysis lemma for that k (Dias-Pan
  Prop 7.2 pattern) is declared as its own follow-up.
- Caps again: the loci route is walled in both formulations at our budgets;
  the chain waits on either bigger declared budgets or the witness-set
  instrument, recorded honestly.
