# EXP-088 - The incidence family across n: why n=3 is exceptional and dim 2 is excluded

- **Question.** In the incidence family pi_n: P^1 x Sym^{n-1}(P^1) -> Sym^n(P^1)
  (choose one root of a degree-n form), for which n is the normalized source
  X_n isomorphic to A^n? Where does dim 2 sit?
- **Motivation (S8/S9, Tao-ChatGPT geometric derivation).** The counterexample is
  pi_3|X_3 with X_3 ~ A^3. X_3's G_m-grading (weights 1,-1,-2) has invariant ring
  C[a,b] (a=xy,b=x^2z) and A = C[x,a/x,b/x^2], a semigroup algebra whose generators
  form a UNIMODULAR basis (det 1) => A^3. The higher-n normalized slice is a
  generalized Danielewski core D_n = {x^{n-2}W = B^{n-2}-1} times A^{n-2}, with
  n-2 boundary components; Cl(X_n) rank ~ n-3. Only n=3 has a LINEAR core (n-2=1)
  and trivial class group.
- **Predictions.**
  1. [MV] 3D toric semigroup (weights 1,-1,-2) is unimodular (det 1) => X_3 = A^3.
  2. [MV] D_n core has n-2 components; n=3 linear (=A^2 => X_3=A^3), n>=4 not A^n
     (Cl rank ~ n-3), n=2 degenerate (n-2=0: the construction is below its own
     exceptional case).
  3. [MV] Residual torus needs H cap Delta = 2p+q (2 support pts) => n=3 only;
     n=2 conic tangent = 2p (Borel, excluded); n>=4 finite stabilizer.
  4. [D] n=3 is the UNIQUE sweet spot; dim 2 excluded from BELOW. No
     incidence-type planar counterexample; consistent with our G_m-rigidity
     theorem (EXP-010).
- **Method.** Exact toric/lattice determinants; Danielewski-core boundary count;
  support-point stabilizer analysis. Honest labels.
- **Success.** The exceptionality of n=3 and the exclusion of n=2 established [MV].
- **Failure.** none (structural).

Declared 2026-07-24 before the run.
