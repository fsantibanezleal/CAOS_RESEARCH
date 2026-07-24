# Strategy expansion (2026-07-24, session 47): all paths that could help

Felipe's directive: explore ALL paths and strategies. The map, ranked by
expected information per unit cost; each candidate becomes a declared
experiment or a dossier before any claim.

## S1. The structural-theorem seeds (the only road to all-degrees statements)
- S1a. GENERALIZE THE ANNIHILATION LEMMA: J(m, P^k) = -kL(P^{k-1}m) and the
  dual identity (c kills all bracket images) both smell like one fact about
  the pairing between the bracket image and the cokernel across ALL windows.
  Hypothesis to declare: for every window system in the staircase transport,
  the cokernel pairs trivially with the ad-image; if provable in general, the
  obstruction theory becomes PURELY top-order for every configuration, a
  uniform lemma feeding any future termination argument.
- S1b. TERMINATION OVER CHAINS: the GGV chain machinery generates finitely
  many candidate chains per degree bound but infinitely many overall. Seek a
  well-quasi-order (Dickson/Higman style) on chain data under which the
  exclusion certificates are monotone: WQO + monotone exclusion = all-degrees
  theorem. Speculative; a dossier first (literature: tropical/valuation trees).
- S1c. THE OBSTRUCTION-MOTION LAW: degrees 1/2/3 show obstructions MOVING
  (diagonal 8-set, then a mixed triple, then nothing through triples).
  Measure WHERE obstructions live as functions of degree on small analog
  systems (toy polygons): an empirical law could reveal the generating
  mechanism and predict whether some finite degree always closes.

## S2. The (72,108) endgame (current thread, continued)
- S2a. Quadruple sweep (EXP-075, running). S2b. Constructive GF(p) solve (R2).
- S2c. CHART COVERS (R4): formalize the axis-chart certificates (EXP-063/065)
  into a finite cover statement: the missing piece is the gluing condition;
  declare the two-chart toy first.

## S3. The [125,150] frontier (C13 thread, continued)
- S3a. EXP-077: the en-point/q1 computation + Prop 3.29 numbering match.
- S3b. The Theorem 5.1 template cases (C08/C09/C14/C15) after C13.

## S4. Independent leverage from the GGV toolbox (unmined)
- S4a. APPROXIMATE ROOTS / SUBRESULTANTS (arXiv 1708.09367): intersection-
  number formulas give INDEPENDENT constraints on the same candidate pairs;
  cross-checking our polygon exclusions against intersection-number
  obstructions could kill cases cheaper or catch errors.
- S4b. Orevkov's methods (flagged by GGHV17 for sporadic chains): literature
  pass; his Lemma 4.1(a) analyzed an F13 sibling extensively.
- S4c. CHAR-P TRANSFER: our EXP-0xx char-p certificates for 3D; is there a
  mod-p shadow of the planar chain machinery giving fast necessary filters?

## S5. Engineering multipliers
- S5a. Port the subsystem sweeps to a compiled GF(p) kernel (galois/numpy
  batched or a small C extension): 100x on sweeps unlocks quadruple+ tiers.
- S5b. SAT/ILP encodings of feasibility sweeps for independent verification.
- S5c. Lean formalization of the theorem ladder (JCB-018, parked): revisit
  once the truncation story stabilizes.

## S6. Community and record
- S6a. GGHV outreach (draft ready; Felipe sends). S6b. Paper B truncation
  chapter + Zenodo republish (authorized). S6c. A methods note on the
  declared-gate discipline (the retraction story) as its own short paper.

Execution order (sessions 47+): S3a and S2a continue now; S1a is the next
DECLARED experiment after EXP-077 (it is cheap: test the dual annihilation on
3 other window systems); S5a lands when the quadruple sweep's cost justifies
it; S4a opens as a dossier in parallel rounds.

SWEEP ECONOMICS NOTE (2026-07-24): EXP-075 measures ~6.4 s/support: the full
quadruple sweep would take ~18 days. Session 47+ should RESTART it REORDERED
(supports containing >= 2 of the 8 degree-1 blockers first, ~8k supports,
~14 h: the degree-2 hit lived in blocker territory) and pursue S5a (compiled
GF(p) kernel) before any full-space quadruple commitment.

## S7. The birational/multiplication structure of the 3D counterexample (from a Tao-ChatGPT exchange, verified 2026-07-24)

A shared exchange (attributed to Tao) reverse-engineered the Alpoge counterexample.
VERIFIED symbolically in-repo (all identities exact):
- The map is the COEFFICIENT MAP of the polynomial product (a+bt)(c+dt+et^2)
  (a linear form times a quadratic), restricted to X = {(a,b,c,d,e): Res(linear,
  quadratic) = a^2 e - abd + cb^2 = 1, and the middle coeff ad+bc = 1}, with
  X isomorphic to A^3 (explicit Phi, defined even at a=0), dropping the middle
  coefficient. This gives G: C^3 -> C^3, det DG = -1, = the counterexample up to
  linear normalization (F_orig = B o G o A).
- The constant Jacobian is STRUCTURALLY FORCED by a birational-Laurent
  cancellation: (x,y,z)->(x,u,r) with u=1+xy, r=2-3xy-x^2 z has Jacobian -x^3;
  the map in (x,u,r) is a simple Laurent map with Jacobian 2 x^{-3}; the pole
  cancels the zero. The map is a degree-3 (three-sheeted) cover; the fibers solve
  a depressed cubic whose discriminant is a perfect square times -4D.

WHAT THIS OPENS FOR JC(2) (routes, ranked):
- S7a [COUNTEREXAMPLE SIDE, genuinely new to us]: the CONSTRUCTIVE TEMPLATE.
  A counterexample = (affine variety X isomorphic to A^n, cut by resultant/norm
  = 1 constraints) + (an algebra-MULTIPLICATION map) + (drop a normalized
  coordinate). For JC(2) search the 2D analog: multiply a linear by a linear (or
  the right bidegree) on a unit-resultant variety isomorphic to A^2, drop a
  coordinate, test the composite. This is a SYNTHESIS search, complementary to
  our exclusion sweeps; it feeds the two-sided reframe (S0) directly.
- S7b [EXCLUSION SIDE]: the Laurent-cancellation OBSTRUCTION. A planar Keller map
  arising from a birational-Laurent factorization needs a pole to cancel a zero;
  with only two coordinates there is "less room". Attempt to prove no such
  factorization closes in 2D (a structural exclusion of this family). Connects to
  S5 (at infinity: the pole lives there).
- S7c [SUPPORTING]: the mechanism is intrinsically >=3D (cubic cover, needs the
  third slot for the Laurent cancellation and the degree-3 elimination). This is
  independent evidence the mechanism does NOT transplant to 2D, consistent with
  our published rigidity/uniqueness theorems. Our T-theorems constrain exactly
  the u=1+xy "unit times monomial" shapes this construction rides on.
- PRELIMINARY [D, to verify in EXP-086]: the FAITHFUL 2D lowering (linear x
  linear = 3 coeffs; resultant=1 AND middle=1 as the two constraints) is
  DEGENERATE (ad-bc=1 with ad+bc=1 forces ad=1, bc=0: no smooth A^2). If robust,
  this is a concrete reason the mechanism resists dimension 2. EXP-086 tests
  whether any non-degenerate 2D analog exists.
