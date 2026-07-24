# EXP-001 verdict (2026-07-24)

Hypothesis: `hypothesis.md` (declared and committed 2026-07-23, before any run, commit
13c1a81). Runner: `run.py` (staged, per-stage caps; final form committed before the
recorded run). Artifacts: `artifacts/` (results.json, run-log.txt, per-stage JSON, the
saturated equal-mass Groebner basis, the n = 4 system dump, the symbolic Euler
eliminant). Recorded run: 2026-07-23 23:03:01 to 2026-07-24 00:34:31 (5490 s), sympy
1.14, Python 3.13, CPU only, deterministic.

## Verdict: confirmed in part, REFUTED in part (P7 uniqueness), inconclusive at caps

| Prediction | Outcome | Machine result |
|---|---|---|
| P1 zero-dim (saturated), (1,1,1) | CONFIRMED | product-Rabinowitsch grevlex GB (37 elements, 428 s) satisfies the pure-power criterion in all 4 variables |
| P1, (1,2,3), (2,3,5), (1,1,2) | INCONCLUSIVE (cap) | saturation Groebner exceeded the 900 s per-sample cap |
| P2 Lagrange point, symbolic masses | CONFIRMED | r = (1,1,1) annihilates all three cleared AC polynomials identically in m1, m2, m3 |
| P3 Euler-Moulton counts | CONFIRMED | EXACTLY ONE positive collinear solution per ordering, for all 4 sample mass vectors (12 chart censuses, eliminant method); equal masses: r12 = r23 = 90^(1/3)/6 on the 2-middle chart |
| P4 symbolic Euler eliminant | CONFIRMED (descriptive) | nonzero eliminant of degree 54 in r23 over QQ(m1,m2,m3), computed in 4 s; factored form persisted (p4-euler-eliminant.txt) |
| P5 equal-mass full torus census | INCONCLUSIVE (cap) | the t-elimination + census on the saturated basis exceeded the 1800 s cap |
| P6 n = 4 assembly | CONFIRMED | 7 nonzero polynomials in 6 distance variables; each AC f: 14 monomials, total degree 15, support affine dim 5; e_CM: 22 monomials, degree 6, support dim 5 |
| P7 unique positive in the rhombus stratum | **REFUTED** | TWO positive torus solutions: the SQUARE (b^2 = 2a^2 exactly, Cayley-Menger = 0, a = CRootOf(32x^6 - 32x^3 + 7, index 1), i.e. a^3 = (4 + sqrt(2))/8) and the REGULAR TETRAHEDRON (a = b = 1, Cayley-Menger = 4 != 0) |
| P7 square-shape sub-claim | CONFIRMED | the square is present, exactly; it is the UNIQUE positive solution with CM = 0 (planar) in the stratum |
| P7 Cayley-Menger at the square | CONFIRMED | exact zero |
| (standing fact) | recorded | the line {r13 = r23 = 0} lies in V(F) for ALL masses (symbolic check): the bare symmetric AC ideal is never 0-dimensional before saturation |

## What the refutation teaches (the load-bearing finding)

The hypothesis predicted a UNIQUE positive solution in the equal-mass rhombus stratum
(a, a, a, a, b, b) and it is FALSE: the Albouy-Chenciner distance system knows nothing
about the ambient dimension, so the REGULAR TETRAHEDRON (a Dziobek CC of dimension
n - 1 = 3, all distances 1 under Lambda = -1) legitimately coexists with the square.
Dimension is selected only when the Cayley-Menger equation is adjoined: with e_CM = 0
added, the machine count in the stratum is exactly one (the square). Consequence for
the program: every planar statement must carry e_CM (and, per HJ11, the asymmetric
G-equations and e_IU) from the start; the bare symmetric F-system is the WRONG object
for planar censuses. This is precisely why HM06/HJ11 work with enriched systems; our
calibration now owns that fact by machine rather than by citation.

Corrected normalization record: the hypothesis' informational hand value a^3 =
(4 + sqrt(2))/2 was wrong by the mass factor (Lambda = -1 corresponds to lambda = M,
here M = 4); the machine value is a^3 = (4 + sqrt(2))/8, minimal polynomial
32x^6 - 32x^3 + 7. The goalposts were not moved: the binding sub-claims (b^2 = 2a^2,
CM = 0) were declared machine-decidable and passed; the uniqueness claim failed and is
recorded as refuted.

## Adversarial-validation record (methodology/03)

- Route 1 (independent re-derivation): the P7 square value was derived by hand from the
  Cartesian force balance (giving the (4 + sqrt(2))/8 correction) and independently by
  the eliminant census; the two agree exactly. P3's equal-mass chart solution
  (90^(1/3)/6) satisfies the chart equations by exact residual.
- Certificates persisted: every accepted census point passed an exact residual test
  (`equals(0) is True` on every defining polynomial); eliminants are elements of the
  ideal by construction (lex Groebner elimination), so candidate completeness is
  structural, not numeric.
- Cross-implementation guard (found a real bug): sympy's `solve_poly_system` silently
  returned an INCOMPLETE solution list on these systems (it missed the square, whose
  b-eliminant factor 4b^6 - 4b^3 - 7 is even radical-solvable; and it returned zero
  positive collinear solutions for unequal masses). Detected by hand-substitution of
  the known square into the torus cores; the runner was rebuilt on the eliminant census
  and `solve_poly_system` is BANNED from verdict-bearing counts in this program.
- Second engineering bug caught: `is_positive` returns None on nested RootOf
  expressions; a naive truthiness filter silently drops genuine solutions. Replaced by
  an exact-backed sign decision plus exact residual acceptance.
- Process note: a first monolithic runner was aborted after ~78 min CPU inside the
  uncapped P1 saturation; the recorded run uses the staged runner with caps and
  incremental artifacts.

## How could this be wrong?

- P1 is confirmed ONLY for equal masses; the three unequal samples are open at cap.
  The pure-power criterion itself is standard and was applied to the full 4-variable
  saturated basis; the risk of a false "pass" is limited to an implementation error in
  the leading-monomial extraction, mitigated by the criterion failing (as expected) on
  the unsaturated ideal.
- The census acceptance relies on sympy's `equals(0)` deciding True on algebraic
  numbers; a silent False-negative would UNDERCOUNT. Mitigation: every expected known
  solution (Euler per ordering, square, tetrahedron) was found; an undercount would
  have surfaced as a missing known point. An overcount is impossible without a false
  True from `equals`, which sympy only returns on a proved zero.
- P3 counts positive solutions per COLLINEAR CHART of the bare F-system; the P7 lesson
  (bare F sees higher-dimensional strata) does not affect n = 3 charts (3 bodies admit
  no dimension above 2, and the chart substitution enforces collinearity), but the
  planar-vs-realizable distinction for the FULL n = 3 census (P5) remains undecided at
  cap.
- The degree-54 symbolic eliminant (P4) is recorded, not yet matched factor-by-factor
  against the classical Euler quintic; that comparison is queued (it requires selecting
  the physical factor and dehomogenizing masses), so P4 carries no classical-agreement
  claim yet.

## Consequences for the strategy

1. Enriched system as default (F + G + e_CM + e_IU, Dziobek where applicable) for
   every planar statement; the method dossier already transcribes the forms.
2. The saturation instrument needs an upgrade before P1/P5-class claims at unequal
   masses: staged/sequential saturation, better orderings, modular preprocessing, or a
   wrapped external GB engine (decision at EXP-002 planning; backlog CCB-007 widened).
3. The eliminant census + exact-residual acceptance is the program's counting
   instrument; regression-gate it on this experiment's exact points (square,
   tetrahedron, Euler solutions) in CI.
4. EXP-002 candidates: (a) re-pose the planar rhombus/n = 3 censuses on the enriched
   system (the corrected question after P7's refutation); (b) HM06 direct read
   (CCB-002) before the n = 4 census rung.
