# From the algebraic lower bound of 2026-11-23 towards Boolean circuits: the degree ladder, and which of the two cases occurs

Date: 2026-11-24. Unit PNP-001 of the programme. Written by the coordinating session. **Reviewed on 2026-11-24 by a
reader other than the writer (reviewer on opus): CORRECT AFTER FIXES**, with two blockers (J1, J2), two major findings
(J3, J4) and eight minor ones (J5 to J12). All twelve are applied in this version and listed at the end. The
reviewer's separate verdict on Proposition 3.1 is PLAUSIBLE WITH NAMED GAPS; the statement below is the corrected
one, and its remaining gap is named in it.

Marks: [P] read on the primary source named; [K] standard, source named, not re-derived; [D] derived here; [R]
confirmed by the reviewer on the page named; [MV] machine-verified by `experiments/EXP-001-rank-metric-finite-checks`
(exact arithmetic); [Q] open.

The paper is: Claude (Anthropic), "VP != VNP over every field", `anthropics/formal-math`, folder `vp-vnp`,
`paper.pdf` with SHA-256 `882f5eef...` (copy under the data root,
`caos-research/millennium-open-four-2026-11-24/main-session/vpvnp/`), merged 2026-11-23. Its own status line: found
and written by AI models, formalized in Lean, "no human mathematician has checked the proof". Every statement below
that depends on the paper is conditional on the paper. Nothing here was checked against the Lean source, and no Lean
build was run.

## 1. What is taken from the paper [P]

- Circuits. An arithmetic circuit over a field k is a list of polynomials, each a variable, a constant, or the sum or
  product of two earlier ones; it computes the polynomial itself, with no bound on degrees. HC_m is the Hamiltonian
  cycle polynomial of the m x m matrix of variables (multilinear, degree m).
- Theorem 1.1 (M.3): over every field, every circuit for HC_m has more than m^(c (log m)^(1/3)) gates for large m.
- Spectral points (Definition 2.1). A spectral point phi on a finite set V of parties is a function on V-tensors with
  phi(1) = 1, phi(st) = phi(s) phi(t), and phi(s) <= sum_j phi(t_j) whenever s = sum_j s_j with each s_j a restriction
  of t_j. On the wire <q>_uv (the q x q identity between the parties u and v) it takes the value q^(d_phi(u,v)) with
  d_phi a pseudometric with values in [0,1].
- Prices (`def_price`, page 5). A price on V is a pointwise limit of functions c d_phi with c >= 0.
- Prices have nonpositive curvature (Proposition C.3): every price is pulled back from the metric of a CAT(0) space.
- The two hypotheses (Definition D.1). For a price on the additive group Mat_mu(F_2) and r <= mu, D(r)^2 is the mean
  of |a, a + W|^2 over all matrices a and all W of rank r. Every price has D(r) <= sqrt(r) D(1). Contracting
  hypothesis: for some mu >= 2 and some s with 1 <= s, s^2 < mu, every price on Mat_mu(F_2) has D(mu) <= s D(1). Flat
  hypothesis: every finite subset of every Euclidean space, with its metric, is a price. Both are hypotheses on the
  field k, on which the notion of a price depends.
- Theorem D.2: at least one of the two holds. Its proof (Steps 1 to 8) shows that if the contracting hypothesis fails
  then, for every mu >= 3, there is a price on Mat_mu(F_2) with |a, a'|^2 = rank(a - a'), and from it a solid
  Euclidean cube. Remark D.3: "We do not show that the two cases exclude each other", "we do not know which case
  occurs", and "for mu >= 3 the price sqrt(rk(a - a')) of the proof above is not [Euclidean]".
- Where a circuit is looked into (Figure 1, Section 2.5). Two steps only: the decomposition lemma `lem_balanced`
  (flat case), which uses the part of the computed polynomial that is linear in each block of variables, and the
  evaluation lemma `lem_lowdeg` (contracting case), which uses its part of low degree. Section 2.5, in its paragraph
  on Boolean circuits, which is stated for circuits over F_2: a Boolean circuit for HC_m "amounts to an arithmetic
  circuit over F_2 that only has to be correct on the inputs 0 and 1", so it may compute any
  g = HC_m + sum_i (x_i^2 - x_i) h_i, and "for g these parts need have nothing to do with those of HC_m"; "The
  substitutions (marked P) are not the obstacle: they send inputs 0 and 1 to inputs 0 and 1 (cor_clauses_hc)."
- Lemma K.2 (evaluation of the part of low degree). For a commutative A-algebra R, a polynomial over R in the
  variables (place, symbol), n places, with a circuit of L gates, and d >= 0: a program of size O(log L + log n + d)
  with O((L + n)^3) constants has as value on every instance z with |z| < n, in (d + |z| + 1)(log(L + n + d))^(O(1))
  steps, "the sum of the homogeneous parts of degree at most d of the polynomial, evaluated at the indicator
  assignment of the word of z".
- Lemma K.3 and its proof. Hypotheses: integers a >= 0 and v >= v_0 with (lg v)^(Ca) <= v; R a field that is an
  A-algebra and in which 2 != 0 (for the permanent); PERM_m with m >= v^(B_0) has a circuit over R with at most v^a
  gates. Conclusion: R has an accelerator of size v^(C(a+1)) at scale v. In the proof, with n = v^(H-32) + 1 and
  t = v^(H+1), Phi is the sum over the words w of fewer than n symbols of the value of the universal automaton on w
  in t steps times the product of the variables that are 1 at the indicator assignment of w; it has degree at most n;
  it is a clause sum with v^(O(1)) literals; the circuit gives one with O(v^a) gates for Phi; Lemma K.2 with d = n
  turns it into a program whose value on every short v^H-plain instance z is sum(z) and whose runs take
  v^(H-32)((a + 1) lg v)^(O(1)) <= v^(H-16) steps. "The proof uses of the permanent only that Corollary E.2 holds for
  it, so the lemma holds for every family that is complete for grid sums (Appendix M), with constants that depend on
  the factor of the family, which takes the place of 3 in Corollary E.2."
- Corollary E.2 and Proposition M.2. A clause sum with q literals is HC_M of an M x M matrix, M >= 40 q, "whose
  entries are 0, 1 and single values W_n(x, r)", and "its entries are again affine in one variable each". By the
  proof of Corollary E.2 (page 32: "r_j = 1 contributes w_j - 1 times the indicators of the literals of the clause,
  and we put the factor w_j - 1 on the first literal") the single values include w_j - 1 for every clause weight
  w_j: the constant -1 for a clause of weight 0, y - 1 for a clause whose weight is a variable y, and a - 1 for a
  clause that carries an entry a of the automaton's matrices, which lie in the ring A [R, and read again by the
  coordinating session on page 32].

## 2. The ladder

Definition [D]. Let k be a field and c >= 1 an integer or infinity. A circuit over k is a *c-functional circuit for
HC_m* if the polynomial g that it computes satisfies g(x) = HC_m(x) for every x in {0,1}^(m x m) and has degree at
most c in each variable. S(c) is the statement: for some function q(m) that grows faster than every polynomial, every
c-functional circuit for HC_m over k has more than q(m) gates for all large m. It is a bound for all large m, not for
infinitely many.

Proposition 2.1 [D, immediate]. A 1-functional circuit for HC_m computes HC_m. So S(1) over every field follows from
Theorem 1.1 of the paper.

Proof. A polynomial of degree at most 1 in each variable is determined by its values on {0,1}^N (the monomials
restricted to the cube are linearly independent functions), and HC_m is such a polynomial.

Proposition 2.2 [D for (a); K for (b), not checked against a source by the writer, re-derived by the reviewer].

(a) Over F_2, the infinity-functional circuits for HC_m with s gates are, up to a constant factor in s, the Boolean
circuits over the basis {AND, XOR, 1} that compute the parity of the number of Hamiltonian cycles of a directed graph
on m vertices given by its adjacency matrix. So S(infinity) over F_2 is the statement that the least size of such
Boolean circuits exceeds every polynomial for all large m. It implies that the function has no Boolean circuits of
polynomial size, hence that parity-P is not inside P/poly (the function is in parity-P: guess a cycle through all
vertices and accept if every edge is present).

(b) The weaker, infinitely-often form (the parity of the number of Hamiltonian cycles has no polynomial-size
circuits) is implied by NP not inside P/poly: Valiant and Vazirani reduce satisfiability to its parity version by a
randomized reduction with one-sided error, the error is made exponentially small by repetition and the random bits
are then fixed for each input length, and the parity of satisfying assignments is a clause sum over F_2, hence the
value of HC_M at a 0/1 matrix (Corollary E.2 and Proposition M.2 over F_2, where -1 = 1). The almost-everywhere
statement S(infinity) is not known to follow from NP not inside P/poly. Neither form is known to imply NP not inside
P/poly.

Proof of (a). On inputs 0 and 1 a product gate over F_2 is AND and a sum gate is XOR, and the value of the polynomial
HC_m at a 0/1 matrix, read in F_2, is the number of Hamiltonian cycles modulo 2. Conversely a Boolean circuit over
that basis is an arithmetic circuit over F_2 whose polynomial has the same values on the cube.

What this means for the programme. The top of the ladder is a weaker target than NP not inside P/poly: it is implied
by it (in the infinitely-often form) and does not imply it.

Remark [K]. Functional lower bounds for restricted circuits are known: M. Forbes, M. Kumar and R. Saptharishi,
"Functional lower bounds for arithmetic circuits and connections to Boolean circuit complexity" (CCC 2016), for
depth three and depth four with low individual degree. For general circuits the question was empty before a lower
bound for S(1) existed.

## 3. The contracting case extends to bounded individual degree, over F_2

Proposition 3.1 [D, conditional on the paper; corrected after review, one gap named]. Suppose the contracting
hypothesis holds for the field F_2 itself. Suppose also that the matrix substituted for the clause sum Phi has O(n)
entries that are not constant [not verified: the paper describes the clause sum and does not print the count]. Then
the bound of the paper's Theorem K.7 holds for every c-functional circuit for HC_m over F_2, for every fixed c, and
more generally for c <= v^15 in the paper's parameters (a small fixed power of m).

Proof, as a list of the places where the paper's argument uses the circuit.

1. The paper's argument uses a circuit for the complete family only in Lemma K.3, and only to obtain an accelerator:
   a program whose value on every short v^H-plain instance z is sum(z), whose runs take at most v^(H-16) steps, and
   whose size and number of constants are v^(O(a+1)). Everything after Lemma K.3 (Lemma K.4, Proposition K.5, the
   diagonal argument) speaks of the accelerator only [R: confirmed on pages 57 to 59].
2. Let C be a c-functional circuit for HC_M over F_2 with at most v^a gates, computing g. Substitute into C the
   matrix A(y) of Proposition M.2 for the clause sum of Phi. The result is a circuit with O(v^a) gates for the
   polynomial G(y) = g(A(y)).
3. Degree. Each entry of A(y) is constant or affine in one variable, and g has degree at most c in each of its
   variables, so the degree of G is at most c times the number E of non-constant entries of A(y) [R for the bound
   cE]. Under the second hypothesis E = O(n).
4. Values. Over F_2 the ring A of the paper is a subring of F_2, so every scalar is 0 or 1, and at the indicator
   assignment y(z) of the word of a short plain instance z every entry of A(y(z)), being 0, 1, w - 1 with w in
   {0, 1}, or y - 1 with y in {0, 1}, is 0 or 1. Hence G(y(z)) = g(A(y(z))) = HC_M(A(y(z))) = Phi(y(z)) = sum(z).
5. Lemma K.2, applied to the circuit of step 2 with d = cE, gives a program whose value at z is the sum of the
   homogeneous parts of degree at most cE of G at y(z), which is G(y(z)) = sum(z) by steps 3 and 4, in
   (cE + |z| + 1)(log(L + n + cE))^(O(1)) steps. With E = O(n), n = v^(H-32) + 1 and c <= v^15 this is at most
   v^(H-16) for large v, as in the paper's proof. The program's size O(log L + log n + cE) is at most v^(C(a+1)) for
   C >= H, as Lemma K.3 already needs for d = n. This is an accelerator of the size the paper needs.

What the proposition is not.

- It is not a statement over a general field. Over a field in which -1 != 1 the matrix A(y(z)) has the entry -1 for
  every clause of weight 0, and over any field other than F_2 the entries a - 1 of the automaton need not be 0 or 1;
  a functional circuit owes nothing at such a matrix, and step 4 fails (finding J1; the first version of this note
  stated the proposition for every field, wrongly). A statement over a general field would need a reduction to HC
  whose matrix is 0/1 at the indicator assignments, for the forbidding clauses and for the automaton's weights. [Q]
- The contracting hypothesis for F_2 is not the hypothesis the paper's Theorem M.3 uses in characteristic 2: that
  theorem passes to the algebraic closure of the prime field (Lemma M.1), where the ring A may contain other
  elements. So the proposition does not follow from "the paper's theorem is in its contracting case in
  characteristic 2".
- It is conditional on a hypothesis that is not known to hold.
- It says nothing for c = infinity: a Boolean circuit of s gates gives a polynomial whose degree in a variable can be
  2^s.

Remark [D]. The degree cannot be taken out of the hypothesis by this route. A polynomial g that agrees with HC_m on
the cube has degree at least m (its multilinear reduction is HC_m), and a functional circuit with no bound on the
individual degree may have degree far above the running time t of the instances, while the accelerator must run in
fewer steps than the instances it replaces. For an exact circuit the degree that matters is the degree n of Phi in
the variables of the word, which is far below t; this is the place where the algebraic model is stronger than the
Boolean one in the paper's contracting case, and it agrees with the paper's sentence "Nor can a large Boolean
circuit take the place of the program that the contracting case refutes, since we know no way to run it faster than
gate by gate."

## 4. The flat case at c = 2: where the decomposition stops

Setting [P]. f = f_(k,l) is linear in each of k blocks of variables x_(a,rho), a = 1..k. Its tensor T has one index
rho_a per block, and T[rho] = f(e_rho), the value at the input that is 1 exactly at x_(a,rho_a), a = 1..k. The
decomposition lemma writes f, from a circuit with L gates, as a sum over the balanced sets S of blocks of
polynomials f_S whose tensor has rank at most L across S.

Lemma 4.1 [D, R]. Let T be any tensor of the form T[rho] = prod over pairs a < b of E_ab[rho_a, rho_b], where each
E_ab is a matrix of rank at most R. Then there is a polynomial g of degree at most k - 1 in each block, with a
circuit of O(k^2 R N) gates (N the largest number of variables in a block), such that g(e_rho) = T[rho] for every
rho. For the complete network f_(k,l), R = 2^l and the circuit has size polynomial in the number of variables.

Proof. For each pair a < b write E_ab[i, j] = sum over s <= R of u_s^(ab)[i] v_s^(ab)[j] and put
U_s^(ab)(x_a) = sum_i u_s^(ab)[i] x_(a,i), V_s^(ab)(x_b) = sum_j v_s^(ab)[j] x_(b,j), linear forms. Then
g = prod over a < b of (sum_s U_s^(ab)(x_a) V_s^(ab)(x_b)) has degree k - 1 in each block, and at a one-hot input
each linear form takes the value of its coefficient vector at the selected index.

Consequence. The values of f at one-hot inputs, which are all that the tensor T records, do not carry a functional
lower bound once the degree in a block may reach k - 1: the polynomial of Lemma 4.1 agrees with f on all one-hot
inputs, not on the cube. A functional bound has to use inputs in which a block has several ones.

Observation 4.2 [D, a description of the obstruction, not a theorem]. Let g have degree at most 2 in each block and
agree with f on the cube. Then T[rho] is the sum, over the multi-degrees e in {1,2}^k, of the coefficients in g of
the monomials prod_a x_(a,rho_a)^(e_a): the multilinear reduction of g is f, and these are the monomials of g that
reduce to prod_a x_(a,rho_a). In characteristic other than 2 a multi-homogeneous component of g polarizes to a
polynomial that is linear in each of at most 2k copies of blocks, to which the decomposition lemma applies (over F_2
polarization divides by 2 and the copies would have to be separated otherwise); but a balanced set of copies may
contain one copy of a block and miss the other. Restricted to the diagonal, a piece is then sum_j u_j[rho_A]
v_j[rho_B] with A and B sets of blocks that overlap. In the network that bounds such a piece a shared block is wired
to both hubs. If every block is shared the piece is a pointwise product sum_j u_j[rho] v_j[rho], which is no
restriction at all (take one term, u = T, v = 1), and the comparison of lengths (2.4) of the paper holds trivially.
So the argument of the flat case gives a bound only for pieces with few shared blocks, and a circuit can put all
its weight on the others.

[Q] S(2) in the flat case: is there a superpolynomial bound for circuits that compute a polynomial of degree at most
2 in each variable (or in each block) agreeing with f_(k,l), or with HC_m, on the cube? Neither a proof nor a
circuit is known to the coordinating session.

## 5. Which case occurs

Proposition 5.1 [P for the content, D for the packaging, R]. For mu >= 3: the contracting hypothesis holds with this
mu (and some s) if and only if the metric sqrt(rank(a - a')) on Mat_mu(F_2) is not a price.

Proof. If sqrt(rank) is a price on Mat_mu(F_2) then D(mu) = sqrt(mu) D(1) for it and no s with s^2 < mu works. If it
is not a price, Steps 1 to 7 of the proof of Theorem D.2, which are written for one fixed mu >= 3, show that the
contracting inequality cannot fail for every s < sqrt(mu).

Proposition 5.2 [D, R: steps (i) to (v) re-derived by the reviewer]. A metric on Mat_2(F_2) pulled back from a
CAT(0) space with D(2)^2 = 2 D(1)^2 > 0 is a constant times sqrt(rank).

Proof. Let F map Mat_2(F_2) into a CAT(0) space Y with D(2)^2 = 2 D(1)^2. As in Steps 1 and 3 of the paper, every
quadrilateral F(a), F(a + W), F(a + W + W'), F(a + W') with W, W' transversal of rank one has equality in Lemma
C.4(b): the squared diagonals add up to the squared sides.

(i) In a CAT(0) space, a quadrilateral x, y, v, u with |xv|^2 + |yu|^2 = |xy|^2 + |yv|^2 + |vu|^2 + |ux|^2 has
diagonals with the same midpoint. Indeed let m be the midpoint of [x, v]. By the CN inequality (Lemma C.4(a))
|ym|^2 <= (|yx|^2 + |yv|^2)/2 - |xv|^2/4 and the same for u; adding, |ym|^2 + |um|^2 <= |yu|^2/2. Since
|ym| + |um| >= |yu|, also |ym|^2 + |um|^2 >= |yu|^2/2. So |ym| = |um| = |yu|/2, and m is the midpoint of [y, u].

(ii) For V of rank two write m(a, V) for the midpoint of [F(a), F(a + V)]. If V = W + W' with W, W' of rank one
(they are then transversal), the quadrilateral at a has the diagonals [F(a), F(a + V)] and [F(a + W), F(a + W')],
and a + W' = (a + W) + V. By (i), m(a, V) = m(a + W, V). The rank-one summands W of an invertible V span Mat_2(F_2)
[MV: six summands of the identity, span of dimension 4; the same for every V by the action of GL_2 x GL_2], so
m(a, V) = M_V does not depend on a.

(iii) For invertible V, V', the CN inequality at the midpoint M_V of [F(b), F(b + V)], applied to the point M_V',
gives |M_V' M_V|^2 <= (r'(b)^2 + r'(b + V)^2)/2 - r(b)^2 with r(b) = |F(b) M_V| and r'(b) = |F(b) M_V'|. The mean
over b is |M_V' M_V|^2 <= mean(r'^2) - mean(r^2). Exchanging V and V' and adding, M_V = M_V' = M.

(iv) So |F(b) M| = |F(b + V) M| for all b and all invertible V. The invertible matrices span Mat_2(F_2) [MV], hence
|F(b) M| = rho for all b, and |F(b), F(b + V)| = 2 rho for every V of rank two.

(v) For W of rank one put n_a(W) = |F(a), F(a + W)|^2. Opposite sides of a quadrilateral with equality are equal
(Lemma C.4(b)), so n_(a + W')(W) = n_a(W) for W' transversal to W; the rank-one matrices transversal to W span
Mat_2(F_2) [MV], so n_a(W) = n(W). The equality for the quadrilateral reads 8 rho^2 = 2 n(W) + 2 n(W'), that is
n(W) + n(W') = 4 rho^2 for every transversal pair. The graph of transversal pairs on the nine matrices of rank one
is connected and contains a triangle [MV], so n(W) = 2 rho^2 for every W. Hence |F(a), F(a')|^2 = 2 rho^2
rank(a - a').

Corollary 5.2' [D, with the paper's Proposition C.3 and Steps 1 and 2]. The contracting hypothesis holds with mu = 2
(and some s with s^2 < 2) if and only if sqrt(rank) on Mat_2(F_2) is not a price. Chain: by Proposition C.3 every
price is pulled back from a CAT(0) space; Step 1 of the paper with i = j = 1 gives D(2)^2 <= 2 D(1)^2 for every
price; if the inequality D(2) <= s D(1) fails for every s < sqrt(2), Step 2 (scaling to D(1) = 1 and compactness,
valid for mu = 2) gives a price with D(1) = 1 and D(2)^2 = 2, which is sqrt(rank) by Proposition 5.2; the converse
is as in Proposition 5.1.

Proposition 5.3 [D, R]. For every mu >= 1 the metric space (Mat_mu(F_2), sqrt(rank(a - a'))) is isometric to a
subset of a CAT(0) space, namely of the Euclidean cone over the spherical building of GL_(2 mu)(F_2).

Proof. Put N = 2 mu and write F_2^N = F_2^mu + F_2^mu. For a in Mat_mu(F_2) let G_a = {(x, ax)}, a subspace of
dimension mu. Then G_a meets G_b in {(x, ax) : (a - b)x = 0}, of dimension mu - r with r = rank(a - b). Let Delta be
the spherical building of type A_(N-1) over F_2: the complex of flags of proper nonzero subspaces, with the metric
in which the apartment of a basis e_1, ..., e_N is the unit sphere of {x in R^N : sum x_i = 0} and the vertex of the
subspace spanned by {e_i : i in S} is the unit vector in the direction 1_S - (|S|/N) 1. With this metric Delta is a
CAT(1) space, any two points lie in a common apartment, and distances are those of the apartment [K: Bridson and
Haefliger, Metric spaces of non-positive curvature, Theorem II.10A.4; Charney and Lytchak, 2001]. Choose a basis of
G_a meet G_b, extend it to bases of G_a and of G_b (together mu + r independent vectors, a basis of G_a + G_b), and
extend to a basis of F_2^N. In its apartment G_a and G_b are the vertices of two sets S, S' of size mu with
|S meet S'| = mu - r. The vectors u_S = 1_S - (1/2) 1 have <u_S, u_S'> = (mu - r) - mu/2 and |u_S|^2 = mu/2, so the
angle theta between the two vertices has cos(theta) = 1 - 2r/mu. The Euclidean cone over a CAT(1) space is CAT(0)
[K: Berestovskii; Bridson and Haefliger, Theorem II.3.14], and the points P_a at distance rho from the apex on the
rays of the G_a have |P_a P_b|^2 = 2 rho^2 (1 - cos(theta)) = 4 rho^2 r/mu. With rho = sqrt(mu)/2 this is
rank(a - b).

Consequences.

- Nonpositive curvature cannot decide between the two cases: every inequality that holds for all finite subsets of
  all CAT(0) spaces holds for sqrt(rank).
- Proposition 5.4 [D, R for mu <= 4; for every mu >= 2 in the note
  `2026-11-24-hilbert-maps-contract-for-every-mu.md`, unit PNP-006, review pending]. For maps of Mat_mu(F_2) into a
  Hilbert space, D(mu)^2 <= (2 - 2^(1-mu)) D(1)^2, with equality for the map a -> (-1)^(a_11). In particular
  sqrt(rank) is not a Euclidean metric, and every Euclidean price satisfies the contracting inequality with
  s^2 = 2 - 2^(1-mu) < mu, so only a non-Euclidean price can make it fail.
  Proof for mu <= 4. For a map F into a Hilbert space, D(r)^2 = sum over characters B of 4 p_r(B) |F^(B)|^2 by
  Parseval, where F^ is the Fourier transform on the group Mat_mu(F_2), chi_B(W) = (-1)^(trace(B^T W)), and p_r(B) is
  the fraction of the matrices W of rank r with chi_B(W) = -1. So the largest ratio is the maximum over B != 0 of
  p_mu(B)/p_1(B). For B of rank one, p_1 = (2^(mu-1)/(2^mu - 1))^2 and p_mu = 2^(mu-1)/(2^mu - 1), ratio
  2 - 2^(1-mu). For mu <= 4 the maximum over all B is attained at rank one [MV: 3/2, 7/4, 15/8].
- One direction of duality [P for the principle, D for the use, R]. A spectral point is monotone under restriction
  and subadditive, so if a product of wires t is obtained, in the asymptotic sense of the paper's duality theorem
  (`thm_duality`), from few restrictions of a product of wires s, then every price gives t at most the length of s.
  One such conversion between products of wires on the parties Mat_mu(F_2), with a shorter source than target in the
  metric sqrt(rank), would therefore prove the contracting hypothesis (by Proposition 5.1 or Corollary 5.2'). The
  converse is not available: prices do not form a convex set (the sum of the cut metrics of two crossing cuts
  violates Lemma C.4(b), while each cut metric is the price of a flattening rank), so the absence of such
  conversions would not make sqrt(rank) a price.

[Q] The first instance. Is the metric on the sixteen matrices of Mat_2(F_2) with distance 1 between matrices that
differ by rank one and sqrt(2) otherwise a price over some field? Equivalently (Corollary 5.2'), does the
contracting hypothesis hold with mu = 2? A first reading of the paper's Appendices A and B and of the literature
(unit PNP-003, 2026-11-24) found nothing that decides even its four-point sub-question, whether the Euclidean unit
square is a price.

## 6. What is not claimed

No statement on P against NP. On NP against P/poly only what Proposition 2.2(b) records as known: the top of the
ladder, in its infinitely-often form, is implied by NP not inside P/poly and is not known to imply it. No statement
on Boolean circuits of unbounded degree. No statement on which case occurs. Proposition 3.1 is conditional on the
paper, on the contracting hypothesis for F_2 and on a count that is not verified. The metric statements of
Propositions 5.2 and 5.3 depend only on standard facts on CAT(0) spaces; their use for the contracting hypothesis
depends on Proposition C.3 and on Steps 1 and 2 of the paper.

## How could this be wrong?

- The paper is one day old and unread by a human mathematician; its Lean statements were not compared here with the
  statements quoted.
- Proposition 3.1 rests on the count E = O(n) of the non-constant entries of the substituted matrix, which the paper
  describes and does not print. If it fails the proposition holds only for c below a smaller bound, or not at all.
- Realized risk (J1): the substituted matrix has the entry -1 in every characteristic other than 2, and entries
  a - 1 with a in the ring A over any field other than F_2. The proposition is therefore stated for F_2 only.
- The contracting hypothesis for F_2 and the one for the algebraic closure of F_2 are different hypotheses; the
  paper's theorem in characteristic 2 uses the second.
- The statements on complexity classes in Proposition 2.2 (Valiant and Vazirani with fixed random bits; membership
  in parity-P) were not checked against a source by the writer; the reviewer re-derived them.
- In Proposition 5.3 the metric on the building is the standard one, in which each apartment is a round sphere; the
  angle formula was derived here from the coordinates of the Coxeter complex and re-derived by the reviewer, not
  looked up.
- Step (i) of Proposition 5.2 uses only the CN inequality and the triangle inequality; steps (ii) to (v) use the
  finite facts of EXP-001. An error in the reading of "transversal" (independent column spaces and independent row
  spaces) would change them.

## Findings of the review of 2026-11-24, all applied

Report in the coordination repository, `wip/caos-research/pnp-001-ladder-and-two-cases-review-2026-11-24.md`.

- J1 (blocker): Proposition 3.1 was stated over every field; its step 4 holds over F_2 only. Restated, with the
  distinction between F_2 and its algebraic closure and the general field marked open.
- J2 (blocker): Proposition 2.2(b) said that the top of the ladder does not follow from NP not inside P/poly. It does,
  in the infinitely-often form (Valiant and Vazirani). Rewritten; Section 6 aligned.
- J3 (major): S(infinity) is a bound for all large m and was equated with "no polynomial-size circuits". Separated.
- J4 (major): Section 1 omitted that the single values of Proposition M.2 are clause weights minus one and that the
  sentence on inputs 0 and 1 is stated over F_2. Added.
- J5 to J12 (minor): Steps 1 to 7 in Proposition 5.1; characteristic other than 2 and the reason for the identity in
  Observation 4.2; Corollary 5.2' written out and Section 6 reworded; three risks added; the sentence on Euclidean
  prices made unambiguous; the size of the program of Lemma K.2 in step 5; the attribution of the definition of a
  price and the hypotheses of Lemma K.3 restored, "follows from" in Proposition 2.1; the notation of Lemma 4.1.
- A wrong sentence of the first draft, found by the writer before the first commit (an equivalence by duality), is
  recorded in the history log.
