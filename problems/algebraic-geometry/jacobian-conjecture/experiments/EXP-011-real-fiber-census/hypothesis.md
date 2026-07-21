# EXP-011 - Real fiber census of F: the 1-or-3 structure over the discriminant surface

- **Question.** Over the reals, how many preimages does the announced map F have, where, and
  what does that make F as a real object?
- **Motivation.** JC-P2 (geometry) + the future web visualization: F has rational coefficients,
  so F restricts to a real polynomial map R^3 to R^3 with CONSTANT Jacobian determinant -2 (an
  orientation-reversing local diffeomorphism everywhere). The fiber polynomial
  W(w) = 4 Phi(w) - w BC + A C^2 is an odd-degree (cubic) real polynomial in w, and EXP-007
  proved escapes happen exactly at multiple roots. This predicts a sharp real census.
- **Falsifiable predictions.**
  1. (Census rule) For real targets with C != 0 off the discriminant surface D = 0: the number
     of REAL preimages equals the number of real roots of W: 3 or 1. Verified at sample targets
     by two independent exact routes (real-root isolation of W + reconstruction, versus direct
     Groebner fiber and real-root isolation of the eliminant).
  2. (Both regions inhabited) Explicit rational targets exist with exactly 3 and with exactly 1
     real preimage; the sign of D separates them at the tested samples (record the empirical
     sign rule).
  3. (Real surjectivity) F(R^3) = R^3: every real target has at least one real preimage.
     Reason [D]: W is an odd-degree real polynomial (leading coefficient -4, constant in the
     target), so it always has a real root; off D = 0 all roots are simple, hence reconstruct
     finite real preimages; on D = 0 and on C = 0 the flat sheet or the surviving simple root
     provides the point (EXP-007 exhibited both). Certified on a rational grid of targets.
  4. (Recorded corollary, not ours in substance) Since F is defined over Q, the real
     restriction is a non-injective real Keller map: the constant-Jacobian real analogue of the
     Jacobian conjecture in dimension 3 falls with the same example (Pinchuk's 1994 real
     counterexample had NON-constant Jacobian). This is immediate from the announcement plus
     EXP-001; stated for the record with the census quantifying it.
- **Method.** sympy over QQ: exact real-root isolation (Sturm-based real_roots) of W per
  target; reconstruction per real root; independent Groebner fiber + real-root count of the
  z-eliminant for cross-validation; a 3x3x3 rational target grid for surjectivity.
- **Success criterion.** Predictions 1-3 verified exactly (4 is a recorded corollary).
- **Failure criterion.** A target where the two routes disagree (reconstruction bug or theory
  gap; escalate), or an empty real fiber (refutes 3).

Declared 2026-07-21 before the run.
