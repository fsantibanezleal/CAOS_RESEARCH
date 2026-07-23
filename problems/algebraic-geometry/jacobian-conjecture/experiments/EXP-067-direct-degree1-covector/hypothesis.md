# EXP-067 - The direct degree-1 covector (sigma-free attack on the gate)

- **Question.** Does a polynomial covector of eps-degree 1 close the reduced system
  for all interior coefficients simultaneously?
- **Motivation (the declared derivation).** EXP-064 refuted termination for the
  pivot-pinned sigma (chain stabilizes at dim 39), but sigma carries a 165-dim
  gauge freedom per solve, so the ladder framing is the wrong tool: the truncated
  covector is itself a FINITE linear object. Write Lambda(eps) = L0 +
  sum_i eps_i Lambda_i with the 51 lower coefficients eps_i. The requirement
  Lambda(eps) M(eps) = L0 M0 for all eps is EXACTLY: (order 1) Lambda_i M0 =
  -L0 M_i for each i; (order 2) Lambda_i M_i = 0 and Lambda_i M_j + Lambda_j M_i
  = 0 for i < j. Parametrize Lambda_i = P_i + N u_i (P_i any particular solution,
  N a basis of the 165-dim left kernel of M0 on the pool): the order-2 conditions
  become one sparse linear system in the 51 x 165 unknowns u, each equation
  touching at most two blocks. No sigma anywhere.
- **Falsifiable predictions.**
  1. [MV] Order-1 solvability reconfirms: all 51 particular solutions P_i exist
     (all-orders solvability, EXP-058).
  2. [MV] Every SINGLE-index block is feasible: for each i, some kernel adjustment
     achieves Lambda_i M_i = 0.
  3. [MV] Every PAIR block (i, j) is feasible in isolation.
  4. [MV] The FULL degree-1 system (all blocks simultaneously) is decided: first
     modulo two independent large primes (inconsistency mod a good prime is
     conclusive for inconsistency over Q on this integer system; consistency mod
     both primes stages an exact confirmation as a follow-up part). If consistent
     and an exact solution is produced: THE SIMULTANEOUS CERTIFICATE EXISTS at
     degree 1 and the statement-upgrade proposal goes to Felipe. If infeasible:
     degree 1 is closed honestly and degree 2 becomes the next target.
- **Method.** Exact Fraction backend on plain lists (the EXP-064 run2 lesson),
  flushed staged prints; mod-p sparse elimination for the full system's decision;
  t = 1 gauge (all t != 0 by the torus gauge). Background per the cap discipline.
- **Success criterion.** Predictions 1-4 decided by machine either way; a refuted
  prediction is a valid recorded outcome.
- **Failure criterion.** Implementation-level failure of the order-1 reconfirmation
  (would contradict EXP-058: fix before any claim).

Declared 2026-07-23 before the run.
