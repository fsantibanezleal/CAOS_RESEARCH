# EXP-039 - The (3, n) column: coverage closure + the explicit (3, 4) machine loop

- **Question.** JCB-021's remainder: the staged (3, 4) elimination and the (3, n) strata.
  Close the column honestly: what does the literature already cover, and what does the
  machine add explicitly?
- **Motivation (derivation, declared).** gcd(3, n) is 1 or 3 for every n. gcd 1 is Magnus
  1954; gcd 3 is prime, Appelgate-Onishi 1985 / Nagata. So EVERY (3, n) bidegree pair is
  classically covered (with (3, 3) also machine-closed by EXP-022). The staged elimination
  JCB-021 queued is therefore replication; its value is the explicit constructive loop at
  (3, 4): the consistency variety in P and explicit inverses, the analog of EXP-019/020's
  (2, n) closure. The leading-form theory predicts the consistency-at-the-top condition:
  J(P_3, Q_4) = 0 with 3, 4 coprime forces P_3 = c ell^3 (a perfect CUBE), the exact
  analog of the (2, 3) discriminant-square ideal.
- **Falsifiable predictions.**
  1. [MV] (Top force by elimination) For generic symbolic P_3 (4 coefficients), the linear
     map Q_4 -> J(P_3, Q_4) (6 x 5) is rank-deficient iff P_3 is a perfect cube: the 5 x 5
     minors' ideal and the cube-locus ideal (vanishing Hessian covariant) have the same
     zero set (checked by substitution of the cube parametrization + non-cube samples +
     Groebner-level containment where cheap).
  2. [MV] (Cube stratum completes and inverts) On the cube stratum (rotated gauge
     P = x + c y^3 + P_2), sampled P_2: whenever the exact bidegree-(3, 4) window is
     consistent, the extracted pair is Keller and has a POLYNOMIAL inverse (lex Groebner
     inverse extraction); no consistent sample fails to invert.
  3. [MV] (Non-cube emptiness) Every sampled P with non-cube top form has an EMPTY exact
     (3, 4) window; spot replications at (3, 5) and (3, 7) too.
  4. [D] (Column coverage) The coverage table (n -> gcd -> covering theorem) closes the
     (3, n) column for all n; recorded with the machine's role stated as replication plus
     explicit inverses.
- **Method.** sympy over QQ; symbolic minors; Groebner containment checks; exact window
  solves at bidegree (window = partner degree exactly); Groebner inverse extraction
  (lex, small degrees). Caps 570 s per part.
- **Success criterion.** 1-3 verified, 4 recorded; JCB-021 closes (remaining strata are
  coverage-subsumed; the machine loop is validated at (3, 4)).
- **Failure criterion.** A rank-deficient non-cube P_3 (the force claim is wrong); a
  consistent sample with no polynomial inverse (ESCALATE: that would be a JC(2)
  counterexample at bidegree (3, 4), contradicting Magnus; instrument bug far more likely).

Declared 2026-07-22 before the run.
