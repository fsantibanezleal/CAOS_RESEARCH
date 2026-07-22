# EXP-037 - The staircase transport: the class ladder is block-triangular

- **Question.** JCB-038, the residual open core. EXP-035 relocated the obstruction from the
  corner to the STAIRCASE: the Keller constant must be manufactured along the lower-left
  Newton boundary from the swallowed linear vertex (1, 0) to the top corner. Formalize the
  transport and test whether it is over-determined.
- **Motivation (derivation, declared).** Fix the x-edge grading w = (v, 1 - u) (the class
  of the lowest staircase edge above x; sigma = v + 1 - u). Decompose P into w-classes:
  P = P_v + sum of strictly HIGHER classes (the staircase terms; strictly lower classes are
  Theorem-2 tails and are already immaterial). For a Q-monomial class t, the diagonal
  operator L_{P_v} sends class t to row class t + u - 1; every higher P-class s > v sends
  class t to row class t + s - sigma > t + u - 1. Hence, ordering Q-classes ascending, the
  window system is BLOCK-TRIANGULAR: row block r couples the NEW class t = r - u + 1
  (diagonally, via the Theorem-1/3 banded operator) with already-processed lower classes.
  Classwise elimination is therefore well-defined and yields, at each class, (i) cokernel
  obstruction equations in the kernel parameters injected so far (the TRANSPORT EQUATIONS)
  and (ii) new kernel parameters (powers of P_v on kv-classes, per EXP-031). The reduced
  system on kernel parameters is the transport chain; JCB-038 asks whether it is
  over-determined for every staircase with a mixed corner.
- **Falsifiable predictions.**
  1. [MV] (Block triangularity) For swallowed-staircase samples, every nonzero entry of the
     window matrix M sits at class offset s - sigma for some P-class s: the block-banded
     structure is exact, and all off-diagonal offsets are strictly above the diagonal one.
  2. [MV] (Transport extraction) Classwise elimination runs to completion on the minimal
     above-weight family P = x + a x^u y^v + c x^p y^q (with (p, q) of strictly higher
     w-class, forming a genuine 3-vertex staircase (1,0), (u,v), (p,q)): the reduced system
     in the kernel parameters is small (rows = coker dimensions), and its inconsistency
     reproduces the window emptiness that EXP-034/035 measured monolithically.
  3. [MV] (Localization) The first inconsistent transport equation localizes at a class
     that tracks the SECOND staircase edge (the vertex-matching classes), not the corner
     class: the obstruction is the hand-off between consecutive edges.
  4. [C] (Chain structure) On a grid over (u, v, p, q), the transport chain has nonzero
     leading coefficients with a recognizable closed pattern (the analog of Theorem 1's
     positive band and EXP-035's diagonal factor p(ib - ja)); a closed form here is the
     candidate THEOREM 5 for above-weight perturbations.
  5. [MV] (Territory) The JCB-028 residue shapes (pure slice plus ABOVE-weight lower-degree
     coefficients, e.g. x + a (xy)^2 + b x^2 and x + a (xy)^2 + b x^2 y) and further
     prescribed 3-vertex staircases all have EMPTY completion windows.
- **Method.** sympy over QQ; exact window systems (Q = y + degrees 2..N); class
  decomposition; blockwise elimination with symbolic kernel parameters; certificates for
  emptiness; numeric spot-checks wherever fraction-field steps are generic-only (EXP-024
  gotcha). Caps 570 s per part; artifacts via tee.
- **Success criterion.** 1-3 and 5 verified; 4 at least mapped empirically (pattern table).
  The transport formalization becomes the standing instrument for JCB-038.
- **Failure criterion.** A nonzero entry off the predicted class offsets (the
  triangularity claim is wrong); a consistent transport system on a mixed-staircase sample
  (candidate component: escalate immediately); classwise elimination disagreeing with the
  monolithic window verdict (instrument bug).

Declared 2026-07-22 before the run.
