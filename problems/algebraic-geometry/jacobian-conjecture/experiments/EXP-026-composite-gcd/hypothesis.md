# EXP-026 - First contact with the composite-gcd frontier: (18, <= 27)

- **Question.** JCB-030. The literature covers gcd in {1, 8}, primes, and twice-primes
  (Magnus 1954; Appelgate-Onishi 1985; Nagata); the first uncovered value is gcd = 9, whose
  minimal non-divisible bidegrees are (18, 27) (tops a h^2 vs b h^3 with deg h = 9). Does the
  machine reach that territory, and is the completion window empty there?
- **Motivation.** Everything the program proved at (4, *) replicates covered ground; this is
  the first literature-uncovered target. A certified exclusion here, even on slices and
  windows, is a bounded NEW statement. The reach is plausible because pure-slice P's are
  SPARSE (2-3 terms), so building the linear system stays cheap even with ~430 unknowns; the
  cost concentrates in exact linear algebra, which EXP-025's scaling (63 unknowns 2 s, 187
  unknowns 10 s) suggests is minutes, not hours. Structural framing: the Keller identity
  splits into homogeneous floors (Magnus's cascade); the window system is that cascade
  assembled, and pure-slice sparsity keeps every floor thin.
- **Falsifiable predictions.**
  1. [MV] (Instrument validation at scale) The certificate pipeline reproduces EXP-024's
     result when run through the same code path used here: the (4, <= 6) pure-slice pairing
     gcd is a pure a-power (cross-check, guards against a scaling bug).
  2. [MV] (Numeric window) For h = x^4 y^5 and P = x + a h^2 at numeric a in {1, -2, 1/3}:
     the (18, <= 27) completion window is EMPTY (linsolve inconsistent) at every sample.
  3. [MV] (h-shape sweep) Same emptiness for h in {x^5 y^4, (xy)^4 (x + y), x^4 y^5 + y^9}
     at a = 1 (three structurally different degree-9 bases: monomial, split-linear factor,
     binomial tail).
  4. [MV -> theorem if it lands] (Certificate) For h = x^4 y^5 with a SYMBOLIC: certificate
     pairings exist with gcd a pure a-power: the (18, <= 27) window is empty for EVERY
     a != 0. That statement is not in the literature's covered set.
  5. (Escalation clause) Any consistent sample is analyzed immediately (true degrees, top
     factorization); a genuine primitive (18, 27) realization goes to the EXP-015 checker as
     a counterexample candidate and everything else stops.
- **Method.** sympy over QQ and QQ(a): the EXP-024/025 instrument (M, rhs; cleared left-null
  pairings; gcd factorization); runtime capped 570 s per part with honest cap-out records;
  gcd-12 reach (24, <= 36) attempted only if (18, 27) is fast.
- **Success criterion.** 1-3 verified; 4 certified or capped honestly.
- **Failure criterion.** The escalation clause fires (that is the biggest possible outcome,
  not a failure of the record); or the instrument fails validation 1 (fix before anything).

Declared 2026-07-21 before the run.
