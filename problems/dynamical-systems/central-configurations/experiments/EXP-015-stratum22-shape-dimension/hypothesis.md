# EXP-015 - The k = 2, p = 2 stratum: shape-variety dimension (Dias-Pan pipeline, stage i)

Declared: 2026-08-01, BEFORE any run. Campaign: CCB-036 stage 3 (dossier
2026-08-01-stratum22-quotient-derivation.md; pair-equality lemma and reduced
block already exact).

## The object

The SHAPE variety of the stratum: all nine-tuples of quotient distances
(r12, d1A, d1B, d2A, d2B, wA, wB, c_s, c_x) realizable by the symmetric
geometry (two bodies on the axis, two mirror pairs), cut in the distance
torus by the polynomial consequences of the coordinate parametrization:

- E1 = c_x^2 - c_s^2 - wA*wB (VERIFIED exact in the dossier);
- with A_i = d_iA^2 - wA^2/4, B_i = d_iB^2 - wB^2/4, H = c_s^2 -
  (wA - wB)^2/4 (the squared height differences, all r-expressible), the
  chain-square consistency equations
  E2 = (A1 + A2 - r12^2)^2 - 4*A1*A2,
  E3 = (A1 + H - B1)^2 - 4*A1*H,
  E4 = (A2 + H - B2)^2 - 4*A2*H,
  E5 = (B1 + B2 - r12^2)^2 - 4*B1*B2 (possibly dependent; kept),
- the Rabinowitsch saturation t * prod(all nine r) - 1.

HONESTY: squaring the sign chains introduces ghost branches (sign-mismatched
"configurations"); the cut is an OVERVARIETY of the true shape locus, so a
dimension UPPER bound on the cut bounds the true shape variety too, and the
expected dimension count (6 coordinates minus 1 translation gauge = 5) is a
prediction about the top of the cut.

## Predictions

- P1 (cost, per the twice-measured law): Singular over QQ completes std of
  {E1..E5, sat} in the 10 variables within 300 s (five sparse equations of
  degree at most 8 in r, no 130-term monsters).
- P2 (dimension): the staircase dimension, read two ways (our independent-set
  computation and Singular's dim()) with agreement REQUIRED, equals 5.
- P3 (the gauged variant): adjoining the scale gauge r12 - 1 drops the
  dimension to exactly 4 (the Dias-Pan analogue: their gauged shape variety E
  had dim 4 for the cross stratum).
- Branches declared: dim above 5 (or gauged above 4) = ghost branches
  dominate, redirect to a sign-stratified cut; below = the parametrization
  count is wrong somewhere and the derivation gets audited; caps = the cost
  law failed on quadratic-quartic systems, which would be genuinely
  surprising and recorded as such.

## Preflight (methodology/12)

- Source-complete: the equations come from today's exact derivation (each
  squared-difference identity is elementary algebra over the verified
  coordinate parametrization); the engine pipeline is EXP-012-validated.
- Smoke (in-run, before Singular): an exact rational WITNESS configuration
  (a1, a2, u, v, p, q) = (3, -1, 2, 1, 1, -2) is substituted into E1..E5 via
  the r^2 values (all E's are polynomials in the SQUARES, so the smoke is
  pure rational arithmetic); all five must vanish exactly. A perturbed
  non-realizable 9-tuple must violate at least one.
- One-sidedness: every branch can refute (P2/P3 values are sharp).
- Invariant-first: the dimension pair (ungauged, gauged) and the wall time.
- Budget and kill: two Singular runs at 300 s each plus the rational smoke;
  no extensions.

## Consequence ladder

- P2 = 5 and P3 = 4: stage (i) of the Dias-Pan pipeline is done for this
  stratum; stage (ii) (the mass-linear 4 x 6 Jacobian rank analysis of the
  reduced block {L13, L15, L23, L25, L35, L36} off determinantal loci) is
  declared next, then the witness eliminant.
- Ghost-dominated or capped: sign-stratify (replace chain squares by the
  case-split linear-in-square relations on the physical branch) and redeclare.
