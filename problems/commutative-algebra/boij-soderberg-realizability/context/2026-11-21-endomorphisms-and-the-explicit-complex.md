# The explicit complex comes from an endomorphism of U, and it exists only for a central commutator

Date: 2026-11-21. Status: derivation [D] by the coordinating session, not yet read by a reviewer. It says what the
mechanism of the notes `2026-11-20-central-pair-theorem.md` and `2026-11-20-central-commutator-criterion.md` is, and
why it cannot reach the characteristics that do not divide e(e - 1). No experiment depends on it.

## Setting

Notation of those notes: U = U(H) over a field k, yx = xy - z, left modules, f, g forms of degree e >= 1,
c = g f - f g, and the sequence

    0 -> U(-4e) -> U(-3e)^2 -> U(-e)^2 -> U,
    1 -> (g, f);   (1, 0) -> s_1 = (c - f g, f^2),  (0, 1) -> s_2 = (g^2, -(g f + c));   (1, 0) -> f,  (0, 1) -> g.

## Statements

Proposition 1 (when the sequence is a complex). The three compositions are

    s_1 . (f, g) = c f - f c,     s_2 . (f, g) = g c - c g,     g s_1 + f s_2 = (g c - c g,  c f - f c).

So the sequence is a complex if and only if c commutes with f and with g.

Proof. (c - f g) f + f^2 g = c f - f (g f - f g) = c f - f c. g^2 f - (g f + c) g = g (g f - f g) - c g = g c - c g.
g (c - f g) + f g^2 = g c - (g f - f g) g = g c - c g, and g f^2 - f (g f + c) = (g f - f g) f - f c = c f - f c. QED.

Proposition 2 (endomorphisms). U is the algebra on x, y with the relations [x, [x, y]] = [y, [x, y]] = 0. So the
forms f, g of degree e with c commuting with f and g are exactly the pairs (phi(x), phi(y)) for the algebra
endomorphisms phi of U that multiply degrees by e; then phi(z) = f g - g f = - c. For such a pair the complex above is
the base change U_phi tensor_U P of the minimal free resolution P of the trivial module k = U/(Ux + Uy), where U_phi
is U as a right U-module through phi. Consequently its homology is Tor^U(U_phi, k), and the pair (f, g) is pure if
and only if Tor_i^U(U_phi, k) = 0 for i = 1, 2, 3.

Proof. The presentation of U is the definition of the enveloping algebra of the Heisenberg algebra (the free Lie
algebra on x, y modulo brackets of length 3). An endomorphism is determined by the images f, g of x, y, and these
must satisfy the two relations, that is, [f, g] commutes with f and g. The trivial module has the minimal resolution

    0 -> U(-4) -> U(-3)^2 -> U(-1)^2 -> U -> k -> 0,
    1 -> (y, x);   (1, 0) -> (-z - x y, x^2),  (0, 1) -> (y^2, -(y x - z));   (1, 0) -> x,  (0, 1) -> y,

which is the sequence above for (f, g) = (x, y), where c = y x - x y = - z. (It is the Chevalley-Eilenberg resolution
of k, of ranks 1, 3, 3, 1, after cancelling the generator z of degree 2 against the relation x y - y x - z.) Applying
phi to every entry gives the sequence for (f, g): phi(-z - x y) = c - f g and phi(y x - z) = g f + c. If the
higher Tor vanish, the complex is a minimal resolution of M = U_phi tensor_U k = U/(Uf + Ug) with the Betti table
(1, 2, 2, 1) on (0, e, 3e, 4e); conversely a pure pair of this kind has an exact complex. QED.

So a pure pair of this kind is the pull-back of the trivial module along an endomorphism of U.

Proposition 3 (central or nothing). Let c = g f - f g be nonzero and commute with f and g. Then c is central in U.

Proof. In both cases the claim is that the centralizer of a non-central element is commutative; then f and g, which
lie in the centralizer of c, commute, and c = 0.
- Characteristic p > 0. Let Z = k[x^p, y^p, z] and K its field of fractions. U is a domain and a free Z-module of
  rank p^2, so Q = U tensor_Z K is a division algebra of dimension p^2 over K. Its centre L contains K, and
  p^2 = [Q : L][L : K] with [Q : L] a square; [Q : L] = 1 is impossible because Q is not commutative; so L = K and Q
  has degree p. A non-central element c generates a subfield K(c) of degree p over K, a maximal subfield, which is
  its own centralizer.
- Characteristic 0. U embeds in the Weyl algebra A_1 over the field k(z) (x, and d = y/z with [x, d] = 1), in which
  the centralizer of an element outside the centre k(z) is commutative (Amitsur; Dixmier). QED.

Corollary. (i) In characteristic 0 the centre of U is k[z]. If c is not zero then c = lambda z^e, and by remark 4 of
the central pair note this is impossible for a pair of finite length with e >= 2. If c = 0, the Jacobian
determinant of the images of f, g vanishes, which by the Euler relations of that remark is impossible for two forms
of degree e >= 2 without common factor. So in characteristic 0 no pure pair of degree e >= 2 has the explicit
complex as its resolution, and no endomorphism of U of degree e >= 2 pulls the trivial module back to a module of
finite length.

(ii) In characteristic p >= 3, c lies in Z. If moreover the pair has finite length, then p divides e(e - 1): c lies
in zU and in Z, so c = z c' with c' in Z of degree 2e - 2; modulo z, c' is a polynomial in x^p, y^p of degree 2e - 2
in x, y, and it is the Jacobian determinant of the images of g, f up to sign; if it is not zero then p divides
2e - 2, and if it is zero then p divides e (central pair note, remark 4, the Euler relations; the images have no
common factor because the pair has finite length).

(iii) So for p not dividing e(e - 1) the two syzygies of degree 3e of a pure pair are not s_1, s_2, and the
commutator of a pure pair does not commute with the pair. The pure pairs found there by search (for example over
GF(7) at e = 5) are of another kind.

## Remarks

1. The class V_e of the criterion note is not every pair with a central commutator: f = P(x) + delta y and
   g = B + beta x, with B, beta, delta central and P any polynomial in x with central coefficients, have
   g f - f g = beta delta z. The criterion is proved for V_e only. By (ii) no pair of this wider kind reaches a new
   pair (e, p).
2. In characteristic p the endomorphisms of the corollary of the criterion note are, for e = p, of the shape
   x -> x^p + (central) y, y -> y^p + (central) x: a twist of the p-th power map, which is not itself an endomorphism
   of finite colength because x^p and y^p commute.

## How could this be wrong?

- Proposition 3 in characteristic 0 rests on a cited theorem on centralizers in the first Weyl algebra over a field
  of characteristic 0; the reviewer should check the statement used (centralizer of a non-central element of A_1(F),
  F = k(z), is commutative) against a source and that U embeds as said.
- In characteristic p it rests on Q being a division algebra of degree p with centre K; the count of dimensions
  assumes that the dimension of a central simple algebra over its centre is a square.
- Proposition 2 uses the minimal resolution of k over U; its exactness is classical and is also the case e = 1 of
  the machine checks (the module k).
