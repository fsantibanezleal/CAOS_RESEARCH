# EXP-019 - The Keller floors: the descent as linear algebra, and wider exhaustive certificates

- **Question.** Reroute the JC(2) attack using our own assets: the missing "second invariant"
  of dimension 2 reappears as the NEXT graded floor of the Newton expansion, and the Keller
  condition couples consecutive floors by identities LINEAR in the lower floor. How far do the
  floor identities + the bilinear harness push the exhaustive JC(2) certificates, and can the
  (2, 3) certificate be upgraded from sampled-in-P to ALL P by eliminating Q?
- **Motivation.** JCB-021 continuation. The graded decomposition of det JF = 1 gives, at each
  total degree s > 0, the floor identity sum_{i+j=s} J(P_i, Q_j) = 0; with the top forms
  degenerate (powers of a common h, EXP-013), each floor constrains the next lower forms
  h-divisibly, and every floor is linear in the unknown lower data: the classical descent is a
  staircase of LINEAR problems. This experiment certifies the framework and harvests it.
- **Falsifiable predictions.**
  1. [MV] (Floor framework) On the EXP-013 library, the graded floor identities at floors 2 and
     3 hold exactly (certifying the implementation), and the h-divisibility corollary of floor
     2 is exhibited explicitly on at least 3 maps (h from the top-form radical divides the
     stated Jacobian combination of subleading forms).
  2. [MV] (Wider exhaustive certificates) The bilinear harness (grid on the SMALLER side,
     complete linear solve on the larger) extends the JC(2) certificates to degree pairs
     (2, 4), (2, 5) and (3, 4): every clean Keller instance has in-image fiber size <= 1, with
     triangular witnesses recovered at the zero samples.
  3. [MV] (Full-A upgrade at (2, 3)) Eliminating the Q-coefficients from the linear Keller
     system by lex Groebner yields the consistency ideal in the P-coefficients alone; the scan
     of EXP-017 is then replaced by a statement over ALL P: for every P on the consistency
     variety (parametrized branches), the completions are injective on tested instances. If the
     elimination is infeasible at this size, that is recorded and the sampled statement stands.
- **Method.** sympy over QQ: graded truncations and exact divisibility for 1; the EXP-017
  harness with swapped roles for 2; lex Groebner elimination (Q-block first) for 3.
- **Success criterion.** 1 and 2 verified; 3 resolved either way (upgrade or documented
  infeasibility).
- **Failure criterion.** A floor identity fails on a library map (implementation bug), or a
  multi-point fiber appears (a planar counterexample: escalate immediately).

Declared 2026-07-21 before the run.
