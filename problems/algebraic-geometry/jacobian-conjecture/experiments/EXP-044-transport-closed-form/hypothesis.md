# EXP-044 - The transport chain's closed form (route N1)

- **Question.** JCB-038's last step. EXP-042 proved Theorem 5 in window form with cleared
  pairings -c_N a^N at windows N = 5..9. What is the law behind c_N, and can the
  obstruction be made window-INDEPENDENT (the all-degree Theorem 5)?
- **Motivation (derivation, declared).** Two views of the same obstruction: the
  NORMALIZED transport elimination (EXP-037) reported the constant-class equation as
  -2a = 0 at every tested window, while the CLEARED certificate (EXP-042) pairs to
  -c_N a^N. Hypothesis: the normalized constant-class equation is IDENTICALLY -2a (for
  u = 2 shapes), independent of the window; the growing exponent and constant c_N are
  exactly the clearing factors of the classwise eliminations (each class contributes one
  factor of a and a rational unit). If the normalized form is window-independent and the
  clearing factors are units for a != 0, the inconsistency persists at every window: the
  all-degree Theorem 5 follows with a [D] induction whose step is the incremental
  structure of window growth (new top-degree classes feed only FORWARD in the
  triangular order, so they cannot repair the constant's row).
- **Falsifiable predictions.**
  1. [MV-generic] (Window independence of the normalized form) The transport elimination
     at (u, v, d) = (2, 1, 2) gives constant-class equation -2a = 0 at EVERY window
     N = 5..13; at (2, 2, 2) the analogous constant-class equation is likewise
     window-independent.
  2. [MV] (The clearing law) The cleared pairing at window N is -c_N a^N with
     c_N/c_{N-1} a positive rational whose factorization tracks the new top class (the
     sequence 420, 1260, 13860, 180180, ... continues with positive ratios; measured to
     N = 11 at least).
  3. [MV] (Certificate coherence) The cleared certificate at window N + 1, restricted to
     the rows of window N, is proportional to the window-N certificate (one common
     ratio): the certificates form a coherent tower, the machine form of the induction
     step.
  4. [D] (The induction skeleton) New degree-(N+1) unknown classes inject strictly
     forward in the triangular order (their diagonal rows sit at classes the constant's
     row does not reference backward): stated and machine-checked on the class
     bookkeeping for N -> N + 1, N = 6..10.
- **Method.** Self-contained copies of the transport elimination (EXP-037) and cleared
  certificates (EXP-042); symbolic (a, b) runs; caps 570 s per part.
- **Success criterion.** 1-3 verified, 4 checked: Theorem 5 all-degree is stated [D]
  (window-independent normalized obstruction + coherent certificate tower + forward-only
  injection), with the residual gap to unconditional stated precisely (the tower
  proportionality proven for all N, not just verified at tested N).
- **Failure criterion.** A window where the normalized constant-class equation changes
  form (the law is wrong); a non-proportional certificate restriction (no tower: the
  induction skeleton dies and the closed form must come another way).

Declared 2026-07-22 before the run.
