# EXP-022 - Quasi-triangular closure, the cube case at (3,3), and the descent inverter

- **Question.** Push the frontier at min degree 3 along three fronts: (A) the shear closure
  generalizes to ANY section polynomial f; (B) at (3,3), the non-proportional-top case forces
  quasi-triangular alignment; (C) the classical descent, restated on our machine, becomes an
  ALGORITHM that explicitly inverts planar Keller maps, with a precise failure signature that
  localizes the remaining open core of JC(2).
- **Motivation (the assembly insight, to certify).** At equal top degrees the leading forms
  are Jacobian-dependent homogeneous of the SAME degree, hence proportional; subtracting the
  right multiple of P from Q kills Q's top and strictly reduces degree. Iterating (with
  power/composition subtractions when deg h = min degree) descends any Keller pair toward min
  degree <= 2, where EXP-021 inverts in closed form; composing the elementary steps back
  yields an explicit inverse. JC(2) is then EXACTLY the claim that the descent never sticks
  (no "primitive" pair with shared base deg h >= 2 and no reduction move): the open core gets
  a machine-checkable failure signature.
- **Falsifiable predictions.**
  1. [MV] (A: closure for any f) J(x + f(ell), ell/beta + H(x + f(ell))) = 1 identically for
     generic symbolic f (deg <= 4, no constant/linear term) and H (deg <= 2); the closed
     inverse (ell = beta (v - H(u)), x = u - f(ell), y = (ell - alpha x)/beta) composes to the
     identity (generic at small degrees; exact spot checks higher).
  2. [MV] (B: the cube case at (3,3)) In the conjugation gauge ell = y: for
     P = x + A0 x^2 + A1 xy + A2 y^2 + a y^3 (a != 0), eliminating Q (deg <= 3) yields a
     consistency ideal that forces the quasi-triangular alignment A0 = A1 = 0 (P = x + A2 y^2
     + a y^3, i.e. P = x + f(y)); the triangular witnesses live there.
  3. [MV] (C: the descent inverter) The algorithm (normalize; while min degree > 2: if tops
     proportional subtract the multiple, else if Q-top = multiple of a power/composition of
     P-top's base subtract it, else STOP "primitive"; finish with the EXP-021 closed inverse;
     compose back) explicitly inverts EVERY map of the deterministic library, verified by
     exact composition; no library map hits "primitive".
- **Method.** sympy over QQ; generic identities; the ell = y gauge elimination (11 variables,
  feasible); the inverter as tested library code (jclib) run over keller2lib.library().
- **Success criterion.** 1-3 verified; the "primitive pair" failure signature is defined in
  code and documented as the residual open core.
- **Failure criterion.** A library map the inverter cannot invert (bug or genuine
  obstruction: escalate immediately); a (3,3) completion OFF the quasi-triangular locus
  (would refute the alignment conjecture: analyze it as a counterexample candidate).

Declared 2026-07-21 before the run.
