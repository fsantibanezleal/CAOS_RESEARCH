# EXP-020 - The JC(2) machine, run: eliminations at (2,4)/(3,4) and the full (2,3) theorem attempt

- **Question.** Run the machine established by EXP-019 on the next degree pairs, and attempt
  the upgrade at (2, 3): parametrize the consistency variety, solve the completion
  symbolically, and construct an EXPLICIT polynomial inverse for the complete family, turning
  the certificates into a theorem: every normalized (2, 3) Keller map is invertible.
- **Motivation.** JCB-021. The (2, 3) consistency ideal is (4 A0 A2 - A1^2)^2: the variety is
  P's quadratic part being a perfect square, parametrized by P2 = (alpha x + beta y)^2. On
  that locus the completion is linear; if the resulting two-parameter family has an explicit
  inverse, JC(2) at (2, 3) is PROVED (in the affine gauge, hence in general), by construction.
- **Falsifiable predictions.**
  1. [MV] (2, 4) elimination: the consistency ideal in the quadratic side is computed; the
     theory predicts it is again supported on the discriminant locus 4 A0 A2 - A1^2 = 0 (the
     leading-form degeneracy is degree-independent); the computed ideal's radical membership is
     checked against that prediction.
  2. [MV] (3, 4) elimination attempted; completed ideal reported, or the failure documented
     with sizes (the honest record either way).
  3. [MV] (The theorem attempt) With P2 = (alpha x + beta y)^2 symbolic: the linear system for
     the cubic completion is solved over QQ(alpha, beta); for every branch, an explicit
     polynomial inverse G with F o G = id and G o F = id is constructed and verified exactly
     (symbolically in alpha, beta and the residual frees). If verified: every normalized
     (2, 3) Keller map is invertible: JC(2) holds at (2, 3) as a THEOREM with an explicit
     inverse, not a sampled certificate.
- **Method.** sympy over QQ and QQ(alpha, beta): lex Groebner eliminations; symbolic linear
  solves; inverse construction by triangular peeling (undo the linear-form shear) verified by
  exact composition.
- **Success criterion.** 1 and 3 verified; 2 resolved either way.
- **Failure criterion.** A branch with no polynomial inverse (then the fiber structure of that
  branch is analyzed immediately: it would be a counterexample candidate; escalate).

Declared 2026-07-21 before the run.
