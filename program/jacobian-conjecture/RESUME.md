# RESUME - Jacobian conjecture program (updated 2026-07-21, session 10 in flight)

The single first-read for a fresh session (contract: methodology/07-session-handoff.md).

## 1. State in one screen

- **World state:** JC is FALSE for every N >= 3 (Alpoge/Fable map, 2026-07-19; our EXP-001
  validated exactly: det JF = -2, fiber over (-1/4, 0, 0) = exactly the 3 announced points).
  JC(2) is open and is the program's target.
- **The mechanism [MV]:** F is a weighted skew-product (weights (1,-1,-2)); with v = xy,
  t = x^2 z, u = 1 + v: the Keller condition reduces to J_2 = 2 c_1^2 in (v, t); fibers are
  the roots of 4 Phi(w) - w BC + A C^2, Phi(w) = w^2 - w^3, at w = u c_1 / 2.
- **The family [MV]:** potential form V' = k^2 p(w) + m s, T' = w V' - k^2 Phi(w)
  (s = q(v) - t, w = u s/k) gives, for admissible seeds (p(0) = 0, int_0^1 p = 0, p(1) != 0,
  p'(1) != 2 p(1)), Keller maps with det = -k p(1)^2, fiber degree deg p + 1, degree law
  (5d-3, 5d-4, 4); new explicit counterexamples at fiber degrees 3..6 with rational collision
  certificates; the announced F is the smallest member; the mechanism is UNIQUE among scanned
  weight systems (m = 1 is the JC(2) bridge; m = 3 empty/rigid; m = 4 potential form empty by
  Groebner certificate).
- **Escape geometry [MV]:** escape <=> multiple fiber root (s = -W'/m);
  A(F) = {C = 0} union {27 A^2 C^2 - 18 A B C + 16 A + B^3 C - B^2 = 0}; real census 3-vs-1
  across that wall; F|_R^3 surjective, non-injective, constant det.
- **2D rigidity THEOREM [D/MV]:** every Gm-equivariant Keller map of C^2 is linear (all
  weights; classification + positive kill factor 1 + w1 dg + w2 df).
- **The JC(2) machine [MV]:** Keller is LINEAR in Q given P (affine gauge). Machine:
  eliminate Q -> consistency ideal in P (theory predicts it) -> parametrize -> complete ->
  invert. Results: consistency ideal at (2,3) AND (2,4) is the single equation
  (4 A0 A2 - A1^2)^2 = 0 (P's top form a perfect square); THEOREMS with explicit inverses at
  (2,3), (2,4), (2,5): P = x + ell^2 (ell = alpha x + beta y),
  Q(2,3) = y - alpha^3 x^2/beta - 2 alpha^2 xy - alpha beta y^2, inverse
  G(u,v) = (u - (alpha u + beta v)^2, v + (alpha/beta)(alpha u + beta v)^2); beta = 0 forces
  affine.
- **Cascade [verified, EXP-016/018]:** Mathieu false for SU(N >= 3); GMC, Zhao vanishing,
  Image, symmetric/gradient JC false (in the stated senses); full Dixmier and Poisson false
  with Dixmier(1) and minimal dimensions open. Published: web Collateral tab +
  manuscript-cascade/ + difusion drafts.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| F | the announced counterexample (u = 1 + xy) | EXP-001/002 |
| constructor v2 | the seed family (potential form) | EXP-004 (code/jclib) |
| the wall | 27A^2C^2 - 18ABC + 16A + B^3C - B^2 = 0 | EXP-007 |
| the landscape | weights (1,-1,-m) survey; uniqueness of m = 2 | EXP-012 |
| the machine | eliminate/parametrize/complete/invert (bilinear harness) | EXP-017/019/020 |
| jc2 checker + bridge | exact certificate adjudication; m = 1 extractor | EXP-015 (code/jclib/jc2.py) |
| keller2lib | shared planar utilities (library, graded pieces) | code/jclib/keller2lib.py |

## 3. Experiment index (verdict; load-bearing output)

001 confirmed (validation; 3-point fiber) · 002 confirmed (structure) · 003 partially refuted
(v1 lift; d = 2 rigidity) · 004 confirmed (constructor v2 + new counterexamples) · 005
confirmed w/ caveats (2D reduction) · 006 confirmed (2D scan: all linear) · 007 confirmed
(escape = multiple root; the wall) · 008 confirmed (degree laws; fiber-6 instance) · 009
confirmed (char-p certificates) · 010 confirmed (2D rigidity THEOREM) · 011 confirmed (real
census) · 012 conf 1-4/refuted 5 (landscape; uniqueness) · 013 conf 1-2/partial 3 (tropical
bridge; (2,2) exhaustive) · 015 confirmed (checker + bridge tooling) · 016 confirmed (cascade
verified) · 017 confirmed (bilinear exhaustives (2,3)/(3,3)) · 018 confirmed (Poisson +
symmetric closure) · 019 confirmed (floors; (2,3) full closure ideal) · 020 confirmed
(THEOREMS (2,3)/(2,4)/(2,5); (3,4) elimination cap-out documented) · 021 IN FLIGHT (below).

## 4. In flight: EXP-021, the uniform (2, n) theorem

Hypothesis declared (experiments/EXP-021-uniform-2n-theorem/hypothesis.md); run.py NOT yet
written. The derivation to certify (write-up in the hypothesis): in shear coordinates
(u1, u2) = (ell, x), P = u2 + u1^2 and Keller becomes the linear PDE
2 u1 Qt_{u2} - Qt_{u1} = c whose characteristic invariant is P itself; hence the COMPLETE
solution is Q = ell/beta + H(P), H an arbitrary polynomial (the free parameters B_11, B_15
seen at n = 4, 5 are H's coefficients), with the closed inverse
ell = beta (q - H(p)), x = p - ell^2, y = (ell - alpha x)/beta.
Parts: A sufficiency identity (generic H, deg <= 4); B completeness = kernel dimension of
L(Q) = J(P, Q) on deg <= n equals floor(n/2) + 1 (n = 3..8, sampled alpha/beta); C the closed
inverse verified generically; D assemble the theorem (with EXP-019/020 consistency ideals +
Wang): every planar Keller map with min degree <= 2 is invertible.

## 5. Next actions, ordered

1. Write experiments/EXP-021-uniform-2n-theorem/run.py (parts A-C per section 4), run:
   `./.venv/Scripts/python.exe problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-021-uniform-2n-theorem/run.py`
   then verdict.md; consolidate v0.11.000 (log, wiki 04/05, CHANGELOG, versions x3, tag, PR).
2. JCB-021 staged (3,4): test the quasi-triangular conjecture (consistency variety at (3, n)
   = {P linear-equivalent to x + f(ell)}) by parametrized completions + sampled converse; the
   PDE closure then gives inverses on the locus (mirror EXP-021's parts).
3. JCB-022 EXP-014 Puiseux escape obstructions at min-degree 3 (design in log session 5/8).
4. JCB-024 Hessian-nilpotent quartic extraction (needs the de Bondt-van den Essen
   symmetrization construction from the primary paper first).
5. Diffusion: both post drafts await Felipe's review (difusion/jacobian-conjecture,
   difusion/jacobian-cascade in CAOS_MANAGE); publish only on his go.

## 6. Where everything lives

- Experiments: problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-*/
  (hypothesis.md, run.py, artifacts/, verdict.md) · shared code: .../code/jclib/
- Wiki: .../wiki/01..05 · history: .../history/log.md (append-only)
- Program: program/jacobian-conjecture/{plan,state,backlog,RESUME}.md · board:
  program/portfolio.yaml
- Manuscripts: manuscript/ (main, v0.05) · manuscript-cascade/ (companion)
- Bake -> web: data-pipeline/researchlab (export_registry) -> data/derived -> frontend/ ->
  https://research.fasl-work.com (Pages via Actions on main)
- Management mirror: CAOS_MANAGE plans/caos-research/ (status, findings F1-F17, history);
  diffusion drafts in CAOS_MANAGE difusion/jacobian-{conjecture,cascade}/
- Repo flow: task work on develop -> PR -> main (tags vX.XX.000); push via the vault PAT
  (see CAOS_MANAGE credentials/general/github/pat.txt; GCM hangs, use the PAT-in-URL form).

## 7. Gotchas

- sympy nonlinear solve() can return [] on solvable underdetermined systems (EXP-013/017:
  refuted by explicit witness): use the bilinear/linear structure or Groebner emptiness
  certificates instead; always keep discard counters (no silent drops).
- Rabinowitsch auxiliaries and free symbols must be instantiated/filtered explicitly (zoo/nan
  leaks produced fake findings twice: EXP-012 C/D first passes).
- Monolithic lex Groebner at ~19 variables exceeds ~10 min (EXP-020 part B): stage
  eliminations degreewise/blockwise.
- Poly(..., extension=False) is invalid in sympy 1.14.
- Runs: cap Bash calls at 600000 ms; long runs in parts (run.py <PART>); artifacts via tee.
- Frontend footer version reads frontend/package.json: bump it with pyproject and
  researchlab/__init__ together (three places, one version).
- Screenshot verification: tools/visual-verify in CAOS_MANAGE with
  PLAYWRIGHT_BROWSERS_PATH=E:/_Temp/ms-playwright; preview server via npx vite preview.
