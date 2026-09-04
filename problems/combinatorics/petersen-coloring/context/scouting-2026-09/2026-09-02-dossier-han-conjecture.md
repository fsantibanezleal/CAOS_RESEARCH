# Dossier: Han's conjecture after the July 2026 disproof. Can an explicit small counterexample be found and certified by computer?

Date: 2026-09-03 (scouting cycle 2026-09). Author: research scout (Lucy) for Felipe Santibanez-Leal.
Scope: primary-source review of Kong-Liu-Shen (arXiv:2608.00177), Liu-Shen (arXiv:2512.12460), the 2023 survey (arXiv:2301.07511), Cibils-Lanzilotta-Marcos-Solotar (arXiv:2509.05135), Wang-Arunachalam-Keller (CRM 2022), Buchweitz-Green-Madsen-Solberg (MRL 2005), Han (JLMS 2006; arXiv:1004.0748), plus the computational-tool landscape.

Marks. [V] = verified against the primary source (full text read, or abstract/metadata page read). [V-abs] = verified from the abstract or metadata only. [V-sum] = read through a machine summary of the source page; wording may be paraphrased. [U] = unverified or not found in any source. [D] = my own derivation from [V] facts; check before citing.

Full texts read line by line for this dossier: arXiv:2608.00177v1 (23 pages, all sections and Appendix A), arXiv:2512.12460v1 (introduction and Section 4), arXiv:2301.07511v2 (Sections 3, 4.1, 4.2), arXiv:2509.05135v2 (Sections 5, 6.5, 7.1), Wang-Arunachalam-Keller CRM 360 (2022) (complete), Han arXiv:1004.0748 (definitions and Theorem 1).

---

## 0. Executive answer

1. Han's conjecture is false over C. Kong, Liu and Shen (arXiv:2608.00177, posted 2026-07-31) construct a finite-dimensional C-algebra A with gldim A = infinity and HH_n(A) = 0 for every n >= 1 [V].
2. The construction is existential in size: the paper gives no presentation, no dimension, no number of simple modules, and no Cartan matrix of A [V: absence checked against the whole text]. From the construction one can derive that A has exactly 26 isomorphism classes of simple modules [D, Section 2.4], and its dimension is realistically in the thousands or more [U estimate].
3. The counterexample lives in a very specific structural pocket: its dg singularity category is the one-periodization of Krah's universal phantom on Bl_10(P^2). Via Wang-Arunachalam-Keller, an algebra is a Han counterexample if and only if its singularity category is nonzero and its canonical dg enhancement has Hochschild homology concentrated in degrees 0 and 1 [D from V facts, Section 3.2]. Every known nonzero Hochschild-acyclic dg category is geometric (phantoms on rational surfaces with 10 or 11 blown-up points, or F_2 blown up at 9 points) [V-abs].
4. A brute-force search over quiver algebras of dimension 10 to 20 is computationally cheap for the finite part (HH_n = 0 for n <= N via minimal bimodule resolutions, with QPA or the brand-new QuiverLab) but structurally unlikely to hit, because the known positive classes exclude almost every small non-monomial shape in characteristic 0. The one real gap where a small example is not excluded by any theorem is: ungraded local (or few-vertex) algebras with non-homogeneous relations in any characteristic, and graded or Koszul algebras in positive characteristic (where the Igusa-formula proofs of Bergh-Madsen do not apply) [V for the theorems, D for the gap].
5. A complete computer certificate of HH_n(A) = 0 for ALL n >= 1 exists only when the minimal bimodule resolution is eventually periodic (an explicit A^e-isomorphism Omega^{q+p}(A) = Omega^q(A)) or admits a closed form; otherwise a human argument on the structure of the resolution or of the singularity category is unavoidable. Details in Section 3.

---

## 1. Exact statement and the positive classes (the exclusion list for any small counterexample)

### 1.1 Statements

Happel's question (1989) [V, survey Section 1 and KLS Introduction]: for a finite-dimensional algebra A over a field, does HH^n(A) = 0 for n >> 0 imply gldim A < infinity? Answered negatively by Buchweitz-Green-Madsen-Solberg (MRL 12 (2005) 805-816) with the quantum exterior algebra A_q = k<x,y>/(x^2, y^2, xy + q yx), q not a root of unity: gldim A_q = infinity while HH^n(A_q) = 0 for n >= 3 (hch.dim = 2) [V-abs, and survey Section 4.1]. Han proved that hh.dim A_q = infinity = gldim A_q for every q, so the homology of A_q is not pathological [V-sum from Han 2006, Proposition 5, and survey Section 4.1]. Bergh-Erdmann (Algebra Number Theory 2 (2008)) built the minimal bimodule resolution of every codimension-2 quantum complete intersection and showed the cohomology vanishes in high degree exactly when q is not a root of unity while the homology is always nonzero [V-abs].

Han's conjecture (Han, "Hochschild (co)homology dimension", J. London Math. Soc. 73 (2006) 657-668, Conjecture 3.4) [V-sum of arXiv math/0408402]: for a finite-dimensional algebra A over an algebraically closed field k, the following are equivalent: (1) hh.dim A < infinity; (2) hh.dim A = 0; (3) gldim A < infinity. Here hh.dim A = sup{n : HH_n(A) != 0} with the convention hh.dim = 0 when HH_n = 0 for all n >= 1 [V, survey Definition 3.1].

Perfect-field form (survey Conjecture 3.8) [V]: if A/J(A) is separable (e.g. k perfect) then (1), (2), (3) are equivalent. The implications (3) => (2) => (1) are theorems (Keller, via cyclic homology of A versus A/J(A); survey Theorem 3.7) [V]. "Han's property" = the implication hh.dim A < infinity => gldim A < infinity [V, survey Definition 3.9]. Liu-Shen restate the conclusion as homological smoothness, which is equivalent to finite global dimension over a perfect field [V, arXiv:2512.12460 Introduction, citing RR22 Cor. 3.19].

Remark on the field: over a non-perfect field the conjecture fails trivially (k(alpha) inseparable has HH_n = k(alpha) for all n and gldim 0; survey Remark 3.4) [V]. So any "small counterexample" search must be run over a perfect field, and the interesting cases are algebraically closed k, or k = Q, or k = F_p with a split basic algebra.

Invariance [V, survey Section 2]: HH_* is Morita and derived invariant (Rickard, Keller); gldim finiteness is derived invariant. So the class of counterexamples is closed under derived equivalence, and a search may be run up to derived equivalence.

### 1.2 Positive classes (Han's property holds), with sources

Table 1 of the survey (arXiv:2301.07511v2, Section 4.1) [V], plus later results.

| Class | Field hypothesis | Source | Status |
|---|---|---|---|
| Finite gldim (hereditary, quotients of acyclic quiver algebras, directed) | any | Eilenberg-Nagao-Nakayama 1956; Cibils 1986; Keller (survey Thm 3.7) | [V] trivial direction |
| Group algebras kG (G finite) | any | Swan 1960; Burghelea 1985 (survey Section 4.1, proof communicated by E. N. Marcos) | [V] |
| Commutative finite-dimensional (indeed finitely generated commutative) | any | Avramov-Vigue-Poirrier 1992; BACH 1994; survey Theorem 4.2 | [V] |
| Monomial algebras kQ/I, I generated by paths | any | Han 2006, Theorem 2 (with an algorithm for HH of monomial algebras via Bardzell's resolution and "minimal cycle algebras") | [V-sum] |
| Exterior algebras | any | Han-Xu 2006 | [V] |
| Quantum complete intersections k<x,y>/(x^a, xy - q yx, y^b) | any | Bergh-Erdmann 2008, Theorem 3.1 | [V] |
| N-Koszul algebras | char 0 | Bergh-Madsen 2009, Theorem 4.5 | [V] |
| Homogeneous (graded) quotients kQ/I with Q containing a loop | char 0 | Bergh-Madsen 2009, Theorem 4.7 (uses Igusa's formula; Igusa's no-loop theorem gives gldim = infinity) | [V] |
| Graded cellular algebras | char 0 | Bergh-Madsen 2009, Theorem 4.9 | [V] |
| Local graded algebras with a certain relation; generalization of QCIs k<x_1..x_n>/(f_1..f_p), f_1 in k[x_1], k[x_1]/(f_1) not smooth | (see paper) | Solotar-Vigue-Poirrier 2010, Theorems I and II | [V] |
| Quantum generalized Weyl algebras | alg. closed, char 0 (infinite-dimensional class) | Solotar-Suarez-Alvarez-Vivas 2013 | [V] |
| Trivial extensions T(A) = A + DA of A local, or self-injective, or graded | alg. closed (char 0 for graded) | Bergh-Madsen 2017, Theorems 3.2, 3.5, 3.9 | [V] |
| Bounded quiver algebras with a 2-truncated oriented cycle (a cycle a_1...a_l with a_i a_{i+1} = 0 in A for all i, indices mod l; in particular a loop x with x^2 = 0) | any | Han, arXiv:1004.0748, Theorem 1: hh.dim = infinity = gldim | [V, full text] |
| Corner algebras, E-triangular algebras, null-square projective algebras built from Han algebras | perfect | Cibils-Redondo-Solotar 2021, Thm 2.21, Cor 2.22, Thm 4.8 | [V] |
| Bounded extensions B subset A (A/B of finite pd as B-bimodule, projective on one side, tensor-nilpotent): B Han iff A Han | any | Cibils-Lanzilotta-Marcos-Solotar 2022, Theorem 4.6 (J. Algebra 598) | [V] |
| Strongly proj-bounded extensions | any | Iusenko-MacQuarrie 2021, Cor 6.17 | [V] |
| Strongly stratifying Morita contexts: Han for the whole iff Han for the diagonal | (see paper) | Cibils-Lanzilotta-Marcos-Solotar arXiv:2303.17369 | [V-abs] |
| Rings admitting a height-2 ladder of derived categories: Han for R iff Han for S x T; hence reduction to "derived 2-simple" rings; skew-gentle algebras; category algebras of finite EI categories; GLS algebras of Cartan triples | (see paper) | Wang-Xu-Zhang-Zhou, arXiv:2409.00945, Theorem 1.2 and Sections 4-5 | [V-sum] |

Derived consequences for a search [D]:
- Radical-square-zero algebras are monomial, hence covered by Han 2006. Gentle algebras and Nakayama algebras are monomial, hence covered. Special biserial algebras with genuine commutativity relations are NOT covered (only skew-gentle via WXZZ).
- Any local algebra kQ/I with a loop x such that x^2 = 0 in A is covered (2-truncated cycle of length 1). Since the theorem applies to any presentation, a local algebra is excluded as soon as SOME element x in J minus J^2 satisfies x^2 = 0, e.g. all quantum exterior algebras.
- Homogeneous local algebras (all relations homogeneous, quiver has loops) are covered in char 0 (BM09). Ungraded local algebras are NOT covered by any theorem in the list except the specific relation shapes of SVP10 and the 2-truncated criterion. The survey (Section 5, "frontiers") names self-injective and Frobenius algebras, and Hopf algebras, as the next open classes [V].
- Positive characteristic: the Bergh-Madsen results (N-Koszul, graded with loops, graded cellular, trivial extensions of graded) all need char 0 because they rest on Igusa's formula relating the Euler characteristic of relative cyclic homology to the graded Cartan determinant [V, survey Section 4.1]. So in char p, graded and Koszul local algebras with loops are open, subject only to Han 2010 (2-truncated cycles) and BE08 (QCIs).
- Symmetric algebras: A = DA as bimodules gives HH_n(A) = D HH^n(A), so Han's property for a symmetric algebra is equivalent to Happel's property for it. The known Happel counterexamples (BGMS quantum exterior algebras, Parker-Snashall Koszul self-injective families, Xu-Zhang) all have infinite hh.dim, so none is symmetric with finite hch.dim [D from V facts; the symmetric case is open per survey Section 5].

The tau-Hochschild paper (Cibils-Lanzilotta-Marcos-Solotar, arXiv:2509.05135v2, to appear in Annals of K-Theory) does NOT add positive classes for Han's conjecture. It proves (Theorem 5.5) that the tau-Hochschild homology of a bound quiver algebra is infinite iff the algebra has "infinite + global dimension" (a pair of vertices y, x with y Lambda x != 0 and Tor_*(k_x, y k) infinite), and (Theorem 5.6) that any positive answer to Han's conjecture is of infinite + global dimension. Its Remark 5.7 and Section 6.5 state that an algebra of infinite global dimension that is not of infinite + global dimension "would be a refutation of Han's conjecture" and that "up to date, there are no known counterexamples to Han's conjecture" (v2 dated 2026-06-17, six weeks before KLS) [V]. Consequence [D]: the KLS algebra A must NOT be of infinite + global dimension, i.e. for every pair of vertices (y, x) of its quiver with y A x != 0, Tor_*^A(k_x, y k) is finite; equivalently every nonzero Peirce component of A sits over a pair of simples with finite total Tor. This is a strong, checkable necessary condition for candidates: a candidate with a loop must violate the "extension conjecture" at that vertex (Proposition 6.11), and CLMS note the extension conjecture is proved for monomial and special biserial algebras (Liu-Morin; Green-Zacharia) [V].

---

## 2. The Kong-Liu-Shen counterexample

Bibliographic: Bochao Kong (MSU), Yeqin Liu (U. Michigan), Yu Shen (MSU), "A counterexample to Han's conjecture", arXiv:2608.00177v1, 31 Jul 2026, 23 pages, MSC 16E40, 16E10, 16E45, 14F08 [V]. Acknowledgment (Section 1.3): "The counterexample presented in this paper was discovered with the assistance of OpenAI's GPT-5.6 Sol Ultra model. All mathematical arguments and references were independently verified by the authors." [V, verbatim].

Main theorem (Theorem 1.1 = Theorem 4.4) [V]: there is a finite-dimensional C-algebra A with HH_n(A) = 0 for every n >= 1 and gldim A = infinity. The authors stress that this is "the strongest possible vanishing in positive degrees" and that A "is an ordinary algebra, viewed as a dg algebra concentrated in degree zero" [V].

### 2.1 Construction chain (Sections 2.4, 3, 4) [V]

Step 0 (geometric phantom). X = Bl_{p_1..p_10} P^2, ten general points over C. Krah (Invent. Math. 235 (2024) 1009-1018; arXiv:2304.01269) constructs a non-full exceptional collection E = (L_1, ..., L_13) of line bundles of maximal length whose right orthogonal P = E^perp is a universal phantom (nonzero admissible subcategory with vanishing Grothendieck group and vanishing additive invariants) [V, KLS Prop. 2.1 and Krah's abstract]. The 13 line bundles are O_X, O_X(D_1), ..., O_X(D_10), O_X(F), O_X(2F) with D_i and F explicit combinations of the hyperplane class H and the exceptional classes E_j; Krah verifies Hom and Ext^2 vanishings by h^0 computations that rely on cases of the SHGH conjecture proved by Dumnicki-Jarnicki and Ciliberto-Miranda [V-sum of the html version; exact signs of D_i, F not re-checked, U]. HH_*(X) is concentrated in degree 0 with dim HH_0(X) = 1 + 11 + 1 = 13 (Hodge numbers + HKR), the 13 exceptional objects account for all of it, and additivity of HH under semiorthogonal decompositions (Kuznetsov 2009) gives HH_*(P) = 0 while H^0(P) != 0 [V, proof of Prop. 2.1].

Step 1 (algebraization). Hille-Perling (Ann. Inst. Fourier 64 (2014) 625-644, Theorems 1.1-1.2): every rational surface has a tilting bundle T with Gamma = End_X(T) a finite-dimensional quasi-hereditary algebra, built by universal extensions from a full exceptional sequence of line bundles [V-abs and KLS Section 2.4]. Hence gldim Gamma < infinity and RHom(T, -): Perf(X) -> Perf(Gamma) is an equivalence, lifted to a dg Morita equivalence by Keller's theorem [V]. Because rank K_0(X) = 13, Gamma has 13 simple modules [D].

Step 2 (dual numbers and one-periodic folding). Lambda = Gamma tensor_C C[eps]/(eps^2). Right Lambda-modules = differential right Gamma-modules (M, d) with d^2 = 0. For a bounded complex P^* of f.g. projective Gamma-modules, Fold(P^*) = (direct sum of all P^r, d) with eps acting as the folded differential. Results of Stai (MRL 2018) and Liu (Czech. Math. J. 2023) identify the triangulated hull of the orbit category Perf(Gamma)/[1] with the one-periodic homotopy category K_1(proj Gamma); Wei (Proc. Roy. Soc. Edinburgh 2015, Thms 3.6-3.7) identifies Gorenstein-projective Lambda-modules with differential modules whose underlying Gamma-module is projective; Lambda is Iwanaga-Gorenstein; Buchweitz's equivalence then gives Dsg(Lambda) = stable Gproj(Lambda) = K_1(proj Gamma) = triangulated hull of Perf(Gamma)/[1] (KLS equation (2.2)) [V]. Dimension bookkeeping [D]: dim Lambda = 2 dim Gamma; Lambda has 13 simples.

Step 3 (folding the exceptional objects). For each i, choose a bounded complex P_i^* of f.g. projective Gamma-modules representing RHom(T, L_i), and put N_i = Fold(P_i^*), a finite-dimensional right Lambda-module [V, Section 3]. Under (2.2) the object L_i goes to N_i.

Step 4 (partial resolution). M = Lambda + N_1 + ... + N_13 (direct sum), A = End_Lambda(M) (Construction 3.1) [V]. A is finite-dimensional because the P_i^* are bounded with f.g. projective terms [V]. Proposition 3.2: Dsg(A) = Dsg(Lambda) / <q(N_1), ..., q(N_13)> (Verdier quotient by the thick subcategory generated by the images of the N_i), by Chen's partial-resolution theorem (Arkiv for Matematik 53 (2015)): for a generator M of mod Lambda with A = End(M), the singularity category of A is the quotient of Dsg(Lambda) by the modules killed by - tensor_A M, provided those modules have finite projective dimension over A [V]. The verification in KLS: with e the idempotent of the summand Lambda, Xi = A/AeA = stable End(N) is a finite-dimensional directed algebra (because Hom_stable(N_i, N_j) = direct sum over n of Hom_D(L_i, L_j[n]) and E is exceptional), hence gldim Xi < infinity; and every projective Xi-module has projective dimension at most 2 over A via the fold exact sequence (2.3)/(3.2) [V].

Step 5 (periodization and the dg quotient square). U = C[t, t^{-1}] with |t| = 1, d = 0 (an associative, not graded-commutative, graded Laurent algebra). Tensoring a dg category with U is the Laurent model of the dg orbit category by the shift (Lemma A.4). Theorem 4.1 (proved in Appendix A with explicit sign conventions) gives a commutative square of dg quotients, and Corollary 4.2: Dsg(A) is dg Morita equivalent to Perf(P tensor_C U) [V]. Corollary 4.3: HH_*(Dsg(A)) = 0, by Shklyarov's Kunneth theorem (Proc. LMS 2013, Thm 2.8) applied to the dg endomorphism algebra of a classical generator of P, whose Hochschild complex is acyclic [V].

Step 6 (conclusion, Theorem 4.4). Wang-Arunachalam-Keller (CRM 360 (2022) 491-496, Corollary 5): for a finite-dimensional algebra over an algebraically closed field, HH_n(Dsg^dg(A)) = HH_{n-1}(A) for n >= 2, so HH_m(A) = 0 for m >= 1. Nonvanishing: for an object Q of P with nonzero class in H^0(P), the identity of Q survives in H^0 End_{P tensor U}(Q) because the degree-0 component is a direct summand; so Dsg(A) != 0 and gldim A = infinity [V].

### 2.2 Why each ingredient is needed [V for the facts, D for the "why"]

- Phantom: the target is a nonzero dg category with zero Hochschild homology. Ordinary finite-dimensional algebras cannot do this (HH_0(A) = A/[A,A] surjects onto HH_0(A/J) = k^{#simples} != 0), so one needs a genuinely triangulated object. All known such objects are geometric phantoms or quasi-phantoms.
- Tilting bundle: converts Perf(X) into Perf(Gamma) for a finite-dimensional algebra Gamma of finite global dimension; without finite gldim the Wei/Buchweitz identification of Dsg(Gamma tensor dual numbers) with the periodized Perf(Gamma) fails (KLS use gldim Gamma < infinity in (2.1), in Lemma A.2, and in Prop. A.3).
- Dual numbers: the cheapest way to make a singularity category out of a smooth algebra. Dsg(Gamma tensor C[eps]) is the one-periodization of Perf(Gamma). Its Hochschild homology is NOT zero: by Kunneth, HH_*(Perf(Gamma) tensor U) = HH_*(Gamma) tensor HH_*(U), and HH_0(Gamma) = C^13, so Lambda alone is consistent with Han (HH_n(Lambda) != 0 for all n, matching BM17-type results) [D].
- The 13 folded exceptional objects: quotienting the periodized Perf(Gamma) by the periodized <E> removes exactly the C^13 in every degree and leaves the periodized phantom. Chen's partial resolution realizes this Verdier quotient as the singularity category of an honest finite-dimensional algebra A = End_Lambda(Lambda + N). This is where the "ordinary algebra" is manufactured.
- Appendix A (dg enhancements): the WAK isomorphism is stated for the canonical dg singularity category while the Kunneth argument is applied to P tensor U; the paper therefore needs the equivalences at the dg level and compatible with quotients, without invoking uniqueness of enhancements (Lunts-Orlov is cited only for pretriangulatedness of Drinfeld quotients) [V, Section 4 opening paragraph].

### 2.3 What the paper says about explicitness, size and fields

- Explicitness: KLS write "Fix a dg enhancement", "choose a bounded complex P_i^*", and never present Gamma, Lambda, N_i, or A by quiver and relations. No dimension, number of simples, Cartan matrix, or Loewy length is stated anywhere [V: absence checked in the full text]. The only finiteness statement is Construction 3.1: A is finite-dimensional over C.
- Field: everything is over C (Krah's surface is over C; Hodge numbers and HKR are used for HH_*(X); "ten general points") [V]. The paper contains no remark on other fields [V]. Liu-Shen's dg counterexample works over any field of characteristic 0 [V].
- Uniqueness or minimality: not discussed [V]. Question 1.0.4 of Liu-Shen (a proper singular variety with finitely many nonzero HH_n) is stated as open [V].

### 2.4 What bound on dim A can be derived [D unless marked]

- Number of simples of A. Gamma has 13 simples (rank K_0(X) = 13 [V]; the tilting bundle of Hille-Perling has one indecomposable summand per member of a full exceptional sequence [V-abs, plausible, U for the exact count of summands]). Lambda = Gamma tensor C[eps] has the same 13 simples. The stable endomorphism ring of N_i is direct sum over n of Hom_D(L_i, L_i[n]) = C, so each N_i has exactly one non-projective indecomposable summand, and for i != j these summands are non-isomorphic (Hom_stable(N_i, N_j) = 0 for i > j by exceptionality) [V for the Hom computation, KLS proof of Prop. 3.2]. Hence add(Lambda + N) has 13 + 13 = 26 indecomposable objects and A is Morita equivalent to a basic algebra with 26 simple modules. Any Han counterexample built by this route on Bl_10(P^2) therefore has at least 26 simples; replacing the surface by Bl_9(F_2) (rank K_0 = 11, a phantom exists there by "A looming of phantoms", arXiv:2511.05381 [V-abs]) would give 22 simples.
- Dimension. dim A = sum over the 26 x 26 Hom spaces. Even dim Gamma is not small: the Hille-Perling tilting bundle is a universal extension of 13 line bundles and its endomorphism algebra is a quasi-hereditary algebra whose Hom spaces are governed by h^0 of many divisor classes on a 10-point blowup [V-abs for the construction, U for numbers]. Then dim N_i = sum_r dim P_i^r, where the P_i^* are projective resolutions of the 13 objects RHom(T, L_i), each term a sum of projective Gamma-modules of dimension dim Hom(T_j, T). A realistic expectation is dim A in the 10^3 to 10^5 range [U, my estimate]. No source gives a number.
- Cartan matrix. Since HH_*(Dsg^dg(A)) vanishes in ALL degrees (Cor. 4.3) and WAK Theorem 4 identifies HH(Dsg^dg(A)) with the cone of the map HH(A) -> D HH(A) whose degree-0 part is the Cartan pairing on HH_0(A) = C^26, the Cartan matrix of (basic) A is invertible over C [D from V facts]. This is compatible with, but not implied by, the Cartan-determinant conjecture (which concerns finite gldim).
- Gorenstein-ness of A: not stated in the paper [V absence]; Lambda is Iwanaga-Gorenstein [V]. Whether A is Gorenstein is [U].

Consequence for the search question: the only known counterexample is far above dimension 20 and has 26 simples. A small example, if it exists, must arise from a different mechanism, or from a currently unknown small "algebraic phantom".

---

## 3. Can HH_n(A) = 0 for ALL n >= 1 be certified by finite computation?

### 3.1 What is being certified

Let A = kQ/I be basic, finite-dimensional, split over a perfect field k. HH_n(A) = Tor_n^{A^e}(A, A) = H_n(A tensor_{A^e} P_*) for any projective A^e-resolution P_* of A [V, survey Definition 2.4]. Each HH_n is computable by linear algebra once P_* is known up to degree n + 1. Two separate assertions must be certified:

(C1) gldim A = infinity. Finite certificates: (a) a loop in Q (Igusa's no-loop theorem for admissible quotients over algebraically closed fields; survey Section 4.1 and Han 2010 Remark 2) [V]; (b) a 2-truncated oriented cycle (Han 2010, Corollary 1) [V], but this also forces hh.dim = infinity so it is useless for a counterexample; (c) a simple S and integers m < m' with an explicit isomorphism Omega^{m'} S = Omega^m S (periodic syzygy; QPA: NthSyzygy, IsOmegaPeriodic [V-sum of QPA Chapter 8]); (d) any nonzero object of Dsg(A) exhibited as a Gorenstein-projective non-projective module with an explicit complete resolution. All are finite.

(C2) HH_n(A) = 0 for all n >= 1. This is an infinite family of statements. Finite certificates known to me:

(C2-a) Eventual periodicity of the diagonal bimodule. If Omega^{q+p}_{A^e}(A) = Omega^q_{A^e}(A) as A-bimodules for some q >= 0, p >= 1 (an explicit isomorphism produced and checked by the computer), then HH_{n+p}(A) = HH_n(A) for n > q, so it suffices to check HH_n(A) = 0 for 1 <= n <= q + p. Caveat: a twisted periodicity Omega^p(A) = A_sigma (twist by an automorphism sigma) does NOT give HH_{n+p}(A) = HH_n(A); it gives HH_{n+p}(A) = HH_n(A, A_sigma), which is a different group unless sigma has finite order (then use the p-multiple) [D, standard]. A periodic diagonal bimodule (q = 0) forces A self-injective [V-sum, Dugas / Erdmann-Skowronski surveys], so for non-self-injective candidates only q > 0 can occur.

(C2-b) Closed-form bimodule resolution. When the reduction system (Groebner basis) of I has finitely many ambiguity patterns that recur uniformly, the Chouhy-Solotar resolution (generalizing Bardzell's for monomial algebras) has a uniform description in all degrees, and the vanishing of A tensor_{A^e} P_* homology in all degrees can be proven by a uniform (human) argument on computer-generated pattern data. Bardzell's resolution is the clean case, and it is exactly the case where Han's conjecture is a theorem (Han 2006) [V]. So (C2-b) is a semi-automatic route, not a push-button certificate.

(C2-c) Reformulation through the singularity category (WAK). For A finite-dimensional over an algebraically closed field, with S = Dsg^dg(A) the canonical dg enhancement, WAK Theorem 4 says HH(S) is the "double Hochschild complex" ... -> A tensor A -> A -> DA -> D(A tensor A) -> ... with DA in degree 0, i.e. the cone of HH(A) -> D HH(A) where the middle map factors through the Cartan pairing on HH_0(A) [V, full text]. Corollary 5: HH_n(S) = HH_{n-1}(A) = D HH_{1-n}(S) for n >= 2, and HH_1(S) = ker(HH_0(A) -> D HH_0(A)), HH_0(S) = coker of the same map [V for Cor. 5 and the displayed HH_1 statement; D for HH_0]. Therefore [D]:

   A is a Han counterexample (HH_n(A) = 0 for all n >= 1, gldim A = infinity)
   if and only if Dsg(A) != 0 and HH_n(Dsg^dg(A)) = 0 for all n outside {0, 1}.

   In words: the dg singularity category must be a "Hochschild phantom in degrees other than 0 and 1", with its degree-0 and degree-1 Hochschild homology equal to the cokernel and kernel of the Cartan pairing. This is the precise structural target. It converts the certificate problem into: exhibit a dg model of Dsg(A) whose Hochschild homology is computable in closed form. Chen-Wang's dg Leavitt algebra L_A (per(L_A) = sg(A), WAK Theorem 8) is such a model in principle, but computing HH of L_A in all degrees is again an infinite problem unless L_A has extra structure (periodicity, Kunneth decomposition as in KLS).

(C2-d) Gorenstein CM-finite candidates. If A is Iwanaga-Gorenstein and Gproj(A) has finitely many indecomposables G_1..G_r, then Dsg(A) = stable Gproj(A) and its dg model is the dg endomorphism algebra of G = sum G_i, whose cohomology is the Tate cohomology Ext-hat^*(G, G) (periodic when the G_i are periodic). If moreover the stable category is 1-periodic (Omega G_i = G_i), the dg model is of the form B tensor U for a finite-dimensional graded algebra B, and HH(B tensor U) = HH(B) tensor HH(U) by Kunneth, so HH_*(S) = 0 iff HH_*(B) = 0, impossible for B an ordinary nonzero algebra. This suggests [D, heuristic]: 1-periodic CM-finite singularity categories cannot give Han counterexamples unless B is a genuinely dg (A-infinity) algebra with acyclic Hochschild complex, i.e. an algebraic phantom. Which brings the problem back to the existence of algebraic phantoms.

(C2-e) Formal verification: no Lean/Coq/Isabelle library for Hochschild homology of quiver algebras exists to my knowledge [U]. "Certified by computer" therefore means: computer-generated finite data (resolution, syzygy isomorphism, HH_n = 0 for n <= N) plus a short human proof that the finite data implies all degrees.

### 3.2 Summary of what a certificate looks like

A complete certificate for a candidate A over Q or F_p is the tuple:
1. A presentation kQ/I with a reduced Groebner basis (so that A and dim A are exact).
2. A witness for gldim A = infinity of type (C1a) or (C1c).
3. The minimal projective A^e-resolution P_* of A up to degree q + p + 1, with explicit differentials.
4. An explicit A^e-isomorphism Omega^{q+p}(A) = Omega^q(A) (type C2-a), or a proof-carrying closed form (C2-b).
5. Verified HH_n(A) = 0 for 1 <= n <= q + p (rank computations over the exact field).
6. A field-independence statement (the computation over F_p for several p, or symbolically over Q, since HH commutes with field extension for A/J separable; survey Prop. 2.6) [V].

Without item 4 (or a substitute), one has only "HH_n(A) = 0 for n <= N", which is evidence, not a counterexample.

---

## 4. Feasibility of a computer search over small quiver algebras (dim about 10 to 20)

### 4.1 Tools (state on 2026-09-03)

| Tool | What it offers | Verified? |
|---|---|---|
| QPA (GAP package, gap-packages/qpa) | Quivers, admissible ideals via Groebner bases, EnvelopingAlgebra(A), AlgebraAsModuleOverEnvelopingAlgebra(A), DualOfAlgebraAsModuleOverEnvelopingAlgebra(A) (Section 4.17), ProjectiveResolutionOfPathAlgebraModule, NthSyzygy, IsOmegaPeriodic, GlobalDimensionOfAlgebra, GorensteinDimensionOfAlgebra (Chapter 8). No built-in Hochschild homology function; HH_n = H_n(A tensor_{A^e} P_*) must be assembled by hand from the resolution of A over A^e [V-sum of the manual chapters 4 and 8]. | [V-sum] |
| QuiverLab (PyPI quiverlab 1.0.1, released 2026-09-03; GitHub MarcoArmenta/quiverlab; MIT) | Claims exact computation over C (no floats) and over finite fields of Hochschild homology and cohomology with cup/cap products and Gerstenhaber brackets, four bimodule-resolution engines (normalized bar, minimal corner-typed A^e, Bardzell, Chouhy-Solotar), global dimension, Koszulity verdicts, AR theory, tau-tilting; 5421 tests run twice (numba and pure Python) [V-sum of PyPI and GitHub pages]. Released today; correctness and performance NOT independently verified [U]. Author's name suggests a representation theorist; treat as a candidate engine to be validated on known cases (BGMS algebra, truncated cycles, monomial algebras with Han's formulas). |
| SageMath HochschildComplex | Bar complex C_n(A, M) = M tensor A^{tensor n} for algebras with a basis; dimension explodes as (dim A)^{n+1}; only for dim A <= 5 and n <= 4 or so [V-sum of Sage docs]. Not a search engine. |
| Macaulay2 | No dedicated package for Hochschild homology of finite-dimensional noncommutative algebras found [U]. Relevant only for the geometric side (h^0 computations on blowups, Hom/Ext of line bundles). |
| Theoretical shortcuts | Han's algorithm for monomial algebras (Han 2006) [V-sum]; Igusa's Euler-characteristic formula in char 0 for graded algebras (BM09) [V]; Anundsen-Sandoy's graded Euler-characteristic method for higher preprojective algebras (arXiv:2606.26255) [V-abs]. None applies to the ungraded non-monomial candidates that matter. |

Practical cost: for dim A <= 20, dim A^e <= 400; computing the minimal A^e-resolution of A to degree 12 is linear algebra on matrices with at most a few thousand rows; seconds per algebra in QPA. Betti numbers of A over A^e can grow exponentially (complexity of A), but for n <= 12 and dim A <= 20 this stays tractable.

### 4.2 The search space, after the exclusion list

Let k be algebraically closed of char 0 for the main run (with a parallel run over F_p for large p and for p = 2, 3, 5 to probe the char-p gap). Filters, in order of cost:

F1. Q has an oriented cycle (otherwise gldim < infinity). [trivial]
F2. I is not monomial in ANY presentation: there must be a relation that is a nontrivial linear combination of at least two parallel paths (same source and target). Minimal quiver shapes: (i) one vertex, two loops x, y (local algebras); (ii) two vertices with two parallel arrows and a return arrow, or a 2-cycle plus a loop; (iii) three vertices on a cycle with a doubled arrow. [Han 2006]
F3. No 2-truncated oriented cycle in any presentation: for a local algebra, no x in J minus J^2 with x^2 = 0 (a quadric condition on P(J/J^2) that can be checked exactly); for general Q, for every oriented cycle a_1..a_l not all products a_i a_{i+1} vanish, for every choice of arrow bases. [Han 2010, Theorem 1]
F4. Not commutative; not a trivial extension of a local, self-injective or graded algebra; not a group algebra; not a QCI; not a corner, null-square projective, bounded or strongly proj-bounded extension of an algebra in the list; not derived equivalent to a monomial or skew-gentle algebra. [survey Tables 1 and 3; WXZZ 2024]
F5. In char 0: if I is homogeneous (with respect to path length or any positive grading) and Q has a loop, excluded (BM09 Thm 4.7); if A is N-Koszul, excluded (BM09 Thm 4.5). Consequence: the char-0 search must concentrate on NON-homogeneous relations (e.g. x^2 = y x y, or a relation mixing lengths 2 and 3), or on loop-free quivers with oriented cycles of length >= 2 and non-homogeneous or non-Koszul relations.
F6. CLMS necessary condition: A must not be of infinite + global dimension; if a loop exists at vertex u then Tor_*(k_u, u k) must be finite, so A must violate the extension conjecture at u. The extension conjecture is known for monomial and special biserial algebras, so candidates with loops must be neither. [CLMS 2026 Theorem 5.6, Prop. 6.11]
F7. Cheap numerical pre-filter: HH_1(A) = 0 and HH_2(A) = 0 computed from a degree-3 bimodule resolution. HH_1(A) = 0 is already a strong condition (for path algebras HH_1 != 0 as soon as the underlying graph is not a tree; survey Section 3) [V].

Size of the space: with the shapes (i)-(iii) and dim A <= 20, the relation ideals come in finitely many combinatorial types but with continuous parameters (coefficients). An exhaustive run is therefore over "relation shapes" with (a) generic parameters realized as random elements of F_p (Schwartz-Zippel), and (b) special parameter loci detected by Groebner-basis degenerations. Order of magnitude: 10^3 to 10^5 shapes, each in seconds. Feasible on one workstation in days.

### 4.3 Expected outcome and what would remain

Honest expectation [D, heuristic]: no hit in char 0 for dim <= 20. Reasons: (a) the WAK reformulation shows a counterexample needs a nonzero singularity category whose dg enhancement is Hochschild-acyclic outside degrees 0 and 1; the only known mechanisms producing Hochschild-acyclic nonzero dg categories are geometric phantoms, all with K_0-rank >= 11 upstairs; (b) small algebras have small, highly structured singularity categories (often CM-finite or 1-periodic), where the Kunneth argument of Section 3.1 (C2-d) pushes the problem back to algebraic phantoms; (c) Bergh-Madsen's Igusa-formula argument removes all graded shapes with loops in char 0.

Where a hit is not excluded by any theorem: (1) ungraded local algebras k<x,y>/(non-homogeneous relations), dim 5 to 12, with x^2, y^2, (x+ty)^2 all nonzero; (2) two- and three-vertex algebras with oriented cycles and commutativity-type relations, not special biserial; (3) in char p: graded local algebras with two loops and quadratic non-monomial relations that are not QCIs (BM09 unavailable), e.g. k<x,y>/(xy - q yx, x^2 - y^2) with q != -1 (which has no 2-truncated loop [D]), and graded cellular or Koszul algebras in char p.

If the run finds a candidate with HH_n = 0 for 1 <= n <= 12 and gldim = infinity, what remains: (i) a certificate of type (C2-a) or (C2-b); (ii) exclusion from every positive class up to derived equivalence; (iii) field independence. If the run finds nothing, the negative result "Han's property holds for all basic algebras of dimension <= N over k" is NOT established by the computation (parameter families are only sampled, and vanishing up to degree 12 is not vanishing in all degrees); proving it needs the classification lists (Gabriel dim <= 4, Mazzola dim 5, Happel dim 6 [V-sum]) plus case analysis, where the ungraded local algebras are the hard cases.

---

## 5. Candidate extension questions (novelty and difficulty)

Difficulty scale: L (weeks of computation and routine argument), M (a paper-length project with a clear path), H (needs a new idea), VH (comparable to the original counterexample).

E1. Explicit presentation of the KLS algebra (or of a variant on Bl_9(F_2) with 22 simples). Compute, over explicit points defined over Q satisfying Krah's genericity conditions, the Hille-Perling tilting bundle, Gamma by quiver and relations, the 13 complexes P_i^*, the folds N_i, and A = End_Lambda(Lambda + N) with its dimension and Cartan matrix. Novelty: high (the paper is non-constructive on every quantitative point) [V]. Difficulty: H (universal extensions on a 10-point blowup, Hom spaces via h^0 of many divisor classes, then an endomorphism algebra of dimension likely >= 10^3; a numerical HH sanity check on A is then out of reach because dim A^e would be >= 10^6). A byproduct would be the first explicit finite-dimensional algebra with a phantom-like singularity category and an invertible Cartan matrix [D]. Prerequisite check [U]: whether Krah's "general position" is an explicit Zariski-open condition satisfiable over Q; Mattoo (arXiv:2510.26107) works with dimension conditions 2.1 and 2.7 but does not make the points explicit [V-sum].

E2. Minimal number of simple modules of a Han counterexample. Lower-bound side: prove Han's property for all algebras with one simple (local algebras, ungraded) or with two simples; upper-bound side: 26 (KLS) or 22 (Bl_9(F_2) route [D]). Novelty: high; the local ungraded case is explicitly open (survey Section 5; SVP10 covers only special relations). Difficulty: H for local ungraded in general; M for dim <= 6 via the classification lists.

E3. Positive characteristic. (a) Does the KLS construction go through over F_p-bar (phantom on Bl_10(P^2) in char p, HKR in char p > 2, Hille-Perling in char p)? (b) Is there a graded or Koszul counterexample in char p, where Bergh-Madsen's proofs fail? Novelty: high; no source discusses fields other than C (KLS) or char 0 (Liu-Shen) [V]. Difficulty: (a) M-H (mostly checking that each cited theorem survives), (b) L for the computer search, H for a proof either way.

E4. Symmetric and self-injective algebras. For symmetric A, Han's property is equivalent to Happel's property [D]. Is there a symmetric algebra with hch.dim < infinity (equivalently a symmetric Han counterexample)? Known Happel counterexamples are non-symmetric [D]; the KLS algebra is not self-injective as far as the paper says [V absence]. The recent symmetric counterexample to Snashall-Solberg (arXiv:2608.17706, trivial extension of the Xu-Snashall algebra) is a trivial extension, so BM17 applies if the base algebra is graded, self-injective or local; it is therefore not a Han counterexample [D, subject to checking which BM17 hypothesis holds]. Novelty: high; difficulty: VH.

E5. Smaller geometric input. The P^2 route needs >= 10 points: del Pezzo surfaces are phantom-free (Pirozhkov, Adv. Math. 424 (2023)) and any surface with an effective smooth anticanonical divisor is phantom-free (Ma-Xiong-Yang, arXiv:2511.07114, Appendix B), which covers Bl_9(P^2) at general points (the unique cubic through the nine points) [D from V-abs]. Bl_9(F_2) has a phantom (arXiv:2511.05381) and K_0-rank 11, so it yields a counterexample with 22 simples [D]. Question: minimal K_0-rank of a smooth projective variety with a tilting bundle and a phantom. Novelty: medium-high; difficulty: H (phantom existence is the bottleneck).

E6. Algebraic phantoms. Is there a finite-dimensional algebra Gamma of finite global dimension, given by a small quiver with relations, such that Perf(Gamma) has a nonzero admissible subcategory with vanishing Hochschild homology? Any such Gamma feeds the KLS machine and gives a Han counterexample with 2 x (#simples of Gamma) simples [D]. Efimov's and Liu-Shen's finite-cell constructions produce kernels with nonzero HH (HH_0 = k^m, HH_1 = k in Liu-Shen) [V], so they do not qualify. Novelty: very high; difficulty: VH (this is the phantom-existence problem in noncommutative form).

E7. Structure theorem for "Hochschild-phantom" singularity categories. Characterize finite-dimensional algebras A with HH_n(Dsg^dg(A)) = 0 for n outside {0, 1}: prove necessary conditions (e.g. constraints from K_0(Dsg(A)) = coker of the Cartan matrix, from tau-Hochschild finiteness via CLMS Theorem 5.5, from the absence of 2-truncated cycles), and prove Han's property for Gorenstein CM-finite algebras or for algebras whose singularity category is 1-periodic (Section 3.1, C2-d). Novelty: high; difficulty: M-H; a good target for a rigorous partial result that also justifies the negative outcome of a small search.

E8. Certification infrastructure. Build the (C2-a) certificate pipeline (minimal A^e-resolution, syzygy-periodicity detection, exact HH_n) on top of QPA or QuiverLab, validate it against the known cases (BGMS quantum exterior algebras: HH^n = 0 for n >= 3 but HH_n != 0; Bergh-Erdmann QCIs; Han's monomial formulas; 2-truncated cycles), and run the Section 4.2 search. Novelty: low as mathematics, medium as a public reproducible artifact (no such validated tool exists in the literature I found [U]). Difficulty: L-M.

---

## 6. Sources

Primary, read in full or in the cited sections:
- B. Kong, Y. Liu, Y. Shen, A counterexample to Han's conjecture, arXiv:2608.00177v1 (31 Jul 2026). [V]
- Y. Liu, Y. Shen, A counterexample to DG version of Han's conjecture, arXiv:2512.12460v1 (13 Dec 2025). [V]
- G. da Costa Cruz, A survey on Han's conjecture, arXiv:2301.07511v2 (14 Sep 2023); Latin American J. Math. 2(2) (2023). [V]
- C. Cibils, M. Lanzilotta, E. N. Marcos, A. Solotar, Happel's question, Han's conjecture and tau-Hochschild (co)homology, arXiv:2509.05135v2 (17 Jun 2026), to appear in Annals of K-Theory. [V]
- Y. Wang, U. Arunachalam, B. Keller, On the Hochschild homology of singularity categories, C. R. Math. 360 (2022) 491-496, doi 10.5802/crmath.318. [V]
- Y. Han, Hochschild homology, global dimension, and truncated oriented cycles, arXiv:1004.0748. [V]
- Y. Han, Hochschild (co)homology dimension, J. London Math. Soc. 73 (2006) 657-668; arXiv:math/0408402. [V-sum]

Abstract or metadata level:
- R.-O. Buchweitz, E. L. Green, D. Madsen, O. Solberg, Finite Hochschild cohomology without finite global dimension, Math. Res. Lett. 12 (2005) 805-816. [V-abs; full text behind a 403]
- P. A. Bergh, K. Erdmann, Homology and cohomology of quantum complete intersections, Algebra Number Theory 2 (2008) 501-522. [V-abs]
- P. A. Bergh, D. Madsen, Hochschild homology and global dimension, Bull. LMS 41 (2009) 473-482; arXiv:0803.3550. [V-abs]
- P. A. Bergh, D. Madsen, Hochschild homology and trivial extensions, arXiv:1509.09039; Proc. AMS 145 (2017). [V-abs]
- C. Cibils, M. Lanzilotta, E. N. Marcos, A. Solotar, Han's conjecture for bounded extensions, J. Algebra 598 (2022); arXiv:2101.02597. [V-abs]
- Wang, Xu, Zhang, Zhou, A recollement approach to Han's conjecture, arXiv:2409.00945. [V-sum]
- J. Krah, A phantom on a rational surface, Invent. Math. 235 (2024) 1009-1018; arXiv:2304.01269. [V-abs, V-sum of html]
- A. Mattoo, Objects of a phantom on a rational surface, arXiv:2510.26107. [V-sum]
- Kemboi et al., A looming of phantoms, arXiv:2511.05381. [V-abs]
- S. Ma, Y. Xiong, S. Yang, A new phantom on a rational surface, arXiv:2511.07114. [V-abs]
- D. Pirozhkov, Admissible subcategories of del Pezzo surfaces, Adv. Math. 424 (2023); arXiv:2006.07643. [V-abs]
- L. Hille, M. Perling, Tilting bundles on rational surfaces and quasi-hereditary algebras, Ann. Inst. Fourier 64 (2014) 625-644; arXiv:1110.5843. [V-abs]
- X.-W. Chen, A note on the singularity category of an endomorphism ring, Ark. Mat. 53 (2015); arXiv:1307.6915. [V-abs]
- X.-W. Chen, Z. Wang, Differential graded enhancements of singularity categories, arXiv:2312.12138; EMS Congress Reports 21 (2025). [V-abs]
- J. Wei, Gorenstein homological theory for differential modules, Proc. Roy. Soc. Edinburgh A 145 (2015) 639-655. [V-sum]
- B. Keller, Invariance and localization for cyclic homology of DG algebras, JPAA 123 (1998). [V-abs]
- QPA manual, Chapters 4 (Section 4.17) and 8, docs.gap-system.org/pkg/qpa. [V-sum]
- QuiverLab 1.0.1, pypi.org/project/quiverlab, github.com/MarcoArmenta/quiverlab (released 2026-09-03). [V-sum; quality U]
- SageMath, sage.homology.hochschild_complex. [V-sum]
- Classification of small algebras: Gabriel (dim <= 4), Mazzola (dim 5, manuscripta math.), Happel (dim 6). [V-sum]

Not found / unverified: any paper computing Hochschild homology for all algebras of a given small dimension [U]; any Macaulay2 package for HH of finite-dimensional noncommutative algebras [U]; any statement by KLS about explicitness, dimension, or other fields [V: none in the text].
