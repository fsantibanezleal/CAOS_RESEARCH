# Maps of Mat_mu(F_2) into a Hilbert space contract for every mu, with the exact constant 2 - 2^(1-mu)

Date: 2026-11-24. Unit PNP-006 of the programme. Written by the coordinating session; **not yet read by a second
reader**. It completes Proposition 5.4 of `2026-11-24-boolean-ladder-and-the-two-cases.md`, which had the statement
for mu <= 4 by computation only.

Marks: [D] derived here; [MV] machine-verified by `experiments/EXP-002-character-sums-closed-forms` (exact
arithmetic); [K] standard.

## 1. Statement

Let mu >= 2 and let F be a map from the additive group Mat_mu(F_2) into a real Hilbert space. For 1 <= r <= mu let
D(r)^2 be the mean of |F(a) - F(a + W)|^2 over all matrices a and all W of rank r.

Theorem [D]. D(mu)^2 <= (2 - 2^(1-mu)) D(1)^2. Equality holds if and only if the Fourier transform of F vanishes at
every character of rank at least 2, that is, if and only if F is a constant plus a combination of the functions
a -> (-1)^(u^T a v) with u, v nonzero vectors.

Consequences.

- The metric sqrt(rank(a - a')) on Mat_mu(F_2) is not isometric to a subset of a Hilbert space for any mu >= 2,
  since it has D(mu)^2 = mu D(1)^2 and mu > 2 - 2^(1-mu). (The paper under study states this for mu >= 3, Remark D.3.)
- In the language of the paper: a price on Mat_mu(F_2) that is a Euclidean metric satisfies the contracting
  inequality with s^2 = 2 - 2^(1-mu) < 2 <= mu. So a failure of the contracting hypothesis needs prices that are far
  from Euclidean, although they are metrics of nonpositive curvature and although the flat hypothesis, which then
  holds, says that every finite Euclidean metric is a price.

## 2. Proof

Characters. For B in Mat_mu(F_2) let chi_B(W) = (-1)^(<B, W>), <B, W> = trace(B^T W) = sum of B_ik W_ik. These are the
characters of the group. Write F = sum_B c_B chi_B with c_B in the Hilbert space (the transform of each coordinate).
Then for a fixed W the mean over a of |F(a) - F(a + W)|^2 is sum_B |c_B|^2 (1 - chi_B(W))^2 = 4 sum over the B with
chi_B(W) = -1 of |c_B|^2. Averaging over the W of rank r,

    D(r)^2 = 4 sum_B p_r(B) |c_B|^2,

where p_r(B) is the fraction of the matrices W of rank r with <B, W> = 1. The numbers p_r(B) are unchanged when B is
replaced by P B Q with P, Q invertible (W -> P^T W Q^T permutes the matrices of rank r), so they depend on the rank j of
B only; take B = diag(1^j, 0). Since p_r(0) = 0, the theorem is the statement

    p_mu(j) / p_1(j) <= 2 - 2^(1-mu) for 1 <= j <= mu, with equality exactly at j = 1.     (*)

Rank one. A matrix of rank one is u v^T with u, v nonzero, uniquely over F_2, and <B, u v^T> = sum over i <= j of
u_i v_i. Over all pairs (u, v) in F_2^mu x F_2^mu the form sum_{i <= j} u_i v_i takes the value 1 exactly
(2^(2j-1) - 2^(j-1)) 2^(2(mu-j)) times (the hyperbolic form on F_2^(2j) has 2^(2j-1) + 2^(j-1) zeros), and none of
these pairs has u = 0 or v = 0. Hence

    p_1(j) = 2^(2 mu - 1) (1 - 2^(-j)) / (2^mu - 1)^2.     [MV for mu <= 4]

Full rank. Let S(j) be the sum of chi_B(W) over the invertible W, so that p_mu(j) = (1 - S(j)/|GL_mu(F_2)|)/2.

Lemma [D; the formula is classical, K]. Over the field with q elements, for a nontrivial additive character psi and
B of rank j in Mat_n(F_q), the sum of psi(<B, W>) over the invertible W is
(-1)^j q^(j(j-1)/2) q^(j(n-j)) |GL_(n-j)(F_q)|.

Proof of the lemma. For a matrix W, the sum over the subspaces U of the kernel of W of the Moebius function
m(U) = (-1)^d q^(d(d-1)/2), d = dim U, of the lattice of subspaces is 1 if the kernel is 0 and 0 otherwise. So the
sum in question is the sum over all subspaces U of m(U) times the sum of psi(<B, W>) over the linear space L_U of the
matrices W that vanish on U. That inner sum is |L_U| = q^(n(n-d)) if <B, W> = 0 for every W in L_U, and 0 otherwise.
The rows of the matrices of L_U run freely over the annihilator of U, so <B, W> = 0 on L_U exactly when every row of
B lies in U, that is when U contains the row space of B. The number of subspaces of dimension d that contain a fixed
subspace of dimension j is the Gaussian binomial coefficient [n-j, d-j]. With e = d - j and m = n - j the sum becomes

    (-1)^j q^(j(j-1)/2) q^(nm) sum_{e=0}^{m} [m, e] (-1)^e q^(e(e-1)/2) (q^(-m))^e,

and by the q-binomial theorem the last sum is the product over i = 0..m-1 of (1 - q^(i-m)) = q^(-m(m+1)/2) times the
product over s = 1..m of (q^s - 1) = q^(-m^2) |GL_m(F_q)|. Since nm - m^2 = j(n - j), the lemma follows.

For q = 2 and n = mu, using |GL_mu| = |GL_(mu-j)| times the product over i < j of (2^(mu-i) - 1) 2^(mu-i-1), the
powers of 2 cancel and

    S(j)/|GL_mu(F_2)| = (-1)^j / prod_{i=0}^{j-1} (2^(mu-i) - 1),
    p_mu(j) = (1 - (-1)^j / prod_{i<j} (2^(mu-i) - 1)) / 2.     [MV for mu <= 4]

The inequality (*). Put R_j = 1 / prod_{i<j} (2^(mu-i) - 1). From the two closed forms,

    p_mu(j)/p_1(j) = (1 - (-1)^j R_j) (1 - 2^(-mu))^2 / (1 - 2^(-j)).

At j = 1, R_1 = 1/(2^mu - 1) and 1 + R_1 = 1/(1 - 2^(-mu)), so the ratio is 2(1 - 2^(-mu)) = 2 - 2^(1-mu). For
j >= 2 every factor of the product is at least 1, so R_j <= R_2 = 1/((2^mu - 1)(2^(mu-1) - 1)) <= 1/3, and
1 - 2^(-j) >= 3/4. Hence the ratio is at most (4/3)(1 + 1/3)(1 - 2^(-mu))^2 = (16/9)(1 - 2^(-mu))^2, which is the
value at j = 1 times (8/9)(1 - 2^(-mu)) < 1. So (*) holds, strictly for j >= 2. [MV: the closed forms satisfy (*)
strictly for every mu from 2 to 40; the difference between the value at j = 1 and the largest value at j >= 2
stays above 2/3 in that range (the two values tend to 2 and to 4/3).]

Equality. D(mu)^2 - (2 - 2^(1-mu)) D(1)^2 = 4 sum_B (p_mu(B) - (2 - 2^(1-mu)) p_1(B)) |c_B|^2, a sum of terms that
are zero at rank 0 and 1 and negative at rank at least 2.

## 3. What is not claimed

Nothing on prices that are not Euclidean, and so nothing on which of the paper's two cases occurs.

## How could this be wrong?

- The inequality for j >= 2 uses R_j <= 1/3 and 1 - 2^(-j) >= 3/4 only. The machine check for mu up to 40 guards
  the conclusion in that range, not the algebra.
- The lemma is proved here from the Moebius function of the subspace lattice; its statement agrees with exhaustive
  counts for n <= 4 and q = 2 only.
