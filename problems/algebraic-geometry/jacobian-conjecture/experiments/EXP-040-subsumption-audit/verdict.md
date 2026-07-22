# EXP-040 - Verdict: CONFIRMED; JCB-028 closes; the ladder recalibrates to B = 16 and (72, 108) (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`. Literature input:
`context/2026-07-22-literature-pass-dossier.md` (primary-source pass, same day).

## Findings

1. **Subsumption by the unconditional theorems [MV].** The pure slice x + a (xy)^2 is
   Theorem-1 shaped (u = v = 2): the queued all-degree closed-form certificate [C] is a
   corollary. Under (v, 1-u) = (2, -1) the seven lower coefficients split 4 below-weight
   (xy, y^2, xy^2, y^3: Theorem 2 covers every combination at ALL degrees) vs 3
   above-weight (x^2, x^2 y, x^3: EXP-037's staircase territory). A deep spot-check agrees:
   the all-below 5-term slice is EMPTY at N = 10.
2. **The JCB-028 remainder, swept [MV].** All 35 4-subsets of the seven coefficients,
   3 rational value tuples each (105 window solves at (4, <= 6)): every one EMPTY; each
   subset tagged with its closure owner (1 pure-below: Theorem 2; 34 involving
   above-weight terms: staircase program).
3. **The recalibration [D, from verified primary sources].** The verified coverage is the
   FULL interval gcd <= 8 (Magnus / Nakai-Baba / Appelgate-Onishi / Nagata; the earlier
   program reading "{1, 8}" as a two-element set was WRONG), plus gcd != p (Abhyankar
   2008), B >= 16 (Heitmann 1990), B != 2p and B = 16 or B > 20 (GGV 2017). Consequently
   EXP-024..028's certificates at gcd 2, 9, 12, 18 are ALL replications inside the
   literature floor (worth keeping as independent machine verifications, nothing more).
   The genuinely open ladder is: B = 16, with GGV's explicit direction set and reduced
   normal form (J. Algebra 471 (2017), Cor 7.13, Thm 8.12) as a concrete attack surface,
   and B > 20 composite non-2p; the lone surviving degree pair below 125 is (72, 108)
   (GGHV arXiv:2204.14178, gcd 36), explicitly left open for compute reasons.
4. **Citation corrections adopted.** Magnus gcd = 1 should cite Math. Scand. 3 (1955)
   (PAMS 5 (1954) is Magnus' formula); Moh's <= 100 has full published detail only for
   the case 64 (GGHV audit); Zoladek's B > 33 claim has a documented gap and must not be
   cited. Wiki and manuscript sweeps queued in the session close.

## What this changes

- JCB-028 CLOSES (corollary + owned residue + swept remainder). JCB-030's frontier
  framing is corrected: the new targets are JCB-040 (attack GGV's B = 16 normal form with
  the transport machine) and the (72, 108) system.
- The manuscript's honesty framing improves: our composite-gcd certificates are
  replications; our unconditional Theorems 1-2 and the equivariant rigidity theorem are
  the novelty candidates (per the adversarial novelty pass: NOT FOUND), with Theorem 3
  "not found as stated, method classical" and Theorem 4 "sharp dichotomy form" (GGV
  Prop 4.1 contains the counterexample half).

## How could this be wrong?

- Part C samples values, not all parameters (declared); the all-parameter statements for
  above-weight subsets await the staircase Theorem 5.
- The literature floor rests on the dossier's primary-source reads; six UNVERIFIED items
  are listed there (notably Moh's verbatim case list and the van den Essen book texts)
  and are carried, not resolved.
