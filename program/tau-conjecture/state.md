# Shub-Smale tau conjecture: state (heartbeat)

- **State:** exploring (opened 2026-08-01; scoped 2026-07-20).
- **Done (2026-08-01, rounds 1-3):** problem opened with full primary-
  source pass; EXP-001 (census anchored to Markstroem 14/14;
  z_max(1..4) = 1,2,3,3); EXP-002 (z_max(5) = 4; DOS/Chebyshev
  mechanism); Chebyshev-tower lemma proved; last-gate lemma; EXP-003
  (z_max(6) = 5 via the multiply-by-x move; our prediction refuted);
  sympy cross-check 284/284; wiki 01-03; approaches evaluation +
  research lines RL-1..6.
- **Done (2026-08-01, rounds 4-5):** monic stall theorem PROVED (single-
  map towers depth-independently bounded for any monic degree >= 2);
  views V5-V8 minted (SAT lane, bottom law, moves calculus, arithmetic
  dynamics) + RL-7..9; **EXP-005 CONFIRMED** (family loophole EMPTY for
  x^2 - c, c <= 200: max yield 5 only at c = 2; DISCOVERED the 2-cycle
  series c = m^2+m+1; classical cycle-length <= 2 ceiling closes the
  iteration flank); **EXP-004 CONFIRMED** (z_max(7) = 5: the bottom law
  BREAKS; sequence 1,2,3,3,4,5,5 with plateaus at 4 and 7; depth-6
  frontier 25,844,905 states exact; 2,013,706 depth-7 polynomials;
  min tau for 6 roots in [8,9]). Wiki 04 transcribed; 03 updated.
- **Done (2026-08-01, round 6):** the census MANUSCRIPT written from the
  verdicts, built, and PUBLISHED on Zenodo: v0.01, CC-BY-4.0, version
  DOI 10.5281/zenodo.21753439, concept DOI 10.5281/zenodo.21753438
  (record live, 200). TCB-022 done.
- **Now:** rounds closed; nothing running.
- **Next:** close the [8,9] window for 6 roots (TCB-021: RL-8 moves
  hunt, then RL-7 SAT decision); TCB-005 canonicalization or compiled
  backend for depth 8; reads (Doyle-Poonen, Narkiewicz, Cheng full);
  wiki 05 (open questions); manuscript updates ship as Zenodo NEW
  VERSIONS on the same concept DOI.

## Round 7 (2026-08-02)

- **EXP-006 CONFIRMED: THE WINDOW IS CLOSED: minimal tau for 6 distinct
  integer roots = 8.** The times-case reduction (final gate x reduces to
  root-set co-occurrence) scanned all 25,844,905 depth-6 states in 2h23m:
  408 witnesses; three reconstructed as explicit 8-gate programs and
  verified independently. Our emptiness prediction REFUTED (third time);
  the five-rooter taxonomy corrected (7 root-set patterns, incl.
  non-consecutive). The hunt confirmed its own blind spot (chained
  subtraction sharing beats independent constant builds).
- Paper v0.02 PUBLISHED as a Zenodo new version: DOI
  10.5281/zenodo.21763182 (concept unchanged 10.5281/zenodo.21753438);
  metadata synced. SAT design note persisted (EXP-007 groundwork,
  rescoped to z_max(8)).
- Wiki 03/05 updated/written. Next: TCB-025 (max union re-scan), TCB-005
  (depth-8 backend), TCB-026 (punctured root sets anatomy), reads.

## Round 8 (2026-08-02)

- **EXP-007 CONFIRMED** (3h07m, complete; 408 anchor reproduced): max
  union = 6: NO 8-gate seven-rooter via final multiplication (our first
  surviving emptiness prediction); z_max(8) = 6 unless a final-pm 8-gate
  7-rooter exists (SAT residual, TCB-029). Seven-root threshold in
  [8, 10] (10-gate witness explicit).
- **Digit census (V9) measured through tau = 7**: odd-root ladder
  1,2,2,2,2,3,4 (prediction "max 3" REFUTED, fourth refutation: the
  digit world has its OWN record family, (x^2-1)(x^2-9) at 7 gates,
  roots {+-1,+-3} all odd); p=3 ladder 1,1,1,2,2,3,3.
- **Punctured anatomy (TCB-026) closed**: two-center DOS products
  x^2(x^2-1)(x-2)(x-4); the hole is the second DOS center.
- V10 (three-worlds trichotomy) persisted; KPT15 pinned precisely;
  TCB-027/028/029 minted. Paper v0.03 queued DELIBERATELY (with the
  z_max(8) resolution).
- **Next:** TCB-029 (SAT final-pm decision at 8), then v0.03; TCB-027
  mod-p instrumentation; TCB-005 depth-8 backend as the larger goal.

## Round 9 (2026-08-19 continuation; EXP-008 in flight)

- EXP-008 (SMT final-pm residual at depth 8) declared 2026-08-03; the
  first launch died with a session teardown before any checkpoint (the
  plain-NIA known-answer was intractable). AMENDED 2026-08-19 (recorded
  in hypothesis.md before the re-run): QF_NIA solvers; value-bounded
  known-answer (SAT-side validation only); ladder root-bounded ->
  doubly-bounded fallback -> unbounded attempt; per-phase immediate
  checkpoints to artifacts/sat8.json.
- The re-run is DETACHED from the session (survives teardown):
  PID 58300, log experiments/EXP-008-sat-depth8/run_detached.log.
  A fresh session should READ artifacts/sat8.json first: phases present
  there are decided; absent phases may still be running (check the PID/
  log mtime) or dead (relaunch run.py with --phase for what is missing).
- V11 (evaluation-matrix view) persisted 2026-08-03; TCB-030 minted;
  subspace-theorem channel swept: no prior art, flagged [C].

## Round 9 close (2026-08-19)

- **EXP-008 INCONCLUSIVE (solver-intractable), honestly recorded.** Three
  launches + two diagnostics: the degenerate-CEGAR incident (179,649
  zero-model blocks) fixed by a structural f != 0 column and loop
  budgets; the known-answer then hit its cap as `unknown`; with concrete
  roots still `unknown`; with the FULL witness pinned: sat in 0.5 s and
  exact replay. Encoding semantics CORRECT; Z3 NIA search is the wall.
  z_max(8) remains: = 6 unless a final-pm 8-gate 7-rooter exists.
  TCB-029 re-scoped (bit-blasted SAT or census backend); TCB-005 is now
  the leading route; v0.03 stays queued.
- RL-3 T(S) structure lemmas PROVED (anti-monotonicity, union+1,
  translation+1, reflection+1; scaling recorded OPEN as TCB-031); exact
  T-table through size 6. V11 evaluation-matrix view persisted
  (TCB-030); subspace channel swept: no prior art.
- Methodology upgrades standing: detached long runs + per-phase
  checkpoints; loop-level kill criteria (a per-check timeout is not a
  phase budget).
- **Next:** TCB-005 (depth-8 census backend: canonicalization proofs or
  compiled/parallel engine) as the route to z_max(8) AND the residual;
  TCB-027 mod-p instrumentation; reads.
