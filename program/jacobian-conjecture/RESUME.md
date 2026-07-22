# RESUME - Jacobian conjecture program (updated 2026-07-22, session 30 closed)

The single first-read for a fresh session (contract: methodology/07-session-handoff.md).

## 1. State in one screen

- **World state:** JC is FALSE for every N >= 3 (Alpoge/Fable map; EXP-001 validated
  exactly). JC(2) is open and is the program's target. NEW (session 22): HC(48) is false
  with OUR explicit witness (EXP-041): the symmetric/gradient JC and Zhao's Vanishing
  Conjecture now fall EXPLICITLY, not just existentially.
- **The theorem ladder (all machine-certified, Theorems 2-4 unconditional):**
  2D equivariant rigidity (EXP-010); the uniform min-degree-2 theorem + shear closure
  (EXP-021/022); T1 weight-class (EXP-029); T2 lower-weight tails (EXP-030/031); T3
  x-anchored edges (EXP-032); T4 vertex dichotomy (EXP-033); annihilation closed form
  (EXP-036). Novelty (adversarial pass, dossier 2026-07-22): T1, T2, rigidity NOT FOUND;
  T3 not-as-stated (method classical); T4 sharp-dichotomy form (GGV Prop 4.1 has the
  counterexample half).
- **The open core and its instrument:** components must swallow x with a mixed staircase
  (EXP-033/034/035). THE STAIRCASE TRANSPORT (EXP-037): the Keller window is
  block-triangular under the x-edge grading (diagonal = MINIMAL P-class); classwise
  elimination is executable and exact; the obstruction sits at the CONSTANT'S class;
  generic reduced equation -2a = 0 on x + a x^u y^v + b x^d. THEOREM 5 target: clear the
  generic elimination into all-parameter certificates + re-instantiate EXP-036.
- **The recalibrated frontier (EXP-040 + literature dossier):** verified coverage = the
  FULL interval gcd <= 8, primes, 2p, B >= 16 (Heitmann), B = 16 or B > 20 (GGV): our
  gcd 2/9/12/18 certificates are replications. LIVE targets (JCB-040): GGV's B = 16
  normal form (explicit directions + reduced shape) and the lone surviving pair
  (72, 108) below 125 (closing it raises the floor to 125).
- **Instruments:** the JC(2) machine (eliminate/complete/invert, validated at
  (2,3)..(2,5), (3,3), (3,4)); the transport chain (EXP-037); the matched-pair law
  (EXP-038: halves window unknowns, adds no depth); the properness certificate (EXP-014:
  one-call proper/escape adjudication; JC(2) <=> empty Jelonek set); jc2 checker + bridge
  (EXP-015); rotate-descent (EXP-034).
- **Routes:** program/jacobian-conjecture/routes-2026-07-22.md (R1 transport PURSUE; R4
  B = 16 + (72,108) PURSUE; pair TOOL; properness HOLD; rotation KEEP; equivariant +
  witness DONE/publish; char-p DORMANT; Lean HOLD).

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| F | the announced counterexample (u = 1 + xy) | EXP-001/002 |
| constructor v2 | the seed family (potential form) | EXP-004 (code/jclib) |
| the wall | 27A^2C^2 - 18ABC + 16A + B^3C - B^2 = 0 | EXP-007 |
| the machine | eliminate/parametrize/complete/invert | EXP-017/019/020/039 |
| the transport chain | classwise elimination under the x-edge grading | EXP-037 (run.py transport()) |
| matched-pair law | alpha p (ib-ja) q_ab = beta q (id-jc) p_cd on matched outputs | EXP-038 |
| properness certificate | resultant leading coefficients constant | EXP-014 |
| f_H / P_star | the dim-48 witness quartic (382 Q(i) monomials) + collision | EXP-041 (artifacts/) |
| jc2 checker + bridge | exact certificate adjudication; m = 1 extractor | EXP-015 (code/jclib/jc2.py) |
| keller2lib | shared planar utilities (library, graded pieces) | code/jclib/keller2lib.py |

## 3. Experiment index (verdict; load-bearing output)

001-036: see wiki/05-experiments.md (unchanged from session 21's index). Session 22 adds:
037 confirmed, prediction 3 refuted as declared (staircase transport: block-triangular;
obstruction at the constant's class; generic -2a = 0) . 038 confirmed (pair corner: exact
matched-pair law; no added depth; half the unknowns) . 039 confirmed ((3,n) closure: cube
force by elimination + GL2 orbits; 4/4 inverses; column classically covered) . 040
confirmed (JCB-028 closed by subsumption; frontier recalibrated to B = 16 + (72,108);
gcd 9/12 demoted to replications) . 014 confirmed (properness instrument; reserved slot
filled) . 041 confirmed (THE DIM-48 WITNESS: HC(48) false explicitly; Thompson input
verified with index corrected 17 -> 18; P_star falsifies Zhao's VC explicitly) . 042
confirmed, prediction 2 refuted-replaced (THEOREM 5 WINDOW FORM: cleared all-parameter
certificates, monomial pairings, window law -c_N a^N; annihilation transfers) . 043
confirmed (x^m-anchored edge operator NEW; B = 16 core = staircase transport; scoping
blocks 13/22) . 044 confirmed (THE CERTIFICATE TOWER: normalized obstruction -2a
window-independent; Theorem 5 all-degree [D]; gap = TOWER LEMMA) . 045 confirmed
(degree-32 frontier certificates; similarity filter x18.8: (48,64) drops to 111 unknowns)
. 046 confirmed (THE TOWER LEMMA PROVED, primitive-top + d >= u+v scope: THEOREM 5
UNCONDITIONAL there; proper-power odd resonances measured zero, derivation queued) . 047
confirmed (filtered (48, <= 64) certificates: three degree-48 samples empty, 2.4-3.6 s
each: the N2 pipeline validated at target scale) . 048 confirmed, universal-kill refuted
(THE HALF-PLANE CERTIFICATE mechanism for proper-power odd resonances) . 049 confirmed
(THEOREM 6, the universal tower: one certified window = all-degree exclusion for
non-proper-power tops; multi-edge harvest) . 050 confirmed (FIRST certificates at the
(72,108) degrees, ~1 s each) . 051 confirmed (THE HALF-PLANE TOWER LEMMA: one
H-certificate = all-degree exclusion on the y-most-corner staircase stratum; P32 and
P72 excluded at ALL partner degrees).

## 4. In flight

Nothing mid-run. Session 23 closed with EXP-042/043, THE MANUSCRIPT SPLIT (A
foundational v0.07 / B planar-program v0.01 NEW / C cascade v0.02 with the explicit
witness; all three PDFs compile), and the routes addendum (current view + N/M/L map +
the standing decision rule: every new experiment names its route).

## 5. Next actions, ordered

1. DONE (EXP-051): the HALF-PLANE TOWER LEMMA covers the y-most-corner staircase
   stratum at all degrees, proper-power tops included. Remaining theory targets:
   (a) shapes where the top corner is NOT the y-most support point (y-heavy tails):
   currently Theorem 6 or full-window towers; map what escapes ALL current lemmas;
   (b) the y-anchored (quasi-triangular-type) completions classification (JCB-035,
   the endgame frame): JC(2) = the triangular family is everything.
2. N2 / JCB-040: EXP-053 = per-stratum 576 certificates; EXP-054 REFUTED rigid
   universality (51 entering combinations) while confirming the 576 pairing is
   stable across strata. FIRST TASK NEXT ROUND: the PERTURBATIVE covector
   Lambda(eps) (linear-in-Lambda, affine-in-eps nullspace, batched over the 51
   entering monomials; termination evidenced by 576-stability). Success = the
   reduced (72,108) stratum closes universally; then the dossier's remaining
   forcing branches; then the floor rises to 125.
3. JCB-041 remainder: the screenshot verification pass ONLY (bake is automatic and
   verified; wiki 04 rewritten in session 24). FELIPE still validates the novelty
   phrasing before submission.
4. JCB-042 (Felipe's call): report the index correction (17 -> 18) upstream to the
   Thompson repo.
5. JCB-018 (optional): Lean hardening of T1/T2/rigidity after the manuscript pass.
6. Diffusion: existing drafts still await Felipe; the witness merits its own post
   (draft only after Felipe validates the framing).

## 6. Where everything lives

- Experiments: problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-*/
  (hypothesis.md, run.py, artifacts/, verdict.md) · shared code: .../code/jclib/
- Context dossiers: .../context/2026-07-22-literature-pass-dossier.md (novelty + floor)
  and .../context/2026-07-22-symmetrization-dossier.md (witness construction; local
  source PDFs in E:\_Temp\jc-dossier\)
- Wiki: .../wiki/01..05 · history: .../history/log.md (append-only)
- Program: program/jacobian-conjecture/{plan,state,backlog,RESUME,routes-2026-07-22}.md
- Manuscripts (three-paper record, split 2026-07-22): manuscript/ (A foundational,
  v0.07) · manuscript-planar/ (B planar program, v0.01) · manuscript-cascade/ (C, v0.02)
- Bake -> web: data-pipeline/researchlab -> data/derived -> frontend/ ->
  https://research.fasl-work.com (Pages via Actions on main)
- Management mirror: CAOS_MANAGE plans/caos-research/ (status, findings, history)
- Repo flow: work on develop -> PR -> main (tags vX.XX.000); push via the vault PAT
  (CAOS_MANAGE credentials/general/github/pat.txt; GCM hangs, use PAT-in-URL).

## 7. Gotchas

- sympy nonlinear solve() can return [] on solvable underdetermined systems: use the
  linear/bilinear structure or Groebner emptiness; keep discard counters.
- Fraction-field RREF/nullspace steps are GENERIC-only (EXP-024): sound all-parameter
  statements need cleared certificates; numeric runs are sound pointwise.
- Radical membership by raw powers can stall (EXP-039 A4: powers to 8 insufficient);
  GL2-orbit classification closed it instead: prefer structural completeness arguments.
- "Trace zero" for matrix polynomials means the SUM of the diagonal entries, not each
  entry (EXP-041 D bug, fixed); guard experiment drivers with `if __name__ == "__main__"`
  (an import executed a whole run once).
- Monolithic lex Groebner at ~19 variables exceeds ~10 min: stage or avoid (top-force
  arguments are cheaper).
- Runs: cap Bash calls at 600000 ms; long runs in parts (run.py <PART>); artifacts via
  tee. Frontend footer version reads frontend/package.json: bump with pyproject and
  researchlab/__init__ together (three places, one version).
- Screenshot verification: tools/visual-verify in CAOS_MANAGE with
  PLAYWRIGHT_BROWSERS_PATH=E:/_Temp/ms-playwright; preview via npx vite preview.
