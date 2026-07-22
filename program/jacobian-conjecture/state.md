# Jacobian conjecture - state (heartbeat)

- **State:** exploring (opened 2026-07-20).
- **Done (2026-07-20, sessions 1-2):** EXP-001 confirmed (exact validation; 3-point fiber).
  EXP-002 confirmed (structure owned). EXP-003 partially refuted (v1 lift; d = 2 rigidity).
  EXP-004 confirmed (constructor v2; new counterexamples P3/P4/P5 with rational collisions).
  EXP-005 confirmed with caveats (2D reduction; caveats honest). EXP-006 confirmed (2D scan
  non-vacuous: 216 instances, all LINEAR, all injective). EXP-007 confirmed (asymptotic variety
  explicit: A(F) = {C=0} union discriminant surface; escape = multiple fiber root). EXP-008
  confirmed (degree law (5d-3, 5d-4, 4); fiber floor 3; NEW fiber-degree-6 instance; F minimal
  within family). EXP-009 confirmed (char-p certificates: degree 12 < ell for ell = 13, 101).
  Wiki 01-05 current; manuscript v0.02 (LaTeX + PDF) built.
- **Also done (2026-07-21, session 4):** EXP-012 confirmed 1-4 / refuted 5: landscape mapped;
  the m = 2 mechanism is UNIQUE among scanned weighted systems (m = 1 = JC(2) bridge; m = 3
  empty/rigid; m = 4 potential form empty by Groebner certificate).
- **Now:** M3 web app (GitHub Pages per ADR-0016/0017/0056/0057/0058: shared shell,
  header/footer, references, page structure; baked census/wall artifacts ready from
  EXP-007/011; portfolio board from program/portfolio.yaml).
- **Also done (2026-07-21, session 3):** EXP-010 confirmed (2D equivariant rigidity THEOREM,
  all weights: every equivariant Keller map of C^2 is linear). EXP-011 confirmed (real census:
  1 or 3 real preimages split by the discriminant wall; real surjectivity; real Keller
  corollary). Manuscript v0.03.
- **Next experiments:** JC-P3 continuation (global-minimality search, degrees 3..6, GPU); JC-P4
  cascade verification from primary sources; optional Lean hardening of the rigidity theorem.

- **Session 5 (2026-07-21):** EXP-013 (ray-sweep bridge certified; (2,2) exhaustive JC(2));
  EXP-016 (cascade verified from primary sources, flags lifted). Queued: JCB-021..024.
- **Session 22 (2026-07-22):** seven experiments (EXP-037/038/039/040/014/041 + the two
  context dossiers): the staircase transport instrumented (block-triangular, obstruction at
  the constant's class, generic -2a = 0); pair theory = tool; (3, n) column closed; JCB-028
  closed by subsumption; the frontier RECALIBRATED to B = 16 + (72, 108) (gcd 9/12
  certificates are replications); the properness instrument shipped; THE DIM-48 WITNESS
  (first explicit symmetric/gradient/HN falsification, HC(48) false explicitly). Routes
  evaluation in routes-2026-07-22.md. v0.25.000.
- **Session 23 (2026-07-22):** EXP-042 (THEOREM 5 window form: cleared all-parameter
  certificates, monomial pairings, window law -c_N a^N; annihilation transfers) + EXP-043
  (x^m-anchored edge operator NEW; B = 16 core = staircase transport; scoping: largest
  blocks 13/22: the frontier attack is block-cheap). THE MANUSCRIPT SPLIT: three papers
  (A foundational v0.07; B planar program v0.01 NEW; C cascade v0.02 with the explicit
  witness); all compile. Routes addendum (current view + N/M/L map + decision rule).
  v0.26.000.
- **Session 24 (2026-07-22):** EXP-044 (the certificate tower: Theorem 5 all-degree [D];
  gap = the TOWER LEMMA) + EXP-045 (degree-32 frontier certificates; similarity filter
  x18.8: the (48,64) sweep is now small). Wiki 04 rewritten; bake verified automatic.
  v0.27.000.
- **Session 25 (2026-07-22):** THE TOWER LEMMA PROVED (EXP-046): THEOREM 5 UNCONDITIONAL
  for primitive tops / d >= u+v (proper-power odd-resonance kill queued); EXP-047: the
  filtered (48, <= 64) certificates run in 2.4-3.6 s each (three samples, all empty).
  manuscript-planar v0.02. v0.28.000.
- **Session 26 (2026-07-22):** THEOREM 6 (the universal tower: one certified window =
  all-degree exclusion, non-proper-power tops) + the half-plane mechanism (EXP-048) +
  FIRST certificates at the (72,108) degrees (EXP-050, ~1 s each). manuscript-planar
  v0.03. v0.29.000. Residual structural gap: the general half-plane construction.
- **Session 27 (2026-07-22):** THE HALF-PLANE TOWER LEMMA (EXP-051): one H-certificate
  = all-degree exclusion on the whole y-most-corner staircase stratum (proper-power tops
  included); FRONTIER PAYOFF: P32 and P72 excluded at ALL partner degrees. v0.30.000.
- **Now:** N1: the transport chain's closed form (Theorem 5 all-degree); N2: the (48, 64)
  validation sweep, then open B = 16, then (72, 108); M1: imported-constraint filters;
  web bake + screenshot pass (nine unbaked records); wiki 04 rewrite.
- **Blocked on:** Felipe: novelty phrasing validation (blocks submission, not work);
  outreach call on the Thompson index correction (17 -> 18); diffusion go/no-go.
