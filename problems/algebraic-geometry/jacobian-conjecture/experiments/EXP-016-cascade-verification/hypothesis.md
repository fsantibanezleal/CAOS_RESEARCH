# EXP-016 - Consequence-cascade verification from primary sources (literature experiment)

- **Question.** The program has carried UNVERIFIED flags on the consequence cascade since day 1
  (context dossier section 4): which implications toward the Jacobian conjecture are actually
  stated in the primary literature, in which direction, and what exactly follows now that
  JC(N >= 3) is false?
- **Motivation.** JCB-009 / JC-P4. Methodology 03: claims imported from literature must be
  re-verified from the primary source before any conclusion depends on them; the wiki and the
  manuscript currently label the cascade UNVERIFIED.
- **Falsifiable predictions** (each resolved by reading the primary record: statement located
  and its direction confirmed, or the flag stays):
  1. Mathieu 1997 states a conjecture on integrals over compact connected Lie groups whose
     truth FOR SU(N) would imply JC(N); hence its SU(3) case is now false.
  2. Derksen, van den Essen and Zhao state the Gaussian moments conjecture and prove that GMC
     (in the relevant dimension family) implies JC; hence GMC fails at some finite dimension.
  3. Zhao's vanishing conjecture (Hessian nilpotency) is proved EQUIVALENT to JC; hence false.
  4. Van den Essen, Wright and Zhao's Image conjecture implies the vanishing conjecture; hence
     false in some dimension.
  5. Tsuchimoto 2005 and Belov-Kanel & Kontsevich 2007 prove the STABLE equivalence between the
     Dixmier conjecture and JC (Dixmier_N implies JC_N; JC_2N implies Dixmier_N); hence the
     full Dixmier conjecture is now false, with the smallest failing Weyl dimension open.
  6. Bass-Connell-Wright 1982 state the degree reduction (JC reduces to degree 3 / cubic
     homogeneous in stably many variables), and the inverse-formal-expansion setting; the
     precise statement is recorded for the future push-through experiment.
- **Method.** WebFetch of primary sources (arXiv/DOI/journal pages); the verdict records, per
  item: the located statement (with its exact reference), the implication direction, and the
  resulting corollary status. No computation; this is a literature experiment under the same
  record discipline.
- **Success criterion.** Each item resolved to verified-with-source (flag lifted) or explicitly
  kept UNVERIFIED with the reason (source unavailable / statement differs).
- **Failure criterion.** A cascade claim turns out misstated in our record (then the dossier,
  wiki and manuscript are corrected immediately; that correction is the result).

Declared 2026-07-21 before the run.
