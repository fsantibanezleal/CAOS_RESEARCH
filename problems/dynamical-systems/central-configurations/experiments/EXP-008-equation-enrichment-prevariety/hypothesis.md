# EXP-008: does ADDING equations shrink the prevariety? (the enrichment law at n = 4)

Declared: 2026-07-24, BEFORE any run. Route: R2/tropical lane. Backlog: CCB-031
(the ADD direction; EXP-004 settled that REMOVING is never right).

## Question

EXP-002 measured the enrichment law affinely (asymmetric equations plus the
energy-inertia relation make the n = 3 ideal zero-dimensional directly) and EXP-004
measured its tropical shadow negatively (removing the dependent symmetric equations
destroys the certificate everywhere). The positive direction is untested: does
ADDING further valid equations SHRINK the prevariety and make hard cases certify?

The sharp test case is the one Jensen-Leykin single out as hard: at n = 4 with
EQUAL valuations (0,0,0,0), the computation is equivalent in difficulty to
Hampton-Moeckel's original, and our EXP-004 run left it with a single undecided
comet (49 recession generators). Hampton-Moeckel needed Dziobek's equations, which
at n = 4 planar are valid because the planar stratum IS the Dziobek stratum
(dim = n - 2 = 2). So the enrichment they needed is exactly the one available here.

## Setup

Systems at n = 4 (all with the planar Cayley-Menger determinants):
  A1 = EXP-004's S1 (asymmetric + symmetric AC + CM), the baseline;
  A2 = A1 + the energy-inertia relation e_IU;
  A3 = A1 + Dziobek's equations (S_12 S_34 = S_13 S_24 = S_14 S_23, cleared);
  A4 = A1 + e_IU + Dziobek.
Valuations: (0,0,0,0) equal (the hard case), (1,2,4,8) powers of 2 (a control that
already certifies), (0,1,2,3) arithmetic.
Decision: exact per-comet pointedness (the EXP-007 instrument), never heuristics.

## Falsifiable predictions

- **P1 (monotone shrinking).** For every valuation, each added family gives an
  f-vector that is entrywise NOT LARGER than the baseline's, and A4 is strictly
  smaller than A1 in at least one entry. Rationale: added valid equations can only
  cut the prevariety, since it is an intersection of tropical hypersurfaces. FAILS
  if any entry grows, which would mean an implementation error in the added
  equations rather than mathematics.
- **P2 (the hard case yields).** With Dziobek adjoined (A3 or A4), the equal-valuation
  case (0,0,0,0) at n = 4 becomes fully pointed: every comet certified pointed by
  the exact decider. This is the prediction with real content: it would show that
  the enrichment which rescued Hampton-Moeckel's algebraic proof also rescues the
  tropical certificate at the same case, and it would give a purely polyhedral
  generic-finiteness certificate at the specialization Jensen-Leykin call hard.
  Declared at MEDIUM confidence; a refutation is informative (it would separate the
  algebraic and tropical roles of the Dziobek equations).
- **P3 (controls unchanged in verdict).** The valuations that already certify under
  A1 still certify under A2, A3, A4 (no positive flips).

## Preflight (methodology/12)

- **P1 source-complete.** Hampton-Moeckel read in full: their Section 2.2 gives the
  Dziobek equations and states they hold for planar noncollinear four-body
  configurations, with the perpendicular-bisector argument for nonzero areas; they
  state explicitly that they could not run their method on the six AC equations
  alone. Jensen-Leykin read in full: Section 4.2 states the equal-valuation n = 4
  case reduces to Hampton-Moeckel's difficulty. Hampton-Jensen read: they keep the
  redundant asymmetric family deliberately. No unread source bears on the question.
- **P2 tooling smoke test.** The pipeline is EXP-004's, already exercised on 16
  cells; the only new code is the Dziobek generator in cclib, which is unit-tested
  against the known identity at the square and the equilateral-plus-center
  configuration before any prevariety run.
- **P3 premise dependencies.** (a) Dziobek's equations are valid at n = 4 planar
  noncollinear: Hampton-Moeckel Section 2.2 (primary, read). Note the scope: they
  hold on the noncollinear stratum, so a certificate obtained with them covers the
  noncollinear part, and the 12 collinear classes are handled classically by
  Moulton. This scope limitation is stated in the verdict regardless of outcome.
  (b) e_IU is a consequence of the AC equations: Hampton-Jensen equation (7).
  (c) The comet decomposition and exact decider: validated in EXP-004 and EXP-007.
- **P4 one-sidedness.** P1 is two-sided (growth refutes the implementation). P2 is
  effectively one-sided for the mathematics: pointedness under A3/A4 gives a
  certificate for the noncollinear stratum, while failure proves nothing about
  finiteness (the prevariety only over-approximates the tropical variety).
- **P5 invariant-first.** Before the runs, the f-vector comparison alone answers P1
  cheaply, and the generator count of the hard comet is the cheap progress
  indicator for P2.
- **P6 budget and kill criterion.** n = 4 cells cost seconds in EXP-004; cap 600 s
  per cell, 1 hour total. If Dziobek at n = 4 does not finish in that budget, the
  cell is recorded inconclusive-cap and the lane continues.

## Success / failure criteria

SUCCESS: P1 and P3 hold and P2 is decided either way with exact certificates.
FAILURE: an f-vector grows (implementation error) or a control flips (instrument
alarm); either stops the lane until resolved.

## Method / environment

`run.sh` mirrors EXP-004's grid runner with the extra systems generated by cclib
(Dziobek and e_IU appended to gfan's `_nbody` output in the same ring), then the
EXP-007 exact decider on every comet. Deterministic; artifacts and hashes persisted.
