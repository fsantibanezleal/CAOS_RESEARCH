# The k = 2, p = 2 stratum: exact quotient derivation (CCB-036 stage 3 opens)

Written 2026-08-01. Companion script:
`experiments/EXP-015-stratum22-shape-dimension/derive_quotient.py` (exact
sympy; every fact below marked VERIFIED was printed as an exact zero by the
interactive derivation this afternoon; the script re-verifies all of them and
adds two enumerations whose output is appended when its background run
completes).

## 0. Novelty pass (recorded)

A targeted search today (six-body, two pairs, symmetric, finiteness) surfaced
existence and enumeration studies (nested equilateral triangles; the JMP 2022
six-body paper; Euler-plus-two at five bodies) but NO generic-finiteness
closure for this stratum. One search-summary claim of "at most 86 zw-diagrams"
was NOT imported (summary-level, unverified; our 117/24 stays as read from the
Chang-Chen primary source). The stratum stands open as far as we can verify.

## 1. Coordinates and the nine quotient distances

Bodies 1, 2 ON the reflection axis at (0, a1), (0, a2); pair A = bodies 3, 4
at (u, v), (-u, v); pair B = bodies 5, 6 at (p, q), (-p, q); u, p > 0 on the
open stratum (non-collision), reflection = x-negation.

VERIFIED distance identities: r13 = r14, r15 = r16, r23 = r24, r25 = r26,
r35 = r46 (same-side), r36 = r45 (cross-side). The nine quotient variables:

    r12; d1A = r13, d1B = r15, d2A = r23, d2B = r25;
    wA = r34 = 2u, wB = r56 = 2p; c_s = r35, c_x = r36.

## 2. The first shape equation is LINEAR in the squares (VERIFIED)

    c_x^2 - c_s^2 = wA * wB        (exactly; from (u+p)^2 - (u-p)^2 = 4up)

The remaining shape relations follow the Dias-Pan (2.2) pattern via
r-expressible squared height differences: (a_i - v)^2 = d_iA^2 - wA^2/4,
(a_i - q)^2 = d_iB^2 - wB^2/4, (v - q)^2 = c_s^2 - (wA - wB)^2/4, and the
chain-square identities that force consistency of the differences
(a1 - a2 = +-r12; (a_i - v) - (a_i - q) = q... sign cases squared away),
each yielding one polynomial equation in the nine r's. The exact inventory
(with degrees) is fixed in the EXP-015 hypothesis; all are quadratic or
quartic and SPARSE, unlike the 130-term spatial Cayley-Menger, which by the
twice-measured cost law (EXP-013/014) stays out of any Groebner core here.

## 3. The pair-equality lemma (VERIFIED closed forms)

With all six masses free, the Laura-Andoyer equations of the two pairs
evaluate EXACTLY to

    L34 = -2u (m5 - m6)(q - v) (c_x^3 - c_s^3) / (c_s^3 c_x^3),
    L56 = +2p (m3 - m4)(q - v) (c_x^3 - c_s^3) / (c_s^3 c_x^3).

Consequences, stated with their exact hypotheses:

- On the open stratum with q != v (pairs at different heights): c_x != c_s
  (since c_x^2 - c_s^2 = wA wB > 0), u, p != 0, so L34 = 0 forces m5 = m6 and
  L56 = 0 forces m3 = m4. The Dias-Pan Prop 3.1 analogue holds.
- On the q = v SUB-STRATUM (both pairs at the same height, a co-linear-pairs
  geometry) these two equations vanish identically and force NOTHING: the
  pair-equality lemma does NOT follow from L34/L56 there. The derivation
  script probes which other L_ij carry antisymmetric mass dependence at
  q = v; until that lands, the campaign scope is declared as the q != v open
  stratum, with q = v flagged as a separately-handled boundary case. This
  precision is a genuine structural difference from the cross stratum and
  must survive into any statement wording.

## 4. Mass space and the target arithmetic

After pair equality (on the declared scope): masses (m1, m2, mA, mB),
projectivized dimension 3. The Dias-Pan pipeline target: show the stratum's
incidence variety has dimension <= 3 + 0 over generic masses via (i) the
shape variety dimension (EXP-015's rung; the configuration count is 6
coordinates - 1 translation gauge = 5, so the UNGAUGED shape variety in the
nine r's is expected to have dimension 5, dropping to 4 with a Dias-Pan-style
scale gauge), (ii) the mass-linear Jacobian rank off determinantal loci
(their (7.1) pattern; our reduced Laura-Andoyer block is mass-linear by
construction), (iii) an explicit witness with exact rank (our census
machinery; candidate witness geometry: equal axis masses with the two pairs
forming a rectangle-plus-axis configuration, to be fixed after the reduced
block lands).

## 5. Honesty

- Everything marked VERIFIED printed as an exact zero in sympy today; the
  enumerations (q = v probe; reduced block inventory) are PENDING the
  background derivation run and are not assumed anywhere above.
- The stratum's openness rests on today's recorded searches; the mandatory
  novelty pass is section 0, and a MathSciNet/zbMATH pass has NOT been done.
- No experiment run has started; EXP-015 is declared separately with its own
  preflight, after the derivation output is in.
