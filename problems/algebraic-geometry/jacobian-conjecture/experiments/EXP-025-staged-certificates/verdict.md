# EXP-025 - Verdict: CONFIRMED (2026-07-21). Slices, windows, a locus, and the sources

Artifacts: `artifacts/output-{A,B,C,D,E,F}-2026-07-21.txt`.

## Established results

1. **Every 2-parameter slice is empty [MV].** For each single lower coefficient s: the
   (4, <= 6) window is empty for ALL (a != 0, s arbitrary). Six slices certify by pure
   a-power gcds (16a^2, 8a^3, -8a^3, 384a^4, 1024a^6, -128a^4); the p30 slice's gcd is
   27s^3 and its unresolved locus {s = 0} lies (radical membership s^3) inside the pure
   slice that EXP-024 emptied: covered by union.
2. **Every 3-parameter pair slice is empty [MV].** All 21 pairs of lower coefficients:
   certified directly or by the union argument ((s u)^k in the pairing ideal with a
   inverted, so every unresolved point falls in an already-certified smaller slice).
3. **The windows climb the ladder [MV].** On the pure slice P = x + a (xy)^2: NO Keller
   partner of degree <= 10 (pairing -128 a^4), <= 14 (-256 a^5), <= 18 (-1024 a^6), for ANY
   a != 0. The rungs (4,10), (4,14), (4,18), where the descent has NO reduction move, die on
   the pure slice. The exponent pattern (2, 4, 5, 6 at windows 6, 10, 14, 18) is recorded;
   a closed-form all-degree certificate is conjectured [C] and queued.
4. **The E-candidate locus closed [MV].** Part E (35 triple slices) surfaced one genuine
   candidate: on p20+p21+p03 the pairing gcd 192 a^4 (4 a s - u^2)^2 vanishes on
   {4 a s = u^2}, exactly where s x^2 + u x^2 y + a x^2 y^2 is a perfect square, i.e. the
   translation orbit (y -> y + u/2a) of pure-slice points, which the slice family does not
   contain. Probed per the declared escalation clause: 9 numeric locus points all
   INCONSISTENT; the (1,2,1) point family certified for ALL w (gcd = the constant 12); and
   the ENTIRE locus at once via the polynomial parametrization a = al^2, u = 2 al be,
   s = be^2: gcd = 12 al^6, pure al-power. Part E closes completely: 35/35.
5. **The sources are verified [was C, now closed: JCB-029].** Magnus, Proc. Amer. Math. Soc.
   5 (1954), 256-266: gcd of the degrees equal 1 implies automorphism (the year 1955 in
   earlier records was wrong; corrected). Appelgate-Onishi, J. Pure Appl. Algebra 37 (1985),
   215-227, with Nagata: gcd prime; refined coverage gcd in {1, 8} u P u 2P. The plane
   conjecture is classically EQUIVALENT to the divisibility statement, i.e. exactly the
   primitive-stratum framing of this machine. Consequence, stated honestly: ALL rungs
   (4, 4k+2) have gcd 2 (a prime), so the entire (4, *) ladder is classically covered; our
   certificates on it are independent machine replications (validation), not new theorems.
   The genuinely open gcd values start at 9 and 12: bidegrees like (18, 27) and (24, 36).

## How could this be wrong?

- Slice certificates cover up to 3 lower coefficients on; the full 8-parameter statement
  remains open (the capped EXP-024 part B); 4-coefficient slices and beyond are queued.
- The union arguments rely on radical membership computed by Groebner reduction (exact).
- The open-gcd analysis depends on the cited theorems' exact statements; both citations were
  read from secondary confirmation of the primary metadata (abstract/venue), not the full
  proofs; the full-text pass stays queued before the manuscript asserts them as its own
  foundation (they are context, not load-bearing for our machine results).

## Consequences

- JCB-028 refocuses: the (4, *) ladder is literature-covered; the machine frontier moves to
  composite gcd (9, 12): bidegrees (18, 27) / (24, 36) are beyond direct elimination today,
  so the route is structural (leading-form constraints + staged slices at those degrees).
- The web app now exposes every experiment record in full (clickable feed and log entries
  opening a modal with hypothesis, verdict, artifacts): the record is readable in place.
