# EXP-029 - Verdict: CONFIRMED (2026-07-21). The weight-class theorem: the machine found a proof

Artifact: `artifacts/output-2026-07-21.txt`.

## THE THEOREM (unconditional, all degrees)

**For u >= 2, v >= 1, a != 0: P = x + a x^u y^v is never a Keller component: no polynomial
Q, of ANY degree, satisfies J(P, Q) = constant != 0.**

Proof (elementary, every step machine-verified on grids). Give (x, y) the weights
(v, 1 - u): P is w-homogeneous of weight v. Hence L = J(P, .) shifts w-weight by a constant
and the Keller equation decouples into independent weight classes; the constant 1 (weight 0)
is reachable only from the class of y (weight 1 - u), spanned by the single ray
g_s = x^{ks} y^{ms+1}, k = (u-1)/d, m = v/d, d = gcd(u-1, v). On the ray, L is BANDED:
L(g_s) = (ms + 1) e_s + a B_s e_{s+d} with B_s a positive integer (bidiagonal when d = 1,
B_s = qs + p in the h = x^p y^q form). Writing Q's class as a finite sum sum c_s g_s, the
e_0 row forces c_0 = 1; the band recursion c_s = -a B_{s-d} c_{s-d} / (ms + 1) keeps the
c_0-chain nonzero; and the row above the last chain entry demands a B c_last = 0:
contradiction for a != 0. Every polynomial Q truncates, so no partner exists at any degree.
QED.

Honesty: the proof is elementary once seen and may be derivable by specialists (folklore
risk); we have not found it stated, and the record claims exactly that. Found BY the machine:
EXP-028's certificate anatomy (support on one ray) predicted the decoupling.

## Machine verification

1. [MV] The banded formula is exact on the grid u in 2..7, v in 1..7 (and the h-form
   bidiagonal L(g_s) = (2qs+1) e_s + 2a(qs+p) e_{s+1} on p, q <= 4), s <= 5.
2. [MV] The closed-form chain product reproduces ALL SEVEN measured pairings up to rational
   units, with exact a-exponents (2, 4, 5, 6; 2; 2; 3): the window program's outputs were
   this formula all along.
3. [MV] End to end incl. d > 1: full-window inconsistency coincides with ray-class
   inconsistency at every probe: NO second obstruction exists.
4. [MV] Beyond the verified floor: for P = x + a x^54 y^81 (degree 135 > the ~108 floor of
   arXiv:2204.14178): the class is inconsistent for ALL a != 0 at every truncation S <= 8
   (partner degrees to ~1073). With the machine-checked decoupling this certifies: no
   Keller partner of degree <= 1000; the theorem's induction covers all degrees.

## What this retires and what it opens

- Retires: the entire pure-slice window program. EXP-024/025/026/027/028's pure-slice
  certificates are now corollaries of one formula; their value stands as the discovery path
  and as independent verification.
- Scope limit, honestly: the theorem needs P w-homogeneous, i.e. the perturbation is ONE
  monomial. Non-monomial slices (P = x + a h^2 with h binomial, and the EXP-025 slices with
  lower-order terms) are NOT covered: there the polygon has genuine multi-edge structure.
  The successor (JCB-033) is the multi-edge calculus: process edges in weight order,
  each edge contributing a banded class system; if the top-edge obstruction survives
  perturbation (upper-triangularity in the edge filtration), large families of non-monomial
  P's fall too. That is the next reasoning step toward JC(2) itself.
- Beyond-floor statements are now ROUTINE for monomial slices: any x + a x^u y^v at any
  degree, e.g. degree 135, is excluded unconditionally: past every verified range.
