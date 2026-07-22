# Symmetrization dossier: extracting a symmetric / gradient / Hessian-nilpotent witness from the Alpoge-Fable counterexample

Date: 2026-07-22. Compiled from primary sources (full texts of de Bondt-van den Essen PAMS 2005, Zhao arXiv:math/0409534v2, Bass-Connell-Wright Bull. AMS 1982 were downloaded and read; local sympy re-verification of the counterexample and of the key construction identities was performed). Anything not confirmed against a primary source is marked UNVERIFIED.

## 0. The input object (verified locally with sympy, 2026-07-22)

The Alpoge-Fable counterexample (announced by Levent Alpoge on 2026-07-19, credited to work with the AI system Fable). With u = 1 + xy:

    P = u^3 z + y^2 u (4 + 3xy)
    Q = y + 3x u^2 z + 3x y^2 (4 + 3xy)
    R = 2x - 3x^2 y - x^3 z

F = (P, Q, R) : C^3 -> C^3.

Verified exactly in sympy (E:\_Temp\jc-dossier\verify_alpoge.py, CAOS_MANAGE .venv, sympy):

- det JF = -2 identically (so F is a Keller map after the trivial scaling normalization).
- Component total degrees: (7, 6, 4). Expanded monomial counts: P has 7, Q has 6, R has 3 monomials (16 total; the map is very sparse).
- THREE-point collision (not two, correcting the task premise):
  F(0, 0, -1/4) = F(1, -3/2, 13/2) = F(-1, 3/2, 13/2) = (-1/4, 0, 0).
- The map is generically three-to-one (Secret Blogging Seminar post; the weighted grading deg(x, y, z) = (-1, 1, 2) makes (P, Q, R) weighted homogeneous of weights (2, 1, -1)).

Consequence: JC is false for every n >= 3 (pad with identity coordinates). n = 2 remains open.

## 1. Task 1: the de Bondt-van den Essen symmetric reduction (primary source, full text read)

Source: M. de Bondt, A. van den Essen, "A reduction of the Jacobian conjecture to the symmetric case", Proc. Amer. Math. Soc. 133 (2005), no. 8, 2201-2205. S 0002-9939(05)07570-2, DOI 10.1090/S0002-9939-05-07570-2. Received 2003-06-30, published electronically 2005-03-04. Preprint: Report No. 0308, University of Nijmegen, June 2003. No arXiv version found (UNVERIFIED that none exists; none surfaced in searches). Full text obtained from the AMS site and extracted; quotes below are from that text.

Setting: everything is over C. C[x] = C[x_1, ..., x_n], H = (H_1, ..., H_n) : C^n -> C^n polynomial. h(f) denotes the Hessian matrix of f. By the Poincare lemma, JH is symmetric iff H = grad f for some f in C[x].

### 1.1 The construction (their equation (3))

Introduce n new variables y_1, ..., y_n and associate to H the polynomial f_H in C[x, y]:

    f_H := (-i) [ H_1(x_1 + i y_1, ..., x_n + i y_n) y_1 + ... + H_n(x_1 + i y_1, ..., x_n + i y_n) y_n ]

i.e. f_H(x, y) = -i * sum_j H_j(x + iy) y_j, a polynomial in 2n variables. With the invertible linear map

    S := (x_1 - i y_1, ..., x_n - i y_n, y_1, ..., y_n)     (det S = 1)

one has g_H := f_H o S = -i * sum_j H_j(x) y_j, and (their equation (4))

    h(g_H) = [ *              (-i)(JH)^t ]
             [ (-i) JH        0          ]

Note: it is essential that i = sqrt(-1) appears; the base field must contain a square root of -1 (the paper works over C). This is not an artifact: over R the construction cannot work, because the only Hessian-nilpotent polynomial with real coefficients is 0 (see Section 2.5).

### 1.2 Exact statements

Hessian Conjecture HC(n) (their formulation): "Let f in C[x]. If h(f) is nilpotent, then F := (x_1 + f_{x_1}, ..., x_n + f_{x_n}) is invertible."

Lemma 1.2 (verbatim): "Let H = (H_1, ..., H_n) : C^n -> C^n and let f_H in C[x, y] be as defined in (3). Then JH is nilpotent iff h(f_H) is nilpotent."

The proof gives the exact characteristic-polynomial identity (their (6)-(7)):

    det(z I_2n - h(f_H)) |_{S(x,y)} = det(z I_n - JH) det(z I_n - (JH)^t)

so char(h(f_H)) = z^{2n} iff char(JH) = z^n.

Theorem 1.1 (verbatim): "The Jacobian Conjecture is equivalent to the Hessian Conjecture. More precisely, if HC(2n) holds, then x + H is invertible for every H : C^n -> C^n with JH nilpotent."

Corollary 1.3 (verbatim): "It suffices to prove the Jacobian Conjecture for all n >= 2 and all F of the form F = (x_1 + f_{x_1}, ..., x_n + f_{x_n}), where h(f) is nilpotent and f is homogeneous of degree 4 (or equivalently for all n >= 2 and all F of the form F = x + H with JH nilpotent and symmetric and H homogeneous of degree 3)." (Combines Theorem 1.1 with the Bass-Connell-Wright cubic homogeneous reduction; if H is homogeneous of degree 3, then f_H is homogeneous of degree 4 in (x, y).)

Hypotheses summary: base field C (char 0, contains i); Theorem 1.1 and Lemma 1.2 need only "JH nilpotent", NOT homogeneity; homogeneity of degree 3 enters only through Corollary 1.3 to get a homogeneous quartic potential.

### 1.3 Direction of the reduction: it IS constructive and preserves non-invertibility

This is the decisive point for the program. The proof of Theorem 1.1 shows (displayed formula in the paper, re-verified symbolically, see 1.4): with Ftil := id_{2n} + grad f_H,

    S^{-1} o Ftil o S = ( x + H(x),  y + (JH(x))^t y - i H(x) )

This conjugated map is TRIANGULAR over the x-block: its first n components are exactly F = x + H, and its last n components are AFFINE in y with matrix I + (JH(x))^t, which is invertible for every x (JH nilpotent). Therefore:

    Ftil is invertible  <=>  F = x + H is invertible.   (Equivalence, both directions.)

The paper states only the direction it needs ("Hence S^{-1} o F o S = (x_1 + H_1(x), ..., x_n + H_n(x), *, ..., *) is invertible, which in turn implies that x + H is invertible"), but the converse is immediate from the same displayed formula, and it yields an EXPLICIT collision witness (derivation ours, from the paper's formula; verified symbolically at the level of the identity):

Given u != v in C^n with F(u) = F(v) (so H(u) - H(v) = v - u), define

    w := i (I + (JH(v))^t)^{-1} (u - v),   where (I + (JH(v))^t)^{-1} = sum_{k=0}^{nu-1} (-(JH(v))^t)^k  (finite sum, JH nilpotent of index nu).

Then the conjugated map collides at (u, 0) and (v, w), hence the symmetric Keller map Ftil = id + grad f_H collides at the two distinct points

    p_1 = S(u, 0) = (u, 0)        and        p_2 = S(v, w) = (v - i w, w).

Check by construction: first block u + H(u) = v + H(v); second block 0 + (JH(u))^t 0 - iH(u) versus w + (JH(v))^t w - i H(v); by choice of w, (I + (JH(v))^t) w = i(H(u) - H(v)), equality holds. All arithmetic is in Q(i) if u, v, H are rational.

So: a non-invertible Keller map x + H with JH nilpotent in dimension n yields an explicit non-invertible SYMMETRIC (gradient) Keller map id + grad f_H in dimension 2n, with an explicit 2-point collision certificate. The reduction is NOT merely a contrapositive at conjecture level.

Caveat: the input must have JH NILPOTENT. The raw Alpoge-Fable map does not qualify (det JF = -2; even after normalizing JF(0) = I, JF - I is not nilpotent). One must first pass through the BCW reduction (Section 3) or use an already-computed nilpotent form (Section 5).

### 1.4 Local symbolic validation

E:\_Temp\jc-dossier\verify_dbvde_identity.py (sympy, exact): for a sample nonhomogeneous H with JH nilpotent, (a) Hess(f_H) is nilpotent (index 3), (b) the triangular conjugation identity S^{-1} o (id + grad f_H) o S = (x + H, y + (JH)^t y - i H) holds identically. Both passed.

### 1.5 Companion papers (cited from within the PAMS paper and Zhao; full texts NOT fetched, statements are as quoted there)

- M. de Bondt, A. van den Essen, "Nilpotent symmetric Jacobian matrices and the Jacobian Conjecture", J. Pure Appl. Algebra 193 (2004), no. 1-3, 61-70. (Report No. 0307, Nijmegen, June 2003.) Contains Theorem 2.1 quoted in the PAMS paper: (i) if the symmetric dependence problem SDP(p) has an affirmative answer for all p <= n, then HC(n) holds; (ii) variant for the homogeneous case. Formulates the (homogeneous) symmetric dependence problems.
- M. de Bondt, A. van den Essen, "Nilpotent symmetric Jacobian matrices and the Jacobian Conjecture II", J. Pure Appl. Algebra 196 (2005), 135-148. (Report No. 0318, Nijmegen, Nov 2003.) Per Zhao's survey of it: JC holds for symmetric F = x + H with JH nilpotent when n <= 4 (H not necessarily homogeneous), and when n = 5 with H homogeneous.
- A. van den Essen, S. Washburn, "The Jacobian Conjecture for symmetric Jacobian matrices", J. Pure Appl. Algebra 189 (2004), no. 1-3, 123-133: the case n <= 4, H homogeneous.

Consequence for us: any non-invertible symmetric Keller map needs dimension >= 5 (>= 6 in the homogeneous case). Our construction below lands in dimension 48; smaller symmetric witnesses may exist but none are known (UNVERIFIED).

## 2. Task 2: Zhao's Hessian-nilpotency formulation (primary source, full text read)

Source: Wenhua Zhao, "Hessian nilpotent polynomials and the Jacobian conjecture", arXiv:math/0409534v2 [math.CV] (2 Nov 2004); published Trans. Amer. Math. Soc. 359 (2007), 249-274. Quotes from the arXiv v2 full text.

Conventions: F(z) = z - H(z), o(H) >= 2; P is HN (Hessian nilpotent) iff Hes P = (d^2 P / dz_i dz_j) is nilpotent; Delta = sum_i d^2/dz_i^2; Q_t(z) is the deformed inversion pair: G(z) = z + t grad Q_t is the formal inverse of F(z) = z - t grad P. All results hold over any Q-algebra in place of C (paper, Section 1 final remarks), EXCEPT that HN-ness itself forces complex coefficients (see 2.5).

### 2.1 The key identities

Theorem 3.4 (verbatim, for HN P): "Q_t^k(z) = k! sum_{m=0}^inf t^m / (2^m m! (m+k)!) Delta^m P^{m+k}(z)" (their Eq. (3.8)); in particular Q_[m] = Delta^{m-1} P^m / (2^{m-1} m! (m-1)!) (Eq. (3.9)).

Theorem 4.3: For any P with o(P) >= 2: P is HN iff Delta^m P^m = 0 for all m >= 1 iff Delta^m P^m = 0 for 1 <= m <= n. (Finite criterion for Hessian nilpotency.)

### 2.2 The vanishing conjecture and the exact equivalence

Conjecture 7.1 (Vanishing Conjecture, verbatim): "For any HN (not necessarily homogeneous) polynomial P(z) of degree d >= 2, its deformed inversion pair Q_t(z) is a polynomial in both t and z. More precisely, Delta^k P^{k+1} = 0 when k >> 0."

Theorem 7.2 (verbatim): "The following statements are equivalent. (1) The vanishing conjecture for homogeneous HNP of degree d = 4. (2) The vanishing conjecture for homogeneous HNP of degree d >= 2. (3) The vanishing conjecture. (4) The Jacobian conjecture." (The quantifier is over ALL dimensions n on both sides.)

Conjecture 7.3 (Homogeneous Vanishing Conjecture, verbatim): "For any homogeneous HNP P(z) of degree d >= 2, we have (1) Delta^m P^{m+1} = 0 for any m > alpha[n,d] := (1/(d-2)) ((d-1)^{n-1} - (d-1)). (2) For any k >= 1, Delta^m P^{m+k} = 0 for any m > k alpha[n,d]." For d = 4: alpha[n,4] = (3^{n-1} - 3)/2 = (3/2)(3^{n-2} - 1), the bound in the abstract. Proposition 7.4: (1) and (2) are equivalent; Conjecture 7.3 (for d >= 2, or just d = 4) is equivalent to JC.

Theorem 6.2 (for any HN power series P): "Delta^m P^{m+k} = 0 when m >> 0 for any k >= 1" iff "for some k_0" iff "Delta^m P^{m+1} = 0 when m >> 0".

### 2.3 Construction direction: Keller counterexample -> failing HN quartic

Chain (all constructive):

1. Non-invertible Keller map in dim 3 (Alpoge-Fable) -> BCW cubic homogeneous non-invertible Keller map G = U + H, JH nilpotent, dim N (Section 3; explicitly N = 24, Section 5).
2. dBvdE: f_H = -i sum_j H_j(x + iy) y_j, homogeneous quartic in dim 2N = 48; Ftil = id + grad f_H non-invertible symmetric Keller, explicit collision (Section 1.3).
3. Zhao sign convention: write Ftil(z) = z - grad P_star with

       P_star := -f_H(x, y)     (homogeneous HN quartic in n = 48 variables).

   P_star is HN (Lemma 1.2 + Theorem 4.3). Since Ftil is not invertible, its formal inverse z + grad Q (Q = Q_{t=1}) is not polynomial; by Theorem 3.4 / Theorem 6.2, Delta^m P_star^{m+1} != 0 for INFINITELY MANY m. So P_star falsifies the Vanishing Conjecture (Conjecture 7.1 and 7.3), consistent with Theorem 7.2 and JC(48) being false.

Certificates, honestly stated:
- "P_star is HN": finitely checkable (Delta^m P_star^m = 0 for m = 1..48, or directly char(Hes P_star) = z^48 via the dBvdE char-poly identity, which reduces it to char(JH) = z^24).
- "Vanishing fails for P_star": the FINITE certificate is the explicit 2-point collision of z - grad P_star (Section 1.3), not a direct computation of some Delta^m P_star^{m+1} != 0; the guaranteed non-vanishing range starts beyond alpha[48,4] = (3^47 - 3)/2, astronomically out of computational reach. Low-m non-vanishing (e.g. Delta P_star^2 != 0) is expected and cheap to compute, and indeed MUST hold: Zhao notes (via his Corollary 3.9) that Conjecture 7.1 holds for any HNP with Delta P^2 = 0, so a failing P_star necessarily has Delta P_star^2 != 0. This is a good sanity check but is not by itself a disproof of anything.

### 2.4 Dimension bookkeeping in Zhao's equivalence

Zhao's Theorem 7.2 equivalence quantifies over all n. Concretely, the failure of JC at n = 3 forces the failure of the Vanishing Conjecture for at least one homogeneous HN quartic in SOME dimension; the pipeline above produces one explicitly in dimension 48 (via the current best explicit nilpotent form; any future smaller cubic-homogeneous form of dimension N gives 2N). Zihan Zhang's July 2026 note (Section 5) states the same consequence non-constructively ("in some dimension").

### 2.5 Reality obstruction

Zhao (Section 7, citing van den Essen-Washburn Theorem 4.1): "the only HNP's (not necessarily homogeneous) P(z) in R[z] (o(P(z)) >= 2) with real coefficients are P(z) = 0." Therefore the failing quartic necessarily has non-real coefficients; the i in the dBvdE construction is unavoidable. Work in Q(i).

## 3. Task 3: the reduction ladder to cubic homogeneous (BCW 1982, Druzkowski 1983)

### 3.1 Bass-Connell-Wright (primary source, full text read)

Source: H. Bass, E. H. Connell, D. Wright, "The Jacobian conjecture: reduction of degree and formal expansion of the inverse", Bull. Amer. Math. Soc. (N.S.) 7 (1982), 287-330. Full text obtained from AMS (open access).

Reduction Theorem (2.1) (statement, over any commutative ring k): given F in MA1_n(k) with invertible Jacobian, there exist m >= 0, elementary automorphisms G, H in EA1_{n+m}(k), and F(T) in MA_{n+m}(k[T]) such that F(1) = G o F^[m] o H (so F invertible iff the new map is), and the induced element L in MA_r(k), r = n + m + 1, has the form L = X_r + N with N CUBIC HOMOGENEOUS, linear in each variable except quadratic in T, and J(N) NILPOTENT. Corollary (2.2): JC for all cubic homogeneous maps with nilpotent Jacobian (all n) implies JC.

The three constructive steps (their Sections 3-4):

1. Reduction to degree <= 3 (Proposition (3.1)): repeatedly pick a top-degree monomial aM in some F_i, factor aM = PQ with deg P, deg Q <= d - 2, and pass to dimension n + 2 via H = (X, X_{n+1} + P, X_{n+2} + Q) and an elementary G, replacing F_1 by F_1 - (X_{n+1} + P)(X_{n+2} + Q). Each step adds 2 variables and reduces (d, e) lexicographically (e = number of top-degree monomials). A refinement makes the map linear in each variable.
2. Making J(F) unipotent: from a degree <= 3 map F = F_(1) + F_(2) + F_(3) in dimension p := n + m_0, pass to dimension 2p via F' = (X, Y) + N, N = (F_(2) + Y, -F_(3)); their Lemma (4.1) (graded-ring lemma: 1 + a invertible iff a nilpotent for a homogeneous of positive degree) shows J(N) is nilpotent. DIMENSION DOUBLES.
3. Homogenization: add one variable T; L = (F(T), T) = (X, T) + (N(T), 0), N(T) = N_(1) T^2 + N_(2) T + N_(3) cubic homogeneous in (X, T), J_X(N) nilpotent. DIMENSION + 1.

Dimension count from the primary source: r = 2(n + 2s) + 1, where s = number of monomial-splitting steps in step 1 (each step adds 2 variables; s depends on the monomial structure, not just on (n, d); no closed-form bound is stated in the paper). For the Alpoge-Fable map (n = 3, 16 monomials, degrees (7, 6, 4)) a naive count gives s of order 20-40 before optimization, i.e. a three-digit naive dimension; sparsity-aware choices do far better (see the explicit 24 below).

Invertibility transfer is an equivalence at every step (composition with elementary automorphisms and extension by identity), so collisions push through the whole ladder mechanically: if F(u) = F(v), then L(H^{-1}-image data) collides correspondingly; all steps are explicit polynomial substitutions.

### 3.2 Druzkowski cubic-linear form

Source: L. M. Druzkowski, "An effective approach to Keller's Jacobian conjecture", Math. Ann. 264 (1983), 303-313. (Citation verified via multiple secondary sources, incl. Gorni-Zampieri; full text NOT fetched, paywalled.) Statement: it suffices to prove JC for all maps of cubic-linear (Druzkowski) form F = X + (AX)^{*3}, i.e. F_i = x_i + (sum_j a_ij x_j)^3, in all dimensions.

Constructive pairing: G. Gorni, G. Zampieri, "On cubic-linear polynomial mappings", Indag. Math. (N.S.) 8 (1997), no. 4, 471-492. A cubic homogeneous map f = x + H in dim n with H(x) = B (Cx)^{*3} (B an n x q matrix, C a q x n matrix) pairs with a cubic-linear map in dimension N = n + q; each is invertible iff the other is, with explicit formulas both ways. Writing the 54 cubic monomials of the explicit 24-variable H as combinations of cubes of linear forms (Waring: a monomial x^3 needs 1 cube, x^2 y needs 3, xyz needs 4), q <= 4 * 54 = 216, so a Druzkowski form of the counterexample lives in dimension N <= 240 (our estimate from the primary dimension formula; the minimal q is certainly smaller). The Druzkowski form is NOT needed for the symmetric extraction; the dBvdE construction consumes the cubic homogeneous form directly.

Note (known no-go direction): symmetry and the Druzkowski form do not combine for free; do not plan a "symmetric cubic-linear" target (no primary source establishes such a combined reduction; UNVERIFIED that one exists).

## 4. Task 4: post-2005 refinements relevant to cheaper extraction

- G. Meng, "Legendre transform, Hessian conjecture and tree formula", arXiv:math-ph/0308035; Appl. Math. Lett. 19 (2006) 503-510. Independent, near-simultaneous gradient reduction (acknowledged in dBvdE Section 3). Meng's version reduces JC to all gradient maps grad f with det h(f) in C^*; dBvdE's version is sharper (preserves nilpotency: x + grad f with h(f) nilpotent), which is what we need. No dimension advantage.
- de Bondt-van den Essen II (JPAA 196 (2005) 135-148) and van den Essen-Washburn (JPAA 189 (2004) 123-133): positive results in low dimension (symmetric JC true for n <= 4 nonhomogeneous, n = 5 homogeneous), giving lower bounds for any witness; no help constructing one.
- M. de Bondt, "Symmetric Jacobians", arXiv:1206.2865, Cent. Eur. J. Math. (2014): it suffices to prove JC for maps x + H over C such that JH satisfies ALL symmetries of the square (dihedral D4: symmetric about both diagonals), H homogeneous of arbitrary degree d >= 3. A strictly stronger structural target; the underlying constructions are of the same doubling type. Could be applied later to impose extra structure on the witness; not needed now.
- Zhao's later program (Generalized Vanishing Conjecture, Image Conjecture, arXiv:0704.1691 etc.) generalizes the target statements but does not shrink the constructive dimension.
- No published refinement was found that beats the n -> 2n doubling of the symmetric reduction, nor one that accepts a non-nilpotent Keller input directly. UNVERIFIED that none exists beyond the searches performed (arXiv + web, 2026-07-22).

## 5. Task 5: what has already been published from the July 2026 counterexample (as of 2026-07-22)

Verified landscape sweep:

- Announcement: Levent Alpoge, 2026-07-19, social media; credited to joint work with Fable (AI). No arXiv preprint by Alpoge found yet (UNVERIFIED whether one is in preparation).
- Secret Blogging Seminar, "The new counterexample to the Jacobian conjecture", 2026-07-20 (sbseminar.wordpress.com). Explicit map, weighted-homogeneity discussion, generically 3-to-1.
- jacobianfun.org / A. Gallagher (with GPT-5.6-sol), "The Jacobian counterexample, explained": independent exact verification (rational arithmetic), a weighted-lift construction producing a FAMILY of counterexamples with generic fiber degree >= 3, including an explicit G with det JG = -6, degrees (12, 11, 4), fiber degree 4, collision G(1,0,0) = G(-1,0,2) = (0,0,1). Source: github.com/algal/jacobianfun (RESEARCH.md). No symmetric/gradient/HN/Druzkowski content.
- Zihan Zhang, "Direct Consequences of the Three-Dimensional Counterexample to the Jacobian Conjecture", 2026-07-20 (zzhang-iu.github.io; no arXiv ID found). Derives: Mathieu conjecture false for SU(3); Gaussian Moments Conjecture false for some finite N; Zhao's Vanishing Conjecture false in some dimension; Image Conjecture false in some finite dimension. Explicitly does NOT construct symmetric Keller maps, gradient maps, or Druzkowski forms. All its consequences are non-constructive in dimension.
- W. Thompson (comment on sbseminar, 2026-07-21; github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample; Zenodo record 21466221): explicit BASS-CONNELL-WRIGHT cubic-homogeneous normal form of the counterexample. G(U) = U + H(U) : Q^24 -> Q^24, every nonzero component of H homogeneous cubic, 54 cubic monomials, 23 active nonlinear coordinates, det DG = 1 exactly, explicit rational collision points (collision_points.txt), nilpotency (JN)^17 = 0 (index 17). Verified two independent ways (sympy exact + Node.js BigInt sparse polynomial arithmetic), matching SHA-256 digest 10f416c2bf813771cddc392469d937fa06a5a9f4aeff1ed2a99af4214b64b632. Files: cubic_map.txt, derivation.md, verify_sympy.py, independent_verify.js.
- wmayner (github.com/wmayner/dixmier-counterexample): Dixmier conjecture false for A_n, n >= 3, with verification scripts.

CONCLUSION FOR TASK 5: nobody has published an explicit symmetric / gradient / Hessian-nilpotent witness as of 2026-07-22. Zhang's note proves existence non-constructively; Thompson's repo supplies exactly the missing input (an explicit cubic homogeneous nilpotent form). The extraction task remains OPEN and is now cheap (see Section 6). This is a construction task, not a verification task, but Step 0 below is a verification of Thompson's artifact.

## 6. Construction recipe: explicit symmetric witness from the degrees-(7,6,4) map

Target: an explicit non-invertible symmetric Keller map Ftil = id + grad f on C^48, f a homogeneous quartic with nilpotent Hessian, plus the failing HN quartic P_star = -f, plus a 2-point collision certificate. All arithmetic in Q(i).

Step 0 (input verification). Download Thompson's cubic_map.txt (dim 24, 54 cubic monomials) and collision_points.txt. Re-verify in sympy with exact rationals: (a) det DG = 1 (or equivalently verify JH nilpotent, Step 2, plus homogeneity); (b) G(u) = G(v) for the published collision pair u != v. If verification fails, fall back to redoing the BCW ladder by hand from the 16-monomial Alpoge map (Section 3.1 steps 1-3; a day of careful sympy work; naive dimension a few hundred, prunable).

Step 1 (potential). With H = (H_1, ..., H_24) from cubic_map.txt, x = (x_1..x_24), y = (y_1..y_24):

    f := f_H = -i * sum_{j=1}^{24} H_j(x + iy) y_j    in Q(i)[x, y], homogeneous of degree 4 in 48 variables.

Size: each cubic monomial c x_a x_b x_c expands into 8 Gaussian-rational monomials under x -> x + iy, times y_j: at most 54 * 8 = 432 quartic monomials before collection. Trivial for sympy (< 1 s).

Step 2 (Hessian nilpotency = HN certificate). By dBvdE Lemma 1.2 and its char-poly identity, char(Hes f) = z^48 iff char(JH) = z^24. Certify JH nilpotent by ANY of: (a) re-verify Thompson's (JN)^17 = 0 by repeated sparse multiplication (heaviest step; sparse 24 x 24 with quadratic entries; feasible, minutes to low hours in sympy, much faster with the Node BigInt approach Thompson ships); (b) Faddeev-LeVerrier / trace test: Tr(JH^k) = 0 for k = 1..24; (c) accept homogeneity + det DG = 1 (a cubic homogeneous H with det(I + JH) = 1 identically has JH nilpotent; standard grading argument = BCW Lemma (4.1)). Recommended: (c) for the proof plus a spot-check of (a) at random rational points.

Step 3 (the symmetric map). Ftil = id_48 + grad f, explicitly:

    Ftil_xk = x_k - i * sum_j (dH_j/du_k)(x + iy) y_j
    Ftil_yk = y_k + sum_j (dH_j/du_k)(x + iy) y_j - i H_k(x + iy)

J(Ftil) - I = Hes f is symmetric by construction and nilpotent by Step 2, so det J(Ftil) = 1: Ftil is a symmetric Keller map, of the exact Corollary 1.3 form.

Step 4 (collision certificate). Take Thompson's rational collision u != v of G (so H(u) - H(v) = v - u). Compute

    w = i * [ sum_{k=0}^{16} (-(JH(v))^t)^k ] (u - v)    in (Q(i))^24  (numeric matrix powers, trivial),
    p_1 = (u, 0),    p_2 = (v - i w, w)    in (Q(i))^48.

Verify p_1 != p_2 (true since u != v) and Ftil(p_1) = Ftil(p_2) by exact substitution (432-term quartics evaluated at Gaussian rationals; < 1 s). This certifies Ftil is a non-invertible symmetric Keller map: HC(48) is FALSE, and with it the symmetric/gradient JC.

Step 5 (the failing HN quartic). P_star := -f. Then Ftil(z) = z - grad P_star matches Zhao's convention; P_star is a homogeneous HN quartic in 48 variables whose deformed inversion pair Q_t is NOT polynomial in t; Delta^m P_star^{m+1} != 0 for infinitely many m: Zhao's Vanishing Conjecture (7.1) and Homogeneous Vanishing Conjecture (7.3, d = 4) fail EXPLICITLY at P_star. Optional sanity computation: Delta P_star^2 != 0 (P_star^2 has order 10^4-10^5 terms; sympy seconds-to-minutes); by Zhao's Corollary 3.9 remark this non-vanishing is forced.

Feasibility verdict: EASY. Dimensions: 24 (input) -> 48 (witness). Term counts: 54 cubic monomials in, <= 432 quartic monomials for f, collision arithmetic over Q(i) trivial. The only nontrivial compute is the independent nilpotency re-verification of JH (Step 2a), already done twice upstream with a published SHA-256 digest. Everything fits comfortably in sympy on the workstation; total wall time dominated by Step 2 at minutes-to-hours, all other steps seconds.

## 7. Sources

Primary (full text read):
- M. de Bondt, A. van den Essen, "A reduction of the Jacobian conjecture to the symmetric case", Proc. Amer. Math. Soc. 133 (2005) 2201-2205, DOI 10.1090/S0002-9939-05-07570-2 (AMS PDF; local copy E:\_Temp\jc-dossier\debondt-pams.pdf).
- W. Zhao, "Hessian nilpotent polynomials and the Jacobian conjecture", arXiv:math/0409534v2; Trans. Amer. Math. Soc. 359 (2007) 249-274 (local copy E:\_Temp\jc-dossier\zhao-0409534.pdf).
- H. Bass, E. H. Connell, D. Wright, "The Jacobian conjecture: reduction of degree and formal expansion of the inverse", Bull. Amer. Math. Soc. 7 (1982) 287-330 (AMS PDF; local copy E:\_Temp\jc-dossier\bcw1982-bullams.pdf).

Primary (abstract / repository level):
- M. de Bondt, "Symmetric Jacobians", arXiv:1206.2865.
- W. Thompson, explicit cubic-homogeneous reduction: github.com/wtho704/explicit-cubic-homogeneous-jacobian-counterexample; Zenodo 21466221.
- github.com/algal/jacobianfun (RESEARCH.md); jacobianfun.org/jacobian-explained.
- Z. Zhang, "Direct Consequences of the Three-Dimensional Counterexample to the Jacobian Conjecture" (zzhang-iu.github.io, 2026-07-20).
- Secret Blogging Seminar post, 2026-07-20: sbseminar.wordpress.com/2026/07/20/the-new-counterexample-to-the-jacobian-conjecture/.

Secondary (citations verified through the above):
- L. M. Druzkowski, "An effective approach to Keller's Jacobian conjecture", Math. Ann. 264 (1983) 303-313. (Full text not fetched.)
- G. Gorni, G. Zampieri, "On cubic-linear polynomial mappings", Indag. Math. (N.S.) 8 (1997) 471-492.
- G. Meng, "Legendre transform, Hessian conjecture and tree formula", arXiv:math-ph/0308035.
- de Bondt-van den Essen JPAA 193 (2004) 61-70 and JPAA 196 (2005) 135-148; van den Essen-Washburn JPAA 189 (2004) 123-133. (Statements as quoted in the two primary papers above; full texts not fetched.)

Local verification artifacts (this dossier): E:\_Temp\jc-dossier\verify_alpoge.py (det JF = -2, degrees (7,6,4), 3-point collision: PASSED), E:\_Temp\jc-dossier\verify_dbvde_identity.py (Hessian nilpotency of f_H and the triangular conjugation identity on a sample: PASSED).
