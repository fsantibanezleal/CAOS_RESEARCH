# Pure pairs in characteristic p dividing an odd e: central forms, a commutator equal to a power of z, and an explicit resolution

Date: 2026-11-20. Status: derivation [D] by the coordinating session. Reviewed on 2026-11-20 by a reader other than
the writer (record `bs-central-pair-theorem-review-2026-11-20` in the coordination repository): every step holds, the
left-module conventions are consistent, no blocker and no major finding; nine minor repairs of wording and of missing
justifications, applied below (the first text is in commit 96578874). The review also checked six cases inside the
hypotheses on (3, 3), (5, 5), (7, 7), (9, 3), with A, B other than x^e, y^e and l_1, l_2 other than y, x, and six
outside them, and found no statement of the theorem in five literature searches (a search, not a claim of novelty).
Machine checks by the coordinating session: the identities, the length and the Betti table at (e, p) = (3, 3) and (5,
5) for three choices of the parameters. EXP-011 checks more cases with two instruments. The note
`2026-11-20-central-commutator-criterion.md` generalizes the statement by another proof.

## Setting

Notation of the note `2026-11-20-pure-pairs-family-dimension.md`: U = U(H) over a field k, PBW monomials x^a y^b z^c
with yx = xy - z (so [x, y] = z is central), deg x = deg y = 1, deg z = 2, H_U(t) = 1/((1 - t)^2 (1 - t^2)) the Hilbert
series of U, u(n) = dim U_n, h_e(n) = u(n) - 2 u(n - e) + 2 u(n - 3e) - u(n - 4e). Modules are left modules; a map
between free modules is written by its values on the basis. A pair of forms f, g of degree e is pure when
M = U/(Uf + Ug) has the Betti table (1, 2, 2, 1) on the degrees (0, e, 3e, 4e).

Facts used, each elementary:

- (F1) U is a domain, z is central, and U/zU is the polynomial ring k[x, y]. (By the PBW theorem the associated graded
  algebra of U for the filtration by the degree in x and y is the polynomial ring k[x, y, z], a domain, so U is one;
  and U/zU is the enveloping algebra of the abelian Lie algebra H/kz.) Write a bar for the image in k[x, y].
- (F2) y x^n = x^n y - n x^(n-1) z and x y^n = y^n x + n y^(n-1) z. So if k has characteristic p > 0 and p divides n,
  then x^n and y^n are central in U, and so is every polynomial in x^p, y^p and z.
- (F3) For l_1 = a_1 x + b_1 y and l_2 = c_1 x + d_1 y in U_1, [l_2, l_1] = (b_1 c_1 - a_1 d_1) z. It is not zero
  exactly when l_1, l_2 are linearly independent.

## Statement

Theorem. Let k be a field of characteristic p > 0, let e be an odd multiple of p (so p is odd and e >= 3), and put
s = (e - 1)/2. Let A = A_0(x^p, y^p) and B = B_0(x^p, y^p) with A_0, B_0 forms of degree e/p in two variables (as
elements of U they are polynomials in the central elements x^p and y^p, of degree e) whose images in k[x, y] have no
common factor, and let l_1, l_2 in U_1 be linearly independent.
Put

    f = A + z^s l_1,    g = B + z^s l_2,    lambda z = [l_2, l_1]   (lambda in k, not zero).

Then:

(a) g f - f g = lambda z^e. In particular z^e lies in the left ideal I = Uf + Ug.

(b) M = U/I has finite length e^3 and Hilbert function h_e.

(c) The complex

    0 -> U(-4e) -> U(-3e)^2 -> U(-e)^2 -> U -> M -> 0

with the maps 1 -> (g, f);  (1, 0) -> s_1 = (lambda z^e - f g, f^2),  (0, 1) -> s_2 = (g^2, -(g f + lambda z^e));
(1, 0) -> f, (0, 1) -> g, is a minimal free resolution of M. So (f, g) is a pure pair.

Corollary. Over the enveloping algebra of the Heisenberg Lie algebra, the point (1, 2, 2, 1) of the degree sequence
(0, e, 3e, 4e) is realized in characteristic p for every odd e and every prime p dividing e. In particular it is
realized on (0, p, 3p, 4p) in characteristic p for every odd prime p, for example by

    f = x^p + y z^((p-1)/2),    g = y^p + x z^((p-1)/2).

The theorem alone settles e = 7 in characteristic 7 and e = 9 in characteristic 3, both open before; e = 3 in
characteristic 3 and e = 5 in characteristic 5 were known from explicit pairs found by search (EXP-006, EXP-008).
After this note alone, e = 7 stays open in characteristics 3 and 5 and e = 9 in the odd characteristics below 18
other than 3 (the note `2026-11-20-central-commutator-criterion.md` then covers e = 7 in characteristic 3).

Addition (review). The proof uses three things about A and B: they are central, they have degree e, and their
images in k[x, y] have no common factor. So the theorem holds verbatim for A, B in the part of degree e of
k[x^p, y^p, z], for example A = x^9 + z^3 x^3 at (e, p) = (9, 3) (checked by the review: length 729, pure table).

## Proof

(a) A and B are central by (F2), and z^s is central. So

    g f - f g = [B + z^s l_2, A + z^s l_1] = z^(2s) [l_2, l_1] = lambda z^(2s + 1) = lambda z^e.

Since g f lies in Uf and f g in Ug, lambda z^e lies in I, and lambda is not zero by (F3). Write c = lambda z^e.

(b), upper bound. Let F_j be the span of the PBW monomials x^a y^b z^c with a + b <= j. A product of two monomials is
a combination of monomials x^(a+a'-i) y^(b+b'-i) z^(c+c'+i), so F_j F_j' lies in F_(j+j'); each F_j is a graded
subspace; and [x, y] = z lies in F_0. So F is a filtration of the graded algebra U whose associated graded algebra is
the commutative polynomial ring k[x, y, z], graded by the total degree with deg z = 2. For the left ideal I, gr I is
an ideal of k[x, y, z] and dim (U/I)_n = dim (k[x, y, z]/gr I)_n for every n (each U_n is finite dimensional and the
filtration is finite on it). The symbols of f, g and c are A-bar, B-bar (of filtration degree e, since z^s l_1 and
z^s l_2 lie in F_1 and e > 1) and lambda z^e (of filtration degree 0). So gr I contains (A-bar, B-bar, z^e). This is a
regular sequence in k[x, y, z]: A-bar, B-bar are forms in x, y without a common factor, and z^e is regular on
(k[x, y]/(A-bar, B-bar))[z]. Its degrees are e, e, 2e, so

    sum_n dim M_n t^n  <=  (1 - t^e)^2 (1 - t^(2e)) H_U(t)  =  (1 - 2 t^e + 2 t^(3e) - t^(4e)) H_U(t)  =  sum_n h_e(n) t^n

coefficient by coefficient.

(c), the complex. With c = g f - f g central:

    (c - f g) f + f^2 g = c f - f (g f - f g) = c f - f c = 0,
    g^2 f - (g f + c) g = g (g f - f g) - c g = g c - c g = 0,
    g s_1 + f s_2 = (g c - (g f - f g) g,  (g f - f g) f - f c) = (g c - c g,  c f - f c) = (0, 0).

So the maps compose to zero. Every entry has positive degree.

The kernel Z_2 of U(-3e)^2 -> U(-e)^2 is U (g, f). Let (v, w) satisfy v s_1 + w s_2 = 0 and put t = v f - w g. The
first component gives v c = v f g - w g^2 = t g; the second gives w c = v f^2 - w g f = t f. Now c = lambda z^e. By
(F1), if z divides a product t g then it divides t, because g-bar = B-bar (here s >= 1, so z^s l_2 lies in zU) is not
zero in the domain k[x, y]; write
t = z t_1 and cancel z from z t_1 g = lambda z^e v (U is a domain and z is central), getting t_1 g = lambda z^(e-1) v.
Repeating e times, t = z^e t_e with t_e g = lambda v. The same division in t f = c w gives t_e f = lambda w. So
(v, w) = (t_e / lambda)(g, f). Conversely U (g, f) lies in Z_2, and u -> (u g, u f) is injective because U is a domain.
So the Hilbert series of Z_2 is t^(4e) H_U, and the image B_1 of U(-3e)^2 in U(-e)^2 has Hilbert series
(2 t^(3e) - t^(4e)) H_U.

(b), lower bound, and exactness. Let Z_1 be the kernel of U(-e)^2 -> U, so that the Hilbert series of I is
2 t^e H_U minus that of Z_1. B_1 lies in Z_1, so the series of Z_1 is at least (2 t^(3e) - t^(4e)) H_U, and

    sum_n dim M_n t^n  =  H_U - (series of I)  >=  (1 - 2 t^e + 2 t^(3e) - t^(4e)) H_U

coefficient by coefficient. With the upper bound this is an equality, which is (b); the length is the value at t = 1
of (1 - t^e)^2 (1 - t^(2e)) / ((1 - t)^2 (1 - t^2)), that is e^3. Equality also gives that Z_1 and B_1 have the same
Hilbert series, so B_1 = Z_1. The complex is then exact at every place, and it is minimal because no entry is a
nonzero constant. QED.

## Remarks

1. The mechanism. M has the Hilbert series of a complete intersection of type (e, e, 2e) in k[x, y, z]. Over the
   polynomial ring such a quotient needs three relations and has the Betti table (1, 3, 3, 1). Over U the third
   relation, z^e, is the commutator of the first two, so it costs no generator, and the Koszul relation between f and
   g of degree 2e is lost with it; what is left is (1, 2, 2, 1) on (0, e, 3e, 4e).

2. The family. The pairs of the theorem as first stated (A, B without terms in z) form a family: A, B run over the
   pairs of forms of degree e/p in x^p, y^p without common factor, l_1, l_2 over the bases of U_1. A change of basis
   of the plane <f, g> acts on (A, B) and on (l_1, l_2) by the same matrix, so the planes form a family of dimension 2
   (e/p + 1) + 4 - 4 = 2 e/p + 2 in G_e. For e = p it has dimension 4.

3. Where the pairs sit among the weight-class strata (note `2026-11-20-weight-class-strata.md`). With A = x^e, B = y^e,
   l_1 = b y, l_2 = d x (b, d not zero) the forms f = x^e + b y z^s and g = y^e + d x z^s have weights {0, s + 1} and
   {e, s}, so the pair
   lies in S(m; 0, e mod m) for every m dividing s + 1 = (e + 1)/2: S(2; 0, 1) for e = 3, S(3; 0, 2) for e = 5,
   S(4; 0, 3) and S(2; 0, 1) for e = 7. These strata are admissible, as they must be.

4. The mechanism needs p to divide e. Suppose f, g in U_e have images without common factor in k[x, y] and z^e lies in
   Uf + Ug; taking homogeneous components, z^e = a f + a' g with a, a' in U_e. Reducing modulo z, a-bar f-bar + a'-bar
   g-bar = 0, and the syzygies of two forms without common factor are the multiples of (g-bar, -f-bar), so (a-bar,
   a'-bar) = q (g-bar, -f-bar) with q in k. q is not zero: otherwise a = z a_1, a' = z a_1' and a_1 f + a_1' g =
   z^(e-1) with a_1, a_1' of degree e - 2 < e, which modulo z forces a_1-bar = a_1'-bar = 0, and the descent continues
   until the degree of the coefficients is 1 or 0 and a power of z would be 0. So a = q g + z a_1, a' = -q f + z a_1',
   and q [g, f] + z (a_1 f + a_1' g) = z^e. The commutator [g, f] lies in zU, and (u-bar, v-bar) -> ([u, v]/z)-bar is
   a biderivation of k[x, y] with value 1 on (x, y), so it is the Jacobian determinant in every characteristic.
   Dividing by z and reducing modulo z (e >= 2): the Jacobian J of f-bar, g-bar lies in the ideal (f-bar, g-bar).

   That forces p to divide e, by the Euler relations (review). Let F, G be forms of degree e >= 2 without common
   factor and suppose e is not zero in k. Then x J = e (F G_y - F_y G) and y J = e (F_x G - F G_x). If J = alpha F +
   beta G with alpha, beta of degree e - 2, then (x alpha - e G_y) F + (x beta + e F_y) G = 0 is a syzygy of degree e
   - 1 < e, hence zero: x alpha = e G_y and x beta = - e F_y; in the same way y alpha = - e G_x and y beta = e F_x.
   Then e^2 G = e (x G_x + y G_y) = - x y alpha + y x alpha = 0, so G = 0, a contradiction.

   So a pair with images free of common factors and z^e in its ideal exists only in characteristic p dividing e
   (purity is not used). The power pair in characteristic 0 is pure without it: there z^e is not in U x^e + U y^e. The
   condition is far from sufficient: the review found z^e outside the ideal for random pairs at (3, 3) and (5, 5). (A
   sharper classical statement: J = e^2 s, where s is the socle element of k[x, y]/(F, G) of residue 1, by the trace
   formula of Scheja and Storch; the review confirmed it numerically on 475 pairs and did not open the primary source.
   It is not used here.)

5. Even e. For even e divisible by p the same construction, f = A + C l_1 and g = B + C l_2 with C central of odd
   degree e - 1, has the commutator lambda C^2 z, and the upper bound needs a pure power of z in it; a central form of
   odd degree has no term that is a power of z. The review checked one such pair at (6, 3): the identities of the
   complex hold and the module is not of finite length. Nothing is claimed here for even e; the note
   `2026-11-20-central-commutator-criterion.md` treats it with other pairs.

## How could this be wrong?

- Step (b), upper bound, uses that gr I contains the symbols of three elements of I and that these form a regular
  sequence; the inequality of Hilbert functions is then for gr I at least that ideal. The reviewer should check the
  filtration (that it is compatible with the grading and that the associated graded algebra is the polynomial ring
  with z of filtration degree 0).
- Step (c) uses that U is a domain, that z is central, that U/zU is a domain, that c is central with lambda not
  zero, and that B-bar is not zero.
- The statement needs A and B central; the proof does not use that they are monomials. If A, B are not central the
  commutator has more terms and the theorem says nothing.
- Machine checks at (3, 3) and (5, 5) confirm the identities, the length and the pure Betti table for
  (b, d) = (1, 1), (1, 2), (2, p - 1) with A = x^e, B = y^e, l_1 = b y, l_2 = d x. They do not replace the review.
