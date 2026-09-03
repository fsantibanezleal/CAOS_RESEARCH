# Dossier: Hoa's 1994 conjecture on maximal non-Hamiltonian graphs and Zhan's 2026 disproof

Date: 2026-09-02 (written 2026-09-03 local time)
Scout: Lucy (Claude Code session, CAOS research program)
Status marks: [V] verified against a primary source that I read; [V2] verified only through a secondary source (abstract page, zbMATH review, citing paper); [U] unverified or not located; [D] my own derivation from verified statements (not in the literature as far as I found).

Persisted primary files (all under `E:\_Temp\caos-research-newproblem\program\scouting-2026-09\`):
- `zhan2608.00957v3.pdf` (arXiv:2608.00957v3, 9 pages, read in full) and `zhan2608.00957v3.txt`
- `bullock2008.pdf/.txt` (Electron. J. Combin. 15 (2008) R18, read Theorem 3.13 and surrounding text)
- `frick-singleton-0407292.pdf/.txt` (arXiv:math/0407292, EJC 12 (2005) R32)
- `platypus1712.05158.pdf/.txt` (Goedgebeur, Neyt, Zamfirescu, Appl. Math. Comput. 386 (2020) 125491)
- `jooken2508.20825.pdf/.txt` (Jooken, Computer-assisted graph theory: a survey, arXiv:2508.20825)
- `gould-updating.pdf/.txt` (Gould, Updating the Hamiltonian problem, survey)
- `atlas_mnh_check.py` (my reproduction of OEIS A185306 for n <= 7 and a check of the conjecture there)
- `cr.py`, `zb.py`, `s2.py` (Crossref, zbMATH, Semantic Scholar lookups used for the citations below)

Note on `zamfirescu-platypus-2017.pdf`: I guessed the arXiv id and it resolved to an unrelated paper; ignore that file. The 2017 JGT paper is cited below through its DOI and through the 2020 paper that restates its lemma.

---

## 1. Definitions and the exact conjecture

**Maximal non-Hamiltonian (MNH) graph.** "A graph G is said to be maximal non-Hamiltonian if G is non-Hamiltonian, but G + e is Hamiltonian for every nonedge e of G." [V] Zhan, arXiv:2608.00957v3, abstract and Section 1. The same definition, with the equivalent reformulation "any two non-adjacent vertices of G are ends of a hamiltonian path", is used by Clark and Entringer (Period. Math. Hungar. 14 (1983) 57-68, DOI 10.1007/BF02023582) [V2, Springer abstract summary] and by Frick and Singleton (EJC 12 (2005) R32, arXiv:math/0407292, Section 1) [V]. Consequences used everywhere below:

- Every MNH graph of order n >= 3 that is not complete is traceable (a Hamilton path joins any nonadjacent pair). [D, immediate from the definition]
- Counting conventions: K_1 is treated as Hamiltonian and K_2 as MNH, so the OEIS count starts 0, 1. [V] OEIS A185306 comment.
- "Every maximal non-Hamiltonian graph of connectivity 1 consists of two complete graphs sharing exactly one vertex. Thus every maximal non-Hamiltonian graph of order at least 4 contains a cycle." [V] Zhan, Section 1 (stated as "easy to see", no citation).

**Longest cycle, circumference, detour.** C is a longest cycle of G; the circumference is |C|. Zhan calls a longest path a detour and its order the detour order. [V] Zhan, Section 1. Hoa's own name for G - V(C) is "restgraph" (title of Hoa 2005). [V] Zhan reference [4]; zbMATH 1602796 table of contents.

**Conjecture 1 (Hoa, 1994).** "If G is a maximal non-Hamiltonian graph and C is a longest cycle of G, then G - V(C) is a complete graph." [V] Zhan, Section 1, verbatim.

Provenance of the conjecture:
- Zhan: "In 1994, Vu Dinh Hoa posed the following conjecture at the Second Krakow Conference on Graph Theory [3]", with [3] = V.D. Hoa, Problem 266, in Research Problems, Discrete Math. 164 (1997) 317-321. [V] Zhan, Section 1 and reference list.
- The Discrete Mathematics item exists: DOI 10.1016/S0012-365X(96)00067-2, "Second Krakow conference on graph theory research problems" (problems collected by Vera T. Sos), Discrete Math. 164 (1997) 317-321; zbMATH 1019078 review: "Open problems formulated during the Second Krakow Conference on Graph Theory (Problems 262 through 270)." [V2] Crossref and zbMATH API. I could not read the text of Problem 266 itself (ScienceDirect blocked); the exact wording as printed in 1997 is [U].
- Hoa's later paper: V.D. Hoa, "Longest cycles and restgraph in maximal nonhamiltonian graphs", in The Mathematical Foundation of Informatics (Hanoi, 25-28 Oct 1999), eds. D.L. Van and M. Ito, World Scientific 2005, pp. 67-70, DOI 10.1142/9789812703118_0007. [V2] Crossref, zbMATH 1602796, Semantic Scholar (its only recorded citation is Zhan 2026). Zhan states: "Hoa [4] later proved that Conjecture 1 holds if (1) the toughness of G is less than 1; or (2) delta(G) >= n/3 where n is the order of G." [V] Zhan, Section 1. I could not open the chapter (World Scientific 403). One web-search summary of the publisher's book page paraphrases the chapter as addressing "Erdos's conjecture that if C is a longest cycle in a maximal nonhamiltonian graph G, then G - C is a complete graph". This attribution to Erdos conflicts with Zhan's attribution to Hoa and is [U]; it should be settled by reading pp. 67-70 and Problem 266.
- Titles guessed in the task brief ("On the length of longest dominating cycles in graphs", "A remark on maximal non-hamiltonian graphs") do not correspond to anything I found for Hoa. Hoa's nearby papers are "A sharp lower bound for the circumference of 1-tough graphs with large degree sums", J. Graph Theory 20 (1995) 137-140, DOI 10.1002/jgt.3190200204, and "Long cycles and neighborhood union in 1-tough graphs with large degree sums", Discuss. Math. Graph Theory 18 (1998) 5-13, DOI 10.7151/dmgt.1059. [V2] Crossref. Neither is the source of the conjecture.

**What Hoa's two theorems imply for any counterexample.** [D] Any counterexample has toughness >= 1 (hence is 2-connected, and in particular is not "two cliques sharing a vertex") and minimum degree delta < n/3. Zhan's G_56 has delta(G) <= 4 (w_7 has degree 4) and a 3-cut {z, x, y} leaving three components, so its toughness is at most 1; combined with Hoa's theorem its toughness is exactly 1. [D from Zhan's construction plus Hoa's theorem as quoted by Zhan]

**Trivial cases that satisfy the conjecture.** [D]
- Connectivity 1 (two cliques K_a, K_b sharing v): the longest cycle is the larger clique, the residual is the other clique minus v, complete.
- Circumference n - 1 (in particular every hypohamiltonian MNH graph such as Petersen, Coxeter, Tietze, and the Isaacs snarks J_k, which Bullock et al. call maximal hypohamiltonian): the residual is K_1. So counterexamples need circumference <= n - 2; Zhan's have circumference exactly n - 2.

---

## 2. Zhan's counterexamples (arXiv:2608.00957)

**Bibliographic.** Xingzhi Zhan (East China Normal University), "Counterexamples to a conjecture of Hoa on maximal non-Hamiltonian graphs", arXiv:2608.00957, v1 2 Aug 2026, v3 14 Aug 2026, 9 pages, 3 figures, MSC 05C38, 05C45, 05C40; supported by NSFC 12271170 and STCSM 22DZ2229014. Declaration of AI use: "ChatGPT was used to assist in developing and checking the constructions and proofs. The author independently verified all mathematical arguments". [V] arXiv abs page and PDF pp. 1, 8. No journal reference as of 2026-09-02. [V] arXiv abs page. Semantic Scholar shows no citing papers yet (query returned 429 once; the Hoa 2005 record lists Zhan as its only citer). [V2]

**Abstract (verbatim).** "A graph G is said to be maximal non-Hamiltonian if G is non-Hamiltonian, but G + e is Hamiltonian for every nonedge e of G. In 1994, Vu Dinh Hoa conjectured that if C is a longest cycle of a maximal non-Hamiltonian graph G, then G - V(C) is a complete graph. We disprove this conjecture by constructing a counterexample of every order n >= 56. We also pose several related open problems." [V]

**Tool imported: Lemma 1 = Bullock, Frick, Singleton, van Aardt, Mynhardt, Theorem 3.13.** Zhan quotes [2, Theorem 3.13] of "Maximal nontraceable graphs with toughness less than one", Electron. J. Combin. 15 (2008) R18, DOI 10.37236/742. The original statement (my extraction from the EJC PDF, p. 15) [V]:

> Theorem 3.13. Let G be a graph with a minimum vertex-cut S = {x, y} such that G - S consists of three noncomplete components G_1, G_2, G_3 and N_{G_i}(x) = N_{G_i}(y) = N_i != V(G_i), for i = 1, 2, 3. Then G is maximal nontraceable if and only if the following hold: (i) xy in E(G). (ii) X_i = <V(G_i) u {x}> is MNH for i = 1, 2, 3. (iii) At most one of the graphs <N_i> has a universal vertex. (iv) All three graphs G_i are traceable and at least two of them are homogeneously traceable. (v) If u is a universal vertex of <N_i> for some i in {1, 2, 3}, then G_i is traceable from u.

Zhan restates it with "dominating vertex" for "universal vertex" and adds that S is a minimum cut of a 2-connected H. [V] Zhan Lemma 1. Bullock et al. illustrate the theorem with three Petersen copies (their Figure 14) and note any X_i may be replaced by a maximal hypohamiltonian graph (Petersen, Coxeter, Chisala's G3-snark, Isaacs' J_k for odd k >= 5). [V] EJC p. 17.

**Auxiliary graphs (verbatim adjacency, upper neighbourhoods Gamma(i) = N(i) intersect {j > i}).** [V] Zhan Section 2.

A_19 on {1, ..., 19}: Gamma(1) = {2,3,7}, Gamma(2) = {3,7}, Gamma(3) = {4,7,8,11,12,18}, Gamma(4) = {5,6,8}, Gamma(5) = {6}, Gamma(6) = {7,11}, Gamma(7) = {8,11,15,19}, Gamma(8) = {9,10,11,15,19}, Gamma(9) = {10,11}, Gamma(10) = {11}, Gamma(11) = {12,18}, Gamma(12) = {13,14,15}, Gamma(13) = {14,15}, Gamma(14) = {15,18,19}, Gamma(15) = {16,17,18}, Gamma(16) = {17,18}, Gamma(17) = {18}, Gamma(18) = {19}. So N_{A_19}(19) = {7, 8, 14, 18}.

A_17 on {1, ..., 18} minus {8}: Gamma(1) = {2,3,11,15,18}, Gamma(2) = {3,14,16}, Gamma(3) = {4,5}, Gamma(4) = {5,12,17}, Gamma(5) = {6,7,11,15}, Gamma(6) = {7}, Gamma(9) = {10,11}, Gamma(10) = {11}, Gamma(11) = {12,13}, Gamma(12) = {13,17}, Gamma(13) = {14,15}, Gamma(14) = {15,16}, Gamma(15) = {18}. Then A_18 = K_1 join A_17 with K_1 = {8}, so N_{A_18}(18) = {1, 8, 15}.

B_18 = A_19 - 19, B_17 = A_18 - 18.

**Lemma 2 (computer-verified).** (i) A_19 and A_18 are MNH; (ii) B_18 and B_17 are homogeneously traceable; (iii) for distinct p, q in {1, 8, 15} the maximum order of a (p,q)-path in B_17 is 15; (iv) for distinct p, q in {7, 8, 14, 18} the maximum order of a (p,q)-path in B_18 is 16. "Proof. Properties (i), (ii), (iii), and (iv) were verified using SageMath programs." [V] Zhan p. 4. No code or data supplement is referenced. [V, absence]

**The maximal nontraceable graph M (order 55).** H_1, H_3 are disjoint copies of B_18 (vertices u_i, v_i), H_2 a copy of B_17 (vertices w_k); add x, y with N[x] = N[y] = {x, y, u_7, u_8, u_14, u_18, v_7, v_8, v_14, v_18, w_1, w_8, w_15}. Lemma 3: M is maximal nontraceable, by checking (i)-(v) of Lemma 1: M[V(H_i) u {x}] is A_19 (i = 1, 3) or A_18 (i = 2); M[N_1] and M[N_3] are 2K_2 (no dominating vertex) while M[N_2] is K_3. [V] Zhan Lemma 3.

**Lemma 4: detour order of M is 53.** Any path meeting all three H_i uses both x and y with exactly one H_i between them. Middle H_2: at most 18 + 15 + 18 + 2 = 53. Middle H_1 or H_3: at most 17 + 16 + 18 + 2 = 53. A path of order 53 exists: P = P_1 u u_7 x u x w_1 u P_2 u w_15 y u y v_7 u P_3 with P_1, P_3 Hamilton paths of H_1, H_3 ending at u_7, v_7, and P_2 = w_1 w_2 ... w_15 (order 15) in H_2. [V] Zhan Lemma 4.

**Lemma 5 (the MNT-to-MNH bridge).** "If H is a connected maximal nontraceable graph, then K_1 join H is maximal non-Hamiltonian, and the circumference is equal to the detour order of H plus one." Stated as obvious. [V] Zhan Lemma 5.

**Lemma 6, the base counterexample G_56.** G = K_1 join M with K_1 = {z}; C = zu u P u vz is a longest cycle, circumference 54, and G - V(C) = w_16 + w_17 = 2K_1 (w_16 w_17 is a nonedge of A_17, hence of M). [V] Zhan Lemma 6.

**Why 56.** 56 = 1 + |M| = 1 + (18 + 17 + 18 + 2). It is the order produced by this particular choice of gadgets (A_19, A_18); the paper makes no claim that 56 is the least order of a counterexample and says nothing about orders below 56. [V, absence of any such claim in the text]

**Theorem 7 (all n >= 56).** "For every integer n >= 56, there exists a maximal non-Hamiltonian graph H of order n with a longest cycle D such that H - V(D) = 2K_1." Construction: w_7 is a simplicial vertex of G with N_G(w_7) = {w_5, w_6, w_8, z} and w_7 w_8 in E(C). For n >= 57 take R = K_{n-56} and join every vertex of R to every vertex of N_G[w_7] = {w_5, w_6, w_7, w_8, z}, i.e. blow the simplicial vertex w_7 up into the clique K = {w_7} u V(R) whose members all have the same closed neighbourhood. Proof sketch: a Hamilton cycle of H would shrink (replace each maximal subpath inside K by an edge or by u' f v') to a Hamilton cycle of G; for a nonedge d_1 d_2 of H, a Hamilton path of G between d_1, d_2 (or between d_1 and f = w_7) is expanded through a Hamilton path of R; circumference of H is n - 2; D is C with the edge w_7 w_8 replaced by a (w_7, w_8)-path through R; H - V(D) = w_16 + w_17. [V] Zhan Section 3.

**The two reusable mechanisms.** [D, naming mine]
1. Join mechanism: G = K_1 join H with H connected MNT; the residual of the longest cycle through z is H minus a detour. So a counterexample of this type exists at order m + 1 exactly when some connected MNT graph H of order m has a detour P with H - V(P) not complete.
2. Simplicial blow-up: replacing a simplicial vertex that lies on a longest cycle by a clique with the same closed neighbourhood preserves MNH-ness, raises circumference and order by the same amount, and preserves the residual. Hence the set of orders admitting a counterexample is upward closed once a counterexample with a simplicial vertex on a longest cycle exists.

**Open problems posed (Section 4, verbatim).** [V]
- "Question 2. Let C be a longest cycle of a maximal non-Hamiltonian graph G. Must every component of G - V(C) be complete?" Remark: "This question is a weaker version of Conjecture 1."
- "Question 3. Does there exist a maximal non-Hamiltonian graph G with a longest cycle C such that G - V(C) is connected but not complete?" Remark: "An affirmative answer to Question 3 would provide a counterexample to Conjecture 1 of a different type."
- "Question 4. For every integer n >= 4, let f(n) denote the greatest integer k for which there exist a maximal non-Hamiltonian graph G of order n and a longest cycle C of G such that G - V(C) has exactly k components. Determine f(n)." Remark: "The results of this paper show that f(n) >= 2 for every n >= 56."

Name clash to keep in mind: Zhan's f(n) is unrelated to the classical f(n) = minimum size of an MNH graph of order n (Bollobas's problem, Section 4 below).

Trivial bounds on Zhan's f(n): f(n) >= 1 for every n >= 4, since an MNH graph of every order exists (K_{n-1} with a pendant edge, Section 4) and any MNH graph is non-Hamiltonian so G - V(C) is nonempty. [D]

---

## 3. The smallest-order question: what is known below 56

**Counts of MNH graphs by order.** OEIS A185306 "Number of maximally nonhamiltonian graphs on n vertices": 0, 1, 1, 1, 3, 3, 7, 9, 18, 31 for n = 1..10; keywords nonn, hard, more; author Eric W. Weisstein, 29 Aug 2013; the only link is MathWorld; there is no b-file, program or reference. [V] OEIS text format via curl. MathWorld lists the same terms and cites Bollobas 1978 (Extremal Graph Theory p. 167), Bondy 1972, Clark and Entringer 1983, Goedgebeur, Neyt, Zamfirescu 2020 and Zamfirescu 2017. [V] MathWorld page. So the public count stops at n = 10 and nobody has recorded n = 11 or 12.

**The 1982 catalogue.** J. Jamrozik, R. Kalinowski, Z. Skupien, "A catalogue of small maximal nonhamiltonian graphs", Discrete Math. 39 (1982) 229-234, DOI 10.1016/0012-365X(82)90145-5. [V2] Crossref and zbMATH 3754736. A web-search summary of the ScienceDirect abstract says it catalogues all MNH graphs of orders up to 10, which would be the source of the OEIS terms; I could not open the abstract (ScienceDirect 403), so the exact scope and the method (hand versus computer) are [U]. Related earlier structural paper: Z. Skupien, "On maximal non-Hamiltonian graphs", Rostock. Math. Kolloq. 11 (1979) 97-106. [V2] zbMATH 3689432, Gould's survey reference 283.

**My reproduction for n <= 7.** Script `atlas_mnh_check.py` (networkx graph atlas, all 1253 graphs on <= 7 vertices; brute-force Hamiltonicity; all longest cycles enumerated by vertex subsets). Output: MNH counts {2:1, 3:1, 4:1, 5:3, 6:3, 7:7}, matching A185306, and zero violations of Conjecture 1 over every longest cycle of every MNH graph of order <= 7. [V, local computation, 2026-09-03] So the least order of a counterexample is at least 8. Orders 8, 9, 10 (9, 18, 31 graphs) were not checked here because the atlas stops at 7; they are a few minutes of work once the graphs are generated (Section 5).

**Smallest-size (not smallest-order) literature, all consistent with the counts above but not enumerative beyond what they needed.**
- Bondy 1972: an MNH graph of order n >= 7 with m vertices of degree 2 has at least (3n + m)/2 edges, so f(n) >= ceil(3n/2) for n >= 7. [V2] Frick and Singleton Section 1 quoting Bondy [2].
- Bollobas 1978 posed the problem of determining f(n). [V2] Frick and Singleton; Clark and Entringer abstract.
- Clark and Entringer 1983: f(n) = ceil(3n/2) for even n >= 36 (Isaacs snarks J_k and variations); for odd n >= 55, f(n) is (3n+1)/2 or (3n+3)/2. [V2] Springer abstract summary. Conference precursor: Congr. Numer. 35 (1982) 431-434. [V2] zbMATH 3825880.
- Clark, Entringer, Shapiro, "Smallest maximally nonhamiltonian graphs II", Graphs Combin. 8 (1992) 225-231, DOI 10.1007/BF02349959. [V2] Crossref.
- X. Lin, W. Jiang, C. Zhang, Y. Yang, "On smallest maximally nonhamiltonian graphs", Ars Combin. 45 (1997) 263-270: f(n) = ceil(3n/2) for all n >= 20 and exact values of f(n) for 3 <= n <= 19; "small cases were set using a computer". [V2] zbMATH 1409195 review. Combined statement used by Frick and Singleton (Theorem 2.1, "Bondy and Lin, Jiang, Zhang and Yang"): every MNH graph of order n >= 6 has at least 3n/2 edges. [V]
- L. Stacho, "Maximally non-hamiltonian graphs of girth 7", Graphs Combin. 12 (1996) 361-371, DOI 10.1007/BF01858469; L. Stacho, "Non-isomorphic smallest maximally non-Hamiltonian graphs", Ars Combin. 48 (1998) 307-317: for n >= 88 at least tau(n) >= 3 smallest MNH graphs, tau(n) -> infinity. [V2] zbMATH 1600936 and Combinatorial Press page.
- P.V. Roldugin, "Construction of maximally non-Hamiltonian graphs", Discrete Math. Appl. 13 (2003) 277-289, DOI 10.1515/156939203322385883. [V2] Crossref; content not read.

**An unpublished list up to order 20 probably exists.** David P. Moulton (IDA Center for Communications Research, Princeton), talk "Maximal non-Hamiltonian graphs", Princeton Discrete Math Seminar, 27 Feb 2014: "every maximal non-Hamiltonian graph of order at least 3 is spanned by a figure-eight graph" (two cycles sharing a vertex, either allowed to degenerate to an edge), and the conjecture that every 2-connected MNH graph is spanned by a theta graph (subdivision of K_{1,1,2}), "verified computationally for all graphs of order at most 20". [V] Princeton abstract pages (math.princeton.edu events page and web.math.princeton.edu/~pds/abs/moulton14s). I found no paper, arXiv preprint or data release corresponding to this talk [U], and no indication that Hoa's conjecture was checked on that list [U]. If the verification really covered all 2-connected MNH graphs of order <= 20, that list would settle the least-order question up to 20 immediately; how it was generated (all graphs on 20 vertices cannot be enumerated) is [U].

**No public list of MNH graphs in House of Graphs.** The HoG meta-directory documents lists for hypohamiltonian graphs, snarks, platypus graphs and others; I found no MNH list. [U, negative search result] Platypus lists are complete for all orders <= 12 and, with girth restrictions, higher (Section 5), and they contain every MNH graph without a universal vertex (Section 4).

**Bottom line for Section 3.** Least order of a counterexample n_0 satisfies 8 <= n_0 <= 56. Nothing in the literature I could reach narrows this; the conjecture has been verified by me for n <= 7 only, and by nobody else in print at any order as far as I found. [V for the bounds; U for the literature gap, which is a negative statement]

---

## 4. Structural facts that bound a search, and known MNH families

**4.1 Degree-sum (Bondy-Chvatal) constraint.** Bondy and Chvatal, "A method in graph theory", Discrete Math. 15 (1976) 111-135, DOI 10.1016/0012-365X(76)90078-9: if u, v are nonadjacent with d(u) + d(v) >= n then G is Hamiltonian iff G + uv is. [V2] Crossref plus standard lecture-note statements. Consequence: in an MNH graph every nonadjacent pair has d(u) + d(v) <= n - 1, i.e. an MNH graph equals its own n-closure and that closure is not complete. [D] Moulton's abstract phrases this as Ore's condition restated for MNH graphs. [V2] This is a strong pruning rule for generation: an MNH graph has no nonadjacent pair of degree sum >= n, and (by Chvatal's degree-sequence version) its degree sequence fails the Chvatal Hamiltonicity condition.

**4.2 Size bounds.** e(G) >= 3n/2 for n >= 6 (Bondy; Lin et al.), and the classical Ore-Erdos maximum: the largest non-Hamiltonian graph of order n >= 6 has (n^2 - 3n + 4)/2 edges, uniquely K_{n-1} with a pendant edge (Bondy 1972 gave a new proof). [V2] Frick and Singleton Thm 2.1; arXiv:2606.16800 summary citing Bondy 1972.

**4.3 Connectivity and toughness.** kappa = 1 forces two cliques sharing a vertex (Zhan). Hoa 2005: the conjecture holds when toughness < 1, so a counterexample is 1-tough, hence 2-connected. [V2 via Zhan] Theorem 3.13 of Bullock et al. describes exactly the toughness < 1 MNT graphs with a 2-cut and three components that Zhan lifts to MNH by a join; the join adds one to every cut, so Zhan's counterexamples sit precisely at toughness 1, the boundary of Hoa's theorem. [D]

**4.4 Maximum degree.** Zamfirescu (J. Graph Theory 86 (2017) 223-243, DOI 10.1002/jgt.22122), as restated in Goedgebeur, Neyt, Zamfirescu 2020, Lemma 2: an MNH graph G is a platypus (non-Hamiltonian, every vertex-deleted subgraph traceable) iff Delta(G) < |V(G)| - 1. Corollary 12 of the 2020 paper: an MNH graph of order n cannot have maximum degree n - 2 or n - 3. [V] platypus1712.05158.txt lines 131-141 and 465-467. So every MNH graph either has a universal vertex or has Delta <= n - 4 and is a platypus.

**4.5 Universal vertex means K_1 join MNT.** If G = K_1 join H is MNH then H is nontraceable (a Hamilton path of H plus z closes to a Hamilton cycle) and for every nonedge e of H, H + e is traceable (delete z from a Hamilton cycle of G + e); so H is MNT. Conversely Zhan's Lemma 5 gives MNH for connected MNT H, and for disconnected MNT H (for instance two disjoint cliques) K_1 join H is the connectivity-1 family. Hence: MNH graphs with a universal vertex are exactly the graphs K_1 join H with H MNT. [D; the forward direction is Zhan's Lemma 5] MNT literature to use: Zelinka, Discuss. Math. Graph Theory 18 (1998) 205-208, DOI 10.7151/dmgt.1076 (two constructions, block graphs characterized) [V2 zbMATH]; Frick and Singleton 2005 (g(n) = minimum size of an MNT graph: g(n) = ceil((3n-2)/2) for n >= 54 and n in I u {12, 13}, and g(n) determined for n <= 9) [V]; Bullock, Frick, Singleton 2007, Discrete Math. 307 (2007) 1266-1275 [V2]; Bullock et al. 2008 (all MNT graphs of order < 8 are Zelinka graphs, "by consulting [10]" = Read and Wilson, An Atlas of Graphs, 1998; the propeller of order 8, size 15, is a smallest non-Zelinka MNT graph; every MNT graph of order 10 has at least 15 edges, from Singleton's 2005 UNISA thesis) [V]; "Further results on maximal nontraceable graphs of smallest size", DMTCS 15 (2013), g(n) = ceil((3n-22)/2)... note: the DMTCS abstract summary I saw quotes ceil((3n-2)/2) for n >= 54 and additional n, and g(n) = ceil(3n/2) for n in {10, 11, 14, 15, 16, 17}; the "(3n-22)/2" in the search summary looks like a transcription error [U]. Frank Bullock's PhD thesis "Detours in graphs", arXiv:2507.12086 (93 pages, July 2025), covers MNT graphs and detour-related classes. [V2] arXiv abs.

**4.6 Dominating longest cycles.** Nash-Williams: 2-connected, delta >= (n+2)/3 implies every longest cycle is dominating (G - V(C) edgeless). Bondy's 1980 conjecture generalizes to k-connected graphs. [V2] arXiv:2606.03696 summary. Hoa's delta >= n/3 theorem for MNH graphs lives next to this; for an MNH graph with delta >= (n+2)/3 the residual is edgeless, so complete only if it is K_1 or empty, which is presumably what Hoa's argument exploits. [D, speculative]

**4.7 Moulton's spanning structure.** Every MNH graph of order >= 3 is spanned by a figure-eight; conjecturally every 2-connected MNH graph is spanned by a theta graph (verified to order 20). [V2] A theta-spanned graph has two vertices joined by three internally disjoint paths covering V(G); the longest cycle uses the two longest of them, so under Moulton's conjecture the residual G - V(C) lies inside the interior of the third path and is therefore an induced subgraph of a path plus chords. That shape is compatible with Zhan's 2K_1 residual and with Question 3 (a connected residual would be a path segment with missing chords). [D]

**4.8 Known MNH families and how they behave under the conjecture.** [D unless noted]
- K_{n-1} with a pendant edge (K_{n-1} . K_2): MNH, kappa = 1, residual K_1. Exists for every n >= 3, so MNH graphs exist at every order.
- Two cliques sharing a vertex (all of kappa = 1): residual complete.
- K_k join (k+1)K_1 (order 2k+1; K_k plus the complement of K_{k+1}, the family named in the task brief): non-Hamiltonian because the independent set has size k + 1; adding an edge inside the independent set yields the Hamilton cycle a b k_1 i_1 k_2 i_2 ... k_{k-1} i_{k-1} k_k a; so MNH. Longest cycle alternates and has order 2k; residual K_1. More generally K_k join (K_{a_1} + ... + K_{a_{k+1}}) is MNH with toughness k/(k+1) < 1 and complete residual (the smallest of the k+1 cliques); these are the split-type graphs. MNH split graphs of Burkard-Hammer type are classified in Ngo Dac Tan and C. Iamjaroen, Discuss. Math. Graph Theory 28 (2008) 67-89, DOI 10.7151/dmgt.1392 [V2 eudml abstract], and in their "completion" paper [U, ResearchGate listing only].
- Cubic MNH graphs: Petersen (order 10, the smallest cubic MNH graph satisfying the Dudek-Katona-Wojda properties D(1), D(2)), Tietze (12), Coxeter (28), Isaacs flower snarks J_k for odd k (Clark and Entringer, Kalinowski and Skupien "Large Isaacs' graphs are maximally non-Hamilton-connected", Discrete Math. 82 (1990) 101-104). [V] Bullock et al. 2008 pp. 10, 16-17; platypus paper Theorem 1. Cubic MNH graphs with D(1), D(2) exist for every even n >= 52 and n in {10, 20, 28, 36, 38, 40, 44, 46, 48}. [V] Bullock et al. p. 10. All hypohamiltonian ones have residual K_1 (Section 1).
- Maximal non-Hamilton-connected graphs (Skupien 1989; Petersen, Coxeter, J_k odd k >= 7) are used as blocks X_i in Theorem 3.12 of Bullock et al. [V]
- Zhan's family G_56 and its simplicial blow-ups (Section 2): residual 2K_1, toughness exactly 1, circumference n - 2.

**4.9 Degree-2 vertices and Bondy's (3n+m)/2 bound** give a cheap filter for the sparse end; combined with 4.1 they make MNH graphs an unusually rigid class for generation (every nonadjacent pair is "tight").

---

## 5. Feasibility of exact computation

**5.1 Raw graph counts (OEIS A000088 / A001349).** All graphs / connected graphs on n unlabeled vertices: n = 10: 12,005,168 / 11,716,571; n = 11: 1,018,997,864 / 1,006,700,565; n = 12: 165,091,172,592 / 164,059,830,476; n = 13: 50,502,031,367,952; n = 14: 29,054,155,657,235,488. [V] OEIS text via curl; Jooken's survey Table 1 repeats n = 11, 12, 13. McKay's data page offers every graph up to n = 11 for download (n = 11: 373 MB compressed, incremental sparse6) and recommends geng for n >= 12. [V] users.cecs.anu.edu.au/~bdm/data/graphs.html.

**5.2 What geng can filter natively.** geng generates all pairwise non-isomorphic graphs on n vertices and accepts constraints on edge counts, minimum and maximum degree, and (bi)connectivity, plus a PRUNE hook for user code; specialized generators are usually needed beyond n = 12 or 13. [V] Jooken survey Section on geng (text lines 146-172, 609). A precedent of exactly the needed shape: Goedgebeur, Neyt, Zamfirescu independently verified their platypus counts "for the smaller orders by using the generator geng to generate all graphs and then filtering the platypuses", while the complete lists (all platypuses up to order 12; girth >= 4 to 14; girth >= 5 to 17; girth >= 6 to 20; girth >= 7 to 21; girth >= 8 to 24) came from a modified hypohamiltonian generator and are downloadable from House of Graphs. [V] platypus paper Section 5 and Table 1: 4, 48, 814, 24847 platypuses of orders 9, 10, 11, 12.

**5.3 Proposed exact pipeline for a complete classification of MNH graphs, and a check of Hoa's conjecture, by order.** [D]
1. Orders 8-10: 12 million graphs; brute-force MNH test (non-Hamiltonian, then for each nonadjacent pair a Hamilton path with those endpoints) and all-longest-cycles enumeration; minutes on one core in C, hours in Python. This confirms 9, 18, 31 and checks the conjecture up to 10.
2. Orders 11-12: 1e9 and 1.65e11 graphs. Use geng -C (biconnected; the kappa = 1 MNH graphs are known analytically) with a PRUNE plugin enforcing d(u) + d(v) <= n - 1 for nonadjacent pairs on the partial graph (the constraint is hereditary in the sense that degrees only grow as geng adds vertices, so a violated pair stays violated; this needs care with geng's vertex-by-vertex extension, but nonadjacency and degree lower bounds are monotone). Edge floor 3n/2 and Delta not in {n-2, n-3} prune further. Order 12 is a cluster job (Goedgebeur's group did comparable geng sweeps at 12 for platypuses).
3. Alternative for 11-13 without geng on all graphs: split by 4.4/4.5. (a) MNH graphs with a universal vertex = K_1 join H with H MNT of order n - 1: generate MNT graphs of order n - 1 (for n = 12 that is all graphs on 11 vertices, 1e9, with a traceability filter; or a dedicated MNT generator, which does not exist in print as far as I found [U]). (b) MNH graphs with Delta <= n - 4 are platypuses: filter the House of Graphs platypus lists (complete to order 12; 24847 graphs at 12) for the MNH property. Together this classifies MNH graphs up to order 12 with a trivial amount of computation beyond the MNT step, and checks Hoa's conjecture on each. Extending to 13-14 requires either a full geng run at 13 (5e13, out of reach) or the girth-restricted platypus lists plus a structural argument for girth 3.
4. Orders 15-20: brute force impossible; a purpose-built canonical-augmentation generator for MNH graphs exploiting 4.1 (every nonadjacent pair tight), 4.2, 4.4, plus Moulton's figure-eight/theta spanning (which if proved would give a generation scheme from a theta skeleton plus chords) is the only route. Moulton's 2014 computation to order 20 shows such a scheme is possible in practice but the method is unpublished. [U]

**5.4 Hamiltonicity oracle.** For n <= 24 a backtracking search with degree-2 forcing suffices; for the MNH test the expensive part is the O(n^2) Hamilton-path queries per graph, but nonadjacent pairs number at most about n^2/2 - 3n/2 and each query on a sparse 12-vertex graph is microseconds. Sage (Zhan used SageMath), networkx, or a small C routine all work; no special solver needed below n = 30.

**5.5 Constructive search guided by Zhan's mechanism at orders below 56.** [D] Zhan's G = K_1 join M has order 3 + sum_i (|X_i| - 1) where X_i are the three MNH gadgets of Theorem 3.13. Define for an MNH gadget (X, x) with H = X - x noncomplete and x not universal: H must be traceable (homogeneously traceable for at least two gadgets); the middle deficiency d(X, x) = |H| - max over distinct neighbours p, q of x of the maximum order of a (p, q)-path in H; and the omitted set O(X, x) for a maximizing pair. Lemma 4's argument shows the detour of M has order 2 + sum |H_i| - min_i d_i, and the residual of K_1 join M for the cycle through the middle gadget i is the omitted set O_i, which is a counterexample iff O_i is not a clique and d_i = min_j d_j. Zhan's gadgets: (A_19, 19) with |H| = 18, d = 2; (A_18, 18) with |H| = 17, d = 2, O = {w_16, w_17} nonadjacent. Petersen with any vertex has |H| = 9 and d = 1 (a 9-vertex Hamilton path between two neighbours of x would close to a Hamilton cycle of P), so the Bullock Figure 14 graph (three Petersens, order 30 after the join) gives residual K_1, not a counterexample. The search: over all MNH graphs X of order <= 12 (from 5.3) and all non-universal vertices x, compute d(X, x) and O(X, x); any gadget with d >= 2 and a non-clique omitted set, combined with two gadgets of deficiency >= 2 satisfying conditions (iii)-(v), gives a counterexample of order 3 + sum (|X_i| - 1). If gadgets of order 10-12 exist with these properties, counterexamples of order around 30-36 follow; if none exist below some order, that is a lower bound for counterexamples of this specific type (not for all counterexamples). Mixed gadget sizes are allowed; the two end gadgets need only d >= d_middle, so the end gadgets could be smaller if their deficiency is at least that of the middle one.

**5.6 Other constructive routes to test.** [D] (a) Theorem 3.12 of Bullock et al. (the case N_{G_i}(x) != N_{G_i}(y)) gives a second family of toughness < 1 MNT graphs; joined with K_1 these may give residuals of a different shape, relevant to Question 3. (b) Zelinka Type I/II MNT graphs joined with K_1 give the kappa <= 2 MNH graphs of toughness <= 1 with small blocks; their detours are easy to analyze by hand. (c) The DKW construction (cubic MNH middle block with properties D(1), D(2), two cut-vertices) joined with K_1.

---

## 6. Candidate extension questions with attributable novelty

Q-A. **Least order of a counterexample.** Known: 8 <= n_0 <= 56 (this dossier: atlas check for n <= 7; Zhan for 56). Deliverables: (i) complete classification of MNH graphs for n <= 12 via 5.3, which also extends OEIS A185306 (marked "hard, more", stuck at n = 10 since 2013) by two or three terms; (ii) verification or refutation of Conjecture 1 on every MNH graph up to that order; (iii) the gadget search 5.5 for an explicit counterexample well below 56; (iv) if Moulton's 2014 data can be obtained, the answer up to 20 may already exist. Attribution: new computational result plus, if 5.5 succeeds, a new construction; no overlap with Zhan's paper, which makes no minimality claim.

Q-B. **Zhan's Question 2** (every component of G - V(C) complete?). The join mechanism reduces it, for MNH graphs with a universal vertex, to: does every connected MNT graph H have, for every detour P, all components of H - V(P) complete? Zhan's M has H - V(P) = 2K_1, consistent with a yes. A counterexample to Q2 of join type needs an MNT graph whose detour complement contains a non-clique component; the gadget search 5.5 tests this automatically (look for an omitted set that is connected and not a clique, which also answers Question 3 for the join type).

Q-C. **Zhan's Question 3** (connected, non-complete residual). Under Moulton's theta conjecture the residual is a chorded path segment, so a connected non-complete residual would be an induced path P_3 or longer, i.e. an MNH graph with a longest cycle missing three consecutive-in-a-path vertices. This suggests a targeted search among MNH graphs with circumference <= n - 3.

Q-D. **Zhan's Question 4** (f(n) = maximum number of components of G - V(C)). Known: f(n) >= 1 for n >= 4 (trivial, this dossier) and f(n) >= 2 for n >= 56 (Zhan). Open in both directions: is f(n) bounded? A natural upper bound attempt: a component count k of G - V(C) forces, via maximality, k pairwise nonadjacent "attachment" structures on C, each nonadjacent pair having degree sum <= n - 1 (4.1). No such bound is in the literature I found. A generalization of Theorem 3.13 to a k-cut with k + 1 components would be the constructive direction.

Q-E. **Toughness and circumference of counterexamples.** Every counterexample has toughness >= 1 (Hoa) and Zhan's have toughness exactly 1 and circumference n - 2. Questions: does a counterexample with toughness > 1 exist? With circumference <= n - 3? With no universal vertex (i.e. a platypus counterexample)? Zhan's graphs all have the universal vertex z; a platypus counterexample would be of a different type and is testable on the HoG platypus lists to order 12 (and girth-restricted lists to 24) with a few CPU-hours.

Q-F. **Attribution and record hygiene.** Read Problem 266 (Discrete Math. 164 (1997) 317-321) and Hoa 2005 pp. 67-70 to settle whether the conjecture is Hoa's or was attributed by Hoa to Erdos, and to record Hoa's exact hypotheses in the two partial theorems (toughness < 1; delta >= n/3). This is a prerequisite for any write-up that cites the conjecture.

Q-G. **Minimal MNH gadgets.** Independently of Hoa's conjecture, the quantities d(X, x) and O(X, x) of 5.5 (path deficiency between neighbours of a vertex in an MNH graph) are new invariants; tabulating them for all MNH graphs up to order 12 gives a reusable table for MNT constructions in the Bullock-Frick-Singleton framework.

---

## 7. Source table

| # | Source | How verified |
|---|---|---|
| 1 | X. Zhan, Counterexamples to a conjecture of Hoa on maximal non-Hamiltonian graphs, arXiv:2608.00957v3 (14 Aug 2026) | [V] full PDF read |
| 2 | V.D. Hoa, Problem 266, Research Problems (Second Krakow Conf.), Discrete Math. 164 (1997) 317-321, DOI 10.1016/S0012-365X(96)00067-2 | [V2] Crossref, zbMATH 1019078; text not read |
| 3 | V.D. Hoa, Longest cycles and restgraph in maximal nonhamiltonian graphs, in The Mathematical Foundation of Informatics, World Scientific 2005, 67-70, DOI 10.1142/9789812703118_0007 | [V2] Crossref, zbMATH 1602796, Semantic Scholar; text not read |
| 4 | F. Bullock, M. Frick, J. Singleton, S. van Aardt, C.M. Mynhardt, Maximal nontraceable graphs with toughness less than one, Electron. J. Combin. 15 (2008) R18, DOI 10.37236/742 | [V] PDF read (Thm 3.13, examples, references) |
| 5 | J.A. Bondy, Variations on the Hamiltonian theme, Canad. Math. Bull. 15 (1972) 57-62, DOI 10.4153/CMB-1972-012-3 | [V2] Crossref; content via Frick-Singleton and Clark-Entringer abstracts |
| 6 | J.A. Bondy, V. Chvatal, A method in graph theory, Discrete Math. 15 (1976) 111-135, DOI 10.1016/0012-365X(76)90078-9 | [V2] Crossref; theorem statement from lecture notes |
| 7 | L. Clark, R. Entringer, Smallest maximally nonhamiltonian graphs, Period. Math. Hungar. 14 (1983) 57-68, DOI 10.1007/BF02023582 | [V2] abstract summaries |
| 8 | L.H. Clark, R.C. Entringer, H.D. Shapiro, Smallest maximally nonhamiltonian graphs II, Graphs Combin. 8 (1992) 225-231, DOI 10.1007/BF02349959 | [V2] Crossref |
| 9 | X. Lin, W. Jiang, C. Zhang, Y. Yang, On smallest maximally nonhamiltonian graphs, Ars Combin. 45 (1997) 263-270 | [V2] zbMATH 1409195 review |
| 10 | J. Jamrozik, R. Kalinowski, Z. Skupien, A catalogue of small maximal nonhamiltonian graphs, Discrete Math. 39 (1982) 229-234, DOI 10.1016/0012-365X(82)90145-5 | [V2] Crossref, zbMATH 3754736; scope [U] |
| 11 | Z. Skupien, On maximal non-Hamiltonian graphs, Rostock. Math. Kolloq. 11 (1979) 97-106 | [V2] zbMATH 3689432 |
| 12 | L. Stacho, Graphs Combin. 12 (1996) 361-371; Ars Combin. 48 (1998) 307-317 | [V2] Crossref, zbMATH 1600936 |
| 13 | P.V. Roldugin, Discrete Math. Appl. 13 (2003) 277-289 | [V2] Crossref |
| 14 | M. Frick, J. Singleton, Lower bound for the size of maximal nontraceable graphs, EJC 12 (2005) R32, arXiv:math/0407292 | [V] PDF read |
| 15 | B. Zelinka, Discuss. Math. Graph Theory 18 (1998) 205-208, DOI 10.7151/dmgt.1076 | [V2] zbMATH review |
| 16 | J. Goedgebeur, A. Neyt, C.T. Zamfirescu, Structural and computational results on platypus graphs, Appl. Math. Comput. 386 (2020) 125491, arXiv:1712.05158 | [V] PDF read (Lemma 2, Cor. 12, Section 5, Table 1) |
| 17 | C.T. Zamfirescu, J. Graph Theory 86 (2017) 223-243, DOI 10.1002/jgt.22122 | [V2] via source 16 |
| 18 | D.P. Moulton, Maximal non-Hamiltonian graphs, Princeton Discrete Math Seminar abstract, 27 Feb 2014 | [V] abstract pages read; no paper found [U] |
| 19 | J. Jooken, Computer-assisted graph theory: a survey, arXiv:2508.20825 | [V] PDF read (geng section, Table 1) |
| 20 | B.D. McKay, Simple graphs data page, users.cecs.anu.edu.au/~bdm/data/graphs.html | [V] fetched |
| 21 | OEIS A185306, A000088, A001349 | [V] text format via curl |
| 22 | MathWorld, Maximally Nonhamiltonian Graph | [V] fetched |
| 23 | N.D. Tan, C. Iamjaroen, Discuss. Math. Graph Theory 28 (2008) 67-89, DOI 10.7151/dmgt.1392 | [V2] eudml abstract |
| 24 | F. Bullock, Detours in graphs (PhD thesis), arXiv:2507.12086 | [V2] arXiv abs |
| 25 | Local computation `atlas_mnh_check.py`, 2026-09-03 | [V] output recorded above |
