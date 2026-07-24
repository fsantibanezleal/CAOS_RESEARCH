# EXP-078 - The truncation ceiling: is (72,108) a FINITE decision?

- **Question.** Is there an explicit N such that a finite covector for the
  reduced (72,108) system exists IFF it exists at eps-degree <= N? Compute N.
- **Motivation (novel-approaches dossier section 1).** The covector, if it
  exists, exists at BOUNDED degree: in the joint-operator framing (EXP-064) a
  finite covector exists iff the A_i are jointly nilpotent on the Krylov
  closure V_inf of Lambda0, and joint nilpotency on a finite-dim space has
  index <= dim V_inf (= 122; ambient kernel 165). A sigma-independent ceiling
  follows from the direct systems (EXP-067/070/072/073): the covector-
  coefficient unknowns vs the order-(d+1) conditions saturate at finite d.
  THE POINT: checking support tiers through the degree implied by N DECIDES
  (72,108) either way (dossier section 0: covector => exclusion; provably no
  covector => consistency => counterexample skeleton).
- **Predictions.** 1. [MV] The Krylov closure dim (V_inf) and the ambient
  kernel dim reproduce (122, 165): a first ceiling N0 = 122. 2. [MV] The
  sigma-free rank-saturation degree d* (where the accumulated direct-condition
  rank stops growing relative to the covector unknowns) is measured: a
  SHARPER ceiling. 3. [D] Statement: 'checking through eps-degree min(N0, d*)
  decides (72,108)', converting the open sweep into a finite procedure.
- **Method.** Reuse EXP-064's Krylov machinery for N0; import the EXP-071
  direct pipeline for the rank-saturation measurement; exact/mod-p per the
  hard rules (modfrac, regression gate). Flushed; background if needed.
- **Success.** A number N and the decision-procedure statement, either way.
- **Failure.** If no finite ceiling is provable from the data, say so and keep
  the sweep open (honest null).

Declared 2026-07-24 before the run.
