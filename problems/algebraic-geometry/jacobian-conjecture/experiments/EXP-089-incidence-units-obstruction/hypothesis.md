# EXP-089 - The incidence mechanism CANNOT give a planar counterexample

- **Question.** The full geometric derivation (Tao-ChatGPT) reduces the 2026
  counterexample to: X_H = {(L,Q): Res(L,Q)=1, [LQ]_next=1}, with pi(L,Q)=LQ
  etale (generically n:1); it yields a Keller counterexample IFF X_H ~ A^n
  (observation (c), the only dimension-specific miracle). Does (c) hold in dim 2?
- **Motivation.** If X_2 is provably NOT A^2, the entire incidence/root-selection
  mechanism (the exact structure of the dim-3 counterexample) cannot produce a
  planar counterexample - a clean, complete exclusion of this class for JC(2).
- **Predictions.**
  1. [MV] dim 2: L,Q both linear; {Res(L,Q)=1, [LQ]_{TS}=1} = {x*delta=1,
     beta*gamma=0}, which is REDUCIBLE (two components), hence NOT A^2.
  2. [MV] finite-root chart: X_2 = A^2 minus the discriminant hyperbola
     {2 c2 zeta + 1 = 0}; (2 c2 zeta + 1) is a nonconstant UNIT, but O(A^2)^*=C^*,
     so X_2 != A^2 (units invariant, no deep classification needed).
  3. [D] contrast: dim 3 the same construction gives smooth irreducible X_3 ~ A^3
     (toric/unimodular). The discriminant-complement is affine space in dim 3 but
     provably not in dim 2.
- **Method.** Exact symbolic (sympy); the constraint solve + the units argument.
- **Success.** X_2 != A^2 established [MV] two independent ways.
- **Failure.** none.

Declared 2026-07-24 before the run.
