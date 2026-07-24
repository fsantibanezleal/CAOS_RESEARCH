# WIP - C13 fork (EXP-077) + quadruple sweep reorder (2026-07-24, session 47)

Validation-agent handoff. Two tasks, both done. Nothing here bumps versions,
opens PRs, or touches other problems. All commits are on `develop` and pushed.

## TASK 1 - EXP-077: the C13 fork is DECIDED (fork collapses)

**Location:** `problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-077-c13-fork-decision/`
(hypothesis.md declared before run.py; exact-arithmetic run.py; artifacts/output-2026-07-24.txt;
verdict.md). Regression gate GREEN. Committed + pushed.

**Verdict: the d_0 fork the dossier / EXP-076 feared DOES NOT EXIST.** The discard's
forcing step extends to C13; only the final endgame exclusion is source-dependent.

Machine-derived (exact), all from the secured primary sources
(E:\_Temp\ggv-sources\1401\src.tex and \1605\src.tex):

1. **q_1 = 4 for C13, identical to the (8,32) sibling.** [GGV1 = arXiv 1401.1784,
   Prop "Case II" tex 2563 + Thm 7.6(3) tex 4288]: en_{4,-1}(F_1) = mu·(abar,bbar)
   with (abar,bbar) = (2,7) the primitive of the SHARED corner A1 = (8,28), d = 4,
   mu = (rho+sig)/v_{4,-1}(2,7) = 3, so en(F_1) = (6,21) and q_1 = d/gcd(mu,d) = 4.
   The (4,-1) leading form of P is exactly the shared edge A1--A2; A0 sits strictly
   below it (v_{4,-1}(A0) = -8 for C13 vs 0 for the sibling) and never reaches the
   en-point. The recorded v_{4,-1}(A0) difference is real but inert here.

2. **d_0 <= 4 for C13, NOT <= 8.** l_{1,0}(P) = R^{m d_0} forces
   d_0·st_{1,0}(R) = st_{1,0}(P). The bottom vertex of the max-x (x=8) edge is
   st_{1,0}(P) = A1 = (8,28), SHARED with the sibling (below A1 the polygon turns to
   A2 at x = 11/4 < 8). So d_0 | gcd(8,28) = 4. **d_0 = 8 is arithmetically
   impossible** (28/8 not integer; R would need y^{3.5}). The (8,40) = 8(1,5) reading
   bounds d_0 only by the TOP vertex and is strictly weaker.

3. **d_0 = 4 UNIQUELY (no fork).** q_1 = 4 | d_0 and d_0 <= 4 give d_0 = 4, exactly
   as the sibling.

4. **EXP-076 correction.** EXP-076's d_0 = 8 / R' = x y^4(y-1) branch is WRONG (its
   bottom vertex is (8,32), not the shared (8,28)); its post-shift corner (8,12) does
   not arise. The corrected shape is R = x^2 y^7·(cubic), bidegree (2,10), vs the
   sibling's (2,8): a degree-3 y-tail vs degree-1. Under the analogous single-root
   shift both give the candidate last corner (8,4).

5. **The GGV2 exclusion is sourced exactly.** [GGV2 = arXiv 1605.09430, Prop "casos
   imposibles" tex 1009 + remark tex 1053]: wp(n',n'-1) with n' >= 2 is NOT a possible
   last lower corner; the remark names (2,1),(3,2),(6,3),(8,4) explicitly. This is the
   published "Proposition 3.29" analog (source numbering is symbolic labels; the
   printed 3.29 is this statement, the (8,4) exclusion stated in the following remark).
   (8,4) = 4(2,1), n' = 2 -> excluded. Verified on the explicit list and against
   non-forms in run.py.

### The ONE remaining gap (DERIVATION NEEDED, source-dependent) - FOR THE MAIN SESSION

Whether C13's degree-3 tail, after the shift, terminates at (8,4) as the **LAST**
lower corner of H(P) (vs the two extra shifted roots spawning a longer admissible
sub-chain that lands elsewhere). The sibling's single root leaves nothing below the
shift corner, so (8,4) is clean; a cubic tail may not. Certifying this needs GGHV22
section 3's exact (8,32) endgame transcribed and adapted to a multi-root tail (the
number of reduction steps; whether Case II with #factors = 3 or 4 changes the
terminal corner).

**No floor-moving claim is made.** IF this resolves to (8,4) (or any excluded
wp(n',n'-1)), the C13 (8,40) chain discards and the [125,150] floor implication is a
STATEMENT-LEVEL claim that goes to the main session for adjudication/publication. The
narrowed question is much cheaper than the dossier's original three-item gap list:
q_1 and d_0 are now settled exactly; only the multi-root shift terminus is open.

## TASK 2 - EXP-075 quadruple sweep REORDERED (blockers-first), relaunched

**Location:** `problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-075-degree3-quadruple-supports/run2.py`
(committed + pushed). Artifact: `artifacts/output-run2-2026-07-24.txt`.

- **What changed.** run2.py supersedes the linear-order run.py. It imports EXP-071's
  pipeline via EXP-075's `setup_ctxs` exactly as EXP-072 does (deg3_subsystem_feasible,
  modfrac, two-prime confirm, the 20-sample regression gate). It orders the same
  C(51,4) = 249900 quadruple supports BLOCKERS-FIRST: the 27762 supports containing
  >= 2 of the 8 degree-1 blockers (1,0),(3,5),(4,6),(4,7),(5,8),(7,13),(8,14),(8,15)
  first, then the 222138 remainder. Deterministic/stable order, so resume-by-index is
  well-defined: `run2.py <index>`.
- **Status.** Smoke-tested (setup ok, 51 ops, all 8 blockers present at ops indices
  [7,25,31,32,37,47,49,50], 27762 blocker-heavy, regression gate green). Relaunched in
  the BACKGROUND and confirmed past checks 0-2 into the sweep. The old linear run.py
  background task (the two matching PIDs from session 46, started 08:06:40, at resume
  index ~6400 of 249900) was STOPPED so it does not compete for CPU; its historical log
  remains at `artifacts/output-2026-07-24.txt`.
- **Note on the run2 process.** It was launched detached (nohup) from a Bash call, so
  it is NOT tracked by the harness background-task notifier. The main session should
  poll `artifacts/output-run2-2026-07-24.txt` for progress (checkpoints every 200
  supports with a `[resume index N]` tag and a blocker-heavy/remainder phase label). If
  it dies, resume with `python run2.py <index>`.
- **IF the sweep finds an infeasible quadruple support:** that CLOSES degree 3. run2.py
  writes the verdict line to its artifact but the STATEMENT-LEVEL claim ("no degree-3
  covector -> degree 3 closed") must go to the MAIN SESSION - do not publish from the
  validation agent. Watch the artifact for a line beginning `[PASS] 3: ... INFEASIBLE`.

## What the main session should pick up

1. **EXP-077 endgame (highest value):** transcribe GGHV22 arXiv 2204.14178 section 3's
   exact (8,32) endgame (the shift/reduction that reads off the last lower corner from
   R) and adapt it to C13's cubic tail. If the terminus is an excluded wp(n',n'-1),
   the (8,40) chain discards -> first [125,150] floor progress. Everything upstream
   (q_1 = 4, d_0 = 4, R = x^2 y^7·cubic, the exact casos-imposibles criterion) is
   settled and in EXP-077.
2. **The quadruple sweep:** monitor run2's artifact. Blocker-heavy phase (~27.8k
   supports) is the promising region; a hit closes degree 3 (statement to the main
   session). All-pass through both phases stages the constructive GF(p) path (R2).
3. **Wiki/history updated:** wiki/05-experiments.md has the EXP-077 row and an EXP-076
   correction note; history/log.md has the session-47 entry. RESUME.md not touched
   (release/handoff owned by the main session).
