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

## 2026-07-20 (session 2) - 2D scan real; asymptotic variety explicit; degree laws; char p

- **EXP-006 (confirmed):** the 2D equivariant scan is now NON-vacuous (valuation-aware ansatz):
  382 branches, 216 polynomial Keller instances, 648 in-image fibers, ALL single-preimage.
  Sharper than predicted: every surviving instance is LINEAR (six shapes, all diagonal/swap
  forms). Within the window (a <= 3, |b1| <= 3, deg <= 3) nothing nonlinear even exists.
- **EXP-007 (confirmed):** family theorem: W'(w) = k^2 p(w) - BC and s = -W'/m, so escape roots
  are EXACTLY multiple fiber roots. A(F) = {C = 0} union
  {27 A^2 C^2 - 18 A B C + 16 A + B^3 C - B^2 = 0} (discriminant surface). Concrete escape
  verified end to end: fiber over (0, 1, 1) is the single point (2, -1/2, 9/8); generic C = 0
  fibers are the single flat-sheet point; the collision target has a full 3-point fiber
  (collisions are generic, not asymptotic).
- **EXP-008 (confirmed):** degree law (5d-3, 5d-4, 4) for d = 2..5; fiber-degree floor 3;
  q-tails strictly increase degrees; k never changes them; hence (7, 6, 4) = the announced F is
  degree-minimal WITHIN the family. NEW fiber-degree-6 counterexample: seed w - 3w^5, k = 5,
  det = -20, degrees (22, 21, 4), rational collision (-1/70, 75, 399000) and
  (1/160, -150, -3824000) to (-750, -750, 1). Global minimality (degrees 3..6) remains open.
- **EXP-009 (confirmed):** P3 reduces mod 13 and 101 to explicit non-injective Keller maps over
  F_ell of degree 12 < ell (collision certificate survives reduction). Explicit certificates
  the char-p literature could not have before July 2026.

## 2026-07-21 (session 3) - 2D rigidity becomes a THEOREM; real census done

- **EXP-010 (confirmed):** 2D equivariant rigidity proved for ARBITRARY weights: equivariant
  components are monomial times f(v); det factors through a bracket identity (648 symbolic
  checks); Keller forces the (x f, y g)/swap shapes (mixed shapes: empty solve); the Keller ODE
  fg + v(w1 fg' + w2 f'g) = c kills all nonconstant (f, g) via the strictly positive factor
  1 + w1 dg + w2 df (empty constrained solves, 8 weight pairs, bidegrees to 5). Every
  Gm-equivariant Keller map of C^2 is LINEAR. The wiki-04 conjecture is upgraded to a theorem;
  a 2D counterexample, if any, must be genuinely non-equivariant.
- **EXP-011 (confirmed):** real fiber census of F: 1 or 3 real preimages, separated by the
  discriminant wall (D > 0: 3; D < 0: 1); two independent exact routes agree at all samples; no
  empty real fiber on a 36-target grid (real surjectivity; odd-degree argument). Recorded
  corollary: F|_R^3 is a surjective, orientation-reversing, non-injective real Keller map
  (constant-Jacobian real analogue in dimension 3 falls with the same example).

## 2026-07-21 (session 4) - The landscape: the m = 2 mechanism is unique

- **EXP-012 (confirmed 1-4, REFUTED 5):** the weighted mechanism landscape for weights
  (1, -1, -m). Determinant lemma + pairing reductions certified generically (orders m - 1 along
  the section). m = 1 is the JC(2) bridge class: 93 instances, all injective (a collision there
  would refute JC(2)). m = 3: the (-2, -2, 1) class is EMPTY (valuation proof at the origin);
  (-3, -1, 1): 60 instances, all injective. m = 4: the potential-form family does NOT exist:
  Groebner emptiness certificate (seed degree <= 5, gauge Q0 = 1, mu != 0 Rabinowitsch). The
  parity-law design hypothesis is refuted; the finding is UNIQUENESS: within everything
  scanned, the announced counterexample's weight system is the only collision-capable weighted
  mechanism. Instrumentation lessons recorded (t-free sections; auxiliary-symbol filters).
- Diffusion updated (Felipe direction): house-style carousel rebuilt (card 1 = origin + our
  findings strip), post v3 with the uniqueness item and hashtags.
- Felipe reminder logged: M3 web app (GitHub Pages) is next; ADR-0016/0017/0056/0057/0058 bind
  the shell, header/footer, references and page structure.

## 2026-07-21 (session 5) - Toward JC(2): the cascade foundation + literature debt cleared

- **EXP-013 (confirmed 1-2, partial 3):** the leading-form cascade. On a library of real Keller
  maps: at EVERY sampled ray, the weighted leading pair is Jacobian-dependent with a common
  radical form: every planar Keller map is, ray by ray, the degenerate boundary of the EXP-010
  equivariant classification (the certified bridge between our rigidity theorem and the
  classical Newton-polygon program; 56 (map, ray) checks). Exhaustive JC(2) verified at (2, 2)
  in the affine gauge (2 branches, all injective). HONEST: (2, 3)/(3, 3) unresolved: sympy's
  empty solve at (2, 3) is a solver artifact (explicit triangular witness exists); a
  triangular-decomposition harness is queued (JCB-021). A naive two-floor coprime kill was
  discarded before running (floor 2 admits solutions).
- **EXP-016 (confirmed):** the consequence cascade verified from primary sources and the flags
  lifted: Mathieu SU(N) => JC(N) (Mathieu 1997; review arXiv:2511.16561; DvdK abelian 1998),
  GMC => JC (arXiv:1506.05192), vanishing <=> JC (arXiv:math/0409534, 0704.1691), Image =>
  vanishing (arXiv:1006.5801), Dixmier stably equivalent (arXiv:math/0512171; Tsuchimoto 2005).
  Corollaries now assertable: Mathieu false for SU(3); GMC false; vanishing false; Image false;
  full Dixmier false with Dixmier(1) open and smallest failing rank in {1, 2}. New target:
  an explicit failing Hessian-nilpotent quartic (queued).
- Queued honestly (budget): EXP-014 Puiseux escape obstructions (JCB-022) and EXP-015 JC(2)
  certificate checker + m = 1 bridge extractor (JCB-023).

## 2026-07-21 (session 6) - The bilinear harness completes; the tooling ships

- **EXP-017 (confirmed):** the bilinear harness: det J is bilinear in the coefficient vectors,
  so the gauge Keller condition is LINEAR in Q given P: solved completely per P-sample. (2, 3):
  216-vector P-grid, 16 consistent, 32 instances, triangular witnesses recovered exactly where
  the old solver failed; (3, 3): 45 structured vectors, 10 instances; every instance injective.
  JC(2) certificates now: (2, 2) exhaustive; (2, 3), (3, 3) exhaustive-in-Q over structured
  grids. Next stage: the consistency variety in P (rank conditions) for the full-A statement.
- **EXP-015 (confirmed):** the JC(2) certificate checker and the m = 1 bridge extractor ship as
  tested library code (CI-permanent): exact adjudication for any claimed planar Keller map or
  collision; the EXP-012 bridge is now executable.
- Still queued: EXP-014 Puiseux escape obstructions (JCB-022), the Hessian-nilpotent quartic
  extraction (JCB-024), the rank-conditions completion and higher-degree scans (JCB-021).

## 2026-07-21 (session 7) - The collateral impact, closed and published

- **EXP-018 (confirmed):** cascade closure: the Poisson chain verified (Adjamagbo-van den
  Essen, arXiv:math/0608009: three-way equivalence, any characteristic: full Poisson conjecture
  false, minimal dimension open) and the symmetric/gradient corollary recorded (de Bondt-van
  den Essen reduction + Zhao equivalence: a non-invertible gradient Keller map exists in some
  dimension). Sweep found no further named open conjecture proven to imply JC;
  Markus-Yamabe and factorial excluded deliberately with reasons.
- Web: new "Collateral impact" tab on the problem page, baked from the jacobian.json cascade
  payload (8 status rows: was/now/chain), screenshot-verified, zero errors; credit line first.
- `manuscript-cascade/`: the companion document (corollaries with chains and references, what
  remains open, the method note), built clean.
- Diffusion: difusion/jacobian-cascade/ post drafted in the management repo (honoring the
  origin; our role = source-verified evaluation).

## 2026-07-21 (session 8) - The descent becomes linear algebra; (2,3) closes in full

- **EXP-019 (confirmed):** the Keller floors. (1) Floor identities 2-3 certified on the
  library; h-divisibility exhibited (up to p = 6). (2) Wider exhaustive certificates: (2,4)
  256-grid, (2,5), (3,4): all injective, witnesses recovered. (3) THE HEADLINE: full-A closure
  of (2,3): the consistency ideal of the linear Keller system is ONE generator,
  (4 A0 A2 - A1^2)^2 = 0: a quadratic P completes iff its top form is a perfect square,
  exactly the leading-form degeneracy EXP-013 predicted. Theory and elimination met in one
  equation. The JC(2) machine is now: eliminate -> parametrize -> complete linearly ->
  fiber-test, degree pair by degree pair, with the tropical theory predicting each consistency
  ideal in advance (JCB-021 continues: (2,4)/(3,4) eliminations, branch tightening of (2,3)).
- Also this day (sessions 7 side): the cascade carousel shipped in the management repo and the
  cascade post links the companion manuscript PDF directly.

## 2026-07-21 (session 9) - Theorems: the (2,n) column falls for n = 3, 4, 5

- **EXP-020 (confirmed):** the machine's full loop validated end to end and it PROVES cases:
  (1) THEOREM: every normalized (2,3) Keller map is invertible, with the explicit inverse
  G(u,v) = (u - (au+bv)^2, v + (a/b)(au+bv)^2) verified by exact composition (b = 0 stratum
  forces the affine case). (2) The (2,4) consistency ideal EQUALS the (2,3) one (the
  discriminant-square locus is completion-degree independent, as the leading-form theory
  predicted). (3) THEOREMS at (2,4) and (2,5) too: one-branch completions with a free family
  parameter, explicitly invertible symbolically including the free. (4) The (3,4) monolithic
  elimination exceeded the compute window; staged strategy queued (JCB-021). Next theorem
  attempt: the uniform all-n statement for the (2,n) column (JCB-025).
