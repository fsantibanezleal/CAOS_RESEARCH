# Pull-back along an endomorphism: in characteristic p the realized Betti tables are closed under multiplying the degrees by d = 0 or 1 modulo p

Date: 2026-11-21. Status: derivation [D] by the coordinating session, not yet read by a reviewer. It rests on the
criterion note `2026-11-20-central-commutator-criterion.md` (under review) and on the note
`2026-11-21-endomorphisms-and-the-explicit-complex.md`. EXP-013 (frozen the same day) checks it by machine.

## Setting

k is a field of characteristic p >= 3, U = U(H), left modules unless said. Let (f, g) be a pure pair of forms of
degree d whose commutator c = g f - f g is central, for example one of the pairs of the corollary of the criterion
note (d >= 3, d = 0 or 1 modulo p). Let phi be the endomorphism of U with phi(x) = f, phi(y) = g (endomorphism note,
proposition 2); it multiplies degrees by d and phi(z) = f g - g f = - c.

Write U_phi for U as a right U-module through phi: u . a = u phi(a). With the grading of the acting copy of U
multiplied by d (call it U', with x, y in degree d and z in degree 2d), U_phi is a graded right U'-module, zero in
negative degrees, and U' is connected graded.

For a graded left U-module M' put phi^* M' = U_phi tensor_U M'. If M' = U^m / (the rows of a matrix R) then
phi^* M' = U^m / (the rows of phi(R)), where phi is applied to every entry.

## Statements

Proposition 1 (freeness). U_phi is a free right U-module of rank d^3, and phi is injective.

Proof. Let P be the minimal free resolution of the trivial left module k. By proposition 2 of the endomorphism note,
U_phi tensor_U P is the explicit complex of the pair (f, g), which is exact in positive homological degrees because
the pair is pure (it is the minimal resolution of M = U/(Uf + Ug)). So Tor_i^U(U_phi, k) = 0 for i >= 1, and
U_phi tensor_U k = M has dimension d^3. Now the graded Nakayama lemma: choose homogeneous elements n_1, ..., n_r of
U_phi whose classes form a basis of U_phi tensor k = U_phi / U_phi U'_+ (r = d^3). They generate U_phi as a right
U'-module, because U_phi is zero in negative degrees. Let G be the free right module on them and K the kernel of
G -> U_phi. The sequence Tor_1(U_phi, k) -> K tensor k -> G tensor k -> U_phi tensor k has its first term zero and its
last map an isomorphism, so K tensor k = 0, and K = 0 because K is zero in negative degrees. If phi(a) = 0 then a
kills the free module U_phi, so a = 0. QED.

Theorem (scaling). Let M' be a finitely generated graded left U-module with minimal free resolution P', with
Betti numbers beta_(i, a)(M'). Then U_phi tensor_U P' is a minimal free resolution of phi^* M' over U, so

    beta_(i, d a)(phi^* M') = beta_(i, a)(M')   for all i and a,   and all other Betti numbers of phi^* M' are 0.

If M' has finite length l, then phi^* M' has finite length d^3 l.

Proof. U_phi is free, hence flat, as a right U-module, so U_phi tensor_U P' is exact in positive degrees with
cokernel phi^* M'. The term U_phi tensor_U U(-a) is the free left U-module on a generator of degree d a, and the maps
are given by the matrices phi(R_i), whose entries lie in the augmentation ideal because those of R_i do. So the
resolution is minimal. The Hilbert series of phi^* M' is that of M' in the variable t^d times
H_U(t) / H_U(t^d) = (1 - t^d)^2 (1 - t^(2d)) / ((1 - t)^2 (1 - t^2)), a polynomial with value d^3 at t = 1. QED.

Corollary 1 (the point (1, 2, 2, 1)). Let E_p be the set of e >= 1 such that the point (1, 2, 2, 1) of
(0, e, 3e, 4e) is realized over U in characteristic p. If e' is in E_p and d >= 3 with d = 0 or 1 modulo p, then
d e' is in E_p. If (f', g') is a pure pair of degree e' then (phi(f'), phi(g')) is a pure pair of degree d e'.

Proof. The corollary of the criterion note gives a pure pair of degree d with central commutator over the prime
field, hence over every field of characteristic p, and the theorem applies to M' = U/(Uf' + Ug') after extending
the field. QED.

Examples of pairs (e, p) that this adds to those with p dividing e(e - 1): (8, 3) = 4 . 2 and (14, 3) = 7 . 2, from
the pure pair of quadrics over GF(3) of EXP-003; (12, 5) = 6 . 2, (16, 7) = 8 . 2 and (24, 7) = 8 . 3, from the power
pairs of degree 2 and 3, which are pure in characteristic at least 2e' (Theorem A); (18, 5) = 6 . 3 and
(20, 3) = 4 . 5, from the pure pairs of degree 3 over GF(5) and of degree 5 over GF(3) of EXP-006. A prime e that is
not 0 or 1 modulo p is not reached: (7, 5) and (11, 3) stay open, and so does (6, 7), because 6 has no divisor at
least 3 that is 0 or 1 modulo 7.

Corollary 2 (every table). If a Betti table is realized by a graded U-module of finite length over a field of
characteristic p >= 3, then so is the table with all degrees multiplied by d, for every d >= 3 with d = 0 or 1 modulo
p. On a pure ray the primitive point does not change when the degree sequence is multiplied by d, so the
realizability of the primitive point, or of a given multiple of it, passes from the degree sequence
(d_0, d_1, d_2, d_3) to (d d_0, d d_1, d d_2, d d_3).

Corollary 3 (which d). For d >= 2 and a field of characteristic p >= 3 the following are equivalent: (i) U has a
graded endomorphism of degree d over which it is a free right module of finite rank; (ii) there is a pure pair of
degree d with central commutator; (iii) p divides d (d - 1). In characteristic 0 there is no such endomorphism for
d >= 2.

Proof. (i) implies (ii): for such phi the pair (phi(x), phi(y)) has its commutator commuting with it, hence central
(endomorphism note, proposition 3), and Tor_i(U_phi, k) = 0 with U_phi tensor k of finite dimension, so the pair is
pure (proposition 2 there). (ii) implies (i) is proposition 1. (ii) implies (iii) is the corollary of the
endomorphism note, part (ii); (iii) implies (ii) is the corollary of the criterion note. Characteristic 0: the
corollary of the endomorphism note, part (i). QED.

## Remarks

1. Over the polynomial ring k[x, y, z] every d works, in every characteristic: x_i -> x_i^d makes the ring free over
   itself, and this is how degree sequences are rescaled there. Over U the same operation exists only in
   characteristic p and only for d = 0 or 1 modulo p; this is one more way in which the realizability over U depends
   on the characteristic.
2. Compositions of the endomorphisms have degrees that are again 0 or 1 modulo p, as they must by corollary 3.
3. The theorem needs no hypothesis on M'. It does not say that phi^* M' is a new module up to the symmetries of U;
   only its Betti table is claimed.

## How could this be wrong?

- Proposition 1 uses the Nakayama lemma for graded modules that vanish in negative degrees over a connected graded
  algebra, and the identification of U_phi tensor P with the explicit complex (the left-right conventions: U_phi is a
  right module through phi and a left module by multiplication; the complex consists of left modules).
- The theorem inherits everything from the criterion note: if that note has a gap, the pairs to which the theorem
  applies are only those whose purity is machine-checked, and the statement for every d = 0 or 1 modulo p falls back
  to those d.
- Corollary 1 in the examples uses pure pairs from experiments ((2, 3) from EXP-003, (5, 3) from EXP-006) and from
  Theorem A; each example is a prediction that EXP-013 tests for (8, 3), (12, 5) and (16, 7).
