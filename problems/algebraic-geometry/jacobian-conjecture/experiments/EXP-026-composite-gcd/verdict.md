# EXP-026 - Verdict: CONFIRMED (2026-07-21). First exclusions in literature-uncovered territory

Artifacts: `artifacts/output-{AB,CDE}-2026-07-21.txt`.

## Established results

1. **Instrument validated at scale [MV].** The exact code path used here reproduces the
   EXP-024 certificate (gcd -8 a^2 at (4, <= 6)) before anything new is claimed.
2. **The (18, <= 27) window is empty numerically [MV].** For h = x^4 y^5, P = x + a h^2 at
   a in {1, -2, 1/3}: no Keller partner of degree <= 27 exists (403 unknowns, ~3 s per
   sample; pure-slice sparsity keeps the system cheap).
3. **The h-shape sweep is empty [MV].** Same emptiness at a = 1 for three structurally
   different degree-9 bases: x^5 y^4 (monomial, reversed exponents), (xy)^4 (x + y) (split
   linear factor), x^4 y^5 + y^9 (binomial tail).
4. **THE CERTIFICATE [MV]: for h = x^4 y^5, NO Keller partner of degree <= 27 exists for ANY
   a != 0** (312 left-null vectors, one nonzero pairing, gcd = -144 a^2, a pure a-power).
   gcd(18, 27) = 9 is outside the literature's covered set {1, 8} u P u 2P (Magnus 1954;
   Appelgate-Onishi 1985; Nagata), so this bounded exclusion is, to our knowledge, the
   program's first statement in genuinely uncovered territory.
5. **The reach extends to gcd 12 [MV].** The (24, <= 36) window (700 unknowns) is empty at
   the probe sample in 9.4 s: the full certificate at gcd 12 is within reach (queued).
6. **Rigidity novelty pass (bounded) [recorded].** Two targeted searches found adjacent work
   (Newton-polygon constraints on minimal counterexamples: Melle-Hernandez et al. line;
   quasi-homogeneous sufficient conditions for the REAL JC) but no statement of the
   equivariant rigidity theorem. Recorded in wiki 04; the full-text pass stays queued
   (JCB-031) before the manuscript calls rigidity unqualifiedly new.

## Scope, honestly

- The exclusions are pure-slice (P = x + a h^2 exactly) and windowed (partner degree <= 27,
  respectively <= 36 at one sample). Lower-order P-coefficients and higher partner degrees
  are open; the EXP-025 slice-and-union program transfers and is queued at these degrees.
- "Literature-uncovered" refers to the gcd-based coverage verified in EXP-025; Moh's
  degree-100 verification DOES numerically cover bidegrees (18, 27) as instances, so the
  honest phrasing is: uncovered by the gcd theorems, inside Moh's verified range, and our
  value is the explicit machine certificate (Moh's method is not constructive per-pair).
  A primary read of Moh's coverage claim is part of JCB-031's full-text pass.

## Consequences

- JCB-030 advances: next moves are the gcd-12 certificate (symbolic a at (24, <= 36)), slice
  widening at (18, 27), and window climbing beyond 27 (the (18, 4k+9) rungs).
- The Newton-polygon structural route gains a concrete companion: every certified window is
  a data point for where the first obstruction floor lives.
