# Dossier: realizability of integral points on pure rays in Boij-Soderberg theory, the Erman-Sam questions answered by Rethlas (May 2026), and what remains open

Date: 2026-09-02 (written 2026-09-03 early). Author: scouting agent (Lucy) for the CAOS research program.
Location: E:\_Temp\caos-research-newproblem\program\scouting-2026-09\2026-09-02-dossier-boij-soderberg-realizability.md
Working files: .\src\ (extracted texts of all primary sources; census scripts hk_census.py, census2.py, census3.py, census4.py, census5.py, appendix.py; raw Rethlas outputs rethlas-q61.md, rethlas-q62.md).

Marks: [V] verified against the primary source quoted (text extracted with pdftotext from the arXiv PDF, or read from the raw GitHub file); [D] derived in this dossier by elementary computation or by direct application of a quoted published statement, reproducible from .\src\; [U] unverified (claim from a secondary source, a memory, or a search snippet not confirmed in a primary text).

Notation: S = k[x,y,z] standard graded, k a field; H = Heisenberg Lie algebra with basis x,y,z, [x,y] = z, other brackets zero, deg x = deg y = 1, deg z = 2; U(H) its universal enveloping algebra with the induced grading. A degree sequence is d = (d0 < d1 < ... < dn). beta = (beta_0, ..., beta_n) denotes the nonzero entries beta_{i,d_i} of a pure Betti table. p(t) := sum_i (-1)^i beta_i t^{d_i} is the alternating Betti polynomial.

---

## 0. Executive summary

1. Erman and Sam (2016, Section 6) asked (Question 6.1) whether for every degree sequence (d0,d1,d2,d3) and every integral point on its pure ray there is a finite length graded module over S = k[x,y,z] OR over U(H) with that Betti table, and (Question 6.2) the analogous question in n variables allowing any n-dimensional positively graded Lie algebra generated in degree 1. [V]
2. Jiang, Li, Sun, Wang, Xiao, Yu (arXiv:2605.25259, May 2026, "resolved by Rethlas", AI-generated and human-verified) answer both negatively with one explicit primitive point each: (0,6,20,21) with beta = (1,2,9,8) for Question 6.1, and (0,1,4,5,6) with beta = (1,2,5,6,2) for Question 6.2. The S-side argument is Krull's height theorem (a cyclic finite length module needs at least 3 relations); the U(H)-side argument is a Hilbert series parity test (p(-1) must vanish). Nothing beyond the single counterexample is characterized: no classification, no smallest example, no statement about non-primitive multiples. [V]
3. Both halves of the Rethlas argument were already in the literature as general obstructions: the S-side is Erman's 2009 "codimension obstruction" (Proposition 3.1(2) of "The semigroup of Betti diagrams"), restated for pure tables by Erman and Sam themselves in Remark 7.4 of the survey that poses the question; the U(H)-side is the standard Hilbert series argument. The new content in the Rethlas paper is the search that found a degree sequence where the two obstructions coincide. [V] for the sources, [D] for the observation.
4. Census computed here (d3 <= 12, 220 degree sequences; scripts in .\src\): (0,6,20,21) is the unique degree sequence with d3 <= 60 whose primitive point is killed by exactly the Rethlas pair of arguments (beta_0 = 1, beta_1 = 2, plus parity failure). [D] But it is NOT the smallest counterexample to Question 6.1: the dual pair (0,1,6,10) with beta = (6,8,3,1) and (0,4,9,10) with beta = (1,3,8,6) are both non-realizable over S by published obstructions of Erman 2009 (the first is literally Erman's worked example in his Section 3; the second follows from "three generators of a height 3 ideal form a regular sequence", so the resolution is Koszul of type (0,4,8,12)) and both fail the U(H) parity test. They give counterexamples to Question 6.1 with d3 = 10 and are, within the obstruction set used here, the smallest possible. [D]
5. Over U(H) the parity test is scale invariant: it kills entire rays. For d3 <= 12 it kills 191 of the 220 rays, so on those rays Question 6.1 is exactly the polynomial ring question. Only 29 rays with d3 <= 12 can use U(H) at all. [D]
6. Status of the PRIMITIVE point over S for the 220 rays with d3 <= 12 (Appendix A): 52 realized (Eisenbud-Schreyer construction hitting the primitive point, or a classical construction: Koszul, S/m^a and its dual, Pfaffians of a generic skew matrix, or a scaled copy via the flat pullback x to x^e), 12 obstructed by published obstructions, 156 undecided, of which 150 have gcd(d1,d2,d3) = 1. The undecided ones are exactly where a computational classification would produce new results. [D]
7. Smallest realizable multiple: the general question is Erman 2009 Section 7 question (2) ("what is the minimal c_d such that c_d pi_d is the Betti diagram of some module?"), and EFW Conjecture 6.1 ("every sufficiently large integral point ... is actually the Betti table") remains open in general (Erman-Sam Section 8, 2016; no later resolution found in searches to September 2026). No published table of minimal multiples for three variables was found. [V] for the questions, [U] for the absence of later work.
8. Feasibility: for d3 <= 12 a complete decision of the primitive point (and of the first few multiples) over S is a medium computational project: Macaulay2's BoijSoederberg package already ships pureBetti, the three construction multiples (pureCharFree, pureTwoInvariant, pureWeyman) and two random-search generators (randomSocleModule, randomModule) whose documentation shows the primitive points of (0,2,3,9) and (0,2,3,7) being hit by random search. The upper bound from Eisenbud-Schreyer ranges from 1 to 5775 on this window, so the interesting rays are those where random inverse systems fail and no obstruction applies. [V] for the tooling, [D] for the numbers.
9. Attributable novelty candidates (Section 5): (A) a complete realizability table of the primitive point and minimal multiple for d3 <= 12 in three variables, with explicit modules and explicit obstructions; (B) the smallest Question 6.1 counterexample (the d3 = 10 pair above, then a proof that nothing with d3 <= 9 works, which needs U(H)-realizability of a few specific rays); (C) realization or obstruction theorems over U(H) for the S-obstructed parity-passing families; (D) a scale-sensitive obstruction on pure rays over S; (E) the exact minimal multiple on the Rethlas ray (currently 3 <= c_d <= 27132).

---

## 1. Definitions (with sources)

### 1.1 Betti tables, pure resolutions, degree sequences

For a finitely generated graded S-module M with minimal free resolution F, beta_{i,j}(M) := dim_k Tor_i(M,k)_j. Erman-Sam [ES16, Section 1]: "The Betti table of M is traditionally displayed as the following array or matrix" with rows indexed by j - i. [V]

Pure resolution [ES16, Section 1]: "a pure resolution of type d = (d0, ..., d_{n+1}) in Z^{n+2}, which is an acyclic complex where the i'th term is generated entirely in degree d_i; in other words, it is a minimal free complex of the form S(-d0)^{beta_{0,d0}} <- S(-d1)^{beta_{1,d1}} <- ... <- S(-d_p)^{beta_{n+1,d_{n+1}}} <- 0. Any such resolution must satisfy d0 < d1 < ... < d_{n+1}". [V]

### 1.2 Herzog-Kuhl equations and the pure ray

Rethlas paper [JLSWXY26, Section 3.7], verbatim: "A strictly increasing tuple (d0, d1, ..., dn) of integers is a degree sequence; the corresponding pure ray in the Boij-Soderberg cone is the half-line of Betti tables supported in degrees (i, di), i.e. with beta_{i,j} = 0 for j != di, whose nonzero entries beta_i := beta_{i,di} satisfy the Herzog-Kuhl equations sum_{i=0}^{n} (-1)^i beta_i d_i^m = 0, m = 0, 1, ..., n-1. An integral point on the ray is a tuple (beta_0, ..., beta_n) of nonnegative integers satisfying these equations. The equations have a one-dimensional solution space, with primitive integral point proportional to (prod_{j != i} |di - dj|^{-1})_{i=0,...,n}." [V]

Eisenbud-Schreyer [ES09, Section 0], verbatim: "In this case Herzog and Kuhl [1984] show that beta_{i,di} = lambda prod_{j != i} 1/|dj - di| for 0 <= i <= c for some rational number lambda. The proof relies on the equations imposed on the beta_{i,j}(M) by the vanishing of the first c coefficients of the Hilbert polynomial of M, corresponding to the fact that the support of M has codimension c. We will call these the Herzog-Kuhl equations." [V] Original: Herzog, Kuhl, "On the Betti numbers of finite pure and linear resolutions", Comm. Algebra 12 (1984), no. 13-14, 1627-1646. [V, bibliographic entry in ES09, EFW11, Erman09]

Erman [Erman09, Section 1]: "It was first shown in [HK] that any two pure diagrams of type d would be scalar multiples of one another." [V]

"Primitive vector of Betti numbers" [EFW11, Section 6]: "the smallest integral multiple of the Betti number on a ray of pure resolutions, corresponding to the given degree sequence d, which we call the primitive vector of Betti numbers." [V] Macaulay2's pureBetti is documented as "list of smallest integral Betti numbers corresponding to a degree sequence". [V]

### 1.3 The cone, its extremal rays, and the meaning of "integral point"

Erman-Sam [ES16, Section 1]: B_c(S) := Q_{>=0}{beta(M) | codim M >= c}; Boij and Soderberg conjectured and Eisenbud-Schreyer proved that the extremal rays of the finite length cone B_{n+1}(S) are exactly the pure rays indexed by degree sequences, and that the cone is a simplicial fan indexed by chains of degree sequences in the termwise partial order. [V] Existence of pure resolutions "was first proven in [22] (= EFW) in characteristic zero and in [25] (= ES) in general" [ES16, Section 1]. [V]

Erman [Erman09, Definitions 1.1-1.2]: the semigroup of Betti diagrams B_mod (images of actual modules), the cone B_Q, and the semigroup of virtual Betti diagrams B_N := lattice points of B_Q. Realizability of an integral point on a pure ray is the question whether that lattice point of B_N lies in B_mod. [V]

### 1.4 Realizability over S, scaling, duality

Realizable over S: there is a finite length graded S-module whose Betti table equals the given integral point (Question 6.1 wording, [ES16]). [V]

Scaling lemma [D]: if (d, beta) is realizable over S then (e d, beta) is realizable over S for every integer e >= 1. Proof: let S' = k[u,v,w] graded with deg u = deg v = deg w = e and phi: S' to S, u to x^e, v to y^e, w to z^e. S is a free S'-module (basis x^a y^b z^c with 0 <= a,b,c < e), so phi is flat; a minimal graded free resolution F of M over S' base-changes to a free resolution of M tensor S, minimal because the entries of the differentials lie in (u,v,w)S', which lies in (x,y,z)S; the twists S'(-d_i) become S(-e d_i) and the ranks are unchanged; M tensor S has finite length because S is finite over S'. The primitive Herzog-Kuhl point of e d equals that of d since all products prod |di - dj| scale by e^n. Used in Appendix A to transfer six realizations from gcd-reduced sequences. The converse (realizable at e d implies realizable at d) is not known to me. [U]

Duality [D, standard]: for a finite length graded S-module M, Ext^3_S(M,S) is finite length with the reversed Betti table (beta_i to beta_{3-i}, degree sequence d to (0, d3 - d2, d3 - d1, d3) up to shift). Hence realizability over S of the primitive point is invariant under d to (0, d3-d2, d3-d1, d3). Whether the same holds over U(H) is not settled here. [U]

### 1.5 The Lie-algebra (non-commutative) variant

Erman-Sam [ES16, Section 6], verbatim: "Consider the degree sequence (0,1,3,4). The Herzog-Kuhl equations state that any finite length module over a polynomial ring in 3 variables with a pure resolution of type (0,1,3,4) is a multiple of the following table: (2) [1 2 - - / - - 2 1]. One can easily deduce that this Betti table is non-realizable: this would be the Betti table of k[x,y,z]/I where I is generated by two linear forms, which must then have a linear Koszul relation. However, there is a way to realize this as the Betti table of a finite length module if we are willing to replace k[x,y,z] by another algebra. In particular, define a 3-dimensional Lie algebra H (Heisenberg Lie algebra) with basis {x,y,z} and the following multiplication [x,y] = z, [x,z] = [y,z] = 0. ... H is graded via deg(x) = deg(y) = 1 and deg(z) = 2. In this case, minimal free resolutions of graded modules are well-defined. The Chevalley-Eilenberg complex ... always gives a free resolution of the residue field, but is not necessarily minimal. For H, the Chevalley-Eilenberg complex looks like: 0 <- U(H) <- U(H)(-1)^2 (+) U(H)(-2) <- U(H)(-2) (+) U(H)(-3)^2 <- U(H)(-4) <- 0. The two terms of degree 2 cancel since it corresponds to the redundancy xy - yx = z. So we get the following minimal free resolution: 0 <- U(H) <- U(H)(-1)^2 <- U(H)(-3)^2 <- U(H)(-4) <- 0 and hence we can realize (2)." [V]

"This suggests that non-realizable integral points in the Boij-Soderberg cone may be realizable over U(g) for a Z_{>0}-graded Lie algebra g. Note that a finite-dimensional Z_{>0}-graded Lie algebra g is necessarily nilpotent since [g, g_i] is contained in g_{i+1}. Also, a standard graded polynomial ring in n variables is U(k^n) where k^n is the abelian Lie algebra of dimension n concentrated in degree 1. In dimension 2, every nilpotent Lie algebra is abelian, and in dimension 3, the only possibilities are k^3 and H (to normalize, we insist that the generators of the Lie algebra consist of degree 1 elements). It is easy to see that every integral point on a pure ray in the Boij-Soderberg cone in 2 variables is realizable, so we offer the following question:" [V]

The word "equivariant" in the task refers to a different object: EFW's GL(m)-equivariant pure resolutions in characteristic 0 (Section 3.2 below). The Lie algebra variant is a non-commutative deformation; Remark 6.3 of [ES16]: "We are appealing to the fact that U(g) 'looks like' a graded polynomial algebra, which is made precise by the Poincare-Birkhoff-Witt theorem. One could also study other non-commutative algebras that look like graded polynomial algebras. ... As a starting point, one may consider Artin-Schelter algebras". [V]

Hilbert series of U(H) [JLSWXY26, proof of Theorem 3.7]: by PBW, H_{U(H)}(t) = sum t^{a+b+2c} = 1/((1-t)^2 (1-t^2)). [V] Compare S: 1/(1-t)^3. Consequence [D]: over S the Herzog-Kuhl equations are equivalent to (1-t)^3 dividing p(t); over U(H) the finite length condition requires (1-t)^3 (1+t) | p(t), i.e. additionally p(-1) = sum (-1)^{i + d_i} beta_i = 0. This "parity test" is homogeneous of degree 1 in beta, hence a property of the ray, not of the point.

---

## 2. The Erman-Sam questions and the Rethlas answers

### 2.1 The questions, verbatim

[ES16, Section 6]:

"Question 6.1. For every degree sequence (d0, d1, d2, d3), and every integral point on the corresponding ray in the Boij-Soderberg cone, is there a finite length module either over k[x,y,z] or U(H) whose Betti table is that integral point?" [V]

"Of course, there is a natural extension for any number of variables: Question 6.2. For every degree sequence (d0, ..., dn), and every integral point on the corresponding ray in the Boij-Soderberg cone, does there exist an n-dimensional Z_{>0}-graded Lie algebra g generated in degree 1, and a finite length module over U(g) whose Betti table is that integral point?" [V]

Surrounding remarks [ES16, Section 6]: "One source of examples for Z_{>0}-graded Lie algebras are the nilpotent radicals of parabolic subalgebras of (split) reductive Lie algebras. ... Over a field of characteristic 0, Kostant's version of the Borel-Weil-Bott theorem ... calculates the Tor groups of the restriction of an irreducible representation from the reductive Lie algebra to the nilpotent one. In fact, the EFW complexes are a special case of Kostant's calculation where the reductive Lie algebra is gl_{n+1} and we take the nilpotent radical of the subalgebra of block upper-triangular matrices with block sizes 1 and n (in this case, the nilpotent radical is abelian). Furthermore, one can construct many kinds of pure resolutions using this construction, though not necessarily all degree sequences are realizable (in the EFW case, they are). We point out that H can be realized as the nilpotent radical for a parabolic subalgebra of the symplectic Lie algebra sp_4 (see [52, Section 2.2]), and using this representation-theoretic perspective, one can realize more integral points which are not realizable over k[x,y,z] than the example presented above. Details will appear in forthcoming work of the second author." [V] ([52] = S. Sam, Homology of analogues of Heisenberg Lie algebras, Math. Res. Lett. 22 (2015), arXiv:1307.1901.) No such forthcoming work was located in web searches (September 2026); the Rethlas paper does not cite one either. [U]

### 2.2 The Rethlas paper

Bibliographic: Jiedong Jiang, Yixiao Li, Zeming Sun, Yuefeng Wang, Liang Xiao, Jiahong Yu, "On some open problems in commutative algebra resolved by Rethlas", arXiv:2605.25259, v1 24 May 2026, v2 28 May 2026, 13 pages, comment "AI-generated, human verified", MSC 13C15, 13D02, 13F05, 13F20, 13J10, 17B55, 05E40, CC BY 4.0. [V] The raw system outputs are in github.com/frenzymath/Rethlas_results, directory CommAlg/arxiv_1606_01867/, files question_6_1.md (2736 bytes) and question_6_2.md (6206 bytes). [V, files downloaded to .\src\]

Abstract (from arXiv): the paper "reports on a collection of open problems in commutative algebra and related areas that have been resolved (proved or disproved) using the Rethlas natural-language automated reasoning system", problems drawn from Cahen-Fontana-Frisch-Glaz's "Open problems in commutative ring theory" and Erman-Sam's survey; "For each problem the paper records the precise statement and a self-contained proof produced (with no human intervention) by Rethlas and subsequently verified by human experts." [V] The paper contains eight problems: Problems 2.1-2.6 (ring theory) and Questions 2.7-2.8 (Boij-Soderberg), with proofs in Sections 3.1-3.8. [V] Rethlas is described in the companion paper Ju et al., "Automated Conjecture Resolution with Formal Verification", arXiv:2604.03789 (2026). [V, bibliographic]

Introduction, verbatim: "Finally, we address two questions on Boij-Soderberg theory [2, 7]. A natural problem in this theory is to determine which integral points on a pure ray of the Boij-Soderberg cone are realizable as Betti table of some module. Question 2.7 asks whether every such point (in codimension 3) is realized over either S = k[x,y,z] or the enveloping algebra of the Heisenberg Lie algebra; Question 2.8 asks the analogous question for arbitrary finite-dimensional positively graded Lie algebras generated in degree 1. Both answers are negative, via constructing explicit degree sequences whose primitive integral points cannot be realized." [V]

### 2.3 Question 2.7 (= Erman-Sam 6.1): Theorem 3.7 and its proof, verbatim

"Theorem 3.7. Let k be a field, let S = k[x,y,z] with deg(x) = deg(y) = deg(z) = 1, and let H be the Heisenberg Lie algebra on basis {x,y,z} with [x,y] = z, [x,z] = [y,z] = 0, graded by deg(x) = deg(y) = 1, deg(z) = 2. There exist a degree sequence (d0,d1,d2,d3) and an integral point on the corresponding pure ray in the Boij-Soderberg cone that arises as the Betti table of no finite length graded module over S and of no finite length graded module over U(H)." [V]

"Proof. Take the degree sequence (d0,d1,d2,d3) = (0,6,20,21). The codimension-3 Herzog-Kuhl ratios for this pure ray are 1/(6*20*21) : 1/(6*14*15) : 1/(20*14*1) : 1/(21*15*1) = 1 : 2 : 9 : 8, so beta = (1,2,9,8) is an integral point on that ray. We show beta is realizable over neither S nor U(H).

Not realizable over S. If a finite length graded S-module M had Betti table beta, then beta_0(M) = 1, so M = S/I for some homogeneous ideal I, and beta_1(M) = 2 means I is generated by two elements. By Krull's height theorem ht(I) <= 2, so dim(S/I) >= 1, contradicting finite length.

Not realizable over A := U(H). By the Poincare-Birkhoff-Witt theorem, the monomials x^a y^b z^c form a graded k-basis of A with deg(x) = deg(y) = 1, deg(z) = 2, so H_A(t) = sum_{a,b,c >= 0} t^{a+b+2c} = 1/((1-t)^2 (1-t^2)). If a finite length graded A-module N had Betti table beta, then H_N(t) = (1 - 2t^6 + 9t^20 - 8t^21)/((1-t)^2 (1-t^2)), and H_N(t) must be a polynomial. Hence P(t) := 1 - 2t^6 + 9t^20 - 8t^21 must be divisible by (1-t)^2 (1-t^2), and in particular by 1+t. However, P(-1) = 1 - 2 + 9 + 8 = 16 != 0, so 1+t does not divide P(t), contradiction. Therefore the integral point (1,2,9,8) on the pure ray for (0,6,20,21) is realizable over neither S nor U(H)." [V; identical in the raw output question_6_1.md, which ends "Hence the answer to the question is negative."]

Verification here [D]: hk_census.py reproduces (0,6,20,21) to (1,2,9,8) and P(-1) = 16.

Remarks in the paper about this result: none beyond the proof. There is no discussion of minimality, of other degree sequences, of non-primitive multiples on the same ray, of the dual sequence (0,1,15,21), or of the points 2 beta, 3 beta, ... [V by absence: full text read]

Note on the raw output [V]: the raw statement block in question_6_1.md paraphrases Erman-Sam as "It is easy to see that every integral point on a pure ray in the Boij-Soderberg cone of dimension <= 3 is realizable over either k[x,y,z] or U(H)", which misreads the survey (the survey says this for 2 variables and asks it for 3). The published paper's Question 2.7 states the question correctly.

### 2.4 Question 2.8 (= Erman-Sam 6.2): Theorem 3.8 and its proof

"Theorem 3.8. Let k be a field. There exist an integer n >= 1, a degree sequence (d0, ..., dn), and an integral point on the corresponding pure ray in the Boij-Soderberg cone for which no n-dimensional Z_{>0}-graded Lie algebra g generated in degree 1 over k admits a finite length graded module M over U(g) whose Betti table is that integral point." [V]

Proof structure [V]: n = 4, d = (0,1,4,5,6). Step 1: solving the four Herzog-Kuhl equations with beta_0 = 1 gives beta_3 = 3 beta_4, 2 beta_2 = 5 beta_4, beta_1 = beta_4, beta_4 = 2, so (1,2,5,6,2), "which is already integral, hence the primitive integral point on the ray". Step 2 (Lemma lem:pbw-hilbert-series in the raw output): for g = (+) g_i with h_i = dim g_i, PBW gives H_{U(g)}(t) = prod_{i >= 1} (1 - t^i)^{-h_i}, and for a finite length graded U(g)-module with a pure resolution, p_M(t) is divisible by prod (1 - t^i)^{h_i}. Step 3: p(t) = 1 - 2t + 5t^4 - 6t^5 + 2t^6 = (1-t)^4 (2t^2 + 2t + 1); since sum h_i = 4, after dividing by (1-t)^4 the quotient q = 2t^2 + 2t + 1 must be divisible by prod_{i >= 2} (1 + t + ... + t^{i-1})^{h_i}; q(-1) = 1 != 0, q = -1 mod (1 + t + t^2), and deg q = 2 excludes i >= 4; hence h_i = 0 for i >= 2, g is concentrated in degree 1, hence abelian, U(g) = k[x1,...,x4], and then beta_0 = 1, beta_1 = 2 with Krull's height theorem gives dim R/I >= 2, contradicting finite length. [V]

Remarks: the argument is again "Krull obstruction on the polynomial ring" plus "Hilbert series divisibility forces the Lie algebra to be abelian". It does not address n = 3 with all Lie algebras (that is Question 6.1, since in dimension 3 only k^3 and H exist), and it gives no positive result. [V]

### 2.5 What the Rethlas result does and does not establish

- Establishes: Questions 6.1 and 6.2 have negative answers; one explicit primitive point each. [V]
- Does not establish: any characterization of realizable points; the smallest counterexample; behaviour of multiples; anything about U(H) beyond the Hilbert series; anything positive. [V by reading]
- Both ingredients are old [V]: Erman 2009, Proposition 3.1(2) ("Codimension obstruction: b = sum_j beta_{1,j}(M) >= e + a - 1", a = number of generators, e = codimension), applied with a = 1, e = 3 gives beta_1 >= 3. Erman-Sam 2016 Remark 7.4 says of the pure diagrams of Proposition 7.2 with beta_0 = 1 and beta_1 = r: "the codimension of S/I is bounded above by r, which is a contradiction. Thus, the pure Betti tables constructed in the proof of Proposition 7.2 cannot correspond to an actual Betti table. Of course, some scalar multiple of each table does come from an actual Betti table." Erman 2009 also proves (Theorem 1.6(3)) that for a prime P the ray of d = (0, 1, P+1, P+2, ..., 2P) in P+1 variables has beta_0 = 1, beta_1 = 2 at its primitive point and hence its first P - 1 lattice points are all obstructed. So the polynomial ring half of both Rethlas theorems is a special case of published results; the Rethlas contribution is the pairing with the Lie algebra Hilbert series and the specific search.

---

## 3. What is known about which integral points are realizable

### 3.1 Two variables: everything

[ES16, Section 6]: "It is easy to see that every integral point on a pure ray in the Boij-Soderberg cone in 2 variables is realizable". [V] Erman 2009, Proposition 1.4: "B_N = B_mod for projective dimension 1 and for projective dimension 2 level modules", proof resting on Soderberg, "Artinian level modules of embedding dimension two", J. Pure Appl. Algebra 207 (2006) 417-432, which constructs level modules with any admissible Hilbert function as quotients of monomial ideals. [V] Erman's Conjecture 1.5: B_N = B_mod for all projective dimension 2 diagrams. [V]

### 3.2 Three constructions, each realizing SOME multiple of the primitive point

(a) Eisenbud-Schreyer, any field [ES09, Theorem 5.1], verbatim: "Let K be any field, and let d = (d0 < ... < dn) be a sequence of integers. There exists a graded K[x1,...,xn]-module of finite length with beta_0 = prod_{i=1}^{n} binom(di - d0 - 1, di - d_{i-1} - 1) generators, whose minimal free resolution is pure with degree sequence d." Built by pushing forward a Koszul complex on P^{n-1} x P^{m_1} x ... x P^{m_n} (m_i = di - d_{i-1} - 1); "In the case where di - d_{i-1} = 1 for all but one value of i, the complexes we produce coincide with those of Buchsbaum-Eisenbud [1973a] and Kirby [1974]". [V] Implemented as pureCharFree in Macaulay2's BoijSoederberg package (returns beta_0) and as pureResolution in the BGG package. [V] Numbers checked here [D]: for (0,3,4,7) beta_0 = 15 (EFW Example 6.2 says "the Eisenbud-Schreyer construction gives 15"), for (0,2,3,9) beta_0 = 56 (M2 doc), for (0,6,20,21) beta_0 = 27132, i.e. the ES module on the Rethlas ray is the 27132-th multiple of the primitive point. Discrepancy flagged [U]: for (0,4,9,13) EFW Example 6.3 says the ES construction gives 380 beta with primitive beta = (5,13,13,5), while the Theorem 5.1 formula gives beta_0 = 15400, i.e. the 3080-th multiple; recompute with pureCharFree before quoting either number.

(b) Eisenbud-Floystad-Weyman, characteristic 0, GL(m)-equivariant [EFW11, Theorems 0.1, 3.2]: for d with e_i = di - d_{i-1}, the complex F(d) has F(d)_i = S_{alpha(d,i)} E tensor A(-di) where alpha(d,i) is obtained from the partition alpha(d,0) by adding e_j boxes to column j for j <= i; "The complex F(d)(E) is a minimal graded free resolution, and the generators of F(d)_i have degree di" and "M(d) is finite dimensional as a vector space". [V] So beta_i = dim S_{alpha(d,i)}(k^m) (hook-content formula). Implemented as pureWeyman (docs reference 0709.1529v3 Section 4) and pureTwoInvariant (the second EFW construction, Theorem 0.2). [V] EFW Section 0: "There is a unique minimum possibility, determined solely by integrality considerations, and it is easy to see that only integral multiples of this minimum can occur. It is known from many examples, that not all occur." [V]

(c) Tensor complexes [BEKS13, Theorem 1.9]: "Let d = (d0, ..., dp) in Z^{p+1} be a degree sequence. Then there exist infinitely many choices of a, b, and w such that w is a pinching weight for a x b, F(a x b, w) is a pure resolution of type d, and M(a x b, w) is a Cohen-Macaulay module that is flat over Z." "The Eisenbud-Schreyer construction arises as a hyperplane section of a certain tensor complex (see Theorem 10.2)." "Our results thus provide the first explicit description of pure resolutions over a field of positive characteristic". [V] Implemented as pureResTC; the M2 documentation example shows pureResTC({0,2,4,5}) with Betti table total (3,10,15,8), which is exactly the primitive point of (0,2,4,5) (hk_census.py). [V for the doc, D for the comparison]

(d) Classical constructions hitting the primitive point [D, all standard]:
- Koszul complex: (0,a,2a,3a) with (1,3,3,1).
- S/m^a: pure of type (0,a,a+1,a+2) (Eagon-Northcott); the census confirms these coincide with the primitive points, e.g. (0,2,3,4) to (1,6,8,3), (0,3,4,5) to (1,10,15,6), (0,4,5,6) to (1,15,24,10). Erman-Sam Section 1 cite S/(x1,x2,x3)^2 as realizing the (0,2,3,4) table. [V]
- Duals of the above: (0,1,2,a+2) with reversed Betti numbers (Ext^3(S/m^a,S)); Erman 2009 Example 4.6 uses N (+) N^vee(4) with N = k[x,y,z]/(x,y,z)^2. [V]
- Pfaffians (Buchsbaum-Eisenbud 1977): a Gorenstein codimension 3 ideal with n = 2r+1 generators of degree a and relations of degree b has resolution 0 <- S <- S(-a)^n <- S(-b)^n <- S(-a-b) <- 0 with a = r(b-a); conversely a generic skew (2r+1) x (2r+1) matrix of forms of degree b-a in three variables has Pfaffian ideal of codimension 3 (finite length), so every primitive point of the form (1,n,n,1) with n odd on a ray (0,a,b,a+b) is realized. EFW Example 6.2 states this for (0,3,4,7): "in this case we know that the primitive vector is achieved by the minimal free resolution of the ideal of 6 x 6 Pfaffians of a 7 x 7 skew-symmetric matrix of linear forms; see Buchsbaum and Eisenbud [1975]". [V for the example, D for the general statement]

### 3.3 Obstructions in print (three variables, pure tables)

Erman 2009, Proposition 3.1 (Buchsbaum-Rim obstructions), for M of codimension e >= 2 with minimal presentation (+)_{l=1}^{b} S(-j_l) to S^a to M to 0, j_1 <= ... <= j_b [V]:
(1) second syzygy obstruction: d_2(M) <= sum_{l=1}^{a+1} j_l;
(2) codimension obstruction: b >= e + a - 1, and "If we have equality, then beta(M) must equal the Betti diagram of the Buchsbaum-Rim complex of phi";
(3) regularity obstruction (Cohen-Macaulay case): reg(M) + e = d_e(M) <= sum_{l = b-e-a+2}^{b} j_l.
Erman's own examples [V]: "the pure diagram pi(0,1,alpha,alpha+1) has a codimension obstruction for any alpha >= 3"; "For the case of equality in Proposition 3.1(2), consider pi(0,1,6,10) = [6 8 - - / ... 3 / ... 1]. Since we have beta_{1,j}(pi(0,1,6,10)) = 8 = 3 + 6 - 1, the diagram pi(0,1,6,10) should equal the Betti table of the Buchsbaum-Rim complex on a map phi: R(-1)^8 to R^6. This is not the case."

Applied to m times the primitive point beta of a ray (0,d1,d2,d3) in three variables (e = 3, all relation degrees d1) these read [D]:
(1) d2 <= (m beta_0 + 1) d1; (2) m (beta_1 - beta_0) >= 2; (3) d3 <= (m beta_0 + 2) d1.
Each gives a lower bound on the realizable multiple m. On the Rethlas ray (0,6,20,21) they give m >= 3 (from (1): 20 <= 6(m+1)), so at least TWO lattice points, beta and 2 beta, are missing over S, which the Rethlas paper does not note. [D]

Erman 2009, Section 4 (linear strand / maximal minor obstruction in projective dimension 3, from Buchsbaum-Eisenbud 1974 multiplier ideals), Proposition 4.1 and Proposition 4.5: non-pure examples such as D = [2 4 3 - / - 3 4 2] (a sum of two pure diagrams) are not Betti tables although 2D is, and Theorem 1.6(4) shows 3D is not. [V] These do not apply to pure rays directly but are the model for an obstruction "sensitive to scalar multiplication" [V, Erman Section 3 opening].

Buchsbaum-Eisenbud structure theorem (codimension 3 Gorenstein ideals are Pfaffian ideals, hence have an odd number of generators) [V, cited as [BE77] by Erman and as [13] by Erman-Sam]: a cyclic pure point (1, n, n, 1) with n even is not realizable over S. [D] On the window d3 <= 12 this excludes (0,3,5,8) with (1,4,4,1) and (0,5,7,12) with (1,6,6,1) (and re-excludes the (1,2,2,1) family). Similarly three generators of a height 3 ideal in S form a regular sequence, so a cyclic pure point with beta_1 = 3 forces d = (0,a,2a,3a). [D] This excludes (0,4,9,10) with (1,3,8,6). Neither of these two elementary obstructions is stated in Erman 2009 or Erman-Sam 2016 in this form. [V by reading; "new in print" is plausible but [U] against the wider literature]

Erman 2009, Theorem 1.6 [V]: (1) B_mod is not saturated: on the ray of (0,1,3,4) "every lattice point except D1 itself belongs to B_mod" (2 D1 is the Buchsbaum-Rim complex of a generic 2 x 4 matrix of linear forms; 3 D1 is realized by an explicit 3 x 6 matrix); (2) |B_N \ B_mod| can be infinite; (3) rays missing at least dim S - 2 consecutive lattice points (the (0,1,P+1,...,2P) family); (4) rays where the realizable points are nonconsecutive.

Characteristic dependence [V, Erman Section 7(3)]: Kunte (thesis 2008; "Gorenstein modules of finite length", Math. Nachr. 2011) shows the pure diagram [1 / 10 16 / 16 10 / 1] (five variables) is not a Betti diagram in characteristic 2 but is in characteristic 0. So realizability tables must record the characteristic.

### 3.4 The "sufficiently large multiple" conjecture and the "smallest multiple" question

EFW Conjecture 6.1 [V]: "Every sufficiently large integral point in the ray defining the possible pure Betti tables of graded modules of finite length over a polynomial ring, with a given degree sequence, is actually the Betti table of the free resolution of a Cohen-Macaulay module." EFW Examples (verbatim) [V]: (0,3,4,7): primitive (1,7,7,1); "The construction of Section 3 gives Betti numbers 6 beta, the Eisenbud-Schreyer construction gives 15 beta and the construction from Section 4 gives 50 beta. Thus all three are needed in order to conclude the conjecture for this extremal ray"; (0,4,9,13): primitive (5,13,13,5), multiples 18, 380, 9075; (0,1,4,6): primitive (5,8,5,2), "All three constructions give 5 beta. This is the smallest sequence for n = 3 where we cannot conclude the conjecture using our three constructions."

Erman-Sam 2016, Section 8 [V]: "Eisenbud, Floystad, and Weyman conjecture that every sufficiently large integral point on an extremal ray comes from an actual Betti table [22, Conjecture 6.1]. This conjecture remains open, though it is known to be false for interior rays in the cone [20, Example 1.7]." ([20] = Eisenbud-Erman-Schreyer, Filtering free resolutions, Compos. Math. 149 (2013).)

Erman 2009, Section 7, question (2) [V]: "The behavior of single rays: Given a degree sequence d, what is the minimal c_d such that c_d pi_d is the Betti diagram of some module? In many cases where computation is feasible, it is known that the examples produced by [EFW] and [ES] do not represent the first element of B_mod on the ray. In some other cases, it is known that pi_d itself does not belong to B_mod so that c_d is greater than 1. Can we find better lower and upper bounds for the integer c_d?"

Semigroup remark [D, elementary]: the set of realizable multiples on a ray is closed under addition (direct sums); if two coprime multiples are realized then all large multiples are (this is how EFW argue for (0,3,4,7) and (0,4,9,13)). Macaulay2's pureAll documentation says exactly this and shows gcd(56,196,21) = 7 for (0,2,3,9), then exhibits the primitive point (7,27,21,1) by randomSocleModule({0,2,3,9},1). [V]

Later work: searches for "smallest realizable multiple", "minimal c_d", "pure Betti table realizable three variables" (2017-2026) returned nothing on the minimal-multiple problem in three variables; Ananthnarayan-Kumar 2018 (Comm. Algebra 46) and Ananthnarayan-Javadekar-Kumar arXiv:2607.06394 (July 2026, "Purity of extremal rays of Betti cones") concern cones over other rings, not integral points. Danus (arXiv:2607.06447, July 2026) mentions Rethlas only as a system. [U: absence of evidence]

### 3.5 Macaulay2 tooling relevant to a classification (all [V] from the online docs)

BoijSoederberg package: pureBetti (smallest integral Betti numbers), pureBettiDiagram, pureCharFree / pureTwoInvariant / pureWeyman / pureAll (the beta_0 of the three constructions), decompose (Boij-Soderberg decomposition), randomSocleModule(L,m) ("a generic module of finite length with the m generators and number of socle elements and regularity corresponding to the pure resolution with degree sequence L"; "There are many cases where these produce pure resolutions of the minimal size"; doc example: {0,2,3,7}, m = 1 gives total (10,42,35,3), which is the primitive point), randomModule(L,m) ("randomly generated having m b_0 generators in degree L_0 and m b_1 relations in degree L_1"; doc example: {0,4,9,10}, m = 1 gives the Koszul table (1,3,3,1) in degrees 0,4,8,12, not the pure table). TensorComplexes package: pureResTC (verified), pureResES (name from search results [U]). BGG package: pureResolution "creates a pure resolution as an iterated direct image" (the ES sparse one).

---

## 4. Census for d3 <= 12 and feasibility of an exact computation

### 4.1 Size of the surface (all [D], scripts in .\src\)

- Degree sequences (0,d1,d2,d3) with d3 <= 12: 220. With d3 <= 60: 34,220.
- Primitive points with beta_0 = 1 (cyclic candidates): 44 of 220. beta_0 <= 3: 79. beta_0 >= 20: 53. Sum of primitive Betti numbers <= 20: 41 rays; <= 60: 90; > 200: 30 (max 378, e.g. (0,2,7,11) with (90,154,99,35)).
- Eisenbud-Schreyer multiple (beta_0^{ES}/beta_0^{prim}) is an integer on all 220 rays; it equals 1 on 33 rays (all (0,1,2,d3), all (0,a,a+1,a+2), and 10 others), is <= 5 on 69, <= 20 on 122, > 100 on 32, max 5775.
- U(H) parity p(-1) = 0 holds on 29 of 220 rays; on the other 191 no point of the ray is realizable over U(H) (scale invariance), so Question 6.1 there is purely about S. On the 29 rays, the U(H) Hilbert function of the primitive point has nonnegative coefficients in all cases (no further Hilbert series obstruction).
- Over S the primitive Hilbert function is nonnegative on all 220 rays (no ray-level Hilbert obstruction).

### 4.2 Status of the primitive point over S (Appendix A has the full table)

- Realized: 52 (33 by the ES formula hitting beta_0^{prim}; Koszul, S/m^a, its dual, generic Pfaffians; 6 by the scaling lemma). (0,2,3,7) is also realized per the M2 randomSocleModule documentation example (total (10,42,35,3)), so the realized count is at least 53; it is listed as undecided in the mechanical table because the table only uses formulas.
- Obstructed by published results: 12. Rays and reasons:
  (0,1,3,4) (1,2,2,1); (0,2,6,8) (1,2,2,1); (0,3,9,12) (1,2,2,1): codimension obstruction (Erman 3.1(2); Erman-Sam's own example).
  (0,1,5,6) (2,3,3,2); (0,1,7,8) (3,4,4,3); (0,1,9,10) (4,5,5,4); (0,1,11,12) (5,6,6,5); (0,2,10,12) (2,3,3,2): codimension obstruction, beta_1 - beta_0 = 1 < 2 (Erman's (0,1,alpha,alpha+1) family and a scaled copy).
  (0,1,6,10) (6,8,3,1): equality case of the codimension obstruction, Erman's explicit example.
  (0,4,9,10) (1,3,8,6): second syzygy obstruction (9 > 2*4) and the three-generator regular sequence argument; dual of (0,1,6,10).
  (0,3,5,8) (1,4,4,1); (0,5,7,12) (1,6,6,1): Buchsbaum-Eisenbud parity (even number of generators of a codimension 3 Gorenstein ideal).
  For all twelve, the second lattice point 2 beta is not excluded by these obstructions (m >= 2 in every case), and for the five (1,2,2,1)/(a,a+1,a+1,a) rays with ES multiple 2 the second point IS realized (ES), so on those rays c_d = 2 exactly. [D]
- Undecided: 156, of which 150 have gcd(d1,d2,d3) = 1. The smallest (by total Betti number) undecided primitive points: (0,3,7,10) (2,5,5,2) [ES multiple 360]; (0,1,3,6) (5,9,5,1) [4]; (0,1,4,6) (5,8,5,2) [3, EFW's Example 6.4]; (0,2,3,6) (2,9,8,1) [5]; (0,2,5,6) (2,5,8,5) [3]; (0,2,5,7) (3,7,7,3) [12]; (0,3,4,6) (1,8,9,2) [5]; (0,3,5,6) (1,5,9,5) [4]; (0,2,7,9) (5,9,9,5) [24]; (0,4,7,11) (3,11,11,3) [600].

### 4.3 The two counterexamples with d3 = 10 and the minimality question

[D] Over S: (0,4,9,10), beta = (1,3,8,6). A finite length cyclic module S/I with three minimal generators of degree 4: ht I = 3 = number of generators, S is Cohen-Macaulay, so the generators form a regular sequence and the minimal resolution is the Koszul complex on three quartics, of type (0,4,8,12), not (0,4,9,10). Hence beta is not realizable over S. By duality (Ext^3(-,S)) the primitive point (6,8,3,1) of (0,1,6,10) is not realizable either, which is also Erman's 2009 worked example (equality case of Proposition 3.1(2)). Over U(H): p(t) = 1 - 3t^4 + 8t^9 - 6t^10 has p(-1) = -16 != 0, and for (0,1,6,10), p(t) = 6 - 8t + 3t^6 - t^10 has p(-1) = 16 != 0. So neither point is realizable over U(H). Both are counterexamples to Question 6.1 with d3 = 10 < 21.

[D] Within d3 <= 12, these are the only two rays whose primitive point is excluded over S by the obstruction set of Section 3.3 AND fails parity. The ten other S-obstructed rays all pass parity, so their Question 6.1 status depends on U(H) (Section 5, item C). Whether a counterexample with d3 <= 9 exists is therefore reducible to: is the primitive point of each of (0,1,3,4) [yes: Erman-Sam], (0,1,5,6), (0,1,7,8), (0,2,6,8), (0,3,5,8) realizable over U(H), and is any parity-failing ray with d3 <= 9 obstructed over S by an obstruction not in the list? The second part is where computation is needed.

[D] With d3 <= 60 the Rethlas pair (beta_0 = 1, beta_1 = 2, parity failure) occurs for exactly one sequence, (0,6,20,21). So the Rethlas example is minimal for its own argument shape but not for the question.

### 4.4 Computational plan for an exact table (d3 <= 12), with cost estimates

Stage 0 (done here, minutes): primitive points, all formula-based upper bounds (ES; add pureTwoInvariant and pureWeyman via M2 in characteristic 0), all formula-based lower bounds (Section 3.3), scaling and duality closure. Output: 52+ realized, 12 obstructed, about 150 undecided primitive points.

Stage 1 (random search, hours of M2 time): for every undecided ray and m = 1, 2, ..., up to the ES bound or a cap, run randomSocleModule(L, m) and randomModule(L, m) over a large prime field (and over GF(2), GF(3) for characteristic dependence), a few hundred trials each, keep any pure hit. Expected: many small primitive points fall (the M2 docs already show (0,2,3,7) and (0,2,3,9)); every hit also settles all multiples in the numerical semigroup it generates with other hits. Cost: each trial is a resolution of a finite length module with up to a few hundred generators; on the sum-of-Betti <= 60 rays (57 undecided) this is seconds per trial.

Stage 2 (structured search for cyclic and low-generator points): beta_0 = 1 undecided points (e.g. (0,3,4,6) (1,8,9,2), (0,3,5,6) (1,5,9,5), (0,4,6,7) (1,7,14,8)) are ideals with beta_1 generators of one degree and a prescribed h-vector; enumerate via Macaulay inverse systems with socle concentrated in degree d3 - 3 (pure of type (0,d1,d2,d3) means generated in degree 0, relations in degree d1, socle in a single degree), and via monomial and toric candidates (fast, but pure monomial ideals of finite length are rare; a classification of Stanley-Reisner rings with pure resolutions exists in the literature [U, title seen in search]). For Gorenstein-shaped points (1,n,n,1): n odd all realized, n even all obstructed, so cyclic Gorenstein is closed.

Stage 3 (obstructions for survivors): implement Erman's maximal-minor obstruction (Proposition 4.1) for pure diagrams, Buchsbaum-Eisenbud-Horrocks-type rank bounds, and an exhaustive search of linear presentation matrices for beta_0 <= 3 using the Eisenbud-Harris classification of spaces of matrices of low rank (this is exactly how Erman proves Theorem 1.6(4)). For rays with d1 = 1 and small beta_0 this is finite and small. For d1 >= 2 there is no finiteness, and residual points will stay open; those are the honest "unknown" entries of the table.

Stage 4 (U(H)): implement U(H) as a graded noncommutative algebra (Macaulay2 AssociativeAlgebras / NCAlgebra, or Singular Plural / letterplace, for the Heisenberg algebra with the given grading) and compute minimal graded resolutions of quotients by left ideals, for the 29 parity-passing rays, targeting the ten S-obstructed ones first. The Chevalley-Eilenberg computation of Erman-Sam for (0,1,3,4) is the template; candidates for (0,2,6,8) are quotients like U(H)/U(H)(x^2, y^2) or (x^2, xy + c z), and for (0,1,5,6) with (2,3,3,2) two-generator modules with three linear relations. Expected size: tiny (Hilbert functions of length at most a few dozen). Whether Ext-duality over U(H) reverses Betti tables should be checked first (U(H) is Auslander-regular of dimension 3 and graded, so this is likely a known fact [U]).

Total: a focused two-to-four-week project with Macaulay2 and one noncommutative system, producing a table of 220 rows with, per row, the realizability status of the primitive point over S and U(H), the minimal realized multiple found, the best lower bound, and the characteristic dependence where observed.

---

## 5. Candidate extension questions with attributable novelty

A. Complete realizability table for three variables, d3 <= 12 (220 rays): for each ray the status of the primitive point over S (realized with an explicit module / obstructed with a named obstruction / open), the minimal realizable multiple c_d found and a lower bound, and the U(H) status on the 29 parity-passing rays. Novelty: no such table exists in print (Erman 2009 Section 7(2) asks for it; EFW list three examples; M2 docs give two). Deliverable: table plus a Macaulay2 script and the explicit modules. Risk: some rows will remain "open"; the honest record is still a result.

B. Smallest counterexample to Question 6.1. Proposition (already provable from this dossier, [D]): the primitive points of (0,1,6,10) and (0,4,9,10) are realizable over neither S nor U(H); d3 = 10 versus Rethlas' 21. Extension: determine whether any counterexample has d3 <= 9. This needs (i) U(H)-realizability of the primitive points of (0,1,5,6), (0,1,7,8), (0,2,6,8), (0,3,5,8) (the S-obstructed, parity-passing rays with d3 <= 9; (0,1,3,4) is done by Erman-Sam), (ii) S-realizability or a new obstruction for the parity-failing undecided rays with d3 <= 9. A clean theorem would be "the smallest d3 admitting a counterexample is 10" or a smaller explicit one.

C. Realization theorems over U(H). The ten S-obstructed parity-passing rays with d3 <= 12 are exactly the (1,2,2,1) family (0,a,3a,4a), the (a,a+1,a+1,a) family (0,1,2a+1,2a+2) and its scaled copy, and the two even-Gorenstein points (0,3,5,8) (1,4,4,1), (0,5,7,12) (1,6,6,1). Question: which of these are realizable over U(H)? Erman-Sam realized (0,1,3,4) and announced more via sp_4 (never published as far as searches show). A theorem of the form "the primitive point of (0,1,2a+1,2a+2) is realizable over U(H) for all a" or "the even Gorenstein points are not realizable over U(H)" would be new. Note that the two obstructions used over S (Krull; Buchsbaum-Eisenbud) both fail over U(H) in principle because U(H)/(x,y) = k is finite length with two relations; so any U(H) obstruction beyond the Hilbert series would be new.

D. A new scale-sensitive obstruction on pure rays over S. All published pure-ray obstructions are the Buchsbaum-Rim ones (Erman 3.1), the Buchsbaum-Eisenbud parity and the regular sequence argument (elementary, Section 3.3), and Erman's maximal-minor obstruction (Section 4, only used on non-pure examples). Any obstruction excluding a point m beta with m beta_0 >= 2 and m (beta_1 - beta_0) >= 2 on a pure ray in three variables would be new; natural candidates come from Erman's Proposition 4.1 (rank of the linear strand) applied to pure rays with d1 = 1 and d2 = 2 or 3, where the presentation matrix is a space of linear forms and the Eisenbud-Harris classification is available.

E. The minimal multiple c_d as a function: on the (1,2,2,1) family c_d = 2 (Erman: 2 D1 is Buchsbaum-Rim; D1 obstructed) and all m >= 2 are realized [V]. On the Rethlas ray 3 <= c_d <= 27132 [D]; determining c_d for (0,6,20,21) is a concrete, citable sub-result ("the ray the AI found: how much of it is really missing?"). Similarly for (0,1,6,10) with c_d >= 2 and ES multiple 70.

F. Scaling and duality structure. Prove or refute: realizability at (e d, beta) implies realizability at (d, beta) (converse of the scaling lemma), and Betti-table duality over U(H). Both are structural lemmas that would halve any table.

G. Characteristic dependence in three variables. Kunte's example lives in five variables; no characteristic-dependent pure point is known in three variables [U]. Stage 1 above over GF(2), GF(3), GF(32003) would either find one (new) or support a conjecture.

Attribution note: item B (the d3 = 10 pair) and the twelve-row obstruction list are established by the computations in this dossier plus published propositions; they should be re-verified independently in Macaulay2 (resolve random modules on the two rays as a sanity check, although the proof does not need it) before being claimed.

---

## 6. Open, unverified, or ambiguous items to resolve before any write-up

1. [U] Whether Sam's announced U(H)/sp_4 realizations were ever published (no trace found).
2. [U] The EFW Example 6.3 number "380" versus the ES formula (15400 total, 3080 as a multiple of the primitive 5); recompute with pureCharFree.
3. [U] Exact names of the TensorComplexes package functions other than pureResTC.
4. [U] Whether duality reverses Betti tables over U(H).
5. [U] Whether any three-variable pure point is characteristic dependent.
6. [U] DOIs: only the EFW numdam DOI (10.5802/aif.2632) was seen in a source; all other references below are given by journal citation as printed in the primary sources' bibliographies.
7. [D, to verify by machine] The twelve obstructed rows and the "52 realized" count (the classical constructions were matched by shape; the Pfaffian genericity claim is standard but was not recomputed in M2 here).

---

## 7. References (as printed in the primary sources' bibliographies; [V] unless marked)

- [JLSWXY26] J. Jiang, Y. Li, Z. Sun, Y. Wang, L. Xiao, J. Yu, On some open problems in commutative algebra resolved by Rethlas, arXiv:2605.25259v2 (28 May 2026). Raw outputs: github.com/frenzymath/Rethlas_results, CommAlg/arxiv_1606_01867/question_6_1.md, question_6_2.md.
- [Ju26] H. Ju et al., Automated Conjecture Resolution with Formal Verification, arXiv:2604.03789 (2026).
- [ES16] D. Erman, S. V. Sam, Questions about Boij-Soderberg theory, in: Surveys on Recent Developments in Algebraic Geometry, Proc. Sympos. Pure Math. 95, AMS, 2017, pp. 285-304. arXiv:1606.01867 (6 June 2016).
- [BS08] M. Boij, J. Soderberg, Graded Betti numbers of Cohen-Macaulay modules and the multiplicity conjecture, J. Lond. Math. Soc. (2) 78 (2008), no. 1, 85-106. arXiv:math/0611081.
- [BS12] M. Boij, J. Soderberg, Betti numbers of graded modules and the multiplicity conjecture in the non-Cohen-Macaulay case, Algebra Number Theory 6 (2012), no. 3, 437-454. arXiv:0803.1645.
- [ES09] D. Eisenbud, F.-O. Schreyer, Betti numbers of graded modules and cohomology of vector bundles, J. Amer. Math. Soc. 22 (2009), no. 3, 859-888. arXiv:0712.1843.
- [EFW11] D. Eisenbud, G. Floystad, J. Weyman, The existence of equivariant pure free resolutions, Ann. Inst. Fourier 61 (2011), no. 3, 905-926. arXiv:0709.1529. DOI 10.5802/aif.2632.
- [Erman09] D. Erman, The semigroup of Betti diagrams, Algebra Number Theory 3 (2009), 341-365. arXiv:0806.4401.
- [BEKS13] C. Berkesch Zamaere, D. Erman, M. Kummini, S. V. Sam, Tensor complexes: multilinear free resolutions constructed from higher tensors, J. Eur. Math. Soc. 15 (2013), no. 6, 2257-2295. arXiv:1101.4604.
- [EES13] D. Eisenbud, D. Erman, F.-O. Schreyer, Filtering free resolutions, Compos. Math. 149 (2013), no. 5, 754-772. arXiv:1001.0585.
- [HK84] J. Herzog, M. Kuhl, On the Betti numbers of finite pure and linear resolutions, Comm. Algebra 12 (1984), no. 13-14, 1627-1646.
- [BE77] D. Buchsbaum, D. Eisenbud, Algebra structures for finite free resolutions, and some structure theorems for ideals of codimension 3, Amer. J. Math. 99 (1977), no. 3, 447-485.
- [BE74] D. Buchsbaum, D. Eisenbud, Some structure theorems for finite free resolutions, Adv. Math. 12 (1974), 84-139.
- [Sod06] J. Soderberg, Artinian level modules of embedding dimension two, J. Pure Appl. Algebra 207 (2006), 417-432.
- [Sam15] S. V. Sam, Homology of analogues of Heisenberg Lie algebras, Math. Res. Lett. 22 (2015). arXiv:1307.1901.
- [Kunte] M. Kunte, Gorenstein modules of finite length, thesis 2008; Math. Nachr. (2011) [U for the journal details].
- [Floystad12] G. Floystad, Boij-Soderberg theory: introduction and survey, in Progress in Commutative Algebra 1, de Gruyter, 2012, pp. 1-54. arXiv:1106.0381.
- [AJK26] H. Ananthnarayan, O. Javadekar, R. Kumar, Purity of extremal rays of Betti cones, arXiv:2607.06394 (July 2026) (not about integral points).
- Macaulay2 documentation: BoijSoederberg package (pureBetti, pureBettiDiagram, pureCharFree, pureTwoInvariant, pureWeyman, pureAll, randomSocleModule, randomModule), TensorComplexes package (pureResTC), BGG package (pureResolution). macaulay2.com/doc.

---

## Appendix A. Census table, degree sequences (0,d1,d2,d3), d3 <= 12

Columns: d; primitive Herzog-Kuhl point; status of the PRIMITIVE point over S = k[x,y,z] as decided by the formulas and published obstructions of Sections 3.2-3.3 (realized / obstructed / UNDECIDED); reason; Eisenbud-Schreyer multiple (beta_0 of the ES module divided by the primitive beta_0; the ES module realizes exactly this multiple of the primitive point); whether the ray passes the U(H) parity test p(-1) = 0 (if "no", no point of the ray is realizable over U(H)); whether the primitive U(H) Hilbert function is nonnegative (only meaningful when parity passes). "realized(scaled from d')" means the scaling lemma from a realized sequence d'. Realizations known only from the Macaulay2 documentation examples ((0,2,3,7) and (0,2,3,9) primitive points hit by randomSocleModule) are NOT folded into this mechanical table. Generated by .\src\appendix.py. All entries [D].

| d | primitive beta | status of primitive point over S | reason / source | ES multiple | U(H) parity p(-1)=0 | U(H) Hilbert fn nonneg |
|---|---|---|---|---|---|---|
| (0,1,2,3) | (1,3,3,1) | realized | ES beta0 = primitive Pfaffian | 1 | no | n/a |
| (0,1,2,4) | (3,8,6,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,5) | (6,15,10,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,6) | (10,24,15,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,7) | (15,35,21,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,8) | (21,48,28,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,9) | (28,63,36,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,10) | (36,80,45,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,11) | (45,99,55,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,2,12) | (55,120,66,1) | realized | ES beta0 = primitive dual(S/m^a) | 1 | no | n/a |
| (0,1,3,4) | (1,2,2,1) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 2 | yes | yes |
| (0,1,3,5) | (8,15,10,3) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,3,6) | (5,9,5,1) | UNDECIDED |  | 4 | no | n/a |
| (0,1,3,7) | (8,14,7,1) | UNDECIDED |  | 5 | no | n/a |
| (0,1,3,8) | (35,60,28,3) | UNDECIDED |  | 2 | no | n/a |
| (0,1,3,9) | (16,27,12,1) | UNDECIDED |  | 7 | no | n/a |
| (0,1,3,10) | (21,35,15,1) | UNDECIDED |  | 8 | no | n/a |
| (0,1,3,11) | (80,132,55,3) | UNDECIDED |  | 3 | no | n/a |
| (0,1,3,12) | (33,54,22,1) | UNDECIDED |  | 10 | no | n/a |
| (0,1,4,5) | (3,5,5,3) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,4,6) | (5,8,5,2) | UNDECIDED |  | 3 | no | n/a |
| (0,1,4,7) | (9,14,7,2) | UNDECIDED |  | 5 | no | n/a |
| (0,1,4,8) | (21,32,14,3) | UNDECIDED |  | 5 | no | n/a |
| (0,1,4,9) | (10,15,6,1) | UNDECIDED |  | 21 | no | n/a |
| (0,1,4,10) | (27,40,15,2) | UNDECIDED |  | 14 | no | n/a |
| (0,1,4,11) | (105,154,55,6) | UNDECIDED |  | 6 | no | n/a |
| (0,1,4,12) | (22,32,11,1) | UNDECIDED |  | 45 | no | n/a |
| (0,1,5,6) | (2,3,3,2) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 2 | yes | yes |
| (0,1,5,7) | (24,35,21,10) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,5,8) | (21,30,14,5) | UNDECIDED |  | 4 | no | n/a |
| (0,1,5,9) | (32,45,18,5) | UNDECIDED |  | 7 | no | n/a |
| (0,1,5,10) | (18,25,9,2) | UNDECIDED |  | 28 | no | n/a |
| (0,1,5,11) | (24,33,11,2) | UNDECIDED |  | 42 | no | n/a |
| (0,1,5,12) | (77,105,33,5) | UNDECIDED |  | 24 | no | n/a |
| (0,1,6,7) | (5,7,7,5) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,6,8) | (35,48,28,15) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,6,9) | (20,27,12,5) | UNDECIDED |  | 7 | no | n/a |
| (0,1,6,10) | (6,8,3,1) | obstructed | reg>=2 | 70 | no | n/a |
| (0,1,6,11) | (25,33,11,3) | UNDECIDED |  | 42 | no | n/a |
| (0,1,6,12) | (55,72,22,5) | UNDECIDED |  | 42 | no | n/a |
| (0,1,7,8) | (3,4,4,3) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 2 | yes | yes |
| (0,1,7,9) | (16,21,12,7) | UNDECIDED |  | 3 | no | n/a |
| (0,1,7,10) | (27,35,15,7) | UNDECIDED |  | 8 | no | n/a |
| (0,1,7,11) | (120,154,55,21) | UNDECIDED |  | 6 | no | n/a |
| (0,1,7,12) | (55,70,22,7) | UNDECIDED |  | 36 | no | n/a |
| (0,1,8,9) | (7,9,9,7) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,8,10) | (63,80,45,28) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,8,11) | (105,132,55,28) | UNDECIDED |  | 3 | no | n/a |
| (0,1,8,12) | (77,96,33,14) | UNDECIDED |  | 15 | no | n/a |
| (0,1,9,10) | (4,5,5,4) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 2 | yes | yes |
| (0,1,9,11) | (80,99,55,36) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,9,12) | (22,27,11,6) | UNDECIDED |  | 20 | no | n/a |
| (0,1,10,11) | (9,11,11,9) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,1,10,12) | (33,40,22,15) | UNDECIDED |  | 3 | no | n/a |
| (0,1,11,12) | (5,6,6,5) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 2 | yes | yes |
| (0,2,3,4) | (1,6,8,3) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,2,3,5) | (1,5,5,1) | realized | Pfaffian | 4 | no | n/a |
| (0,2,3,6) | (2,9,8,1) | UNDECIDED |  | 5 | no | n/a |
| (0,2,3,7) | (10,42,35,3) | UNDECIDED |  | 2 | no | n/a |
| (0,2,3,8) | (5,20,16,1) | UNDECIDED |  | 7 | no | n/a |
| (0,2,3,9) | (7,27,21,1) | UNDECIDED |  | 8 | no | n/a |
| (0,2,3,10) | (28,105,80,3) | UNDECIDED |  | 3 | no | n/a |
| (0,2,3,11) | (12,44,33,1) | UNDECIDED |  | 10 | no | n/a |
| (0,2,3,12) | (15,54,40,1) | UNDECIDED |  | 11 | no | n/a |
| (0,2,4,5) | (3,10,15,8) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,2,4,6) | (1,3,3,1) | realized | Pfaffian | 15 | yes | yes |
| (0,2,4,7) | (15,42,35,8) | UNDECIDED |  | 3 | no | n/a |
| (0,2,4,8) | (3,8,6,1) | realized | realized(scaled from (0, 1, 2, 4)) | 35 | yes | yes |
| (0,2,4,9) | (35,90,63,8) | UNDECIDED |  | 6 | no | n/a |
| (0,2,4,10) | (6,15,10,1) | realized | realized(scaled from (0, 1, 2, 5)) | 63 | yes | yes |
| (0,2,4,11) | (63,154,99,8) | UNDECIDED |  | 10 | no | n/a |
| (0,2,4,12) | (10,24,15,1) | realized | realized(scaled from (0, 1, 2, 6)) | 99 | yes | yes |
| (0,2,5,6) | (2,5,8,5) | UNDECIDED |  | 3 | no | n/a |
| (0,2,5,7) | (3,7,7,3) | UNDECIDED |  | 12 | no | n/a |
| (0,2,5,8) | (9,20,16,5) | UNDECIDED |  | 14 | no | n/a |
| (0,2,5,9) | (14,30,21,5) | UNDECIDED |  | 24 | no | n/a |
| (0,2,5,10) | (12,25,16,3) | UNDECIDED |  | 63 | no | n/a |
| (0,2,5,11) | (27,55,33,5) | UNDECIDED |  | 56 | no | n/a |
| (0,2,5,12) | (7,14,8,1) | UNDECIDED |  | 396 | no | n/a |
| (0,2,6,7) | (10,21,35,24) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,2,6,8) | (1,2,2,1) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 70 | yes | yes |
| (0,2,6,9) | (14,27,21,8) | UNDECIDED |  | 20 | no | n/a |
| (0,2,6,10) | (8,15,10,3) | realized | realized(scaled from (0, 1, 3, 5)) | 105 | yes | yes |
| (0,2,6,11) | (30,55,33,8) | UNDECIDED |  | 70 | no | n/a |
| (0,2,6,12) | (5,9,5,1) | UNDECIDED |  | 924 | yes | yes |
| (0,2,7,8) | (15,28,48,35) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,2,7,9) | (5,9,9,5) | UNDECIDED |  | 24 | no | n/a |
| (0,2,7,10) | (12,21,16,7) | UNDECIDED |  | 45 | no | n/a |
| (0,2,7,11) | (90,154,99,35) | UNDECIDED |  | 20 | no | n/a |
| (0,2,7,12) | (25,42,24,7) | UNDECIDED |  | 198 | no | n/a |
| (0,2,8,9) | (7,12,21,16) | UNDECIDED |  | 3 | no | n/a |
| (0,2,8,10) | (3,5,5,3) | realized | realized(scaled from (0, 1, 4, 5)) | 63 | yes | yes |
| (0,2,8,11) | (27,44,33,16) | UNDECIDED |  | 35 | no | n/a |
| (0,2,8,12) | (5,8,5,2) | UNDECIDED |  | 693 | yes | yes |
| (0,2,9,10) | (28,45,80,63) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,2,9,11) | (7,11,11,7) | UNDECIDED |  | 40 | no | n/a |
| (0,2,9,12) | (35,54,40,21) | UNDECIDED |  | 44 | no | n/a |
| (0,2,10,11) | (36,55,99,80) | realized | ES beta0 = primitive | 1 | no | n/a |
| (0,2,10,12) | (2,3,3,2) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 198 | yes | yes |
| (0,2,11,12) | (15,22,40,33) | UNDECIDED |  | 3 | no | n/a |
| (0,3,4,5) | (1,10,15,6) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,3,4,6) | (1,8,9,2) | UNDECIDED |  | 5 | no | n/a |
| (0,3,4,7) | (1,7,7,1) | realized | Pfaffian | 15 | no | n/a |
| (0,3,4,8) | (5,32,30,3) | UNDECIDED |  | 7 | no | n/a |
| (0,3,4,9) | (5,30,27,2) | UNDECIDED |  | 14 | no | n/a |
| (0,3,4,10) | (7,40,35,2) | UNDECIDED |  | 18 | no | n/a |
| (0,3,4,11) | (14,77,66,3) | UNDECIDED |  | 15 | no | n/a |
| (0,3,4,12) | (6,32,27,1) | UNDECIDED |  | 55 | no | n/a |
| (0,3,5,6) | (1,5,9,5) | UNDECIDED |  | 4 | no | n/a |
| (0,3,5,7) | (8,35,42,15) | UNDECIDED |  | 3 | no | n/a |
| (0,3,5,8) | (1,4,4,1) | obstructed | BE-parity(m=1 excluded) | 84 | yes | yes |
| (0,3,5,9) | (8,30,27,5) | UNDECIDED |  | 28 | no | n/a |
| (0,3,5,10) | (7,25,21,3) | UNDECIDED |  | 72 | no | n/a |
| (0,3,5,11) | (16,55,44,5) | UNDECIDED |  | 63 | no | n/a |
| (0,3,5,12) | (21,70,54,5) | UNDECIDED |  | 88 | no | n/a |
| (0,3,6,7) | (2,7,14,9) | UNDECIDED |  | 5 | no | n/a |
| (0,3,6,8) | (5,16,20,9) | UNDECIDED |  | 14 | no | n/a |
| (0,3,6,9) | (1,3,3,1) | realized | Pfaffian | 280 | no | n/a |
| (0,3,6,10) | (14,40,35,9) | UNDECIDED |  | 60 | no | n/a |
| (0,3,6,11) | (20,55,44,9) | UNDECIDED |  | 105 | no | n/a |
| (0,3,6,12) | (3,8,6,1) | realized | realized(scaled from (0, 1, 2, 4)) | 1540 | no | n/a |
| (0,3,7,8) | (5,14,30,21) | UNDECIDED |  | 4 | no | n/a |
| (0,3,7,9) | (8,21,27,14) | UNDECIDED |  | 20 | no | n/a |
| (0,3,7,10) | (2,5,5,2) | UNDECIDED |  | 360 | yes | yes |
| (0,3,7,11) | (32,77,66,21) | UNDECIDED |  | 75 | no | n/a |
| (0,3,7,12) | (15,35,27,7) | UNDECIDED |  | 440 | no | n/a |
| (0,3,8,9) | (5,12,27,20) | UNDECIDED |  | 7 | no | n/a |
| (0,3,8,10) | (7,16,21,12) | UNDECIDED |  | 45 | no | n/a |
| (0,3,8,11) | (5,11,11,5) | UNDECIDED |  | 315 | no | n/a |
| (0,3,8,12) | (15,32,27,10) | UNDECIDED |  | 385 | no | n/a |
| (0,3,9,10) | (7,15,35,27) | UNDECIDED |  | 8 | no | n/a |
| (0,3,9,11) | (16,33,44,27) | UNDECIDED |  | 35 | no | n/a |
| (0,3,9,12) | (1,2,2,1) | obstructed | codim>=2,2ndsyz>=2,reg>=2 | 3080 | yes | yes |
| (0,3,10,11) | (28,55,132,105) | UNDECIDED |  | 3 | no | n/a |
| (0,3,10,12) | (21,40,54,35) | UNDECIDED |  | 44 | no | n/a |
| (0,3,11,12) | (6,11,27,22) | UNDECIDED |  | 20 | no | n/a |
| (0,4,5,6) | (1,15,24,10) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,4,5,7) | (3,35,42,10) | UNDECIDED |  | 2 | no | n/a |
| (0,4,5,8) | (3,30,32,5) | UNDECIDED |  | 7 | no | n/a |
| (0,4,5,9) | (1,9,9,1) | realized | Pfaffian | 56 | no | n/a |
| (0,4,5,10) | (3,25,24,2) | UNDECIDED |  | 42 | no | n/a |
| (0,4,5,11) | (21,165,154,10) | UNDECIDED |  | 12 | no | n/a |
| (0,4,5,12) | (14,105,96,5) | UNDECIDED |  | 33 | no | n/a |
| (0,4,6,7) | (1,7,14,8) | UNDECIDED |  | 5 | no | n/a |
| (0,4,6,8) | (1,6,8,3) | realized | realized(scaled from (0, 2, 3, 4)) | 35 | yes | yes |
| (0,4,6,9) | (5,27,30,8) | UNDECIDED |  | 28 | no | n/a |
| (0,4,6,10) | (1,5,5,1) | realized | Pfaffian | 420 | yes | yes |
| (0,4,6,11) | (35,165,154,24) | UNDECIDED |  | 30 | no | n/a |
| (0,4,6,12) | (2,9,8,1) | UNDECIDED |  | 1155 | yes | yes |
| (0,4,7,8) | (3,14,32,21) | UNDECIDED |  | 5 | no | n/a |
| (0,4,7,9) | (5,21,30,14) | UNDECIDED |  | 24 | no | n/a |
| (0,4,7,10) | (9,35,40,14) | UNDECIDED |  | 60 | no | n/a |
| (0,4,7,11) | (3,11,11,3) | UNDECIDED |  | 600 | no | n/a |
| (0,4,7,12) | (10,35,32,7) | UNDECIDED |  | 495 | no | n/a |
| (0,4,8,9) | (5,18,45,32) | UNDECIDED |  | 7 | no | n/a |
| (0,4,8,10) | (3,10,15,8) | realized | realized(scaled from (0, 2, 4, 5)) | 105 | yes | yes |
| (0,4,8,11) | (21,66,77,32) | UNDECIDED |  | 75 | no | n/a |
| (0,4,8,12) | (1,3,3,1) | realized | Pfaffian | 5775 | yes | yes |
| (0,4,9,10) | (1,3,8,6) | obstructed | 2ndsyz>=2 | 70 | no | n/a |
| (0,4,9,11) | (35,99,154,90) | UNDECIDED |  | 20 | no | n/a |
| (0,4,9,12) | (10,27,32,15) | UNDECIDED |  | 385 | no | n/a |
| (0,4,10,11) | (21,55,154,120) | UNDECIDED |  | 6 | no | n/a |
| (0,4,10,12) | (2,5,8,5) | UNDECIDED |  | 693 | yes | yes |
| (0,4,11,12) | (14,33,96,77) | UNDECIDED |  | 15 | no | n/a |
| (0,5,6,7) | (1,21,35,15) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,5,6,8) | (1,16,20,5) | UNDECIDED |  | 7 | no | n/a |
| (0,5,6,9) | (2,27,30,5) | UNDECIDED |  | 14 | no | n/a |
| (0,5,6,10) | (2,24,25,3) | UNDECIDED |  | 42 | no | n/a |
| (0,5,6,11) | (1,11,11,1) | realized | Pfaffian | 210 | no | n/a |
| (0,5,6,12) | (7,72,70,5) | UNDECIDED |  | 66 | no | n/a |
| (0,5,7,8) | (3,28,60,35) | UNDECIDED |  | 2 | no | n/a |
| (0,5,7,9) | (8,63,90,35) | UNDECIDED |  | 6 | no | n/a |
| (0,5,7,10) | (3,21,25,7) | UNDECIDED |  | 72 | no | n/a |
| (0,5,7,11) | (24,154,165,35) | UNDECIDED |  | 30 | no | n/a |
| (0,5,7,12) | (1,6,6,1) | obstructed | BE-parity(m=1 excluded) | 1980 | yes | yes |
| (0,5,8,9) | (1,6,15,10) | UNDECIDED |  | 21 | no | n/a |
| (0,5,8,10) | (3,16,25,12) | UNDECIDED |  | 63 | no | n/a |
| (0,5,8,11) | (9,44,55,20) | UNDECIDED |  | 105 | no | n/a |
| (0,5,8,12) | (7,32,35,10) | UNDECIDED |  | 495 | no | n/a |
| (0,5,9,10) | (2,9,25,18) | UNDECIDED |  | 28 | no | n/a |
| (0,5,9,11) | (8,33,55,30) | UNDECIDED |  | 70 | no | n/a |
| (0,5,9,12) | (7,27,35,15) | UNDECIDED |  | 440 | no | n/a |
| (0,5,10,11) | (3,11,33,25) | UNDECIDED |  | 42 | no | n/a |
| (0,5,10,12) | (7,24,42,25) | UNDECIDED |  | 198 | no | n/a |
| (0,5,11,12) | (7,22,70,55) | UNDECIDED |  | 36 | no | n/a |
| (0,6,7,8) | (1,28,48,21) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,6,7,9) | (1,21,27,7) | UNDECIDED |  | 8 | no | n/a |
| (0,6,7,10) | (2,35,40,7) | UNDECIDED |  | 18 | no | n/a |
| (0,6,7,11) | (10,154,165,21) | UNDECIDED |  | 12 | no | n/a |
| (0,6,7,12) | (5,70,72,7) | UNDECIDED |  | 66 | no | n/a |
| (0,6,8,9) | (1,12,27,16) | UNDECIDED |  | 7 | no | n/a |
| (0,6,8,10) | (1,10,15,6) | realized | realized(scaled from (0, 3, 4, 5)) | 63 | yes | yes |
| (0,6,8,11) | (5,44,55,16) | UNDECIDED |  | 63 | no | n/a |
| (0,6,8,12) | (1,8,9,2) | UNDECIDED |  | 1155 | yes | yes |
| (0,6,9,10) | (2,15,40,27) | UNDECIDED |  | 14 | no | n/a |
| (0,6,9,11) | (5,33,55,27) | UNDECIDED |  | 56 | no | n/a |
| (0,6,9,12) | (1,6,8,3) | realized | realized(scaled from (0, 2, 3, 4)) | 1540 | no | n/a |
| (0,6,10,11) | (2,11,33,24) | UNDECIDED |  | 42 | no | n/a |
| (0,6,10,12) | (1,5,9,5) | UNDECIDED |  | 924 | yes | yes |
| (0,6,11,12) | (5,22,72,55) | UNDECIDED |  | 42 | no | n/a |
| (0,7,8,9) | (1,36,63,28) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,7,8,10) | (3,80,105,28) | UNDECIDED |  | 3 | no | n/a |
| (0,7,8,11) | (3,66,77,14) | UNDECIDED |  | 15 | no | n/a |
| (0,7,8,12) | (5,96,105,14) | UNDECIDED |  | 33 | no | n/a |
| (0,7,9,10) | (1,15,35,21) | UNDECIDED |  | 8 | no | n/a |
| (0,7,9,11) | (8,99,154,63) | UNDECIDED |  | 10 | no | n/a |
| (0,7,9,12) | (5,54,70,21) | UNDECIDED |  | 88 | no | n/a |
| (0,7,10,11) | (6,55,154,105) | UNDECIDED |  | 6 | no | n/a |
| (0,7,10,12) | (1,8,14,7) | UNDECIDED |  | 396 | no | n/a |
| (0,7,11,12) | (5,33,105,77) | UNDECIDED |  | 24 | no | n/a |
| (0,8,9,10) | (1,45,80,36) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,8,9,11) | (1,33,44,12) | UNDECIDED |  | 10 | no | n/a |
| (0,8,9,12) | (1,27,32,6) | UNDECIDED |  | 55 | no | n/a |
| (0,8,10,11) | (3,55,132,80) | UNDECIDED |  | 3 | no | n/a |
| (0,8,10,12) | (1,15,24,10) | realized | realized(scaled from (0, 4, 5, 6)) | 99 | yes | yes |
| (0,8,11,12) | (1,11,32,22) | UNDECIDED |  | 45 | no | n/a |
| (0,9,10,11) | (1,55,99,45) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
| (0,9,10,12) | (1,40,54,15) | UNDECIDED |  | 11 | no | n/a |
| (0,9,11,12) | (1,22,54,33) | UNDECIDED |  | 10 | no | n/a |
| (0,10,11,12) | (1,66,120,55) | realized | ES beta0 = primitive S/m^a | 1 | no | n/a |
