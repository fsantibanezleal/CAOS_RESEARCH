# EXP-060 - The forced-family certificate (route N2, the scope-corrected closure)

- **Question.** EXP-059 showed a single constant minor does not exist over the FULL
  26-coefficient stratum. Scope correction: the GGHV Prop 4.3 reduction forces the
  corner and edge structure of the reduced P, so the closure only needs certificates
  over the LOW-DIMENSIONAL forced family. Compute the fully symbolic cleared
  certificate there.
- **Motivation (the declared derivation).** The reduced N(P) has corners (8,14) and
  (8,16) on its right edge; the forced family includes the top edge y^8 (xy - t)^8
  and the corner coefficients as the structural parameters. A cleared covector with
  polynomial entries over QQ(t, beta[, gamma]) and pairing a NONZERO polynomial in
  the parameters (nonvanishing on the stratum t != 0, corner coefficients as forced)
  closes the whole family at once: with GGHV's Prop 4.3, the (72, 108) case is
  discarded and the floor rises to 125, modulo the dossier's edge-shape transcription
  caveats (stated; the verbatim verification is the assembly checklist's remaining
  branch).
- **Falsifiable predictions.**
  1. [MV] The two-parameter family P = x + y^8 (xy - t)^8 + beta x^8 y^14 has a
     cleared H-certificate with c^T M = 0 identically in (t, beta) and pairing a
     nonzero polynomial in (t, beta) (candidate: a monomial or beta-free form).
  2. [MV] The three-parameter extension (+ gamma x^8 y^15, the second right-edge
     point) likewise, budget permitting (degrade to numeric-gamma slices with the
     (t, beta)-symbolic certificate re-verified per slice; recorded).
  3. [MV] The pairing's vanishing locus intersected with the stratum's constraints
     (t != 0; forced-nonzero corners) is EMPTY: the forced family is CLOSED at all
     parameters.
  4. [D] Assembly statement: with 1-3 and Prop 4.3, the (72, 108) case is discarded
     [conditional on the dossier's edge-shape transcription, verbatim verification
     queued]: the JC(2) floor rises from 108 to 125. Felipe validates the claim's
     phrasing before any outreach.
- **Method.** sympy over QQ(t, beta[, gamma]); the H-restricted reduced system;
  cleared covectors with polynomial identity verification; background runs per the
  cap discipline.
- **Success criterion.** 1 and 3 verified (2 as budget allows): the forced family
  closes; 4 stated with its exact conditionality.
- **Failure criterion.** A pairing that vanishes on a locus INSIDE the stratum:
  adjudicate that locus directly (per-point solve); a genuinely consistent point is
  a candidate counterexample and escalates immediately.

Declared 2026-07-22 before the run.
