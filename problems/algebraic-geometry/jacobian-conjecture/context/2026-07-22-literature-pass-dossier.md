# Literature pass dossier: primary-source verification for the JC(2) program

Date: 2026-07-22
Scope: five tasks requested by the research program (Moh 1983; Abhyankar similarity; the 108 floor;
novelty pass for Theorems 1-4 plus 2D equivariant rigidity; minimal-counterexample polygon constraints).
Method: web search plus direct reading of arXiv PDFs (GGV 1401.1784 v3 read page by page from the PDF;
GGHV 2204.14178 read from the PDF; GGHV 1708.07936 sections 5-6 read from the PDF; Druzkowski's Banach
Center survey read from the PDF; Moskowicz arXiv:1610.01621 read from the PDF). Everything not read
verbatim from a primary source is marked UNVERIFIED. No citation below is invented; each carries its
source URL or DOI.

Notation used below: a "Jacobian pair" (P,Q) means P,Q in K[x,y], char K = 0, with
[P,Q] := P_x Q_y - P_y Q_x in K^* (a nonzero constant); "counterexample" means a Jacobian pair that is
not an automorphism pair. B := min gcd(v_{1,1}(P), v_{1,1}(Q)) over counterexamples
(= min gcd(deg P, deg Q) in the standard normalization).

---

## Task 1. Moh 1983: exact statement and the surviving configurations

### 1.1 Bibliographic record (verified)

T. T. Moh, "On the Jacobian conjecture and the configurations of roots",
J. Reine Angew. Math. (Crelle) 340 (1983), 140-212.
- DOI: 10.1515/crll.1983.340.140 (De Gruyter landing page:
  https://www.degruyterbrill.com/document/doi/10.1515/crll.1983.340.140/html)
- EUDML record: https://eudml.org/doc/152524 (keywords: Jacobian conjecture; configurations of roots;
  Puiseux series). EUDML links Zbl 0525.13011 and full text at GDZ
  (http://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002200376).
- MR691964 (84m:14018), as cited in the reference lists of GGV, J. Algebra 471 (2017) 13-74
  (arXiv:1401.1784) and GGHV arXiv:1708.07936.
- The GDZ scan resolver works but the article text could not be machine-extracted in this pass;
  page-level quotes from Moh's own text below are therefore only those relayed by secondary sources.

### 1.2 What Moh verified (verified through three independent secondary sources)

- GGHV, arXiv:2204.14178, p. 1 (read from PDF): "In [10] the author discards all possible
  counterexamples with max{deg(P), deg(Q)} <= 100 using approximate roots of polynomials in two
  variables, but provides a detailed proof only for the smallest case." ([10] = Moh 1983.)
- Druzkowski, "The Jacobian Conjecture: survey of some results", Banach Center Publ. 31 (1995),
  163-171 (read from PDF, https://matwbn.icm.edu.pl/ksiazki/bcp/bcp31/bcp31116.pdf), p. 169:
  "Recall that the two dimensional complex Jacobian Conjecture is true if max{deg f, deg g} < 100,
  cf. [Mo]." (Note the strict "< 100" here versus "<= 100" in GGHV; the two statements agree because
  the surviving degree structures near 100 have max in {64, 75, 84, 96, 99}, see 1.3.)
- Moskowicz, "Ideas about the Jacobian Conjecture", arXiv:1610.01621 (read from PDF), p. 4, points to
  "Moh's theorem [16, Theorem 10.2.30]" where [16] = van den Essen's book (Progress in Mathematics 190,
  Birkhauser, 2000), i.e. the book records Moh's degree-100 theorem as Theorem 10.2.30.
  (Exact wording of Theorem 10.2.30 in the book: UNVERIFIED, book not accessible in this pass.)

### 1.3 The surviving configurations ("shapes") of Moh's analysis (verified)

Two levels of precision are available from GGHV's papers, which are the modern audit of Moh:

(a) The degree cases Moh treated with less than full detail. GGHV arXiv:2204.14178, p. 2 (read from
PDF): "In [10] the cases with max{deg(P), deg(Q)} in {64, 75, 84, 99} have been considered, but only
in the case 64 a complete proof is given. This case was also computed by Heitman in [7]."
([7] = R. Heitmann, "On the Jacobian conjecture", J. Pure Appl. Algebra 64 (1990), 35-72; GGHV spell
the name "Heitman" there.) Their Table on p. 3 marks "no detail in [10]" for the cases
(A0, (m,n), max) = ((5,20), (2,3), 75), ((5,20), (3,2), 75), ((7,21), (2,3), 84), ((9,24), (2,3), 99).

(b) The "six cases" statement (this is the verified form of the program's "six shapes" claim).
GGHV, "Some algorithms related to the Jacobian Conjecture", arXiv:1708.07936, Section 6, p. 27
(read from PDF): "In [6] there are listed four cases (which correspond to six cases in our
terminology) of possible counterexamples with max(deg(P), deg(Q)) <= 100. They are discarded by
hand." ([6] = Moh 1983.) Their Section 6 table then marks in red exactly six cases with
max{deg P, deg Q} <= 100:

  | Family | (m,n)  | max{deg P, deg Q} | corresponding degree pair |
  |--------|--------|-------------------|---------------------------|
  | F1     | (3,4)  | 64                | (48, 64)                  |
  | F2     | (2,3)  | 75                | (50, 75)                  |
  | F3     | (3,2)  | 75                | (75, 50) type             |
  | F9     | (2,3)  | 84                | (56, 84)                  |
  | F17    | (2,3)  | 99                | (66, 99)                  |
  | F22    | (2,3)* | 96                | (64, 96)                  |

and states (same page, read from PDF): "Five of them correspond to the six cases found by Moh, one
of the cases of Moh was discarded by the algorithm because it featured (A0, A0') = ((7,21), (2,1)),
and (2,1) not in PLLC. The sixth red case, marked with a star, corresponds to F22. This case was
probably discarded as a possible counterexample by Heitmann (with no mention to it) by symmetry
reasons. This case corresponds to the first case listed in [5, pag. 426]"
([5] = Lih-Chung Wang, "On the Jacobian conjecture", Taiwanese J. Math. 9 (2005), no. 3, 421-431,
MR2162887).

So the precise verified statement is: Moh's paper lists four exceptional degree cases
(max in {64, 75, 84, 99}), which become six configurations in the GGV corner terminology; GGHV's own
algorithmic enumeration of possible counterexamples with max <= 100 also yields six configurations
(the table above), five of which match Moh's, with F22 (max 96) extra and one Moh configuration
((7,21),(2,1)) eliminated by their PLLC (possible last lower corner) filter. Any sharper attribution
of "six shapes" to Moh's own text is UNVERIFIED pending the Crelle scan.

Shape data for the six families (from the Section 5 table of arXiv:1708.07936, p. 25, read from PDF;
A0 is the top corner of the support, A1 the next corner along the chain, (m,n) the degree ratio
parameters; families are parameterized by j in N_0):

  F1:  A0 = (4,12),  A0' = (1,0), A1 = (7/4,3),  k=1, m = 2j+3, n = 3j+4
  F2:  A0 = (5,20),  A0' = (1,0), A1 = (7/5,2),  k=1, m = j+2,  n = 2j+3
  F3:  A0 = (5,20),  A0' = (1,0), A1 = (8/5,3),  k=1, m = 4j+3, n = 3j+2
  F9:  A0 = (7,21),  A0' = (1,0), A1 = (11/7,2), k=1, m = j+2,  n = 2j+3
  F17: A0 = (9,24),  A0' = (1,0), A1 = (11/3,8), k=1, m = 5j+2, n = 8j+3
  F22: A0 = (8,24),  A0' = (2,0), A1 = (14/4,6), A1' = (5/4,2), A2 = (5/4,2), k=1, m = j+2, n = 2j+3

Note gcd values v_{1,1}(A0) for these six: 16, 25, 25, 28, 33, 32; all >= 16, consistent with
Heitmann's bound (Task 5).

Moh's own assessment of the exceptional cases, as quoted by GGV (arXiv:1401.1784 v3, p. 2, read from
PDF): the author of [7] (Heitmann) is contrasted with Moh "who says 'we have no nice way to handle
these cases', referring to the exceptional cases found by Moh." (Quote of Moh relayed by GGV;
position in Moh's paper UNVERIFIED.)

Additional audit trail on Moh's hardest surviving case (99, 66): Yansong Xu, "Intersection Numbers
and Split of Minor Roots" (arXiv:1604.07683, versions 2016-2022) discusses "all possibilities of the
splits of principle minor roots for the case of degree (99, 66)" and finds "an unknown possible
split" (abstract, verified at https://arxiv.org/abs/1604.07683). GGHV translated Xu's formulas and
obtained one of them only as an inequality (arXiv:1708.09367 abstract, verified).

---

## Task 2. Abhyankar's similarity of Newton polygons

### 2.1 Primary source

S. S. Abhyankar, "Lectures on expansion techniques in algebraic geometry", Tata Institute of
Fundamental Research Lectures on Mathematics and Physics, vol. 57, TIFR, Bombay, 1977. Notes by
Balwant Singh. MR542446 (80m:14016). (Bibliographic data read from the reference list of GGV,
arXiv:1401.1784 v3, p. 70, read from PDF.) The Tata notes cover "Irreducibility, Newton's Polygon;
The Jacobian Problem" (table of contents per
https://www.e-booksdirectory.com/details.php?ebook=7504). Verbatim theorem text from the Tata notes:
UNVERIFIED in this pass (scanned volume; not machine-readable here).

A web snippet found during the search (source page of arXiv:1605.09430 surroundings) states: "The
Newton polygons of a jacobian pair are similar (a result first presented by Abhyankar in the early
1970's)" and "Abhyankar shows in his 1977 Tata notes that an affirmative answer is equivalent to
showing that the Newton polygons of a jacobian pair are triangles." (Secondary phrasing; exact
locus in the Tata notes UNVERIFIED.)

### 2.2 The exact modern statement (verified, with the N^0 convention)

The statement as recorded in van den Essen's book and quoted verbatim by Lee-Li:

  "If (f,g) is a Jacobian pair with deg(f) > 1 and deg(g) > 1, then N^0(f) is similar to N^0(g)
  with the origin as center of similarity."

This is Proposition 2.1 of K. Lee and L. Li, "On the two-dimensional Jacobian conjecture: Magnus'
formula revisited, IV" (arXiv:2408.01279, verified at https://arxiv.org/html/2408.01279), where it
is attributed to [18, Theorem 10.2.1] with [18] = A. van den Essen, "Polynomial Automorphisms and
the Jacobian Conjecture", Progress in Mathematics 190, Birkhauser, 2000, MR1790619. The similarity
ratio is deg(f) : deg(g).

Recorded hypotheses and conventions:
- Ground field: characteristic zero (algebraically closed in the Lee-Li setting; van den Essen's
  book works over char-0 fields).
- "Jacobian pair" means J(f,g) is a nonzero constant.
- BOTH degrees must exceed 1. Edge case: if deg f = 1 or deg g = 1 the pair is elementarily an
  automorphism pair and the similarity statement is not asserted (a linear f has N^0(f) a segment
  or small triangle and similarity with N^0(g) generally fails).
- The N^0 convention: N^0(f) is the Newton polygon taken together with the origin, i.e. the convex
  hull of Supp(f) union {(0,0)} (this is why the similarity is "with the origin as center"). The
  verbatim definition in van den Essen's book: UNVERIFIED here (book paywalled); the convention is
  used in exactly this form by Lee-Li.
- "Similar" means: N^0(f) maps onto N^0(g) under the homothety centered at the origin with ratio
  deg(g)/deg(f) (equivalently deg P : deg Q as segment ratio).

Related refinements verified in this pass:
- van den Essen book, Corollary 10.2.21 (cited and used by GGV, arXiv:1401.1784 v3, p. 17, read
  from PDF): a counterexample can be brought to "subrectangular shape": there is an automorphism
  phi of L and integers 1 <= a <= b with (a,b) in Supp(phi(P)) subset of
  {(i,j) : 0 <= i <= a, 0 <= j <= b}. GGV attribute the argument they use to Leonid Makar-Limanov
  (acknowledgment, p. 64 of the PDF).
- van den Essen book, Theorem 10.2.23 (cited in GGV Remark 4.2, p. 15, read from PDF): for a
  minimal pair, neither v_{1,1}(P) divides v_{1,1}(Q) nor conversely ("classical argument").
- GGV Remark 4.5 (p. 15, read from PDF): on a common edge direction, en and st endpoints of P and Q
  are proportional with factor lambda = v_{rho,sigma}(Q) / v_{rho,sigma}(P) (the edge-level form of
  similarity).
- A dedicated chapter "Radial Similarity of Newton Polygons" exists in the Curacao proceedings
  volume (Automorphisms of Affine Spaces, Kluwer 1995), chapter DOI 10.1007/978-94-015-8555-2_10
  (Springer page found; author name UNVERIFIED, page blocked behind the publisher login).
- J. Lang and S. Maslamani, "Newton polygons of jacobian pairs", J. Pure Appl. Algebra 72 (1991)
  (ScienceDirect pii 002240499190128O, https://www.sciencedirect.com/science/article/pii/002240499190128O;
  page range UNVERIFIED, page blocked); studies Jacobian pairs f,g in C[x,y] via Newton polygons.
  Jeffrey Lang's companion paper "Jacobian pairs II", J. Pure Appl. Algebra 74 (1991), no. 1, 61-71,
  DOI 10.1016/0022-4049(91)90049-8, is reference [11] of GGV 1401.1784 (read from its reference
  list).

---

## Task 3. The 108 floor: arXiv:2204.14178

Verified from the arXiv abstract page and the PDF (both read):

- Title: "Increasing the degree of a possible counterexample to the Jacobian Conjecture from
  100 to 108".
- Authors: Jorge A. Guccione, Juan J. Guccione, Rodrigo Horruitiner, Christian Valqui.
- arXiv:2204.14178 [math.AG], v1 submitted 2022-04-29. DOI: 10.48550/arXiv.2204.14178.
- Abstract (verified): "We list all the pairs (deg(P), deg(Q)) with max{deg(P), deg(Q)} < 125 for
  any hypothetical counterexample to the plane Jacobian Conjecture and discard them all, except the
  pair (72,108) (and the symmetric pair (108,72)), thus we confirm the lower bound of 100 obtained
  by Moh and raise it up to 108."
- Main theorem (Theorem 2.1, p. 2, read from PDF): "If (P,Q) is a counterexample to the Jacobian
  Conjecture, then we have either max{deg(P), deg(Q)} >= 125, or
  (deg(P), deg(Q)) in {(72,108), (108,72)}."
- The 10-case table with max < 125 (p. 3, read from PDF), columns (A0, (m,n), max, discarded-by):
  ((4,12),(3,4),64: [4, sec 3.5],[10],[7]), ((4,12),(5,7),112: [4, sec 3.5]),
  ((5,20),(2,3),75: [3, sec 5], no detail in [10]), ((5,20),(3,2),75: same),
  ((7,21),(2,3),84: no detail in [10]; discarded in this paper),
  ((8,24),(2,3),96: [5, Prop 6.1]), ((8,28),(3,2),108: this paper / left open track),
  ((8,32),(3,2),120: this paper), ((9,24),(2,3),99: no detail in [10]; this paper),
  ((9,27),(2,3),108: this paper).
- The (72,108) case corresponds to (A0,(m,n)) = ((8,28),(3,2)); the authors "couldn't solve the
  corresponding system of polynomial equations, thus it is left open" (p. 2, read from PDF). They
  add: "With enough computing power we would be able to raise it up from 108 to 125, since there is
  only one case left" (p. 2).
- gcd(72,108) = 36 (consistent with all gcd constraints of Task 5).
- Publication status: no journal reference on arXiv; no published version found in this pass.
  Status as of 2026-07-22: preprint (UNVERIFIED whether under review or published elsewhere).

---

## Task 4. Novelty pass for the five program theorems

Method: adversarial search for prior statements. Sources examined in detail: GGV J. Algebra 471
(2017) 13-74 (arXiv:1401.1784 v3, full PDF), GGHV arXiv:1708.07936 (sections 1, 5, 6),
GGHV arXiv:2204.14178, GGV arXiv:1605.09430 (abstract), GGV arXiv:1708.09367 (abstract),
Heitmann JPAA 64 (1990) (via GGV and GGHV's accounts), van den Essen book ch. 10 (via Moskowicz's
and Lee-Li's verbatim quotations of 10.2.1, 10.2.21, 10.2.23, 10.2.24, 10.2.25, 10.2.26, 10.2.30),
Moh 1983 (via GGHV), Lee-Li series I-IV, Makar-Limanov (2013 MPIM preprint, Izv. Math. 2021,
Serdica 2025, Israel J. Math. 2025), Cassou-Nogues 2011, Miyanishi 2023, Dubouloz-Palka 2018,
Joseph 1975 and Dixmier 1968 (as used by GGV), Appelgate-Onishi 1985, Nagata 1988/1989,
Magnus 1954/1955, Nakai-Baba, Oka 1983, Zoladek 2008, Orevkov 2001, Xu 2016-2022,
Abhyankar-Assi math/0209159, Borisov 2020.

### THEOREM 1 (P = x + a x^u y^v, u >= 2, v >= 1, never a Keller component). Verdict: NOT FOUND.

No prior statement of this exclusion (for all partner degrees, automorphism case included) was
found. Closest adjacent art:
- GGV Proposition 4.6(5) (arXiv:1401.1784 v3, p. 15, read from PDF): for an (m,n)-pair, "Neither P
  nor Q are monomials." (Much weaker: monomials, not x + monomial.)
- The corner/last-lower-corner restrictions of Heitmann (JPAA 64 (1990), Theorems 2.24, 2.25:
  "establishes several restrictions on these possible corners (a,b)" and "finds families
  {(r+sj, t+uj) : j in N} of admissible pairs (m,n)"; description read from GGHV 1708.07936 p. 2)
  and of GGV/GGHV (PLLC filters, Definition 1.1 of 1708.07936) exclude vast classes of supports for
  counterexamples, but none of the published statements is the two-term component exclusion, and
  they only concern counterexamples (not components of automorphisms).
- The weight-decoupling technique itself (mixed-sign gradings (rho,sigma), leading-form power
  statements) is standard: GGV Remark 1.12, Theorem 2.6; van den Essen 10.2.8 with 10.2.17(i); and
  it "can be traced back to 1975 in [8]" = A. Joseph, "The Weyl algebra - semisimple and nilpotent
  elements", Amer. J. Math. 97 (1975), 597-615 (GGV intro, p. 1, read from PDF), with J. Dixmier,
  "Sur les algebres de Weyl", Bull. SMF 96 (1968), 209-242 behind it. The technique being known does
  not make the statement known.
Searches run (representative): "Jacobian pair binomial component"; "Keller map x + x^u y^v";
"two monomials Jacobian pair exclusion Newton polygon"; "coordinate x + monomial C[x,y]";
GGV corner classification papers; Heitmann corner lists. No hit on the statement.

### THEOREM 2 (Theorem 1 plus any strictly lower (v, 1-u)-weight tail R). Verdict: NOT FOUND.

Same landscape as Theorem 1. The idea "conclusion depends only on the top (rho,sigma)-leading form"
is implicit in all edge analyses (Joseph 1975; vdE 10.2.8; GGV Theorem 2.6 and Corollaries 7.2/7.4,
which "guarantee that the leading forms of P associated with certain directions can be written as
powers of certain polynomials", GGV p. 2, read from PDF), but no published statement excludes the
class "x + a x^u y^v + lower weight" as a Keller component. NOT FOUND as a statement.

### THEOREM 3 (no Newton-polygon top edge anchored at the linear vertex x; edge operator
(ms+1) phi + k z phi' on the y-class). Verdict: NOT FOUND as stated; PARTIALLY KNOWN in the
minimal-counterexample setting.

- For minimal counterexamples, the known shape restrictions already forbid many anchored-at-x
  configurations: GGV Proposition 4.7 and equation (4.6) (p. 16-17, read from PDF) put a
  normalized counterexample in subrectangular shape with strict direction constraints
  (-1,1) < Succ(1,0) < (-1,0); GGHV 2204.14178 Propositions 4.1-4.2 exhibit N(P) with lower-left
  chain {(0,0),(1,1),...}, i.e. the (1,1) corner rather than the bare x vertex. These are
  counterexample-only statements and do not cover the automorphism side, and none of them treats an
  edge x * phi(z), z = x^k y^m, by the multiplication-operator identity of Theorem 3.
- Edge-operator computations of exactly this flavor appear in the literature as tools: GGV's
  endnote [7] (p. 65, read from PDF) computes [F, l_{rho,sigma}(P)] for F = x^{u/l} y^v f(z),
  P = x^{r/l} y^s p(z), z a monomial in x^{-sigma/rho} y, obtaining
  x^{(u+r)/l - 1} y^{v+s-1} (c f(z) p(z) + a z f(z) p'(z) - b z f'(z) p(z)); the program's operator
  (ms+1) phi + k z phi' is a specialization of this known bracket calculus. Similar calculus:
  Appelgate-Onishi (JPAA 37 (1985), 215-227), Nagata's quasi-homogeneous edge obstructions (as
  described in Zoladek, Topology 47 (2008): "expansions ... with respect to quasi-homogeneous
  gradations defined by means of edges of Newton diagrams, obtaining similarity of Newton diagrams,
  reduction of their sizes, and obstructions to quasi-homogeneous parts"), Lang-Maslamani JPAA 72
  (1991), Oka, "On the boundary obstructions to the Jacobian problem", Kodai Math. J. 6 (1983),
  419-433 (https://projecteuclid.org/journals/kodai-mathematical-journal/volume-6/issue-3/), and
  Cassou-Nogues, "Newton trees at infinity of algebraic curves", CRM Proc. Lecture Notes 54, AMS
  2011, 1-19 (Newton-tree constraints at infinity for Jacobian pairs). None of these states
  Theorem 3's exclusion of ALL Keller components with a top edge anchored at the linear vertex x.
Verdict justification: the operator identity is within known bracket calculus (so the METHOD is not
new); the theorem STATEMENT (all coefficients, all partner degrees, automorphisms included) was not
found anywhere.

### THEOREM 4 (x a vertex of N(P), linear part x, implies P = x + f(y)). Verdict: PARTIALLY KNOWN
(counterexample side essentially implied by known results; the clean dichotomy not found).

- GGV Proposition 4.1 (arXiv:1401.1784 v3, p. 15, read from PDF) is the closest prior statement.
  Verbatim from its proof: assuming v_{rho,sigma}(P) <= rho for a direction between (1,0) and (0,1),
  "(i,j) in Supp(P) ==> i rho + j sigma <= rho ==> i = 0, or i = 1 and j = 0, which means that
  P = mu x + f(y) for some mu in K and f in K[y], and obviously (P,Q) can not be a counterexample
  to JC." I.e. GGV isolate exactly the alternative "P = mu x + f(y) (triangular, automorphism
  side) versus v_{rho,sigma}(P) > rho for all intermediate directions (counterexample side)". For
  counterexamples this forces the support strictly above the ray through x in every intermediate
  direction, which is the content of "x cannot be a Newton-polygon vertex" after normalization.
- Also relevant on the counterexample side: van den Essen 10.2.21 (subrectangular shape with corner
  (a,b), 1 <= a <= b); Makar-Limanov, "On the Newton polytope of a Jacobian pair", Izv. Math. 85:3
  (2021), 457-467, DOI 10.1070/IM9067 (arXiv:2106.06869): the minimal-counterexample polytope has a
  vertex v = (m,n) with n > m > 0 and lies in a trapezoid attached to v; and his Serdica Math. J.
  51 (2025), no. 3-4, 299-314 (DOI 10.55630/serdica.2025.51.299-314) develops "further information
  on the shape of the Newton polygon of f if the pair f,g is a counterexample."
- The automorphism side of Theorem 4 (a coordinate with linear part x and vertex x is exactly
  x + f(y)) was not found as a stated result; it is adjacent to Jung-van der Kulk structure theory
  (via [8] = Joseph and vdE Corollary 5.1.6(a), used by GGV p. 17: for an automorphism, one of
  M = v_{1,1}(psi(x)), N = v_{1,1}(psi(y)) divides the other).
Conclusion: the dichotomy as a single clean statement appears new, but its counterexample half is
essentially contained in GGV Prop 4.1 plus vdE 10.2.21; a novelty claim should be phrased as "sharp
dichotomy form" rather than "new exclusion".

### THEOREM 5 / earlier theorem (2D equivariant rigidity: every Gm-equivariant Keller map of C^2
with weights (w1, -w2) is linear). Verdict: NOT FOUND for the Gm (torus) case on C^2; the finite
group analog IS known, and the C* analog on OTHER surfaces is known to FAIL.

- M. Miyanishi, "Equivariant Jacobian Conjecture in dimension two", Transformation Groups 28 (2023),
  951-971, DOI 10.1007/s00031-022-09727-7, arXiv:2110.06709: for G a SMALL FINITE subgroup of
  GL(2,C) and a G-equivariant etale endomorphism of A^2, the endomorphism is an automorphism if the
  order of G is even (main theorem verified from the ar5iv text; the paper contains no discussion of
  C*/Gm actions in the equivariance hypothesis, verified by direct inspection of the ar5iv HTML).
- A. Dubouloz, K. Palka, "The Jacobian Conjecture fails for pseudo-planes", Adv. Math. 339 (2018),
  248-284, DOI 10.1016/j.aim.2018.09.020 (arXiv:1701.01425): counterexamples to the equivariant
  Generalized Jacobian Conjecture with G infinite exist "if and only if G = C*", but on Q-acyclic
  pseudo-planes of negative Kodaira dimension, NOT on C^2 itself (verified from abstract). This is
  the key adjacent result: it shows C*-equivariance does NOT rigidify etale endomorphisms on
  general surfaces, so a C^2-specific proof has content.
- The positive-weights case (both weights positive) is folklore-trivial by weight counting
  (v(P) + v(Q) = w1 + w2 forces linearity); the mixed-sign case (w1, -w2) is precisely where the
  weight classes are infinite-dimensional, and no prior statement was found. Nagata's edge-gradation
  "obstructions to quasi-homogeneous parts" (per Zoladek's description, see Theorem 3 above) and GGV
  Remark 1.12 / Proposition 1.13 (facts about (rho,sigma)-homogeneous Jacobian pairs, read from
  PDF p. 4) are the closest published machinery, again without the rigidity statement.
Searches run (representative): "equivariant Jacobian conjecture" (found only Miyanishi and
Dubouloz-Palka); "C*-equivariant polynomial endomorphism plane"; "torus equivariant Keller linear";
"quasi-homogeneous Jacobian pair two variables linear"; "weighted homogeneous Keller map
invertible". No statement covering Gm-equivariant Keller maps of C^2 with mixed weights was found.

---

## Task 5. Minimal-counterexample polygon constraints (the "lower-left staircase" landscape)

### 5.1 gcd / degree-pair coverage (all verified against the cited texts)

- Magnus, gcd = 1. Moskowicz arXiv:1610.01621 p. 3, item (12) (read from PDF): "Magnus' theorem
  [25]: If the greatest common divisor of the degrees of F1 and F2 is 1, then F is an automorphism,
  and the degree of F1 is 1 or the degree of F2 is 1." Recorded in van den Essen's book as (a
  generalization) Theorem 10.2.24, with Corollary 10.2.25: if deg F1 or deg F2 is prime, F is an
  automorphism. CITATION CAUTION for the program (which currently cites "Magnus 1954"): two Magnus
  papers circulate. (i) A. Magnus, "Volume preserving transformations in several complex variables",
  Proc. Amer. Math. Soc. 5 (1954), 256-266: this is the source of "Magnus' formula" per Lee-Li
  (arXiv:2201.06613 abstract, verified). (ii) A. Magnus, "On polynomial solutions of a differential
  equation", Math. Scand. 3 (1955), 255-260: this is the paper standardly cited for the coprime
  theorem (web search consensus). Which of the two contains the gcd = 1 theorem verbatim:
  UNVERIFIED here; the program should cite the 1955 Math. Scand. paper for gcd = 1 and the 1954
  PAMS paper for Magnus' formula.
- Nakai-Baba, gcd <= 2. Moskowicz p. 4 (read from PDF): "F is an automorphism, if the greatest
  common divisor of the degrees of F1 and F2 is: <= 2; Nakai and Baba [4]." (Standard citation:
  Y. Nakai, K. Baba, Osaka J. Math. 14 (1977); exact bibliographic detail UNVERIFIED here.)
- Appelgate-Onishi and Nagata, gcd <= 8 or prime. Moskowicz p. 4 (read from PDF): "<= 8 or a prime
  number; Appelgate and Onishi [3] and Nagata [30]. Those results can be found in Essen's book
  [16, pages 254-256]." Primary: H. Appelgate, H. Onishi, "The Jacobian conjecture in two
  variables", J. Pure Appl. Algebra 37 (1985), 215-227
  (https://www.sciencedirect.com/science/article/pii/0022404985900994; the paper proves JC "under
  the further assumption that the degree of f or g has at most two prime factors", per the
  ScienceDirect record); M. Nagata, "Two-dimensional Jacobian conjecture", in: Algebra and Topology
  (Korea, 1988), and M. Nagata, "Some remarks on the two-dimensional Jacobian Conjecture", Chinese
  J. Math. 17 (1989), 1-7 (venues per web search; exact page data of the 1988 proceedings
  UNVERIFIED).
- Abhyankar 2008: gcd != p and B >= 9. From GGV arXiv:1401.1784 v3 p. 2 (read from PDF): "in
  [2, Lemma 6.1] it is proven that gcd(deg(P), deg(Q)) != p" and "in [3, Corollary 8.9] it is
  proven that B >= 9", where [2] = S. S. Abhyankar, "Some thoughts on the Jacobian Conjecture,
  Part II", J. Algebra 319 (2008), 1154-1248, and [3] = "... III", J. Algebra 320 (2008),
  2720-2826 (reference list read from PDF p. 70).
- Heitmann 1990: B >= 16. GGV p. 1-2 (read from PDF): elementary reproof of "the result of Heitmann
  in [7], which states that gcd(deg(P), deg(Q)) >= 16 for any counterexample (P,Q)"; [7] =
  R. Heitmann, "On the Jacobian conjecture", J. Pure Appl. Algebra 64 (1990), 35-72, MR1055020.
  GGV also quote Heitmann's own caveat: "Nothing like this appears in the literature but results of
  this type are known by Abhyankar and Moh and are easily inferred from their published work",
  adding "we do not know how to do this, and we did not find anything like this in the literature
  till now" (p. 2, read from PDF).
- GGV 2014-2017: gcd != 2p; B = 16 or B > 20; case-16 shape. GGV, J. Algebra 471 (2017), 13-74
  (arXiv:1401.1784 v3): abstract (verified): elementary proof of gcd >= 16, proof that
  gcd(deg P, deg Q) != 2p for any prime p, and a thorough analysis of the case gcd = 16 "adapting a
  reduction of degree technique introduced by Moh". Sharper internal results read from the PDF:
  Corollary 7.9 (p. 45): for a standard (m,n)-pair, (a,b) := (1/m) en_{1,0}(P) has gcd(a,b) > 2,
  and B != p, B != 2p; Corollary 7.12 (p. 47): "We have B = 16 or B > 20"; Theorem 7.11 (p. 45):
  either v_{1,1}(A0) > 20 or A0 = (4,12), (rho,sigma) = (4,-1), gamma = 3, en(F) = (3,9);
  Corollary 7.13 (p. 47): if B = 16 then Dir(P) = Dir(Q) = {(4,-1),(-2,1),(-1,-1),(0,-1)}, with
  l_{4,-1}(P) = lambda_P R0^m for R0 = x(x y^4 - lambda_0)^3 and l_{-2,1}(P) = lambda_P R1^{4m} for
  R1 = y(x y^2 - lambda_1); Theorem 8.12 (p. 64): full reduced normal form of a hypothetical B = 16
  pair. IMPORTANT AUDIT NOTE from GGV p. 2 (read from PDF): H. Zoladek, "An application of
  Newton-Puiseux charts to the Jacobian problem", Topology 47 (2008), 431-469, claims B > 16 (and
  the author "claims to have verified that B > 33"), but GGV report the proof "relies on
  [15, Lemma 4.10], which has a gap, since it claims without proof that I2 subset (1/m) Gamma(f2),
  an assertion which cannot be proven to be true", so "B >= 16 remains up to the moment the best
  lower limit for B". Do not cite Zoladek's B > 33.
- Combined coverage: a counterexample gcd B satisfies B >= 16, B composite, B != 2p, B = 16 or
  B > 20. This is exactly the "{1..8} union primes union 2 primes" coverage the program refers to:
  gcd in {1,...,8} (Magnus, Nakai-Baba, Appelgate-Onishi, Nagata), gcd prime (Magnus corollary /
  Abhyankar Lemma 6.1), gcd = 2p (GGV; also announced by Abhyankar per GGV p. 2). If the program's
  "{1,8}" means the two-element set {1, 8}, that is UNVERIFIED / incorrect; the verified coverage
  is the full interval gcd <= 8.

### 5.2 Shape and corner constraints for minimal counterexamples (verified)

- Trapezoidal minimal pairs: GGV arXiv:1401.1784 v3, p. 3 (read from PDF): "At the beginning of
  Section 4 we introduce the concept of a minimal pair and prove that a minimal pair can be assumed
  to have a trapezoidal shape." Minimal pair := counterexample with B = gcd(v11(P), v11(Q))
  (Section 4, p. 14, read from PDF). Standard (m,n)-pair: an (m,n)-pair with P,Q in L^(1) and
  v_{1,-1}(st_{1,0}(P)) < 0 (Definition 4.3, p. 15, read from PDF).
- Direction/corner facts (GGV Prop 4.6, p. 15, read from PDF): v_{1,0}(P), v_{1,0}(Q) > 0;
  en_{1,0}(Q) = (n/m) en_{1,0}(P); (1/m) en_{1,0}(P) is in (1/l)N x N with
  v_{1,-1}(en_{1,0}(Q)) < 0; v_{0,-1}(en) < -1; neither P nor Q monomials.
- Edges cut above the diagonal: GGV Prop 5.16, with the remark (p. 2, read from PDF) that this
  "geometric fact ... was already known to Joseph and used in [8, Theorem 4.2], in order to prove
  the polarization theorem" (Joseph 1975).
- Lower side restrictions: GGV, "The two-dimensional Jacobian conjecture and the lower side of the
  Newton polygon", arXiv:1605.09430 (v2 2017-08-29), abstract (verified): "if the Jacobian
  Conjecture in two variables is false and (P,Q) is a standard minimal pair, then the Newton
  polygon HH(P) of P must satisfy several restrictions that had not been found previously",
  allowing them to discard corners and infinite families found in prior work.
- Algorithmic corner enumeration: GGHV arXiv:1708.07936 (verified, abstract plus sections 5-6 read
  from PDF): computes all possible corners (a,b) with a+b < 36 and all families for
  gcd(deg P, deg Q) <= 35, and all pairs (deg P, deg Q) with max <= 150; 24 families F1..F24 listed
  (17 of chain length 1, 7 of length 2); 34 possible counterexample configurations with
  max <= 150, of which 13 come from the families (table p. 27, read from PDF), 9 more with chains
  of length 1, 11 with length 2, 1 with length 3 (tables pp. 27-28). Remark 5.1: the possible
  counterexample in F13 with j = 1 "was analyzed extensively by Orevkov" in S. Yu. Orevkov,
  "Counterexamples to the 'Jacobian conjecture at infinity'", Proc. Steklov Inst. Math. 235 (2001),
  173-201.
- Reduced polygons for the surviving small cases: GGHV arXiv:2204.14178 Prop 4.1 (case (9,27)):
  N(P) = {(0,0),(1,1),(6,16),(6,18),(0,18)}, N(Q) = {(0,0),(1,0),(9,24),(9,27),(0,27)}; Prop 4.2
  (case (9,24)) similar with three sub-cases (read from PDF p. 5). Note the (1,1) lower corner.
- Makar-Limanov's polytope program: MPIM preprint 2013-53 "On the Newton polygon of a Jacobian
  mate" (reference [13] of GGV 1401.1784, read from its reference list); Izv. Math. 85:3 (2021)
  457-467 (three-dimensional Newton polytope of the dependence P(x,F,G) = 0: all vertices in two
  coordinate planes, two horizontal right-triangle faces, no slanted edges; sharper geometric
  degree bound; new proof of Abhyankar's two-characteristic-pair case; verified from ar5iv);
  Serdica Math. J. 51 (2025) 299-314 (further shape information); "A Jacobian mate defines the
  Jacobian pair", Israel J. Math. (2025), DOI 10.1007/s11856-025-2863-6, abstract (verified):
  given f, the subalgebra C[f,g] is determined and g is recovered up to a polynomial in f.
- Lee-Li program (2022-2024): "On the two-dimensional Jacobian conjecture: Magnus' formula
  revisited" I (Hurst, Lee, Li, Nasr, arXiv:2201.06613), II (arXiv:2205.12792), IV (Lee, Li,
  arXiv:2408.01279: F-generator, "northeastern vertex of the Newton polygon of each inner
  polynomial is located in a specific region", Conjecture E partial results; verified from the
  HTML). These give new vertex-region constraints on counterexample polygons.
- Borisov: A. Borisov, "Frameworks for two-dimensional Keller maps", Electron. J. Combin. 27(3)
  (2020), #P3.54 (https://www.combinatorics.org/ojs/index.php/eljc/article/view/v27i3p54)
  (combinatorial "framework" constraints at infinity for Keller maps; found in search, details not
  further verified in this pass).
- Newton trees: P. Cassou-Nogues, "Newton trees at infinity of algebraic curves", in Affine
  Algebraic Geometry, CRM Proc. Lecture Notes 54, AMS, 2011, 1-19 (constraints on Newton trees at
  infinity relevant to Jacobian pairs; found via GGV reference [4] and web search).

### 5.3 Newer degree-pair exclusions 2015-2026 (verified)

- GGV arXiv:1605.09430 (2016-2017): eliminates corners and infinite families beyond 1401.1784.
- GGHV arXiv:1708.07936 (2017): full enumeration gcd <= 35 and max deg <= 150 (see 5.2).
- GGHV arXiv:2204.14178 (2022): all pairs with max < 125 discarded except (72,108)/(108,72);
  floor raised 100 -> 108 (Task 3).
- Xu arXiv:1604.07683 (2016-2022): case (99,66) split analysis; one unknown split remains.
- Lee-Li I-IV (2022-2024): vertex-region constraints (see 5.2); no new absolute floor claimed.
- Makar-Limanov 2021/2025: polytope constraints and degree estimate (see 5.2).
No newer verified absolute floor beyond 108 was found (the GGHV remark that 125 is reachable "with
enough computing power" remains prospective).

---

## Summary table

| Program theorem | Verdict | Key prior references (closest art) |
|---|---|---|
| T1: P = x + a x^u y^v never a Keller component | NOT FOUND (statement new as far as this pass can tell; method classical) | Joseph AJM 97 (1975) 597-615; GGV J. Algebra 471 (2017) Prop 4.6(5), Thm 2.6; Heitmann JPAA 64 (1990) corner lists; vdE book 10.2.8/10.2.17 |
| T2: T1 plus lower-weight tail | NOT FOUND | same as T1; GGV Cor 7.2/7.4 (leading forms are powers) |
| T3: no top edge x*phi(z) at the linear vertex | NOT FOUND as stated; PARTIALLY KNOWN for minimal counterexamples (corner restrictions); operator identity is standard bracket calculus | GGV 1401.1784 endnote [7] bracket computation; GGHV 2204.14178 Prop 4.1-4.2; Appelgate-Onishi JPAA 37 (1985); Nagata 1988/89; Oka Kodai 6 (1983); Cassou-Nogues 2011; Lang-Maslamani JPAA 72 (1991) |
| T4: vertex x implies P = x + f(y) | PARTIALLY KNOWN (counterexample half essentially in GGV Prop 4.1 + vdE Cor 10.2.21; clean dichotomy not found) | GGV 1401.1784 Prop 4.1 (verbatim "P = mu x + f(y)" alternative); vdE 10.2.21; Makar-Limanov Izv. Math. 85:3 (2021) |
| T5: Gm-equivariant Keller maps of C^2 linear | NOT FOUND for Gm on C^2; finite-G analog known (Miyanishi); C* analog FAILS on pseudo-planes (Dubouloz-Palka), so C^2 case has content | Miyanishi, Transf. Groups 28 (2023) 951-971; Dubouloz-Palka, Adv. Math. 339 (2018) 248-284; folklore positive-weight case |
| Moh floor (context) | VERIFIED: max <= 100 discarded, full detail only for 64; four exceptional cases = six configurations | Moh Crelle 340 (1983) 140-212; GGHV 2204.14178; GGHV 1708.07936 sec. 6; Heitmann JPAA 64 (1990); Wang TJM 9 (2005) 421-431 |
| 108 floor (context) | VERIFIED: max >= 125 or (72,108)/(108,72); preprint status | GGHV arXiv:2204.14178 Thm 2.1 |
| Similarity theorem (context) | VERIFIED: vdE book Thm 10.2.1 form, N^0 polygons, deg > 1 both, origin-centered, ratio deg P : deg Q; primary origin Abhyankar Tata 1977 | vdE Progress in Math. 190 (2000); Lee-Li arXiv:2408.01279 Prop 2.1; Abhyankar TIFR LN 57 (1977) |

## Open verification items (flagged UNVERIFIED above)

1. Verbatim text of Moh's own list of exceptional cases in Crelle 340 (GDZ scan not machine-readable
   in this pass; the four-cases/six-configurations statement rests on GGHV's two papers).
2. Verbatim statements of van den Essen book Theorems 10.2.1 / 10.2.21 / 10.2.23 / 10.2.24 /
   10.2.25 / 10.2.26 / 10.2.30 (quoted here through Lee-Li, GGV and Moskowicz).
3. Which Magnus paper (PAMS 1954 vs Math. Scand. 1955) contains the gcd = 1 theorem verbatim.
4. Author of the "Radial Similarity of Newton Polygons" chapter (Kluwer 1995, DOI
   10.1007/978-94-015-8555-2_10).
5. Publication status of arXiv:2204.14178 (no journal reference found).
6. Page range of Lang-Maslamani JPAA 72 (1991); exact venue data of Nagata 1988 (Korea proceedings)
   and Nakai-Baba 1977.
