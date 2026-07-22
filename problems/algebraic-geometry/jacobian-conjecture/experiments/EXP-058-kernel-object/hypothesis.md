# EXP-058 - The kernel object k(t): computation, identification, annihilation (route N2)

- **Question.** EXP-057 discovered the one-dimensional right kernel of the reduced
  (72, 108) system. Compute k(t) explicitly, identify what it is, and verify the
  annihilation mechanism that the 276/276 ladder record implies.
- **Motivation (the declared derivation).** k is a Q-polygon polynomial with [P0, k]
  vanishing on the whole row pool. Since the monomial x of P0 lies OUTSIDE N(Q) (below
  the (0,0)-(2,1) edge), k cannot be affine in P0; by primitivity of P0 the exact
  bracket [P0, k] is therefore NONZERO, so it must be supported entirely OFF-pool
  (rows with i - j >= 3: the x-heavy overflow): k is a HALF-PLANE kernel object, the
  right-kernel mirror of the half-plane certificates. The annihilation condition
  rhs . k = -Lambda_prev([m, k]) = 0 should then follow the EXP-036 pattern:
  [m, k]'s pool part lies in the column space (an image of the window operator), which
  every ladder covector kills.
- **Falsifiable predictions.**
  1. [MV] The nullspace of M0 over QQ(t) is exactly one-dimensional; k(t) is computed,
     cleared to polynomial entries, and persisted.
  2. [MV] The exact bracket [P0, k] is nonzero and supported entirely off-pool
     (every monomial has i - j >= 3): the half-plane mirror.
  3. [MV] For every entering lower monomial m: the pool part of [m, k] lies in the
     column space of M0 (rank test): the annihilation has the EXP-036 shape, and
     pairing checks against Lambda0 and sampled Lambda_i give zero.
  4. [C -> D] Identification: k matches a structured candidate (a truncation of a
     bracket-commuting object built from P0; or the reduced shadow of the GGHV
     solved-case D-object); whatever structure is found is recorded and drives the
     closed-form annihilation proof.
- **Method.** sympy over QQ(t); one nullspace; exact brackets; rank tests; background
  if heavy, per the cap discipline.
- **Success criterion.** 1-3 verified: ALL-ORDERS SOLVABILITY stands [MV at the
  mechanism level, D for the general statement]; 4 recorded.
- **Failure criterion.** Kernel dimension != 1 over QQ(t) (t-jumps: map them); a
  rank test failing in 3 (then the 276/276 record has a different mechanism:
  investigate before any claim).

Declared 2026-07-22 before the run.
