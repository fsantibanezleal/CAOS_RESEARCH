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

## 2026-07-21 (session 10) - The uniform theorem; the resume contract; the feed summary

- **Methodology 07 (session handoff) + program RESUME.md shipped:** every session now closes
  by updating the problem's RESUME (state, objects, in-flight, next actions, gotchas): a new
  session resumes with zero loss.
- **EXP-021 (confirmed): THE UNIFORM THEOREM.** Every planar Keller map with min degree <= 2
  is (x + ell^2, ell/beta + H(x + ell^2)) up to affine gauge, invertible by one closed
  formula. Certified: shear-PDE sufficiency (generic H); completeness by exact kernel
  dimensions (floor(n/2) + 1, n = 3..6); the closed inverse (generic deg <= 1 + exact spot
  checks at 3, 4). Three independent routes now agree (elimination ideals, leading forms,
  PDE characteristics); EXP-020's free parameters are H's coefficients, retro-explained.
  JC(2)'s frontier formally moves to min degree >= 3 (JCB-026: the quasi-triangular
  conjecture is the next theorem attempt).
- Web: the Home feed is now a summary (20 most recent, newest first, problem-labeled).

## 2026-07-21 (session 11) - Quasi-triangular closure; forced alignment; the descent runs

- **EXP-022 (confirmed):** (A) the shear closure holds for ANY f: J = 1 and the closed
  inverse, generically + spot checks: the uniform theorem's true scope is P ~ x + f(ell), any
  degree. (B) (3,3) cube case: alignment FORCED at the radical level (A0^2, A1^6 in the ideal
  with a inverted): the quasi-triangular conjecture holds at (3,3). (C) the descent inverter
  explicitly inverted all 8 library maps (0-4 steps), no primitive hits. JC(2) sharpened to:
  can a Keller pair be PRIMITIVE (shared base h of degree >= 2, non-power tops)? That stratum
  is the next target (JCB-027).

## 2026-07-21 (session 12) - First contact with the primitive stratum

- **EXP-023 (confirmed):** the (4, <= 6) completion window is EMPTY on the primitive slice:
  all 25 structured samples of P = x + P2 + P3 + a h^2 (h rank 2 and the rank-1 control) admit
  NO Keller completion of degree <= 6 (linear inconsistency every time), and one descent step
  extends the exclusion to degree <= 8. Positive controls prove the scan non-vacuous (the
  harness finds quasi-triangular completions; the detector fires on a genuine degree-6
  realization). Literature context [C, primary fetch queued]: gcd = 1 (Magnus) and gcd = prime
  (Appelgate-Onishi, Nagata) are classically excluded; our gcd-2 emptiness replicates a slice
  independently; the open ladder is (4, 4k+2), k >= 2, and composite gcd >= 4 ((8,12)).

## 2026-07-21 (session 12, addendum) - The (4,6) pure-slice certificate

- **EXP-024 (confirmed):** sound all-parameter certificates via cleared left-null vectors
  (the fraction-field RREF instrument was first refuted: it normalizes the obstruction to 1,
  generic-only). Pure slice P = x + a (xy)^2: the single pairing is -8 a^2, so the (4, <= 6)
  window is empty for EVERY a != 0 (theorem on the slice, exceptional-locus gap closed). The
  8-parameter certificate capped at 540 s (documented); staged variants queued (JCB-028).

## 2026-07-21 (session 13) - Slices, windows, a locus closed; sources verified; the web reader

- **EXP-025 (confirmed):** (A/D/E) the (4, <= 6) window is empty for ALL parameter values on
  every slice with up to THREE lower coefficients on (7 + 21 + 35 slices; union arguments via
  radical membership where pairings degenerate). (C) pure-slice windows: no partner of degree
  <= 10, <= 14, <= 18 for any a != 0: the rungs where the descent has no move die there.
  (F) the one genuine candidate locus (4 a s = u^2 on p20+p21+p03, the translation orbit of
  the pure slice) closed COMPLETELY via the polynomial parametrization (gcd 12 al^6).
- **JCB-029 closed:** Magnus 1954 (gcd 1; year corrected from 1955) and Appelgate-Onishi 1985
  + Nagata (gcd prime; coverage {1,8} u P u 2P) verified; plane JC is classically EQUIVALENT
  to divisibility, i.e. our primitive-stratum framing. Honest consequence: the whole (4, *)
  ladder has gcd 2 and is literature-covered (our certificates are independent replications);
  the open frontier is composite gcd 9, 12: bidegrees (18,27), (24,36).
- **Web:** every experiment record is now readable in place: feed and log titles open a modal
  with the full hypothesis, verdict and artifact inventory (baked into experiments.json);
  lazy-loaded renderer; screenshot-verified in both themes on both pages.

## 2026-07-21 (session 14) - First exclusions at composite gcd; the reach test; the novelty pass

- **EXP-026 (confirmed):** first contact with gcd 9 territory, bidegrees (18, 27): the
  (18, <= 27) completion window is empty numerically (3 samples, ~3 s each at 403 unknowns)
  and for three structurally different degree-9 bases; THE CERTIFICATE: for h = x^4 y^5, no
  Keller partner of degree <= 27 exists for ANY a != 0 (pairing gcd -144 a^2). gcd 9 is
  outside the gcd-coverage theorems ({1,8} u P u 2P); honest framing: (18,27) sits inside
  Moh's degree-100 verified range, so the new content is the explicit machine certificate,
  not the truth itself; beyond-Moh degrees are the next rung. The gcd-12 reach test
  ((24, <= 36), 700 unknowns) is empty at the probe in 9.4 s: the full gcd-12 certificate is
  within reach.
- **Rigidity novelty pass (bounded):** two targeted searches found adjacent work but no
  statement of the equivariant rigidity theorem; recorded in wiki 04; full-text pass queued
  (JCB-031).

## 2026-07-21 (session 14, addendum) - The gcd-12 certificate

- **EXP-027 (confirmed):** at (24, <= 36), h = x^5 y^7: no Keller partner for ANY a != 0
  (700 unknowns, one pairing, gcd -80 a^2, 227 s). Both uncovered composite gcds (9, 12) now
  carry certified pure-slice exclusions; same Moh-range framing as EXP-026.

## 2026-07-21 (session 15) - The strategy shift: polygons explain the machine

- **EXP-028 (confirmed):** (A) the lattice sieve from Abhyankar similarity is exact
  (admissible partner degrees = multiples of deg P only). (B) the DECISIVE window: (18, <= 36)
  contains the first admissible rung n = 36 and is EMPTY anyway. (C) certified: no partner of
  degree <= 36 for any a != 0 (one pairing, gcd -576 a^3). (D) obstruction anatomy: the
  certificate vector is supported EXACTLY on the ray parallel to P's Newton-edge direction:
  each certificate is a weighted edge residue (closed form conjectured, JCB-032).
- **Derived [D, conditional]:** P = x + a h^2 (h = x^p y^q, p != q) is NEVER a Keller
  component at ANY degree (similarity sieve + edge descent + machine shadow through 36);
  hardens when the similarity theorem's hypotheses are read from the primary text.
- **Sources:** Abhyankar similarity primary-cited (similar TRIANGLES, ratio deg f : deg g);
  Moh 1983 (<= 100, six candidate shapes eliminated); arXiv:2204.14178 raises the floor to
  108: beyond-current-knowledge starts above ~108 (e.g. gcd 45 at (90, 135)).

## 2026-07-21 (session 16) - THE WEIGHT-CLASS THEOREM: the machine found a proof

- **EXP-029 (confirmed):** the edge residue in closed form became an unconditional theorem:
  for u >= 2, v >= 1, a != 0, P = x + a x^u y^v is NEVER a Keller component at ANY degree.
  Proof: the (v, 1-u) grading makes P w-homogeneous, the Keller system decouples by weight
  class, the constant's class is one ray, L is banded there with positive integer
  coefficients, and the chain recursion contradicts the last row. Machine verification: the
  banded formula exact on grids; ALL SEVEN measured pairings reproduced (they were this
  formula all along); no second obstruction (full window == ray class, incl. d > 1); and the
  beyond-floor certificate at degree 135 > 108 (partner degrees to ~1073 checked, all a).
  Honest caveat: elementary once seen, folklore risk recorded; found by the machine's
  anatomy. Retires the pure-slice window program; opens the multi-edge calculus (JCB-033)
  for non-monomial slices: the next reasoning step toward JC(2).

## 2026-07-22 (session 17) - THEOREM 2: refuted proof, repaired proof, perturbations fall

- **EXP-030 (partially refuted, then decisive):** the naive injectivity step DIED in public
  (L_top has kernels on kv-classes: exactly P_top^k) while every empirical prediction held
  (perturbed windows empty; quasi-triangular control consistent; b-free pairings;
  beyond-floor perturbed instance falls). The refutation pointed at the correct proof.
- **EXP-031 (confirmed):** the repair closes. Kernels identified exactly; the ANNIHILATION
  LEMMA verified with adequate windows (first-run nonzeros were window-truncation artifacts,
  recorded); the reduction identity J(m, P_top^k) = -k P_top^(k-1) J(P_top, m) exact; danger
  tails certified b, c-free. THEOREM 2: P = x + a x^u y^v + R (u >= 2, v >= 1, a != 0, R any
  lower-weight polynomial) is NEVER a Keller component, at any degree: dense-polygon,
  unbounded-degree families, beyond every verified floor. Remaining [D] gap: annihilation in
  closed form. Next frontier: perturbations of weight >= v (the top edge itself deforms).

## 2026-07-22 (session 18) - THEOREM 3: every x-anchored edge falls

- **EXP-032 (confirmed):** on the y-class, the operator for a FULL edge E = x phi(z)
  (z = x^k y^m, deg phi = g >= 1) is MULTIPLICATION by (ms+1) phi + k z phi' [MV symbolic],
  so the obstruction is a univariate one-liner: the top coefficient (mD + kg + 1) phi_g of
  the class ODE kills every polynomial candidate. THEOREM 3: no Keller component has a
  Newton top edge anchored at the linear vertex x with interior direction, regardless of the
  edge coefficients (binomial, trinomial, perfect powers: all verified empty; QQ(a,b)
  certificate 60 a^3 b-free; kernels = E^j; tails never rescue; quasi-triangular control
  consistent). Subsumes Theorems 1-2's leading forms. One instrument bug (wrong class
  weights in the kernel scan) caught and fixed mid-run, recorded. The frontier is now
  SHARP: components must have y-anchored (quasi-triangular-type) tops; JC(2) = nothing else
  lives there (JCB-035).

## 2026-07-22 (session 19) - The edge fan closes: THE VERTEX DICHOTOMY

- **EXP-033 (confirmed):** the two boundary edge directions fall: k = 0 (P = x phi(y): the
  constant's class reads phi h' = 1, no polynomial solution; kernels (x phi)^s; certificate
  -c1^6) and m = 0 (P = x phi(x): Q_y = 1/(x phi)', one line). THEOREM 4 (the vertex
  dichotomy): if the monomial x is a VERTEX of N(P) for a Keller component, then
  P = x + f(y) exactly: every edge at the vertex is excluded except segments to pure-y
  vertices (no interior lattice points). Machine-verified on all three sides: vertex-x mixed
  samples inconsistent; triangular samples consistent; x-swallowed samples (x + (x+y)^2,
  x + (x+2y)^3) consistent: the escape route is real and is exactly where non-triangular
  components live. Strategy recorded (JCB-036): induction by gauge rotation on the
  dominating direction: the germ of a route to the full classification (JC(2) = the
  induction closes on the triangular family).

## 2026-07-22 (session 20) - The audit: rotation works where it can; the core is the corner

- **EXP-034 (confirmed):** the strategic audit Felipe asked for, with machine data. (A)
  rotate-descent (rotation of linear-base tops + de Jonquieres subtraction) LINEARIZES the
  entire library (0-6 steps each): the induction closes on all known components. (B) its
  exact limit is stated: mixed-corner tops stay mixed under rotation: the "hard-shape" stop
  is the classical hard territory (Moh shapes), NOT covered by Theorems 1-4 when x is
  swallowed; eight swallowed-mixed samples all have EMPTY windows: the uncovered territory
  resists and the exclusions now exceed the proved theorems. (C) certificate anatomy there:
  support spans many rows across directions (16/42, 25/49): the mixed-corner obstruction is
  NOT a single-ray residue: the corner calculus must handle multi-edge interaction. The
  program's standing question is now precise: prove hard-shape (mixed-corner) pairs cannot
  be Keller; instruments queued.

## 2026-07-22 (session 21) - The corner is diagonal; the annihilation gap is CLOSED

- **EXP-035 (confirmed):** the mixed corner is not the hard object. J(B^p, x^a y^b) =
  p(ib - ja) x^{ip+a-1} y^{jp+b-1}: DIAGONAL, kernel exactly the powers of B, and a pure
  corner can never carry the constant. So the Keller constant must be manufactured along the
  STAIRCASE of Newton vertices from the swallowed linear vertex to the corner: the open core
  is a transport problem on the lower-left boundary (the classical Moh staircase), not the
  corner. Territory widened: 30 monomial-corner samples, all windows EMPTY.
- **EXP-036 (confirmed after a REFUTED first derivation):** the declared closed form used
  L_top and was refuted on both tests (nonzero in-window pairings; rank outside the column
  space); the operator that matters is the FULL L = J(P, .). Corrected: J(m, P^k) =
  -k L(P^{k-1} m), so every source is an image with an explicit preimage; the certificate
  covector is left-null on the image by construction; rank tests confirm. The window
  criterion RETRODICTS EXP-031's artifacts number for number (15, 30a, 30, 45 at window 6;
  945 a^2 at window 10). JCB-033 CLOSED: THEOREMS 2, 3 AND 4 ARE NOW UNCONDITIONAL.

## 2026-07-22 (session 22) - Seven experiments; the frontier recalibrated; the dim-48 witness

- Felipe's directive: continue with ALL remaining experiments and evaluate ALL proposed
  reasoning paths and routes, at maximum depth. Two literature agents ran in parallel with
  the machine work; both dossiers are in context/ (literature pass; symmetrization).
- **EXP-037 (confirmed; declared prediction 3 refuted):** the STAIRCASE TRANSPORT is real
  and executable: the Keller window is block-triangular under the x-edge grading (diagonal
  = the MINIMAL P-class, which also makes the sweep triangular for genuine components);
  classwise elimination reproduces every monolithic verdict; the obstruction localizes at
  the CONSTANT'S class 8/8 (NOT at the vertex hand-off, refuting the declared guess); the
  generic reduced equation on x + a x^u y^v + b x^d is -2a = 0: the Theorem 5 target.
  JCB-038 steps (a)-(c) instrumented.
- **EXP-038 (confirmed):** pair-level corner theory: the matched-pair law at the second
  class is exact; the pair constraint adds NO obstruction depth (4/4 samples), only
  efficiency (roughly half the unknowns). JCB-039 answered: tool, not a route.
- **EXP-039 (confirmed):** the (3, n) column closes: (3, 4) tops are forced to perfect
  cubes (elimination minors + GL2-orbit completeness), the cube stratum completes and
  inverts (4/4 explicit inverses), non-cube tops empty at (3, <= 4/5/7); gcd(3, n) in
  {1, 3} is classically covered (Magnus 1955; Appelgate-Onishi/Nagata). JCB-021 closed.
- **EXP-040 (confirmed):** subsumption + recalibration: pure slice = Theorem 1 corollary;
  below-weight slices = Theorem 2 corollaries; the 4-subset sweep (105 solves) is clean.
  THE RECALIBRATION (from the literature dossier, primary sources): verified coverage is
  the FULL interval gcd <= 8 (the "{1,8}" reading was wrong) + primes + 2p + Heitmann's
  B >= 16 + GGV's "B = 16 or B > 20"; hence our gcd 2/9/12/18 certificates
  (EXP-024..028) are REPLICATIONS inside the floor. The live frontier: GGV's B = 16
  normal form (explicit attack surface) and the lone surviving pair (72, 108) below 125
  (GGHV 2204.14178; left open for compute). JCB-028 closed; JCB-040 opened.
- **EXP-014 (confirmed; reserved slot filled):** the properness/escape instrument: exact
  certificates (8/8 library), controls separating properness from injectivity, and the
  reduction JC(2) <=> empty Jelonek set for every planar Keller map. JCB-022 first
  contact done.
- **EXP-041 (confirmed): THE DIMENSION-48 WITNESS.** First explicit symmetric/gradient
  witness anywhere (verified sweep): HC(48) is false explicitly: f_H = -i sum_j
  H_j(x + iy) y_j (382 Q(i) monomials, homogeneous quartic, Hessian nilpotent) built by
  the de Bondt-van den Essen construction from Thompson's dim-24 BCW artifact
  (sha256-matched, verified in-house; his nilpotency index claim corrected 17 -> 18 by
  our exact sparse chain: (JH)^18 = 0, (JH)^17 has 6 terms); the conjugation identity
  verified in all 48 components; the explicit 2-point Q(i) collision verified; P_star =
  -f_H falsifies Zhao's Vanishing Conjecture at an explicit polynomial. Two instrument
  bugs caught and recorded (a per-entry "trace" check; a module-import guard).
- **Novelty pass (JCB-031, dossier):** Theorems 1, 2 and the equivariant rigidity
  theorem: NOT FOUND in the literature (rigidity has genuine content: the C* analog
  FAILS on pseudo-planes, Dubouloz-Palka 2018); Theorem 3: not found as stated, method
  classical (GGV bracket calculus); Theorem 4: sharp-dichotomy form (GGV Prop 4.1 has
  the counterexample half). Citation corrections: Magnus gcd 1 = Math. Scand. 1955;
  never cite Zoladek's B > 33 (documented gap); Moh's <= 100 fully detailed only at 64.
- **Routes evaluation shipped** (program/jacobian-conjecture/routes-2026-07-22.md): R1
  staircase transport PURSUE (Theorem 5 via cleared certificates); R4 redeploy the
  machine at B = 16 + (72, 108) PURSUE (JCB-040); pair theory TOOL; properness HOLD;
  rotation frame KEEP; equivariant + witness DONE (publish); char-p pool DORMANT; Lean
  HOLD.
- Debt queued honestly: manuscript + wiki-04 integration of the recalibration and the
  witness (Felipe validates the novelty phrasing first); web bake + screenshot pass for
  the seven new records; upstream index-correction note to the Thompson repo (Felipe's
  call). v0.25.000.

## 2026-07-22 (session 23) - Theorem 5 window form; the frontier engaged; the manuscripts split

- Felipe's directives: improve all manuscripts; run additional experiments; define routes
  covering more of the current view; and (mid-session) evaluate SPLITTING the manuscript
  into a preliminary/foundational record and the specific active one, keeping history.
- **EXP-042 (confirmed; declared prediction 2 refuted, replaced):** THEOREM 5 IN WINDOW
  FORM: cleared polynomial covectors (c^T M = 0 verified identically; EXP-024 discipline)
  across the (u, v, d) staircase grid, with MONOMIAL pairings (-13860 a^7, -32 a^4, ...;
  6/8 b-free, the rest delegating only their b = 0 locus to Theorem 1): the completion
  window is empty for ALL parameters with a != 0. The declared window-stability guess was
  refuted by a cleaner law: pairing = -c_N a^N at every window N = 5..9. The annihilation
  machinery transfers verbatim (the Leibniz identity is P-agnostic; in-window sources pair
  to zero 4/4). A 3-parameter tail certificate (-27720 a^7 c3^4) extends the family. The
  all-degree Theorem 5 now needs exactly one thing: the transport chain's closed form.
- **EXP-043 (confirmed):** the live frontier engaged. GGV's B = 16 data verified [MV]
  (R0 (4,-1)-homogeneous, collinear x-anchored support; R1; R0-power dependence). NEW
  OPERATOR: J(x^m phi(z), x^a y^b) = x^{m+a-1} y^{b-1} [b m phi + (bk - al) z phi']
  identically (Theorem 3 = the m = 1 case). Consequence: for m >= 2 NO monomial reaches
  the Keller constant from the R0^m edge: the B = 16 problem IS a staircase transport.
  Theorem 4 excludes the pure m = 1 shape outright (window replication empty); swallowed
  variants empty. Scoping: the (48, 64) attack has 2142 unknowns in 315 classes with
  largest diagonal block 13; (72, 108): 5992 unknowns, 535 classes, largest block 22:
  the classwise attack is block-cheap; the cost is coupling bookkeeping, which the
  EXP-037 instrument automates.
- **The manuscript SPLIT (decision taken per Felipe's directive, history preserved):**
  the record is now THREE papers: A = manuscript/ (foundational 3D aftermath, v0.07:
  planar sections moved out, Moh phrasing corrected, companions declared);
  B = manuscript-planar/ (NEW, v0.01: the machine, Theorems 1-4 + annihilation, the
  staircase transport with Theorem 5 window form and its certificate table, the
  matched-pair law and the x^m operator, the recalibrated frontier with replication
  labels, the positioning/novelty section per the dossier); C = manuscript-cascade/
  (v0.02: the explicit dimension-48 witness section with Thompson credit and the index
  correction; rows upgraded from existential to explicit). All three PDFs compile clean;
  nothing deleted: content moved with its EXP labels; the log remains the single
  chronological record. JCB-041's manuscript half is DONE; the novelty PHRASING still
  awaits Felipe's validation before submission anywhere.
- **Routes addendum shipped** (routes-2026-07-22.md): the current view in one paragraph
  (JC(2) = inconsistency of the transport chain for every mixed staircase); near-term N1
  (transport closed form) and N2 ((48,64) validation sweep, then open B = 16, then
  (72,108)); mid-term M1 (NEW route: literature shape restrictions imported as machine
  window FILTERS: GGV/GGHV/Makar-Limanov/Lee-Li), M2 (staircase-length induction), M3
  (properness cross-check); long-term L1-L3 (Lean; publication sequence; dormant pools);
  a standing decision rule (every new experiment names its route).
- Remaining debt: web bake + screenshot pass (now nine unbaked records); wiki 04 deep
  rewrite; Felipe's calls: novelty phrasing, Thompson outreach, diffusion. v0.26.000.

## 2026-07-22 (session 24) - The certificate tower; the filter multiplier; debt burned down

- Felipe's directive: continue with all. Routes N1, N2, M1 advanced; JCB-041 debt largely
  cleared; blocked-on-Felipe items untouched by design.
- **EXP-044 (confirmed, route N1):** the closed-form push: the NORMALIZED constant-class
  transport equation is IDENTICALLY -2a at every window (N <= 13, two shapes); the
  cleared pairings follow -c_N a^N with positive ratios (the odd primes 2N - 3 from
  N = 7); and THE CERTIFICATE TOWER exists: each window's covector restricts to the
  previous one on ALL rows with one common ratio, while window growth adds unknowns only
  upstream of the constant's row. THEOREM 5 ALL-DEGREE now stands at [D]; the single
  remaining gap is the TOWER LEMMA (the restriction ratio is a nonzero multiple of a for
  every N; verified through N = 11).
- **EXP-045 (confirmed, routes N2 + M1):** the x^{m-1}-divisibility one-liner (pure R0^m
  is trivially never a component); NEW mid-scale certificates at degree 32
  (P32 = x + R0(1)^2: windows 12, 16, 20 empty; 88-228 unknowns); the similarity filter
  verified sound on library pairs and worth x18.8: P32's partner-degree-48 window drops
  1222 -> 65 unknowns and the (48, 64) system drops 2142 -> 111. JCB-043's declared value
  test PASSED decisively: the (48, 64) validation sweep and beyond are now SMALL
  computations.
- **Wiki 04 rewritten** (recalibrated gcd landscape with the corrected coverage and
  citations; rigidity novelty upgraded to the full-pass verdict; new sections: the
  staircase transport + Theorem 5 + tower; the frontier engaged; the witness pointer).
- **Web bake:** verified automatic on main merges (live experiments.json already served
  EXP-040..043); the local pipeline run bakes EXP-044/045 cleanly and ships with this
  session's PR. Remaining JCB-041 debt: the screenshot verification pass only.
- v0.27.000.

## 2026-07-22 (session 25) - THE TOWER LEMMA IS PROVED; the frontier pipeline runs in seconds

- Felipe's directive: iterate until proof or counterexample, with the full routine each
  cycle. Honest status: JC(2) itself remains open; this session PROVED the queued lemma
  and validated the frontier pipeline at target scale.
- **EXP-046 (confirmed): THE TOWER LEMMA, PROVED** (primitive-top and d >= u+v scopes),
  by four machine-verified ingredients: (i) old columns vanish on new rows (degree
  bookkeeping); (ii) the new block is J(T, .) with kernel = top-form powers (verified
  exactly); (iii) THE KEY IDENTITY: each resonance kappa = lambda (P - low)^k, so
  kappa - lambda P^k is in-window and P^k is in ker L: L(kappa) is an in-window image,
  annihilated by every certificate (rank test confirms); (iv) the extension realized
  explicitly across the active resonance 8 -> 9 (ratio 2, pairing preserved).
  CONSEQUENCE: **THEOREM 5 IS UNCONDITIONAL** for P = x + a x^u y^v + b x^d with
  gcd(u, v) = 1 or d >= u + v: the first all-degree exclusion of an above-weight
  (staircase) perturbation; staircase length 2 falls on that scope. The proper-power
  case (u = v = 2): the odd resonance (xy)^5 and even (xy)^6 both pair to ZERO
  (measured); deriving that kill is the lemma's one remaining case (queued).
- **EXP-047 (confirmed, route N2):** the filtered (48, <= 64) sweep RAN: three degree-48
  F1-flavor samples (pure x + R0(1)^3 + two swallowed variants): filtered windows at
  N = 64 (111 unknowns, 270 equations) EMPTY in 2.4-3.6 s each: by similarity nesting,
  all partners of degree <= 64 are excluded per sample. Classical case-64 degrees:
  sampled-level replication; the demonstrated cost makes the open territory
  (max > 150; (72, 108)) affordable at seconds per certificate.
- **Routine executed:** manuscript-planar v0.02 (the Tower Lemma stated with its proof
  ingredients; Theorem 5 upgraded to unconditional on scope; the frontier subsection
  updated with the run results); wiki 04/05 updated; bake refreshed; v0.28.000.
- Next iteration: (a) the proper-power odd-resonance derivation (closes Theorem 5
  entirely); (b) generalize the tower induction to arbitrary above-weight tails and
  longer staircases (the M2 induction: JC(2) = all staircases excluded); (c) transcribe
  (72, 108) + beyond-150 shapes and sweep. Felipe's pending calls unchanged (novelty
  phrasing, outreach, diffusion).

## 2026-07-22 (session 26) - THEOREM 6: the universal tower; the half-plane mechanism; (72, 108) reached

- Felipe's directive: keep iterating to proof or counterexample, full routine, max depth.
  Honest status: JC(2) remains open; this iteration generalized the tower to its
  universal form and put the machine ON the open pair's degrees.
- **EXP-048 (confirmed; declared universal-kill prediction refuted as stated):** the
  proper-power odd-resonance mechanism is THE HALF-PLANE CERTIFICATE: at (2,2,2) the
  left-null space is 20-dimensional with two pairing-nonzero directions, exactly one of
  which kills the odd resonance, and its support lies ENTIRELY in the y-heavy half-plane
  {i < j}, disjoint from the always-x-heavy sources (L((xy)^s) = s x^s y^{s-1}(1+2bx)).
  Theorem 5's proper-power case stands [D] with the mechanism named; the general
  half-plane construction is the remaining formalization, and it is exactly what the
  B = 16 frontier shapes need.
- **EXP-049 (confirmed): THEOREM 6, THE UNIVERSAL TOWER.** For ANY P = x + R whose
  total-degree top form is NOT a proper power: one certified window (N >= deg P - 1)
  excludes P at ALL partner degrees. Proof: the EXP-046 tower with T the FULL top form:
  ker J(T, .) = T-powers exactly (verified for monomial, binomial and dense-cubic tops),
  and T = P - lower BY DEFINITION so T^k - P^k is always in-window: every resonance
  reduces. Harvest: multi-edge staircases now fall at all degrees from single cleared
  window solves (x + a x^2 y + b x^3: -4620 a^7 b; the THREE-term staircase
  x + a x^2 y + b x^2 + c x^3 y^2: -4620 c^4; x + a x^3 y + b x^2: -630 a^4;
  x + a x^2 y + b x^4 y^3: -168 b^3). Route M2's induction collapses to per-shape base
  certificates on the non-proper-power stratum.
- **EXP-050 (confirmed, route N2):** FIRST certificates at the (72, 108) degrees: two
  sampled degree-72 shapes with the GGHV corner (16, 56), filtered windows at N = 108
  EMPTY in 1.2-1.4 s each: all partners of degree <= 108 excluded per sample. The
  systematic parametrized sweep (which would close the case and raise the floor to 125)
  awaits the GGHV shape transcription from the primary text (queued).
- **Routine executed:** manuscript-planar v0.03 (Theorem 6 + the half-plane remark +
  the (72,108) first contact); wiki 04/05; bake refreshed; v0.29.000.
- The program's residual structural gap is now SINGLE: the general half-plane
  certificate construction for proper-power tops (it closes Theorem 5 entirely AND
  unlocks the tower on the frontier shapes). Next iteration: derive it; transcribe the
  GGHV family; sweep.

## 2026-07-22 (session 27) - THE HALF-PLANE TOWER LEMMA; frontier shapes fall at all degrees

- Felipe's directive: non-stop rounds until proof or counterexample. Honest status:
  JC(2) remains open; this round CLOSED the program's single residual structural gap on
  its natural stratum and produced the first all-degree frontier exclusions.
- **EXP-051 (confirmed): THE HALF-PLANE TOWER LEMMA.** For P = x + R whose top corner
  is the y-most support point (the swallowed-staircase geometry), the y-heavy
  half-plane subsystem H = {i <= j} has a fully-resolved tower: T-power resonances
  reduce (universal identity), non-T-power kernel resonances have x-heavy sources with
  EMPTY H-part, and straddling columns are vacuous (T attains mu; zero violations
  measured). ONE H-certificate = exclusion at ALL partner degrees, proper-power tops
  included. Machine record: symbolic monomial-pairing H-certificates at every window
  7..10 at (2,2,2); case-c sweeps clean on both test shapes. THE FRONTIER PAYOFF:
  P32 = x + R0(1)^2 + x^2 (degree 32, B = 16 flavor) and P72 = x + 2(x^2 y^7)^8 + x^2
  (degree 72, the (72,108) corner geometry) carry H-certificates (pairings -256, -32):
  BOTH EXCLUDED AT ALL PARTNER DEGREES: the first all-degree exclusions on
  frontier-shaped polynomials.
- Consequence for the ladder: Theorems 5-6 + the half-plane lemma now cover the entire
  swallowed-staircase stratum with y-most top corners, at all degrees, from one window
  solve per shape (seconds).
- In flight: the GGHV (72,108) shape-transcription agent (dossier lands in context/);
  the parametrized all-degree sweep is next round's target.
- Routine: manuscript-planar v0.04 (the half-plane lemma + frontier all-degree
  results); wiki 04/05; bake refreshed; v0.30.000.

## 2026-07-22 (session 28) - The reduced open case is on the bench

- The GGHV transcription landed (context/2026-07-22-gghv-72108-dossier.md, verified
  against the LaTeX sources): Prop 4.3 reduces the open (72, 108) case to pairs with
  [P, Q] = x^2 on SMALL reduced polygons (N(P) corners (0,0),(1,0),(8,14),(8,16),(0,8);
  N(Q) corners (0,0),(2,1),(12,21),(12,24),(0,12)); the paper never printed the system
  it could not solve; the solved-case template and family machinery are transcribed;
  two source typos flagged.
- **EXP-052 (confirmed):** the reduced system runs: 61 P-side / 125 Q-side lattice
  points; five P samples (four random with forced corners + one structured top edge
  y^8 (xy - 1)^8): the linear Q-system is INCONSISTENT every time (2-14 s per sample).
  Sampled evidence toward closing the lone open pair below 125. THE DECLARED NEXT
  TARGET: the all-P parametrized certificate (61 parameters, linear in 125 unknowns:
  exactly the cleared-certificate machinery's shape): closing it would raise the JC(2)
  floor to 125.
- Routine: wiki 05; log; RESUME; v0.31.000; bake. Honest status: JC(2) open; the open
  case below 125 is now a concrete 61-parameter certificate hunt on our own
  instruments.

## 2026-07-22 (session 29) - The 576 certificate: the open case's obstruction is structural

- **EXP-053 (confirmed):** the stratified attack on the reduced (72, 108) system
  landed: with the forced top edge y^8 (xy - t)^8 SYMBOLIC, the H-restricted system
  (threshold i - j <= 2, 289 rows) carries cleared certificates with pairing THE
  CONSTANT 576: nonzero for every t and IDENTICAL across three sampled lower strata
  (bare; x y^4; y^3 + x^2 y^6), 55-92 s per stratum. Support: FIVE rows (the target
  row (2,0) and the ray (9,16),(16,32),(17,33),(18,34)): the obstruction has the
  Theorem-1 chain anatomy and a closed form looks within reach.
- Remaining for full closure (next round, small and concrete): (a) support-entry
  analysis (if generic lower coefficients never enter the five rows, the certificate
  is UNIVERSAL and the case closes); (b) the sweep over the dossier's remaining
  forced parameters; (c) assembly with GGHV Prop 4.3 = the floor rises to 125.
- Routine: wiki 05; log; RESUME; v0.32.000; bake. Honest status: JC(2) open; the lone
  open pair below 125 is one support-entry analysis from closure.

## 2026-07-22 (session 30) - The universality refutation sharpens the closure route

- **EXP-054 (predictions 2-3 REFUTED as declared; the methodology at its best):** the
  fixed five-row 576 covector is NOT universal: 51 lower-point x support-row
  combinations enter with nonzero bracket factors, and adversarial samples confirm the
  identity breaks, even though the recomputed per-stratum pairing stays 576 every
  time. The measured truth: the obstruction VALUE is stable across strata; the
  covector is stratum-dependent. The closure route is now sharp: build the
  PERTURBATIVE covector Lambda(eps), polynomial in the lower coefficients (the
  certificate equation is linear in Lambda, affine in eps: a batched parametrized
  nullspace solve; termination is evidenced by the 576 stability). Next round's first
  task; success = the reduced (72,108) stratum closes universally = the floor rises
  to 125 (modulo the dossier's remaining forcing branches).
- Routine: wiki 05; log; RESUME; v0.33.000; bake. Honest status: JC(2) open; the
  refutation cost one covector and bought the correct construction.

## 2026-07-22 (session 31) - First-order universality; the ladder continues at order 2

- **EXP-055 (confirmed 1-2; prediction 3 refuted as declared):** the perturbative
  covector construction ran (background completion at 1374 s; the 590 s cap discipline
  is noted in the verdict). SOUND BASE: rhs is the constant x^2 vector and Lambda0 is
  globally left-null (symbolic t, column by column). FIRST-ORDER UNIVERSALITY PROVED:
  all 26 entering lower monomials admit correctors Lambda_i with Lambda_i M0 =
  -Lambda0 M_i and the (2,0)-entry pinned: the pairing stays exactly 576 to first
  order, with localized supports (<= 19 rows). Order-1 termination REFUTED: 15 of 36
  tested second-order pairs have nonzero residuals: the ladder continues with order-2
  correctors (same mechanism; the full 351-pair sweep and the order-3 test are next
  round's first task).
- Honest state: the reduced (72,108) stratum is empty for all t and all lower
  coefficients TO FIRST ORDER (plus exact per-stratum certificates at every sampled
  point); closure = finish the corrector ladder; then the dossier's remaining forcing
  branches; then the floor rises to 125.
- Routine: wiki 05; log; RESUME; v0.34.000; bake. JC(2) remains open.

## 2026-07-22 (session 32) - Perfect solvability; the pivot to the structural route

- **EXP-056 (confirmed 1-2; prediction 3 refuted as declared):** the order-2 ladder
  ran to completion in background (1414 s + 12326 s; cap discipline noted). PERFECT
  SOLVABILITY: all 26 first-order and all 250 nonzero second-order correctors exist
  with the (2,0)-pin: 276/276 solves, not one failure: the solvability is structural.
  Termination at order 2 refuted: 1134/6500 order-3 combinations nonzero; the profile
  is monotone (100 -> 71 -> 17 percent) but rung costs grow combinatorially. THE
  PIVOT (EXP-057): prove (i) ALL-ORDERS SOLVABILITY (every ladder rhs annihilates the
  right kernel of M0: a Jacobi/Leibniz bracket argument, the annihilation-lemma
  pattern) and (ii) A PRIORI TERMINATION (fixed finite row pool + rising eps-degree
  per rung bounds the order): together they yield the universal covector WITHOUT
  computing the rungs, closing the reduced stratum.
- Parallel routine done while the ladder ran: manuscript-planar v0.05 (the full
  (72,108) attack subsection); wiki 04 arc section; the assembly checklist
  (program/jacobian-conjecture/72108-assembly-checklist.md: the one substantive
  remaining branch is the edge-normalization verification; corners/Q-forcing/scaling
  subsumed); live site verified serving through EXP-055.
- Routine: wiki 05; log; RESUME; v0.35.000; bake. JC(2) remains open; the closure of
  the reduced stratum is now two lemmas away, both with named proof patterns.

## 2026-07-22 (session 33) - The one-dimensional kernel: the solvability lemma becomes concrete

- **EXP-057 (prediction 1 REFUTED; a structural discovery):** rank(M0) = 124 at every
  sampled t: the reduced system's right kernel is ONE-DIMENSIONAL, so rung solvability
  is NOT automatic; the perfect 276/276 record (EXP-055/056) means every ladder
  right-hand side has annihilated the single kernel object k(t). Via
  rhs . k = -Lambda_prev([m, k]), the all-orders solvability lemma is now CONCRETE:
  prove Lambda_prev([m, k]) = 0 for all perturbing monomials m and ladder covectors:
  the exact Jacobi/Leibniz annihilation pattern of EXP-036, now with an explicit
  target. (The coded 125-row minor crashed downstream of the refutation: recorded.)
- Next round, sharp: (a) compute k(t) explicitly; (b) identify its closed form
  (candidate: a truncation of a bracket-commuting object built from P0); (c) prove the
  annihilation condition; (d) revisit termination with k in hand (the kernel is also
  the only rhs-obstruction: the two lemmas may merge).
- Routine: wiki 05; log; RESUME; v0.36.000; bake. JC(2) remains open; the (72,108)
  closure now rests on ONE explicit object.

## 2026-07-22 (session 34) - k = 1: all-orders solvability proved in one line

- **EXP-058 (confirmed 1,3; prediction 2 refuted trivially):** the one-dimensional
  right kernel of the reduced (72,108) system is THE CONSTANTS: k = 1 (one nonzero
  coefficient at (0,0); rank exactly 124; the machine confirms nothing else joins).
  The declared off-pool-bracket prediction was refuted in the cleanest way: [P0, 1] =
  0 identically: the reasoning had missed the constant polynomial itself.
  CONSEQUENCE, PROVED IN ONE LINE: a ladder rung solves iff its rhs annihilates the
  kernel, and the rhs entry at the constant column is -Lambda_prev([m, 1]) = 0
  IDENTICALLY (brackets kill constants): ALL-ORDERS SOLVABILITY holds for any order
  and any parameters: the ladder can never stick; the 276/276 record is fully
  explained. Rank tests (part 3) concur.
- Remaining for the stratum closure: TERMINATION alone. Two candidate routes queued:
  the support-drift bound on the fixed pool, and the fixed-P determinantal framing
  (rank M(eps) = 124 with the x^2 rhs outside the column space for every parameter,
  now that the kernel is known to be exactly the constants for EVERY P).
- Routine: wiki 05; log; RESUME; v0.37.000; bake. JC(2) remains open; the (72,108)
  stratum closure = one termination lemma; then the edge branch; then the floor-raise.

## 2026-07-22 (session 35) - The constant-minor refutation; the chart-covering frame

- **EXP-059 (predictions 2-3 REFUTED; the tenth refutation of the series):** the
  augmented 125 x 125 minor exists at the base with a huge nonzero determinant, but it
  is NOT constant: 40/40 random parameter points give different values (at some points
  the row-label set itself changes). The constant-576 phenomenon is a property of the
  CLEARED pairing normalization, not of a parameter-free minor: consistent in
  hindsight with EXP-044's growing clearing constants. THE LOAD-BEARING OBSERVATION:
  every sampled determinant is NONZERO: across EXP-052..059, every parameter point
  ever tested keeps the reduced system inconsistency-certified: no candidate
  consistent point has appeared anywhere. The run was STOPPED once the interim data
  decided the predictions (hours of foregone symbolic confirmation saved; recorded).
- Corrected closure frame: the statement is that the IDEAL of augmented minors has
  empty vanishing locus on the stratum: a finite covering-by-charts argument (the
  row-set-changed trials already exhibit the alternative charts), OR the termination
  ladder with all-orders solvability in hand (EXP-058). Route (a) queued first.
- Routine: wiki 05; log; RESUME; v0.38.000; bake. JC(2) remains open.

## 2026-07-22 (session 36) - The edge verification lands; cases a/b close; case c in flight

- **The edge-normalization branch VERIFIED** (assembly checklist updated from the
  dossier's verbatim tex-line-referenced pipeline): under the stated inversion
  (x -> x^{-1}, y -> x^4 y, sending x^a y^b to x^{4b-a} y^b and [P,Q] to -[P,Q] x^2),
  the pre-forced factor (x^3 y - alpha_2)^{4m} maps at m = 2 to (xy - alpha_2)^8:
  OUR certificate stratum y^8 (xy - t)^8 IS the verbatim forced family for case c).
  The right edge's R^2 relation (R = x^4 y^7 (a0 + a1 y)) is subsumed by
  free-parameter certificates; cases a/b reduce to one companion run.
- **EXP-061 (confirmed):** the a/b companion CLOSES: sub-polygon certificates with
  monomial pairings (chart a1 = 1: 200 a0^3 bare, 600 a0^3 and 560 a0^4 with interior
  samples; chart a0 = 1: 200 a1^4), 2-23 s each; the vanishing loci sit exactly where
  the a/b polygons' own vertices would degenerate, which their forcing excludes; the
  two charts cover the gauge boundary. The a/b Q-side was already covered by the
  bigger-polygon emptiness.
- **EXP-060 (in flight):** the case-c (t, beta)-symbolic certificate is computing in
  background; adjudicated on its notification.
- State of the (72,108) closure: cases a/b DONE on forced families (interior
  sampled); case c = EXP-060 pending; then the free-interior upgrade + orientation
  swap; then the assembled floor-raise to 125 goes to Felipe for phrasing validation.
- Routine: wiki 05; log; RESUME; v0.39.000; bake. JC(2) remains open.

## 2026-07-22 (session 37) - Case c closes; all three branches covered

- **EXP-060 stopped and superseded** (the two-symbol nullspace stalled for hours with
  no output; no claim taken): the torus gauge (x -> lambda x, y -> mu y with
  lambda mu = t; the bracket target restored by a linear Q-rescale) normalizes t to 1
  WLOG, reducing case c to one-symbol certificates.
- **EXP-062 (confirmed): CASE C CLOSES.** (1) The gauge verified concretely: the
  t = 4 system and its transported t = 1 companion (target 8 x^2) give the same
  EMPTY verdict. (2) The beta-symbolic certificates at t = 1: pairing
  23592960 beta on the bare family and both interior-sampled variants; beta = 0 (the
  degenerate corner) falls back to the EXP-053/055 stratum certificates: the forced
  family is empty for ALL t != 0 and ALL beta. (3) The free-interior upgrade opened:
  four interior coefficients symbolic, each with the CONSTANT pairing 368640:
  nonvanishing for all values.
- **Assembly state: all three Prop 4.3 branches are certificate-covered on their
  forced families** (a/b: EXP-061; c: EXP-062 + gauge). Remaining, mechanical: the
  rest of the interior sweep (one-symbol runs, seconds each); the orientation swap;
  then the assembled statement ((72,108) discarded, completing GGHV's missing case;
  the JC(2) floor rises from 108 to 125) goes to Felipe for phrasing validation.
- Routine: wiki 05; log; RESUME; v0.40.000; bake. JC(2) remains open.

## 2026-07-22 (session 38) - Validation, the adversarial audit, and the amendment

- Felipe validated the then-current state ("I validate all the current state") and
  directed the new paths with deep research and revision. The closure statement was
  marked VALIDATED and the manuscript gained the closure section (v0.06).
- **The commissioned adversarial audit landed** (context/2026-07-22-beyond125-and-
  audit-dossier.md) and CAUGHT AN OVERCLAIM in our own validated statement: (a) the
  GGHV reduction forces NO interior coefficients, so the closure must hold for ALL
  interior values, and axis-symbolic + sampled coverage does not establish that (the
  program's own EXP-054 lesson); (b) the statement cited EXP-063 before its artifact
  existed; (c) the residuals list was incomplete (beta = 0 hand-off; sampled-t kernel
  basis; one-sample gauge check; the derived unpublished R^2 edge forcing; the N()
  convention; an inherited bridging gap at (66,99) in Thm 2.1's published record).
- **The amendment, applied immediately on all surfaces:** the closure statement
  downgraded to the certified scope (strong evidence toward, not yet a proof of, the
  closure; the floor-raise gated on the simultaneous-symbolic certificate);
  manuscript-planar v0.07 amended likewise; wiki 04/05 aligned. Nothing left the repo
  at any point. The audit's NINE ranked hardening tasks are the queue; GGHV outreach
  is last. The eleventh refutation of the series, aimed at ourselves by design.
- **The new path provisioned:** the same dossier transcribes the complete [125, 150]
  frontier: 24 configurations (6 family members F2/F7/F8/F9/F11/F24, 18 sporadic),
  tex-line-referenced, with pipeline inputs for deriving each reduced system and
  cheap first targets flagged (C13 shares our open case's final corner). Opens after
  hardening.
- EXP-063 (the interior sweep + orientation check) still in flight; adjudicated on
  its notification as hardening task 1's first half (the a/b interior sweep is the
  second half).
- Routine: wiki 04/05; log; RESUME; closure statement; manuscript v0.07; v0.41.000;
  bake. JC(2) remains open.

## 2026-07-22 (session 39, the continuous loop) - Hardening 1, 3-8 done or disclosed; the gate in flight

- Felipe's directive: continuous non-stop work with wakeups; executed (a fallback
  wakeup armed; task notifications remain the primary signals).
- **EXP-063 (confirmed):** the case-c interior AXIS SWEEP IS COMPLETE: all 44
  remaining points certify with nonzero constant pairings; the orientation reading
  adds nothing (4605 s background).
- **EXP-065 (confirmed):** the a/b interior sweep: 20/20 points in 98 s: HARDENING
  TASK 1 COMPLETE on both polygon families.
- **EXP-066 (confirmed):** the soundness batch: the beta = 0 corner carries explicit
  576 certificates (task 3); three gauge orbits verified (task 5). Tasks 4, 6-8
  clarified/disclosed in the statement's hardening log (the kernel was symbolic-t all
  along; the R^2 derivation labeled DERIVED; the N() convention and the (66,99)
  record gap disclosed).
- **The gate (EXP-064) remains in flight:** the joint-nilpotency chain computes in
  background; it alone gates the simultaneous-symbolic statement and hence the
  floor-raise. Task 9 (outreach) stays gated on Felipe.
- Routine: wiki 05; log; RESUME; the statement's hardening log; v0.42.000; bake.
  JC(2) remains open.

## 2026-07-23 (session 40) - The gate adjudicated: pinned ladder refuted, degree 1 closed; the papers PUBLISHED

- **Zenodo publication (Felipe approved and pressed Publish):** the three papers
  are live under CC-BY 4.0: A 10.5281/zenodo.21503366, B 10.5281/zenodo.21503368,
  C 10.5281/zenodo.21503372 (concept DOIs .21503365/.21503367/.21503371). Paper B
  carries the audited certified scope, so no published claim is affected by this
  session's refutations. DOIs are wired into manuscripts/README.md and the
  problem page; metadata centralized in the management repo. The manuscripts moved
  to the global tree manuscripts/jacobian-conjecture/{foundational,planar,cascade}
  (history preserved); GitHub release v0.42.000 created for the Zenodo GitHub
  archiver. Thompson index-correction issue filed (their repo, issue #1); GGHV
  outreach draft committed for Felipe to send.
- **EXP-064 (prediction 3 refuted, as declared possible):** the descending chain
  W_{k+1} = sum A_i W_k stabilizes NONZERO at dim 39 (V_inf dim 122, monotone
  descent 121..39): the pivot-pinned right-inverse does NOT terminate. All-orders
  solvability stands; the certificate is not refuted (165-dim gauge per solve).
  Operational lesson recorded: the sympy background run flushed NOTHING in 20 h;
  the identical mathematics on a plain-Fraction backend with flushed staged
  prints finished in 88 s.
- **EXP-067 (decided: DEGREE 1 CLOSED):** the sigma-free direct attack. All 51
  particular solutions exist; 8 single-index blocks are infeasible ((1,0),
  (3,5), (4,6), (4,7), (5,8), (7,13), (8,14), (8,15)); all 1275 pair blocks
  feasible in isolation (the obstruction is purely diagonal at degree 1); the
  full system is infeasible mod 2147483629, conclusive over Q. No degree-1
  covector.
- **The structural discovery:** the cokernel is 1-dimensional, so EVERY block
  condition reduces to one scalar obstruction against the cleared covector c.
  The truncation question is an explicit obstruction calculus, finite per degree:
  EXP-068 (the obstruction functional; aiming at a theorem for which degrees can
  close) is declared next; then the [125,150] frontier (C13).
- Routine: verdicts; wiki 05; log; RESUME; backlog; v0.43.000; bake; tag; PR;
  mirror (F55, F56). The floor-raise claim remains gated. JC(2) remains open.

## 2026-07-23 (session 41) - The correction round: the dual annihilation identity; degree 2 stays open

- **EXP-068 (premise refuted; the failure IS the discovery):** the cokernel
  covector c annihilates EVERY bracket image: all solvability conditions hold
  automatically at every order (the dual annihilation identity, explaining
  EXP-058 structurally). My scalar-obstruction reading in the EXP-067 verdict
  was WRONG and is corrected in place ([SUPERSEDED] block kept for the record);
  EXP-068's vacuous scalar conclusions are withdrawn in its verdict.
- **EXP-069 stage a (decided; expectation refuted):** all 51 diagonal-triple
  necessary blocks for degree 2 are feasible mod both primes: the level-1 gauge
  clears every diagonal obstruction, including the 8 degree-1 blockers. Degree 2
  stays OPEN; the joint order-3 system (about 2.9M sparse mod-p equations in
  227k gauge unknowns) is stage b, blockers-first with early-abort.
- Routine: verdicts; wiki 05; log; RESUME; v0.44.000; bake; tag; PR; mirror
  (F57 dual annihilation identity, F58 degree-2 stage a). The floor-raise stays
  gated. JC(2) remains open.

## 2026-07-23 (session 42) - DEGREE 2 CLOSED (EXP-070)

- **EXP-070 (decided):** the support-restricted necessaries of the joint order-3
  system, numpy mod-p over the exact Fraction setup. The sweep hit an INFEASIBLE
  pair subsystem at {(2,6),(5,9)} (both primes, conclusive over Q): NO DEGREE-2
  COVECTOR EXISTS. 800+ prior pair subsystems feasible; the obstruction sits at
  a mixed pair away from the 8 degree-1 blockers: the obstruction pattern MOVES
  with the degree.
- Standing: truncation degrees 1 and 2 both closed; the floor-raise stays gated;
  published Paper B scope unchanged. Declared next: degree-3 necessaries, the
  all-degrees pattern theorem, or the [125,150] frontier (C13).
- Also this session block: ORCID icon + link added on all three title pages
  (orcidlink; v0.08/v0.08/v0.03; PR #53), Zenodo new-version drafts created and
  AWAITING FELIPE'S PUBLISH (21504299/21504302/21504303).
- Routine: verdict; wiki 05; log; RESUME; v0.45.000; bake; tag; PR; mirror (F59).
  JC(2) remains open.

## 2026-07-23 (session 43) - THE RETRACTION ROUND: degree 2 re-opened; degree 3 open at pairs

- EXP-071's declared regression gate refused to reproduce EXP-070: the hunt
  found int(Fraction) TRUNCATION in EXP-070's mod-p assembly (plus an int64
  overflow fixed on the way). Under correct arithmetic (modfrac) the pair
  {(2,6),(5,9)} is FEASIBLE: EXP-070's "degree 2 closed" is RETRACTED in its
  verdict, wiki, and the mirror (F59 corrected). Session 42's headline is
  WITHDRAWN; v0.45.000's CHANGELOG entry superseded by this correction.
- Corrected decisions (EXP-071 run4): degree-2 pair sweep ALL FEASIBLE (degree 2
  OPEN); EXP-069a re-verified; degree-3 pair sweep ALL FEASIBLE (open at pairs).
  Degree 1 stands (EXP-067 was exact).
- Lessons hardened: never int() a Fraction for modular reduction; every new
  arithmetic path carries a declared regression gate against an exact decision.
- Routine: verdicts; wiki; log; RESUME; v0.46.000; bake; tag; PR; mirror
  (F59 corrected, F60). JC(2) remains open.

## 2026-07-23 (session 44) - DEGREE 2 CLOSED on the sound pipeline (EXP-072)

- **EXP-072 (decided):** with the modfrac pipeline regression-gated (20 sampled
  pairs reproduce EXP-071 run4), the degree-2 triple-support sweep hit
  INFEASIBLE at {(0,1),(1,0),(3,5)} (both primes; conclusive): NO DEGREE-2
  COVECTOR. Two degree-1 blockers in the support: the obstruction pattern
  persists at triple scope. This SUPERSEDES the retracted EXP-070 claim with an
  independent decision at a different support on sound arithmetic.
- Standing: degrees 1 and 2 closed; degree 3 open at pairs, triple tier next;
  if it closes, the pattern-theorem proposal goes TO FELIPE. Floor-raise gated.
- Routine: verdict; wiki; log; RESUME; v0.47.000; bake; tag; PR; mirror (F61).

## 2026-07-23/24 (session 45) - Degree 3 open through triples; R3 vacuous; Zenodo v2 live

- **EXP-073 (decided):** all 20825 degree-3 triple supports feasible (gate
  green; 13414 s): degree 3 OPEN through the triple tier. Escalation: R1
  quadruples (resumable multi-day) or R2 constructive GF(p).
- **EXP-074 (route closed):** the rational-in-eps route is VACUOUS: the gate
  found Lambda0 M0 = 0 (homogeneity clears rationals to polynomials). The
  declared-gate discipline again decided before any wrong build-out.
- **Publication:** the three Zenodo v2 records PUBLISHED on Felipe's
  instruction (A/B v0.08, C v0.03: ORCID title pages; concept DOIs resolve to
  v2); the problem page now links concept DOIs (PR #57).
- Felipe's MAX-DEPTH DIRECTIVE persisted in RESUME with the route map R1-R6
  (R3 now closed).
- Routine: verdicts; wiki; log; RESUME; v0.48.000; bake; tag; PR; mirror
  (F62, F63). JC(2) remains open.

## 2026-07-24 (session 46) - The quadruple sweep launched; the [125,150] frontier OPENS at C13

- **EXP-075 (in flight):** the degree-3 quadruple sweep (249900 supports,
  resumable, gate green) runs as a multi-day background task.
- **EXP-076 (decided at probe scope):** the frontier opens. The (8,32)
  sibling-discard arithmetic reproduces by machine, and every analogue exists
  for C13's (8,40): the forcing shape R' = x y^4 (y-1) (8m-power matches),
  post-shift corner (8,12); one structural difference recorded (v_{4,-1}(A0) =
  -8 vs 0). Gap list persisted: Cor 7.4 divisibility, Prop 3.29 at (8,12), the
  en-point recomputation: NO discard claim until the primary sources (GGV2,
  GGHV22 sec. 3) are fetched and verified next round.
- Routine: verdicts; wiki; log; RESUME; v0.49.000; bake; tag; PR; mirror
  (F64, F65). JC(2) remains open.

## 2026-07-24 (session 47) - EXP-077: the C13 d_0 fork COLLAPSES; discard's forcing extends

- **EXP-077 (decided; regression gate green):** the fork feared by the dossier /
  EXP-076 does not exist. From the primary sources (GGV1 = arXiv 1401.1784,
  GGV2 = arXiv 1605.09430, secured at E:\_Temp\ggv-sources):
  - [GGV1 Prop "Case II" + Thm 7.6(3)] gives q_1 = 4 for C13, identical to the
    (8,32) sibling: the (4,-1) leading form is the SHARED edge A1--A2, so
    en(F_1) = mu(2,7) = (6,21), mu = 3, d = 4, q_1 = 4. v_{4,-1}(A0) = -8 (vs 0)
    is below the edge and never reaches the en-point.
  - The perfect-power bound l_{1,0}(P) = R^{m d_0} on the SHARED bottom vertex
    st_{1,0}(P) = A1 = (8,28) forces d_0 | gcd(8,28) = 4; d_0 = 8 is impossible
    (28/8 not integer). q_1 = 4 | d_0 then pins d_0 = 4 UNIQUELY. EXP-076's
    d_0 = 8 / R' = x y^4(y-1) branch (bottom (8,32)) is CORRECTED.
  - C13's R = x^2 y^7·(cubic), bidegree (2,10), vs the sibling's (2,8): the
    single-root shift corner is again (8,4), excluded by [GGV2 "casos
    imposibles" (tex 1009) + remark (tex 1053)]: wp(n',n'-1), n' >= 2, with the
    explicit list (2,1),(3,2),(6,3),(8,4). This is the published Prop 3.29 analog.
  - Residual [D] DERIVATION NEEDED: whether C13's degree-3 tail shift terminates
    at (8,4) as the LAST lower corner (vs a longer admissible sub-chain). No
    floor-moving claim; routes to the main session.
- **EXP-075 superseded:** the linear-order quadruple sweep is replaced by
  run2.py (blockers-first order: supports with >= 2 of the 8 degree-1 blockers
  first, then the rest), resumable by index, relaunched in the background.
