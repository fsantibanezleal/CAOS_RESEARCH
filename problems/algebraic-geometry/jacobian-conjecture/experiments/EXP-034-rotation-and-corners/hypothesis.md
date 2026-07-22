# EXP-034 - The rotation induction stress-tested; first contact with the mixed-corner core

- **Question.** JCB-036 first data, PLUS the strategic audit Felipe asked for: is the
  rotation induction sound and where exactly does it stop? Design analysis (declared): the
  induction step works when the standard top form of the leading pair member is a power of a
  LINEAR form (rotate it onto y, then the de Jonquières subtraction, our descent, reduces
  degree). It CANNOT work when a top is a power of a genuinely mixed base (x^al y^be
  corner): rotation preserves mixedness. Those mixed-corner pairs are exactly the classical
  hard shapes (Moh's candidate list); Theorem 4 does not cover them when x is swallowed. So
  the useful frame is: rotate-descend until linearized OR until a mixed top appears (the
  "hard shape" signature); then attack mixed-corner shapes directly with windows and
  certificate anatomy.
- **Falsifiable predictions.**
  1. [MV] (Rotate-descent, the induction's data) The algorithm (while degree > 1: factor
     the top of the larger-degree member; if it is c ell^d with ell linear: rotate ell to y
     and apply the descent subtraction; else STOP "hard shape") fully LINEARIZES every pair
     of the deterministic library, with no hard-shape stops: the induction closes on all
     known components.
  2. [MV] (The uncovered territory is real, and it resists) Swallowed-mixed P shapes
     (x not a vertex of N(P), standard top a mixed monomial or mixed-based form), which
     Theorem 4 does NOT cover, e.g. x + x^2 + x^2 y, x + x^2 + x^3 y, x + (x+y)^2 + x^2 y^2,
     x + x^2 + x^2 y^3: completion windows are EMPTY at every sample. Any CONSISTENT sample
     is analyzed immediately (it is a component of a new kind or an error; either decisive).
  3. [MV] (Anatomy at the new territory) For two inconsistent swallowed-mixed shapes, the
     certificate vector's support localizes on few rows (recorded): first data toward a
     corner-anchored closed form (the mixed-corner analogue of the multiplication
     structure).
- **Method.** sympy over QQ; the descent inverter extended with a rotation step (gauge
  bookkeeping: rotations act on the source, compositions tracked and verified by exact
  composition at the end); window scans; certificate anatomy. Caps 570 s.
- **Success criterion.** 1-3 verified; the strategic audit recorded: the induction's exact
  domain (linear-base tops) and its exact stopping signature (mixed corners) stated in the
  record, with the mixed-corner territory mapped as the program's true residual core,
  converging with the classical hard-shape picture but now carrying new instruments.
- **Failure criterion.** A library pair that stops (the induction claim is wrong for known
  components: fix the algorithm or the claim); a consistent swallowed-mixed sample
  (escalate: candidate new component).

Declared 2026-07-22 before the run.
