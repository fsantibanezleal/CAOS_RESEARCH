# EXP-005: the n = 6 tropical prevariety at powers-of-3 valuations

Declared: 2026-07-24, BEFORE any run. Route: R2/tropical lane; the n = 6 attempt
Jensen-Leykin leave open (their single tried valuation: recession cones not all
pointed, ~100 cpu-days; "more experimentation with different valuations or different
versions of the Albouy-Chenciner equations is needed"). Felipe's explicit GO
(2026-07-24) covers this multi-day run. Builds on EXP-003 (exact JL25 reproduction)
and EXP-004 (screening: powers-of-3 was the unique globally pointed valuation family
among six tested at n = 5; dropping the dependent symmetric equations is
catastrophic, so the S1 system is used).

## Question

Is the tropical prevariety of the n = 6 planar central-configuration system (30
asymmetric AC + 15 symmetric AC + 15 planar Cayley-Menger polynomials), with mass
valuations (1, 3, 9, 27, 81, 243), pointed (globally or per component)? A YES,
verified per component with exact certificates, would give GENERIC-MASS FINITENESS
OF PLANAR CENTRAL CONFIGURATIONS FOR n = 6 by the Jensen-Leykin argument
(Bieri-Groves + density of tropicalization fibers): a new theorem at the frontier.
A NO is itself frontier data: the failing components' structure directs the
equation-variant and valuation follow-ups.

## Falsifiable predictions

- **P1 (feasibility).** The computation completes within the 96-hour cap on 30
  threads with --bits 64 (throughput calibrated in EXP-003: ~25 cpu-min per
  wall-min; JL25's n = 6 attempt was ~100 cpu-days).
- **P2 (the frontier question; genuinely uncertain).** The prevariety is pointed
  per component (exact certificates via comet_analysis: separating vector per
  component, verified in rational arithmetic). Basis for the prediction: powers of 3
  was the ONLY globally pointed family at n = 5 (EXP-004), and JL25 observe their
  method has "more hope" in the general n = 6 case than in special cases; the
  prediction is declared at LOW confidence and its refutation is a fully valuable
  outcome (the failing comets become the target list for S1+IU and valuation
  variants).
- **P3 (structure record, unconditional).** Whatever the outcome, the run records:
  the f-vector, the count of unbounded directions and their sign profile, the
  component count, and the list of non-pointed components (if any) with their rays:
  the data JL25 do not publish for their failed attempt.

## Success / failure criteria

- P1 fails if the cap strikes (recorded; restart decision goes to Felipe with the
  partial timing data).
- P2: machine decides; verdict states pointed / not-pointed with exact
  certificates either way. If pointed per component: the claim "generic finiteness
  for n = 6" is drafted but goes to FELIPE FIRST (statement-level), then to the
  overflow-checked rerun (gfan templated integer class, ~10x slower, per JL25's own
  hardening) BEFORE any external communication; the manuscript gains the result
  only after that rerun.
- P3 always deliverable.

## Preflight addendum (methodology/12, added 2026-07-24 after the standard landed; the run was declared before it existed)

- **P1 source-complete.** JL25 read in full, including section 4.3 (their own n = 6
  attempt) and 4.2 (why special cases are harder); HM06 read in full; HJ11 read.
  Their closing remarks are exactly what motivates this run, so no unread source is
  known to settle it.
- **P2 tooling smoke test.** Satisfied by EXP-003: the identical pipeline reproduced
  both published n = 5 datasets on this machine before any n = 6 time was spent.
  Note the gap this rule would have caught earlier: gfan writes no incremental
  progress, so a failure is only visible at abort; the two overflow aborts were
  detected within minutes precisely because they abort loudly.
- **P3 premise dependencies.** (a) Pointedness of every comet implies dimension 0
  and hence generic finiteness: JL25's argument via Bieri-Groves and density of
  tropicalization fibers, read in full. (b) Our comet extraction and certificates
  are sound: validated in EXP-004 by reproducing their published 257-component
  count. (c) Powers of 2 are a viable family: established by EXP-004 at n = 5.
- **P4 one-sidedness.** POINTED is a positive result (it would establish generic
  finiteness for n = 6, subject to the hardening rerun and the Felipe-first gate).
  NOT-POINTED proves nothing about finiteness: the prevariety only over-approximates
  the tropical variety, so a non-pointed comet may still contain no tropical curve.
  A negative outcome therefore yields DATA (which comets survive, with their rays),
  not a refutation of finiteness, and directs the next equation-variant attempt.
- **P5 invariant-first.** No single invariant is known to decide n = 6 cheaply; the
  candidate cheap probes (f-vector growth, global recession-cone sign profile) are
  computed as by-products and recorded, but none of them can settle the question.
- **P6 budget and kill criterion.** 7-day timeout per variant, two variants in
  parallel on 15 and 14 threads. If a variant hits the timeout, it is recorded as
  inconclusive-at-budget and the decision to extend goes to Felipe with the measured
  progress; no silent restarts.

## Method / environment

gfan 0.7 (EXP-003 install, hashes recorded), WSL, `gfan _nbody -N6 --masses
--alsosymmetric --cayleymenger2`, sed substitutions m_i -> t^{3^{i-1}}, `gfan
_tropicalprevariety --usevaluation -j30 --mint --minx --bits 64`, output to
E:\_Datos (expected large) with in-repo f-vector/rays extracts and hashes;
comet_analysis.py for the per-component certificates. Deterministic.
