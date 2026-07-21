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
