# EXP-051 - Verdict: CONFIRMED; THE HALF-PLANE TOWER LEMMA stands; frontier shapes fall at all degrees (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`.

## THE HALF-PLANE TOWER LEMMA ([MV/D])

Let P = x + R whose total-degree top form T attains mu = min{p - q over supp(P)} (the
swallowed-staircase geometry: the top corner is the y-most support point), and let
H = {rows (i, j) : i <= j}. If the H-restricted window system has a left-null covector
with nonzero pairing at ONE window N >= deg P - 1, then P is not a Keller component at
ANY partner degree. Proof ingredients, machine-verified: (a) T-power resonances reduce
in-window (the universal reduction) and Lambda_H kills H-parts of in-window images by
definition; (b) non-T-power kernel resonances have x-heavy sources with EMPTY H-part;
(c) columns whose T-output leaves H are entirely zero in M_H (T attains mu, so its
output minimizes i - j among the column's outputs): zero case-c violations measured on
both test shapes at full column sweeps.

## Findings

1. **[MV]** H-certificates exist at (2,2,2) at EVERY window 7..10 with monomial
   pairings over QQ(a, b) (-32 a^4, -64 a^4, -64 a^5, -512 a^5): the H-tower is real
   and all-parameter sound.
2. **[MV]** Case-c vacuity and mu-attainment verified on (2,2,2) and P32.
3. **THE FRONTIER PAYOFF [MV].** P32 = x + R0(1)^2 + x^2 (degree 32, B = 16 flavor,
   proper-power top x^8 y^24) has an H-certificate at N = 14 (380 H-rows, pairing
   -256), and P72 = x + 2 (x^2 y^7)^8 + x^2 (degree 72, the (72, 108) corner geometry)
   has one at N = 12 (135 H-rows, pairing -32): by the lemma, BOTH ARE EXCLUDED AT ALL
   PARTNER DEGREES: the first all-degree exclusions on frontier-shaped polynomials.

## Consequences

- Theorem 5's proper-power case CLOSES on the mu-attaining stratum: Theorems 5 and 6
  plus this lemma now cover every swallowed-staircase shape whose top corner is its
  y-most support point, at all degrees, from one window solve each.
- The frontier program upgrades from window certificates to ALL-DEGREE exclusions per
  sampled shape; the GGHV (72, 108) parametrized sweep (transcription in flight) can
  now aim directly at all-degree closure.

## How could this be wrong?

- The lemma's scope requires T to attain mu (y-most top corner); shapes with y-heavier
  non-top monomials fall outside and keep Theorem 6 or full-window towers.
- Frontier pairings are parameter-free constants because the samples were numeric; the
  parametrized sweep should re-derive them with symbolic coefficients.
