# EXP-087 - The incidence construction in dim 2: why it degenerates

- **Question.** The geometric derivation (Tao-ChatGPT) recasts the 3D
  counterexample as pi|X: X -> Y where pi: P^1 x Sym^2(P^1) -> Sym^3(P^1) chooses
  one root of a binary cubic, X = (P^1 x Sym^2) \ (R u pi^-1 H) ~ A^3, Y = Sym^3 \
  H ~ A^3, with H tangent-but-NOT-osculating to the small diagonal (twisted
  cubic). Does the d=2 analog produce a planar counterexample or degenerate?
- **Motivation.** If it degenerates for a STRUCTURAL reason, that reason is new
  evidence JC(2) resists; if not, it is a construction route. The conversation's
  own reframe: JC = (elementary incidence geometry giving X -> A^n etale deg n)
  + (recognition X ~ A^n). In dim 2 the recognition step is TRACTABLE (surface
  classification: Miyanishi-Sugie characterization of A^2), unlike the open
  dim-3 miracle.
- **Predictions.**
  1. [MV] For the degree-d rational normal curve, a hyperplane with contact
     order exactly 2 that is NON-osculating requires 2 < d (osculating = contact
     d, Borel stabilizer). For d=2 the small diagonal is a CONIC: every tangent
     line has contact exactly 2 = d = osculating (Borel). So the 3D construction's
     essential ingredient has NO faithful d=2 analog; the 2D case is forced into
     the regime the 3D construction explicitly excluded.
  2. [MV] Algebraic shadow: the two normalizing constraints (resultant=1,
     middle=1) that cut a smooth A^3 in 3D COINCIDE in 2D (ad-bc=1 with ad+bc=1
     => ad=1, bc=0, a singular hyperplane, not A^2). EXP-086's degeneracy is
     exactly this.
  3. [D] Residual symmetry: 3D H=2p+q (distinct) -> torus G_m (the (-2,-1,+1)
     weights); 2D H=2p (forced double) -> Borel. Any G_m-equivariant planar
     Keller map is LINEAR by our published 2D equivariant rigidity theorem
     (foundational manuscript, EXP-010) => no counterexample from this
     construction in 2D.
- **Method.** Contact/stabilizer analysis; exact algebra of the slice; cite our
  rigidity theorem. Honest labels.
- **Success.** The d=2 degeneration explained structurally (predictions 1-2 [MV],
  3 [D]).
- **Failure.** none (structural analysis).

Declared 2026-07-24 before the run.
