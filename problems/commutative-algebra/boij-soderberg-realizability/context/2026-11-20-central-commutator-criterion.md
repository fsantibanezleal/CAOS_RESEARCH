# Pairs with a central commutator in characteristic p: a criterion for purity, and pure pairs for every e = 0 or 1 modulo p

Date: 2026-11-20. Status: derivation [D] by the coordinating session. Reviewed on 2026-11-21 by a reader other than
the writer (record `bs-central-commutator-criterion-review-2026-11-20` in the coordination repository): every step
holds, the acyclicity lemma was checked against a source, no blocker and no major finding; twelve minor repairs,
applied below (the first text is in commit 588d6bb1). The reviewer's own computations confirm the explicit pairs of
cases B, C, D at (4, 3), (6, 5), (8, 7), (6, 3), (7, 3) and the criterion on 180 random pairs. It generalizes the note
`2026-11-20-central-pair-theorem.md` (whose proof is elementary and independent of this one). Machine checks so far,
by a script of the coordinating session on settled pairs only: on 604 pairs (four explicit, 600 random) at (e, p) =
(3, 3), (5, 5), (4, 3), (6, 3) the criterion below and the pure Hilbert function agree on every pair, the commutator
identity holds on every pair, and 24 of 24 Betti tables computed on pairs with the pure Hilbert function are pure
(script and log under the data root, `caos-research/boij-soderberg-realizability/EXP-012-probe/`). EXP-012 (frozen the
same day) checks the statement on open pairs with two instruments.

## Setting

Notation of the note `2026-11-20-central-pair-theorem.md`. Throughout, k is a field of characteristic p >= 3,
X = x^p, Y = y^p, and Z = k[X, Y, z], a polynomial ring in three variables inside U whose elements are central
(fact F2 of that note). Z is graded with deg X = deg Y = p, deg z = 2. By the PBW basis, U is a free Z-module with
basis x^i y^j, 0 <= i, j <= p - 1; so each U(-d) is a graded free Z-module of rank p^2, and right multiplication by
an element of U is Z-linear.

For a point q of Spec Z with residue field K, write U(q) = U tensor_Z K, a K-algebra of dimension p^2, and a(q) for
the image of a in U(q). Only closed points over an algebraic closure of k are used: q = (X_0, Y_0, z_0) in K^3 with K
algebraically closed, and "q is not the origin" means (X_0, Y_0, z_0) is not (0, 0, 0). Two regimes: when z_0 = 0,
U(q) is the commutative local ring K[x, y]/(x^p - X_0, y^p - Y_0); when z_0 is not 0, U(q) is the algebra of p by p
matrices over K.

The class. V_e = Z_e + Z_(e-1) x + Z_(e-1) y, the forms of degree e of the shape

    f = A + beta_1 x + beta_2 y,    A in Z_e,   beta_1, beta_2 in Z_(e-1).

For such f put l_f = beta_1 x + beta_2 y and n(f) = A^p + beta_1^p X + beta_2^p Y, an element of Z of degree p e.

## Four lemmas

Lemma 1. For beta_1, beta_2 in Z, (beta_1 x + beta_2 y)^p = beta_1^p X + beta_2^p Y.

Proof. Put a = beta_1 x, b = beta_2 y; then [a, b] = beta_1 beta_2 z is central. By Jacobson's formula, in an
associative algebra of characteristic p, (a + b)^p = a^p + b^p + s_1(a, b) + ... + s_(p-1)(a, b), where each s_i is a
Lie polynomial in a and b, homogeneous of degree p (Jacobson, Lie Algebras, chapter V, section 7). Every bracket of
length at least 3 in a and b vanishes because [a, b] is central, and p >= 3, so every s_i vanishes. Hence (a + b)^p =
a^p + b^p = beta_1^p X + beta_2^p Y. QED.

Lemma 2. Let f = A + l_f be in Z + Z x + Z y and q a point. Then f(q) is a unit of U(q) if and only if n(f)(q) is
not zero.

Proof. A is central, so with f* = sum over i = 0, ..., p - 1 of (-1)^i A^(p-1-i) l_f^i one has
f f* = f* f = A^p + l_f^p = n(f), by Lemma 1 and because p is odd. If n(f)(q) is not zero, f(q) is a unit. Suppose
n(f)(q) = 0. If l_f(q) = 0 then f(q) = A(q) and A(q)^p = n(f)(q) = 0, so f(q) = 0. If l_f(q) is not zero, say with
beta_1(q) not zero, then l_f(q)^i = beta_1(q)^i x^i + (terms of lower degree in x) for i <= p - 1, so
1, l_f(q), ..., l_f(q)^(p-1) are linearly independent in U(q), f*(q) is not zero, and f(q) f*(q) = 0 shows that f(q)
is a zero divisor. QED.

Lemma 3. Let R be a ring and f, g in R with c = g f - f g central in R. Let F_R be the sequence of left R-modules

    0 -> R -> R^2 -> R^2 -> R -> 0,
    1 -> (g, f);   (1, 0) -> s_1 = (c - f g, f^2),  (0, 1) -> s_2 = (g^2, -(g f + c));   (1, 0) -> f,  (0, 1) -> g.

It is a complex. (i) If c is a unit, the first map is injective, the last is surjective, and the complex is exact at
the R^2 that receives R (the second place from the left). (ii) The same holds if c = 0 and f or g is a unit.

Proof. The three compositions vanish by the identities of the earlier note, which use only that c = g f - f g is
central. Let (v, w) with v s_1 + w s_2 = 0 and t = v f - w g; the two components give t g = c v and t f = c w.
(i) If u g = u f = 0 then u c = (u g) f - (u f) g = 0, so u = 0. The element c = g f - f g lies in R f + R g, so the
last map is surjective. And (v, w) = (c^(-1) t)(g, f). (ii) Say f is a unit; then f and g commute. u f = 0 gives
u = 0; R f = R; and t f = 0 gives t = 0, so v f = w g, v = w g f^(-1) = w f^(-1) g and (v, w) = (w f^(-1))(g, f).
The case of g is symmetric. QED.

When R is an algebra of finite dimension over a field, the alternating sum of the dimensions of the four terms is 0,
so in cases (i) and (ii) the complex F_R is exact at every place.

Lemma 4. Let 0 -> F_3 -> F_2 -> F_1 -> F_0 be a complex of graded free Z-modules of finite rank with homogeneous
maps, and suppose that for every closed point q other than the origin, over an algebraic closure of k, the complex
of fibres 0 -> F_3(q) -> F_2(q) -> F_1(q) -> F_0(q) -> 0 is exact. Then the complex is exact at F_3, F_2 and F_1, and
the cokernel of F_1 -> F_0 has finite length.

Proof. Extending the field is faithfully flat, so take k algebraically closed. At a closed point q other than the
origin, the localization at q is a bounded complex of free modules of finite rank over a local ring whose reduction
modulo the maximal ideal is exact, so it is exact (Nakayama's lemma, from the right). So every homology module of the
complex, the cokernel included, is a finitely generated graded Z-module whose localization at every closed point other
than the origin is zero; its support is closed and its closed points are dense in it (Z is a finitely generated
algebra over a field), so the support is the origin or empty and the module has finite length. Such a module equals
its localization at the origin. The acyclicity lemma of Peskine and Szpiro (Lemme 1.8 of their "Dimension projective
finie et cohomologie locale"; Stacks Project, Tag 00N0: a complex 0 -> F_s -> ... -> F_0 of finitely generated modules
over a noetherian local ring with depth F_i >= i, whose homology in each positive degree is zero or of depth 0, is
exact in positive degrees), applied at the origin, where each F_i has depth 3, gives the exactness. QED.

## The criterion

Theorem. Let f = A + beta_1 x + beta_2 y and g = B + delta_1 x + delta_2 y be in V_e, and put
D = beta_1 delta_2 - beta_2 delta_1, an element of Z of degree 2e - 2.

(a) g f - f g = - D z. It is central.

(b) The following are equivalent.
  (i) M = U/(Uf + Ug) has finite length.
  (ii) The elements z D, n(f), n(g) of Z have no common zero other than the origin (over an algebraic closure of k).
  (iii) (f, g) is a pure pair: the complex of Lemma 3 over R = U, with c = - D z, is a minimal free resolution of M,
        so M has the Betti table (1, 2, 2, 1) on (0, e, 3e, 4e), the Hilbert function h_e and length e^3.

Proof. (a) A, B and the coefficients are central, so g f - f g = [delta_1 x + delta_2 y, beta_1 x + beta_2 y]
= (delta_1 beta_2 - delta_2 beta_1) [x, y] = - D z.

(ii) implies (iii). The complex F_U is a complex of graded free Z-modules of rank p^2, 2 p^2, 2 p^2, p^2 with
homogeneous Z-linear maps, and its fibre at q is the complex F_(U(q)) of Lemma 3 for f(q), g(q), c(q). Let q be a
closed point other than the origin. If (z D)(q) is not zero, c(q) is a unit and Lemma 3 (i) applies. Otherwise
c(q) = 0 and by (ii) one of n(f)(q), n(g)(q) is not zero, so one of f(q), g(q) is a unit by Lemma 2 and Lemma 3 (ii)
applies. In both cases the fibre is exact at every place. By Lemma 4 the complex is exact at its three left places
and its cokernel M has finite length. Its maps are U-linear, so it is a free resolution of M over U, minimal
because no entry is a nonzero constant. The Hilbert series of M is then (1 - 2 t^e + 2 t^(3e) - t^(4e)) H_U.

(iii) implies (i): the Betti table gives the Hilbert series (1 - 2 t^e + 2 t^(3e) - t^(4e)) H_U, a polynomial.

(i) implies (ii). Let q be a common zero other than the origin, over an algebraically closed field K. Since M tensor_Z
    K(q) = U(q)/(U(q) f(q) + U(q) g(q)), it is enough to show that U(q) f(q) + U(q) g(q) is not U(q): then q lies in
    the support of M, and the support of a graded Z-module of finite length is the origin. By Lemma 2 neither f(q) nor
    g(q) is a unit.
- If z(q) = 0, U(q) = K[x, y]/(x^p - X_0, y^p - Y_0) is a commutative local ring (x^p - X_0 is a p-th power of a
  linear polynomial), and two non-units generate a proper ideal.
- If z(q) is not 0, then D(q) = 0, so the linear forms l_f(q) and l_g(q) are linearly dependent. If both are zero,
  f(q) and g(q) are scalars and non-units, so both are zero. Otherwise let l be one of them that is not zero; the
  other is a multiple of it, so f(q) and g(q) lie in the commutative subalgebra K[l]. By Lemma 1, l^p is a scalar, say
  lambda_0^p, so K[l] is a quotient of K[T]/((T - lambda_0)^p), a local ring, with l - lambda_0 nilpotent. A unit of
  K[l] is a unit of U(q), so f(q) and g(q) are non-units of K[l], hence multiples of l - lambda_0 there, and U(q) f(q)
  + U(q) g(q) lies in U(q)(l - lambda_0), which is a proper left ideal because l - lambda_0 is nilpotent. QED.

Remark (which e). An element of V_e is not divisible by z only if e = 0 or 1 modulo p: modulo z, A becomes a form
of degree e in x^p, y^p, and beta_1, beta_2 become forms of degree e - 1 in x^p, y^p. A pair of forms divisible by z
is not of finite length. So V_e holds pure pairs only when p divides e or e - 1.

## Pure pairs for every e = 0 or 1 modulo p

Corollary. Let p be an odd prime and e >= 3 with e = 0 or 1 modulo p. Over every field of characteristic p the
following pair (f, g) is pure, so the point (1, 2, 2, 1) of (0, e, 3e, 4e) is realized over U in characteristic p.

| Case | Condition | f | g |
|---|---|---|---|
| A | p divides e, e odd | x^e + y z^s | y^e + x z^s, with s = (e - 1)/2 |
| B | p divides e - 1, e even | x^e + z^(e/2) | y^e + z^(e/2) |
| C | p divides e, e even | x^e + z^(e/2) + y^(p+1) z^j | y^e + x^(p+1) z^j, with j = (e - p - 1)/2 |
| D | p divides e - 1, e odd | x^e + y z^s + x^p z^j | y^e + x z^s, with s = (e - 1)/2, j = (e - p)/2 |

Proof, case by case: the data (A, beta_1, beta_2; B, delta_1, delta_2), then D, n(f), n(g), then the common zeros of
z D, n(f), n(g). Write e = n p or e = n p + 1.

- A. (X^n, 0, z^s; Y^n, z^s, 0). D = - z^(e-1); n(f) = X^e + z^(s p) Y; n(g) = Y^e + z^(s p) X. A common zero has z =
  0, then X = Y = 0. (This is the central pair of the earlier note with l_1 = y, l_2 = x.)
- B. (z^(e/2), X^n, 0; z^(e/2), 0, Y^n). D = X^n Y^n; n(f) = z^(p e/2) + X^e; n(g) = z^(p e/2) + Y^e. If z = 0 then X
  = Y = 0. If X = 0 then z = 0 by n(f); if Y = 0 then z = 0 by n(g).
- C. (X^n + z^(e/2), 0, Y z^j; Y^n, X z^j, 0). D = - X Y z^(2j); n(f) = X^e + z^(p e/2) + Y^(p+1) z^(j p); n(g) = Y^e
  + X^(p+1) z^(j p). If z = 0 then X = Y = 0. If z is not 0 and X = 0, then Y = 0 by n(g) and n(f) = z^(p e/2) is not
  0. If z is not 0 and Y = 0, then X = 0 by n(g), and again n(f) is not 0. (Here e >= 2p, so j >= 1, and j is an
  integer because n is even.)
- D. (X z^j, X^n, z^s; 0, z^s, Y^n). D = X^n Y^n - z^(e-1); n(f) = X^p z^(j p) + X^e + z^(s p) Y; n(g) = z^(s p) X +
  Y^e. If z = 0 then X = Y = 0 (here j >= 1). If z is not 0 and D = 0, then X and Y are not 0 and (delta_1, delta_2) =
  mu (beta_1, beta_2) at q with mu = z^s / X^n, so by the definition of n, n(g) = mu^p (n(f) - A^p) at q; if n(f) =
  n(g) = 0 there, then A = X z^j vanishes, a contradiction.

In each case (ii) holds, and the theorem gives (iii). QED.

What this settles, with what was known. For e = 6: characteristic 5 by case B (open before) and characteristic 3 by
case C (known from a search, EXP-008); characteristic 11 is known from the linear family (EXP-009). For e = 7:
characteristic 3 by case D (open before) and characteristic 7 by case A, which is the central pair of the earlier
note; characteristics 11 and 13 are known from EXP-009. For e <= 7 the pairs (e, p) left open are (6, 7) and (7, 5).
For e = 8 case B gives characteristic 7, and characteristics 3, 5, 11 and 13 stay open after this note (the note
`2026-11-21-pull-back-and-scaling.md` then covers characteristic 3). Theorem A covers characteristic 0 and at least
2e, and Theorem C excludes characteristic 2.

## Remarks

1. The central pair of the earlier note with general A, B, l_1, l_2 is the case beta_i, delta_i in k z^s; for
   independent l_1, l_2 its condition (ii) reads: A-bar, B-bar have no common zero other than the origin, which is the
   hypothesis there. The elementary proof given there does not use the fibres.
2. The theorem classifies the pure pairs inside V_e: they are the pairs of finite length. On settled pairs 27 to 58
   percent of the pairs of V_e over GF(p) are pure (63 of 151 at (3, 3), 88 of 151 at (5, 5), 41 of 151 at (4, 3), 51
   of 151 at (6, 3)), against 0.14 percent of random pairs at (5, 5) and 0.02 percent at (6, 3) with the pure Hilbert
   function (EXP-008: 120 of 86,250 and 63 of 289,000).
3. A pair of case D without the term x^p z^j is not of finite length: for A = B = 0 the forms n(f), n(g) are
   proportional along D = 0, and they have a common zero there.
4. The class cannot reach e = 2, ..., p - 1 modulo p. There the commutator of a pure pair is not central (the centre
   of U is Z): modulo z^2 it is z times the Jacobian determinant of the images, which is not a polynomial in x^p, y^p
   unless it vanishes, and it does not vanish, because a pure pair has images without common factor and p does not
   divide e.

5. Outside V_e the equivalence of (i) and (iii) fails (review): over GF(3) at e = 3 there are pairs of finite length,
   with the pure Hilbert function, whose Betti table is not pure.

## How could this be wrong?

- Lemma 4 carries the weight: fibrewise exactness away from the origin plus the acyclicity lemma. The reviewer should
  check the statement of the acyclicity lemma against a source and the passage from fibres to localizations.
- Lemma 3 is used in two regimes; in (ii) the unit must commute with the other element, which holds because c(q) = 0.
- The direction (i) implies (ii) uses that a non-unit of the local ring K[l] lies in its maximal ideal and that
  l - lambda_0 is nilpotent; and, at z(q) = 0, that U(q) is commutative local.
- Case D of the corollary uses the proportionality of the linear parts along D = 0; the reviewer should redo it.
- The machine checks are on settled pairs; EXP-012 tests the open pairs (6, 5) and (7, 3) and larger e.
