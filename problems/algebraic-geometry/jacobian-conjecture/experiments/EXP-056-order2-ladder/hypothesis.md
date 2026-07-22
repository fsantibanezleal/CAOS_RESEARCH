# EXP-056 - The order-2 corrector ladder and the termination test (route N2)

- **Question.** EXP-055 proved first-order universality and refuted order-1
  termination. Solve the order-2 correctors (all nonzero-residual pairs) and test
  termination at order 3: if the order-3 residuals vanish, the universal polynomial
  covector is EXPLICIT and the reduced (72, 108) stratum closes.
- **Motivation (the declared derivation).** Order-2 equations: Lambda_ij M0 =
  -(Lambda_i M_j + Lambda_j M_i) (i != j; self-pairs with a single product), with the
  (2,0)-entry pinned to keep the pairing exactly 576. Efficiency: assemble ALL
  right-hand sides as columns of one matrix and run ONE gauss-jordan elimination of
  M0^T per order (the per-solve loop was the EXP-055 cost); residuals are sparse
  bracket products (pure combinatorics). Termination at order 2 means: for all
  triples, Lambda_ij M_k + Lambda_ik M_j + Lambda_jk M_i = 0, which the machine tests
  on the full nonzero set and a triple sample.
- **Falsifiable predictions.**
  1. [MV] The first-order correctors recompute in ONE matrix solve (persisted this
     time), matching EXP-055's count (26/26).
  2. [MV] All nonzero second-order residual pairs (measured over the full 351) admit
     correctors with the (2,0)-pin, in one matrix solve.
  3. [MV] The order-3 residuals VANISH on the tested triple set: termination at order
     2: Lambda(eps) = Lambda0 + sum eps_i Lambda_i + sum eps_ij Lambda_ij is the
     UNIVERSAL covector and the stratum closes (pairing identically 576).
  4. [D] If 3 fails: the ladder's growth profile is recorded (how many triples
     survive) and the next order is scheduled; the construction remains unblocked as
     long as solvability (predictions 1-2 style) persists.
- **Method.** sympy over QQ(t); one gauss-jordan per order with matrix RHS; sparse
  bracket combinatorics for residuals; parts run separately under the 590 s cap
  (background with notification if a part overruns; recorded).
- **Success criterion.** 1-2 verified; 3 answered either way (termination = closure;
  non-termination = profile + schedule).
- **Failure criterion.** An unsolvable order-2 equation (the mechanism breaks:
  investigate the row-space geometry before any conclusion).

Declared 2026-07-22 before the run.
