# Explicit pure pairs in the linear family for p = 2e - 1 and p = 2e - 3

Date: 2026-11-20. Status: derivation by the coordinating session, checked by machine (section 5); to be reviewed by
a reader other than the writer. It depends on Theorem 2 and Corollary 3 of
`2026-11-20-pairs-with-exponent-t.md` (under review when this note was written): every statement below is
conditional on that note.

## 0. Setting

Notation of `2026-11-20-pairs-with-exponent-t.md`, with t = e - 2, d = 1, w = 2e - 2. For a, b in k, not zero, the
short pair is

    f = x^e + a y^(e-2) z,      g = y^e + b x^(e-2) z,      n = ab,

that is alpha = a z and beta = b z. Then A_(e-t) = A_2 = h (h + z),

    Delta = ab z^2 - h (h + z) = - q,          q = h^2 + h z - n z^2,
    L = (h - (e-1) z)(h - e z) ... (h - (2e-4) z),      L' = (h + e z)(h + (e+1) z) ... (h + (2e-3) z),
    X = L tau^w(Delta),      X' = L' sigma^w(Delta),

and, with z = 1, rho(h) = X'(h)/X(h) = L'(h) q(h + w) / (L(h) q(h - w)).

Facts from the note, for these pairs:

- z does not divide Delta. (C1) holds: q(0, z) = q(-z, z) = - n z^2 is not zero.
- If Delta is coprime to X and X', then (F1) and (F2) hold with forms c, c' of degree 1 (Corollary 3), and
  c c' = h (h + z) + mu Delta. Since c and c' are linear forms, mu = 0 exactly when c is a scalar multiple of h or of
  h + z.
- So by Theorem 2: if p = 0 or p >= 2e - 4, Delta is coprime to X and X', and c is a multiple of neither h nor h + z,
  then (f, g) is a pure pair: U/(Uf + Ug) has the Betti table (1, 2, 2, 1) on (0, e, 3e, 4e).

With z = 1, c is the polynomial of degree at most 1 with c = a X' X^(-1) modulo q.

**Lemma 1.** Assume Delta coprime to X and X'. (i) If q(h, 1) has two distinct roots theta and theta' = -1 - theta
(in k or a quadratic extension), then mu = 0 exactly when

    rho(theta) theta' = rho(theta') theta        or        rho(theta) theta = rho(theta') theta'.

(ii) If q(h, 1) = (h - theta)^2 (so theta = -1/2 and n = -1/4), then mu = 0 exactly when the logarithmic derivative
lambda = rho'(theta)/rho(theta) equals -2 or 2.

*Proof.* (i) c is the interpolation polynomial with c(theta) = a rho(theta), c(theta') = a rho(theta'), so
c(0) (theta - theta') = theta c(theta') - theta' c(theta) and
c(-1) (theta - theta') = theta c(theta) - theta' c(theta') (because -1 - theta' = theta and -1 - theta = theta').
c is a multiple of h when c(0) = 0 and of h + 1 when c(-1) = 0. (ii) c = a (rho(theta) + rho'(theta)(h - theta)),
the Taylor polynomial of a X'/X at theta, and rho(theta) is not zero; c(0) = 0 reads lambda = 1/theta = -2 and
c(-1) = 0 reads lambda = 1/(1 + theta) = 2. []

## 1. The prime p = 2e - 1

**Theorem A.** Let e >= 3 be such that p = 2e - 1 is prime, and let k have characteristic p. The pair

    f = x^e + y^(e-2) z,      g = y^e + 2 x^(e-2) z

is a pure pair, unless p = 11 or p = 43.

*Proof.* n = 2 and q = (h - 1)(h + 2): theta = 1, theta' = -2, distinct because p is not 3. Modulo p, w = -1, so
q(h + w) = q(h - 1) and q(h - w) = q(h + 1); and q(theta - 1) = - 2 theta, q(theta + 1) = 2 theta + 2 = - 2 theta'
for a root theta. Modulo p, - l = 2e - 1 - l, so

    L(h) = (h + 3)(h + 4) ... (h + e),          L'(h) = (h - 2)(h - 3) ... (h - (e-1)),

and

    L(1) = (e+1)!/6,     L(-2) = (e-2)!,     L'(1) = (-1)^e (e-2)!,     L'(-2) = (-1)^e (e+1)!/6.

All four are not zero modulo p because e + 1 < p. Coprimality: X(1) = L(1) Delta(2) = - 4 L(1),
X(-2) = L(-2) Delta(-1) = 2 L(-2), X'(1) = L'(1) Delta(0) = 2 L'(1), X'(-2) = L'(-2) Delta(-3) = - 4 L'(-2), none
zero; and p >= 2e - 4. With kappa = (e-1) e (e+1) = (e+1)!/(e-2)!,

    rho(1) = (L'(1)/L(1)) (theta/theta') = (-1)^(e+1) 3/kappa,        rho(-2) = (L'(-2)/L(-2)) (theta'/theta) = (-1)^(e+1) kappa/3.

By Lemma 1 (i), mu = 0 exactly when - 6/kappa = kappa/3 or 3/kappa = - 2 kappa/3, that is kappa^2 = - 18 or
2 kappa^2 = - 9. Now 8 kappa = (2e)^3 - 4 (2e) = 1 - 4 = - 3 modulo p, so 64 kappa^2 = 9, and the two conditions are
9 = - 1152 and 18 = - 576: p divides 1161 = 3^3 43 or 594 = 2 3^3 11. With p >= 5 this is p = 43 or p = 11. []

At the two exceptional primes other short pairs work, by an exact evaluation of the same conditions (section 5):
for p = 11, e = 6, the pair with n = 3, f = x^6 + y^4 z, g = y^6 + 3 x^4 z (the pure pair found by EXP-009); for
p = 43, e = 22, the pair with n = 1, f = x^22 + y^20 z, g = y^22 + x^20 z.

**Corollary A.** For every prime p >= 5 the primitive point (1, 2, 2, 1) of the ray (0, e, 3e, 4e) with
e = (p + 1)/2 is the Betti table of a module over U over GF(p), with an explicit pair of generators.

(For p = 3, e = 2, the point is realized over GF(3) by the pair of EXP-003; that case is outside this note.)

## 2. The prime p = 2e - 3

**Theorem B.** Let e >= 4 be such that p = 2e - 3 is prime, and let k have characteristic p. The pair

    f = x^e + y^(e-2) z,      g = y^e - (1/4) x^(e-2) z

is a pure pair, unless the Fermat quotient q_p(2) = (2^(p-1) - 1)/p is congruent to 1/2 or to 3/2 modulo p.

*Proof.* n = -1/4 and q = (h + 1/2)^2, theta = -1/2. Modulo p, w = 1, so q(h + w) = (h + 3/2)^2 and
q(h - w) = (h - 1/2)^2, and - l = 2e - 3 - l gives

    L(h) = (h + 1)(h + 2) ... (h + e - 2),          L'(h) = h (h - 1) ... (h - (e-3)).

Coprimality: L(-1/2) is the product of the (2k - 1)/2 and L'(-1/2) the product of the - (2k + 1)/2, with
2k - 1 and 2k + 1 odd numbers between 1 and 2e - 5 = p - 2, not zero; Delta(theta - 1) = Delta(theta + 1) = - 1;
and p >= 2e - 4. The logarithmic derivative of rho = L' (h + 3/2)^2 / (L (h - 1/2)^2) at theta = -1/2 is

    lambda = - sum over 0 <= k <= e-3 of 2/(2k+1) + 2 - sum over 1 <= k <= e-2 of 2/(2k-1) + 2 = 4 - 4 S,
    S = 1 + 1/3 + 1/5 + ... + 1/(p-2).

By Lemma 1 (ii), mu = 0 exactly when S = 3/2 or S = 1/2. Finally S = q_p(2) modulo p: (2^p - 2)/p is the sum over
1 <= k <= p-1 of binom(p, k)/p, congruent to the sum of the (-1)^(k-1)/k, which is the sum over the odd k minus the
sum over the even k; and the sum over the even k is minus the sum over the odd k (replace k by p - k). So
2 q_p(2) = 2 S. []

For p = 5 (e = 4), q_5(2) = 3 = 1/2: the pair is not pure (computed), and the short pair with n = 3,
f = x^4 + y^2 z, g = y^4 + 3 x^2 z, is. The primes p <= 2,000,000 with q_p(2) = 1/2 or 3/2 modulo p are 5, 30577
and 45827; at the last two the short pair with n = 1 satisfies the conditions of section 0 (exact evaluation,
section 5).

**Corollary B.** For every prime p with 5 <= p <= 2,000,000 the primitive point (1, 2, 2, 1) of the ray
(0, e, 3e, 4e) with e = (p + 3)/2 is the Betti table of a module over U over GF(p), with an explicit pair of
generators: the pair of Theorem B, or the short pair with n = 3 (p = 5) or n = 1 (p = 30577, 45827).

## 3. The rule of the linear family

The note on the weight-zero projection proves that for an odd prime p <= 2e - 5 no member of the stratum of the
linear family has finite length. Corollaries A and B give the other half of the rule "pure members exactly when
2e - p <= 3" for p = 2e - 1 (every e) and for p = 2e - 3 (every e with p <= 2,000,000; beyond that bound, whenever
q_p(2) is not 1/2 or 3/2, and otherwise as soon as one short pair satisfies the conditions).

## 4. What is not proved

- That for a prime p = 2e - 3 above 2,000,000 with q_p(2) = 1/2 or 3/2 another member works (it does at the three
  exceptional primes found).
- Anything for members of the linear family with alpha or beta not a multiple of z; the conditions of the note
  apply to them, and about half of the products n = ab pass in every case computed (section 5), but no closed form
  is given.
- The statements depend on Theorem 2 of the note on the pairs with exponent t.

## 5. Machine checks

Scripts and logs: data root, `caos-research/boij-soderberg-realizability/notes/exponent-t-2026-11-20/`
(`probe_short_pairs.py`, `probe_short_pairs_range.py`, `probe_short_pairs_exceptions.py`, with their logs
`short_3_34.log`, `short_range.log`, `short_exceptions.log`). The conditions are evaluated with exact polynomial
arithmetic over GF(p) (the filter (F0) to (F3) of EXP-019 and the test of (C1)), independently of the closed forms
of sections 1 and 2.

- Theorem A against the filter: for the 137 primes p = 2e - 1 with 3 <= e <= 400 the pair with n = 2 passes with
  (C1) except at p = 11 and p = 43, where it fails (F3) only.
- Theorem B against the filter: for the 137 primes p = 2e - 3 with 4 <= e <= 400 the pair with n = -1/4 passes with
  (C1) except at p = 5, where it fails (F3) only; the Fermat quotient rule agrees at every one of them.
- The exceptional primes: first products that pass with (C1): n = 3 at (e, p) = (4, 5) and (6, 11); n = 1 at
  (22, 43), (15290, 30577) and (22915, 45827).
- Against the computation in U (the Betti table with `uhlib`) for e <= 8: the pairs with n = 2 at (3, 5), (4, 7),
  (7, 13) and with n = -1/4 at (5, 7), (7, 11), (8, 13) are pure; the pair with n = 2 at (6, 11) and the pair with
  n = -1/4 = 1 at (4, 5) are not; in the 19 pairs tabled, "passes with (C1)" and "pure in U" agree.
- EXP-019 found pure pairs in the same stratum at (15, 29), (16, 29) and (16, 31) by a random search with the
  filter, confirmed in U by two instruments.

## How could this be wrong?

- Through the note it depends on. If Theorem 2 needed a further hypothesis, the comparison with U for e <= 8 would
  still hold, but the statements for larger e would lose their proof.
- A slip in the reductions modulo p (the index sets of L and L') would be seen by the comparison with the filter,
  which evaluates L, L' and Delta from their definitions for 274 primes.
- The congruence S = q_p(2) is classical; it is rederived above and checked numerically inside the comparison of
  Theorem B with the filter (the rule agrees at all 137 primes).
