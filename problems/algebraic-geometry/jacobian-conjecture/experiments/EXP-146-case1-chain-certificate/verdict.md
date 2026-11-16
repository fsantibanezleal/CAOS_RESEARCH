# EXP-146 verdict: CONFIRMED (both Case 1 branch ideals are certified as the unit ideal)

Date: 2026-11-15; rerun with the corrected code and records 2026-11-16 (see "Errata and corrections"). Hypothesis frozen
at 8133b594 (not edited). CPU only; python-flint 0.9.0 exact arithmetic, numpy int64 Hungarian, Singular 4.3.2 (WSL) as
the second implementation. `run.py` exits 0; `artifacts/results.json` carries the verdict word and every measured value.
Production run (`results.json` seconds_total 1853.5, `run-log.txt`): 1,854 s in all, of which G4 took 1,392 s (four
branch controls killed at their 300 s wall limit, 1,200 s, and two finished controls, two extended controls and the
Singular nonemptiness check); the two trees took 252 s (plus) and 102 s (minus); replay at p2 about 3 s and the Singular
checks 12.4 s and 3.5 s. The rerun reproduces the 99ebd728 certificates exactly: `artifacts/rerun-comparison.json`
(`compare_slp.py`), 0 differences in trees, pivots, formal degrees, L values and the constants at p1 and p2.

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
| Singular's images equal python-flint's at every step | CONFIRMED | `artifacts/singular-check.txt`: 153 digests per branch (130 member digests and 23 digests of the final univariates V) and 18 constants compared, 0 mismatches, 0 missing, 0 flags (0 sign flips: both resultants use the same sign convention) |
| The first two chain levels from exact supports replace the probe's image supports | DONE | 118 exact polynomials (`exact_levels_checked` counts polynomials, not levels: 59 per branch, levels 1 and 2 of the 5 nodes of each; G2 real, G5); the fallback of an exact level 3 was never needed |

## The tree (identical shape on both branches)

Elimination order q5, q3, q4, q2, q0 at the root. Degrees are formal degrees, equal to the image degrees at every
pivot (the attained-bound rule). Constants: nonzero final images over the pairs (V_i, V_pivot).

| Node | Order (last variable) | Pivots (variable, member, degree) | Univariates (degree after division by w^L) | Nonzero constants | Outcome |
|---|---|---|---|---|---|
| t (root) | q5 q3 q4 q2 q0 | q5: E3, 1; q3: l1.0, 2; q4: l1.2, 2; q2: l3.0, 14 | 3 of degree 688 in q0, L = 0 | 0 of 2 | split on E3's q5 leading coefficient alpha + beta q0 (w1); gcd of the images (q0 - root)^212 |
| t.nz (w1 != 0) | q5 q3 q4 q2 w1 | same four pivots | 3 of degree 476, L = 212 each (the order lower bound of the M4 bound, here the composed bound of two propagated steps; the division by w^212 was checked exact at the images) | 2 of 2 | certified |
| t.z (w1 = 0) | q5 q3 q4 q2 | q5: E5, 1; q3: E3, 1; q4: l2.1, 2 | degrees 14, 17, 17, 17, 15 in q2 | 0 of 4 | split on E3's q3 leading coefficient a2 + b2 q2 (w2); gcd (q2 - root)^2 |
| t.z.nz (w2 != 0) | q5 q3 q4 w2 | same three pivots | degrees 12, 14, 14, 14, 12; L = 2, 3, 3, 3, 3 | 3 of 4 | certified |
| t.z.z (w2 = 0) | q5 q3 q4 | q5: E5, 1; q3: l1.0, 2 | degrees 1, 2, 6, 6, 6, 6, 2 in q4 (pivot E3, degree 1) | 6 of 6 | certified |

The split roots at p1: 302286424 (plus) and 234584485 (minus) for w1; 306016849 for w2 on both. Members whose image is
zero were dropped and are recorded in results.json (`members.<id>.dropped`): l3.5 and l4.3 at the root and at t.nz,
l3.5 at t.z and t.z.nz. No input was dropped. The exact levels 1 and 2 of every node are in the data root
(`exp146/exact-levels-plus.json`, `-minus.json`, 145 MB in all (144,964,257 bytes), not in the repository).

## Gates

| Gate | Result | Measured |
|---|---|---|
| G0 | PASS | `branches.py` rerun on EXP-141's `eqs.json`: both outputs have the SHA-256 of the data-root files and of the hypothesis |
| G1 | PASS | P(r1) = 0 mod p1, P(r2) = 0 mod p2, both primes below 2^29, integer coordinates |
| G2 random | PASS | `G2_random`: 2,000 pairs drawn, 1,862 kept (the rest had a free or constant x). On all 1,862: 551 proven-zero coefficients checked, all zero. 560 of them have a zero formal resultant (skipped for weights); on the other 1,302 pairs (`weight_checked_pairs`) 54,390 weights were checked, 0 violations, and the order lower bound equals the true order in 543. Planted: cancellations 2,002, monomial factors 1,513, formal degree above the true degree in 926 cases, x as split variable in 338 |
| G2 composed | PASS | `G2_composition` (`run.py` calls `gates.g2_composition(600)`): 600 pairs of two composed steps (elimination of x, then of a) drawn; 197 skipped; 131 with a zero resultant at either step, excluded from the weight and order checks; 272 kept, on which 3,557 weights were compared with the exact formal Sylvester resultant of the second step, 0 violations; the order lower bound of the split variable checked in 131 of the 179 kept split cases, 0 violations; 180 proven-zero coefficients, 0 violations. The gate's inline mutant (every entry lowered by 1) passes by construction: `chaincert.py:257` sets the bound to 0 at w = 0, where the exact maximum is also 0, so it fires once in each of the 272 kept cases and its pass condition (at least one violation) is not evidence. The composed-bound mutants are in `artifacts/mutants.json`: M1b (every entry of the second-step table lowered by 1, w = 0 included) raises 2,381 violations on the 272 kept cases, weight and order-lower-bound checks counted together, 272 of them at w = 0 by the same construction; M1c (the same with the w = 0 entry left unlowered, added after the final check) raises 2,109 and still fails the gate, so a lowered composed bound is caught away from w = 0. Only the level-4 members of t and t.nz rest on a bound that passes through two propagated steps (every other bound is one step from exact supports): that is the kind of bound this family tests |
| G2 real | PASS | 118 exact polynomials (59 per branch: levels 1 and 2 of the 5 nodes of each branch): the propagated M4 bound is at least the exact-support bound at every weight, 0 violations |
| G3 | PASS | 500 cases, leading coefficients of f vanishing at r (drop 1 in 269, drop 2 in 231), phi(exact formal resultant) equals the M5 image: 0 mismatches |
| G4 | PASS | planted unit (3 variables) certified; planted unit with a known exact final constant certified and the constant equals phi(exact) up to sign; planted systems with a common root (a point; a point surviving the chain) not certified; a planted nonempty system that splits (`planted_split_common`: 4 generators in 2 variables) not certified: its nodes psc and psc.nz are nonempty (Singular dim 0, vdim 1 each) with 2 final pairs each, both zero, and psc.z is empty (dim -1) and certified by the constant member f1. Branch plus with one equation removed from {E3, E5, E6, E7, E10, E11}: 2 of 6 controls finished (E10 and E11: the tree finished, node neg.nz UNKNOWN, not certified), 4 of 6 are inconclusive (E3, E5, E6, E7: child killed at its 300 s wall limit, so no certificate appeared but no evidence either way), 0 crashed. Singular nonemptiness of the drop-one systems (`branch_subset_nonemptiness`, pass true): at p1 and p2 each of the six drop-one ideals has dim 0 with vdim 146, 120, 120, 122, 104, 104 (removal of E3, E5, E6, E7, E10, E11) and the full subset has dim -1. Extended controls with n + 2 = 7 generators (drop E10 or E11 plus two of the subset's own ideal members, `branch_extended_controls`): finished, not certified, on nonempty nodes neg and neg.nz (dim 0, vdim 104) but with 1 final pair each. `final_pair_summary`: `nonempty_nodes_with_two_zero_pairs` = 2, both from `planted_split_common`; no branch-derived control with n + 2 generators reaches two final pairs on a nonempty node. The per-node generator and variable counts (psc 4 and 2, psc.nz 5 and 3, as Singular sees them) are recorded by `gates.prove_nonempty` since the rerun and are in `artifacts/g4-planted-generator-counts.json` (the planted part of G4 rerun alone; the branch controls of results.json predate the field) |
| G5 | PASS | 118 exact polynomials: phi(exact) equals the mod-p chain image, 0 mismatches |

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
   w.a <= B(k w)/k and the integrality of w.a. B_h(0) = 0 for a nonzero h: this rule, tab[0] := 0, is applied to
   every resultant table (valid because a nonzero polynomial has w-degree 0 at w = 0). Two rules of the code are narrower
   than the frozen wording of M4 ("carried unchanged" for a member that does not meet the pivot variable): a member
   whose coefficients of x^c, c >= 1, are all proven zero (formal degree 0) passes the step with the table
   B'(w) = min over s of B(w + s e_x) (`drop_var`), valid because (w + s e_x).a = w.a for every monomial a of a
   polynomial free of x and every s; the pass route also checks that the image (and the exact support when known) is
   free of x and raises otherwise. Neither the pass route nor `drop_var` was used in this run (member kinds per branch: 91 res, 0 pass, counted in the SLP steps).
   Checks: G2 random, G2 composition (two composed steps; its inline mutant passes by construction, see the G2 composed
   row, and the composed-bound mutants are M1b and M1c in `artifacts/mutants.json`) and G2 real; the bound-lowered
   and degree-drop mutants and their measured failures are recorded in `artifacts/mutants.json` (`mutants.py`).
   Composed bounds: only the level-4 step of the root t and of t.nz propagates a bound through two steps from exact
   supports; `G2_composition` (above) compares that step with the exact formal Sylvester resultant at every weight.
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
own coordinate changes, resultants, degree-drop factors and divisions (digests equal at 153 places per branch: 130
member digests and 23 digests of the final univariates).

## Adversarial validation (methodology/03)

- **Cross-implementation (route 3 and 1):** python-flint against Singular 4.3.2 on every member of every node at
  (p1, r1), digest = term count, degree in each variable and the values at two fixed points of F_p, compared up to
  sign (0 flips): 153 digests per branch (130 member digests and the 23 digests of the final univariates); the 18 constants per branch (including the zero constants of the two internal
  nodes) agree. Second ring map: (p2, r2), same tree, same SLP, every leaf nonzero.
- **Stress family (route 4):** G2 random pairs with planted top-coefficient cancellation, zero top coefficients,
  monomial factors and a negative-weight split variable; mutants (`artifacts/mutants.json`) are caught: every bound
  lowered by 1 gives 30,314 violations (weight and order checks counted together; 54,390 weights checked) over 1,862 pairs
  (G2 random) and 2,381 over 272 cases (the second composed step, M1b; 2,109 with the w = 0 entry left unlowered, M1c); the degree-drop factor removed gives 60 of 60 and 500 of 500 mismatches. G3 with degree
  drops 1 and 2.
- **Exact against images (G5, G2 real):** 118 exact polynomials, 0 mismatches and 0 under-bounds.
- **Controls (G4):** nonempty systems never certified: planted common roots, the planted split-common system, and the
  branch systems with one equation of the minimal unit subset removed. Singular shows that each of the six drop-one
  ideals is zero-dimensional and nonempty at p1 and p2 (a point set, dim 0), but only 2 of the 6 controls finished
  (E10, E11); the other 4 were killed at their limit and are inconclusive. The only evidence with two or more zero
  final pairs on a nonempty node is the planted split-common system (two nonempty nodes with two zero final pairs each,
  Singular dim 0); the two extended controls (nodes neg and neg.nz, Singular dim 0, `G4.branch_extended_controls`) and
  the review's planted system common2 add one zero final pair each on nonempty nodes; no branch-derived control with
  n + 2 generators reaches two final pairs on a nonempty node. A certificate on
  a nonempty system would have stopped the experiment.

## How could this be wrong?

- The Singular check evaluates the SAME recorded structure (pivot choices, formal degrees, L_i, the split data). It
  checks the images, not the bounds. The bounds rest on the proof above, G2 and G2 real; Singular does not
  independently validate that a formal degree is an upper bound. A formal degree below the true degree would make
  both implementations agree on a wrong object; the exact levels (118 polynomials) and the second prime guard it
  partly, the later levels (3 and 4, never exact) rest on M4 alone, and the level-4 bound of t and t.nz on the composition
  of two propagated steps (`G2_composition` tests that composition on random pairs, not on these exact objects).
- The digests compare term counts, degrees and two evaluation points, not every coefficient: an image difference
  confined to a few coefficients would be missed with probability about (degree / p)^2 per member at most, not zero.
- The negative controls on the branch with one equation removed are weak in four of six cases: the child process was
  killed at its 300 s limit (E3, E5, E6, E7), so those controls show only that no certificate appeared in that time
  (inconclusive); 2 of 6 finished (E10, E11). The extended controls with n + 2 generators cover only drop E10 and drop
  E11, not E3, E5, E6, E7, and reach one final pair on their nonempty nodes. The only final-pair negative evidence with two or
  more zero pairs on a nonempty node is the planted split-common system (two nonempty nodes, two zero pairs each,
  Singular dim 0); the extended controls and the review's common2 add one zero final pair each on nonempty nodes; G4 passes when every
  branch control is killed, by design (a kill is inconclusive, never a pass of its own).
- The irreducibility of P (L a field) and EXP-142's reduction are premises; this experiment does not re-derive them
  beyond G0.
- The mod-p image is a proof of nonvanishing, not of vanishing: a zero image never certified anything, so an
  unlucky prime could only have made a node UNKNOWN, never a false certificate; both primes certify.
- Both implementations share the SLP and the formulas of M1 and M5; a shared misreading of the Sylvester sign or of
  the degree-drop factor would affect both. G3 compares against the exact determinant computed separately (subset
  expansion), which is the guard.

## Errata and corrections (2026-11-16)

The review of 2026-11-15 and its re-check of 2026-11-16 corrected the first record; the figures above are those of the
rerun with the corrected code (`artifacts/results.json`, `run-log.txt`). What changed against the first record:

- **Frozen hypothesis, wrong citation.** `hypothesis.md:133-136` (G4) gives "a zero-dimensional ideal with points,
  EXP-142 `structure.md` item 7" as the source for the drop-one systems. Item 7 of EXP-142's structure.md drops rows of
  rref_plus at p = 1021, not original equations, so it does not establish that each drop-one ideal has points. The
  hypothesis is not edited. The fact is now measured here: Singular at p1 and p2 gives dim 0 for each of the six
  drop-one ideals (vdim 146, 120, 120, 122, 104, 104) and dim -1 for the full subset
  (`G4.branch_subset_nonemptiness`; a planted unit drop-one ideal makes that check, and G4, fail: `tests/test_jacobian_exp146.py`).
- **Controls.** The first record (99ebd728) called each of the six drop-one systems "a zero-dimensional ideal with
  points" (not measured then; measured now at p1 and p2, above) and called "the planted common root systems and the two
  finished controls" "the real negative evidence"; only 2 of the 6 drop-one controls finished and 4 were killed
  (inconclusive), and the two finished square controls form no final pair at the root or in w != 0 nodes, so they never
  tested the final-pair route (review F1; they test the constant-member route, the bounds and the split). No
  branch-derived control with n + 2 generators reaches two final pairs on a nonempty node; the only final-pair evidence
  with two or more zero pairs on a nonempty node is `planted_split_common`.
- **Counts.** Digests: 153 per branch (130 member digests plus 23 digests of the final univariates), not 130.
  `exact_levels_checked` (118) counts polynomials (59 per branch), not levels. G2 random: 1,862 kept of 2,000 drawn; the
  proven-zero checks run on all 1,862 and the weight and order checks on the 1,302 with a nonzero resultant (560 zero).
- **Mutants.** "2,035 violations of 54,390" is replaced by the figures of `artifacts/mutants.json`: 30,314 violations
  (G2 random, 54,390 weights checked), 2,381 (second composed step, M1b, 3,557 weights checked), 60 of 60 and 500 of 500
  (degree-drop factor removed); the violation counts of M1 and M1b include order-lower-bound checks. M1c (added
  2026-11-16 with `mutants.py` rerun: every earlier entry reproduced exactly) leaves the w = 0 entry unlowered and gives
  2,109.
- **Timing.** The about 1,250 s of G4 in the first record were the four killed controls (1,200 s) and little else; the
  rerun's G4 took 1,392 s.
- **L of t.nz.** The orders 212 are the order lower bound of the propagated bound (a composed bound), not a bound "proven
  from supports".
- **Proof of record item 2.** States the tab[0] := 0 rule and the drop_var rule, narrower than the frozen "carried
  unchanged"; neither drop_var nor the pass route was used in the run.
- **Reproduction.** `compare_slp.py` against the 99ebd728 SLPs (`artifacts/rerun-comparison.json`): 0 differences in
  both branches; the only new fields are the 23 V digests per branch.

## Addendum (2026-11-16): archived independent checks and inputs

The review's third-prime scripts and their outputs are archived in `independent-checks/third-prime/` (rebuilt from the
recorded edits after the review's scratch folder was deleted; each script has the SHA-256 printed in the review report; the
outputs are a rerun with the review's commands and agree with its recorded outputs), and the two branch inputs are committed
in `inputs/` (SHA-256 equal to G0's). See `independent-checks/README.md`. No verdict number changes.

