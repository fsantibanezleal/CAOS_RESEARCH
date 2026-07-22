# EXP-059 - The determinantal certificate (route N2, the closure reframe)

- **Question.** Close the reduced (72, 108) stratum WITHOUT the corrector ladder:
  with the kernel exactly the constants (EXP-058), rank M(eps, t) <= 124 always, so
  inconsistency for ALL parameters follows from ONE 125 x 125 minor of the augmented
  matrix [M | r] (r the x^2 vector, its row included) that never vanishes. The
  constant-576 pairing across strata predicts the strongest form: the minor is
  CONSTANT.
- **Motivation (the declared derivation).** Inconsistency at a parameter point means
  rank[M | r] = rank M + 1; since rank M <= 124 everywhere (constants in the kernel
  for every P), a nonvanishing 125 x 125 augmented minor certifies inconsistency
  pointwise; if the minor is a nonzero constant (or c t^k, nonvanishing for t != 0),
  the ENTIRE stratum closes in one determinant: no termination lemma needed. The
  ladder's role collapses into this single object.
- **Falsifiable predictions.**
  1. [MV] At the base point (eps = 0, t = 1), rank[M | r] = 125; a 125-row selection
     is extracted (r's row included).
  2. [MV-sampled] The selected minor's determinant is THE SAME rational number at
     ~40 random parameter points (mixed eps directions, several t): the constancy
     phenomenon.
  3. [MV] Axis constancy, symbolic: the determinant with t as the only symbol
     (eps = 0) is constant; and with a single eps_i as the only symbol (t = 1) it is
     constant for each tested eps_i (as many of the 26 as fit the budget
     symbolically, the rest at 3-point numeric slices).
  4. [D] Assembly: 1-3 give THE DETERMINANTAL CERTIFICATE at [MV/D] strength (axis
     constancy symbolic + mixed-direction sampling; the full multilinear expansion
     stated as the residual): the reduced stratum closes; then the edge branch; then
     the floor-raise.
- **Method.** sympy; numeric dets (fast) + single-variable Bareiss dets; background
  for the symbolic parts per the cap discipline.
- **Success criterion.** 1-2 verified; 3 at least substantially covered; 4 stated
  with the exact residual.
- **Failure criterion.** A parameter point where the minor vanishes (then rank[M|r]
  can drop there: test inconsistency directly at that point before any conclusion;
  a genuinely consistent point would be a candidate counterexample and is escalated
  immediately).

Declared 2026-07-22 before the run.
