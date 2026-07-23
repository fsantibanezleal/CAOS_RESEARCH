# EXP-063 - The interior sweep and the orientation remark (route N2, the mechanical endgame)

- **Question.** Complete the remaining mechanical steps of the (72, 108) closure:
  every interior lattice point of the reduced N(P) with its coefficient SYMBOLIC (one
  at a time, t = 1 gauge), and the orientation swap.
- **Motivation.** EXP-062 opened the upgrade with constant pairings (368640) at four
  points; the sweep extends it to all remaining interior points. The (0,0) point is
  trivially free (brackets kill constants: the P-constant never enters the system).
  The orientation: (108, 72) is the SAME reduced object read in the other order: if
  [P, Q] = x^2 then [Q, P] = -x^2, and the sign is absorbed by Q -> -Q (linear), so
  consistency is orientation-invariant: a remark plus one machine spot-check, not a
  new family.
- **Falsifiable predictions.**
  1. [MV] Every remaining interior point admits the one-symbol certificate at t = 1
     with a nonzero polynomial pairing (expected: constants/monomials, per the
     pattern).
  2. [MV] The orientation spot-check: the sample system with target -x^2 has the
     same EMPTY verdict as with x^2.
  3. [D] The assembly document is drafted (program/jacobian-conjecture/
     72108-closure-statement.md): the claim, its exact evidence chain
     (EXP-052..063), its stated generality (axis-symbolic + dense-sample interior
     coverage; the simultaneous-symbolic statement flagged as the honest residual),
     and the conditionalities: FOR FELIPE'S VALIDATION, nothing leaves the repo.
- **Method.** sympy over QQ(eps); ~22 one-symbol H-certificates (background, per the
  cap discipline); one linsolve spot-check.
- **Success criterion.** 1-2 verified; 3 drafted.
- **Failure criterion.** An interior point whose pairing vanishes on a locus inside
  the stratum: adjudicate that locus directly before any claim; escalate genuine
  consistency immediately.

Declared 2026-07-22 before the run.
