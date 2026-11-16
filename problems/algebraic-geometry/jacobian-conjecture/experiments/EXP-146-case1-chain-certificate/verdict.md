# EXP-146 verdict: CONFIRMED (both Case 1 branch ideals are certified as the unit ideal)

Date: 2026-11-15. Hypothesis frozen at 8133b594 (not edited). CPU only; python-flint 0.9.0 exact arithmetic, numpy int64
Hungarian, Singular 4.3.2 (WSL) as the second implementation. `run.py` exits 0; `artifacts/results.json` carries the
verdict word and every measured value. Production run: 1,490 s in all, of which about 1,250 s are G4's four branch
controls killed at their 300 s wall limit; the two trees took 95 s and 70 s; replay and Singular under 30 s.

## Result

Both branch ideals I_+ and I_- of EXP-142 (q1 = +c and q1 = -c over L = Q[y]/(P)) are certified by the same
three-leaf tree of resultant chains, at (p1, r1) = (536870909, 505390653), every degree used in a resultant proven by
M4, with nonzero final constants. With EXP-142's exact reduction this closes Case 1 of GGHV Proposition 4.3 at
(72,108) as encoded by the 13 compatibility equations: no solution over the algebraic closure of Q. Nothing beyond
Case 1 is claimed. JCB-103 is closed by this verdict.

## Prediction table

| Prediction (hypothesis.md) | Outcome | Evidence |
|---|---|---|
| Both branches certified at (p1, r1) by the three-leaf tree of the probe (HIGH plus, MODERATE minus) | CONFIRMED on both | `artifacts/results.json` branches.plus.nodes, branches.minus.nodes; tree below |
| Every leaf nonzero again at (p2, r2) = (536870879, 12005842) | CONFIRMED | results.json replay: 3 of 3 leaves per branch certified, no problems; nonzero constants 2 of 2, 3 of 4, 6 of 6 |
| Singular's images equal python-flint's at every step | CONFIRMED | `artifacts/singular-check.txt`: 130 member digests and 18 constants compared per branch, 0 mismatches, 0 flags (0 sign flips: both resultants use the same sign convention) |
| The first two chain levels from exact supports replace the probe's image supports | DONE | 118 exact levels (G2 real, G5) over the 10 nodes; the fallback of an exact level 3 was never needed |

## The tree (identical shape on both branches)

Elimination order q5, q3, q4, q2, q0 at the root. Degrees are formal degrees, equal to the image degrees at every
pivot (the attained-bound rule). Constants: nonzero final images over the pairs (V_i, V_pivot).

| Node | Order (last variable) | Pivots (variable, member, degree) | Univariates (degree after division by w^L) | Nonzero constants | Outcome |
|---|---|---|---|---|---|
| t (root) | q5 q3 q4 q2 q0 | q5: E3, 1; q3: l1.0, 2; q4: l1.2, 2; q2: l3.0, 14 | 3 of degree 688 in q0, L = 0 | 0 of 2 | split on E3's q5 leading coefficient alpha + beta q0 (w1); gcd of the images (q0 - root)^212 |
| t.nz (w1 != 0) | q5 q3 q4 q2 w1 | same four pivots | 3 of degree 476, L = 212 each (proven from supports) | 2 of 2 | certified |
| t.z (w1 = 0) | q5 q3 q4 q2 | q5: E5, 1; q3: E3, 1; q4: l2.1, 2 | degrees 14, 17, 17, 17, 15 in q2 | 0 of 4 | split on E3's q3 leading coefficient a2 + b2 q2 (w2); gcd (q2 - root)^2 |
| t.z.nz (w2 != 0) | q5 q3 q4 w2 | same three pivots | degrees 12, 14, 14, 14, 12; L = 2, 3, 3, 3, 3 | 3 of 4 | certified |
| t.z.z (w2 = 0) | q5 q3 q4 | q5: E5, 1; q3: l1.0, 2 | degrees 1, 2, 6, 6, 6, 6, 2 in q4 (pivot E3, degree 1) | 6 of 6 | certified |

The split roots at p1: 302286424 (plus) and 234584485 (minus) for w1; 306016849 for w2 on both. Members whose image is
zero were dropped and are recorded in results.json (`members.<id>.dropped`): l3.5 and l4.3 at the root and at t.nz,
l3.5 at t.z and t.z.nz. No input was dropped. The exact levels 1 and 2 of every node are in the data root
(`exp146/exact-levels-plus.json`, `-minus.json`, 139 MB in all, not in the repository).

## Gates

| Gate | Result | Measured |
|---|---|---|
| G0 | PASS | `branches.py` rerun on EXP-141's `eqs.json`: both outputs have the SHA-256 of the data-root files and of the hypothesis |
| G1 | PASS | P(r1) = 0 mod p1, P(r2) = 0 mod p2, both primes below 2^29, integer coordinates |
| G2 random | PASS | 1,862 nonempty random pairs (2,000 drawn; the rest had a free or constant x), 54,390 weights checked, 0 violations; 551 proven-zero coefficients checked, all zero; planted cancellations 2,002, monomial factors 1,513, formal degree above the true degree in 926 cases, x as split variable in 338, the order lower bound equal to the true order in 543 cases |
| G2 real | PASS | 118 exact levels (levels 1 and 2 of 10 nodes): the propagated M4 bound is at least the exact-support bound at every weight, 0 violations |
| G3 | PASS | 500 cases, leading coefficients of f vanishing at r (drop 1 in 269, drop 2 in 231), phi(exact formal resultant) equals the M5 image: 0 mismatches |
| G4 | PASS | planted unit (3 variables) certified; planted unit with a known exact final constant certified and the constant equals phi(exact) up to sign; planted systems with a common root (a point; a point surviving the chain) not certified. Branch plus with one equation removed from {E3, E5, E6, E7, E10, E11}: not certified in all six; removing E3, E5, E6, E7 the tree did not finish in 300 s (child killed by its own wall limit, so no certificate), removing E10 or E11 the tree finished with a node UNKNOWN |
| G5 | PASS | 118 exact levels: phi(exact) equals the mod-p chain image, 0 mismatches |

## Proof of record

Notation as in hypothesis.md. The certificate is the recorded SLP (`artifacts/slp-plus.json`, `slp-minus.json`):
exact inputs; per node the exact coordinate change, the pivot indices, the formal degrees, the L_i, the final pairs
and constants. The argument has four links.

1. **Ring maps (M1).** P is monic, so phi: Z[y]/(P) -> F_p, y -> r, with P(r) = 0 mod p, is a ring homomorphism. If
   phi(c) != 0 then c != 0 in Z[y]/(P), hence c is a unit of the field L (P irreducible over Q; EXP-141).
2. **Bounds (M4) never under-bound.** For a polynomial h with B_h(w) >= w.a on supp(h) for every weight w of W, and
   f viewed in x with coefficients f_c: for every (a', c) in supp f and every s in the x range,
   w.a' + s c <= B_f(w + s e_x), so w.a' <= e_c(w) := min_s (B_f(w + s e_x) - s c); at w = 0 a nonzero coefficient has
   w-degree 0, so e_c(0) < 0 proves f_c = 0. For h = Res_{x; m, n}(f, g) the Leibniz expansion of the Sylvester
   determinant is a sum of products of one entry per row and column; the w-degree of a product is at most the sum of
   the entry bounds, the w-degree of a sum at most the largest, so B_h(w) = the maximum over permutations of the sum
   of entry bounds, computed exactly by the integer assignment (entries proven zero excluded; if no permutation
   survives h = 0). The argument is word for word valid for a weight with a negative component, since the Laurent
   degree of a product is the sum and that of a sum is at most the maximum. Normalization uses
   w.a <= B(k w)/k and the integrality of w.a. B_h(0) = 0 for a nonzero h.
   Checks: G2 (random, with the bound minus one as a mutant that fails 2,035 times) and G2 real.
3. **Images of formal resultants (M5, M6).** phi commutes with the formal Sylvester determinant for the fixed formal
   degrees (m, n). If phi f has x-degree m' < m and phi g has degree exactly n (the pivot attains its proven bound,
   so its exact degree is n and its exact leading coefficient has a nonzero image), then
   phi Res_{m, n}(f, g) = (-1)^(n (m - m')) lc(phi g)^(m - m') Res(phi f, phi g). G3 checks this against the exact
   determinant over Z[y]/(P); dropping the factor as a mutant fails all 60 trial cases. Members with zero image are
   dropped: the chain is a sequence of resultants (combinations of generators of the node ideal), so a subset of them
   still lies in the ideal. The exact division of M6: U_i has w-order at least L_i = -B_{U_i}(-e_w) (M4 with the
   weight -e_w), and V_i = U_i / w^(L_i) is an element of I + (w s - 1) (V = s^L U + (1 - (w s)^L) V), where s is
   the inverse of w and never appears in a computation; every division was also verified exact at the image level
   (shift_down refuses an inexact division; Singular's own check printed no INEXACT_DIVISION). Constants: a final
   c_i = Res_{x; m_i, n}(V_i, V_pivot) is a constant of Z[y]/(P) by construction (a resultant of two univariates), so
   only its image must be nonzero. A member counts as a nonzero constant before the last variable only if its PROVEN
   bounds are 0 in every variable (B(e_x) = 0 for all x) and its image is nonzero; an image that merely happens to
   be constant does not (`is_constant_member`, unit-tested with a loose bound). No branch used that case: all leaves
   were certified by final pairs.
4. **The tree (M7).** For an ideal I and a polynomial w, I = (1) iff I + (w) = (1) and I + (w s - 1) = (1): if
   w^N lies in I (from I + (w s - 1) = (1): substitute s = 1/w in the identity and clear denominators; Rabinowitsch)
   and 1 = h + w g with h in I (from I + (w) = (1)), then 1 = (h + w g)^N lies in I. In the child "w != 0" only elements of I are
   formed and divisions by w^L are justified in I + (w s - 1); in the child "w = 0" the inputs are the transformed
   inputs with w := 0. The coordinate change w = a + b v (b a nonzero element of Z[y]/(P), hence a unit of L) is an
   automorphism of L[variables], and b^(deg_v f) f((w - a)/b) differs from f(v) by a unit, so the ideal is unchanged.
   Leaves: t.nz, t.z.nz and t.z.z, all certified, so I_+ = (1) and I_- = (1).

The two independent checks of the same exact constants: the evaluation at (p2, r2), a second ring map (nonzero
constants 2 of 2, 3 of 4, 6 of 6 again), and Singular's evaluation at (p1, r1) from the coordinate vectors with its
own coordinate changes, resultants, degree-drop factors and divisions (digests equal at 130 steps per branch).

## Adversarial validation (methodology/03)

- **Cross-implementation (route 3 and 1):** python-flint against Singular 4.3.2 on every member of every node at
  (p1, r1), digest = term count, degree in each variable and the values at two fixed points of F_p, compared up to
  sign (0 flips): 130 per branch; the 18 constants per branch (including the zero constants of the two internal
  nodes) agree. Second ring map: (p2, r2), same tree, same SLP, every leaf nonzero.
- **Stress family (route 4):** G2 random pairs with planted top-coefficient cancellation, zero top coefficients,
  monomial factors and a negative-weight split variable; mutants (every bound lowered by 1; the degree-drop factor
  removed) are caught (2,035 violations of 54,390 checks, and 60 of 60 mismatches). G3 with degree drops 1 and 2.
- **Exact against images (G5, G2 real):** 118 exact levels, 0 mismatches and 0 under-bounds.
- **Controls (G4):** nonempty systems never certified (planted common roots; six branch systems with one equation of
  the minimal unit subset removed, each a zero-dimensional ideal with points). A certificate on any of them would have
  stopped the experiment.

## How could this be wrong?

- The Singular check evaluates the SAME recorded structure (pivot choices, formal degrees, L_i, the split data). It
  checks the images, not the bounds. The bounds rest on the proof above, G2 and G2 real; Singular does not
  independently validate that a formal degree is an upper bound. A formal degree below the true degree would make
  both implementations agree on a wrong object; the exact levels (118) and the second prime guard it partly, the
  later levels (3 and 4, never exact) rest on M4 alone.
- The digests compare term counts, degrees and two evaluation points, not every coefficient: an image difference
  confined to a few coefficients would be missed with probability about (degree / p)^2 per member at most, not zero.
- The negative controls on the branch with one equation removed are weak in four of six cases: the child process was
  killed at its 300 s limit, so those controls show only that no certificate appeared in that time. The planted common
  root systems and the two finished controls are the real negative evidence.
- The irreducibility of P (L a field) and EXP-142's reduction are premises; this experiment does not re-derive them
  beyond G0.
- The mod-p image is a proof of nonvanishing, not of vanishing: a zero image never certified anything, so an
  unlucky prime could only have made a node UNKNOWN, never a false certificate; both primes certify.
- Both implementations share the SLP and the formulas of M1 and M5; a shared misreading of the Sylvester sign or of
  the degree-drop factor would affect both. G3 compares against the exact determinant computed separately (subset
  expansion), which is the guard.
