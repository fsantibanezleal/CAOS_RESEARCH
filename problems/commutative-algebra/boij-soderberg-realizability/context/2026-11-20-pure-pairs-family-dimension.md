# The pure pairs of forms of degree e form a family of dimension at least 2 u(e) - 4 - 2 h_e(3e) through <x^e, y^e>

Date: 2026-11-20. Status: derivation [D], written after the hypothesis of EXP-006 was frozen and before any of its
results was read; not yet reviewed by a reader other than the writer. Nothing here is used in a manuscript before that
review.

## Setting

U = U(H) over a field k, u(n) = dim U_n = floor((n + 2)^2 / 4). For e >= 2 let G_e = Gr(2, U_e), of dimension
2 (u(e) - 2). For W in G_e put M_W = U / (U W), a cyclic left module with two relations of degree e, and let
mu_n(W): U_(n-e) tensor W to U_n be left multiplication, so that H_W(n) = dim (M_W)_n = u(n) - rank mu_n(W). The
Hilbert function of the pure table (1, 2, 2, 1) on (0, e, 3e, 4e) is
h_e(n) = u(n) - 2 u(n-e) + 2 u(n-3e) - u(n-4e). Call W pure when M_W has that Betti table, and let P_e be the set of
pure W.

Two values: h_e(3e) = u(3e) - 2 u(2e) + 2 equals ((e - 2) / 2)^2 for e even and (e - 1)(e - 3) / 4 for e odd (0, 0,
1, 2, 4, 6 for e = 2, ..., 7).

## Statement

Let e >= 2 and let k be algebraically closed. Put r = 2 u(2e) - 2 and
D_e = {W in G_e : rank mu_(3e)(W) <= r}.

(a) Every irreducible component of D_e has codimension at most 2 h_e(3e) in G_e.

(b) P_e is contained in D_e and is open in D_e.

(c) Hence every irreducible component of P_e has dimension at least 2 u(e) - 4 - 2 h_e(3e): 4 and 8 for e = 2, 3
(where P_e is open in G_e), and 12, 16, 20, 24 for e = 4, 5, 6, 7.

(d) If the characteristic of k is 0 or at least 2e, then P_e is not empty: it contains W_0 = <x^e, y^e> (Theorem A
of the manuscript). The orbit of W_0 under the automorphisms of H that act on G_e (the group PGL_2 acting on x, y;
the scalars act trivially on G_e) has dimension 2. So for e >= 4 the pure cyclic modules on the ray (0, e, 3e, 4e) form
a family of dimension at least 12 in which the modules of the published family U/U(l_1^e, l_2^e) are a subfamily of
dimension 2: up to automorphism there are at least 9 parameters of pure modules at e = 4, and at least
2 u(e) - 7 - 2 h_e(3e) in general.

## Proof

(a) On G_e let S be the tautological subbundle of rank 2. Left multiplication is a map of vector bundles
mu_(3e): U_(2e) tensor S to U_(3e) tensor O, of ranks 2 u(2e) and u(3e). D_e is its locus of rank at most r. Since
h_e(3e) >= 0, r <= u(3e), and each component of a locus of rank at most r of a map between bundles of ranks m and n
has codimension at most (m - r)(n - r) (for example Fulton, Intersection Theory, Theorem 14.4 (b)). Here
(m - r)(n - r) = 2 (u(3e) - 2 u(2e) + 2) = 2 h_e(3e).

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
nu_n(W_1) is the third syzygy, of dimension u(n-4e).

On V the image of nu_n(W) lies in the kernel of mu_n(W), so
rank mu_n(W) <= 2 u(n-e) - (2 u(n-3e) - u(n-4e)) = u(n) - h_e(n) for 3e < n <= 4e + 1; with 3 this is an equality.
So H_W(n) = h_e(n) for every n <= 4e + 1. Since h_e(n) = 0 for n >= 4e - 3 and M_W is generated in degree 0, M_W
vanishes from degree 4e - 3 on, and H_W = h_e.

So V is a neighbourhood of W_1 in D_e on which the Hilbert function is constant. Over V with its reduced structure the
graded pieces of M_W are vector bundles, and the graded Betti numbers b_(i,j)(W) = dim Tor_i^U(k, M_W)_j, computed
from the finite free resolution of the trivial module tensored with M_W, are upper semicontinuous on V. For W in V
the Betti numbers are at least those of the pure table: M_W has one generator, in degree 0, and two minimal
relations, in degree e; U has global dimension 3; and the Hilbert series fixes the alternating sums, so
b_(2,j) - b_(3,j) is 2 for j = 3e, -1 for j = 4e and 0 otherwise, which gives b_(2,3e) >= 2, b_(3,4e) >= 1. At W_1
the Betti numbers are those of the pure table, so by semicontinuity they are on a neighbourhood of W_1 in V. That
neighbourhood lies in P_e.

(c) follows from (a) and (b): a component of P_e is open in a component of D_e.

(d) The stabilizer of W_0 in PGL_2 contains the diagonal torus, and W_0 determines the pair of points {x = 0}, {y = 0}
of the projective line (the linear forms whose e-th power lies in W_0: the coefficient of x^(e-1) y in (a x + b y)^e
is e a^(e-1) b, not zero unless a b = 0, in characteristic 0 or larger than e), so the stabilizer has dimension 1 and
the orbit, the set of unordered pairs of distinct points, has dimension 2.

## Remarks

- For e = 2 and e = 3, h_e(3e) = 0 and D_e = G_e: the pure Hilbert function is the generic one and P_e is open in G_e
  (it is empty in characteristic 2 by Theorem C).
- The statement says nothing about odd characteristic below 2e: there P_e is open in D_e as well, and D_e is not empty
  (for e = 4 its class in the Chow ring of Gr(2, 9) is 300 sigma_2 + 325 sigma_(1,1), hypothesis of EXP-006), but no
  pure point is known in advance. EXP-006 looks for one over small fields.
- A count over a finite field tests (c): if a component of P_4 of dimension 12 is defined over GF(q) and geometrically
  irreducible, a random W over GF(q) is pure with probability about q^(-2) (Lang and Weil). The control family B2 of
  EXP-006 (GF(11) and GF(13)) measures that share.
- An explicit pure pair over QQ outside the orbit of W_0 would make (d) concrete at e = 4; none is written here.
- Not claimed: irreducibility of P_e or of D_e, the exact dimension, smoothness.
