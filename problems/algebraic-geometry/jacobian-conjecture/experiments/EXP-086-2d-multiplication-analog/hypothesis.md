# EXP-086 - Does the counterexample's multiplication-construction lower to 2D?

- **Question.** The 3D counterexample is the coefficient map of (linear)x(quadratic)
  on X = {resultant=1, middle=1} isomorphic to A^3, minus the middle coord (VERIFIED).
  Does any faithful 2D analog (a variety isomorphic to A^2 + a multiplication map,
  drop a coord) produce a constant-Jacobian NON-invertible planar map, or does it
  collapse (to invertible, or to a non-smooth / non-A^2 variety)?
- **Motivation (strategy S7).** A non-collapsing 2D analog would be a counterexample
  route (S0 two-sided); a forced collapse is a structural reason JC(2) resists and
  supports our rigidity results (S7c).
- **Predictions.** 1. [MV] Regression: reproduce the 3D construction (det DG=-1,
  F_orig=BoGoA) - DONE in the session log, re-assert here. 2. [MV] The naive
  linear x linear analog with the two natural constraints (resultant ad-bc=1,
  middle ad+bc=1) is DEGENERATE (forces ad=1, bc=0: not A^2). 3. [MV/D] Search
  alternative 2D analogs (different bidegree splits; different constraint pairs;
  the SL2/unit-resultant variety with ONE constraint + a section) for a
  constant-Jacobian map; for each, compute det and test invertibility (Groebner
  inverse or fiber count).
- **Method.** Exact sympy; Jacobian determinants; invertibility via lex Groebner
  or generic fiber cardinality. Honest labels; a collapse is a valid recorded
  outcome.
- **Success.** Each candidate 2D analog decided (constant-Jac + invertible, or not
  constant-Jac, or non-A^2/degenerate).
- **Failure.** none (exploratory construction).

Declared 2026-07-24 before the run.
