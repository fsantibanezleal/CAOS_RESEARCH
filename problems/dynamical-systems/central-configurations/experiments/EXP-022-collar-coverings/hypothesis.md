# EXP-022: the collar coverings (hypothesis, declared before the runs)

2026-08-19. The k = 3 chain step needs the ladder dim(R_j meet shape+) <= j
for j = 0, 1, 2 on the WHOLE open gauged stratum (u, p > 0, f = v - q != 0),
not only on the EXP-021 core. The slice-limit route (prove a rank bound on
the boundary slice, transfer by semicontinuity) has a closure hole: a
low-rank 2-dim set can hide in a shrinking tube near the limit slice, and
controlling the limit slice alone does not control nearby slices. We
therefore EXTEND THE COVERINGS instead: every collar becomes a certified
interval covering of a rescaled-analytic matrix on a region that includes
its boundary face, and only genuine singular sets (collisions) are excised
into lower-dimensional blow-up coverings or exact lemmas.

## Ladder level j = 0 (CLOSED here)

r0-lemma.py: J = 0 forces d1A = d2A and d1B = d2B (four single-s-term
entries with monomial brackets), hence v = 0 = q, hence f = 0: OFF the
stratum. R_0 meet stratum = EMPTY, globally, exactly. Levels j = 1, 2 off
the exceptional balls follow from the rank >= 3 coverings; on the balls
from the rank-2 + gradient-pair certificates (EXP-021 addendum).

## The region atlas (u, p > 0 after the gauge a1 = 1, a2 = -1)

Bounded part (u, p <= 3, |v|, |q| <= 3):
- A_core: u, p in [1/4,3], |f| >= 1/4. EXP-021 integrated (running).
- A_band: u, p in [1/4,3], |f| <= 1/4, max(|u-p|, |f|) >= 1/16. THIS
  experiment, part (a): same entry matrix (nonsingular: cs >= 1/16), same
  menu/mean-value/bisection machinery, no exclusion balls (the pentagon
  has |f| = sqrt5 > 1/4).
- A_tube: |u-p| <= 1/16, |f| <= 1/16, (u+p)/2 in [1/8, 3]: the collision
  set {u = p, f = 0} (bodies A+ B+ and A- B- coincide). Part (b): polar
  blow-up (u-p = rho cos phi, f = rho sin phi), rows carrying cs^-3
  rescaled by rho^2, covering over (w, v, phi) x rho in [0, 1/16].
- A_ulow: u in [0, 1/4], p in [1/4, 3], minus the corner tubes
  {u <= 1/16, |v -+ 1| <= 1/16} (A collides with an axis body) and minus
  the A_tube sliver: mA column rescaled by 4u^2 (analytic at u = 0; the
  face matrix has generic rank 4: L13 -> (0,0,h1,0), L15/L25/L35-L36 span
  the rest). Part (c). A_plow: by the pair-swap identity (verified once,
  exactly): no separate run.
- A_uplow (u, p both <= 1/4) and the corner tubes: deferred to part (d);
  the double-collapse corner {u = p -> 0, f -> 0} needs a two-step
  blow-up. Declared pending, not assumed.

Outer part (u > 3 or p > 3 or |v| > 3 or |q| > 3): inverted-coordinate
charts (u = 1/u^, etc.), row/column rescalings chosen so the chart matrix
is analytic on the closed chart including the infinity faces; one covering
per chart; the pair-swap and mirror symmetries fold the chart count.
Deferred to part (e); declared pending.

## Success criteria (declared)

Per covering: zero residual failures at depth cap 44 within a 12 h budget,
checkpointed and resumable; any stubborn cluster is investigated as a
potential rank-degeneracy discovery (the pentagon precedent) and, if
confirmed, gets ball certificates (rank-2 witness + gradient pair). A
budget exhaustion is a recorded FAILURE of that part; no silent extension.

## Order

(a) band first (largest region, no new mathematics), then (b) tube blow-up
(new leading-order derivation, machine-verified before the run), then (c)
ulow + swap identity, then (d) corners, (e) outer charts. Findings mirror
to CAOS_MANAGE as CC-F33+ as they land.

## Addendum (2026-08-20): fa1 resume declaration

The fa1 covering exhausted its declared 12 h budget with 8 boxes left on
the stack (zero depth-cap failures; 59,972 trap certificates made the run
an order of magnitude costlier per box than the band). Per the standing
rule this is recorded as a FAILED run under its original declaration. NEW
declaration: ONE resume from the last checkpoint with a fresh 4 h budget,
same depth cap 44, same success criterion (zero residual failures). If the
resume also exhausts, the remaining boxes are investigated individually
before any further declaration.

## Addendum (2026-08-20b): bicorner-same resume declaration

bicorner-same exhausted its declared 6 h budget with 20 boxes on the
stack (zero depth-cap failures; the widened 7/32 seed and CPU contention
across eight concurrent coverings slowed it). Recorded as FAILED under
the original declaration. NEW declaration: ONE resume from the last
checkpoint, fresh 3 h budget, same depth cap and criteria.
