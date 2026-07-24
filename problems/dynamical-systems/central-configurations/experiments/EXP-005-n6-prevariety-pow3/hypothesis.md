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

## Method / environment

gfan 0.7 (EXP-003 install, hashes recorded), WSL, `gfan _nbody -N6 --masses
--alsosymmetric --cayleymenger2`, sed substitutions m_i -> t^{3^{i-1}}, `gfan
_tropicalprevariety --usevaluation -j30 --mint --minx --bits 64`, output to
E:\_Datos (expected large) with in-repo f-vector/rays extracts and hashes;
comet_analysis.py for the per-component certificates. Deterministic.
