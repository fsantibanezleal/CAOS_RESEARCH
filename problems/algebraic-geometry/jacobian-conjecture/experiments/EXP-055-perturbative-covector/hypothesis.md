# EXP-055 - The perturbative covector Lambda(eps) (route N2, the closure attempt)

- **Question.** Build the polynomial covector Lambda(eps) whose existence EXP-054's
  refutation pointed to: if it terminates at low order with target-row entry fixed at
  576, the reduced (72, 108) stratum closes UNIVERSALLY (all t, all lower
  coefficients).
- **Motivation (the declared derivation).** M(eps) = M0 + sum eps_i M_i (each M_i the
  sparse bracket contribution of one lower lattice point); rhs is the CONSTANT x^2
  vector (Q0 has no base term, so [P, 0] - x^2 = -x^2 independent of P). Ansatz
  Lambda(eps) = Lambda0 + sum eps_i Lambda_i + sum eps_i eps_j Lambda_ij + ...;
  order-by-order: Lambda_i M0 = -Lambda0 M_i (solvable per i or the route fails
  there), with the normalization Lambda_i[(2,0)] = 0 so the pairing stays EXACTLY 576.
  Termination at order k (all order-(k+1) residuals zero) gives an explicit polynomial
  covector: search the correctors on a RESTRICTED row set (near the supports and their
  eps-shifts), then VERIFY GLOBALLY as a polynomial identity.
- **Falsifiable predictions.**
  1. [MV] rhs is the constant x^2 vector (P-independent).
  2. [MV] Every first-order equation is solvable (all entering lower points), with the
     (2,0)-normalization; supports stay localized.
  3. [MV] The series terminates by order 2 on the tested batches (second-order
     residuals solvable or zero), and the assembled Lambda(eps) passes the GLOBAL
     residual identity on symbolic batches.
  4. [D] Assembly: with 2-3 on all batches, the stratum closes universally; whatever
     batch resists is recorded as the exact residue.
- **Method.** sympy over QQ(t, eps-batch); restricted-search + global-verify; caps
  570 s per part; degradations recorded.
- **Success criterion.** 1-3 verified on the full entering set or an explicitly listed
  majority: the universal certificate (or its precise residue) on record.
- **Failure criterion.** A first-order equation unsolvable (route fails at that
  monomial: record; try the second pairing-nonzero covector as Lambda0 before
  concluding).

Declared 2026-07-22 before the run.
