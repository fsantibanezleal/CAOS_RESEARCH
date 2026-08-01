# EXP-010 - Dziobek-variety dimension calibration at n = 4 (the incidence-dimension lane opens)

Declared: 2026-08-01, BEFORE any run. Backlog: CCB-033 (approaches-evaluation view V1).
Round context: EXP-009 double-capped the direct n = 4 torus census; this experiment
opens the valuation-free route whose unit of progress is a DIMENSION, not a
solution list.

## Question

Can randomized linear-section dimension probes, with every algebraic call kept
zero-dimensional by construction, certify the dimension of the n = 4 Dziobek
variety, agreeing with the value that Moeckel's generic-finiteness picture
predicts, and cheaply enough that the same instrument has a credible path to
n = 5 (spatial Dziobek) and then to the mass-parametric n = 6 incidence ideal?

## The object

Work in the 6 mutual-distance coordinates r_ij on the torus (all r_ij invertible,
enforced by the Rabinowitsch equation t * prod r_ij - 1 = 0). The DZIOBEK VARIETY
D4 is cut out by:

- the cleared Dziobek differences h_ab, h_bc, h_ac (cclib.dziobek4; HM06 Section
  2.2 eq. (12): S_12 S_34 = S_13 S_24 = S_14 S_23 with S_ij = r_ij^-3 - 1; two are
  independent on the torus, all three kept for manifest S_4 symmetry, monomial
  factors stripped as in EXP-008),
- the planar Cayley-Menger determinant (cclib.cayley_menger_planar4; zero iff the
  four points embed in the plane).

Masses do NOT appear: for planar noncollinear configurations the Dziobek products
characterize central configurations with the masses recovered from the geometry
(HM06, after Dziobek). This is the mass-free avatar of the incidence variety, and
that is exactly why the lane's first calibration lives here: the dimension of D4
should equal the dimension of the (projectivized) mass space, dim = 3, if the
mass-recovery map is generically finite, which is the content of the generic
Dziobek finiteness picture (Moeckel 2001, tag [Vs]; used as INTERPRETATION, not as
a premise of any prediction).

Consistency cross-check available in-house: EXP-001 proved the bare AC system is
dimension-blind (the unit tetrahedron passes it), and here the tetrahedron
r_ij = 1 satisfies all three Dziobek equations trivially (every S_ij = 0) but is
EXCLUDED by the Cayley-Menger equation, which is nonzero on it. The smoke test
checks both memberships explicitly.

## Instrument

Random affine-linear sections L_k = c_0 + sum c_ij r_ij with integer coefficients
drawn uniformly from [-10^6, 10^6] by random.Random(20260801) (seed fixed here,
draws recorded verbatim in the artifacts). The sectioned systems
{h_ab, h_bc, h_ac, CM, t-saturation} + {L_1..L_d} go to msolve (0.10.1, WSL,
hashes on record) which is asked for the full zero-dimensional census; sympy
performs the exact residual verification of any rational data used downstream.

Epistemic status, stated up front: a specific section is generic only with high
probability. Emptiness or finiteness at recorded random sections is
PROBABILISTIC-EXACT evidence (exact arithmetic at the drawn parameters; the bad
locus of section parameters is contained in a hypersurface whose degree is
bounded by the degree data this same experiment measures, so the failure
probability is bounded explicitly a posteriori and recorded in the verdict). The
DETERMINISTIC rung is P3: a grevlex Groebner staircase dimension of the
unsectioned ideal under its own cap. If P3 completes, P1/P2 become its
cross-checks; if P3 caps, P1/P2 carry the (probabilistic) result. This division
is the point of the calibration: at n = 5 and 6 only the sections will scale, so
their reliability must be measured here, where the deterministic answer is still
reachable.

## Predictions

- P1 (dimension from below + degree data): for TWO independent 3-section draws,
  the sectioned system is zero-dimensional and NONEMPTY over C; msolve returns
  the census within 900 s per draw. Recorded output: the complex count (the
  section degree) per draw.
- P2 (dimension from above): for TWO independent 4-section draws, the sectioned
  system is EMPTY; msolve returns [] within 900 s per draw.
- P3 (deterministic rung): the Krull dimension of the unsectioned stripped ideal
  is 3 in QQ[r, t]. The Rabinowitsch variable is fixed by
  t * prod(r_ij) - 1 and therefore adds one variable and one equation, not one
  dimension. The computation has an 1800 s sympy cap. Inconclusive-cap is an
  admissible outcome that leaves P1/P2 carrying the claim.
- P4 (internal consistency = degree well-defined): the complex counts of the two
  P1 draws AGREE. Two generic sections of the same variety see the same degree;
  disagreement would prove at least one draw non-generic (or a bug) and would
  invalidate the instrument at this size.

## Preflight (methodology/12)

- Source-complete: HM06 eq. (12) read directly (2026-07-24 dossier); dziobek4 and
  cayley_menger_planar4 implemented and already machine-exercised (EXP-001 smoke,
  EXP-008 tropical activity). Moeckel 2001 is interpretation only.
- Smoke test (before any solver time): (a) the exact equal-mass square
  (side minpoly 32x^6 - 32x^3 + 7, EXP-001) satisfies h_ab, h_bc, h_ac and CM
  exactly; (b) the unit tetrahedron satisfies the h's but NOT CM; (c) the
  nonsquare 3-by-4 rectangle has rational mutual distances 3, 4, and 5,
  satisfies CM exactly, and does NOT satisfy all h's. Three-way
  discrimination, sympy exact, expected under 60 s.
- Premise dependencies: none of P1-P4 depends on an [U]-tagged claim; all are
  machine-decidable statements about our own systems.
- One-sidedness check: every rung can refute. A nonempty 4-section refutes
  dim <= 3 (probabilistically) and would contradict the Moeckel picture, which
  would be major either way; empty 3-sections would refute dim >= 3; caps refute
  the ENGINE VIABILITY of the lane at its cheapest instance, which is precisely
  what EXP-009 taught us to test first.
- Invariant-first: the monotone invariant of the lane is the section census count
  (the degree); it is recorded per draw and will be the cost predictor for n = 5.
- Budget and kill criterion: worst case about 5400 s total (4 x 900 msolve +
  1800 sympy + smoke). Any capped call is recorded inconclusive-cap; if BOTH P1
  draws cap, the lane's msolve assumption is REFUTED at n = 4 and the verdict
  promotes CCB-034 (witness sets, Julia) instead; no cap extensions inside this
  experiment.

## Consequence ladder

- PASS (P1, P2, P4, with or without P3): the lane is calibrated; EXP-011 is the
  n = 5 SPATIAL Dziobek variety (Moeckel's theorem covers Dziobek configurations
  for every n; expected dim = 4), which would cross-validate the Hampton-Jensen
  tropical spatial-5-body result by a completely independent method; only after
  that does the mass-parametric n = 6 incidence ideal get any spend.
- ENGINE REFUTED (caps): CCB-034 promotion; the msolve version of the lane is
  closed at n = 4 and the record says so.
- DIMENSION SURPRISE (any of P1/P2/P4 fails algebraically rather than by cap):
  stop, verify exactly, and treat as a finding about D4's component structure
  (excess components would themselves be publishable data); nothing propagates
  to n = 5 until understood.
