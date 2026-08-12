# EXP-021 - conductor fiber cone and canonical Cohen--Macaulayization

Status: DECLARED before formal implementation or execution on 2026-08-12.

## Question

For `p>=4`, does the special fiber `C_p=F(T_p)` canonically realize the Cohen--Macaulay quotient
of the Buchsbaum tangent cone, and what is its exact Artinian socle?

## Falsifiable predictions

- P1: `T_p^2=m_pT_p`, hence `T_p^(n+1)=m_pT_p^n` for all `n>=1`.
- P2: the natural surjection `G_p -> C_p` has kernel exactly `H^0(G_p)=m_p/T_p`, so
  `G_p/H^0(G_p) isomorphic to C_p` as graded algebras.
- P3: over `F_p=k[x_p]`, the free-shift vector is `(1,10p-1,12p,2p-1,1)`.
- P4: `C_p` is Cohen--Macaulay with Hilbert function
  `(1,10p,22p,24p-1,24p,24p,...)`, multiplicity `24p`, regularity four, and `a=3`.
- P5: for `B_p=C_p/(x_p)`, the socle vector is `(0,0,10p,0,1)`. Thus the type is
  `10p+1`, and `C_p` is neither level nor Gorenstein.

## Premise dependencies

EXP-013 and EXP-016--020 supply the exact conductor, power profiles, minimal reduction, tangent-cone
Hilbert series, full torsion, and Noether-normalization module. Any failed premise invalidates this
experiment's deductive conclusion.

## Required proof and evidence

1. Prove the square identity from the closed value blocks and derive all higher identities.
2. Prove the natural graded-algebra kernel statement degree by degree.
3. Derive the module, Hilbert, Cohen--Macaulay, regularity, and `a`-invariant statements.
4. Compute the Artinian reduction's basis and prove its exact socle blocks and type.
5. Run two exact routes for `p=4,...,300`, beginning with a mandatory `p=4` smoke gate.
6. Independently rebuild selected parameters, verify all-row hashes, and run adversarial controls.

## PASS, FAIL, and one-sidedness

- A finite computational PASS validates the implementations only; the infinite theorem requires
  the symbolic block and kernel proofs.
- Any mismatch at `p=4` refutes the affected formula and stops the campaign. Any later mismatch
  also refutes the formula as stated and must be preserved.
- `CONFIRMED` requires the symbolic proof, both exact routes, all controls, stable row hashes, and
  the independent audit.

## Invariant-first design

The decisive invariant is the square equality `T_p^2=m_pT_p`. It turns an abstract
Cohen--Macaulay quotient from EXP-019/020 into the natural fiber-cone algebra. The finite Artinian
reduction then decides type, levelness, and Gorensteinness without a defining-ideal computation.

## Exact routes

- Route A: reconstruct `Gamma_p`, `T_p`, `m_p`, their monomial ideal products, minimal generators,
  multiplication by `t^(24p)`, the quotient basis, and its socle directly from values.
- Route B: evaluate the closed block formulas, the induced Hilbert and free-shift formulas, and
  the predicted socle blocks without importing Route A's intermediate sets.
- Independent audit: rebuild `p=4,5,17,73,151,300` and recompute the aggregate from all stored
  row hashes.

## Adversarial controls

- delete one value from `m_pT_p`, forcing a false square identity;
- inject a positive-degree element into the kernel of `G_p -> C_p`;
- change `mu(T_p^2)` from `22p` to `22p-1`;
- delete one degree-two socle element;
- mark a degree-three basis element as socle;
- replace type `10p+1` by the false Gorenstein value one.

Every corruption must be rejected.

## Compute budget and verdict rule

CPU only, exact integer/set arithmetic, no randomness. The full campaign budget is two minutes and
the audit budget is one minute. No checkpoint is required because rows are independent and cheap.
Budget exhaustion yields `INCONCLUSIVE`, never a negative mathematical verdict.
