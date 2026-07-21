# EXP-022 - Verdict: CONFIRMED (2026-07-21). Quasi-triangular closure, forced alignment, and the running descent

Artifacts: `artifacts/output-{A,B,C}-2026-07-21.txt` (part A's first monolithic shape timed
out on composition blowup; restructured to generic-at-small + exact spot checks, recorded).

## Established results

1. **The shear closure holds for ANY section f [MV].** J(x + f(ell), ell/beta + H(x+f(ell)))
   = 1 identically (generic f deg <= 4, H deg <= 2), with the closed inverse verified
   (generic small; exact spot check at f deg 4, H deg 2). The quasi-triangular class is
   closed in one stroke for every f: the uniform theorem's real scope is "P equivalent to
   x + f(ell)", any degree.
2. **The (3,3) cube-case alignment is FORCED [MV].** In the ell = y gauge with P = x + A0 x^2
   + A1 xy + A2 y^2 + a y^3: the consistency ideal (7 generators) contains A0^2 a^2 and
   (after reduction) A0^2 and A1^6 with a inverted: on the variety with a != 0, A0 = A1 = 0.
   A degree-3 P with cube top admits completions ONLY in quasi-triangular form: the
   quasi-triangular conjecture holds at (3,3). (Instructive detour recorded: the ideal is not
   radical; the first membership test used the variables instead of their powers and failed
   correctly until the radical-level test was used.)
3. **The descent inverter runs [MV].** The algorithm (swap to put the smaller degree first;
   while min degree > 2, subtract c P^k whenever Q's top is proportional to a power of P's
   top; finish with the closed-form inverse; replay the elementary steps on the value side)
   explicitly inverted ALL 8 library maps (0 to 4 steps each), verified by exact composition;
   no map hit the "primitive" failure signature.

## The sharpened open core

JC(2) now reads, in machine terms: does any Keller pair hit "primitive": tops NOT
proportional to a power of the smaller top, i.e. a shared base form h of degree >= 2 with
non-power relationship? Everything else descends to min degree <= 2 and inverts by the closed
formula. The (4,6)-type shared-quadratic cases are exactly this territory; the next
experiments target the primitive stratum directly (its consistency ideals, its leading-form
constraints, and a search harness with the EXP-015 checker adjudicating).

## How could this be wrong?

- Part B is one gauge slice (cube-top, ell = y, deg Q <= 3); other (3, n) and mixed-top
  degree-3 strata are the queued sweep.
- The inverter's termination is proved only where it terminated (the library; statuses are
  explicit); "primitive" is a defined signature, not an impossibility claim.

## Consequences

- Wiki 04's machine section and the manuscript gain the uniform + quasi-triangular closures
  and the running inverter; JCB-026 advances to the primitive stratum (JCB-027).
