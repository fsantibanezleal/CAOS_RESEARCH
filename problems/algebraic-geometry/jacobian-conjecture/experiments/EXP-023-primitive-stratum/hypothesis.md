# EXP-023 - First contact with the primitive stratum: the (4,6) scan

- **Question.** The open core of JC(2) after EXP-022 is the primitive stratum: pairs whose
  tops share a base form h of degree >= 2 without a power relationship (smallest bidegrees
  (4, 6): P_top = a h^2, Q_top = b h^3, h quadratic of rank 2). Does ANY Keller pair realize
  exact primitive bidegrees (4, 6)?
- **Motivation.** JCB-027. If JC(2) holds, the classical divisibility fact for planar
  automorphisms (deg P | deg Q or deg Q | deg P) forbids exact bidegrees (4, 6) entirely, so
  the linear completion system must never realize them; conversely a genuine primitive
  completion is a counterexample candidate that the EXP-015 checker adjudicates on the spot.
  Either outcome is decisive content: a mapped exclusion zone, or the find.
- **Falsifiable predictions.**
  1. [MV] (rank-2 scan, h = xy) For P = x + P2 + P3 + a (xy)^2 over structured coefficient
     samples with a != 0: the complete linear solution set in Q (deg <= 6) NEVER contains a
     completion with true degree 6 whose top is b (xy)^3 (b != 0). Consistent samples may
     exist, but their completions all have true deg Q < 6 or degenerate top data.
  2. [MV] (rank sweep control) Same scan with h_gamma = x^2 + gamma y^2 for gamma in
     {1, -1, 0}: the gamma = 0 (rank 1) control behaves as the quasi-triangular theory
     predicts (any consistent completions are f(ell)-shaped, degree a multiple of 4 or < 6);
     no primitive (rank-2) realization appears at any gamma.
  3. (Escalation clause) Any sample realizing exact (4, 6) with rank-2 top base is
     immediately adjudicated by jclib.jc2.check_keller2 and fiber-tested; if it survives,
     this is a JC(2) counterexample candidate and everything else stops.
- **Method.** sympy over QQ: the bilinear harness (complete linear solve in Q per P-sample;
  ~25 unknowns, fast); per consistent sample, enumerate solution branches, instantiate frees,
  measure TRUE degrees and top factorization (is Q_top proportional to h^3?); counters for
  everything (no silent drops).
- **Success criterion.** Predictions 1-2 verified over the declared sample sets, with counts
  reported; the exclusion statement is sampled (declared), not exhaustive.
- **Failure criterion.** The escalation clause fires (that is not a failure but the biggest
  possible outcome; it just ends the scan).

Declared 2026-07-21 before the run.
