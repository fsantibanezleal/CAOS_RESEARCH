# EXP-035 - The corner is diagonal; the obstruction is the staircase

- **Question.** JCB-037. EXP-034 found the mixed-corner certificate is MULTI-ray. Locate the
  coupling: is the corner top itself the hard object, or is it the staircase of Newton
  vertices connecting the swallowed linear vertex x = (1, 0) up to the top corner?
- **Motivation (derivation, declared).** For B = x^i y^j (i, j >= 1) and G = x^a y^b:
  J(B^p, G) = p (i b - j a) x^{ip + a - 1} y^{jp + b - 1}. This is DIAGONAL: one monomial in,
  one monomial out, coefficient p(ib - ja), kernel exactly {(a, b) parallel to (i, j)} =
  powers of B. So the corner operator is clean; a pure high corner cannot even reach the
  constant (output exponents ip + a - 1, jp + b - 1 are never both 0 for i, j >= 1, a, b >=
  0 except degenerate). Therefore the constant of a Keller component with a swallowed x and
  a mixed top must be produced along the STAIRCASE from x to the corner, and the multi-ray
  coupling is the staircase, not the corner. This relocates the open core to a concrete
  combinatorial object (the lower-left Newton boundary), the classical "Moh staircase".
- **Falsifiable predictions.**
  1. [MV] (Diagonal formula) J(B^p, x^a y^b) = p(ib - ja) x^{ip+a-1} y^{jp+b-1} exactly on
     a grid of (i, j, p) and (a, b); kernel on each homogeneous class is exactly powers of B.
  2. [MV] (Corner cannot make the constant) For i, j >= 1, no monomial G gives J(B^p, G) a
     nonzero constant term (checked on the grid): the constant needs lower structure.
  3. [MV] (Staircase mapping) For swallowed-mixed samples (x + x^2 + x^2 y and kin, all
     window-EMPTY), record the Newton polygon vertices and the lower-left staircase from
     (1, 0) to the top; verify the certificate's support lattice tracks the staircase band
     (the coupling follows the staircase), not a single ray.
  4. [MV] (Territory widened) A wider monomial-corner scan (B in {xy, x^2 y, x y^2, x^2 y^2,
     x^3 y}, p <= 2, several fillers): every completion window EMPTY, extending the mapped
     exclusions; any consistent sample escalates.
- **Method.** sympy over QQ; exact Jacobians; window linsolve; Newton-polygon vertex
  extraction (lower-left hull); certificate support extraction. Caps 570 s.
- **Success criterion.** 1-4 verified; the reframe recorded: corner clean/diagonal, core =
  staircase; JCB-037 refocused on the staircase transport (new branch JCB-038).
- **Failure criterion.** A diagonal-formula mismatch (derivation wrong); a consistent
  monomial-corner sample (escalate: candidate component).

Declared 2026-07-22 before the run.
