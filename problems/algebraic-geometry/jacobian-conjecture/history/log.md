# Jacobian conjecture - investigation log (append-only)

## 2026-07-20 - Problem opened; counterexample validated; structure program launched

- Entry event: Alpöge/Fable N=3 counterexample announced 2026-07-19/20 (X post; no arXiv paper).
- Deep-research dossier persisted (`context/2026-07-20-deep-research-dossier.md`): statement,
  Kraus-to-Keller history, classical results ladder, equivalence cascade, the counterexample,
  secondary structural analysis (flagged UNVERIFIED), 2D status, research directions.
- **EXP-001 (confirmed):** exact validation. det JF = -2 identically; fiber over (-1/4, 0, 0) is
  exactly the 3 announced points (lex Groebner). JC(N >= 3) is false; program ground truth set.
- Decision: JC-P1 (structure + generalization) and JC-P5 (2D obstruction) run first, per Felipe's
  directive (focus on generalization and the 2-dimensional extension; explore novel approaches if
  the standing hypotheses run dry).
- Launched: EXP-002 (structure reverse-engineering, exact), EXP-003 (seed-family constructor),
  EXP-004 (2D obstruction analysis). Verdicts appended when runs complete.

## 2026-07-20 (later) - Structure owned; family generalized; 2D obstruction localized

- **EXP-002 (confirmed):** structure of F established exactly and independently: weighted scaling
  symmetry (1, -1, -2) -> (-2, -1, 1); z-linearity (u^3, 3xu^2, -x^3); reduction to invariants
  v = xy, t = x^2 z; reduced Keller identity J2 = 2 c1^2 (TWO variables); fiber cubic
  Phi(w) = w^2 - w^3 at w = u c1/2 with w-values (1, 0, 0) at the EXP-001 preimages; generating
  identity a1 = u b1/2 - u^2 + u^3 c1/2.
- **EXP-003 (partially refuted):** the v1 constructor (c1 = h(v) - t) is a degree-2 coincidence;
  for deg p >= 3 the polynomiality system is unsolvable. The d = 2 solve is sharp: the announced
  F is, up to scale k, the unique map of its shape (branch p1 = k, p2 = -3k/2, m = k^2/2,
  det = -k^3/4). Failure analysis produced the potential form (constructor v2).
- **EXP-004 (confirmed):** constructor v2 established: V' = k^2 p(w) + m s, T' = w V' - k^2 Phi(w)
  lifts, for admissible (p, k, q), to a polynomial Keller map with det = -k p(1)^2 and fiber
  degree deg p + 1; generic skew-product determinant lemma verified symbolically; NEW explicit
  counterexamples produced with exact rational collision certificates (d = 3: det -3, degrees
  (12, 11, 4); d = 4: det -350, degrees (17, 16, 4); q-tail instance degrees (8, 7, 5), beyond
  the announced family shape); exact reconstruction inverse verified modulo the fiber polynomial.
- **EXP-005 (confirmed with caveats):** 2D equivariant reduction proved symbolically (Keller
  becomes ONE univariate ODE: b1 f g' - b2 f' g = const with b1 + b2 = 1 - a); the two-invariant
  requirement localized as a proposition (one invariant -> J2 = 0 -> not Keller); no coordinate
  slice of F is Keller. CAVEATS recorded honestly: the small-degree injectivity scan was vacuous
  (0 instances; EXP-006 queued) and the collapse check is a proposition, not a discovery.
- Novel-direction pool updated (JCB-012): non-reductive symmetries (Ga-actions), no-symmetry
  searches, char-p behavior of the potential form.
