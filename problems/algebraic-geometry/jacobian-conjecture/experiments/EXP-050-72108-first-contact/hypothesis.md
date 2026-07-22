# EXP-050 - First contact at the (72, 108) degrees (route N2)

- **Question.** JCB-040. The lone surviving degree pair below 125 is (72, 108) (GGHV
  2204.14178, left open for compute). Can the filtered pipeline produce the first
  certificates AT those degrees?
- **Motivation.** The GGHV case has (A0, (m, n)) = ((8, 28), (3, 2)): the P-side polygon
  corner sits at 2 (8, 28) = (16, 56) (degree 72). Sampled shapes with that corner and a
  swallowed linear vertex are the honest first-contact objects; the similarity filter
  (ratio 108/72 = 3/2; nested for all partner degrees <= 108) makes the full window
  affordable. These are SAMPLES, not the GGHV parametrized variety (whose full shape
  data needs the primary text; queued): the value is the first machine exclusions at the
  open pair's degrees plus the measured cost.
- **Falsifiable predictions.**
  1. [MV] Sampled degree-72 shapes with corner (16, 56) (g = x^2 y^7: P = x + a g^8 +
     x^2, and a two-term-top variant) have EMPTY filtered windows at N = 108: no Keller
     partner of ANY degree <= 108 exists for these samples.
  2. [D] Cost recorded; feasibility verdict for the systematic sweep once the GGHV
     shape data is transcribed.
- **Method.** sympy over QQ; the hull filter; caps 570 s per sample (degrade the window
  to 90 or 72 before capping out; record any degradation).
- **Success criterion.** 1 verified with timings; the first certificates at the open
  pair's degrees are on record.
- **Failure criterion.** A consistent filtered window (escalate hard: adjudicate
  unfiltered before any claim; a genuine completion at these degrees would be a
  candidate counterexample to JC(2)).

Declared 2026-07-22 before the run.
