# EXP-145 - Verdict: CONFIRMED (2026-11-14). The image of F misses exactly the curve Gamma; the plane C = 0 carries three-point fibers off B^2 = 16A

Hypothesis: [`hypothesis.md`](hypothesis.md) (frozen before any code). Code: [`run.py`](run.py), run from the repository root with the research
venv (sympy 1.14.0), one process, exit 0, 4.9 s of wall time (kill criterion: 600 s per Groebner basis; none came near it).
Artifacts: [`artifacts/results.json`](artifacts/results.json) (every prediction with its bases, quotient dimensions, points, residuals
and times), [`artifacts/run-log.txt`](artifacts/run-log.txt). Tests: `tests/test_jacobian_exp145.py` (3 tests, red before `run.py`
existed, green after). Seed 20261114 for the random targets; all arithmetic is exact over Q (sympy `Rational`), except one
80-digit residual check that is a sanity sample next to the exact identity (see the record below).

## Prediction table

| ID | Statement | Outcome | Evidence |
|---|---|---|---|
| Premise | `det JF = -2`; `disc_w(W) = -16 C^2 Sigma`; on `Gamma(c)`, `W = -4 (w - 1/3)^3`; reconstruction identity | PASS | `run-log.txt` premise block. The identity `F(x(w), y(w), z(w)) = (A, B, C)` holds modulo `W(w)` in `Q(A,B,C)[w]` (exact remainder 0 for all three components), with `s = -W'(w)/m`, `v = 2w/s - 1`, `x = C/s`, `y = v/x`, `z = (q(v) - s)/x^2`. |
| P1 | Reduced lex Groebner basis of `(27c^2 F1 - 4, 3c F2 - 4, F3 - c, cv - 1)` in `Q[x,y,z,c,v]` is `[1]` | PASS | basis printed `[1]`, 0.05 s: no point of `C^3` maps to `Gamma(c)` for any `c != 0`. |
| C1 | With `5/27` for `4/27` the basis is not `[1]` | PASS | 4 basis elements, 0.09 s: the perturbed curve is in the image, so the `[1]` of P1 is not an artifact of the construction. |
| P2(a) | `F(0, y, z) = (z + 4y^2, y, 0)`; `(0, B, A - 4B^2)` maps to `(A, B, 0)` | PASS | symbolic, exact expansion. |
| P2(b) | 40 targets with `C != 0` off `Gamma` (20 random, 10 on `Sigma = 0` from a prescribed double root, 10 within `1e-3` per coordinate of a point of `Gamma`): proper fiber ideal, quotient dimension 1 to 3, a real preimage | PASS 40/40 | Quotient dimension (grevlex staircase): 3 at all 20 random and all 10 near-`Gamma` targets, 1 at all 10 on-`Sigma` targets; equal in every row to the number of simple roots of `W` (`sqf_list`); `Sigma` exactly 0 on the 10 on-`Sigma` targets, off `Gamma` exactly at all 40. A real simple root exists at every target (exact Sturm count `count_roots` of the squarefree simple part, 1 or 3 real simple roots); its reconstruction maps back to the target with relative residual below `1e-75` at 80 digits. |
| P3(a) | `F(x, (Bx-6)/(4x), (26-3Bx)/(4x^2)) = (B^2/16 - 1/(4x^2), B, 0)`, equal to `(A, B, 0)` exactly on `x^2 (B^2 - 16A) = 4` | PASS | symbolic simplification. |
| P3(b) | 20 targets `(A, B, 0)`, `B^2 != 16A`: dimension 3, three distinct points (radical); 5 targets `B^2 = 16A`: dimension 1 | PASS 25/25 | Dimension 3 (resp. 1) at every target; the three points (flat sheet and the two with `x = +-2/sqrt(B^2 - 16A)`) are substituted exactly into `F` and equal the target, with distinct `x`; radicality by a second route: the `x`-eliminant of the lex basis (order `z > y > x`) is squarefree of degree 3 (resp. 1). The 20 targets include `(0, 1)` and `(-1/4, 0)` (rational square `B^2 - 16A`) and 18 others, of which 8 have `B^2 - 16A < 0` (non-real points). |
| P3(c) | Fiber over `(0, 1, 0)` is `{(0,1,-4), (2,-1/2,5/4), (-2,1,2)}`; over `(-1/4, 0, 0)` the three announced points | PASS | solved from the lex Groebner basis, dimension 3 each, all three points mapped back exactly. |
| C2 | EXP-007 item 4 targets, read from its artifact, have three complex points, exactly one rational | PASS | Targets `(3/5, -2/7, 0)` and `(5, 1/3, 0)` parsed from `EXP-007/artifacts/output-2026-07-20.txt`; `B^2 - 16A = -2332/245` and `-719/9`, neither a rational square, so the two extra points (`x^2 = 4/(B^2 - 16A)`) are not rational; the one rational point is the recorded flat-sheet point `(0, -2/7, 67/245)` resp. `(0, 1/3, 41/9)`; dimension 3 each. |

## What this establishes

- **The image.** `F` is not surjective over `C` nor over `R`: no point maps to `Gamma(c) = (4/(27c^2), 4/(3c), c)`, `c != 0` (P1, exact).
  Every other target has a preimage: over `C = 0` by the flat sheet (P2(a), symbolic); over `C != 0` off `Gamma`, `W` has degree 3
  and is not a triple root, so it has a simple root, `s = -W'(w)/m != 0` there, and the reconstruction identity (exact, above)
  produces a preimage. That last step is the paper's argument, certified here in its two ingredients (the reconstruction
  identity and the triple-root locus `W = -4(w - 1/3)^3` exactly on `Gamma`), and sampled at 40 targets (P2(b)); it is not a
  separate exhaustive computation over all targets.
- **The plane `C = 0`.** Three-point fibers off `B^2 = 16A`, the flat-sheet point only on `B^2 = 16A` (P3). Real: three real points
  iff `B^2 - 16A > 0`, one real point otherwise (from `x^2 = 4/(B^2 - 16A)`).

## Statements superseded (EXP-007 and EXP-011 are not edited)

- [EXP-011 verdict](../EXP-011-real-fiber-census/verdict.md), item 4 ("`F|_{R^3}` is a surjective, orientation-reversing, non-proper,
  non-injective real Keller map"): restated as not surjective, over `R` as over `C`; the image is the complement of `Gamma`.
  Orientation-reversing (`det = -2`), non-proper and non-injective stand.
- EXP-011 verdict item 3 ("Real surjectivity (grid-certified)", with "structurally [D]: ... a real root always exists, and off the
  wall all roots are simple"): the structural argument misses the triple root, which is a real root of multiplicity 3 with no
  simple root; the grid of 36 targets never meets `Gamma`, so it could not see the gap. Restated: every real target off `Gamma` has
  a real preimage.
- [EXP-007 verdict](../EXP-007-asymptotic-variety/verdict.md), item 4 ("The plane `C = 0` is asymptotic with a flat-sheet remainder.
  Over generic `(A, B, 0)` the exact fiber is exactly one point ... both curved sheets escape"): restated as three points over
  generic `(A, B, 0)` (the flat-sheet point and two with `x^2 (B^2 - 16A) = 4`), one point only on `B^2 = 16A`. The recorded single
  point is the one rational point (C2): the `fiber_points` filter of EXP-007 `run.py` kept `is_rational` solutions only.
  The plane `C = 0` is therefore not asymptotic away from `B^2 = 16A`; the asymptotic variety there is the line `{C = 0, B^2 = 16A}`
  (limits of the points with `x = 2/sqrt(B^2 - 16A) -> infinity`).
- EXP-007 items 1 to 3 and 5 (discriminant characterization, the escape at `(0, 1, 1)`, collisions off the variety) are not contested;
  the premise block re-checks `D = -16 C^2 Sigma` and the reconstruction.

## Consequence for the foundational paper

Theorem on the fibers over `C = 0` (three points off `B^2 = 16A`) and the real census and image theorem (image the complement of
`Gamma`, `F` not surjective over `C` or `R`) can carry machine-verified marks, with EXP-145 as the source: P3 and C2 for the plane,
P1 and C1 for the missing curve, P2(b) for the samples. The paragraph that an enumeration of rational solutions sees one point
is explained by C2. The statement that `Gamma` is the whole complement of the image over `C != 0` remains the paper's derivation
with samples, as stated above.

## Adversarial validation record

- Route 1 (symbolic identities): P2(a), P3(a), the reconstruction identity and the triple-root factorization are polynomial or
  rational-function identities, not samples.
- Route 2 (control): C1 changes one coefficient (`4/27 -> 5/27`) and the basis stops being `[1]`; the
  4 basis elements, so the unit ideal at `4/27` is a property of `Gamma`.
- Route 3 (two independent routes): the quotient dimension from the Groebner staircase equals the number of simple roots of `W` at
  all 40 P2(b) targets; the radicality at the C = 0 targets is checked by distinct exact points and by a squarefree eliminant.
- Route 4 (adversarial targets): 10 targets within `1e-3` of `Gamma` (where the three roots of `W` nearly coincide and `x = C/s`
  is large) and 10 on `Sigma = 0`; every one has the predicted dimension and a real preimage.
- Route 5 (reading the prior record): C2 reads the EXP-007 targets from its stored output rather than retyping them.

## How could this be wrong?

- The hypothesis checks P1 only for `c != 0` inverted; the curve `Gamma` has no point at `c = 0`, so nothing is missed, but a target
  with `C = 0` is covered by P2(a) alone.
- P2(b) is 40 samples; the claim for all `C != 0` targets off `Gamma` rests on the simple-root argument plus the exact
  reconstruction identity, which has one gap a reader could press: the identity is checked as a remainder modulo `W` over the
  fraction field `Q(A, B, C)`, so at a target where a denominator of the reconstruction vanishes (`s = 0`, a multiple root) it says
  nothing, which is exactly why multiple roots are excluded and why the on-`Sigma` samples keep only the simple root.
- The residual check at 80 digits is numerical; the exact statement is the identity. A faulty `real_roots` would be caught by the exact
  `count_roots` (Sturm) comparison only at the count level.
- The `C2` reading is of one artifact (two targets) and of the filter in EXP-007's `run.py`; a different, unrecorded explanation of the
  "one point" would not be excluded by this experiment, only shown unnecessary.
- sympy's Groebner and `solve` are trusted; the three-point fibers are cross-checked by exact substitution into `F`, which does not
  depend on them.
