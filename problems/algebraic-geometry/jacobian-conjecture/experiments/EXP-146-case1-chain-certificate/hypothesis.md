# EXP-146 - Case 1 by single-prime resultant-chain certificates with proven degree bounds (JCB-103)

Date: 2026-11-15. Frozen before any code of this experiment is written or run. CPU only.

## Question

Are the two branch ideals I_+ and I_- of EXP-142 (Case 1 split at q1 = +c and q1 = -c, over L = Q[y]/(P),
P = y^5 - y^4 + 3y^3 + 3y^2 + 26) the unit ideal, certified by trees of resultant chains whose final constants are
nonzero modulo one prime, with every degree used in a resultant proven?

## Why

EXP-139 to EXP-143 are UNKNOWN: exact standard bases do not finish, and the multi-modular cofactor certificates exceed
about 94,000 digits per coordinate (EXP-143). A resultant chain needs no certificate of that height: every resultant
Res_x(f, g) is a combination a f + b g, so a chain that ends in a nonzero constant c proves the ideal is (1), and the
image of c under a ring map Z[y]/(P) -> F_p proves c != 0 when the image is nonzero. The obstacle is that the image of
a resultant equals the resultant of the images only when the formal Sylvester degrees are the exact degrees (or proven
upper bounds handled by the degree-drop formula). This experiment proves those degrees.

Probes of 2026-11-14 and 2026-11-15 (evidence only, scripts outside the repository, not part of the result; summary
in CAOS_MANAGE `plans/caos-research/jacobian-conjecture/status.md`), at p = 536870909, r = 505390653:

1. The plain chain (pivots q5, q3, q4, q2) reaches univariates of degree 688 in q0 in 0.3 s (python-flint), all sharing
   the factor l^212, where l = alpha + beta q0 is the q5 coefficient of E3; their resultants vanish.
2. Support-based degree bounds (below) computed from the inputs alone are loose from the first level (exact
   cancellations, for example the q0-degree 7 against a bound 8 of a level-1 member). With the first two chain levels
   taken from exact supports and weights in {0..3}, every later bound equals the image degree (688 = 688).
3. In coordinates w1 = l (q0 = (w1 - alpha)/beta), the factor w1^212 is proven from supports (lower bound 212 = image
   order). In the case w1 != 0 it can be divided out; the two final resultants are nonzero. In the case w1 = 0 the
   univariates in q2 share a squared linear factor, the root of the q3 pivot's leading coefficient a2 + b2 q2; a second
   split of the same kind (w2 = a2 + b2 q2) certifies both children. Both branches gave the same three-leaf tree:
   w1 != 0 (2 of 2 constants nonzero), w1 = 0 and w2 != 0 (3 of 4), w1 = 0 and w2 = 0 (6 of 6). The classical
   assignment bound and the tropical bound gave the same result.

## Inputs and premises

- The branch systems written by EXP-142 `branches.py` from EXP-141's `eqs.json` (data root
  `caos-research/jacobian-conjecture/exp141-main/eqs.json`): nine equations each in q0, q2, q3, q4, q5, coefficients
  as integer coordinate vectors in the basis 1, y, ..., y^4, i.e. elements of Z[y]/(P). The data-root copies
  `exp142-143-branch-plus/eqs.json` and `exp142-143-branch-minus/eqs.json` have SHA-256
  `bd227b531c813586f60b1792b90ef7595d19d226b7ab2d380b3125250849424a` and
  `0a3a390581c4f44c06907a61022069f7d704283e3b1def8947bb44cafaae76e9`.
- EXP-142's exact reduction [D]: Case 1 is empty iff both branch ideals are (1) in L[q0, q2, q3, q4, q5]. EXP-141's field
  step [D] and EXP-140's reduction [D] carry over unchanged. This experiment does not re-derive them.

## Method

**M1. Ring maps.** For a prime p and r with P(r) = 0 mod p, phi = phi_{p,r}: Z[y]/(P) -> F_p, y -> r, is a ring
homomorphism (P is monic), extended coefficient-wise to polynomial rings. A nonzero phi(c) implies c != 0 in
Z[y]/(P), hence c is a unit of L. phi commutes with sums, products, coefficient extraction, the formal Sylvester
resultant Res_{x; m, n} for fixed formal degrees m, n (a determinant of the coefficients), substitution of a variable
by an affine expression with coefficients in Z[y]/(P), and exact division by a monomial x^L when x^L divides exactly.

**M2. Exact objects.** Every polynomial of the certificate is defined exactly, as a straight-line program (SLP) over
Z[y]/(P) from the inputs, by: coordinate changes and substitutions on a node's inputs (computed exactly); formal
resultants Res_{x; m, n}(f, g) with m, n proven upper bounds on deg_x f and deg_x g; exact division by x^L when every
monomial of the exact polynomial has x-exponent at least L (proven). The program is evaluated exactly for the first
two chain levels of every node and only through phi afterwards.

**M3. Exact levels.** At every node, chain levels 1 and 2 are computed exactly over Z[y]/(P) (python-flint
fmpz_mpoly with y adjoined, every result reduced modulo P), and their supports are read exactly. A gate (G5) checks that
phi of each exact level-1 and level-2 polynomial equals the image computed by the mod-p chain. If at some node no pivot
attains its bound at level 3 or later, level 3 of that node is also computed exactly (the only fallback allowed).

**M4. Proven degree bounds.** Each polynomial h with variable set V(h) carries B_h(w) >= max over a in supp(h) of
w.a, for every weight w in W(V(h)): components in {0, 1, 2, 3}, except the node's split variable (M7), whose
component ranges over {-3, ..., 3} (a negative component bounds the order of vanishing from below).
- Exact polynomials (inputs, exact levels): B_h(w) = max over the exact support.
- Normalization: B_h(w) <- min(B_h(w), floor(B_h(k w) / k)) for k = 2, 3 when k w is in W.
- Coefficient bounds: for f viewed in x with coefficients f_c, e_c(w) = min over s in the x-range of
  B_f(w + s e_x) - s c (valid because w.a' + s c <= B_f(w + s e_x) for every (a', c) in supp f). If e_c(0) < 0 then
  f_c = 0 exactly (a nonzero polynomial has w-degree >= 0 at w = 0). The formal degree of f in x is the largest c with
  c <= B_f(e_x) and f_c not proven zero.
- Resultant bound: for h = Res_{x; m, n}(f, g), B_h(w) = the maximum over permutations of the Sylvester matrix of the
  sum of the entry bounds (e_c(w) of f in the n rows of f, of g in the m rows of g; proven-zero entries excluded),
  computed exactly by an integer Hungarian assignment. Valid because each term of the Leibniz expansion is a product of
  entries, whose w-degree is at most the sum of the entry w-degrees; the sum of the terms cannot exceed the largest.
  For a weight with a negative component the same argument holds for Laurent degrees.
- The bound of a member free of x is carried unchanged.

**M5. Chain at a node.** The node has inputs and a variable order. For each variable x but the last:
- pivot: a member whose image has x-degree equal to its proven bound B(e_x) (so its exact x-degree is that bound and
  its exact leading coefficient has a nonzero image); among those the lowest bound, then the fewest image terms, then
  the lowest index;
- every other member f with B_f(e_x) > 0 is replaced by Res_{x; m, n}(f, pivot), m = formal degree of f, n = the pivot's;
  its image is (-1)^(n (m - m')) lc_x(phi pivot)^(m - m') Res_x(phi f, phi pivot) when phi f has x-degree m' < m,
  and Res_x(phi f, phi pivot) when m' = m;
- members whose image is zero are dropped (a subset of generators: sound); members free of x pass unchanged.

**M6. Last variable.** The remaining members U_i are univariate in the last variable x. In a node of type "w != 0"
(M7, x = w), L_i = -B_{U_i}(-e_w) is a proven lower bound on the w-order of U_i, and V_i = U_i / w^(L_i) (exact
division, M2), formal degree B_{U_i}(e_w) - L_i; otherwise V_i = U_i. Pivot rule as in M5; constants
c_i = Res_{x; m_i, n}(V_i, V_pivot). The node is certified if some phi(c_i) != 0, or if some member is a nonzero
constant before the last variable.

**M7. Tree construction.** If a node is not certified, take the gcd of the images of the V_i. The split polynomial is
the leading coefficient of the first pivot (in elimination order) that is, as an exact polynomial, of the form a + b v
with v the node's last variable, a, b in Z[y]/(P), b != 0, and whose image root -phi(a)/phi(b) is a root of the gcd
(the pivot is an input or an exact-level polynomial, so a and b are exact). If none exists, the node is UNKNOWN.
Coordinates w = a + b v, applied exactly to the node's inputs as b^(deg_v f) f((w - a)/b). Two children:
- "w != 0": order = the node's order without v, then w; split variable w;
- "w = 0": the transformed inputs with w := 0; order = the node's order without v.
Soundness [D]: for an ideal I and a polynomial w, I = (1) iff I + (w) = (1) and I + (w s - 1) = (1) (Rabinowitsch: the
second gives w^N in I, the first gives 1 = h + w g with h in I, and (h + w g)^N lies in I). In the child "w != 0" only
elements of I are formed, and dividing by w^L stays in I + (w s - 1) because w is a unit there (V = s^L U + (1 - (w s)^L) V);
s never appears in a computation. The coordinate change is an automorphism of L[variables] (b is a unit of L), and
multiplying an input by a nonzero constant does not change the ideal. Depth limit 4.

**M8. Primes.** The tree is built at (p1, r1) = (536870909, 505390653). The SLP is recorded (node coordinate changes as
exact elements, pivot indices, formal degrees, L_i, the final pairs and the image constants). It is evaluated again at
(p2, r2): p2 the largest prime below p1 at which P has a root, r2 its smallest root; the exact objects and bounds are
the same, only phi changes, and every leaf must again give a nonzero constant. Both primes are below 2^29 (Singular's
limit for M9).

**M9. Second implementation.** Singular 4.3.2 (WSL) reads the exact inputs and the recorded SLP, computes the images at
(p1, r1) itself (its own evaluation of the coordinate vectors at r1, its own coordinate changes, resultants, degree-drop
factors and divisions) and prints every member's image and the final constants. Its images must equal
python-flint's at every step up to sign (the sign conventions of the two resultants may differ; a sign does not change
whether a constant is zero).

## Gates (before production)

- G0. Inputs: rerun EXP-142 `branches.py` on EXP-141's `eqs.json`; both outputs equal the data-root branch files
  (SHA-256 above). Failure stops the experiment.
- G1. Ring maps: P(r1) = 0 mod p1 and P(r2) = 0 mod p2; the inputs have integer coordinates.
- G2. Bound engine soundness: 2,000 random pairs of sparse polynomials over Z (2 to 4 variables, degrees up to 6,
  including planted top-coefficient cancellations, zero top coefficients and monomial factors), exact resultants by
  python-flint: for every weight in W, the bound is at least the exact value, and every proven-zero coefficient is
  zero. On the real system: at levels 1 and 2 of every node, the bound propagated by M4 from the previous level is at
  least the exact-support value, for every weight (no violation).
- G3. Degree-drop formula: 500 random cases over Z[y]/(P) with degree drops modulo p planted (an exact leading
  coefficient divisible by p at r): phi of the exact formal resultant equals the M5 image formula.
- G4. Controls: a planted system over Z[y]/(P) in 3 variables, unit with a known exact constant, is certified; the
  branch system q1 = +c with one equation removed from EXP-142's greedy minimal unit subset (a zero-dimensional ideal with
  points, EXP-142 `structure.md` item 7) is not certified; a planted system with a common root is not certified. A
  certificate on a nonempty system stops the experiment as a bug.
- G5. Exact against images: phi of every exact level-1 and level-2 polynomial equals the mod-p chain's image.

## Prediction

Both branch ideals are certified at (p1, r1) by the three-leaf tree of the probe (HIGH for the tree shape on the
plus branch, MODERATE on the minus branch until the exact levels replace the probe's image supports); every leaf is
nonzero again at (p2, r2); Singular's images equal python-flint's.

## Budget and stop condition

Six hours of wall time in all, at most two processes. A node that exceeds 30 minutes, or a tree deeper than 4, is
UNKNOWN; the verdict is then UNKNOWN with the tree and the measured bounds.

## What a CONFIRMED verdict claims

Both branch ideals are (1) in L[q0, q2, q3, q4, q5]; with EXP-142's reduction, Case 1 of GGHV Proposition 4.3 at
(72,108), as encoded by our 13 compatibility equations, has no solution over the algebraic closure of Q [D]. The proof
is the recorded SLP: exact inputs and exact levels, the bound rules of M4 (proved above), the Rabinowitsch splits of M7
and nonzero images at (p1, r1). The evaluation at (p2, r2) and the Singular evaluation are independent checks of the
same exact constants. Nothing beyond Case 1 is claimed. JCB-103 is closed by a CONFIRMED verdict.

## How this could be wrong

1. A bound under the true degree (an engine bug): the image would not be phi of the exact resultant. Guarded by the
   proof in M4, by G2 (random and real-system checks) and by the attained-bound rule for pivots.
2. A lower bound L_i above the true w-order: the division would not be exact. L_i comes only from supports (negative
   weights, M4), and G2 includes monomial factors.
3. Wrong inputs: G0.
4. A shared misconception of the two implementations: both use the same SLP and M1; the second prime checks phi.
5. A tree that certifies a nonempty system: G4's negative controls.

## Invariant-first note

The deciding invariant is the order of vanishing of the univariates along the pivot's leading coefficient: a power of
that coefficient is the only common factor in the probe, and it becomes a monomial, hence provable from supports, in
coordinates where the coefficient is a variable.
