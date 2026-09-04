# Dossier: sweep of AI-linked and computer-found disproofs, 2026-07-01 to 2026-09-03

Written 2026-09-03 (session date 2026-09-02). Purpose: shortlist the next problem for the
certified-minimality / family / mechanism programme, scored with `program/counterexample-radar.md`.
Every claim carries a URL. Marks: `[V]` read from the primary source (arXiv abstract/HTML, GitHub
PR, Zenodo) in this sweep; `[S]` taken from an automated reading of the primary source and not yet
checked against the PDF; `[U]` unverified (search-engine or secondary summary only).

Excluded by ownership (other sessions): Jacobian conjecture and every Jacobian-derived item
(Gaussian moments, generalized vanishing conjecture, Mathieu, xz-conjecture, Hessian conjecture,
separable Jacobian, weak Markus-Yamabe), Huneke-Wiegand, rigid ideals. They are listed in section 5
only so the exclusion is auditable.

Round-1 leads already dossiered elsewhere in this folder (`2026-09-02-sweep-round-1.md`): Han's
conjecture (L1), AB rings localization (L2), Bougard-Joret (L3), Hoa (L4), Erman-Sam (L5), Sra's
count-ex-machina (L6). They are re-scored here in the same table for a single ranking.

## 1. Sources swept

- Index: https://aimath.robertj1.com/ read 2026-09-03; entries 2026-07-19 to 2026-08-14 extracted
  `[V]`. The page exposes filters and no permalinks or feed. Entries typed disproof in the window:
  purely-prime ideals (08-14), generalized vanishing (08-07, excluded), Babai minimal Cayley (08-06),
  inverse generator (08-06), Schiffer/Pompeiu (08-05), HRT (08-05), Connes rigidity (08-01), Carlson
  depth (07-26), rank-two Poisson (07-23), Dere real forms (07-21), Kourovka 19.25 / 21.147 / 21.150
  (07-20), Kourovka 21.142 (07-30, "blocking debts"). The index has NO entry for a group scheme of
  order 4 or for Deligne/Mumford `[V]`; that item lives on the Xena blog and in mathlib (section 2.6).
- arXiv monthly listings scanned by title for counterexample / disproof / refute / fails / Kourovka:
  math.GR 2026-07, 2026-08, 2026-09; math.AC 2026-07, 2026-08, 2026-09; math.RA 2026-07, 2026-08,
  2026-09; math.AG 2026-07, 2026-08; math.NT 2026-07, 2026-08; math.CO 2026-07 (partial: the listing
  fetch returned the first page only), 2026-08 (first page only), 2026-09. Listing URLs of the form
  https://arxiv.org/list/math.CO/2026-08. The math.CO August listing is large and only the first
  block was scanned by the fetcher; the WebSearch pass added the August math.CO items below. A
  full title scan of math.CO August remains a gap `[U]`.
- Secondary: Xena blog 2026-07-20
  https://xenaproject.wordpress.com/2026/07/20/human-mathematicians-are-being-outcounterexampled/
  `[V]`; Sra, "GPT, the Counterexample Machine", https://arxiv.org/abs/2608.29595 `[V]`.

## 2. Items named in the brief (index entries), one block each

### 2.1 Carlson's associated-prime depth conjecture (index 2026-07-26)

- Primary: Dai, Deng, Shi, Wu, Yang, "An Exact Counterexample to Carlson's Associated-Prime Depth
  Conjecture from a Group of Order 128", https://arxiv.org/abs/2607.23732 (math.GR, cs.AI), HTML
  https://arxiv.org/html/2607.23732 `[V]`.
- Statement disproved: Carlson 1995 Question 3.1, whether the depth of H*(G;k) (k of characteristic
  p dividing |G|) is always realized as the dimension of one of its associated primes `[V]`.
- Object: G = SmallGroup(128,859), structure (C4 x C4):(C4 x C2), k = F_2, Krull dimension 4,
  depth 2, Duflot bound 1; every rank-two elementary abelian subgroup (75 of them) has a centralizer
  of cohomological depth >= 3, so no associated prime of dimension 2 exists `[V]`.
- Verification: exact arithmetic over F_2; colon-ideal certificates (I:f1) = I and
  ((I+(f1)):f2) = I+(f1), a socle witness w with 13 generator-multiplication tests; two exceptional
  centralizers SmallGroup(64,90) and SmallGroup(64,216) get explicit regular-sequence certificates;
  the other four centralizer types satisfy the Duflot bound (center rank >= 3). Cohomology
  presentations come from the Green-King catalogue of order-128 groups. Ancillary files ship
  certificate checkers `[S]`. Tools named only implicitly (GAP-style enumeration, Groebner
  reductions); the exact software list must be read from the PDF `[U]`.
- AI: "initially identified by the TARS agent system"; the certificates were independently verified
  by X. Dai `[V]`.
- Explicit follow-ups: none stated. The paper does NOT claim minimality; it reports a negative
  control (SmallGroup(128,858)) and no sweep of order 64 or of the other 2327 groups of order 128 `[S]`.
- Radar note: order 64 has 267 groups and order 128 has 2328; Green and King published the mod-2
  cohomology rings of all of them (UNVERIFIED that the data is downloadable in a machine-readable
  form today; citation to check: Green and King, "The computation of the cohomology rings of all
  groups of order 128", J. Algebra 2011, https://doi.org/10.1016/j.jalgebra.2010.08.016 `[U]`).

### 2.2 Dere's real-form conjecture (index 2026-07-21)

- Primary: Borovoi, de Graaf, Guralnick, "Constructing a complex Lie algebra isomorphic to its
  complex conjugate but not definable over reals", https://arxiv.org/abs/2607.19513 (math.RA,
  math.RT), HTML https://arxiv.org/html/2607.19513 `[V]`.
- Statement: Dere (2019) conjectured that a complex Lie algebra isomorphic to its complex conjugate
  is definable over R. Demarche (2026) disproved it non-constructively in dimension 10; this paper
  gives an explicit example `[V]`.
- Object: a 10-dimensional two-step nilpotent Lie algebra of type (6,4), given by a tensor in
  (Lambda^2 V10*) tensor V10 with explicit structure constants involving i; equivalently
  L = V6 + (Lambda^2 V6)/F with F an 11-dimensional subspace `[S]`.
- Verification: Galois-cohomology criterion (a real form exists iff some g in GL(V) satisfies
  gamma(g F) = g F); stabilizer computation of the Pfaffian cubic in four variables via Magma
  Groebner bases; the obstruction is lambda * conj(lambda) = -1 `[S]`.
- Minimality: 10 is minimal among two-step nilpotent algebras (dims <= 8 have {0,1} structure
  constants, Galitski-Timashev 1999; dim 9 two-step checked by de Graaf by computer). No claim of
  global minimality `[S]`.
- AI: Claude (called "Claude Fable" in the abstract) supplied the idea of passing from a nonlinear
  stabilizer condition to linear necessary conditions; the authors re-derived everything `[V]`.
- Open follow-ups stated: dimension 9 in general, non-nilpotent, three-step nilpotent `[S]`.
- Index caption "Explicit minimal-dimensional counterexample" overstates the paper (minimal only
  within two-step nilpotent) `[V]`.

### 2.3 Babai's minimal Cayley graph problem (index 2026-08-06)

- Primary: Davies, Hatzel, Yepremyan, "Minimal Cayley graphs with large chromatic number",
  https://arxiv.org/abs/2608.06254 (math.CO, math.GR), HTML https://arxiv.org/html/2608.06254 `[V]`.
- Statement: Babai 1978 asked whether Cayley graphs Cay(G,S) with S a minimal generating set have
  bounded chromatic number `[V]`.
- Object: Theorem 1, for every k a finite group G with a minimal generating set S of involutions
  and chi(Cay(G,S)) >= k. Inductive, deterministic construction (Tutte-style plus Hales-Jewett);
  group order grows doubly exponentially; no explicit small example beyond order 2 `[S]`.
- Verification: proof only; no computation `[S]`.
- AI: parts of Section 2 drafted with ChatGPT 5.6 Sol, edited by the authors `[S]`.
- Explicit follow-ups: Conjecture 1 (large girth and chromatic number simultaneously), Conjecture 2
  (m-minimal variant), Conjecture 3 (Babai 1995, independence ratio). Not stated but open: the
  smallest minimal Cayley graph with chi = 4 (or 5) `[S]`.
- Prior work to read before claiming novelty: the same authors' "Counterexample to Babai's lonely
  colour conjecture", https://arxiv.org/abs/2410.05199 `[U]`; whether a chi = 4 minimal Cayley graph
  is already in the literature is UNVERIFIED.

### 2.4 Purely-prime ideals (index 2026-08-14)

- Primary: Tarizadeh, "A counterexample to a question on the maximality of purely-primes",
  https://arxiv.org/abs/2608.14251 (math.AC, math.RA), HTML https://arxiv.org/html/2608.14251 `[V]`.
- Statement: Conjecture 5.8 of Tarizadeh-Aghajani, Comm. Algebra 49 (2021), that every purely-prime
  ideal of a commutative ring is purely-maximal `[S]`.
- Object: R = k[X1, X2, ...]/(Xi(1 - Xj) : i < j), k a domain; the only pure ideals are 0, I = (x_i),
  and R, so 0 is purely-prime but not purely-maximal. Countably generated, infinite `[S]`.
- Verification: hand proof through separating homomorphisms to k and k[t] `[S]`. AI: ChatGPT via
  Brian Conrad `[S]`.
- Follow-ups stated: Conjecture 2.6 (pdim R <= dim R) and Conjecture 2.7 (pure dimension finite).
  In Noetherian rings purely-prime ideals are purely-maximal, so no finite/Noetherian counterexample
  exists `[S]`.

### 2.5 HRT conjecture (index 2026-08-05)

- Primary: Faulhuber, Petersen, van Velthoven, Voigtlaender, "Linear dependence of time-frequency
  shifts of a Schwartz function", https://arxiv.org/abs/2608.05044 (math.FA, math.CA) `[V]`.
- Statement: Heil-Ramanathan-Topiwala 1996, finitely many time-frequency shifts of a nonzero
  L^2 function are linearly independent `[V]`.
- Object: 12 time-frequency shifts of a Schwartz function `[V]`.
- Verification: an analytical proof and a certified numerical proof; Python code in the ancillary
  files `[V]`. Exact arithmetic: no (interval/certified numerics). AI: none stated `[V]`.
- Follow-ups: none stated. Open by inspection: the minimal number of shifts (HRT is known for <= 3
  points and for (2,2) configurations, https://arxiv.org/abs/1006.0735 `[U]`), and whether a
  compactly supported or Gaussian window can be dependent.

### 2.6 "Deligne-Mumford / group-scheme of order 4" (not in the index)

- What the brief refers to is the Grothendieck (SGA 3) question whether every finite locally free
  group scheme of order n is killed by n; Deligne proved the commutative case. Xena blog 2026-07-20
  reports a counterexample of order 4 not killed by 4, found by GPT-5.6 Sol on a prompt from
  Akhil Mathew and auto-formalized in Lean by Claude in four hours (1,076 lines) `[V]` (blog).
- Primary artefact: mathlib4 PR #41748 "A finite free group scheme of order four not killed by
  four", merged 2026-08-03, https://github.com/leanprover-community/mathlib4/pull/41748 `[V]`.
  Base ring R = Z[a,b]/(a^3, b^3, a^2 b + 2); Hopf algebra A = R[U,V]/(U^2 - abU + b^2 V,
  V^2 - a^2 V), free of rank 4; the fourth convolution power sends U to 2bUV, nonzero; the eighth
  power is the unit. AI disclosure per mathlib policy (Codex and Claude under the author's
  direction) `[S]`.
- Manuscript: https://github.com/j2d9w5xtjn-png/GrothendieckRankP2 (file
  A_RANK_FOUR_COUNTEREXAMPLE_TO_GROTHENDIECKS_POWER_QUESTION_2026-07-12.tex) `[U]`; no arXiv id found.
- Follow-ups: reviewers "noted potential for generalization", none pursued in the PR `[S]`. Open by
  inspection: smallest base ring (length, characteristic), whether a base of pure characteristic 2
  works (R above has mixed characteristic through a^2 b = -2), classification of rank-4
  non-commutative group schemes over Artinian rings, and orders 8, 9, p^2.
- Order 4 is the smallest possible order since prime-order group schemes are commutative
  (Tate-Oort) `[U]` (standard; cite Tate-Oort 1970 before use).

### 2.7 Connes's rigidity conjecture (index 2026-08-01)

- Primaries: Zhou, "ICC property (T) groups without W*-superrigidity",
  https://arxiv.org/abs/2608.02327 (math.OA, math.DS, math.GR), HTML
  https://arxiv.org/html/2608.02327v1 `[V]`; OpenAI "ten proofs" repository
  https://github.com/openai/ten-proofs (Lean) `[U]`.
- Object (Zhou): Gamma_i = D_i semidirect (SL_3(F_2[t]) x Sp_4(k)), same D and H, two actions
  differing by a cocycle; L(Gamma_1) = L(Gamma_2) via a Haar-preserving fiber shear; non-isomorphism
  via semisimplicity of D as a Q-module; ICC by Lemmas 5.1-5.3 `[S]`. AI: GPT-5.6 Sol `[V]`.
- Dispute: a PhilArchive note argues the OpenAI Lean construction has non-trivial centres (not ICC),
  https://philarchive.org/archive/NIEWTCv2 `[U]`; Zhou's paper says the OpenAI construction is
  distinguished by torsion, not by centre `[S]`. Status: contested in public, no finite certificate.

### 2.8 Rank-two Poisson conjecture (index 2026-07-23)

- Primaries: Long, "An Explicit Counterexample to the Rank-Two Poisson Conjecture",
  https://arxiv.org/abs/2608.23777 (math.RA, math.AG), HTML https://arxiv.org/html/2608.23777 `[V]`;
  repository https://github.com/octonion/mathematics/tree/main/poisson `[V]`.
- Statement: PC(n), every Poisson endomorphism of C[x_1..x_n, p_1..p_n] with the canonical bracket
  is an automorphism `[V]`.
- Object: R, T, D, S in Q[x,q,p,z]; R = x(2 - 3xq) (degree 3), S (22 terms, degree 11), T (47 terms,
  degree 15), D = D_0 + H with H a degree-23 Hamiltonian correction of 137 terms; the map is a
  Poisson endomorphism with a three-point fibre `[S]`.
- Verification: hand (three coefficient identities) plus SymPy script and a stdlib-only sparse
  script, all over Q `[S]`. AI: ChatGPT 5.6 Sol produced the construction; Claude audits `[S]`.
- Follow-ups: none stated. Built on the three-variable Jacobian counterexample (Mathew and Claude),
  so it is Jacobian-adjacent; PC(n), DC(n) and JC(2n) are stably equivalent (Bavula; Adjamagbo-van
  den Essen) `[U]`. Ownership risk: high.

### 2.9 Kourovka 19.25 and 21.150 (index 2026-07-20)

- Primary: van Doorn, Judin, Monticone, Morrison, "On Some Problems from the Kourovka Notebook",
  https://arxiv.org/abs/2607.17477 (math.GR, math.CO), HTML https://arxiv.org/html/2607.17477 `[V]`;
  Lean files https://github.com/pitmonticone/Kourovka `[V]` (index link). All eight solutions found
  and Lean-verified by Aristotle (Harmonic), reviewed by the Kourovka editors and proposers `[V]`.
- 19.25: is a finite group with the same order and the same totient sum sum_g phi(|g|) as a finite
  simple group itself simple? Counterexample: G = PSU(3,3), |G| = 6048, totient sum 23984, versus
  H = C6 x S4 x (C7 : C6), same order and sum. The partner is not unique (an H' is given). The paper
  says 6048 "appears minimal" without a certified sweep `[S]`.
- 21.150 (statement transcribed from an automated reading; check the PDF): for a p-group with a
  normal elementary abelian A, a subgroup B, and a in A with trivial centralizer in B, is
  rank(Z(H) cap H') <= rank(B) for H = <a, B>? Counterexample: p = 3, A = F_3[x,y]/(x,y)^3 as
  (Z/3)^6, B = <b1, b2> = (Z/3)^2 acting by multiplication operators; rank(Z(H) cap H') = 3 > 2.
  No minimality claim; the construction generalizes to semidirect products with non-pure
  subgroups `[S]`.
- 21.147 (right-relatively convex subgroups do not form a sublattice) is also a counterexample but
  concerns infinite ordered groups `[S]`.

### 2.10 Kourovka 21.142 (index 2026-07-30, "blocking debts")

- Primary: Gong, Zeng, Yang, "Albilich: Steerable Proof-State Orchestration ...",
  https://arxiv.org/abs/2607.27705 (cs.AI), HTML https://arxiv.org/html/2607.27705 `[V]`.
- Claim: for fixed distinct primes p, q, some alternating group A_m (m >= 9) does not embed in a
  finite group invariably generated by elements of orders p and q; structural obstruction, 10 of 11
  claims verified, "residual ledger debts remain" `[S]`. No explicit object. Not usable.

## 3. Items added from the arXiv listing sweep (not in the index)

Group theory and algebra:

- Kourovka 16.11, 17.32, 17.47, 19.94 and others: Ionin, Semidetnov, "On Some More Problems from the
  Kourovka Notebook", https://arxiv.org/abs/2608.29219, HTML https://arxiv.org/html/2608.29219 `[V]`.
  16.11 answered negatively by SmallGroup(256,511), whose derived subgroup is the Hall-Senior group
  32/40; GAP with SmallGrp 1.5.4 and SONATA 2.9.7; LLMs (ChatGPT 5.6 Sol, Claude Opus 5) supplied
  strategies, authors verified `[S]`. No minimality claim.
- Kourovka 21.88: Beyer de Ryke, https://arxiv.org/abs/2608.03003: no group of odd order has
  commuting probability 1/17; p = 97 is the next unresolved prime `[V]`.
- Kourovka 17.102: Wan, https://arxiv.org/abs/2608.00504, infinite groups, separability `[V]`.
- Zassenhaus ZC2/ZC3: Verbeken, "Cyclic-by-abelian counterexamples ...",
  https://arxiv.org/abs/2608.03254, HTML https://arxiv.org/html/2608.03254 `[V]`. G_r =
  (C5 x C3 x C_r) : W, |W| = 32, gcd(r,30) = 1, |G_r| = 480 r, smallest r = 7 gives order 3360;
  "no absolute minimality assertion is made"; no CAS reported; answers Margolis-del Rio negatively `[S]`.
- Polycirculant conjecture: Freedman, Lee, https://arxiv.org/abs/2607.23423, elusive 2-closed group
  7^6.PSU_3(3) on 16,464 points, infinite family `[V]`.
- Byott's conjecture (skew braces): Di Matteo, Ferrara, Trombetti, https://arxiv.org/abs/2607.22795,
  soluble additive group with insoluble multiplicative group (quotient PSL_2(7)); order not in the
  abstract `[V]`.
- Wehlau's conjectures on Noether numbers: Anwar, https://arxiv.org/abs/2607.18585 (D8 in
  characteristic 2, 6-dim V with 5-dim U, beta(k[U]^G) = 6 > 5) and norm conjectures
  https://arxiv.org/abs/2607.23857 (C2^3, C2^4 over F_8, 4-dim faithful) `[V]`.
- Saxl-graph common-neighbour conjectures: Rizzoli, Thomas, https://arxiv.org/abs/2609.01367,
  infinitely many primitive groups at every base size `[V]`.
- Han's conjecture: Kong, Liu, Shen, https://arxiv.org/abs/2608.00177 (round-1 L1) `[V]`.
- Snashall-Solberg, symmetric case: Wang, Zhou, https://arxiv.org/abs/2608.17706, trivial
  extension of the Xu-Snashall algebra (quiver with 2 vertices, arrows a, b, c, relations
  a^2, b^2, ab - ba, ac); method suggested by the AI assistant Kimi `[S]`.
- Radical equality in primitive axial algebras: Peng, https://arxiv.org/abs/2608.28653,
  2-dimensional algebra a^2 = a, ab = 2b, b^2 = b; fully closed `[V]`.
- Kalck's global-dimension bound: Kong, Liu, Shen, https://arxiv.org/abs/2608.23981, 13-dim
  radical-square-zero algebra with gldim 4 `[V]`.

Commutative algebra and algebraic geometry:

- Peskine-Szpiro dimension inequality, strong intersection and grade conjectures: Ma,
  https://arxiv.org/abs/2608.24018 `[V]` (objects not in the abstract).
- F-injectivity does not deform: Schwede, Simpson, https://arxiv.org/abs/2608.15470, 4-dim local
  domain in characteristic 2 `[V]`.
- Weibel's conjecture: Kelly, https://arxiv.org/abs/2608.16066, dim-1 rings with K_{-d} nonzero `[V]`.
- Period-index conjecture false: Perry, https://arxiv.org/abs/2608.03684; hyperkaehler version:
  Belmans, Hotchkiss, https://arxiv.org/abs/2608.09436 `[V]`.
- Batyrev stringy Hodge non-negativity: Satriano, Usatine, https://arxiv.org/abs/2607.19184 `[V]`.
- Ulrich existence (Eisenbud-Schreyer-Weyman): Anghel, https://arxiv.org/abs/2609.02718 `[V]`.
- AB rings localization: Lyle, Nasseh, https://arxiv.org/abs/2609.00754 (round-1 L2) `[V]`.

Combinatorics:

- Petersen coloring conjecture: Putman, "A 112-Vertex Counterexample ...",
  https://arxiv.org/abs/2608.10012, HTML https://arxiv.org/html/2608.10012 `[V]`. Bridgeless cubic,
  112 vertices, 168 edges, built from Petersen 4-poles F (4 per 36-vertex block L) and claw 6-poles;
  two CNF encodings (about 3,640 variables, 68,324 clauses), CaDiCaL 3.0.1 UNSAT, DRAT checked by
  drat-trim; artefacts at Zenodo https://doi.org/10.5281/zenodo.21845291; a second D3-symmetric
  112-vertex example; "we do not address whether 112 is minimum"; infinitely many via Ma, Mattiolo,
  Steffen, Wolf `[S]`.
- Zero forcing versus independence (TxGraffiti 2017): Fischer, https://arxiv.org/abs/2607.23664,
  subcubic 24 vertices (alpha 9, Z 11) and cubic 36 vertices (alpha 15, Z 17); standalone Python
  verifier and graph6 files; minimality open `[V]`.
- Mizzi's unstable-graph conjecture: Srivastava, https://arxiv.org/abs/2608.15281, 10 vertices,
  exact dependency-free verifier `[V]`.
- Henning-Yeo identifying vertex cover bound: Wang, https://arxiv.org/abs/2608.19455, two-parameter
  family, evaluators shipped, minimal counterexample open `[V]`.
- Albertson-Berman: Cames van Batenburg, Goedgebeur, Jooken, https://arxiv.org/abs/2608.23260,
  minimum order 29 certified, 41-vertex 4-connected example; minimality already done `[V]`.
- Bougard-Joret: Das, Gupta, https://arxiv.org/abs/2608.18828 (round-1 L3) `[V]`.
- Stanley-Gasharov (claw-free Schur positivity): Wang, Zhang, Zhao, https://arxiv.org/abs/2607.27166,
  12-vertex line graph and 13-vertex non-line graph, two infinite families `[V]`.
- Hoa's maximal non-Hamiltonian conjecture: Zhan, https://arxiv.org/abs/2608.00957 (round-1 L4) `[V]`.
- Tree Product Conjecture: Munaro, https://arxiv.org/abs/2608.04659 (d >= 2) `[V]`.
- Target Ramsey numbers: Lecomte, https://arxiv.org/abs/2608.06446 `[V]`.
- Minimum period conjecture (Beck-Sam-Woods 2008): Liu, Tang, Xin, Zhang,
  https://arxiv.org/abs/2608.02085 `[V]`.
- Erdos-Gyarfas: Tranquilli, https://arxiv.org/abs/2608.02675, certified 60-vertex lower bound for
  cubic bipartite counterexamples (not a disproof; a bounded-search exemplar) `[V]`.
- Umans-Wang divisor covers: He, Sahai, https://arxiv.org/abs/2608.06681 (math.NT), proof-based `[V]`.

Analysis (outside the exact-arithmetic remit, listed for completeness):

- Schiffer / Pompeiu: Cao-Labora, de Dios Pont, https://arxiv.org/abs/2608.05114 `[V]`.
- Inverse generator problem: Lorist, Meyries, Veraar, https://arxiv.org/abs/2608.06272 (Lean 4
  certificate added in v3) `[V]`.
- Sra, count-ex-machina, https://arxiv.org/abs/2608.29595, repository
  https://github.com/suvrit/count-ex-machina (round-1 L6) `[V]`.

## 4. Radar scores

Criteria in order: EV exact verifier, BS bounded search, CL construction language, IR independent
route, AC adversarial controls, SC source completeness, NW novelty window, CF compute fit (commodity
CPU, exact arithmetic, Python/Singular/GAP/SAT), XV extension value. Max 18. Scores are for the
EXTENSION we would run, not for the paper.

| rank | item | EV | BS | CL | IR | AC | SC | NW | CF | XV | total | zero in first four |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Babai minimal Cayley: smallest chi >= 4 example (2608.06254) | 2 | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 17 | no |
| 2 | Petersen coloring: minimal counterexample and gadget family (2608.10012) | 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 17 | no |
| 3 | Kourovka 21.150: minimal p-group example and p = 2 (2607.17477) | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 1 | 17 | no |
| 4 | Carlson depth: sweep of orders 64 and 128 (2607.23732) | 2 | 2 | 1 | 2 | 2 | 2 | 2 | 1 | 2 | 16 | no |
| 5 | Grothendieck order-4 group scheme: minimal base ring (mathlib #41748) | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 2 | 2 | 15 | no |
| 6 | Zero forcing vs independence: minimal cubic/subcubic (2607.23664) | 2 | 2 | 1 | 1 | 2 | 2 | 2 | 2 | 1 | 15 | no |
| 7 | Dere real forms: dimension 9 and three-step (2607.19513) | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 1 | 2 | 14 | no |
| 8 | Kourovka 16.11: minimal order for derived subgroup 32/40 (2608.29219) | 2 | 2 | 1 | 1 | 2 | 1 | 2 | 2 | 1 | 14 | no |
| 9 | Kourovka 19.25: certify 6048 minimal (2607.17477) | 2 | 1 | 1 | 2 | 2 | 2 | 1 | 1 | 1 | 13 | no |
| 10 | Henning-Yeo: minimal counterexample (2608.19455) | 2 | 1 | 2 | 1 | 1 | 2 | 1 | 2 | 1 | 13 | no |
| 11 | Zassenhaus ZC2/ZC3 cyclic-by-abelian: minimal order (2608.03254) | 1 | 1 | 2 | 1 | 1 | 2 | 2 | 1 | 2 | 13 | no |
| 12 | Bougard-Joret: corrected f(n,alpha,k) in n <= k alpha (2608.18828, L3) | 2 | 1 | 1 | 1 | 2 | 2 | 1 | 2 | 1 | 13 | no |
| 13 | Unstable graphs: certify 10 minimal (2608.15281) | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 2 | 0 | 13 | no |
| 14 | AB rings localization: minimal embedding dimension (2609.00754, L2) | 2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 2 | 12 | no |
| 15 | HRT: fewer than 12 shifts (2608.05044) | 1 | 0 | 1 | 2 | 1 | 2 | 2 | 1 | 2 | 12 | yes (BS) |
| 16 | Wehlau Noether numbers: minimal dimension (2607.18585) | 2 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 12 | no |
| 17 | Byott skew braces: minimal order (2607.22795) | 2 | 1 | 1 | 1 | 1 | 1 | 2 | 1 | 2 | 12 | no |
| 18 | Erdos-Gyarfas cubic bipartite: extend the 60 bound (2608.02675) | 2 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 0 | 12 | no |
| 19 | Rank-two Poisson: minimal degree, PC(1) (2608.23777) | 2 | 0 | 1 | 2 | 1 | 2 | 0 | 2 | 1 | 11 | yes (BS); Jacobian-adjacent |
| 20 | Stanley-Gasharov: certify 12/13 minimal (2607.27166) | 2 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 11 | no |
| 21 | Polycirculant: smallest elusive 2-closed group (2607.23423) | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 0 | 2 | 11 | no |
| 22 | Hoa MNH graphs: smallest order (2608.00957, L4) | 2 | 1 | 1 | 1 | 1 | 2 | 2 | 0 | 1 | 11 | no |
| 23 | Snashall-Solberg symmetric: smaller symmetric example (2608.17706) | 1 | 0 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 10 | yes (BS) |
| 24 | Kourovka 21.88: cp(G) = 1/97 (2608.03003) | 1 | 1 | 0 | 1 | 0 | 2 | 2 | 1 | 1 | 9 | yes (CL) |
| 25 | Han's conjecture: explicit small algebra (2608.00177, L1) | 1 | 0 | 0 | 1 | 0 | 2 | 2 | 0 | 2 | 8 | yes |
| 26 | Purely-prime ideals (2608.14251) | 0 | 0 | 1 | 1 | 0 | 2 | 1 | 0 | 1 | 6 | yes |
| 27 | Connes rigidity (2608.02327, ten-proofs) | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 5 | yes; contested |
| 28 | Kourovka 21.142 (2607.27705) | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 0 | 1 | 3 | yes; unverified |

Not scored (proof-theoretic, no finite exact surface, or fully closed): Peskine-Szpiro, F-injectivity,
Weibel, period-index (both), Batyrev, Ulrich, Saxl graphs, Kourovka 17.102 and 21.147, tree product,
target Ramsey, minimum period, Umans-Wang, Schiffer, inverse generator, Kalck bound, axial algebras
(closed: 2-dim, unique), Albertson-Berman (minimality already certified), Sra items (analysis).

## 5. Excluded by ownership (for the audit trail)

Jacobian in dim > 2 https://arxiv.org/abs/2608.00222; separable Jacobian char 2
https://arxiv.org/abs/2608.02634 and https://arxiv.org/abs/2607.20968; Hessian five variables
https://arxiv.org/abs/2607.22198; weak Markus-Yamabe dim 14 https://arxiv.org/abs/2608.05392
(built from Jacobian counterexamples); Gaussian moments https://arxiv.org/abs/2607.18186; xz and
Mathieu for SU(2) https://arxiv.org/abs/2607.19012; generalized vanishing five variables
https://arxiv.org/abs/2608.07338; Mathieu for compact Lie groups
https://github.com/octonion/mathematics/blob/main/mc/; withdrawn C^5 injectivity claim
https://arxiv.org/abs/2607.20049. The rank-two Poisson item (2.8) is kept in the table but flagged
Jacobian-adjacent; it should be offered to the Jacobian session, not opened here.

## 6. Shortlist (five) and the first experiment for each

### S1. Babai minimal Cayley graphs: the smallest minimal Cayley graph with chromatic number 4

Hypothesis to commit: every Cayley graph Cay(G,S) with S a minimal generating set and |G| <= N_0
is 3-colourable, for an N_0 to be found, and the first failure is a specific (G, S) that we can
name. First experiment: in GAP (WSL, install `gap` with SmallGrp), for every group of order <= 64
(and then <= 128 minus order 128 itself, then 128), enumerate minimal generating sets up to
Aut(G) (both the all-involution case of Theorem 1 and the general inverse-closed case), build the
Cayley graph, and decide chi <= 3 exactly by SAT (cadical, DRAT checked by drat-trim for UNSAT, a
colouring checked by a 20-line verifier for SAT). Controls: a non-minimal S = G minus 1 yields K_n
(chi = n); a deliberately corrupted encoder (drop one edge clause) must flip a known non-3-colourable
instance to SAT. Independent route: a plain backtracking colourer on the same graph6 files. The
day-1 deliverable is the table order x max chi, with the smallest chi = 4 instance as an explicit
(group id, generating set). Before any claim: read Babai 1978 and the authors' 2410.05199 for known
small examples `[U]`. Sources: https://arxiv.org/abs/2608.06254.

### S2. Petersen coloring conjecture: a smaller counterexample inside the gadget grammar

Hypothesis: within the grammar {Petersen 4-poles F, claw 6-poles C, and the two joining rules of
2608.10012}, 112 is the minimum order of a non-Petersen-colourable cubic graph; and outside the
grammar, every bridgeless cubic graph on <= 36 vertices is Petersen-colourable (UNVERIFIED whether
this is already a published check; establish first). First experiment: reproduce the 112-vertex
UNSAT from the Zenodo artefacts with the WSL cadical and the shared drat-trim binary (round-trip
time and proof size logged); re-implement the normal-5-edge-colouring CNF independently (second
encoding, different variable scheme); then enumerate all compositions of the grammar with fewer
than three L-blocks or fewer than four F-poles per block, running both encodings on each. Controls:
the Petersen graph itself (SAT), the 112-vertex graph (UNSAT), and a corrupted graph (one edge
removed) that must become SAT or break cubicity. Extension value: the first certified minimality
statement inside the grammar and the exact border where Ma-Mattiolo-Steffen-Wolf families start.
Sources: https://arxiv.org/abs/2608.10012, https://doi.org/10.5281/zenodo.21845291.

### S3. Kourovka 21.150: the minimal counterexample and the p = 2 case

Hypothesis: with A = F_p[x,y]/(x,y)^k acted on by multiplication operators, the 3-group of order 3^8
from 2607.17477 is the smallest counterexample in that family, and no counterexample exists with
p = 2 and rank(A) <= 6. First experiment: GAP script that, for p in {2,3,5} and rank(A) <= 8,
enumerates elementary abelian B <= GL(A) of rank <= 3 (up to conjugacy, using the polynomial-ring
normal form as the construction language and random elementary abelian subgroups as a second,
implementation-diverse route), picks a in A with trivial centralizer in B, forms H = <a, B>, and
records rank(Z(H) cap H') against rank(B). Independent route: the Lean statement in
https://github.com/pitmonticone/Kourovka gives the exact hypothesis to encode; recompute the
published example first (must return 3 > 2) and a Duflot-style positive control (abelian B acting
trivially returns rank 0). The transcription of the 21.150 statement in this dossier is `[S]` and
must be corrected from the PDF before coding. Bundle: the same sweep infrastructure certifies
Kourovka 16.11 minimality (derived subgroups of all 2328 groups of order 128 against 32/40) in one
run. Sources: https://arxiv.org/abs/2607.17477, https://arxiv.org/abs/2608.29219.

### S4. Carlson depth conjecture: is 128 the minimal order, and how many counterexamples at 128

Hypothesis: no group of order 64 violates Carlson's Question 3.1 (so SmallGroup(128,859) is a
smallest 2-group counterexample), and the set of counterexamples among the 2328 groups of order
128 is a short explicit list with a common centralizer mechanism (exceptional centralizers of
centre rank 2 with depth >= 3, as in the paper). First experiment: obtain the Green-King mod-2
cohomology ring presentations (verify the download exists; fallback is HAP in GAP for order 64,
which is slow but exact), then for each group compute depth by colon-ideal certificates in Singular
(the paper's certificate shape) and the minimum associated-prime dimension by Okuyama's criterion
over rank-r elementary abelian subgroups and their centralizers in GAP. Controls: SmallGroup(128,859)
must reproduce depth 2 with no dimension-2 associated prime; SmallGroup(128,858) is the paper's
negative control; corrupt a colon-ideal certificate and confirm the checker rejects it. Compute:
Singular Groebner bases over F_2 in 4 to 8 variables are commodity; the sweep is resumable per
group id. Sources: https://arxiv.org/abs/2607.23732, Green-King catalogue `[U]`.

### S5. Grothendieck's order-4 question: the smallest base ring

Hypothesis: there is a rank-4 non-commutative group scheme not killed by 4 over an Artinian ring of
smaller length than R = Z[a,b]/(a^3, b^3, a^2 b + 2), and possibly over a base of pure
characteristic 2; conversely, over any base where the relevant coefficients vanish the scheme is
killed by 4. First experiment: implement the Hopf algebra A = R[U,V]/(U^2 - abU + b^2 V,
V^2 - a^2 V) with its comultiplication in Python (exact polynomial arithmetic modulo the base
relations, or Singular over Z with the quotient), reproduce "[4]U = 2bUV, nonzero" and "[8] = unit"
(positive control against the merged Lean proof), then parametrize the family
U^2 - alpha U + beta V, V^2 - gamma V with alpha, beta, gamma ranging over monomials of small
Artinian rings Z[a,b]/I of length <= L, keeping only those for which the coassociative Hopf
structure closes (a finite exact check), and record the first n with [n] = unit. Controls:
commutative specialisations must be killed by 4 (Deligne); a corrupted comultiplication must fail
coassociativity. Priority: read the author's manuscript repository
https://github.com/j2d9w5xtjn-png/GrothendieckRankP2 first, since "generalization" was raised in
review and may already be in progress `[U]`. Sources:
https://github.com/leanprover-community/mathlib4/pull/41748,
https://xenaproject.wordpress.com/2026/07/20/human-mathematicians-are-being-outcounterexampled/.

Reserve: S6 zero forcing versus independence (2607.23664), an exhaustive geng sweep of connected
cubic graphs to 24 vertices for Z = alpha + 2, cheap and fully exact, if any of S1 to S5 stalls on
tooling (GAP or Green-King data).

## 7. Gaps to close before the plan

- Full title scan of math.CO 2026-07 (after 07-15) and 2026-08 listings; the fetcher returned only
  the first page of each `[U]`.
- PDF reads of 2607.23732 (software list, certificate format), 2607.17477 (exact 21.150 statement),
  2608.06254 (whether any small chi = 4 example is discussed), 2608.10012 (whether smaller orders
  were tested), and the mathlib PR diff (exact Lean statement).
- Prior-art checks: Babai 1978 ("Chromatic number and subgraphs of Cayley graphs"), Green-King
  catalogue availability, published Petersen-colouring verification bounds for small cubic graphs.
