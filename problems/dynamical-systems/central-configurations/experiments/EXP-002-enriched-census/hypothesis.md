# EXP-002: censuses on the enriched system (F + G + e_IU, + Cayley-Menger for planarity)

Declared: 2026-07-24, BEFORE any run. Route: R1 (calibration ladder). Backlog: CCB-001
follow-up; the corrected questions after EXP-001's P7 refutation (dimension-blindness
of the bare F-system) and P5 cap. Supersedes nothing; EXP-001 stands as recorded.

## Question

On the ENRICHED Albouy-Chenciner system (symmetric F, asymmetric Roberts G, the
energy-inertia relation e_IU; Cayley-Menger adjoined where a dimension is asserted;
forms per the method dossier, from HJ11), do the exact planar censuses come out
classical, and does the enrichment remove the structural pathologies EXP-001 found in
the bare F-system (coordinate-line components; dimension mixing)?

## Setup

Same builders and normalization as EXP-001 (Lambda = -1, cleared polynomial forms over
QQ[m][r], repo .venv, sympy 1.14). Census instrument: the eliminant census of EXP-001
(lex-GB univariate eliminants, CRootOf isolation, exact residual acceptance);
solve_poly_system remains banned. Sample masses: (1,1,1), (1,2,3), (2,3,5), (1,1,2).
Enriched n = 3 system: E3(m) = {f_12, f_13, f_23} + {g_ij, i != j} + {e_IU} (10
polynomials, 3 variables; e_CM vacuous for 3 bodies, realizability = weak triangle
inequality). Rhombus stratum for n = 4 equal masses: substitute
(a, a, a, a, b, b) into F, G, e_IU and adjoin the planar e_CM(a, b).

## Falsifiable predictions

- **P1 (enrichment kills the lines).** For each sample mass vector, the enriched ideal
  E3(m) in QQ[r12, r13, r23] is ZERO-DIMENSIONAL as is (grevlex pure-power criterion),
  WITHOUT any saturation: the G-equations and e_IU cut away the coordinate-hyperplane
  components that made EXP-001's P1 heavy. (Also checked symbolically: the EXP-001
  line {r13 = r23 = 0} does NOT satisfy the enriched system for symbolic masses.)
- **P2 (the full n = 3 census, all samples).** The eliminant census of E3(m) over the
  positive reals finds, for every sample mass vector: the equilateral point (1, 1, 1),
  and exactly 3 collinear points (one per ordering, each satisfying its degenerate
  triangle equality exactly), and these are ALL the realizable positive solutions. Any
  additional positive solutions must be non-realizable (strict triangle-inequality
  violations); their number is recorded. FAILURE: a known CC missing, or a realizable
  positive solution beyond the classical 4 (which would contradict Euler-Lagrange-
  Moulton), or a census breakdown.
- **P3 (the planar rhombus census, corrected P7).** On the equal-mass rhombus stratum
  with e_CM adjoined, the census finds EXACTLY ONE positive solution: the square, with
  b^2 = 2a^2 and a^3 = (4 + sqrt(2))/8 (minpoly 32x^6 - 32x^3 + 7, the EXP-001 value).
  The tetrahedron (a = b = 1) satisfies the enriched F + G + e_IU stratum equations
  but violates e_CM (recorded as the Dziobek sanity check).
- **P4 (invariant baseline, informational; the round's INVARIANT-lens exploration).**
  At every census point we record exact U, I, M and the scale-free invariant
  J = U I^(1/2) / M^(5/2); machine-check the identity U = M I (e_IU) at every accepted
  point. This stage is informational except the identity check, which must PASS at
  every accepted census point (it is an ideal member).

## Success / failure criteria

SUCCESS: P1, P2, P3 pass as machine asserts, P4's identity check passes everywhere.
FAILURE: any assert fails (recorded as refuted; corrected questions become EXP-003).
Caps: any Groebner stage capped at 900 s per sample reports inconclusive-cap honestly.

## Method / environment

run.py staged as EXP-001 (incremental artifacts, subprocess caps), deterministic, CPU
only, exact arithmetic; artifacts tee'd to `artifacts/`.
