# Dossier: the Bougard-Joret conjecture and its 2026 disproof (Das-Gupta)

Date: 2026-09-02 (written 2026-09-03 local). Scout: Lucy. Program: mathematics scouting, new-problem search.

Marker legend. [V] = read in the primary source (full text extracted with pdftotext from the PDF, or the arXiv HTML alttext). [U] = known only from a search-engine or CrossRef summary; the primary text was not read. Every claim carries one marker and a citation.

Primary sources read in full (local copies under `src/` next to this file):

- P1. N. Bougard, G. Joret, "Turan's Theorem and k-Connected Graphs", J. Graph Theory 58 (2008), no. 1, 1-13, DOI 10.1002/jgt.20289. Author preprint read: https://gjoret.be/papers/turan.pdf (13 pp). CrossRef confirms the journal metadata (online 2008-01-07, print May 2008) [V].
- P2. J. Das, S. Gupta, "Counterexample to the Bougard-Joret Conjecture", arXiv:2608.18828v1 [math.CO], submitted 2026-08-19, 12 pp, 2 figures, MSC 05C35, 05C40, license CC BY-NC-SA 4.0, DOI 10.48550/arXiv.2608.18828. Read: https://arxiv.org/abs/2608.18828, https://arxiv.org/html/2608.18828, https://arxiv.org/pdf/2608.18828 [V].

Secondary sources (not read in full; cited through P2 or CrossRef):

- S1. T. Wang, B. Wu, "The size of graphs with given feedback vertex number", Discrete Appl. Math. 314 (2022) 213-222, DOI 10.1016/j.dam.2022.02.013 (CrossRef metadata confirmed; paywalled, no arXiv version found) [U].
- S2. L. Liu, B. Ning, "A spectral analogue of Ore's problem on Turan theorem", Linear Algebra Appl. 735 (2026) 112-122, DOI 10.1016/j.laa.2026.01.012 (CrossRef metadata confirmed; paywalled, no arXiv version found on the author's arXiv listing https://arxiv.org/a/ning_b_1) [U].
- S3. J. Christophe et al., "Linear inequalities among graph invariants: using GraPHedron to uncover optimal relationships", Networks 52 (2008) 287-298, DOI 10.1002/net.20250 [U].
- S4. I. Gitler, C. E. Valencia, "On bounds for some graph invariants", Bol. Soc. Mat. Mexicana (3) 16 (2010) 73-94, arXiv:math/0510387 [U].
- S5. L.-T. Yuan, "A note on Turan's theorem", Appl. Math. Comput. 361 (2019) 13-14, DOI 10.1016/j.amc.2019.05.020 [U].
- S6. F. Harary, "The maximum connectivity of a graph", Proc. Natl. Acad. Sci. USA 48 (1962) 1142-1146, DOI 10.1073/pnas.48.7.1142 [U].
- S7. S. Sra, "GPT, the Counterexample Machine", arXiv:2608.29595 (submitted 2026-08-30), repository https://github.com/suvrit/count-ex-machina. Fetched and scanned: it contains no graph-theory item and does not mention Bougard, Joret, or f(n, alpha, k) [V, scan of the HTML].
- OEIS A000088, A001349, A000055, A006290, A007112, A086216 (fetched as text from oeis.org) [V].

---

## 1. Definitions, the exact conjecture, and what Bougard-Joret proved

### 1.1 Definitions (P1, Section 1 and 2) [V]

- Graphs are finite and simple. alpha(G) is the stability (independence) number. ||G|| is the size (number of edges), |G| the order. K1 is treated as connected and 1-connected in P1.
- Turan graph in P1's convention: T(n, alpha) is the disjoint union of alpha balanced cliques (orders differ by at most one); t(n, alpha) = ||T(n, alpha)||. P2 writes the same quantity as t(n, alpha) = r*C(q+1, 2) + (alpha - r)*C(q, 2) where n = q*alpha + r, 0 <= r < alpha, and warns that this differs from the complete-multipartite convention [V, P2 eq. (2.1)].
- P1: "Given three positive integers n, alpha, k such that n >= alpha + k (or n >= 1 if alpha = k = 1), let f(n, alpha, k) denote the minimum size of a k-connected graph with order n and stability number alpha." A graph attaining it is (n, alpha, k)-extremal [V, P1 p. 2].
- P2 uses the same f and the same extremal notion, adds e(G), delta(G), kappa(G), the join G v H, the edgeless graph K_s-bar and the path P_s, and defines m(p, d) = minimum size of a d-connected graph of order p (no condition when d = 0) [V, P2 Section 2].
- P2 Proposition 2.1 (from Harary S6 for d >= 2; d = 0, 1 elementary): m(p, 0) = 0; m(p, 1) = p - 1; m(p, d) = ceil(pd/2) for 2 <= d <= p - 1. The d = 1 line is the exceptional one: ceil(p/2) = p - 1 only for p in {2, 3} [V].

### 1.2 What Bougard-Joret proved (P1) [V]

- Proposition 1 (Christophe et al. S3, Gitler-Valencia S4; short proof in P1 Prop. 5): f(n, alpha, 1) = t(n, alpha) + alpha - 1 for n >= alpha + 1. Extremal graphs: exactly the tree-linkings of a twisted T(n, alpha) (P1 Prop. 5(b); "twisted" replaces some K2 and one K3 components by odd cycles, only when 2*alpha < n < 3*alpha).
- Case n <= 2*alpha, k = 2: f = 2*alpha; extremal iff bipartite with 2*alpha edges (P1 Section 4, first paragraph).
- Proposition 6 (k = 2, n >= 2*alpha + 1): f(n, alpha, 2) = t(n, alpha) + alpha - 1 if alpha = 1 or n - 2*alpha = 1, and t(n, alpha) + alpha otherwise. Extremal graphs: cycle-linkings of a twisted T(n, alpha), odd subdivisions of K4, or the graph H obtained by pasting K4 onto K4 (Wessel pasting).
- Proposition 7 (improves Brouwer): a connected graph with n >= 3*alpha and ||G|| <= t(n, alpha) + ceil(n/alpha) + alpha - 4 has a partition of V into alpha cliques; bound best possible for alpha >= 2.
- Proposition 8: a 2-connected graph with n >= 3*alpha >= 9 and ||G|| <= t(n, alpha) + ceil(n/alpha) + alpha - 3 has a partition of V into alpha cliques; best possible.
- Section 6 (k >= 3), verbatim statements:
  - "It is not difficult to determine f(n, alpha, k) for k >= 3 when n <= 2*alpha: ... a k-connected graph G with order n and stability number alpha is k-extremal if and only if it is bipartite and ||G|| = k*alpha." So f(n, alpha, k) = k*alpha for n <= 2*alpha [V, P1 p. 11].
  - "If 2*alpha <= n <= k*alpha, then f(n, alpha, k) >= ceil(nk/2), as every vertex of a k-connected graph has degree at least k. If n >= k*alpha, we have f(n, alpha, k) <= t(n, alpha) + ceil(k*alpha/2), since the graph T(n, alpha) can be made k-connected by the adjunction of ceil(k*alpha/2) edges without decreasing its stability number. We are tempted to believe that these two bounds are actually the exact value of f(n, alpha, k)." [V, P1 p. 11]

### 1.3 The exact conjecture (P1, Conjecture 1, Section 6, pp. 11-12) [V]

> Conjecture 1. Let n, alpha, k be three positive integers such that n >= 2*alpha, n >= alpha + k, alpha >= 2 and k >= 3. Then
> f(n, alpha, k) = ceil(nk/2) if n <= k*alpha, and f(n, alpha, k) = t(n, alpha) + ceil(k*alpha/2) otherwise.

P2 reproduces it verbatim as (1.1)-(1.2) and confirms the location "Conjecture 1 in Section 6 of [1, pp. 11-12]" [V, P2 p. 2].

Regime vocabulary used below: Regime A (first line) = alpha + k <= n <= k*alpha with n >= 2*alpha. Regime B (second line) = n > k*alpha.

### 1.4 Cases of the conjecture proven in P1 (Section 6) [V]

- n = k*alpha: both bounds coincide (t(k*alpha, alpha) + ceil(k*alpha/2) = ceil(nk/2)), so f is known there and the conjecture holds. P1: "for n = k*alpha, we have f(n, alpha, k) = t(n, alpha) + ceil(k*alpha/2) = ceil(nk/2)". P2 phrases this as "established (1.2) on the boundary n = k*alpha" [V].
- alpha >= 3 and n >= ceil((k-2)*alpha/2)*alpha + 2*alpha: true, via Proposition 8 (a hypothetical extremal graph with at most t + ceil(k*alpha/2) - 1 <= t + ceil(n/alpha) + alpha - 3 edges would have a clique partition, and a k-connected graph with a partition into alpha cliques has at least t(n, alpha) + ceil(k*alpha/2) edges). The pdftotext rendering of P1 loses the ceiling and alpha symbols in this bound; the form above is the one printed in P2's HTML alttext ("n >= ceil((k-2) alpha / 2) alpha + 2 alpha") and is the algebraic consequence of Proposition 8's hypothesis (ceil(n/alpha) >= ceil(k alpha/2) - alpha + 2) [V for P2's rendering; the P1 symbols are inferred].
- alpha = 2 and n >= 2k: true. n >= 2k + 2 via Proposition 7; n = 2k is the n = k*alpha boundary; n = 2k + 1 by a direct Brooks-theorem argument in P1 (an extremal graph has a vertex of degree >= k + 1; both the alpha-critical and the non-alpha-critical cases give ||G|| >= t(2k+1, 2) + k) [V, P1 p. 12].
- P1 also notes: the conjecture "generalizes the 2-connected case when n >= 2*alpha + 2" [V].

Consequently, before P2, Regime A was open for every triple with alpha + k <= n < k*alpha other than what follows from n <= 2*alpha, and Regime B was open for alpha >= 3 with k*alpha < n < ceil((k-2)*alpha/2)*alpha + 2*alpha. Later literature: S1 recorded the k >= 3 conjecture as "still unsettled" (Section 1) and S2 restated it as Conjecture 3.1 and called it "still wide open" (Section 3, p. 121); both quotations are taken from P2 p. 2 [V for the quotation in P2; U for S1/S2 themselves]. P2: "We are not aware of an earlier counterexample." [V]

---

## 2. What Das-Gupta prove (P2) [V throughout]

### 2.1 Main theorem: the boundary n = alpha + k

On n = alpha + k, hypotheses (1.1) reduce to alpha >= 2, k >= 3, k >= alpha, and every such triple is in Regime A (n <= k*alpha automatically since alpha >= 2, k >= 3) [V, P2 Section 3, first paragraph].

Theorem 3.1. Let alpha >= 2, k >= 3, k >= alpha. Then f(alpha + k, alpha, k) = alpha*k + m(k, k - alpha). Equivalently, with d = k - alpha:
- f = k^2 if alpha = k (d = 0);
- f = k^2 - 1 if alpha = k - 1 (d = 1);
- f = ceil(k(alpha + k)/2) if 2 <= alpha <= k - 2 (d >= 2).

Proof mechanism (P2 pp. 3-5): pick a maximum independent set S, |S| = alpha, T = V \ S, |T| = k. Every s in S has degree >= k and all its neighbours lie in T, so N(s) = T; hence G = K_alpha-bar v H with H = G[T] and e(G) = alpha*k + e(H). Deleting S together with any X subset T, |X| < d, deletes fewer than k vertices, so H - X is connected: H is d-connected, giving e(H) >= m(k, d). Construction: G0 = K_alpha-bar v H_d with H_0 = K_k-bar, H_1 = P_k, H_d any d-connected graph of order k and size m(k, d) (Harary). alpha(G0) = max(alpha, alpha(H_d)) = alpha in each case (for d >= 2, an independent set of size alpha + 1 in H_d would force a vertex of degree <= d - 1). k-connectivity of G0 is checked directly.

The stated source of the failure (P2 p. 2): "On the boundary n = alpha + k ... Deleting a maximum independent set leaves exactly k vertices. When alpha = k - 1, those vertices must induce a connected graph. That residual connectivity costs k - 1 edges, whereas the degree-sum estimate for a one-connected graph accounts for only ceil(k/2) edges."

### 2.2 Extremal characterization on the boundary

Corollary 3.2. With alpha >= 2, k >= 3, k >= alpha, d = k - alpha: a k-connected graph G of order alpha + k and independence number alpha is extremal iff G = K_alpha-bar v H where H has order k and (i) d = 0: H = K_k-bar (so G = K_{k,k}); (ii) d = 1: H is a tree; (iii) d >= 2: H is d-connected with e(H) = ceil(kd/2). Necessity is the lower-bound argument plus e(H) = m(k, d); sufficiency "follows exactly the same way as Theorem 3.1" (the authors skip it) [V, P2 pp. 5-6].

### 2.3 The counterexample family

Corollary 3.3. For every k >= 4, f(2k - 1, k - 1, k) = k^2 - 1, and the extremal graphs are precisely K_{k-1}-bar v T with T any tree of order k. The triple is admissible (n = 2k - 1 >= 2*alpha = 2k - 2, alpha = k - 1 >= 3) and lies in Regime A since k*alpha - n = (k-1)(k-2) - 1 > 0 for k >= 4. The conjecture predicts ceil(k(2k-1)/2) = k^2 - floor(k/2); the gap is floor(k/2) - 1 >= 1 for k >= 4 [V, P2 pp. 6-7]. For k = 3 (triple (5, 2, 3)) the gap is 0 and there is no failure; in fact d = 1 with k = 3 gives m(3, 1) = 2 = ceil(3/2).

Consequence stated in P2 (Section 1): "(1.2) is correct on n = alpha + k except precisely when k - alpha = 1 and k >= 4."

### 2.4 Smallest failure and order-minimality

Proposition 4.1. Among admissible triples, the minimum order of a counterexample is seven: f(7, 3, 4) = 15 while (1.2) predicts 14. Extremal graphs: K_3-bar v T with T a tree of order 4 (P2 gives K_3-bar v P4 as the example). Direct explanation why 14 is impossible: a 4-connected graph on 7 vertices with 14 edges is 4-regular, its complement is 2-regular; alpha = 3 forces a triangle component in the complement, so the complement is C3 + C4 and deleting the three C3 vertices leaves C4-bar = 2K2, disconnected [V, P2 pp. 8-9]. Admissible triples of order <= 6 are exactly (5,2,3), (6,2,3), (6,2,4), (6,3,3), all in Regime A, and each attains ceil(nk/2): K5 minus a 2-matching (8 edges), the triangular prism (9), K6 minus a perfect matching (12), K_{3,3} (9) [V, P2 pp. 9-10].

### 2.5 Every explicit remark and open direction in P2 [V]

- Proposition 4.2 (recorded, not new): if alpha >= 2, G is k-connected of order n and V(G) has a partition into alpha nonempty cliques, then e(G) >= t(n, alpha) + ceil(k*alpha/2). P2 stresses "it does not imply that every extremal graph has the required partition."
- "The general second regime remains a separate question: a proof must either establish the partition or obtain (4.3) without it."
- "The counterfamily above shows that the first regime requires revision before a unified statement can be true. The boundary n = alpha + k is completely determined by (3.2), and Corollary 3.2 determines every equality case there. Any corrected conjecture must therefore include the exceptional value k^2 - 1 and the extremal family K_{k-1}-bar v T when alpha = k - 1."
- No corrected conjecture is proposed. No result is claimed for n = alpha + k + 1 or for any interior point of Regime A. No computer search is mentioned; "Data availability: ... no datasets were generated or analyzed".
- AI declaration (verbatim scope): "the authors used AI to discuss proof strategies, organize and check bibliographic information, check algebraic calculations and proof exposition, and improve language and readability", with the authors taking full responsibility.
- Affiliations: Das at SRM Institute of Science and Technology, Chennai; Gupta at NISER Bhubaneswar.

---

## 3. Known exact values of f(n, alpha, k) and open ranges

No table of numerical values exists in P1 or P2; both give closed forms. Assembled state of knowledge (all [V] unless marked):

| Range | Value | Source |
|---|---|---|
| k = 1, n >= alpha + 1 | t(n, alpha) + alpha - 1 | S3, S4, P1 Prop. 5 |
| k = 2, n <= 2*alpha | 2*alpha | P1 Section 4 |
| k = 2, n >= 2*alpha + 1 | t + alpha - 1 if alpha = 1 or n = 2*alpha + 1; else t + alpha | P1 Prop. 6 |
| k >= 3, n <= 2*alpha (needs n >= alpha + k) | k*alpha (extremal iff bipartite with k*alpha edges) | P1 Section 6 |
| k >= 3, n = k*alpha | ceil(nk/2) | P1 Section 6 |
| k >= 3, alpha = 2, n >= 2k | t(n, 2) + k (= C(ceil(n/2),2) + C(floor(n/2),2) + k) | P1 Section 6 |
| k >= 3, alpha >= 3, n >= ceil((k-2)alpha/2)alpha + 2alpha | t(n, alpha) + ceil(k*alpha/2) | P1 Section 6 via Prop. 8 |
| k >= 3, n = alpha + k, alpha <= k | alpha*k + m(k, k - alpha) (three-case formula of 2.1) | P2 Thm 3.1 |
| (2k - 1, k - 1, k), k >= 4 | k^2 - 1 (conjecture said k^2 - floor(k/2)) | P2 Cor. 3.3 |

Open after P2 (Regime A interior): alpha + k < n < k*alpha with n >= 2*alpha, alpha >= 2, k >= 3. For alpha = 2 this is k + 3 <= n <= 2k - 1. Open (Regime B): alpha >= 3 and k*alpha < n < ceil((k-2)*alpha/2)*alpha + 2*alpha; for k = 3 this is 3*alpha < n < ceil(alpha/2)*alpha + 2*alpha. Nothing in the literature read here settles any interior point of Regime A beyond the order <= 6 list in P2.

---

## 4. Has anyone computed f(n, alpha, k) by computer? Plus this scout's own computation

### 4.1 Literature search result

- No published table of f(n, alpha, k) for k >= 3 was found. Searches run (2026-09-03): "minimum number of edges k-connected graph independence number", "Bougard Joret conjecture", "House of Graphs / GraPHedron k-connected independence number minimum edges", "computer search k-connected independence number nauty geng", author names. Only P2 and P1 surface; P2 itself states no dataset was generated [V].
- S3 (Christophe et al.) is the GraPHedron paper: a polyhedral system that computes optimal linear inequalities among invariants from exhaustive small-order data; the search summary says it obtained the optimal inequalities between stability number and number of edges (this is the k = 1 case that P1 calls Ore's problem) [U]. It is the only computer-assisted antecedent found, and it concerns connectivity 1.
- AI-assisted work: P2's authors declare AI use for proof strategy discussion and checking (Section 2.5 above) [V]. S7 (Sra, "GPT, the Counterexample Machine", 2026-08-30) lists no graph-theory counterexample and does not mention this problem [V, scan]. No AlphaEvolve/LLM-search record of f(n, alpha, k) was found [U, absence in searches].

### 4.2 Own computation (this dossier; scripts in `src/`, reproducible)

Two independent methods, both on E:\_Temp, Python 3.13, `python-sat` in `.venv-scout`:

- `src/bruteforce_f.py`: exhaustive labeled enumeration for n <= 7 (2^21 graphs, 29 s at n = 7), computing alpha and kappa by bitmask brute force.
- `src/sat_f.py`: for each (n, alpha, k) and m from ceil(nk/2) upward, a CaDiCaL 1.5.3 model with edge variables, S = {0..alpha-1} fixed independent (WLOG), one clause per (alpha+1)-subset forbidding a larger independent set, sequential-counter degree >= k, totalizer e(G) <= m, and k-connectivity enforced lazily (each non-k-connected model yields a separator X, |X| < k, and a component C of G - X, and the sound clause "some edge between C and V \ (X u C)" is added). f is the least satisfiable m; the satisfying graph is a certificate for the upper bound; the UNSAT answer at m = f - 1 is the solver's word (no DRAT proof emitted in this pass).
- Cross-check: the two methods agree on every triple at n = 5, 6, 7, and every value at n <= 6 matches P2 Prop. 4.1. `src/sat_extremal_count.py` enumerates all labeled extremal graphs with S fixed and groups them by degree sequence.

Results (admissible triples only; "conj" = value of Conjecture 1; outputs in `src/sat_out_*.txt`):

| n | alpha | k | f | conj | note |
|---|---|---|---|---|---|
| 5 | 2 | 3 | 8 | 8 | boundary, d = 1, k = 3 (no gap) |
| 6 | 2 | 3 | 9 | 9 | |
| 6 | 2 | 4 | 12 | 12 | boundary, d = 2 |
| 6 | 3 | 3 | 9 | 9 | boundary, d = 0 (K_{3,3}) |
| 7 | 2 | 3 | 12 | 12 | Regime B |
| 7 | 2 | 4 | 14 | 14 | |
| 7 | 2 | 5 | 18 | 18 | boundary, d = 3 |
| 7 | 3 | 3 | 11 | 11 | |
| 7 | 3 | 4 | 15 | 14 | FAILS (P2 Prop. 4.1 reproduced) |
| 8 | 2 | 3 | 15 | 15 | Regime B |
| 8 | 2 | 4 | 16 | 16 | |
| 8 | 2 | 5 | 20 | 20 | |
| 8 | 2 | 6 | 24 | 24 | boundary, d = 4 |
| 8 | 3 | 3 | 12 | 12 | |
| 8 | 3 | 4 | 16 | 16 | n = alpha + k + 1 with alpha = k - 1: no failure |
| 8 | 3 | 5 | 20 | 20 | boundary, d = 2 |
| 8 | 4 | 3 | 12 | 12 | |
| 8 | 4 | 4 | 16 | 16 | boundary, d = 0 (K_{4,4}) |
| 9 | 2 | 3 | 19 | 19 | Regime B |
| 9 | 2 | 4 | 20 | 20 | Regime B |
| 9 | 2 | 5 | 23 | 23 | |
| 9 | 2 | 6 | 27 | 27 | |
| 9 | 2 | 7 | 32 | 32 | boundary, d = 5 |
| 9 | 3 | 3 | 14 | 14 | |
| 9 | 3 | 4 | 18 | 18 | |
| 9 | 3 | 5 | 23 | 23 | |
| 9 | 3 | 6 | 27 | 27 | boundary, d = 3 |
| 9 | 4 | 3 | 14 | 14 | |
| 9 | 4 | 4 | 18 | 18 | |
| 9 | 4 | 5 | 24 | 23 | FAILS (P2 Cor. 3.3, k = 5) |
| 10 | 2 | 3 | 23 | 23 | Regime B |
| 10 | 2 | 4 | 24 | 24 | Regime B |
| 10 | 2 | 5 | 25 | 25 | n = k*alpha |
| 10 | 2 | 6 | 30 | 30 | |
| 10 | 2 | 7 | 35 | 35 | |
| 10 | 2 | 8 | 40 | 40 | boundary, d = 6 |
| 10 | 3 | 3 | 17 | 17 | Regime B, inside the open gap 9 < n < 12 for (alpha, k) = (3, 3); 53 s, 1319 cuts |
| 10 | 3 | 4 | 20 | 20 | |
| 10 | 3 | 5 | 25 | 25 | |
| 10 | 3 | 6 | 30 | 30 | n = alpha + k + 1 |
| 10 | 3 | 7 | 35 | 35 | boundary, d = 4 |
| 10 | 4 | 3 | 15 | 15 | |
| 10 | 4 | 4 | 20 | 20 | |
| 10 | 4 | 5 | 25 | 25 | n = alpha + k + 1 with alpha = k - 1: no failure (k = 5) |
| 10 | 4 | 6 | 30 | 30 | boundary, d = 2 |
| 10 | 5 | 3 | 15 | 15 | |
| 10 | 5 | 4 | 20 | 20 | |
| 10 | 5 | 5 | 25 | 25 | boundary, d = 0 (K_{5,5}) |
| 11, 12 | * | * | PENDING | | see `src/sat_out_11_12.txt` |

Extremal-class counts on the boundary (labeled, S fixed; classes by degree sequence, which separates these families):
- (7,3,4), m = 15: 16 labeled = 4^2 labeled trees on 4 vertices (Cayley); 2 degree sequences = {P4, K_{1,3}} = the 2 trees of order 4. Matches P2 Cor. 3.3.
- (9,4,5), m = 24: 125 = 5^3 labeled trees; 3 classes = the 3 trees of order 5 (OEIS A000055: 1,1,1,1,2,3,6,11,23 for n = 0..8). Matches.
- (8,3,5), m = 20 (d = 2): 12 labeled = the 12 labeled 5-cycles; H = C5 is the unique 2-connected graph with 5 vertices and ceil(10/2) = 5 edges. One class.
- (8,4,4), m = 16 (d = 0): 1 labeled graph, K_{4,4}. One class.
- (9,3,6), m = 27 (d = 3): 70 labeled = 60 (prism, 6!/12) + 10 (K_{3,3}, 6!/72): the two cubic graphs on 6 vertices. Two classes, both 3-connected, both allowed by Cor. 3.2(iii).

Timings: every Regime A triple with n <= 10 solves in < 0.1 s; Regime B triples need thousands of lazy cuts (f(10,2,4): 4885 cuts, 5.6 s) because minimum-degree-k graphs with few edges are abundant and mostly not k-connected.

---

## 5. Feasibility of exact computation for n <= 12 (and a bit beyond)

### 5.1 Search sizes (OEIS, [V])

Unlabeled graphs (A000088) / connected (A001349) / connected with minimum degree >= 3 (A007112, offset 1) / 3-connected (A006290, offset 4) / 4-connected (A086216, offset 1):

| n | all | connected | conn. mindeg >= 3 | 3-connected | 4-connected |
|---|---|---|---|---|---|
| 7 | 1,044 | 853 | 150 | 136 | 25 |
| 8 | 12,346 | 11,117 | 2,589 | 2,388 | 384 |
| 9 | 274,668 | 261,080 | 84,242 | 80,890 | 14,480 |
| 10 | 12,005,168 | 11,716,571 | 5,203,110 | 5,114,079 | 1,211,735 |
| 11 | 1,018,997,864 | 1,006,700,565 | 577,076,528 | 573,273,505 | 184,649,399 |
| 12 | 165,091,172,592 | 164,059,830,476 | 113,373,005,661 | 113,095,167,034 | 47,952,362,294 |

Labeled counts for brute force: 2^C(n,2) = 2^28 (n = 8), 2^36 (n = 9), 2^45 (n = 10): pure-Python brute force stops at n = 7 (done above).

### 5.2 Enumeration route (nauty geng)

- geng generates unlabeled graphs at roughly 10^6 to 10^7 per second per core [U, folklore figure; measure locally before planning]. A full `geng -c -d3 12` (1.1e11 graphs) is a multi-core-day job before filtering, so full enumeration at n = 12 is impractical; n <= 10 (5.2e6 graphs with `-d3`) is minutes.
- The decisive pruning is by edge count: to decide f(n, alpha, k) <= m0 one only needs `geng -c -d{k} n 0:m0` where m0 = conjectured (or target) value. Near ceil(nk/2) edges with minimum degree k the graphs are nearly k-regular and few (e.g. (12,5,7): 7-regular graphs on 12 vertices at 42 edges). geng's `-d` and edge bounds prune the orderly generation itself, so the counts of emitted graphs, not the totals above, govern the cost. For Regime A triples at n = 11, 12 this is expected to be seconds to minutes per triple; for Regime B with k = 3 the edge bound is t(n, alpha) + ceil(3 alpha/2), well above 3n/2, and the emitted set is larger (still far below A007112) [U, estimate].
- Post-filter per graph: alpha by branch-and-bound (n <= 12 trivial), kappa by Even's algorithm or by testing all C(n, k-1) deletions. Cost negligible relative to generation.
- Certificate value: the enumeration is reproducible and geng counts can be cross-checked against OEIS (the table above); there is no independent proof object, only trust in geng plus the filter code. Suitable as the "exhaustive check" half of a small-parameter table.
- Practical blocker on this machine: no gcc in PATH (MSVC 2022 is installed; nauty's configure expects a POSIX toolchain, so use WSL, MSYS2 gcc, or a Linux box such as the Hetzner VPS). nauty 2.8.9 source is already downloaded to `src/nauty.tar.gz`.

### 5.3 SAT / ILP route with certificates

- The `sat_f.py` model above scales to n ~ 14-16 for Regime A triples (instances are tiny: C(n,2) edge variables, C(n, alpha+1) independence clauses, e.g. 924 for (12, 5, *)). Regime B and small k need many lazy cuts; a Menger-style full encoding (k internally disjoint paths between each pair, or a flow encoding) removes the lazy loop at the price of O(k n^3) variables, still fine at n = 12.
- Certificates: upper bound = explicit graph (verify alpha, kappa, e independently). Lower bound = DRAT/LRAT proof from CaDiCaL for the CNF (base clauses + the lazily added cut clauses, each of which is a one-line lemma: "in a k-connected graph, for |X| < k and a proper nonempty C subset V \ X, some edge leaves C"). Checked with drat-trim/cake_lpr. This gives a fully checkable table.
- ILP (HiGHS via scipy.optimize.milp, already installed in the CAOS_MANAGE venv) can minimize e(G) directly with lazy connectivity cuts, but ILP optimality proofs are not independently checkable; keep SAT for the certificate and ILP only as a cross-check.
- Symmetry: fixing S = {0..alpha-1} is the main reduction; further breaking (lexicographic ordering of degrees within S and within T) would speed Regime B.
- Estimated budget: full table for all admissible triples with n <= 12 (n = 12 has alpha in {2..6}, k in {3..n-alpha}: 5+6+... ~ 30 triples) on a single machine: under one hour with the current script for Regime A; Regime B triples at n = 12, k = 3 may need minutes each with lazy cuts (extrapolating 2.4 s at n = 10 to a factor of ~50-100 per two extra vertices) [U, extrapolation]. n = 13, 14 in Regime A: still feasible; Regime B at k = 3 becomes the bottleneck and would benefit from the geng route with an edge bound.

---

## 6. Candidate extension questions (attributable novelty)

Each item states what is known (with source) and what would be new.

Q1. Corrected conjecture for Regime A. Data (this dossier, n <= 10 so far; n = 11, 12 pending): the only failures of ceil(nk/2) among admissible triples are the boundary points (2k - 1, k - 1, k), k >= 4 (P2). Candidate statement: for n >= 2 alpha, alpha + k <= n <= k alpha, alpha >= 2, k >= 3, f(n, alpha, k) = ceil(nk/2) unless n = alpha + k and alpha = k - 1 >= 3, where f = k^2 - 1. Novelty: P2 explicitly declines to state a corrected conjecture ("requires revision before a unified statement can be true"). Evidence needed: the n <= 12 table plus a structural argument that for n >= alpha + k + 1 the deleted-independent-set argument no longer forces connectivity of the residual graph. Note (8,3,4) = 16 and (9,3,5) = 23, (9,4,4) = 18 already show that one extra vertex kills the obstruction for k = 4, 5.

Q2. Next boundary n = alpha + k + 1. Structure: with S maximum independent, |T| = k + 1, every s in S misses at most one vertex of T. Determine f(alpha + k + 1, alpha, k) exactly and characterize extremal graphs (P2 covers only n = alpha + k). Conjecturally ceil(nk/2) throughout (data: (7,2,4), (8,2,5), (8,3,4), (9,2,6), (9,3,5), (9,4,4), (10,2,7) all equal ceil(nk/2)). A proof would be a genuine Regime A interior result; none exists.

Q3. Extremal graphs at n = alpha + k + 1 and beyond. Are they still joins K_alpha-bar v H, or do "almost-joins" (each s misses one vertex of T) appear as equality cases? The SAT enumerator with blocking clauses answers this for n <= 10 immediately; the classification is new.

Q4. Regime B gap for alpha >= 3: k alpha < n < ceil((k-2) alpha/2) alpha + 2 alpha. P2 says a proof "must either establish the partition or obtain (4.3) without it". Smallest open instances: k = 3, alpha = 3: 9 < n < 12, i.e. n = 10, 11 (f(10,3,3) pending in this run; conjecture 17); k = 3, alpha = 4: 12 < n < 16. A computed table for these is new and either supports the second line or produces a second counterexample family.

Q5. Small-parameter table with certificates. Nobody has published f(n, alpha, k) for k >= 3 numerically (Section 4.1). A DRAT-certified table for n <= 12 (or 14), with all extremal isomorphism classes (nauty canonical forms), plus the geng cross-check, is a self-contained, citable artifact; House of Graphs upload of the extremal graphs is the natural distribution channel.

Q6. Boundary generalization. Theorem 3.1 reads f(alpha + k, alpha, k) = alpha k + m(k, k - alpha). For n = alpha + k + j the analogous reduction is to a graph H on k + j vertices with a prescribed "deficiency" pattern; find the right m-type function whose exceptional line (d = 1, the tree case) explains all failures, and check whether any other (d, j) has an exceptional line. This is the conceptual version of Q1.

Q7. Alpha-critical/Brooks route for the interior. P1's tools (alpha-critical edges, Wessel pasting, Brooks' theorem) proved k = 2 and the alpha = 2 case; whether they give f(n, 2, k) for k + 3 <= n <= 2k - 1 (the only open alpha = 2 range) is untested in print. Data: all alpha = 2 values up to n = 10 equal ceil(nk/2).

---

## Files

- This dossier: `E:\_Temp\caos-research-newproblem\program\scouting-2026-09\2026-09-02-dossier-bougard-joret.md`
- Sources: `src/bougard-joret-turan.pdf` + `src/bougard-joret.txt`; `src/das-gupta-2608.18828.{pdf,html}` + `src/das-gupta.txt`, `src/das-gupta-html.txt`
- Scripts and outputs: `src/bruteforce_f.py`, `src/bruteforce_out.txt`, `src/sat_f.py`, `src/sat_out_7_8.txt`, `src/sat_out_9_10.txt`, `src/sat_out_11_12.txt`, `src/sat_extremal_count.py`, `src/sat_extremal_out.txt`
- Environment: `.venv-scout` (python-sat 1.9.dev15, CaDiCaL 1.5.3 backend), `src/nauty.tar.gz` (nauty 2.8.9 source, not built: no gcc on this machine)
