# The pure pairs of forms of degree e form a family of dimension at least 4e - 4 through <x^e, y^e>

Date: 2026-11-20. Status: derivation [D], written after the hypothesis of EXP-006 was frozen and before any of its
results was read. Reviewed on 2026-11-20 by a reader other than the writer (record
`bs-pure-family-dimension-review-2026-11-20` in the coordination repository): the statement (a) to (d) and its proof
are correct; one remark was false and is replaced below (the locus D_e is not of the expected codimension), and seven
minor repairs are applied. The first text is in commit e458e215.

## Setting

U = U(H) over a field k, u(n) = dim U_n = floor((n + 2)^2 / 4) for n >= 0 and u(n) = 0 for n < 0. For e >= 2 let
G_e = Gr(2, U_e), of dimension 2 (u(e) - 2). For W in G_e put M_W = U / (U W), a cyclic left module with two relations
of degree e, and let mu_n(W): U_(n-e) tensor W to U_n be left multiplication, so that
H_W(n) = dim (M_W)_n = u(n) - rank mu_n(W). The Hilbert function of the pure table (1, 2, 2, 1) on (0, e, 3e, 4e) is
h_e(n) = u(n) - 2 u(n-e) + 2 u(n-3e) - u(n-4e). Call W pure when M_W has that Betti table, and let P_e be the set of
pure W.

Two values: h_e(3e) = u(3e) - 2 u(2e) + 2 equals ((e - 2) / 2)^2 for e even and (e - 1)(e - 3) / 4 for e odd (0, 0,
1, 2, 4, 6 for e = 2, ..., 7), and 2 u(e) - 4 - 2 h_e(3e) = 4e - 4 for every e (for e even it is
((e + 2)^2 - (e - 2)^2) / 2 - 4, for e odd ((e + 1)(e + 3) - (e - 1)(e - 3)) / 2 - 4).

## Statement

Let e >= 2 and let k be algebraically closed. Put r = 2 u(2e) - 2 and
D_e = {W in G_e : rank mu_(3e)(W) <= r}.

(a) Every irreducible component of D_e has codimension at most 2 h_e(3e) in G_e.

(b) P_e is contained in D_e and is open in D_e, in every characteristic.

(c) Hence every irreducible component of P_e has dimension at least 4e - 4: 4 and 8 for e = 2, 3 (where P_e is open
in G_e), and 12, 16, 20, 24 for e = 4, 5, 6, 7. The bound concerns the components of D_e that meet P_e.

(d) If the characteristic of k is 0 or at least 2e, then P_e is not empty: it contains W_0 = <x^e, y^e> (Theorem A
of the manuscript). P_e is stable under the graded automorphisms of U (the group GL_2 acting on U_1 = <x, y>; it acts
on G_e through PGL_2, of dimension 3), and the orbit of W_0 has dimension 2. So for e >= 4 the pure cyclic modules on
the ray (0, e, 3e, 4e) form a family of dimension at least 4e - 4 in which the modules of the published family
U/U(l_1^e, l_2^e) are a subfamily of dimension 2: up to automorphism there are at least 4e - 7 parameters of pure
modules (9 at e = 4).

## Proof

(a) On G_e let S be the tautological subbundle of rank 2. Left multiplication is a map of vector bundles
mu_(3e): U_(2e) tensor S to U_(3e) tensor O, of ranks m = 2 u(2e) and n = u(3e). D_e is its locus of rank at most r,
and r <= min(m, n) because h_e(3e) >= 0. Locally on G_e the bundle map is a morphism phi from an open set of G_e to
the space of m by n matrices, and D_e is the preimage of the variety Y_r of matrices of rank at most r, which is
irreducible of codimension (m - r)(n - r) (Bruns and Vetter, Determinantal Rings, chapter 2). The preimage is the
intersection of the graph of phi with G_e times Y_r inside the smooth variety G_e times the space of matrices, so
each of its components has dimension at least dim G_e - (m - r)(n - r) (the dimension of an intersection in a smooth
variety). Here (m - r)(n - r) = 2 (u(3e) - 2 u(2e) + 2) = 2 h_e(3e). (The same bound is Theorem 14.4 (b) of Fulton,
Intersection Theory; the book was not opened for this note, which is why the argument is written out.)

(b) Let W be pure. Its minimal resolution has two second syzygies, in degree 3e, and none below, so mu_n(W) is
injective for n < 3e and the kernel of mu_(3e)(W) has dimension 2: rank mu_(3e)(W) = r and W lies in D_e.

Openness. Let W_1 be pure. The following conditions define a subset V of D_e that contains W_1, and each is open in D_e:

1. mu_n(W) is injective for e <= n < 3e (maximal rank);
2. rank mu_(3e)(W) >= r (so the rank is r on V, and K(W) = ker mu_(3e)(W) is a vector bundle of rank 2 on V with its
   reduced structure);
3. for 3e < n <= 4e + 1, rank mu_n(W) >= u(n) - h_e(n);
4. for 3e < n <= 4e + 1, the map nu_n(W): U_(n-3e) tensor K(W) to U_(n-e) tensor W (left multiplication of the two
   syzygies) has rank at least 2 u(n-3e) - u(n-4e), its rank at W_1.

Conditions 1, 2 and 3 are lower bounds on the rank of a map of vector bundles, and so is 4 on the locus of 2. At W_1
they hold with equality, by the pure resolution: the kernel of mu_n(W_1) is the image of nu_n(W_1), and the kernel of
nu_n(W_1) is the third syzygy, of dimension u(n-4e) (U is a domain).

On V the image of nu_n(W) lies in the kernel of mu_n(W), because mu is linear for left multiplication, so
rank mu_n(W) <= 2 u(n-e) - (2 u(n-3e) - u(n-4e)) = u(n) - h_e(n) for 3e < n <= 4e + 1; with 3 this is an equality.
So H_W(n) = h_e(n) for every n <= 4e + 1. Since h_e(n) = 0 for n >= 4e - 3 and M_W is generated in degree 0, M_W
vanishes from degree 4e - 3 on, and H_W = h_e.

So V is a neighbourhood of W_1 in D_e on which the Hilbert function is constant. Over V with its reduced structure the
graded pieces of M_W are vector bundles, and the graded Betti numbers b_(i,j)(W) = dim Tor_i^U(k, M_W)_j, computed
from the finite free resolution of the trivial module tensored with M_W, are upper semicontinuous on V. Only the
finitely many (i, j) with i <= 3 and j <= 4e can be nonzero on V, since M_W vanishes from degree 4e - 3 on. For W in V
the Betti numbers are at least those of the pure table: M_W has one generator, in degree 0, and two minimal
relations, in degree e (automatic for W of dimension 2); the trivial module has a resolution of length 3; and the
Hilbert series fixes the alternating sums, so b_(2,j) - b_(3,j) is 2 for j = 3e, -1 for j = 4e and 0 otherwise, which
gives b_(2,3e) >= 2, b_(3,4e) >= 1. At W_1 the Betti numbers are those of the pure table, so by semicontinuity they
are on a neighbourhood of W_1 in V. That neighbourhood lies in P_e.

(c) follows from (a) and (b): the components of P_e are its nonempty intersections with the components of D_e, each
open in its component.

(d) The graded automorphisms of U are GL_2 acting on U_1 (the relations [x,[x,y]] = [y,[x,y]] = 0 span a stable
space), with z going to det(g) z; the scalars act on U_e by a scalar, hence trivially on G_e. A twist by a graded
automorphism preserves Betti tables, so P_e is stable and the orbit of W_0 lies in P_e. The stabilizer of W_0 in PGL_2
contains the diagonal torus, and W_0 determines the pair of points {x = 0}, {y = 0} of the projective line: the
coefficient of the PBW monomial x^(e-1) y in (a x + b y)^e (equivalently, in its image in U/(z) = k[x, y]) is
e a^(e-1) b, and that of x y^(e-1) is e a b^(e-1), so l^e lies in W_0 only for l a multiple of x or of y, in
characteristic 0 or larger than e. So the stabilizer has dimension 1 and the orbit, the set of unordered pairs of
distinct points, has dimension 2. (In characteristic p = e every line has its e-th power in W_0; the hypothesis of (d)
excludes that case.)

## Remarks

- For e = 2 and e = 3, h_e(3e) = 0 and D_e = G_e: the pure Hilbert function equals the maximal-rank function
  max(0, u(n) - 2 u(n-e)) and P_e is open in G_e (it is empty in characteristic 2 by Theorem C). For e >= 4 the two
  functions differ exactly in the degrees 3e to 4e - 4.
- D_e is not of the expected codimension for e >= 4 (found by the review; the first text of this note and derivation 3
  of the hypothesis of EXP-006 said that the class of D_4 in the Chow ring of Gr(2, 9) is 300 sigma_2 + 325 sigma_(1,1),
  which is false). If the images of a basis of W in U/(z) = k[x, y] share a factor q of degree d, then M_W maps onto
  k[x, y]/(q), of dimension d in every degree from d - 1 on, so rank mu_(3e)(W) <= u(3e) - d. With d = h_e(3e) this puts
  the common-factor locus R_e inside D_e; R_e has codimension h_e(3e) in G_e, less than 2 h_e(3e), and its modules have
  infinite length, so it contains no pure point. At e = 4 it is the resultant hypersurface. So D_e is not of the
  expected codimension, it is not empty in any characteristic, and a random W over GF(q) lies in D_4 with probability
  about 1/q, not q^(-2). D_e is reducible at e = 4 whenever it has a pure point (then D_4 is a proper closed set, of
  dimension at most 13, that contains the irreducible hypersurface R_4 and a point outside it), and for e = 4 to 7
  over the rationals, where the component through W_0 has dimension 4e - 4, less than the dimension of R_e
  (EXP-007); for e >= 8 reducibility is not shown. (The first reviewed text said "D_e is reducible" for every
  e >= 4; the review of the manuscript v0.02 pointed out that this does not follow, record
  `bs-manuscript-v002-review-2026-11-20`, finding M2.) None of (a) to (d) is affected: W_0 is not in R_e, since x^e
  and y^e are coprime.
- The statement says nothing about odd characteristic below 2e: there P_e is open in D_e as well, but no pure point is
  known in advance. EXP-006 looks for one over small fields.
- A count over a finite field tests (c): if a component of P_4 of dimension 12 is defined over GF(q) and geometrically
  irreducible, a random W over GF(q) is pure with probability about q^(-2) (Lang and Weil). The control family B2 of
  EXP-006 (GF(11) and GF(13)) measures that share.
- Not claimed in the statement: irreducibility of P_e or of D_e, the exact dimension, smoothness.

## Supplements reported by the review (computed with the repository's instrument in a scratch run; to be archived by an experiment before a manuscript states them)

- The tangent space of D_e at W_0 has dimension exactly 4e - 4 over QQ for e = 4, 5, 6, 7. If so, D_e and P_e are
  smooth of dimension 4e - 4 at W_0 in characteristic 0, the component of P_e through W_0 is unique and the bound of (c)
  is attained there. The dimension is larger in some positive characteristics at least 2e (22 over GF(13) at e = 6,
  26 over GF(17) at e = 7).
- Explicit pure pairs over QQ outside the orbit of W_0: <x^4 + x y^3, y^4>, <x^4 + 31 x^2 y^2 - 8 x y z, y^4>,
  <x^4 + 59 x^2 y^2 - 4 z^2, y^4>, <x^4 + 2 x y^3 - 3 y^2 z, y^4 + 5 x^3 y + 7 x^2 z>, and at e = 5
  <x^5 + 2 x y^4 - 3 y^3 z, y^5 + 5 x^4 y + 7 x^3 z>. A weight argument for the diagonal torus puts the linear family
  <x^e + a x y^(e-1) + b y^(e-2) z, y^e + c x^(e-1) y + d x^(e-2) z> inside D_e at e = 4, 5, and its general member is
  pure.
- These rest on one instrument and on scripts that were deleted with the review's scratch folder. Backlog BSB-025
  archives them with a second instrument.
