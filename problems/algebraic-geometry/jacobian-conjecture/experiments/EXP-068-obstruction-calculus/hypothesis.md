# EXP-068 - The obstruction calculus (the scalar functional; toward degree 2)

- **Question.** Make the truncation obstruction EXPLICIT as one linear functional
  and decide the degree-2 prerequisites: can the level-1 gauge be chosen so that
  ALL order-2 blocks become solvable, and does a degree-2 covector then survive a
  sufficient order-3 probe?
- **Motivation (the declared derivation).** The pool system has rank 124 of 125:
  the cokernel is spanned by ONE covector c (the consistency row of the
  Gauss-Jordan transform). A vector equation V = 0 mod im(M0) holds iff c.V = 0:
  every block of every truncation degree carries exactly one scalar obstruction.
  EXP-067's refutation says: for 8 operators, c annihilates the reachable set
  (c^T B_i = 0) while the particular scalar c.(P_i M_i) is nonzero. Degree 2
  changes the game: the 2e_i and e_i+e_j conditions no longer need to VANISH,
  only to be SOLVABLE (their scalar obstruction must vanish so that
  Lambda_{alpha} exists at level 2), and the new binding conditions move to
  order 3.
- **Falsifiable predictions.**
  1. [MV] The functional test reproduces EXP-067 exactly: c^T B_i = 0 AND
     c.(P_i M_i) != 0 precisely for the 8 blocked operators.
  2. [MV] The LEVEL-1 GAUGE SYSTEM (choose u, 51 x 165 unknowns, so that all
     1377 order-2 scalar obstructions vanish, making every level-2 corrector
     exist) is decided mod two primes. Prediction: FEASIBLE (the 1377 conditions
     sit in 8415 unknowns and the pair couplings were all individually feasible).
  3. [MV] With a u-solution FIXED from 2, the SUFFICIENT order-3 probe (choose
     the level-2 gauge v so that all order-3 scalar obstructions vanish) is
     decided mod p. Feasible: a degree-2 covector candidate exists (exact
     confirmation staged as the follow-up; the statement upgrade would go TO
     FELIPE after the exact pass). Infeasible: NOT conclusive against degree 2
     (u was fixed); the joint (u, v) decision is staged as the follow-up.
- **Method.** Exact Fractions for c, P_i, B_i; sparse mod-p elimination for the
  gauge systems (primes 2147483629, 2147483587); flushed staged prints;
  background per the cap discipline. t = 1 gauge throughout.
- **Success criterion.** 1-3 decided by machine either way; refuted predictions
  recorded.
- **Failure criterion.** Prediction 1 failing (would contradict EXP-067: an
  implementation bug; fix before any claim).

Declared 2026-07-23 before the run.
